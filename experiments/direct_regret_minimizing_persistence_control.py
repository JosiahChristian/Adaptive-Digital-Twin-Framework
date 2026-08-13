import csv
import statistics
from collections import Counter
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score

from experiments.adaptive_release_persistence_policy import (
    PERSISTENCE_LEVELS,
)
from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)


OUTPUT_PATH = Path(
    "results/"
    "direct_regret_minimizing_persistence_control.csv"
)

RANDOM_STATE = 42
TEST_FRACTION = 0.30


FEATURE_NAMES = [
    "benefit_probability",
    "release_probability",
    "anchor_age",
    "trigger_score",
    "feature_distance",
    "current_mismatch_indicator",
    "current_parameter_estimate",
]


def feature_vector(
    row: dict,
) -> list[float]:

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


def train_exact_label_classifier(
    rows: list[dict],
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
    )

    return model


def train_loss_models(
    rows: list[dict],
) -> dict[int, RandomForestRegressor]:

    x = [
        feature_vector(row)
        for row in rows
    ]

    models = {}

    for persistence in (
        PERSISTENCE_LEVELS
    ):

        y = [
            float(
                row[
                    f"loss_k{persistence}"
                ]
            )
            for row in rows
        ]

        model = RandomForestRegressor(
            n_estimators=500,
            min_samples_leaf=3,
            random_state=(
                RANDOM_STATE
                + persistence
            ),
        )

        model.fit(
            x,
            y,
        )

        models[
            persistence
        ] = model

    return models


def predict_exact_labels(
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


def predict_direct_losses(
    models: dict[
        int,
        RandomForestRegressor,
    ],
    rows: list[dict],
) -> tuple[
    list[int],
    list[dict],
]:

    x = [
        feature_vector(row)
        for row in rows
    ]

    predicted_loss_arrays = {}

    for persistence in (
        PERSISTENCE_LEVELS
    ):

        predicted_loss_arrays[
            persistence
        ] = models[
            persistence
        ].predict(
            x
        )

    predictions = []
    prediction_rows = []

    for index, row in enumerate(
        rows
    ):

        predicted_losses = {
            persistence:
                float(
                    predicted_loss_arrays[
                        persistence
                    ][index]
                )
            for persistence
            in PERSISTENCE_LEVELS
        }

        selected_persistence = min(
            PERSISTENCE_LEVELS,
            key=lambda persistence: (
                predicted_losses[
                    persistence
                ],
                persistence,
            ),
        )

        predictions.append(
            selected_persistence
        )

        prediction_rows.append(
            {
                "context_index":
                    int(
                        row[
                            "context_index"
                        ]
                    ),

                "true_best_persistence":
                    int(
                        row[
                            "best_persistence"
                        ]
                    ),

                "selected_persistence":
                    selected_persistence,

                "predicted_loss_k1":
                    predicted_losses[1],

                "predicted_loss_k2":
                    predicted_losses[2],

                "predicted_loss_k3":
                    predicted_losses[3],

                "actual_loss_k1":
                    float(
                        row[
                            "loss_k1"
                        ]
                    ),

                "actual_loss_k2":
                    float(
                        row[
                            "loss_k2"
                        ]
                    ),

                "actual_loss_k3":
                    float(
                        row[
                            "loss_k3"
                        ]
                    ),

                "best_loss":
                    float(
                        row[
                            "best_loss"
                        ]
                    ),

                "selected_loss":
                    selected_loss(
                        row,
                        selected_persistence,
                    ),

                "regret":
                    regret(
                        row,
                        selected_persistence,
                    ),
            }
        )

    return (
        predictions,
        prediction_rows,
    )


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

    losses = [
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

    consequential_regret_fraction = (
        sum(
            value > 0.005
            for value in regrets
        )
        / len(regrets)
    )

    return {
        "policy": name,

        "accuracy":
            accuracy_score(
                true_labels,
                predictions,
            ),

        "mean_loss":
            statistics.mean(
                losses
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

        "regret_gt_0_005_fraction":
            consequential_regret_fraction,
    }


def directional_regret_summary(
    predictions: list[int],
    rows: list[dict],
) -> dict:

    under_regrets = []
    over_regrets = []
    exact_regrets = []

    for row, prediction in zip(
        rows,
        predictions,
    ):

        best = int(
            row[
                "best_persistence"
            ]
        )

        value = regret(
            row,
            prediction,
        )

        if prediction < best:

            under_regrets.append(
                value
            )

        elif prediction > best:

            over_regrets.append(
                value
            )

        else:

            exact_regrets.append(
                value
            )

    return {
        "under_count":
            len(
                under_regrets
            ),

        "under_mean_regret":
            (
                statistics.mean(
                    under_regrets
                )
                if under_regrets
                else 0.0
            ),

        "under_max_regret":
            (
                max(
                    under_regrets
                )
                if under_regrets
                else 0.0
            ),

        "over_count":
            len(
                over_regrets
            ),

        "over_mean_regret":
            (
                statistics.mean(
                    over_regrets
                )
                if over_regrets
                else 0.0
            ),

        "over_max_regret":
            (
                max(
                    over_regrets
                )
                if over_regrets
                else 0.0
            ),

        "exact_count":
            len(
                exact_regrets
            ),
    }


def print_policy_result(
    result: dict,
) -> None:

    print(
        f"{result['policy']:<26} "
        f"accuracy="
        f"{result['accuracy']:.3%} "
        f"mean_loss="
        f"{result['mean_loss']:.6f} "
        f"mean_regret="
        f"{result['mean_regret']:.6f} "
        f"median_regret="
        f"{result['median_regret']:.6f} "
        f"max_regret="
        f"{result['max_regret']:.6f} "
        f"zero_regret="
        f"{result['zero_regret_fraction']:.3%} "
        f"regret>0.005="
        f"{result['regret_gt_0_005_fraction']:.3%}"
    )


def print_distribution(
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

        print(
            f"  k={persistence}: "
            f"{count} "
            f"({count / len(predictions):.3%})"
        )


def print_directional_summary(
    name: str,
    summary: dict,
) -> None:

    print(
        name
    )

    print(
        "  insufficient persistence: "
        f"n={summary['under_count']} "
        f"mean_regret="
        f"{summary['under_mean_regret']:.6f} "
        f"max_regret="
        f"{summary['under_max_regret']:.6f}"
    )

    print(
        "  excessive persistence:    "
        f"n={summary['over_count']} "
        f"mean_regret="
        f"{summary['over_mean_regret']:.6f} "
        f"max_regret="
        f"{summary['over_max_regret']:.6f}"
    )

    print(
        "  exact persistence:        "
        f"n={summary['exact_count']}"
    )


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


def main() -> None:

    rows = generate_analysis_rows()

    (
        train_rows,
        test_rows,
    ) = deterministic_split(
        rows
    )

    exact_label_model = (
        train_exact_label_classifier(
            train_rows
        )
    )

    loss_models = (
        train_loss_models(
            train_rows
        )
    )

    exact_predictions = (
        predict_exact_labels(
            exact_label_model,
            test_rows,
        )
    )

    (
        direct_predictions,
        _,
    ) = predict_direct_losses(
        loss_models,
        test_rows,
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
            predictions=exact_predictions,
            rows=test_rows,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="direct_loss_model",
            predictions=direct_predictions,
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

    print("=" * 150)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "DIRECT REGRET-MINIMIZING "
        "PERSISTENCE CONTROL"
    )

    print("=" * 150)

    print(
        f"total contexts="
        f"{len(rows)}"
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

        print_policy_result(
            result
        )

    print()

    print(
        "PREDICTION DISTRIBUTIONS"
    )

    print_distribution(
        "Exact-label model",
        exact_predictions,
    )

    print_distribution(
        "Direct-loss model",
        direct_predictions,
    )

    print()

    print(
        "DIRECTIONAL REGRET"
    )

    print_directional_summary(
        "Exact-label model",
        directional_regret_summary(
            exact_predictions,
            test_rows,
        ),
    )

    print_directional_summary(
        "Direct-loss model",
        directional_regret_summary(
            direct_predictions,
            test_rows,
        ),
    )

    print("=" * 150)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()