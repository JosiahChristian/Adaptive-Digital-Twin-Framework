import csv
import statistics
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor

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
    "learned_lexicographic_consequence_equivalent_operating_point_selection.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "learned_lexicographic_consequence_equivalent_operating_point_selection_contexts.csv"
)

BASE_GENERATION_SEED = 44000

TEST_FRACTION = 0.30
META_FRACTION = 0.30

RISK_LEVELS = [
    0.00,
    0.10,
    0.25,
    1.00,
]

EPSILON_VALUES = [
    0.0000,
    0.0001,
    0.0005,
    0.0010,
    0.0025,
    0.0050,
    0.0100,
]

RANDOM_STATE = 42
FLOAT_TOLERANCE = 1e-12


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

    meta_start = int(
        len(development_rows)
        * (
            1.0
            - META_FRACTION
        )
    )

    base_train_rows = development_rows[
        :meta_start
    ]

    meta_train_rows = development_rows[
        meta_start:
    ]

    return (
        base_train_rows,
        meta_train_rows,
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


def candidate_predictions(
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict[
    float,
    list[int],
]:

    output = {
        0.00:
            direct_predictions(
                predicted_losses
            )
    }

    for risk_level in [
        0.10,
        0.25,
        1.00,
    ]:

        output[
            risk_level
        ] = adaptive_risk_predictions(
            predicted_losses,
            predicted_risks,
            risk_level,
        )

    return output


def train_regret_models(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict[
    float,
    RandomForestRegressor,
]:

    candidates = candidate_predictions(
        predicted_losses,
        predicted_risks,
    )

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

    models = {}

    for risk_level in (
        RISK_LEVELS
    ):

        y = [
            regret(
                row,
                candidates[
                    risk_level
                ][index],
            )
            for index, row in enumerate(
                rows
            )
        ]

        model = RandomForestRegressor(
            n_estimators=700,
            min_samples_leaf=2,
            random_state=(
                RANDOM_STATE
                + int(
                    risk_level
                    * 1000
                )
                + 1
            ),
        )

        model.fit(
            x,
            y,
        )

        models[
            risk_level
        ] = model

    return models


def predicted_regret_table(
    models: dict[
        float,
        RandomForestRegressor,
    ],
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> list[dict]:

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

    arrays = {
        risk_level:
            models[
                risk_level
            ].predict(
                x
            )
        for risk_level
        in RISK_LEVELS
    }

    output = []

    for index in range(
        len(rows)
    ):

        output.append(
            {
                risk_level:
                    max(
                        0.0,
                        float(
                            arrays[
                                risk_level
                            ][index]
                        ),
                    )
                for risk_level
                in RISK_LEVELS
            }
        )

    return output


def predicted_equivalence_set(
    predicted_regret_row: dict,
    epsilon: float,
) -> list[float]:

    minimum = min(
        predicted_regret_row.values()
    )

    return [
        risk_level
        for risk_level
        in RISK_LEVELS
        if (
            predicted_regret_row[
                risk_level
            ]
            <= (
                minimum
                + epsilon
                + FLOAT_TOLERANCE
            )
        )
    ]


def lexicographic_risk_levels(
    predicted_regrets: list[dict],
    epsilon: float,
) -> tuple[
    list[float],
    list[int],
]:

    selected_levels = []
    class_sizes = []

    for row in predicted_regrets:

        equivalent = (
            predicted_equivalence_set(
                row,
                epsilon,
            )
        )

        selected_levels.append(
            min(
                equivalent
            )
        )

        class_sizes.append(
            len(
                equivalent
            )
        )

    return (
        selected_levels,
        class_sizes,
    )


def actions_from_selected_risk(
    selected_risk_levels: list[float],
    candidates: dict[
        float,
        list[int],
    ],
) -> list[int]:

    return [
        int(
            candidates[
                risk_level
            ][index]
        )
        for index, risk_level in enumerate(
            selected_risk_levels
        )
    ]


def true_regret_table(
    rows: list[dict],
    candidates: dict[
        float,
        list[int],
    ],
) -> list[dict]:

    output = []

    for index, row in enumerate(
        rows
    ):

        output.append(
            {
                risk_level:
                    regret(
                        row,
                        candidates[
                            risk_level
                        ][index],
                    )
                for risk_level
                in RISK_LEVELS
            }
        )

    return output


def true_minimum_equivalence_set(
    regret_row: dict,
) -> list[float]:

    minimum = min(
        regret_row.values()
    )

    return [
        risk_level
        for risk_level
        in RISK_LEVELS
        if abs(
            regret_row[
                risk_level
            ]
            - minimum
        )
        <= FLOAT_TOLERANCE
    ]


def oracle_responsive_levels(
    true_regrets: list[dict],
) -> tuple[
    list[float],
    list[int],
]:

    levels = []
    sizes = []

    for row in true_regrets:

        equivalent = (
            true_minimum_equivalence_set(
                row
            )
        )

        levels.append(
            min(
                equivalent
            )
        )

        sizes.append(
            len(
                equivalent
            )
        )

    return (
        levels,
        sizes,
    )


def equivalence_recovery_metrics(
    selected_levels: list[float],
    predicted_class_sizes: list[int],
    true_regrets: list[dict],
) -> dict:

    in_true_minimum_set = 0
    exact_responsive_choice = 0

    true_class_size_total = 0
    predicted_class_size_total = 0

    responsive_oracle_levels = []

    for (
        selected,
        predicted_size,
        true_row,
    ) in zip(
        selected_levels,
        predicted_class_sizes,
        true_regrets,
    ):

        true_set = (
            true_minimum_equivalence_set(
                true_row
            )
        )

        responsive_oracle = min(
            true_set
        )

        responsive_oracle_levels.append(
            responsive_oracle
        )

        if selected in true_set:

            in_true_minimum_set += 1

        if (
            selected
            == responsive_oracle
        ):

            exact_responsive_choice += 1

        true_class_size_total += len(
            true_set
        )

        predicted_class_size_total += (
            predicted_size
        )

    count = len(
        selected_levels
    )

    return {
        "minimum_set_recovery":
            (
                in_true_minimum_set
                / count
            ),

        "responsive_oracle_accuracy":
            (
                exact_responsive_choice
                / count
            ),

        "mean_true_class_size":
            (
                true_class_size_total
                / count
            ),

        "mean_predicted_class_size":
            (
                predicted_class_size_total
                / count
            ),

        "mean_selected_lambda":
            statistics.mean(
                selected_levels
            ),

        "mean_responsive_oracle_lambda":
            statistics.mean(
                responsive_oracle_levels
            ),
    }


def save_csv(
    path: Path,
    rows: list[dict],
) -> None:

    path.parent.mkdir(
        exist_ok=True
    )

    if not rows:
        return

    fields = []

    for row in rows:

        for key in row.keys():

            if key not in fields:

                fields.append(
                    key
                )

    for row in rows:

        for field in fields:

            row.setdefault(
                field,
                ""
            )

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )

        writer.writeheader()
        writer.writerows(
            rows
        )


def print_policy_result(
    result: dict,
) -> None:

    print(
        f"{result['policy']:<30} "
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


def main() -> None:

    rows = generate_analysis_rows(
        base_seed=BASE_GENERATION_SEED
    )

    (
        base_train_rows,
        meta_train_rows,
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

    meta_losses = predicted_loss_table(
        loss_models,
        meta_train_rows,
    )

    meta_risks = predict_two_stage_risk(
        occurrence_model,
        magnitude_model,
        meta_train_rows,
    )

    regret_models = train_regret_models(
        meta_train_rows,
        meta_losses,
        meta_risks,
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

    predicted_regrets = (
        predicted_regret_table(
            regret_models,
            test_rows,
            test_losses,
            test_risks,
        )
    )

    true_regrets = true_regret_table(
        test_rows,
        candidates,
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

    context_rows = []

    for epsilon in (
        EPSILON_VALUES
    ):

        (
            selected_levels,
            predicted_class_sizes,
        ) = lexicographic_risk_levels(
            predicted_regrets,
            epsilon,
        )

        selected_actions = (
            actions_from_selected_risk(
                selected_levels,
                candidates,
            )
        )

        recovery = (
            equivalence_recovery_metrics(
                selected_levels,
                predicted_class_sizes,
                true_regrets,
            )
        )

        result = evaluate_policy(
            name=(
                "lexicographic_epsilon_"
                f"{epsilon:.4f}"
            ),
            predictions=selected_actions,
            rows=test_rows,
            direct=direct,
        )

        result[
            "epsilon"
        ] = epsilon

        result[
            "mean_selected_lambda"
        ] = recovery[
            "mean_selected_lambda"
        ]

        result[
            "minimum_set_recovery"
        ] = recovery[
            "minimum_set_recovery"
        ]

        result[
            "responsive_oracle_accuracy"
        ] = recovery[
            "responsive_oracle_accuracy"
        ]

        result[
            "mean_true_class_size"
        ] = recovery[
            "mean_true_class_size"
        ]

        result[
            "mean_predicted_class_size"
        ] = recovery[
            "mean_predicted_class_size"
        ]

        result[
            "mean_responsive_oracle_lambda"
        ] = recovery[
            "mean_responsive_oracle_lambda"
        ]

        evaluations.append(
            result
        )

        for index, (
            row,
            selected_level,
            predicted_size,
        ) in enumerate(
            zip(
                test_rows,
                selected_levels,
                predicted_class_sizes,
            )
        ):

            predicted_set = (
                predicted_equivalence_set(
                    predicted_regrets[
                        index
                    ],
                    epsilon,
                )
            )

            true_set = (
                true_minimum_equivalence_set(
                    true_regrets[
                        index
                    ]
                )
            )

            selected_action = int(
                candidates[
                    selected_level
                ][index]
            )

            context_rows.append(
                {
                    "epsilon":
                        epsilon,

                    "test_index":
                        index,

                    "best_persistence":
                        int(
                            row[
                                "best_persistence"
                            ]
                        ),

                    "predicted_under_risk":
                        float(
                            test_risks[
                                index
                            ]
                        ),

                    "selected_lambda":
                        selected_level,

                    "selected_action":
                        selected_action,

                    "selected_regret":
                        regret(
                            row,
                            selected_action,
                        ),

                    "predicted_class_size":
                        predicted_size,

                    "predicted_equivalence_set":
                        "|".join(
                            f"{level:.2f}"
                            for level
                            in predicted_set
                        ),

                    "true_minimum_set":
                        "|".join(
                            f"{level:.2f}"
                            for level
                            in true_set
                        ),

                    "selected_in_true_minimum_set":
                        int(
                            selected_level
                            in true_set
                        ),

                    "responsive_oracle_lambda":
                        min(
                            true_set
                        ),

                    "responsive_oracle_match":
                        int(
                            selected_level
                            == min(
                                true_set
                            )
                        ),

                    "predicted_regret_0.00":
                        predicted_regrets[
                            index
                        ][
                            0.00
                        ],

                    "predicted_regret_0.10":
                        predicted_regrets[
                            index
                        ][
                            0.10
                        ],

                    "predicted_regret_0.25":
                        predicted_regrets[
                            index
                        ][
                            0.25
                        ],

                    "predicted_regret_1.00":
                        predicted_regrets[
                            index
                        ][
                            1.00
                        ],
                }
            )

    (
        oracle_levels,
        oracle_class_sizes,
    ) = oracle_responsive_levels(
        true_regrets
    )

    oracle_actions = (
        actions_from_selected_risk(
            oracle_levels,
            candidates,
        )
    )

    oracle_result = evaluate_policy(
        name="oracle_equivalence",
        predictions=oracle_actions,
        rows=test_rows,
        direct=direct,
    )

    oracle_result[
        "epsilon"
    ] = 0.0

    oracle_result[
        "mean_selected_lambda"
    ] = statistics.mean(
        oracle_levels
    )

    oracle_result[
        "minimum_set_recovery"
    ] = 1.0

    oracle_result[
        "responsive_oracle_accuracy"
    ] = 1.0

    oracle_result[
        "mean_true_class_size"
    ] = statistics.mean(
        oracle_class_sizes
    )

    oracle_result[
        "mean_predicted_class_size"
    ] = ""

    oracle_result[
        "mean_responsive_oracle_lambda"
    ] = statistics.mean(
        oracle_levels
    )

    evaluations.append(
        oracle_result
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

    save_csv(
        OUTPUT_PATH,
        evaluations,
    )

    save_csv(
        CONTEXT_OUTPUT_PATH,
        context_rows,
    )

    print("=" * 185)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "LEARNED LEXICOGRAPHIC "
        "CONSEQUENCE-EQUIVALENT "
        "OPERATING-POINT SELECTION"
    )

    print("=" * 185)

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
        f"regret-model contexts="
        f"{len(meta_train_rows)}"
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
        "LEXICOGRAPHIC RECOVERY SWEEP"
    )

    for result in evaluations:

        if not result[
            "policy"
        ].startswith(
            "lexicographic_epsilon_"
        ):

            continue

        print(
            f"epsilon="
            f"{float(result['epsilon']):.4f} "
            f"mean_lambda="
            f"{float(result['mean_selected_lambda']):.4f} "
            f"mean_predicted_class="
            f"{float(result['mean_predicted_class_size']):.3f} "
            f"minimum_set_recovery="
            f"{float(result['minimum_set_recovery']):.3%} "
            f"responsive_oracle_accuracy="
            f"{float(result['responsive_oracle_accuracy']):.3%} "
            f"regret="
            f"{result['mean_regret']:.6f} "
            f"under="
            f"{result['under_count']} "
            f"over="
            f"{result['over_count']} "
            f"entropy="
            f"{result['action_entropy']:.3f}"
        )

    print()

    print(
        "ORACLE EQUIVALENCE BENCHMARK"
    )

    print(
        f"mean_lambda="
        f"{statistics.mean(oracle_levels):.4f} "
        f"mean_true_class="
        f"{statistics.mean(oracle_class_sizes):.3f} "
        f"regret="
        f"{oracle_result['mean_regret']:.6f} "
        f"under="
        f"{oracle_result['under_count']} "
        f"over="
        f"{oracle_result['over_count']} "
        f"entropy="
        f"{oracle_result['action_entropy']:.3f}"
    )

    print("=" * 185)

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