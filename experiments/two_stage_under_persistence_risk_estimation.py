import csv
import statistics
from pathlib import Path

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
)

from experiments.adaptive_release_persistence_policy import (
    PERSISTENCE_LEVELS,
)
from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)


OUTPUT_PATH = Path(
    "results/"
    "two_stage_under_persistence_risk_estimation.csv"
)

RANDOM_STATE = 42
TEST_FRACTION = 0.30

FIXED_RISK_PENALTY = 0.010

ADAPTIVE_RISK_MULTIPLIERS = [
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
        true_under_persistence_risk(
            row
        )
        > 1e-12
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


def train_single_stage_risk_model(
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


def train_risk_occurrence_model(
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


def train_positive_risk_magnitude_model(
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
        true_under_persistence_risk(
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

    arrays = {}

    for persistence in (
        PERSISTENCE_LEVELS
    ):

        arrays[
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
        for value in model.predict(x)
    ]


def predict_two_stage_risk(
    occurrence_model: RandomForestClassifier,
    magnitude_model: RandomForestRegressor,
    rows: list[dict],
) -> tuple[
    list[float],
    list[float],
    list[float],
]:

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

    expected_risks = []

    for probability, magnitude in zip(
        probabilities,
        magnitudes,
    ):

        probability = float(
            probability
        )

        magnitude = max(
            0.0,
            float(
                magnitude
            ),
        )

        expected_risks.append(
            probability
            * magnitude
        )

    return (
        [
            float(value)
            for value in probabilities
        ],
        [
            max(
                0.0,
                float(value),
            )
            for value in magnitudes
        ],
        expected_risks,
    )


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

    for row, predicted_risk in zip(
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


def evaluate_risk_predictions(
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

    positive_pairs = [
        (
            actual,
            predicted,
        )
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
                positive_pairs
            ),

        "positive_risk_mae":
            (
                statistics.mean(
                    abs(
                        predicted
                        - actual
                    )
                    for actual, predicted
                    in positive_pairs
                )
                if positive_pairs
                else 0.0
            ),

        "mean_true_positive_risk":
            (
                statistics.mean(
                    actual
                    for actual, _
                    in positive_pairs
                )
                if positive_pairs
                else 0.0
            ),

        "mean_predicted_positive_risk":
            (
                statistics.mean(
                    predicted
                    for _, predicted
                    in positive_pairs
                )
                if positive_pairs
                else 0.0
            ),
    }


def evaluate_occurrence_model(
    rows: list[dict],
    probabilities: list[float],
) -> dict:

    true_labels = [
        positive_risk_label(
            row
        )
        for row in rows
    ]

    predicted_labels = [
        int(
            probability >= 0.5
        )
        for probability in probabilities
    ]

    return {
        "accuracy":
            accuracy_score(
                true_labels,
                predicted_labels,
            ),

        "precision":
            precision_score(
                true_labels,
                predicted_labels,
                zero_division=0,
            ),

        "recall":
            recall_score(
                true_labels,
                predicted_labels,
                zero_division=0,
            ),

        "predicted_positive":
            sum(
                predicted_labels
            ),

        "true_positive":
            sum(
                true_labels
            ),
    }


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


def print_risk_metrics(
    label: str,
    metrics: dict,
) -> None:

    print(
        label
    )

    print(
        "  mean true risk="
        f"{metrics['mean_true_risk']:.6f}"
    )

    print(
        "  mean predicted risk="
        f"{metrics['mean_predicted_risk']:.6f}"
    )

    print(
        "  risk MAE="
        f"{metrics['risk_mae']:.6f}"
    )

    print(
        "  positive-risk MAE="
        f"{metrics['positive_risk_mae']:.6f}"
    )

    print(
        "  mean true positive risk="
        f"{metrics['mean_true_positive_risk']:.6f}"
    )

    print(
        "  mean predicted positive risk="
        f"{metrics['mean_predicted_positive_risk']:.6f}"
    )


def print_policy_result(
    result: dict,
) -> None:

    print(
        f"{result['policy']:<32} "
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
        train_risk_occurrence_model(
            train_rows
        )
    )

    magnitude_model = (
        train_positive_risk_magnitude_model(
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

    (
        risk_probabilities,
        risk_magnitudes,
        two_stage_risks,
    ) = predict_two_stage_risk(
        occurrence_model,
        magnitude_model,
        test_rows,
    )

    single_stage_metrics = (
        evaluate_risk_predictions(
            test_rows,
            single_stage_risks,
        )
    )

    two_stage_metrics = (
        evaluate_risk_predictions(
            test_rows,
            two_stage_risks,
        )
    )

    occurrence_metrics = (
        evaluate_occurrence_model(
            test_rows,
            risk_probabilities,
        )
    )

    direct_predictions = (
        direct_loss_predictions(
            predicted_losses
        )
    )

    fixed_risk_predictions_values = (
        fixed_risk_predictions(
            predicted_losses,
            FIXED_RISK_PENALTY,
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
            name="direct_loss_model",
            predictions=direct_predictions,
            rows=test_rows,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="fixed_risk_0.010",
            predictions=fixed_risk_predictions_values,
            rows=test_rows,
        )
    )

    for multiplier in (
        ADAPTIVE_RISK_MULTIPLIERS
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
                    "single_stage_risk_"
                    f"{multiplier:.2f}"
                ),
                predictions=single_predictions,
                rows=test_rows,
            )
        )

        evaluations.append(
            evaluate_policy(
                name=(
                    "two_stage_risk_"
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

    print("=" * 170)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "TWO-STAGE UNDER-PERSISTENCE "
        "RISK ESTIMATION"
    )

    print("=" * 170)

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
        "RISK OCCURRENCE MODEL"
    )

    print(
        "accuracy="
        f"{occurrence_metrics['accuracy']:.3%}"
    )

    print(
        "precision="
        f"{occurrence_metrics['precision']:.3%}"
    )

    print(
        "recall="
        f"{occurrence_metrics['recall']:.3%}"
    )

    print(
        "true positive-risk contexts="
        f"{occurrence_metrics['true_positive']}"
    )

    print(
        "predicted positive-risk contexts="
        f"{occurrence_metrics['predicted_positive']}"
    )

    print()

    print(
        "RISK ESTIMATION COMPARISON"
    )

    print_risk_metrics(
        "Single-stage risk regression",
        single_stage_metrics,
    )

    print_risk_metrics(
        "Two-stage expected risk",
        two_stage_metrics,
    )

    print()

    print(
        "MEAN PREDICTED POSITIVE-RISK MAGNITUDE="
        f"{statistics.mean(risk_magnitudes):.6f}"
    )

    print()

    print(
        "POLICY PERFORMANCE"
    )

    for result in evaluations:

        print_policy_result(
            result
        )

    print("=" * 170)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()