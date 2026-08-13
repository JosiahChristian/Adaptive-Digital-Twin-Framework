import csv
import statistics
from collections import Counter
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor

from experiments.adaptive_release_persistence_policy import (
    PERSISTENCE_LEVELS,
)
from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)


OUTPUT_PATH = Path(
    "results/"
    "state_dependent_risk_sensitive_persistence_control.csv"
)

RANDOM_STATE = 42
TEST_FRACTION = 0.30

FIXED_RISK_PENALTY = 0.010

RISK_MULTIPLIERS = [
    0.25,
    0.50,
    1.00,
    1.50,
    2.00,
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


def true_under_persistence_risk(
    row: dict,
) -> float:

    optimal = int(
        row[
            "best_persistence"
        ]
    )

    if optimal <= 1:
        return 0.0

    lower_actions = [
        persistence
        for persistence
        in PERSISTENCE_LEVELS
        if persistence < optimal
    ]

    lower_regrets = [
        regret(
            row,
            persistence,
        )
        for persistence in lower_actions
    ]

    if not lower_regrets:
        return 0.0

    return max(
        lower_regrets
    )


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
            selected_loss(
                row,
                persistence,
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


def train_under_risk_model(
    rows: list[dict],
) -> RandomForestRegressor:

    x = [
        feature_vector(row)
        for row in rows
    ]

    y = [
        true_under_persistence_risk(
            row
        )
        for row in rows
    ]

    model = RandomForestRegressor(
        n_estimators=600,
        min_samples_leaf=3,
        random_state=(
            RANDOM_STATE
            + 100
        ),
    )

    model.fit(
        x,
        y,
    )

    return model


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


def predict_under_risk(
    model: RandomForestRegressor,
    rows: list[dict],
) -> list[float]:

    x = [
        feature_vector(row)
        for row in rows
    ]

    predictions = model.predict(
        x
    )

    return [
        max(
            0.0,
            float(value),
        )
        for value in predictions
    ]


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


def fixed_risk_predictions(
    predicted_losses: list[dict],
    penalty: float,
) -> list[int]:

    output = []

    for row in predicted_losses:

        selected = min(
            PERSISTENCE_LEVELS,
            key=lambda persistence: (
                row[
                    persistence
                ]
                +
                penalty
                * (
                    max(
                        PERSISTENCE_LEVELS
                    )
                    - persistence
                ),
                -persistence,
            ),
        )

        output.append(
            selected
        )

    return output


def adaptive_risk_predictions(
    predicted_losses: list[dict],
    predicted_risks: list[float],
    multiplier: float,
) -> list[int]:

    output = []

    for (
        row,
        predicted_risk,
    ) in zip(
        predicted_losses,
        predicted_risks,
    ):

        selected = min(
            PERSISTENCE_LEVELS,
            key=lambda persistence: (
                row[
                    persistence
                ]
                +
                multiplier
                * predicted_risk
                * (
                    max(
                        PERSISTENCE_LEVELS
                    )
                    - persistence
                ),
                -persistence,
            ),
        )

        output.append(
            selected
        )

    return output


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


def evaluate_policy(
    name: str,
    predictions: list[int],
    rows: list[dict],
) -> dict:

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
        "policy": name,

        "accuracy":
            exact
            / len(rows),

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
            under,

        "over_count":
            over,

        "exact_count":
            exact,
    }


def evaluate_risk_estimator(
    rows: list[dict],
    predicted_risks: list[float],
) -> dict:

    true_risks = [
        true_under_persistence_risk(
            row
        )
        for row in rows
    ]

    errors = [
        abs(
            predicted
            - actual
        )
        for actual, predicted in zip(
            true_risks,
            predicted_risks,
        )
    ]

    positive_true = [
        actual
        for actual in true_risks
        if actual > 1e-12
    ]

    positive_predicted = [
        predicted
        for actual, predicted in zip(
            true_risks,
            predicted_risks,
        )
        if actual > 1e-12
    ]

    return {
        "mean_true_risk":
            statistics.mean(
                true_risks
            ),

        "mean_predicted_risk":
            statistics.mean(
                predicted_risks
            ),

        "risk_mae":
            statistics.mean(
                errors
            ),

        "positive_contexts":
            len(
                positive_true
            ),

        "mean_true_positive_risk":
            (
                statistics.mean(
                    positive_true
                )
                if positive_true
                else 0.0
            ),

        "mean_predicted_positive_risk":
            (
                statistics.mean(
                    positive_predicted
                )
                if positive_predicted
                else 0.0
            ),
    }


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


def print_result(
    result: dict,
) -> None:

    print(
        f"{result['policy']:<30} "
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


def main() -> None:

    rows = generate_analysis_rows()

    (
        train_rows,
        test_rows,
    ) = deterministic_split(
        rows
    )

    loss_models = train_loss_models(
        train_rows
    )

    risk_model = train_under_risk_model(
        train_rows
    )

    predicted_losses = (
        predicted_loss_table(
            loss_models,
            test_rows,
        )
    )

    predicted_risks = (
        predict_under_risk(
            risk_model,
            test_rows,
        )
    )

    risk_metrics = (
        evaluate_risk_estimator(
            test_rows,
            predicted_risks,
        )
    )

    direct_predictions = (
        direct_loss_predictions(
            predicted_losses
        )
    )

    fixed_risk = (
        fixed_risk_predictions(
            predicted_losses,
            FIXED_RISK_PENALTY,
        )
    )

    adaptive_predictions = {}

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
            name="direct_loss_model",
            predictions=direct_predictions,
            rows=test_rows,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="fixed_risk_0.010",
            predictions=fixed_risk,
            rows=test_rows,
        )
    )

    for multiplier in (
        RISK_MULTIPLIERS
    ):

        predictions = (
            adaptive_risk_predictions(
                predicted_losses,
                predicted_risks,
                multiplier,
            )
        )

        adaptive_predictions[
            multiplier
        ] = predictions

        evaluations.append(
            evaluate_policy(
                name=(
                    "adaptive_risk_"
                    f"{multiplier:.2f}"
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

    print("=" * 165)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "STATE-DEPENDENT RISK-SENSITIVE "
        "PERSISTENCE CONTROL"
    )

    print("=" * 165)

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
        "UNDER-PERSISTENCE RISK ESTIMATOR"
    )

    print(
        "mean true risk="
        f"{risk_metrics['mean_true_risk']:.6f}"
    )

    print(
        "mean predicted risk="
        f"{risk_metrics['mean_predicted_risk']:.6f}"
    )

    print(
        "risk MAE="
        f"{risk_metrics['risk_mae']:.6f}"
    )

    print(
        "positive-risk contexts="
        f"{risk_metrics['positive_contexts']}"
    )

    print(
        "mean true risk on positive contexts="
        f"{risk_metrics['mean_true_positive_risk']:.6f}"
    )

    print(
        "mean predicted risk on positive contexts="
        f"{risk_metrics['mean_predicted_positive_risk']:.6f}"
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

    print_distribution(
        "Fixed risk penalty 0.010",
        fixed_risk,
    )

    for multiplier in (
        RISK_MULTIPLIERS
    ):

        print_distribution(
            (
                "Adaptive risk multiplier "
                f"{multiplier:.2f}"
            ),
            adaptive_predictions[
                multiplier
            ],
        )

    print("=" * 165)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()