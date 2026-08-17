"""Experiment 151: preregistered context-tail label-audit mitigation.

Frozen after Experiment 150 and before observing Experiment 151 outcomes.
This is an oracle-audit upper-bound experiment, not an operational detector.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN = Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST = Path("results/prospective_action_conditioned_support_representation_actions_511_550.csv")
OUT = Path("results/preregistered_context_tail_label_audit_mitigation.csv")
TRIALS = Path("results/preregistered_context_tail_label_audit_random_trials.csv")
FEATURES = ["action_2", "action_3", "context_support_distance"]
POISON_DOSE = 0.20
AUDIT_FRACTION = 0.20
N_RANDOM = 500
SOURCE_UNSAFE_RECALL_TARGET = 0.80
RNG_SEED = 15144550


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


def choose_index(losses, actions, excluded):
    available = np.flatnonzero(excluded == 0)
    if len(available) == 0:
        available = np.arange(len(losses))
    return int(min(available.tolist(), key=lambda i: (float(losses[i]), int(actions[i]))))


def evaluate(model, te, exclusion_count):
    flags = top_n_flags(model.predict_proba(te[FEATURES])[:, 1], exclusion_count)
    tmp = te.assign(hazard_flag=flags)
    unsafe_selected = 0
    total_regret = 0.0
    contexts = 0
    for _, g in tmp.groupby(["generation_seed", "test_index"], sort=True):
        if len(g) != 3:
            raise ValueError("Expected exactly three candidate actions per context")
        idx = choose_index(g.predicted_action_loss.to_numpy(float), g.action.to_numpy(int), g.hazard_flag.to_numpy(np.int8))
        unsafe_selected += int(g.unsafe_action.to_numpy(int)[idx])
        total_regret += float(g.realized_action_regret.to_numpy(float)[idx])
        contexts += 1
    return {"unsafe_selected": unsafe_selected, "unsafe_rate": unsafe_selected / contexts, "total_regret": total_regret, "mean_regret": total_regret / contexts, "contexts": contexts}


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
    clean_met = evaluate(clean_model, te, exclusion_count)

    # Reproduce Experiment 150's primary targeted attack exactly.
    targeted_order = unsafe_idx[np.argsort(-tr.loc[unsafe_idx, "context_support_distance"].to_numpy(), kind="stable")]
    flip_n = max(1, int(round(POISON_DOSE * len(unsafe_idx))))
    poison_idx = targeted_order[:flip_n]
    poisoned = clean.copy()
    poisoned[poison_idx] = 0
    poisoned_met = evaluate(fit_model(tr, poisoned), te, exclusion_count)

    # Frozen defense: audit top 20% of all source rows by context distance.
    audit_n = max(1, int(round(AUDIT_FRACTION * len(tr))))
    audit_order = np.argsort(-tr.context_support_distance.to_numpy(float), kind="stable")
    audit_idx = audit_order[:audit_n]
    defended = poisoned.copy()
    defended[audit_idx] = clean[audit_idx]
    defended_met = evaluate(fit_model(tr, defended), te, exclusion_count)

    rng = np.random.default_rng(RNG_SEED)
    random_unsafe = np.empty(N_RANDOM, int)
    random_regret = np.empty(N_RANDOM, float)
    trial_rows = []
    for trial in range(N_RANDOM):
        idx = rng.choice(len(tr), size=audit_n, replace=False)
        labels = poisoned.copy()
        labels[idx] = clean[idx]
        met = evaluate(fit_model(tr, labels), te, exclusion_count)
        random_unsafe[trial] = met["unsafe_selected"]
        random_regret[trial] = met["total_regret"]
        trial_rows.append({"trial": trial + 1, "audit_rows": audit_n, "poison_rows_recovered": int(np.intersect1d(idx, poison_idx).size), "unsafe_selected": met["unsafe_selected"], "total_regret": met["total_regret"]})

    row = {
        "source_rows": len(tr), "source_unsafe_rows": len(unsafe_idx), "poison_rows": flip_n, "audit_rows": audit_n,
        "target_contexts": clean_met["contexts"], "target_exclusion_count": exclusion_count,
        "clean_unsafe_selected": clean_met["unsafe_selected"], "clean_total_regret": clean_met["total_regret"],
        "poisoned_unsafe_selected": poisoned_met["unsafe_selected"], "poisoned_total_regret": poisoned_met["total_regret"],
        "defended_unsafe_selected": defended_met["unsafe_selected"], "defended_total_regret": defended_met["total_regret"],
        "defended_poison_rows_recovered": int(np.intersect1d(audit_idx, poison_idx).size),
        "random_audit_unsafe_p05": float(np.percentile(random_unsafe, 5)), "random_audit_regret_p05": float(np.percentile(random_regret, 5)),
        "random_audit_unsafe_mean": float(random_unsafe.mean()), "random_audit_regret_mean": float(random_regret.mean()),
    }
    row["criterion_unsafe_improves_vs_poisoned"] = int(row["defended_unsafe_selected"] < row["poisoned_unsafe_selected"])
    row["criterion_regret_improves_vs_poisoned"] = int(row["defended_total_regret"] < row["poisoned_total_regret"])
    row["criterion_unsafe_beats_random_p05"] = int(row["defended_unsafe_selected"] <= row["random_audit_unsafe_p05"])
    row["criterion_regret_beats_random_p05"] = int(row["defended_total_regret"] <= row["random_audit_regret_p05"])
    row["criterion_unsafe_within_clean_10pct"] = int(row["defended_unsafe_selected"] <= 1.10 * row["clean_unsafe_selected"])
    row["criterion_regret_within_clean_10pct"] = int(row["defended_total_regret"] <= 1.10 * row["clean_total_regret"])
    row["primary_mitigation_criteria_pass"] = int(all(row[k] for k in ["criterion_unsafe_improves_vs_poisoned", "criterion_regret_improves_vs_poisoned", "criterion_unsafe_beats_random_p05", "criterion_regret_beats_random_p05", "criterion_unsafe_within_clean_10pct", "criterion_regret_within_clean_10pct"]))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row]).to_csv(OUT, index=False)
    pd.DataFrame(trial_rows).to_csv(TRIALS, index=False)
    print(pd.DataFrame([row]).to_string(index=False))


if __name__ == "__main__":
    main()
