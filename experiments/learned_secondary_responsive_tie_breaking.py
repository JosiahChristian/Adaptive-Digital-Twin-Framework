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
    "learned_secondary_responsive_tie_breaking.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "learned_secondary_responsive_tie_breaking_contexts.csv"
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

# Experiment 071 showed that this was the
# largest tested predicted-regret tolerance
# that preserved observed regret and
# under-persistence.
PRIMARY_EPSILON = 0.0005

SECONDARY_SAFETY_THRESHOLDS = [
    0.50,
    0.60,
    0.70,
    0.80,
    0.90,
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


def candidate_specific_features(
    row: dict,
    predicted_risk: float,
    predicted_losses: dict,
    risk_level: float,
    candidate_action: int,
) -> list[float]:

    base = feature_vector(
        row,
        predicted_risk,
        predicted_losses,
    )

    return (
        base
        + [
            float(
                risk_level
            ),
            float(
                candidate_action
            ),
            float(
                candidate_action - 1
            ),
            float(
                3 - candidate_action
            ),
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


def true_minimum_set(
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

    predictions = {
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
                            predictions[
                                risk_level
                            ][index]
                        ),
                    )
                for risk_level
                in RISK_LEVELS
            }
        )

    return output


def predicted_safe_set(
    predicted_regret_row: dict,
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
                + PRIMARY_EPSILON
                + FLOAT_TOLERANCE
            )
        )
    ]


def train_secondary_safety_models(
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

    true_regrets = true_regret_table(
        rows,
        candidates,
    )

    models = {}

    for risk_level in (
        RISK_LEVELS
    ):

        x = []

        y = []

        for index, row in enumerate(
            rows
        ):

            x.append(
                candidate_specific_features(
                    row,
                    predicted_risks[
                        index
                    ],
                    predicted_losses[
                        index
                    ],
                    risk_level,
                    candidates[
                        risk_level
                    ][index],
                )
            )

            minimum_set = (
                true_minimum_set(
                    true_regrets[
                        index
                    ]
                )
            )

            y.append(
                1.0
                if risk_level
                in minimum_set
                else 0.0
            )

        model = RandomForestRegressor(
            n_estimators=700,
            min_samples_leaf=2,
            random_state=(
                RANDOM_STATE
                + 5000
                + int(
                    risk_level
                    * 1000
                )
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


def predict_secondary_safety(
    models: dict[
        float,
        RandomForestRegressor,
    ],
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
    candidates: dict[
        float,
        list[int],
    ],
) -> list[dict]:

    output = [
        {}
        for _ in rows
    ]

    for risk_level in (
        RISK_LEVELS
    ):

        x = [
            candidate_specific_features(
                row,
                predicted_risks[
                    index
                ],
                predicted_losses[
                    index
                ],
                risk_level,
                candidates[
                    risk_level
                ][index],
            )
            for index, row in enumerate(
                rows
            )
        ]

        predictions = models[
            risk_level
        ].predict(
            x
        )

        for index, value in enumerate(
            predictions
        ):

            output[
                index
            ][
                risk_level
            ] = min(
                1.0,
                max(
                    0.0,
                    float(
                        value
                    ),
                ),
            )

    return output


def baseline_lexicographic_levels(
    predicted_regrets: list[dict],
) -> tuple[
    list[float],
    list[int],
]:

    levels = []
    sizes = []

    for row in predicted_regrets:

        safe_set = predicted_safe_set(
            row
        )

        levels.append(
            min(
                safe_set
            )
        )

        sizes.append(
            len(
                safe_set
            )
        )

    return (
        levels,
        sizes,
    )


def secondary_selected_levels(
    predicted_regrets: list[dict],
    predicted_safety: list[dict],
    threshold: float,
) -> tuple[
    list[float],
    list[int],
    list[int],
]:

    selected_levels = []

    safe_set_sizes = []

    secondary_feasible_sizes = []

    for (
        regret_row,
        safety_row,
    ) in zip(
        predicted_regrets,
        predicted_safety,
    ):

        primary_set = predicted_safe_set(
            regret_row
        )

        safe_set_sizes.append(
            len(
                primary_set
            )
        )

        secondary_feasible = [
            risk_level
            for risk_level
            in primary_set
            if (
                safety_row[
                    risk_level
                ]
                >= threshold
            )
        ]

        secondary_feasible_sizes.append(
            len(
                secondary_feasible
            )
        )

        if secondary_feasible:

            selected = min(
                secondary_feasible
            )

        else:

            # If the secondary model is not confident
            # about any candidate, preserve the primary
            # consequence objective by selecting the
            # minimum predicted-regret member.
            selected = min(
                primary_set,
                key=lambda risk_level: (
                    regret_row[
                        risk_level
                    ],
                    risk_level,
                ),
            )

        selected_levels.append(
            selected
        )

    return (
        selected_levels,
        safe_set_sizes,
        secondary_feasible_sizes,
    )


def actions_from_levels(
    levels: list[float],
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
        for index, risk_level
        in enumerate(
            levels
        )
    ]


def recovery_metrics(
    levels: list[float],
    true_regrets: list[dict],
) -> dict:

    minimum_set_hits = 0

    responsive_oracle_hits = 0

    responsive_oracle_levels = []

    for (
        selected,
        regret_row,
    ) in zip(
        levels,
        true_regrets,
    ):

        minimum_set = true_minimum_set(
            regret_row
        )

        responsive_oracle = min(
            minimum_set
        )

        responsive_oracle_levels.append(
            responsive_oracle
        )

        if selected in minimum_set:

            minimum_set_hits += 1

        if selected == responsive_oracle:

            responsive_oracle_hits += 1

    count = len(
        levels
    )

    return {
        "minimum_set_recovery":
            minimum_set_hits
            / count,

        "responsive_oracle_accuracy":
            responsive_oracle_hits
            / count,

        "mean_selected_lambda":
            statistics.mean(
                levels
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
        f"{result['policy']:<34} "
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

    secondary_models = (
        train_secondary_safety_models(
            meta_train_rows,
            meta_losses,
            meta_risks,
        )
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

    predicted_safety = (
        predict_secondary_safety(
            secondary_models,
            test_rows,
            test_losses,
            test_risks,
            candidates,
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

    (
        baseline_levels,
        baseline_class_sizes,
    ) = baseline_lexicographic_levels(
        predicted_regrets
    )

    baseline_actions = actions_from_levels(
        baseline_levels,
        candidates,
    )

    baseline_recovery = recovery_metrics(
        baseline_levels,
        true_regrets,
    )

    baseline_result = evaluate_policy(
        name="lexicographic_baseline",
        predictions=baseline_actions,
        rows=test_rows,
        direct=direct,
    )

    baseline_result[
        "secondary_threshold"
    ] = ""

    baseline_result[
        "mean_selected_lambda"
    ] = baseline_recovery[
        "mean_selected_lambda"
    ]

    baseline_result[
        "minimum_set_recovery"
    ] = baseline_recovery[
        "minimum_set_recovery"
    ]

    baseline_result[
        "responsive_oracle_accuracy"
    ] = baseline_recovery[
        "responsive_oracle_accuracy"
    ]

    baseline_result[
        "mean_primary_class_size"
    ] = statistics.mean(
        baseline_class_sizes
    )

    baseline_result[
        "mean_secondary_feasible_size"
    ] = ""

    evaluations.append(
        baseline_result
    )

    context_rows = []

    for threshold in (
        SECONDARY_SAFETY_THRESHOLDS
    ):

        (
            selected_levels,
            primary_sizes,
            secondary_sizes,
        ) = secondary_selected_levels(
            predicted_regrets,
            predicted_safety,
            threshold,
        )

        selected_actions = actions_from_levels(
            selected_levels,
            candidates,
        )

        recovery = recovery_metrics(
            selected_levels,
            true_regrets,
        )

        result = evaluate_policy(
            name=(
                "secondary_threshold_"
                f"{threshold:.2f}"
            ),
            predictions=selected_actions,
            rows=test_rows,
            direct=direct,
        )

        result[
            "secondary_threshold"
        ] = threshold

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
            "mean_primary_class_size"
        ] = statistics.mean(
            primary_sizes
        )

        result[
            "mean_secondary_feasible_size"
        ] = statistics.mean(
            secondary_sizes
        )

        evaluations.append(
            result
        )

        for index, row in enumerate(
            test_rows
        ):

            primary_set = predicted_safe_set(
                predicted_regrets[
                    index
                ]
            )

            true_set = true_minimum_set(
                true_regrets[
                    index
                ]
            )

            selected_level = selected_levels[
                index
            ]

            selected_action = selected_actions[
                index
            ]

            context_rows.append(
                {
                    "secondary_threshold":
                        threshold,

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

                    "primary_safe_set":
                        "|".join(
                            f"{level:.2f}"
                            for level
                            in primary_set
                        ),

                    "primary_safe_set_size":
                        len(
                            primary_set
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

                    "true_minimum_set":
                        "|".join(
                            f"{level:.2f}"
                            for level
                            in true_set
                        ),

                    "responsive_oracle_lambda":
                        min(
                            true_set
                        ),

                    "selected_in_true_minimum_set":
                        int(
                            selected_level
                            in true_set
                        ),

                    "responsive_oracle_match":
                        int(
                            selected_level
                            == min(
                                true_set
                            )
                        ),

                    "safety_score_0.00":
                        predicted_safety[
                            index
                        ][
                            0.00
                        ],

                    "safety_score_0.10":
                        predicted_safety[
                            index
                        ][
                            0.10
                        ],

                    "safety_score_0.25":
                        predicted_safety[
                            index
                        ][
                            0.25
                        ],

                    "safety_score_1.00":
                        predicted_safety[
                            index
                        ][
                            1.00
                        ],
                }
            )

    oracle_levels = [
        min(
            true_minimum_set(
                regret_row
            )
        )
        for regret_row
        in true_regrets
    ]

    oracle_actions = actions_from_levels(
        oracle_levels,
        candidates,
    )

    oracle_result = evaluate_policy(
        name="oracle_equivalence",
        predictions=oracle_actions,
        rows=test_rows,
        direct=direct,
    )

    oracle_result[
        "secondary_threshold"
    ] = ""

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
        "mean_primary_class_size"
    ] = ""

    oracle_result[
        "mean_secondary_feasible_size"
    ] = ""

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

    print("=" * 190)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "LEARNED SECONDARY RESPONSIVE "
        "TIE-BREAKING"
    )

    print("=" * 190)

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
        f"secondary-training contexts="
        f"{len(meta_train_rows)}"
    )

    print(
        f"test contexts="
        f"{len(test_rows)}"
    )

    print(
        f"primary epsilon="
        f"{PRIMARY_EPSILON:.4f}"
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
        "SECONDARY TIE-BREAKING SWEEP"
    )

    print(
        "baseline "
        f"mean_lambda="
        f"{baseline_recovery['mean_selected_lambda']:.4f} "
        f"minimum_set_recovery="
        f"{baseline_recovery['minimum_set_recovery']:.3%} "
        f"responsive_oracle_accuracy="
        f"{baseline_recovery['responsive_oracle_accuracy']:.3%} "
        f"mean_primary_size="
        f"{statistics.mean(baseline_class_sizes):.3f} "
        f"regret="
        f"{baseline_result['mean_regret']:.6f} "
        f"entropy="
        f"{baseline_result['action_entropy']:.3f}"
    )

    for result in evaluations:

        if not result[
            "policy"
        ].startswith(
            "secondary_threshold_"
        ):

            continue

        print(
            f"threshold="
            f"{float(result['secondary_threshold']):.2f} "
            f"mean_lambda="
            f"{float(result['mean_selected_lambda']):.4f} "
            f"minimum_set_recovery="
            f"{float(result['minimum_set_recovery']):.3%} "
            f"responsive_oracle_accuracy="
            f"{float(result['responsive_oracle_accuracy']):.3%} "
            f"mean_primary_size="
            f"{float(result['mean_primary_class_size']):.3f} "
            f"mean_secondary_size="
            f"{float(result['mean_secondary_feasible_size']):.3f} "
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
        f"regret="
        f"{oracle_result['mean_regret']:.6f} "
        f"under="
        f"{oracle_result['under_count']} "
        f"over="
        f"{oracle_result['over_count']} "
        f"entropy="
        f"{oracle_result['action_entropy']:.3f}"
    )

    print("=" * 190)

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