"""Experiment 123: frozen cross-population transfer of action-harm geometry.

Fit predeclared logistic models on population 071-110 only, then score the
untouched 111-150 population once. No target-population refitting, feature
selection, sign flipping, or threshold optimization is permitted.
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    balanced_accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN_PATH = Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST_PATH = Path("results/prospective_action_conditioned_support_representation_actions_111_150.csv")
OUT_PATH = Path("results/frozen_cross_population_action_harm_transfer.csv")
BOOT_PATH = Path("results/frozen_cross_population_action_harm_transfer_bootstrap.csv")
COEF_PATH = Path("results/frozen_cross_population_action_harm_transfer_coefficients.csv")
N_BOOT = 5000
RNG_SEED = 12344150

MODELS = {
    "context_support_only": ["context_support_distance"],
    "action_support_only": ["action_support_distance"],
    "predicted_loss_only": ["predicted_action_loss"],
    "context_plus_loss": ["context_support_distance", "predicted_action_loss"],
    "context_plus_action_support": ["context_support_distance", "action_support_distance"],
    "context_loss_action_support": [
        "context_support_distance",
        "predicted_action_loss",
        "action_support_distance",
    ],
}


def clean(frame: pd.DataFrame) -> pd.DataFrame:
    required = sorted({c for cols in MODELS.values() for c in cols} | {"unsafe_action"})
    out = frame.dropna(subset=required).copy()
    out["unsafe_action"] = out["unsafe_action"].astype(int)
    return out


def stratified_bootstrap_indices(y: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    safe = np.flatnonzero(y == 0)
    unsafe = np.flatnonzero(y == 1)
    return np.concatenate(
        [rng.choice(safe, safe.size, replace=True), rng.choice(unsafe, unsafe.size, replace=True)]
    )


def percentile(values: list[float], q: float) -> float:
    return float(np.percentile(np.asarray(values, dtype=float), q))


def main() -> None:
    train = clean(pd.read_csv(TRAIN_PATH))
    test = clean(pd.read_csv(TEST_PATH))
    y_train = train["unsafe_action"].to_numpy()
    y_test = test["unsafe_action"].to_numpy()

    if len(np.unique(y_train)) != 2 or len(np.unique(y_test)) != 2:
        raise RuntimeError("Both populations must contain safe and unsafe outcomes")

    fitted = {}
    predictions = {}
    rows = []
    coef_rows = []

    for name, features in MODELS.items():
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(
                class_weight="balanced",
                max_iter=5000,
                solver="lbfgs",
                random_state=RNG_SEED,
            ),
        )
        model.fit(train[features], y_train)
        probability = model.predict_proba(test[features])[:, 1]
        predicted = (probability >= 0.5).astype(int)
        fitted[name] = model
        predictions[name] = probability

        rows.append(
            {
                "model": name,
                "features": "|".join(features),
                "train_rows": len(train),
                "train_unsafe": int(y_train.sum()),
                "test_rows": len(test),
                "test_unsafe": int(y_test.sum()),
                "test_safe": int((y_test == 0).sum()),
                "roc_auc": roc_auc_score(y_test, probability),
                "balanced_accuracy_at_frozen_0_5": balanced_accuracy_score(y_test, predicted),
                "unsafe_recall_at_frozen_0_5": recall_score(y_test, predicted),
                "unsafe_precision_at_frozen_0_5": precision_score(y_test, predicted, zero_division=0),
            }
        )

        lr = model.named_steps["logisticregression"]
        for feature, coefficient in zip(features, lr.coef_[0]):
            coef_rows.append(
                {
                    "model": name,
                    "feature": feature,
                    "standardized_training_coefficient": float(coefficient),
                }
            )
        coef_rows.append(
            {
                "model": name,
                "feature": "intercept",
                "standardized_training_coefficient": float(lr.intercept_[0]),
            }
        )

    rng = np.random.default_rng(RNG_SEED)
    boot = {name: [] for name in MODELS}
    joint = "context_loss_action_support"
    differences = {name: [] for name in MODELS if name != joint}

    for _ in range(N_BOOT):
        idx = stratified_bootstrap_indices(y_test, rng)
        y_b = y_test[idx]
        joint_auc = roc_auc_score(y_b, predictions[joint][idx])
        for name in MODELS:
            auc = roc_auc_score(y_b, predictions[name][idx])
            boot[name].append(float(auc))
            if name != joint:
                differences[name].append(float(joint_auc - auc))

    bootstrap_rows = []
    for name in MODELS:
        values = boot[name]
        bootstrap_rows.append(
            {
                "contrast": name,
                "estimate": roc_auc_score(y_test, predictions[name]),
                "ci_2_5": percentile(values, 2.5),
                "ci_97_5": percentile(values, 97.5),
                "probability_positive": "",
                "bootstrap_samples": N_BOOT,
            }
        )
    for name, values in differences.items():
        bootstrap_rows.append(
            {
                "contrast": f"{joint}_minus_{name}",
                "estimate": roc_auc_score(y_test, predictions[joint])
                - roc_auc_score(y_test, predictions[name]),
                "ci_2_5": percentile(values, 2.5),
                "ci_97_5": percentile(values, 97.5),
                "probability_positive": float(np.mean(np.asarray(values) > 0)),
                "bootstrap_samples": N_BOOT,
            }
        )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT_PATH, index=False)
    pd.DataFrame(bootstrap_rows).to_csv(BOOT_PATH, index=False)
    pd.DataFrame(coef_rows).to_csv(COEF_PATH, index=False)

    print(pd.DataFrame(rows).to_string(index=False))
    print()
    print(pd.DataFrame(bootstrap_rows).to_string(index=False))


if __name__ == "__main__":
    main()
