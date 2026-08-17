"""Experiment 142: preregistered ninth-population incremental-context ablation.

Frozen before seeds 44351-44390 are generated. Compares a source-trained action-only
logistic model with an action+context model at identical unlabeled target coverage.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN = Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST = Path("results/prospective_action_conditioned_support_representation_actions_351_390.csv")
OUT = Path("results/preregistered_ninth_population_incremental_context.csv")
SEED_OUT = Path("results/preregistered_ninth_population_incremental_context_by_seed.csv")
BOOT_OUT = Path("results/preregistered_ninth_population_incremental_context_bootstrap.csv")
ACTION_FEATURES = ["action_2", "action_3"]
CONTEXT_FEATURES = ["action_2", "action_3", "context_support_distance"]
SOURCE_UNSAFE_RECALL_TARGET = 0.80
N_BOOT = 10000
RNG_SEED = 14244390


def prep(path):
    d = pd.read_csv(path)
    d["action_2"] = (d.action.astype(int) == 2).astype(int)
    d["action_3"] = (d.action.astype(int) == 3).astype(int)
    d["unsafe_action"] = d.unsafe_action.astype(int)
    return d.dropna(subset=CONTEXT_FEATURES + ["unsafe_action", "seed"]).copy()


def fit(features, tr):
    m = make_pipeline(
        StandardScaler(),
        LogisticRegression(class_weight="balanced", max_iter=5000, random_state=RNG_SEED),
    )
    m.fit(tr[features], tr.unsafe_action.to_numpy())
    return m


def metrics(y, z):
    tn, fp, fn, tp = confusion_matrix(y, z, labels=[0, 1]).ravel()
    return {
        "unsafe_recall": tp / (tp + fn),
        "unsafe_precision": tp / (tp + fp),
        "safe_specificity": tn / (tn + fp),
        "balanced_accuracy": 0.5 * (tp / (tp + fn) + tn / (tn + fp)),
        "true_positives": int(tp),
        "alert_coverage": float(np.mean(z)),
    }


def fixed_coverage_alert(scores, coverage):
    threshold = float(np.quantile(scores, 1 - coverage, method="higher"))
    z = (scores >= threshold).astype(int)
    # Deterministically trim ties if needed so both models have the same alert count.
    target_n = int(round(coverage * len(scores)))
    idx = np.flatnonzero(z == 1)
    if len(idx) > target_n:
        order = idx[np.argsort(-scores[idx], kind="stable")]
        z[:] = 0
        z[order[:target_n]] = 1
    return z, threshold


def main():
    tr, te = prep(TRAIN), prep(TEST)
    ytr = tr.unsafe_action.to_numpy()
    y = te.unsafe_action.to_numpy()

    action_model = fit(ACTION_FEATURES, tr)
    context_model = fit(CONTEXT_FEATURES, tr)
    source_context_scores = context_model.predict_proba(tr[CONTEXT_FEATURES])[:, 1]
    source_unsafe_scores = np.sort(source_context_scores[ytr == 1])
    source_threshold = float(source_unsafe_scores[max(0, int(np.floor((1 - SOURCE_UNSAFE_RECALL_TARGET) * len(source_unsafe_scores))))])
    frozen_coverage = float(np.mean(source_context_scores >= source_threshold))

    action_scores = action_model.predict_proba(te[ACTION_FEATURES])[:, 1]
    context_scores = context_model.predict_proba(te[CONTEXT_FEATURES])[:, 1]
    action_alert, action_threshold = fixed_coverage_alert(action_scores, frozen_coverage)
    context_alert, context_threshold = fixed_coverage_alert(context_scores, frozen_coverage)

    am = metrics(y, action_alert)
    cm = metrics(y, context_alert)
    action_auc = float(roc_auc_score(y, action_scores))
    context_auc = float(roc_auc_score(y, context_scores))

    rows = []
    for seed, g in te.assign(action_alert=action_alert, context_alert=context_alert).groupby("seed"):
        gy = g.unsafe_action.to_numpy()
        aa = g.action_alert.to_numpy()
        ca = g.context_alert.to_numpy()
        rows.append({
            "seed": int(seed),
            "rows": len(g),
            "unsafe_rows": int(gy.sum()),
            "action_true_positives": int(np.sum((aa == 1) & (gy == 1))),
            "context_true_positives": int(np.sum((ca == 1) & (gy == 1))),
            "delta_true_positives": int(np.sum((ca == 1) & (gy == 1)) - np.sum((aa == 1) & (gy == 1))),
        })
    seed_df = pd.DataFrame(rows)

    rng = np.random.default_rng(RNG_SEED)
    deltas = seed_df.delta_true_positives.to_numpy(dtype=float)
    boot = np.array([rng.choice(deltas, size=len(deltas), replace=True).mean() for _ in range(N_BOOT)])
    ci_lo, ci_hi = np.percentile(boot, [2.5, 97.5])

    out = {
        "test_rows": len(te),
        "test_unsafe": int(y.sum()),
        "test_prevalence": float(y.mean()),
        "frozen_source_coverage": frozen_coverage,
        "action_target_threshold": action_threshold,
        "context_target_threshold": context_threshold,
        "action_auc": action_auc,
        "context_auc": context_auc,
        "delta_auc_context_minus_action": context_auc - action_auc,
    }
    for prefix, m in [("action", am), ("context", cm)]:
        out.update({f"{prefix}_{k}": v for k, v in m.items()})
    out["delta_true_positives_context_minus_action"] = cm["true_positives"] - am["true_positives"]
    out["delta_unsafe_recall_context_minus_action"] = cm["unsafe_recall"] - am["unsafe_recall"]
    out["delta_balanced_accuracy_context_minus_action"] = cm["balanced_accuracy"] - am["balanced_accuracy"]
    out["bootstrap_mean_seed_delta_true_positives"] = float(boot.mean())
    out["bootstrap_seed_delta_ci_2_5"] = float(ci_lo)
    out["bootstrap_seed_delta_ci_97_5"] = float(ci_hi)
    out["criterion_context_more_true_positives"] = int(cm["true_positives"] > am["true_positives"])
    out["criterion_context_auc_higher"] = int(context_auc > action_auc)
    out["criterion_seed_bootstrap_ci_above_zero"] = int(ci_lo > 0)
    out["all_primary_criteria_pass"] = int(
        out["criterion_context_more_true_positives"]
        and out["criterion_context_auc_higher"]
        and out["criterion_seed_bootstrap_ci_above_zero"]
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([out]).to_csv(OUT, index=False)
    seed_df.to_csv(SEED_OUT, index=False)
    pd.DataFrame({"bootstrap_mean_seed_delta_true_positives": boot}).to_csv(BOOT_OUT, index=False)
    print(pd.DataFrame([out]).to_string(index=False))


if __name__ == "__main__":
    main()
