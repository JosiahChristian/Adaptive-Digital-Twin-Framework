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

SUMMARY_PATH = Path("results/strict_feature_reduction_action_harm_stability.csv")
SELECTION_PATH = Path("results/strict_feature_reduction_action_harm_stability_selection.csv")
PREDICTION_PATH = Path("results/strict_feature_reduction_action_harm_stability_predictions.csv")

RANDOM_STATE = 119
BOOTSTRAPS = 250
L1_C_VALUES = (0.05, 0.1, 0.25, 0.5, 1.0)
MIN_SELECTION_FREQUENCY = 0.60
MIN_SIGN_CONSISTENCY = 0.80


def matrix(rows, features):
    return np.asarray(
        [[float(row[feature]) for feature in features] for row in rows],
        dtype=float,
    )


def labels(rows):
    return np.asarray([int(row["harmful_target"]) for row in rows], dtype=int)


def stratified_bootstrap_indices(y, rng):
    parts = []
    for value in (0, 1):
        indices = np.flatnonzero(y == value)
        if len(indices) == 0:
            raise RuntimeError("Both outcome classes are required.")
        parts.append(rng.choice(indices, size=len(indices), replace=True))
    output = np.concatenate(parts)
    rng.shuffle(output)
    return output


def stability_select(training_rows, held_out_population):
    x = matrix(training_rows, BROADER_STATE_FEATURES)
    y = labels(training_rows)
    rng = np.random.default_rng(RANDOM_STATE + sum(ord(c) for c in held_out_population))

    nonzero = {feature: 0 for feature in BROADER_STATE_FEATURES}
    positive = {feature: 0 for feature in BROADER_STATE_FEATURES}
    negative = {feature: 0 for feature in BROADER_STATE_FEATURES}
    coefficient_values = {feature: [] for feature in BROADER_STATE_FEATURES}

    total_fits = 0
    for c_value in L1_C_VALUES:
        for _ in range(BOOTSTRAPS):
            sample = stratified_bootstrap_indices(y, rng)
            model = Pipeline(
                [
                    ("scaler", StandardScaler()),
                    (
                        "classifier",
                        LogisticRegression(
                            penalty="l1",
                            C=c_value,
                            solver="liblinear",
                            class_weight="balanced",
                            random_state=RANDOM_STATE,
                            max_iter=5000,
                        ),
                    ),
                ]
            )
            model.fit(x[sample], y[sample])
            coefficients = model.named_steps["classifier"].coef_[0]
            total_fits += 1

            for feature, coefficient in zip(BROADER_STATE_FEATURES, coefficients):
                coefficient = float(coefficient)
                coefficient_values[feature].append(coefficient)
                if abs(coefficient) > 1e-10:
                    nonzero[feature] += 1
                    positive[feature] += int(coefficient > 0)
                    negative[feature] += int(coefficient < 0)

    records = []
    selected = []

    for feature in BROADER_STATE_FEATURES:
        nz = nonzero[feature]
        selection_frequency = nz / total_fits
        sign_consistency = max(positive[feature], negative[feature]) / nz if nz else 0.0
        nonzero_values = [value for value in coefficient_values[feature] if abs(value) > 1e-10]
        median_coefficient = statistics.median(nonzero_values) if nonzero_values else 0.0
        qualifies = (
            selection_frequency >= MIN_SELECTION_FREQUENCY
            and sign_consistency >= MIN_SIGN_CONSISTENCY
        )

        records.append(
            {
                "held_out_population": held_out_population,
                "feature": feature,
                "total_fits": total_fits,
                "selection_frequency": selection_frequency,
                "sign_consistency": sign_consistency,
                "median_nonzero_coefficient": median_coefficient,
                "selected": int(qualifies),
            }
        )
        if qualifies:
            selected.append(feature)

    if not selected:
        ranked = sorted(
            records,
            key=lambda row: (
                row["selection_frequency"],
                row["sign_consistency"],
            ),
            reverse=True,
        )
        selected = [row["feature"] for row in ranked[:3]]
        for row in records:
            if row["feature"] in selected:
                row["selected"] = 1
                row["fallback_selection"] = 1

    return selected, records


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


def fit_evaluate(training_rows, test_rows, features, model_name, held_out_population):
    x_train = matrix(training_rows, features)
    y_train = labels(training_rows)
    x_test = matrix(test_rows, features)
    y_test = labels(test_rows)

    model = classifier()
    model.fit(x_train, y_train)
    probability = model.predict_proba(x_test)[:, 1]
    auc = float(roc_auc_score(y_test, probability))

    coefficient_map = dict(
        zip(features, model.named_steps["classifier"].coef_[0])
    )

    summary = {
        "record_type": "fold",
        "held_out_population": held_out_population,
        "model": model_name,
        "features": "|".join(features),
        "feature_count": len(features),
        "training_rows": len(training_rows),
        "training_harmful": int(np.sum(y_train)),
        "test_rows": len(test_rows),
        "test_harmful": int(np.sum(y_test)),
        "roc_auc": auc,
        "action2_coefficient": (
            float(coefficient_map["action2_indicator"])
            if "action2_indicator" in coefficient_map
            else ""
        ),
    }

    predictions = []
    for row, score in zip(test_rows, probability):
        predictions.append(
            {
                "held_out_population": held_out_population,
                "model": model_name,
                "generation_seed": row["generation_seed"],
                "test_index": row["test_index"],
                "action": row["action"],
                "harmful_target": row["harmful_target"],
                "predicted_probability": float(score),
            }
        )

    return summary, predictions


def summarize(fold_rows):
    summaries = []
    for model_name in sorted({row["model"] for row in fold_rows}):
        matching = [row for row in fold_rows if row["model"] == model_name]
        aucs = [float(row["roc_auc"]) for row in matching]
        action_coefficients = [
            float(row["action2_coefficient"])
            for row in matching
            if row["action2_coefficient"] != ""
        ]
        summaries.append(
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
    return summaries


def save_csv(path, rows):
    path.parent.mkdir(exist_ok=True)
    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main():
    print("=" * 180)
    print("EXPERIMENT 119 - STRICT FEATURE REDUCTION AND ACTION-HARM STABILITY")
    print("=" * 180)
    print(
        f"training-only stability selection: {BOOTSTRAPS} bootstraps x "
        f"{len(L1_C_VALUES)} L1 regularization values"
    )
    print(
        f"selection frequency >= {MIN_SELECTION_FREQUENCY:.0%}; "
        f"sign consistency >= {MIN_SIGN_CONSISTENCY:.0%}"
    )

    rows = early_population() + late_population()
    fold_rows = []
    selection_rows = []
    prediction_rows = []

    for held_out_population in (POPULATION_EARLY, POPULATION_LATE):
        training_rows = [
            row for row in rows if row["population"] != held_out_population
        ]
        test_rows = [
            row for row in rows if row["population"] == held_out_population
        ]

        selected, records = stability_select(training_rows, held_out_population)
        selection_rows.extend(records)

        print()
        print(f"held out={held_out_population}")
        print(f"selected state features={selected}")

        specs = {
            "action_only": ["action2_indicator"],
            "full_state_only": BROADER_STATE_FEATURES,
            "full_state_plus_action": BROADER_STATE_FEATURES + ["action2_indicator"],
            "reduced_state_only": selected,
            "reduced_state_plus_action": selected + ["action2_indicator"],
        }

        for model_name, features in specs.items():
            result, predictions = fit_evaluate(
                training_rows,
                test_rows,
                features,
                model_name,
                held_out_population,
            )
            fold_rows.append(result)
            prediction_rows.extend(predictions)
            print(
                f"{model_name:<28} features={len(features):>2} "
                f"AUC={result['roc_auc']:.3f}"
            )

    summary_rows = summarize(fold_rows)
    print()
    print("RECIPROCAL POPULATION-HELD-OUT SUMMARY")
    for row in sorted(summary_rows, key=lambda item: item["mean_auc"], reverse=True):
        stability = row["action2_sign_stability"]
        stability_text = f"{stability:.1%}" if stability != "" else "n/a"
        print(
            f"{row['model']:<28} mean_AUC={row['mean_auc']:.3f} "
            f"min_AUC={row['min_auc']:.3f} "
            f"action_sign_stability={stability_text}"
        )

    reduced = next(
        row for row in summary_rows if row["model"] == "reduced_state_plus_action"
    )
    reduced_state = next(
        row for row in summary_rows if row["model"] == "reduced_state_only"
    )
    full = next(
        row for row in summary_rows if row["model"] == "full_state_plus_action"
    )

    conclusion = {
        "record_type": "falsification_summary",
        "model": "reduced_state_plus_action",
        "mean_auc": reduced["mean_auc"],
        "min_auc": reduced["min_auc"],
        "delta_mean_auc_vs_reduced_state": (
            reduced["mean_auc"] - reduced_state["mean_auc"]
        ),
        "delta_min_auc_vs_reduced_state": (
            reduced["min_auc"] - reduced_state["min_auc"]
        ),
        "delta_mean_auc_vs_full_combined": reduced["mean_auc"] - full["mean_auc"],
        "action2_sign_stability": reduced["action2_sign_stability"],
    }

    print()
    print("PRIMARY FALSIFICATION ENDPOINT")
    for key, value in conclusion.items():
        if key not in {"record_type", "model"}:
            print(f"{key}={value}")

    save_csv(SUMMARY_PATH, summary_rows + fold_rows + [conclusion])
    save_csv(SELECTION_PATH, selection_rows)
    save_csv(PREDICTION_PATH, prediction_rows)

    print()
    print(f"saved={SUMMARY_PATH}")
    print(f"saved={SELECTION_PATH}")
    print(f"saved={PREDICTION_PATH}")


if __name__ == "__main__":
    main()
