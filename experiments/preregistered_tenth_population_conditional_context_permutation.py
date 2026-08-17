"""Experiment 144: preregistered tenth-population conditional-context permutation.

Frozen before seeds 44391-44430 are generated. Tests whether correct row-level
context pairing adds ranking value beyond action identity, seed environment, and
marginal context distributions.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN = Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST = Path("results/prospective_action_conditioned_support_representation_actions_391_430.csv")
OUT = Path("results/preregistered_tenth_population_conditional_context_permutation.csv")
TRIALS = Path("results/preregistered_tenth_population_conditional_context_permutation_trials.csv")
FEATURES = ["action_2", "action_3", "context_support_distance"]
SOURCE_UNSAFE_RECALL_TARGET = 0.80
N_PERM = 5000
RNG_SEED = 14444430


def prep(path):
    d = pd.read_csv(path)
    d["action_2"] = (d.action.astype(int) == 2).astype(int)
    d["action_3"] = (d.action.astype(int) == 3).astype(int)
    d["unsafe_action"] = d.unsafe_action.astype(int)
    return d.dropna(subset=FEATURES + ["unsafe_action", "generation_seed", "action"]).copy()


def fit_source(tr):
    m = make_pipeline(
        StandardScaler(),
        LogisticRegression(class_weight="balanced", max_iter=5000, random_state=RNG_SEED),
    )
    m.fit(tr[FEATURES], tr.unsafe_action.to_numpy())
    return m


def top_n_alert(scores, n):
    z = np.zeros(len(scores), dtype=np.int8)
    if n <= 0:
        return z
    idx = np.argpartition(scores, -n)[-n:]
    z[idx] = 1
    return z


def main():
    tr, te = prep(TRAIN), prep(TEST)
    ytr = tr.unsafe_action.to_numpy()
    y = te.unsafe_action.to_numpy()
    model = fit_source(tr)

    source_scores = model.predict_proba(tr[FEATURES])[:, 1]
    source_unsafe_scores = np.sort(source_scores[ytr == 1])
    source_threshold = float(source_unsafe_scores[max(0, int(np.floor((1 - SOURCE_UNSAFE_RECALL_TARGET) * len(source_unsafe_scores))))])
    frozen_coverage = float(np.mean(source_scores >= source_threshold))
    target_n = int(round(frozen_coverage * len(te)))

    primary_scores = model.predict_proba(te[FEATURES])[:, 1]
    primary_alert = top_n_alert(primary_scores, target_n)
    primary_tp = int(np.sum((primary_alert == 1) & (y == 1)))

    context = te.context_support_distance.to_numpy(dtype=float)
    action2 = te.action_2.to_numpy(dtype=float)
    action3 = te.action_3.to_numpy(dtype=float)

    scaler = model.named_steps["standardscaler"]
    clf = model.named_steps["logisticregression"]
    means = scaler.mean_
    scales = scaler.scale_
    coef = clf.coef_[0]
    intercept = float(clf.intercept_[0])

    base_action_logit = (
        ((action2 - means[0]) / scales[0]) * coef[0]
        + ((action3 - means[1]) / scales[1]) * coef[1]
        + intercept
    )
    context_multiplier = coef[2] / scales[2]
    context_offset = -(means[2] / scales[2]) * coef[2]

    groups = [g.index.to_numpy(dtype=int) for _, g in te.reset_index(drop=True).groupby(["generation_seed", "action"], sort=True)]
    rng = np.random.default_rng(RNG_SEED)
    trial_tp = np.empty(N_PERM, dtype=int)

    for i in range(N_PERM):
        perm_context = context.copy()
        for idx in groups:
            perm_context[idx] = rng.permutation(context[idx])
        logits = base_action_logit + context_multiplier * perm_context + context_offset
        alert = top_n_alert(logits, target_n)
        trial_tp[i] = int(np.sum((alert == 1) & (y == 1)))

    p99 = float(np.percentile(trial_tp, 99))
    p975 = float(np.percentile(trial_tp, 97.5))
    empirical_ge = float(np.mean(trial_tp >= primary_tp))
    unsafe_total = int(y.sum())
    safe_total = int(len(y) - unsafe_total)
    primary_fp = int(primary_alert.sum() - primary_tp)
    primary_fn = unsafe_total - primary_tp
    primary_tn = safe_total - primary_fp

    out = {
        "test_rows": len(te),
        "test_unsafe": unsafe_total,
        "test_prevalence": float(y.mean()),
        "frozen_source_coverage": frozen_coverage,
        "target_alert_count": target_n,
        "primary_true_positives": primary_tp,
        "primary_unsafe_recall": primary_tp / unsafe_total,
        "primary_unsafe_precision": primary_tp / target_n,
        "primary_safe_specificity": primary_tn / safe_total,
        "primary_balanced_accuracy": 0.5 * (primary_tp / unsafe_total + primary_tn / safe_total),
        "permutation_true_positives_mean": float(trial_tp.mean()),
        "permutation_true_positives_ci_2_5": float(np.percentile(trial_tp, 2.5)),
        "permutation_true_positives_ci_97_5": p975,
        "permutation_true_positives_p99": p99,
        "primary_minus_permutation_mean_true_positives": float(primary_tp - trial_tp.mean()),
        "probability_permutation_ge_primary": empirical_ge,
        "criterion_primary_above_permutation_p99": int(primary_tp > p99),
    }
    out["primary_criterion_pass"] = out["criterion_primary_above_permutation_p99"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([out]).to_csv(OUT, index=False)
    pd.DataFrame({"trial": np.arange(1, N_PERM + 1), "true_positives": trial_tp}).to_csv(TRIALS, index=False)
    print(pd.DataFrame([out]).to_string(index=False))


if __name__ == "__main__":
    main()
