import csv
import math
import statistics
from collections import Counter
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
    "responsiveness_preserving_safe_persistence_control.csv"
)

RANDOM_STATE = 42
TEST_FRACTION = 0.30

FIXED_RISK_PENALTY = 0.010

RISK_MULTIPLIERS = [
    0.10,
    0.25,
    0.50,
    0.75,
    1.00,
    1.25,
    1.50,
    2.00,
]

UNDER_PERSISTENCE_LIMITS = [
    0,
    1,
    2,
    4,
    6,
    8,
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


def action_entropy(
    predictions: list[int],
) -> float:

    counts = Counter(
        predictions
    )

    total = len(
        predictions
    )

    entropy = 0.0

    for persistence in (
        PERSISTENCE_LEVELS
    ):

        probability = (
            counts[
                persistence
            ]
            / total
        )

        if probability > 0.0:

            entropy -= (
                probability
                * math.log(
                    probability
                )
            )

    maximum_entropy = math.log(
        len(
            PERSISTENCE_LEVELS
        )
    )

    if maximum_entropy <= 0.0:
        return 0.0

    return (
        entropy
        / maximum_entropy
    )


def dominant_action_fraction(
    predictions: list[int],
) -> float:

    counts = Counter(
        predictions
    )

    return (
        max(
            counts.values()
        )
        / len(
            predictions
        )
    )


def deviation_from_direct(
    predictions: list[int],
    direct: list[int],
) -> float:

    return (
        sum(
            prediction
            != direct_prediction
            for (
                prediction,
                direct_prediction,
            ) in zip(
                predictions,
                direct,
            )
        )
        / len(
            predictions
        )
    )


def evaluate_policy(
    name: str,
    predictions: list[int],
    rows: list[dict],
    direct: list[int],
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

        "action_entropy":
            action_entropy(
                predictions
            ),

        "dominant_action_fraction":
            dominant_action_fraction(
                predictions
            ),

        "deviation_from_direct":
            deviation_from_direct(
                predictions,
                direct,
            ),
    }


def pareto_safe_policies(
    evaluations: list[dict],
) -> list[dict]:

    output = []

    for under_limit in (
        UNDER_PERSISTENCE_LIMITS
    ):

        candidates = [
            result
            for result in evaluations
            if result[
                "under_count"
            ]
            <= under_limit
        ]

        if not candidates:
            continue

        best = min(
            candidates,
            key=lambda result: (
                result[
                    "mean_regret"
                ],
                -result[
                    "action_entropy"
                ],
                result[
                    "over_count"
                ],
            ),
        )

        output.append(
            {
                "under_limit":
                    under_limit,

                "policy":
                    best[
                        "policy"
                    ],

                "mean_regret":
                    best[
                        "mean_regret"
                    ],

                "action_entropy":
                    best[
                        "action_entropy"
                    ],

                "dominant_action_fraction":
                    best[
                        "dominant_action_fraction"
                    ],

                "under_count":
                    best[
                        "under_count"
                    ],

                "over_count":
                    best[
                        "over_count"
                    ],
            }
        )

    return output


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
        f"{result['policy']:<28} "
        f"mean_regret="
        f"{result['mean_regret']:.6f} "
        f"zero_regret="
        f"{result['zero_regret_fraction']:.3%} "
        f"under="
        f"{result['under_count']:<2} "
        f"over="
        f"{result['over_count']:<2} "
        f"entropy="
        f"{result['action_entropy']:.3f} "
        f"dominant="
        f"{result['dominant_action_fraction']:.3%} "
        f"deviation="
        f"{result['deviation_from_direct']:.3%}"
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

    predicted_risks = (
        predict_two_stage_risk(
            occurrence_model,
            magnitude_model,
            test_rows,
        )
    )

    direct = direct_predictions(
        predicted_losses
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
            direct=direct,
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
            direct=direct,
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
            direct=direct,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="direct_loss",
            predictions=direct,
            rows=test_rows,
            direct=direct,
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
            direct=direct,
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

        evaluations.append(
            evaluate_policy(
                name=(
                    "two_stage_"
                    f"{multiplier:.2f}"
                ),
                predictions=predictions,
                rows=test_rows,
                direct=direct,
            )
        )

    evaluations.append(
        evaluate_policy(
            name="oracle",
            predictions=oracle_predictions(
                test_rows
            ),
            rows=test_rows,
            direct=direct,
        )
    )

    save_results(
        evaluations
    )

    safe_frontier = (
        pareto_safe_policies(
            evaluations
        )
    )

    print("=" * 175)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "RESPONSIVENESS-PRESERVING "
        "SAFE PERSISTENCE CONTROL"
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

    print()

    print(
        "SAFE RESPONSIVENESS FRONTIER"
    )

    for point in safe_frontier:

        print(
            f"under<= "
            f"{point['under_limit']:<2} "
            f"policy="
            f"{point['policy']:<22} "
            f"regret="
            f"{point['mean_regret']:.6f} "
            f"entropy="
            f"{point['action_entropy']:.3f} "
            f"dominant="
            f"{point['dominant_action_fraction']:.3%} "
            f"under="
            f"{point['under_count']} "
            f"over="
            f"{point['over_count']}"
        )

    print("=" * 175)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()