"""Experiment 152: preregistered constrained context-tail audit.

The audit budget (164 rows), attack, controls, target seeds, endpoints, and
criteria were frozen before the 44551-44590 target population was observed.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN = Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST = Path("results/prospective_action_conditioned_support_representation_actions_551_590.csv")
OUT = Path("results/preregistered_constrained_context_tail_audit.csv")
TRIALS = Path("results/preregistered_constrained_context_tail_audit_random_trials.csv")
FEATURES = ["action_2", "action_3", "context_support_distance"]
POISON_DOSE = 0.20
AUDIT_N = 164
N_RANDOM = 1000
SOURCE_UNSAFE_RECALL_TARGET = 0.80
RNG_SEED = 15244590


def prep(path):
    d = pd.read_csv(path).copy()
    d["action_2"] = (d.action.astype(int) == 2).astype(int)
    d["action_3"] = (d.action.astype(int) == 3).astype(int)
    d["unsafe_action"] = d.unsafe_action.astype(int)
    needed = FEATURES + ["unsafe_action", "realized_action_regret", "predicted_action_loss", "generation_seed", "test_index", "action"]
    return d.dropna(subset=needed).copy()


def fit_model(d, labels):
    m = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=5000, random_state=RNG_SEED))
    m.fit(d[FEATURES], np.asarray(labels, dtype=int))
    return m


def top_n_flags(scores, n):
    flags = np.zeros(len(scores), dtype=np.int8)
    if n > 0:
        flags[np.argsort(-scores, kind="stable")[:n]] = 1
    return flags


def evaluate(model, te, exclusion_count):
    flags = top_n_flags(model.predict_proba(te[FEATURES])[:, 1], exclusion_count)
    tmp = te.assign(hazard_flag=flags)
    unsafe_selected = 0
    total_regret = 0.0
    contexts = 0
    for _, g in tmp.groupby(["generation_seed", "test_index"], sort=True):
        if len(g) != 3:
            raise ValueError("Expected exactly three candidate actions per context")
        losses = g.predicted_action_loss.to_numpy(float)
        actions = g.action.to_numpy(int)
        excluded = g.hazard_flag.to_numpy(np.int8)
        available = np.flatnonzero(excluded == 0)
        if len(available) == 0:
            available = np.arange(len(g))
        idx = int(min(available.tolist(), key=lambda i: (float(losses[i]), int(actions[i]))))
        unsafe_selected += int(g.unsafe_action.to_numpy(int)[idx])
        total_regret += float(g.realized_action_regret.to_numpy(float)[idx])
        contexts += 1
    return unsafe_selected, total_regret, contexts


def main():
    tr = prep(TRAIN).reset_index(drop=True)
    te = prep(TEST).sort_values(["generation_seed", "test_index", "action"], kind="stable").reset_index(drop=True)
    clean = tr.unsafe_action.to_numpy(int)
    unsafe_idx = np.flatnonzero(clean == 1)
    clean_model = fit_model(tr, clean)
    source_scores = clean_model.predict_proba(tr[FEATURES])[:, 1]
    sorted_unsafe_scores = np.sort(source_scores[clean == 1])
    threshold = float(sorted_unsafe_scores[max(0, int(np.floor((1 - SOURCE_UNSAFE_RECALL_TARGET) * len(sorted_unsafe_scores))))])
    coverage = float(np.mean(source_scores >= threshold))
    exclusion_count = int(round(coverage * len(te)))
    clean_unsafe, clean_regret, contexts = evaluate(clean_model, te, exclusion_count)

    targeted_order = unsafe_idx[np.argsort(-tr.loc[unsafe_idx, "context_support_distance"].to_numpy(), kind="stable")]
    poison_n = max(1, int(round(POISON_DOSE * len(unsafe_idx))))
    poison_idx = targeted_order[:poison_n]
    if poison_n != 328 or AUDIT_N >= poison_n:
        raise ValueError(f"Frozen design expected poison_n=328 and audit_n<{poison_n}; got {poison_n}")
    poisoned = clean.copy(); poisoned[poison_idx] = 0
    poisoned_unsafe, poisoned_regret, _ = evaluate(fit_model(tr, poisoned), te, exclusion_count)

    audit_order = np.argsort(-tr.context_support_distance.to_numpy(float), kind="stable")
    audit_idx = audit_order[:AUDIT_N]
    defended = poisoned.copy(); defended[audit_idx] = clean[audit_idx]
    defended_unsafe, defended_regret, _ = evaluate(fit_model(tr, defended), te, exclusion_count)
    recovered = int(np.intersect1d(audit_idx, poison_idx).size)

    rng = np.random.default_rng(RNG_SEED)
    rand_u = np.empty(N_RANDOM, int); rand_r = np.empty(N_RANDOM, float)
    rows = []
    for trial in range(N_RANDOM):
        idx = rng.choice(len(tr), size=AUDIT_N, replace=False)
        labels = poisoned.copy(); labels[idx] = clean[idx]
        u, r, _ = evaluate(fit_model(tr, labels), te, exclusion_count)
        rand_u[trial] = u; rand_r[trial] = r
        rows.append({"trial": trial + 1, "audit_rows": AUDIT_N, "poison_rows_recovered": int(np.intersect1d(idx, poison_idx).size), "unsafe_selected": u, "total_regret": r})

    result = {
        "source_rows": len(tr), "source_unsafe_rows": len(unsafe_idx), "poison_rows": poison_n, "audit_rows": AUDIT_N,
        "target_contexts": contexts, "target_exclusion_count": exclusion_count,
        "clean_unsafe_selected": clean_unsafe, "clean_total_regret": clean_regret,
        "poisoned_unsafe_selected": poisoned_unsafe, "poisoned_total_regret": poisoned_regret,
        "defended_unsafe_selected": defended_unsafe, "defended_total_regret": defended_regret,
        "defended_poison_rows_recovered": recovered,
        "random_audit_unsafe_p05": float(np.percentile(rand_u, 5)), "random_audit_regret_p05": float(np.percentile(rand_r, 5)),
        "random_audit_unsafe_mean": float(rand_u.mean()), "random_audit_regret_mean": float(rand_r.mean()),
    }
    result["criterion_unsafe_improves_vs_poisoned"] = int(defended_unsafe < poisoned_unsafe)
    result["criterion_regret_improves_vs_poisoned"] = int(defended_regret < poisoned_regret)
    result["criterion_unsafe_beats_random_p05"] = int(defended_unsafe <= result["random_audit_unsafe_p05"])
    result["criterion_regret_beats_random_p05"] = int(defended_regret <= result["random_audit_regret_p05"])
    result["primary_constrained_audit_pass"] = int(all(result[k] for k in ["criterion_unsafe_improves_vs_poisoned", "criterion_regret_improves_vs_poisoned", "criterion_unsafe_beats_random_p05", "criterion_regret_beats_random_p05"]))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([result]).to_csv(OUT, index=False)
    pd.DataFrame(rows).to_csv(TRIALS, index=False)
    print(pd.DataFrame([result]).to_string(index=False))


if __name__ == "__main__":
    main()
