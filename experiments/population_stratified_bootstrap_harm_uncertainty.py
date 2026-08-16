import csv
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from experiments.broader_controller_state_action_harm_decomposition import (
    BROADER_STATE_FEATURES,
    POPULATION_EARLY,
    POPULATION_LATE,
    early_population,
    late_population,
)

OUTPUT_PATH = Path("results/population_stratified_bootstrap_harm_uncertainty.csv")
PREDICTION_PATH = Path(
    "results/population_stratified_bootstrap_harm_uncertainty_predictions.csv"
)

RANDOM_STATE = 121
BOOTSTRAPS = 5000
ACTION = "action2_indicator"

PREDICTED_RISK_REGRET = [
    "predicted_under_risk",
    "predicted_primary_regret",
    "predicted_expanded_regret",
    "predicted_regret_margin",
]
TEMPORAL_SUPPORT_CONTEXT = [
    "context_anchor_age",
    "context_trigger_score",
    "context_feature_distance",
]

MODEL_SPECS = {
    "full_state_plus_action": BROADER_STATE_FEATURES + [ACTION],
    "full_state_only": BROADER_STATE_FEATURES,
    "action_only": [ACTION],
    "leave_predicted_risk_regret_out": [
        feature
        for feature in BROADER_STATE_FEATURES
        if feature not in PREDICTED_RISK_REGRET
    ]
    + [ACTION],
    "leave_temporal_support_context_out": [
        feature
        for feature in BROADER_STATE_FEATURES
        if feature not in TEMPORAL_SUPPORT_CONTEXT
    ]
    + [ACTION],
}


def matrix(rows, features):
    return np.asarray(
        [[float(row[feature]) for feature in features] for row in rows],
        dtype=float,
    )


def labels(rows):
    return np.asarray([int(row["harmful_target"]) for row in rows], dtype=int)


def classifier():
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    C=1.0,
                    solver="liblinear",
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                    max_iter=5000,
                ),
            ),
        ]
    )


def fit_predictions(training, test):
    y_train = labels(training)
    predictions = {}
    for name, features in MODEL_SPECS.items():
        model = classifier()
        model.fit(matrix(training, features), y_train)
        predictions[name] = model.predict_proba(matrix(test, features))[:, 1]
    return predictions


def stratified_indices(y, rng):
    output = []
    for value in (0, 1):
        indices = np.flatnonzero(y == value)
        output.append(rng.choice(indices, size=len(indices), replace=True))
    combined = np.concatenate(output)
    rng.shuffle(combined)
    return combined


def interval(values):
    values = np.asarray(values, dtype=float)
    return {
        "bootstrap_mean": float(np.mean(values)),
        "bootstrap_std": float(np.std(values, ddof=1)),
        "ci_lower_95": float(np.quantile(values, 0.025)),
        "ci_upper_95": float(np.quantile(values, 0.975)),
    }


def main():
    print("=" * 180)
    print("EXPERIMENT 121 - POPULATION-STRATIFIED BOOTSTRAP HARM UNCERTAINTY")
    print("=" * 180)
    print(f"paired stratified bootstrap replicates={BOOTSTRAPS}")

    all_rows = early_population() + late_population()
    rng = np.random.default_rng(RANDOM_STATE)
    fold_data = {}
    prediction_rows = []

    for held_out in (POPULATION_EARLY, POPULATION_LATE):
        training = [row for row in all_rows if row["population"] != held_out]
        test = [row for row in all_rows if row["population"] == held_out]
        y = labels(test)
        predictions = fit_predictions(training, test)

        observed = {
            name: float(roc_auc_score(y, scores))
            for name, scores in predictions.items()
        }
        distributions = {name: [] for name in MODEL_SPECS}

        for _ in range(BOOTSTRAPS):
            sample = stratified_indices(y, rng)
            for name, scores in predictions.items():
                distributions[name].append(
                    float(roc_auc_score(y[sample], scores[sample]))
                )

        fold_data[held_out] = {
            "observed": observed,
            "distributions": distributions,
        }

        for row, index in zip(test, range(len(test))):
            record = {
                "held_out_population": held_out,
                "generation_seed": row["generation_seed"],
                "test_index": row["test_index"],
                "harmful_target": row["harmful_target"],
                "action": row["action"],
            }
            for name, scores in predictions.items():
                record[f"probability__{name}"] = float(scores[index])
            prediction_rows.append(record)

    output = []

    for held_out, data in fold_data.items():
        full_distribution = np.asarray(
            data["distributions"]["full_state_plus_action"]
        )
        for name in MODEL_SPECS:
            values = np.asarray(data["distributions"][name])
            row = {
                "record_type": "fold_model_interval",
                "held_out_population": held_out,
                "model": name,
                "observed_auc": data["observed"][name],
                **interval(values),
            }
            if name != "full_state_plus_action":
                differences = full_distribution - values
                row.update(
                    {
                        "comparison": f"full_minus_{name}",
                        "observed_auc_difference": (
                            data["observed"]["full_state_plus_action"]
                            - data["observed"][name]
                        ),
                        "difference_mean": float(np.mean(differences)),
                        "difference_ci_lower_95": float(
                            np.quantile(differences, 0.025)
                        ),
                        "difference_ci_upper_95": float(
                            np.quantile(differences, 0.975)
                        ),
                        "probability_full_better": float(
                            np.mean(differences > 0)
                        ),
                    }
                )
            output.append(row)

    populations = (POPULATION_EARLY, POPULATION_LATE)
    for name in MODEL_SPECS:
        fold_mean_distribution = np.mean(
            [
                np.asarray(fold_data[population]["distributions"][name])
                for population in populations
            ],
            axis=0,
        )
        observed_mean = float(
            np.mean(
                [
                    fold_data[population]["observed"][name]
                    for population in populations
                ]
            )
        )
        row = {
            "record_type": "reciprocal_mean_interval",
            "held_out_population": "reciprocal_mean",
            "model": name,
            "observed_auc": observed_mean,
            **interval(fold_mean_distribution),
        }

        if name != "full_state_plus_action":
            full_mean_distribution = np.mean(
                [
                    np.asarray(
                        fold_data[population]["distributions"][
                            "full_state_plus_action"
                        ]
                    )
                    for population in populations
                ],
                axis=0,
            )
            differences = full_mean_distribution - fold_mean_distribution
            observed_full = float(
                np.mean(
                    [
                        fold_data[population]["observed"][
                            "full_state_plus_action"
                        ]
                        for population in populations
                    ]
                )
            )
            row.update(
                {
                    "comparison": f"full_minus_{name}",
                    "observed_auc_difference": observed_full - observed_mean,
                    "difference_mean": float(np.mean(differences)),
                    "difference_ci_lower_95": float(
                        np.quantile(differences, 0.025)
                    ),
                    "difference_ci_upper_95": float(
                        np.quantile(differences, 0.975)
                    ),
                    "probability_full_better": float(np.mean(differences > 0)),
                }
            )
        output.append(row)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    fields = []
    for row in output:
        for field in row:
            if field not in fields:
                fields.append(field)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in output:
            writer.writerow({field: row.get(field, "") for field in fields})

    prediction_fields = list(prediction_rows[0])
    with PREDICTION_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=prediction_fields)
        writer.writeheader()
        writer.writerows(prediction_rows)

    print()
    print("RECIPROCAL MEAN PAIRED DIFFERENCES")
    for row in output:
        if (
            row["record_type"] == "reciprocal_mean_interval"
            and row["model"] != "full_state_plus_action"
        ):
            print(
                f"{row['comparison']:<55} "
                f"observed={row['observed_auc_difference']:+.3f} "
                f"95%CI=[{row['difference_ci_lower_95']:+.3f}, "
                f"{row['difference_ci_upper_95']:+.3f}] "
                f"P(full>comparison)={row['probability_full_better']:.3f}"
            )

    print()
    print(f"saved={OUTPUT_PATH}")
    print(f"saved={PREDICTION_PATH}")


if __name__ == "__main__":
    main()
