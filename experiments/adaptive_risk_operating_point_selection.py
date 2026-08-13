import csv
import statistics
from collections import Counter
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier

from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)
from experiments.responsiveness_preserving_safe_persistence_control import (
    FEATURE_NAMES,
    train_loss_models,
    train_occurrence_model,
    train_magnitude_model,
    predicted_loss_table,
    predict_two_stage_risk,
    adaptive_risk_predictions,
    direct_predictions,
    fixed_predictions,
    oracle_predictions,
    evaluate_policy,
)


OUTPUT_PATH = Path(
    "results/"
    "adaptive_risk_operating_point_selection.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "adaptive_risk_operating_point_selection_contexts.csv"
)

BASE_GENERATION_SEED = 44000

TEST_FRACTION = 0.30
SELECTOR_FRACTION = 0.30

RISK_LEVELS = [
    0.00,
    0.10,
    0.25,
    1.00,
]

RANDOM_STATE = 42


def feature_vector(
    row: dict,
    predicted_risk: float,
    predicted_losses: dict,
) -> list[float]:

    base_features = [
        float(
            row[name]
        )
        for name in FEATURE_NAMES
    ]

    loss_k1 = float(
        predicted_losses[1]
    )

    loss_k2 = float(
        predicted_losses[2]
    )

    loss_k3 = float(
        predicted_losses[3]
    )

    return (
        base_features
        + [
            float(
                predicted_risk
            ),
            loss_k1,
            loss_k2,
            loss_k3,
            loss_k1 - loss_k2,
            loss_k1 - loss_k3,
            loss_k2 - loss_k3,
        ]
    )


def three_way_split(
    rows: list[dict],
) -> tuple[
    list[dict],
    list[dict],
    list[dict],
]:

    test_start = int(
        len(rows)
        * (
            1.0
            - TEST_FRACTION
        )
    )

    development_rows = rows[
        :test_start
    ]

    test_rows = rows[
        test_start:
    ]

    selector_start = int(
        len(development_rows)
        * (
            1.0
            - SELECTOR_FRACTION
        )
    )

    base_train_rows = development_rows[
        :selector_start
    ]

    selector_train_rows = development_rows[
        selector_start:
    ]

    return (
        base_train_rows,
        selector_train_rows,
        test_rows,
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


def candidate_predictions(
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict[
    float,
    list[int],
]:

    output = {}

    for risk_level in (
        RISK_LEVELS
    ):

        if risk_level == 0.0:

            output[
                risk_level
            ] = direct_predictions(
                predicted_losses
            )

        else:

            output[
                risk_level
            ] = adaptive_risk_predictions(
                predicted_losses,
                predicted_risks,
                risk_level,
            )

    return output


def best_risk_level_for_context(
    row: dict,
    index: int,
    candidates: dict[
        float,
        list[int],
    ],
) -> float:

    results = []

    for risk_level in (
        RISK_LEVELS
    ):

        persistence = candidates[
            risk_level
        ][index]

        context_regret = regret(
            row,
            persistence,
        )

        results.append(
            (
                context_regret,
                risk_level,
            )
        )

    return min(
        results,
        key=lambda value: (
            value[0],
            value[1],
        ),
    )[1]


def build_selector_training_data(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> tuple[
    list[list[float]],
    list[int],
]:

    candidates = candidate_predictions(
        predicted_losses,
        predicted_risks,
    )

    x = []
    y = []

    for index, row in enumerate(
        rows
    ):

        x.append(
            feature_vector(
                row,
                predicted_risks[
                    index
                ],
                predicted_losses[
                    index
                ],
            )
        )

        best_level = (
            best_risk_level_for_context(
                row,
                index,
                candidates,
            )
        )

        y.append(
            RISK_LEVELS.index(
                best_level
            )
        )

    return (
        x,
        y,
    )


def train_selector(
    x: list[list[float]],
    y: list[int],
) -> RandomForestClassifier:

    model = RandomForestClassifier(
        n_estimators=600,
        min_samples_leaf=2,
        random_state=RANDOM_STATE,
        class_weight="balanced",
    )

    model.fit(
        x,
        y,
    )

    return model


def predict_risk_levels(
    model: RandomForestClassifier,
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> list[float]:

    x = [
        feature_vector(
            row,
            predicted_risk,
            loss_row,
        )
        for (
            row,
            predicted_risk,
            loss_row,
        ) in zip(
            rows,
            predicted_risks,
            predicted_losses,
        )
    ]

    predicted_classes = (
        model.predict(
            x
        )
    )

    return [
        RISK_LEVELS[
            int(
                class_index
            )
        ]
        for class_index
        in predicted_classes
    ]


def actions_from_selected_risk(
    selected_risk_levels: list[float],
    candidates: dict[
        float,
        list[int],
    ],
) -> list[int]:

    actions = []

    for index, risk_level in enumerate(
        selected_risk_levels
    ):

        actions.append(
            int(
                candidates[
                    risk_level
                ][index]
            )
        )

    return actions


def oracle_risk_level_predictions(
    rows: list[dict],
    candidates: dict[
        float,
        list[int],
    ],
) -> list[float]:

    return [
        best_risk_level_for_context(
            row,
            index,
            candidates,
        )
        for index, row in enumerate(
            rows
        )
    ]


def evaluate_risk_selector(
    predicted_levels: list[float],
    oracle_levels: list[float],
) -> dict:

    exact = sum(
        predicted
        == actual
        for (
            predicted,
            actual,
        ) in zip(
            predicted_levels,
            oracle_levels,
        )
    )

    return {
        "selector_accuracy":
            exact
            / len(
                oracle_levels
            ),

        "predicted_mean_risk_level":
            statistics.mean(
                predicted_levels
            ),

        "oracle_mean_risk_level":
            statistics.mean(
                oracle_levels
            ),
    }


def save_policy_results(
    rows: list[dict],
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
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(
            rows
        )


def save_context_results(
    rows: list[dict],
) -> None:

    CONTEXT_OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )

    with CONTEXT_OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(
            rows
        )


def print_policy_result(
    result: dict,
) -> None:

    print(
        f"{result['policy']:<24} "
        f"mean_regret="
        f"{result['mean_regret']:.6f} "
        f"zero_regret="
        f"{result['zero_regret_fraction']:.3%} "
        f"regret>0.005="
        f"{result['regret_gt_0_005_fraction']:.3%} "
        f"under="
        f"{result['under_count']:<2} "
        f"over="
        f"{result['over_count']:<2} "
        f"entropy="
        f"{result['action_entropy']:.3f} "
        f"dominant="
        f"{result['dominant_action_fraction']:.3%}"
    )


def print_risk_distribution(
    label: str,
    values: list[float],
) -> None:

    counts = Counter(
        values
    )

    print(
        label
    )

    for risk_level in (
        RISK_LEVELS
    ):

        count = counts[
            risk_level
        ]

        print(
            f"  lambda="
            f"{risk_level:.2f}: "
            f"{count} "
            f"({count / len(values):.3%})"
        )


def main() -> None:

    rows = generate_analysis_rows(
        base_seed=BASE_GENERATION_SEED
    )

    (
        base_train_rows,
        selector_train_rows,
        test_rows,
    ) = three_way_split(
        rows
    )

    loss_models = train_loss_models(
        base_train_rows
    )

    occurrence_model = (
        train_occurrence_model(
            base_train_rows
        )
    )

    magnitude_model = (
        train_magnitude_model(
            base_train_rows
        )
    )

    selector_losses = (
        predicted_loss_table(
            loss_models,
            selector_train_rows,
        )
    )

    selector_risks = (
        predict_two_stage_risk(
            occurrence_model,
            magnitude_model,
            selector_train_rows,
        )
    )

    (
        selector_x,
        selector_y,
    ) = build_selector_training_data(
        selector_train_rows,
        selector_losses,
        selector_risks,
    )

    selector_model = train_selector(
        selector_x,
        selector_y,
    )

    test_losses = predicted_loss_table(
        loss_models,
        test_rows,
    )

    test_risks = predict_two_stage_risk(
        occurrence_model,
        magnitude_model,
        test_rows,
    )

    candidates = candidate_predictions(
        test_losses,
        test_risks,
    )

    selected_risk_levels = (
        predict_risk_levels(
            selector_model,
            test_rows,
            test_losses,
            test_risks,
        )
    )

    adaptive_actions = (
        actions_from_selected_risk(
            selected_risk_levels,
            candidates,
        )
    )

    oracle_risk_levels = (
        oracle_risk_level_predictions(
            test_rows,
            candidates,
        )
    )

    oracle_operating_actions = (
        actions_from_selected_risk(
            oracle_risk_levels,
            candidates,
        )
    )

    direct = candidates[
        0.00
    ]

    evaluations = []

    evaluations.append(
        evaluate_policy(
            name="direct_loss",
            predictions=direct,
            rows=test_rows,
            direct=direct,
        )
    )

    for risk_level in [
        0.10,
        0.25,
        1.00,
    ]:

        evaluations.append(
            evaluate_policy(
                name=(
                    "fixed_lambda_"
                    f"{risk_level:.2f}"
                ),
                predictions=candidates[
                    risk_level
                ],
                rows=test_rows,
                direct=direct,
            )
        )

    evaluations.append(
        evaluate_policy(
            name="adaptive_lambda",
            predictions=adaptive_actions,
            rows=test_rows,
            direct=direct,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="oracle_lambda",
            predictions=oracle_operating_actions,
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
            name="action_oracle",
            predictions=oracle_predictions(
                test_rows
            ),
            rows=test_rows,
            direct=direct,
        )
    )

    selector_metrics = (
        evaluate_risk_selector(
            selected_risk_levels,
            oracle_risk_levels,
        )
    )

    for result in evaluations:

        result[
            "selector_accuracy"
        ] = selector_metrics[
            "selector_accuracy"
        ]

        result[
            "predicted_mean_risk_level"
        ] = selector_metrics[
            "predicted_mean_risk_level"
        ]

        result[
            "oracle_mean_risk_level"
        ] = selector_metrics[
            "oracle_mean_risk_level"
        ]

    context_rows = []

    for index, (
        row,
        selected_level,
        oracle_level,
        selected_action,
        oracle_action,
    ) in enumerate(
        zip(
            test_rows,
            selected_risk_levels,
            oracle_risk_levels,
            adaptive_actions,
            oracle_operating_actions,
        )
    ):

        context_rows.append(
            {
                "test_index":
                    index,

                "best_persistence":
                    int(
                        row[
                            "best_persistence"
                        ]
                    ),

                "predicted_risk":
                    float(
                        test_risks[
                            index
                        ]
                    ),

                "selected_lambda":
                    selected_level,

                "oracle_lambda":
                    oracle_level,

                "selected_action":
                    selected_action,

                "oracle_lambda_action":
                    oracle_action,

                "selected_regret":
                    regret(
                        row,
                        selected_action,
                    ),

                "oracle_lambda_regret":
                    regret(
                        row,
                        oracle_action,
                    ),
            }
        )

    save_policy_results(
        evaluations
    )

    save_context_results(
        context_rows
    )

    print("=" * 170)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "ADAPTIVE RISK OPERATING-POINT "
        "SELECTION"
    )

    print("=" * 170)

    print(
        f"generation seed="
        f"{BASE_GENERATION_SEED}"
    )

    print(
        f"total contexts="
        f"{len(rows)}"
    )

    print(
        f"base-training contexts="
        f"{len(base_train_rows)}"
    )

    print(
        f"selector-training contexts="
        f"{len(selector_train_rows)}"
    )

    print(
        f"test contexts="
        f"{len(test_rows)}"
    )

    print()

    print(
        "RISK-LEVEL SELECTOR"
    )

    print(
        "selector accuracy="
        f"{selector_metrics['selector_accuracy']:.3%}"
    )

    print(
        "predicted mean lambda="
        f"{selector_metrics['predicted_mean_risk_level']:.4f}"
    )

    print(
        "oracle mean lambda="
        f"{selector_metrics['oracle_mean_risk_level']:.4f}"
    )

    print()

    print_risk_distribution(
        "Predicted operating-point distribution",
        selected_risk_levels,
    )

    print_risk_distribution(
        "Oracle operating-point distribution",
        oracle_risk_levels,
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
        f"Policy results saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Context results saved to: "
        f"{CONTEXT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()