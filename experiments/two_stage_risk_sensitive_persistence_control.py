import csv
import statistics
from pathlib import Path

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
)

from experiments.adaptive_release_persistence_policy import (
    PERSISTENCE_LEVELS,
)
from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)


OUTPUT_PATH = Path(
    "results/"
    "two_stage_risk_sensitive_persistence_control.csv"
)

RANDOM_STATE = 42
TEST_FRACTION = 0.30

FIXED_RISK_PENALTY = 0.010

RISK_MULTIPLIERS = [
    0.25,
    0.50,
    0.75,
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


def true_under_risk(
    row: dict,
) -> float:

    optimal = int(
        row[
            "best_persistence"
        ]
    )

    lower_actions = [
        persistence
        for persistence
        in PERSISTENCE_LEVELS
        if persistence < optimal
    ]

    if not lower_actions:
        return 0.0

    return max(
        regret(
            row,
            persistence,
        )
        for persistence
        in lower_actions
    )


def positive_risk_label(
    row: dict,
) -> int:

    return int(
        true_under_risk(
            row
        )
        > 1e-12
    )


def train_loss_models(
    rows: list[dict],
) -> dict[int, RandomForestRegressor]:

    x = [
        feature_vector(row)
        for row in rows
    ]

    models = {}

    for persistence in PERSISTENCE_LEVELS:

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


def train_single_stage_risk_model(
    rows: list[dict],
) -> RandomForestRegressor:

    x = [
        feature_vector(row)
        for row in rows
    ]

    y = [
        true_under_risk(
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


def train_occurrence_model(
    rows: list[dict],
) -> RandomForestClassifier:

    x = [
        feature_vector(row)
        for row in rows
    ]

    y = [
        positive_risk_label(
            row
        )
        for row in rows
    ]

    model = RandomForestClassifier(
        n_estimators=600,
        min_samples_leaf=3,
        random_state=(
            RANDOM_STATE
            + 200
        ),
        class_weight="balanced",
    )

    model.fit(
        x,
        y,
    )

    return model


def train_magnitude_model(
    rows: list[dict],
) -> RandomForestRegressor:

    positive_rows = [
        row
        for row in rows
        if positive_risk_label(
            row
        )
        == 1
    ]

    x = [
        feature_vector(row)
        for row in positive_rows
    ]

    y = [
        true_under_risk(
            row
        )
        for row in positive_rows
    ]

    model = RandomForestRegressor(
        n_estimators=600,
        min_samples_leaf=2,
        random_state=(
            RANDOM_STATE
            + 300
        ),
    )

    model.fit(
        x,
        y,
    )

    return model


def predicted_loss_table(
    models: dict[int, RandomForestRegressor],
    rows: list[dict],
) -> list[dict]:

    x = [
        feature_vector(row)
        for row in rows
    ]

    arrays = {
        persistence:
            models[
                persistence
            ].predict(
                x
            )
        for persistence
        in PERSISTENCE_LEVELS
    }

    output = []

    for index in range(
        len(rows)
    ):

        output.append(
            {
                persistence:
                    float(
                        arrays[
                            persistence
                        ][index]
                    )
                for persistence
                in PERSISTENCE_LEVELS
            }
        )

    return output


def predict_single_stage_risk(
    model: RandomForestRegressor,
    rows: list[dict],
) -> list[float]:

    x = [
        feature_vector(row)
        for row in rows
    ]

    return [
        max(
            0.0,
            float(value),
        )
        for value in model.predict(
            x
        )
    ]


def predict_two_stage_risk(
    occurrence_model: RandomForestClassifier,
    magnitude_model: RandomForestRegressor,
    rows: list[dict],
) -> list[float]:

    x = [
        feature_vector(row)
        for row in rows
    ]

    probabilities = (
        occurrence_model.predict_proba(
            x
        )[:, 1]
    )

    magnitudes = (
        magnitude_model.predict(
            x
        )
    )

    return [
        float(probability)
        * max(
            0.0,
            float(magnitude),
        )
        for probability, magnitude
        in zip(
            probabilities,
            magnitudes,
        )
    ]


def direct_predictions(
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
                + penalty
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

    for row, risk in zip(
        predicted_losses,
        predicted_risks,
    ):

        selected = min(
            PERSISTENCE_LEVELS,
            key=lambda persistence: (
                row[
                    persistence
                ]
                + multiplier
                * risk
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
        for row, prediction
        in zip(
            rows,
            predictions,
        )
    ]

    losses = [
        selected_loss(
            row,
            prediction,
        )
        for row, prediction
        in zip(
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
        "policy":
            name,

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
        f"{result['policy']:<34} "
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

    single_stage_model = (
        train_single_stage_risk_model(
            train_rows
        )
    )

    occurrence_model = (
        train_occurrence_model(
            train_rows
        )
    )

    magnitude_model = (
        train_magnitude_model(
            train_rows
        )
    )

    predicted_losses = (
        predicted_loss_table(
            loss_models,
            test_rows,
        )
    )

    single_stage_risks = (
        predict_single_stage_risk(
            single_stage_model,
            test_rows,
        )
    )

    two_stage_risks = (
        predict_two_stage_risk(
            occurrence_model,
            magnitude_model,
            test_rows,
        )
    )

    evaluations = []

    evaluations.append(
        evaluate_policy(
            name="fixed_k1",
            predictions=fixed_predictions(
                1,
                test_rows,
            ),
            rows=test_rows,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="fixed_k2",
            predictions=fixed_predictions(
                2,
                test_rows,
            ),
            rows=test_rows,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="fixed_k3",
            predictions=fixed_predictions(
                3,
                test_rows,
            ),
            rows=test_rows,
        )
    )

    direct = direct_predictions(
        predicted_losses
    )

    evaluations.append(
        evaluate_policy(
            name="direct_loss_model",
            predictions=direct,
            rows=test_rows,
        )
    )

    fixed_risk = (
        fixed_risk_predictions(
            predicted_losses,
            FIXED_RISK_PENALTY,
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

        single_predictions = (
            adaptive_risk_predictions(
                predicted_losses,
                single_stage_risks,
                multiplier,
            )
        )

        two_stage_predictions = (
            adaptive_risk_predictions(
                predicted_losses,
                two_stage_risks,
                multiplier,
            )
        )

        evaluations.append(
            evaluate_policy(
                name=(
                    "single_stage_"
                    f"{multiplier:.2f}"
                ),
                predictions=single_predictions,
                rows=test_rows,
            )
        )

        evaluations.append(
            evaluate_policy(
                name=(
                    "two_stage_"
                    f"{multiplier:.2f}"
                ),
                predictions=two_stage_predictions,
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

    print("=" * 175)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "TWO-STAGE RISK-SENSITIVE "
        "PERSISTENCE CONTROL"
    )

    print("=" * 175)

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

    print("=" * 175)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()