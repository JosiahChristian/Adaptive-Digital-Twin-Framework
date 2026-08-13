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
    "asymmetric_risk_sensitive_persistence_control.csv"
)

RANDOM_STATE = 42
TEST_FRACTION = 0.30

UNDER_PERSISTENCE_PENALTIES = [
    0.000,
    0.002,
    0.005,
    0.010,
    0.020,
]


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
        row[
            f"loss_k{persistence}"
        ]
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
        - float(
            row[
                "best_loss"
            ]
        )
    )


def train_exact_classifier(
    rows: list[dict],
) -> RandomForestClassifier:

    x = [
        feature_vector(row)
        for row in rows
    ]

    y = [
        int(
            row[
                "best_persistence"
            ]
        )
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
) -> dict[
    int,
    RandomForestRegressor,
]:

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


def predict_exact(
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


def predicted_loss_table(
    models: dict[
        int,
        RandomForestRegressor,
    ],
    rows: list[dict],
) -> list[dict]:

    x = [
        feature_vector(row)
        for row in rows
    ]

    predictions = {}

    for persistence in (
        PERSISTENCE_LEVELS
    ):

        predictions[
            persistence
        ] = models[
            persistence
        ].predict(
            x
        )

    output = []

    for index in range(
        len(rows)
    ):

        output.append(
            {
                persistence:
                    float(
                        predictions[
                            persistence
                        ][index]
                    )
                for persistence
                in PERSISTENCE_LEVELS
            }
        )

    return output


def direct_loss_predictions(
    predicted_losses: list[dict],
) -> list[int]:

    return [
        min(
            PERSISTENCE_LEVELS,
            key=lambda persistence: (
                row[
                    persistence
                ],
                persistence,
            ),
        )
        for row in predicted_losses
    ]


def risk_sensitive_predictions(
    predicted_losses: list[dict],
    penalty: float,
) -> list[int]:

    predictions = []

    for row in predicted_losses:

        scored = {}

        for persistence in (
            PERSISTENCE_LEVELS
        ):

            # Conservative directional risk:
            # lower-persistence actions receive a larger
            # penalty because under-persistence was shown
            # to be substantially more costly.
            under_persistence_risk = (
                max(PERSISTENCE_LEVELS)
                - persistence
            )

            scored[
                persistence
            ] = (
                row[
                    persistence
                ]
                + penalty
                * under_persistence_risk
            )

        selected = min(
            PERSISTENCE_LEVELS,
            key=lambda persistence: (
                scored[
                    persistence
                ],
                -persistence,
            ),
        )

        predictions.append(
            selected
        )

    return predictions

    predictions = []

    for row in predicted_losses:

        best_predicted = min(
            PERSISTENCE_LEVELS,
            key=lambda persistence: (
                row[
                    persistence
                ],
                persistence,
            ),
        )

        scored = {}

        for persistence in (
            PERSISTENCE_LEVELS
        ):

            under_distance = max(
                0,
                best_predicted
                - persistence,
            )

            scored[
                persistence
            ] = (
                row[
                    persistence
                ]
                + penalty
                * under_distance
            )

        selected = min(
            PERSISTENCE_LEVELS,
            key=lambda persistence: (
                scored[
                    persistence
                ],
                -persistence,
            ),
        )

        predictions.append(
            selected
        )

    return predictions


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
        int(
            row[
                "best_persistence"
            ]
        )
        for row in rows
    ]


def directional_error_counts(
    rows: list[dict],
    predictions: list[int],
) -> dict:

    under = 0
    over = 0
    exact = 0

    for row, prediction in zip(
        rows,
        predictions,
    ):

        optimal = int(
            row[
                "best_persistence"
            ]
        )

        if prediction < optimal:
            under += 1

        elif prediction > optimal:
            over += 1

        else:
            exact += 1

    return {
        "under_count": under,
        "over_count": over,
        "exact_count": exact,
    }


def evaluate_policy(
    name: str,
    predictions: list[int],
    rows: list[dict],
) -> dict:

    true_labels = [
        int(
            row[
                "best_persistence"
            ]
        )
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

    directions = (
        directional_error_counts(
            rows,
            predictions,
        )
    )

    under_regrets = [
        regret(
            row,
            prediction,
        )
        for row, prediction in zip(
            rows,
            predictions,
        )
        if prediction
        <
        int(
            row[
                "best_persistence"
            ]
        )
    ]

    over_regrets = [
        regret(
            row,
            prediction,
        )
        for row, prediction in zip(
            rows,
            predictions,
        )
        if prediction
        >
        int(
            row[
                "best_persistence"
            ]
        )
    ]

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

        "max_regret":
            max(
                regrets
            ),

        "zero_regret_fraction":
            (
                sum(
                    value <= 1e-12
                    for value in regrets
                )
                / len(regrets)
            ),

        "regret_gt_0_005_fraction":
            (
                sum(
                    value > 0.005
                    for value in regrets
                )
                / len(regrets)
            ),

        "under_count":
            directions[
                "under_count"
            ],

        "over_count":
            directions[
                "over_count"
            ],

        "under_mean_regret":
            (
                statistics.mean(
                    under_regrets
                )
                if under_regrets
                else 0.0
            ),

        "over_mean_regret":
            (
                statistics.mean(
                    over_regrets
                )
                if over_regrets
                else 0.0
            ),
    }


def print_result(
    result: dict,
) -> None:

    print(
        f"{result['policy']:<28} "
        f"accuracy="
        f"{result['accuracy']:.3%} "
        f"mean_loss="
        f"{result['mean_loss']:.6f} "
        f"mean_regret="
        f"{result['mean_regret']:.6f} "
        f"max_regret="
        f"{result['max_regret']:.6f} "
        f"zero_regret="
        f"{result['zero_regret_fraction']:.3%} "
        f"regret>0.005="
        f"{result['regret_gt_0_005_fraction']:.3%} "
        f"under="
        f"{result['under_count']} "
        f"over="
        f"{result['over_count']}"
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

    classifier = (
        train_exact_classifier(
            train_rows
        )
    )

    loss_models = (
        train_loss_models(
            train_rows
        )
    )

    exact_predictions = (
        predict_exact(
            classifier,
            test_rows,
        )
    )

    predicted_losses = (
        predicted_loss_table(
            loss_models,
            test_rows,
        )
    )

    direct_predictions = (
        direct_loss_predictions(
            predicted_losses
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

    risk_predictions = {}

    for penalty in (
        UNDER_PERSISTENCE_PENALTIES
    ):

        predictions = (
            risk_sensitive_predictions(
                predicted_losses,
                penalty,
            )
        )

        risk_predictions[
            penalty
        ] = predictions

        evaluations.append(
            evaluate_policy(
                name=(
                    "risk_sensitive_"
                    f"{penalty:.3f}"
                ),
                predictions=predictions,
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

    print("=" * 160)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "ASYMMETRIC RISK-SENSITIVE "
        "PERSISTENCE CONTROL"
    )

    print("=" * 160)

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

        print_result(
            result
        )

    print()

    print(
        "ACTION DISTRIBUTIONS"
    )

    print_distribution(
        "Direct-loss model",
        direct_predictions,
    )

    for penalty in (
        UNDER_PERSISTENCE_PENALTIES
    ):

        print_distribution(
            (
                "Risk-sensitive "
                f"penalty={penalty:.3f}"
            ),
            risk_predictions[
                penalty
            ],
        )

    print("=" * 160)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()