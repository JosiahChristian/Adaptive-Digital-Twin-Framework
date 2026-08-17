"""Experiment 155: prospective replication of the apparent poisoning boundary effect."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN = Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST = Path("results/prospective_action_conditioned_support_representation_actions_591_630.csv")
OUT = Path("results/prospective_poisoning_boundary_replication.csv")
CONTEXT_OUT = Path("results/prospective_poisoning_boundary_replication_context_changes.csv")
FEATURES = ["action_2", "action_3", "context_support_distance"]
POISON_DOSE = 0.20
SOURCE_UNSAFE_RECALL_TARGET = 0.80
RNG_SEED = 15544630


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


def top_n_mask(scores, n):
    mask = np.zeros(len(scores), dtype=bool)
    if n > 0:
        mask[np.argsort(-scores, kind="stable")[:n]] = True
    return mask


def choose_idx(g, mask_col):
    losses = g.predicted_action_loss.to_numpy(float)
    actions = g.action.to_numpy(int)
    excluded = g[mask_col].to_numpy(bool)
    available = np.flatnonzero(~excluded)
    if len(available) == 0:
        available = np.arange(len(g))
    return int(min(available.tolist(), key=lambda i: (float(losses[i]), int(actions[i]))))


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

    targeted_order = unsafe_idx[np.argsort(-tr.loc[unsafe_idx, "context_support_distance"].to_numpy(), kind="stable")]
    poison_n = max(1, int(round(POISON_DOSE * len(unsafe_idx))))
    poisoned_labels = clean.copy(); poisoned_labels[targeted_order[:poison_n]] = 0
    poisoned_model = fit_model(tr, poisoned_labels)

    clean_scores = clean_model.predict_proba(te[FEATURES])[:, 1]
    poison_scores = poisoned_model.predict_proba(te[FEATURES])[:, 1]
    clean_mask = top_n_mask(clean_scores, exclusion_count)
    poison_mask = top_n_mask(poison_scores, exclusion_count)
    y = te.unsafe_action.to_numpy(int)

    both = clean_mask & poison_mask
    clean_only = clean_mask & ~poison_mask
    poison_only = poison_mask & ~clean_mask
    union = clean_mask | poison_mask

    rows = []
    transitions = {"same":0, "safe_to_unsafe":0, "unsafe_to_safe":0, "unsafe_to_unsafe":0, "safe_to_safe_changed":0}
    clean_regret = poison_regret = 0.0
    clean_unsafe_selected = poison_unsafe_selected = 0
    changed_regret_delta = []
    for (seed, idx), g in te.assign(clean_excluded=clean_mask, poison_excluded=poison_mask).groupby(["generation_seed","test_index"], sort=True):
        ci = choose_idx(g, "clean_excluded")
        pi = choose_idx(g, "poison_excluded")
        ca = int(g.action.to_numpy(int)[ci]); pa = int(g.action.to_numpy(int)[pi])
        cu = int(g.unsafe_action.to_numpy(int)[ci]); pu = int(g.unsafe_action.to_numpy(int)[pi])
        cr = float(g.realized_action_regret.to_numpy(float)[ci]); pr = float(g.realized_action_regret.to_numpy(float)[pi])
        clean_regret += cr; poison_regret += pr
        clean_unsafe_selected += cu; poison_unsafe_selected += pu
        if ca == pa:
            t = "same"
        elif cu == 0 and pu == 1:
            t = "safe_to_unsafe"
        elif cu == 1 and pu == 0:
            t = "unsafe_to_safe"
        elif cu == 1 and pu == 1:
            t = "unsafe_to_unsafe"
        else:
            t = "safe_to_safe_changed"
        transitions[t] += 1
        if ca != pa:
            changed_regret_delta.append(pr-cr)
        rows.append({"generation_seed":seed,"test_index":idx,"clean_action":ca,"poison_action":pa,"clean_unsafe":cu,"poison_unsafe":pu,"clean_regret":cr,"poison_regret":pr,"transition":t})

    summary = {
        "target_rows": len(te), "target_contexts": len(rows), "target_exclusion_count": exclusion_count,
        "clean_unsafe_selected": clean_unsafe_selected, "poison_unsafe_selected": poison_unsafe_selected,
        "clean_total_regret": clean_regret, "poison_total_regret": poison_regret,
        "clean_auc": roc_auc_score(y, clean_scores), "poison_auc": roc_auc_score(y, poison_scores),
        "clean_ap": average_precision_score(y, clean_scores), "poison_ap": average_precision_score(y, poison_scores),
        "topn_jaccard": float(both.sum()/max(1,union.sum())),
        "both_excluded": int(both.sum()), "clean_only_excluded": int(clean_only.sum()), "poison_only_excluded": int(poison_only.sum()),
        "clean_only_unsafe_prevalence": float(y[clean_only].mean()) if clean_only.any() else np.nan,
        "poison_only_unsafe_prevalence": float(y[poison_only].mean()) if poison_only.any() else np.nan,
        "changed_contexts": int(sum(1 for r in rows if r["clean_action"] != r["poison_action"])),
        "mean_poison_minus_clean_regret_on_changed": float(np.mean(changed_regret_delta)) if changed_regret_delta else 0.0,
        **{f"transition_{k}":v for k,v in transitions.items()},
    }
    summary["apparent_poisoning_benefit_replicated"] = int(
        poison_unsafe_selected < clean_unsafe_selected and poison_regret < clean_regret
    )
    summary["replication_classification"] = "replicated" if summary["apparent_poisoning_benefit_replicated"] else "not_replicated"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([summary]).to_csv(OUT, index=False)
    pd.DataFrame(rows).to_csv(CONTEXT_OUT, index=False)
    print(pd.DataFrame([summary]).to_string(index=False))


if __name__ == "__main__":
    main()
