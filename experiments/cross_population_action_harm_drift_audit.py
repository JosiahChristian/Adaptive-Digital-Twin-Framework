"""Experiment 124: diagnose population drift behind failed frozen transfer."""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, pointbiserialr, wasserstein_distance
from sklearn.metrics import roc_auc_score

TRAIN = Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST = Path("results/prospective_action_conditioned_support_representation_actions_111_150.csv")
OUT = Path("results/cross_population_action_harm_drift_audit.csv")
ACTION_OUT = Path("results/cross_population_action_harm_drift_by_action.csv")

FEATURES = [
    "context_support_distance",
    "action_support_distance",
    "action_support_minus_context",
    "predicted_action_loss",
    "predicted_relative_loss",
]


def standardized_shift(a, b):
    pooled = np.sqrt((np.var(a, ddof=1) + np.var(b, ddof=1)) / 2)
    return float((np.mean(b) - np.mean(a)) / pooled) if pooled > 0 else np.nan


def safe_auc(y, x):
    return float(roc_auc_score(y, x)) if len(np.unique(y)) == 2 else np.nan


def main():
    tr = pd.read_csv(TRAIN).dropna(subset=FEATURES + ["unsafe_action", "action"])
    te = pd.read_csv(TEST).dropna(subset=FEATURES + ["unsafe_action", "action"])
    tr["unsafe_action"] = tr["unsafe_action"].astype(int)
    te["unsafe_action"] = te["unsafe_action"].astype(int)

    rows = []
    for feature in FEATURES:
        a = tr[feature].to_numpy()
        b = te[feature].to_numpy()
        ks = ks_2samp(a, b)
        train_corr = pointbiserialr(tr["unsafe_action"], a).statistic
        test_corr = pointbiserialr(te["unsafe_action"], b).statistic
        train_auc = safe_auc(tr["unsafe_action"], a)
        test_auc = safe_auc(te["unsafe_action"], b)
        rows.append({
            "feature": feature,
            "train_mean": np.mean(a),
            "test_mean": np.mean(b),
            "standardized_mean_shift_test_minus_train": standardized_shift(a, b),
            "wasserstein_distance": wasserstein_distance(a, b),
            "ks_statistic": ks.statistic,
            "ks_pvalue": ks.pvalue,
            "train_point_biserial": train_corr,
            "test_point_biserial": test_corr,
            "correlation_sign_reversal": int(np.sign(train_corr) != np.sign(test_corr)),
            "train_univariate_auc": train_auc,
            "test_univariate_auc": test_auc,
            "auc_direction_reversal": int((train_auc - 0.5) * (test_auc - 0.5) < 0),
        })

    action_rows = []
    for population, frame in [("train_071_110", tr), ("test_111_150", te)]:
        for action, group in frame.groupby("action"):
            action_rows.append({
                "population": population,
                "action": int(action),
                "rows": len(group),
                "row_fraction": len(group) / len(frame),
                "unsafe_rows": int(group["unsafe_action"].sum()),
                "unsafe_prevalence": group["unsafe_action"].mean(),
                "mean_realized_regret": group["realized_action_regret"].mean(),
                "mean_predicted_loss": group["predicted_action_loss"].mean(),
                "mean_context_support": group["context_support_distance"].mean(),
                "mean_action_support": group["action_support_distance"].mean(),
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    pd.DataFrame(action_rows).to_csv(ACTION_OUT, index=False)
    print("Train unsafe prevalence:", tr["unsafe_action"].mean())
    print("Test unsafe prevalence:", te["unsafe_action"].mean())
    print(pd.DataFrame(rows).to_string(index=False))
    print(pd.DataFrame(action_rows).to_string(index=False))


if __name__ == "__main__":
    main()
