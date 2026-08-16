import csv
import statistics
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

SUMMARY_PATH = Path("results/grouped_state_action_harm_ablation.csv")
PREDICTION_PATH = Path("results/grouped_state_action_harm_ablation_predictions.csv")
CORRELATION_PATH = Path("results/grouped_state_action_harm_ablation_correlations.csv")

RANDOM_STATE = 120
ACTION = "action2_indicator"

FEATURE_GROUPS = {
    "controller_probabilities": [
        "context_benefit_probability",
        "context_release_probability",
    ],
    "temporal_support_context": [
        "context_anchor_age",
        "context_trigger_score",
        "context_feature_distance",
    ],
    "estimated_plant_state": [
        "context_current_mismatch_indicator",
        "context_current_parameter_estimate",
    ],
    "predicted_risk_regret": [
        "predicted_under_risk",
        "predicted_primary_regret",
        "predicted_expanded_regret",
        "predicted_regret_margin",
    ],
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


def evaluate(training_rows, test_rows, features, model_name, held_out):
    x_train = matrix(training_rows, features)
    y_train = labels(training_rows)
    x_test = matrix(test_rows, features)
    y_test = labels(test_rows)

    model = classifier()
    model.fit(x_train, y_train)
    probability = model.predict_proba(x_test)[:, 1]
    coefficients = dict(
        zip(features, model.named_steps["classifier"].coef_[0])
    )

    row = {
        "record_type": "fold",
        "model": model_name,
        "held_out_population": held_out,
        "features": "|".join(features),
        "feature_count": len(features),
        "training_rows": len(training_rows),
        "training_harmful": int(np.sum(y_train)),
        "test_rows": len(test_rows),
        "test_harmful": int(np.sum(y_test)),
        "roc_auc": float(roc_auc_score(y_test, probability)),
        "action2_coefficient": (
            float(coefficients[ACTION]) if ACTION in coefficients else ""
        ),
    }

    predictions = [
        {
            "model": model_name,
            "held_out_population": held_out,
            "generation_seed": source["generation_seed"],
            "test_index": source["test_index"],
            "action": source["action"],
            "harmful_target": source["harmful_target"],
            "predicted_probability": float(score),
        }
        for source, score in zip(test_rows, probability)
    ]
    return row, predictions


def model_specs():
    specs = {
        "action_only": [ACTION],
        "full_state_only": list(BROADER_STATE_FEATURES),
        "full_state_plus_action": list(BROADER_STATE_FEATURES) + [ACTION],
    }

    for group_name, group_features in FEATURE_GROUPS.items():
        specs[f"group_only__{group_name}"] = list(group_features)
        specs[f"group_plus_action__{group_name}"] = list(group_features) + [ACTION]
        retained = [
            feature
            for feature in BROADER_STATE_FEATURES
            if feature not in group_features
        ]
        specs[f"leave_group_out__{group_name}"] = retained + [ACTION]

    return specs


def training_correlations(training_rows, held_out):
    x = matrix(training_rows, BROADER_STATE_FEATURES)
    correlation = np.corrcoef(x, rowvar=False)
    rows = []
    for left_index, left in enumerate(BROADER_STATE_FEATURES):
        for right_index in range(left_index + 1, len(BROADER_STATE_FEATURES)):
            right = BROADER_STATE_FEATURES[right_index]
            rows.append(
                {
                    "held_out_population": held_out,
                    "feature_1": left,
                    "feature_2": right,
                    "correlation": float(correlation[left_index, right_index]),
                    "absolute_correlation": abs(
                        float(correlation[left_index, right_index])
                    ),
                }
            )
    return rows


def summarize(folds):
    output = []
    for model_name in sorted({row["model"] for row in folds}):
        matching = [row for row in folds if row["model"] == model_name]
        aucs = [float(row["roc_auc"]) for row in matching]
        action_coefficients = [
            float(row["action2_coefficient"])
            for row in matching
            if row["action2_coefficient"] != ""
        ]
        output.append(
            {
                "record_type": "model_summary",
                "model": model_name,
                "mean_auc": statistics.mean(aucs),
                "min_auc": min(aucs),
                "max_auc": max(aucs),
                "action2_sign_stability": (
                    max(
                        statistics.mean(value > 0 for value in action_coefficients),
                        statistics.mean(value < 0 for value in action_coefficients),
                    )
                    if action_coefficients
                    else ""
                ),
            }
        )

    full = next(
        row for row in output if row["model"] == "full_state_plus_action"
    )
    for row in output:
        row["delta_mean_auc_vs_full"] = row["mean_auc"] - full["mean_auc"]
        row["delta_min_auc_vs_full"] = row["min_auc"] - full["min_auc"]
    return output


def save(path, rows):
    path.parent.mkdir(exist_ok=True)
    fields = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main():
    print("=" * 180)
    print("EXPERIMENT 120 - GROUPED STATE/ACTION HARM ABLATION")
    print("=" * 180)
    print(f"frozen feature groups={FEATURE_GROUPS}")

    rows = early_population() + late_population()
    folds = []
    predictions = []
    correlations = []
    specs = model_specs()

    for held_out in (POPULATION_EARLY, POPULATION_LATE):
        training = [row for row in rows if row["population"] != held_out]
        test = [row for row in rows if row["population"] == held_out]
        correlations.extend(training_correlations(training, held_out))

        print()
        print(f"held out={held_out}")
        for model_name, features in specs.items():
            row, model_predictions = evaluate(
                training, test, features, model_name, held_out
            )
            folds.append(row)
            predictions.extend(model_predictions)
            print(
                f"{model_name:<52} n={len(features):>2} "
                f"AUC={row['roc_auc']:.3f}"
            )

    summaries = summarize(folds)

    print()
    print("RECIPROCAL TRANSFER SUMMARY")
    for row in sorted(summaries, key=lambda item: item["mean_auc"], reverse=True):
        print(
            f"{row['model']:<52} mean={row['mean_auc']:.3f} "
            f"min={row['min_auc']:.3f} "
            f"dMeanFull={row['delta_mean_auc_vs_full']:+.3f}"
        )

    leave_out = [
        row for row in summaries if row["model"].startswith("leave_group_out__")
    ]
    worst_mean_loss = min(
        leave_out,
        key=lambda row: row["delta_mean_auc_vs_full"],
    )
    worst_min_loss = min(
        leave_out,
        key=lambda row: row["delta_min_auc_vs_full"],
    )

    conclusions = [
        {
            "record_type": "ablation_conclusion",
            "model": worst_mean_loss["model"],
            "endpoint": "largest_mean_auc_loss",
            "value": worst_mean_loss["delta_mean_auc_vs_full"],
        },
        {
            "record_type": "ablation_conclusion",
            "model": worst_min_loss["model"],
            "endpoint": "largest_min_auc_loss",
            "value": worst_min_loss["delta_min_auc_vs_full"],
        },
    ]

    print()
    print("PRIMARY GROUP-ABLATION OUTCOME")
    for row in conclusions:
        print(f"{row['endpoint']}={row['model']} ({row['value']:+.3f})")

    save(SUMMARY_PATH, summaries + folds + conclusions)
    save(PREDICTION_PATH, predictions)
    save(CORRELATION_PATH, correlations)

    print()
    print(f"saved={SUMMARY_PATH}")
    print(f"saved={PREDICTION_PATH}")
    print(f"saved={CORRELATION_PATH}")


if __name__ == "__main__":
    main()
