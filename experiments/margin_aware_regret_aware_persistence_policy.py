import csv
import statistics
from collections import Counter
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from experiments.adaptive_release_persistence_policy import (
    PERSISTENCE_LEVELS,
)


FEATURE_NAMES = [
    "benefit_probability",
    "release_probability",
    "anchor_age",
    "trigger_score",
    "feature_distance",
    "current_mismatch_indicator",
    "current_parameter_estimate",
]
from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)


OUTPUT_PATH = Path(
    "results/"
    "margin_aware_regret_aware_persistence_policy.csv"
)

RANDOM_STATE = 42
TEST_FRACTION = 0.30

MARGIN_FLOOR = 0.001


def feature_vector(row: dict) -> list[float]:
    return [
        float(row[name])
        for name in FEATURE_NAMES
    ]


def deterministic_split(
    rows: list[dict],
) -> tuple[list[dict], list[dict]]:

    split_index = int(
        len(rows)
        * (1.0 - TEST_FRACTION)
    )

    return (
        rows[:split_index],
        rows[split_index:],
    )


def train_classifier(
    rows: list[dict],
    sample_weights=None,
) -> RandomForestClassifier:

    x = [
        feature_vector(row)
        for row in rows
    ]

    y = [
        int(row["best_persistence"])
        for row in rows
    ]

    model = RandomForestClassifier(
        n_estimators=400,
        min_samples_leaf=3,
        random_state=RANDOM_STATE,
        class_weight="balanced",
    )

    model.fit(
        x,
        y,
        sample_weight=sample_weights,
    )

    return model


def margin_weights(
    rows: list[dict],
) -> list[float]:

    return [
        max(
            float(row["absolute_margin"]),
            MARGIN_FLOOR,
        )
        for row in rows
    ]


def selected_loss(
    row: dict,
    persistence: int,
) -> float:

    return float(
        row[f"loss_k{persistence}"]
    )


def regret(
    row: dict,
    persistence: int,
) -> float:

    return (
        selected_loss(
            row,
            persistence,
        )
        - float(row["best_loss"])
    )


def evaluate_policy(
    name: str,
    predictions: list[int],
    rows: list[dict],
) -> dict:

    true_labels = [
        int(row["best_persistence"])
        for row in rows
    ]

    regrets = [
        regret(
            row,
            prediction,
        )
        for row, prediction in zip(
            rows,
            predictions,
        )
    ]

    selected_losses = [
        selected_loss(
            row,
            prediction,
        )
        for row, prediction in zip(
            rows,
            predictions,
        )
    ]

    zero_regret_fraction = (
        sum(
            value <= 1e-12
            for value in regrets
        )
        / len(regrets)
    )

    return {
        "policy": name,
        "accuracy": accuracy_score(
            true_labels,
            predictions,
        ),
        "mean_selected_loss":
            statistics.mean(
                selected_losses
            ),
        "mean_regret":
            statistics.mean(
                regrets
            ),
        "median_regret":
            statistics.median(
                regrets
            ),
        "max_regret":
            max(
                regrets
            ),
        "zero_regret_fraction":
            zero_regret_fraction,
    }


def predict_model(
    model: RandomForestClassifier,
    rows: list[dict],
) -> list[int]:

    x = [
        feature_vector(row)
        for row in rows
    ]

    return [
        int(value)
        for value in model.predict(x)
    ]


def fixed_predictions(
    persistence: int,
    rows: list[dict],
) -> list[int]:

    return [
        persistence
        for _ in rows
    ]


def oracle_predictions(
    rows: list[dict],
) -> list[int]:

    return [
        int(row["best_persistence"])
        for row in rows
    ]


def save_results(
    evaluations: list[dict],
) -> None:

    OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=evaluations[0].keys(),
        )

        writer.writeheader()
        writer.writerows(
            evaluations
        )


def print_evaluation(
    result: dict,
) -> None:

    print(
        f"{result['policy']:<24} "
        f"accuracy="
        f"{result['accuracy']:.3%} "
        f"mean_loss="
        f"{result['mean_selected_loss']:.6f} "
        f"mean_regret="
        f"{result['mean_regret']:.6f} "
        f"median_regret="
        f"{result['median_regret']:.6f} "
        f"max_regret="
        f"{result['max_regret']:.6f} "
        f"zero_regret="
        f"{result['zero_regret_fraction']:.3%}"
    )


def print_prediction_distribution(
    name: str,
    predictions: list[int],
) -> None:

    counts = Counter(
        predictions
    )

    print(
        name
    )

    for persistence in (
        PERSISTENCE_LEVELS
    ):

        count = counts[
            persistence
        ]

        fraction = (
            count
            / len(predictions)
        )

        print(
            f"  k={persistence}: "
            f"{count} "
            f"({fraction:.3%})"
        )


def main() -> None:

    rows = generate_analysis_rows()

    train_rows, test_rows = (
        deterministic_split(
            rows
        )
    )

    baseline_model = (
        train_classifier(
            train_rows
        )
    )

    weighted_model = (
        train_classifier(
            train_rows,
            sample_weights=margin_weights(
                train_rows
            ),
        )
    )

    baseline_predictions = (
        predict_model(
            baseline_model,
            test_rows,
        )
    )

    weighted_predictions = (
        predict_model(
            weighted_model,
            test_rows,
        )
    )

    evaluations = []

    for persistence in (
        PERSISTENCE_LEVELS
    ):

        evaluations.append(
            evaluate_policy(
                name=f"fixed_k{persistence}",
                predictions=fixed_predictions(
                    persistence,
                    test_rows,
                ),
                rows=test_rows,
            )
        )

    evaluations.append(
        evaluate_policy(
            name="exact_label_model",
            predictions=baseline_predictions,
            rows=test_rows,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="margin_weighted_model",
            predictions=weighted_predictions,
            rows=test_rows,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="oracle",
            predictions=oracle_predictions(
                test_rows
            ),
            rows=test_rows,
        )
    )

    save_results(
        evaluations
    )

    print("=" * 140)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "MARGIN-AWARE / REGRET-AWARE "
        "PERSISTENCE POLICY"
    )

    print("=" * 140)

    print(
        f"total contexts={len(rows)}"
    )

    print(
        f"training contexts="
        f"{len(train_rows)}"
    )

    print(
        f"test contexts="
        f"{len(test_rows)}"
    )

    print()

    print(
        "POLICY PERFORMANCE"
    )

    for result in evaluations:
        print_evaluation(
            result
        )

    print()

    print(
        "PREDICTION DISTRIBUTIONS"
    )

    print_prediction_distribution(
        "Exact-label model",
        baseline_predictions,
    )

    print_prediction_distribution(
        "Margin-weighted model",
        weighted_predictions,
    )

    print("=" * 140)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()