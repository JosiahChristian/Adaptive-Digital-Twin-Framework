import csv
import statistics
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
    "learned_responsive_optimality_selection.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "learned_responsive_optimality_selection_contexts.csv"
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

PRIMARY_EPSILON = 0.0005

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

    return (
        feature_vector(
            row,
            predicted_risk,
            predicted_losses,
        )
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
) -> dict:

    from sklearn.ensemble import RandomForestRegressor

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
    models: dict,
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


def responsive_oracle_level(
    regret_row: dict,
) -> float:

    return min(
        true_minimum_set(
            regret_row
        )
    )


def train_responsive_optimality_models(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict[
    float,
    RandomForestClassifier,
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

            responsive_level = (
                responsive_oracle_level(
                    true_regrets[
                        index
                    ]
                )
            )

            y.append(
                int(
                    risk_level
                    == responsive_level
                )
            )

        model = RandomForestClassifier(
            n_estimators=700,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=(
                RANDOM_STATE
                + 7000
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


def positive_probability(
    model: RandomForestClassifier,
    x: list[list[float]],
) -> list[float]:

    probabilities = model.predict_proba(
        x
    )

    classes = list(
        model.classes_
    )

    if 1 not in classes:
        return [
            0.0
            for _ in x
        ]

    positive_index = classes.index(
        1
    )

    return [
        float(
            row[
                positive_index
            ]
        )
        for row in probabilities
    ]


def predict_responsive_scores(
    models: dict[
        float,
        RandomForestClassifier,
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

        scores = positive_probability(
            models[
                risk_level
            ],
            x,
        )

        for index, score in enumerate(
            scores
        ):

            output[
                index
            ][
                risk_level
            ] = score

    return output


def baseline_levels(
    predicted_regrets: list[dict],
) -> list[float]:

    return [
        min(
            predicted_safe_set(
                regret_row
            )
        )
        for regret_row
        in predicted_regrets
    ]


def responsive_model_levels(
    predicted_regrets: list[dict],
    responsive_scores: list[dict],
) -> list[float]:

    output = []

    for (
        regret_row,
        score_row,
    ) in zip(
        predicted_regrets,
        responsive_scores,
    ):

        safe_set = predicted_safe_set(
            regret_row
        )

        selected = max(
            safe_set,
            key=lambda risk_level: (
                score_row[
                    risk_level
                ],
                -risk_level,
            ),
        )

        output.append(
            selected
        )

    return output


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

    responsive_levels = []

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

        responsive_level = min(
            minimum_set
        )

        responsive_levels.append(
            responsive_level
        )

        if selected in minimum_set:
            minimum_set_hits += 1

        if selected == responsive_level:
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
                responsive_levels
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

    occurrence_model = train_occurrence_model(
        base_train_rows
    )

    magnitude_model = train_magnitude_model(
        base_train_rows
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

    responsive_models = (
        train_responsive_optimality_models(
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

    predicted_regrets = predicted_regret_table(
        regret_models,
        test_rows,
        test_losses,
        test_risks,
    )

    responsive_scores = (
        predict_responsive_scores(
            responsive_models,
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

    baseline = baseline_levels(
        predicted_regrets
    )

    baseline_actions = actions_from_levels(
        baseline,
        candidates,
    )

    baseline_recovery = recovery_metrics(
        baseline,
        true_regrets,
    )

    baseline_result = evaluate_policy(
        name="lexicographic_baseline",
        predictions=baseline_actions,
        rows=test_rows,
        direct=direct,
    )

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

    evaluations.append(
        baseline_result
    )

    responsive_levels = (
        responsive_model_levels(
            predicted_regrets,
            responsive_scores,
        )
    )

    responsive_actions = actions_from_levels(
        responsive_levels,
        candidates,
    )

    responsive_recovery = recovery_metrics(
        responsive_levels,
        true_regrets,
    )

    responsive_result = evaluate_policy(
        name="responsive_optimality_model",
        predictions=responsive_actions,
        rows=test_rows,
        direct=direct,
    )

    responsive_result[
        "mean_selected_lambda"
    ] = responsive_recovery[
        "mean_selected_lambda"
    ]

    responsive_result[
        "minimum_set_recovery"
    ] = responsive_recovery[
        "minimum_set_recovery"
    ]

    responsive_result[
        "responsive_oracle_accuracy"
    ] = responsive_recovery[
        "responsive_oracle_accuracy"
    ]

    evaluations.append(
        responsive_result
    )

    oracle_levels = [
        responsive_oracle_level(
            regret_row
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

    context_rows = []

    for index, row in enumerate(
        test_rows
    ):

        safe_set = predicted_safe_set(
            predicted_regrets[
                index
            ]
        )

        true_set = true_minimum_set(
            true_regrets[
                index
            ]
        )

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

                "predicted_under_risk":
                    float(
                        test_risks[
                            index
                        ]
                    ),

                "predicted_safe_set":
                    "|".join(
                        f"{level:.2f}"
                        for level
                        in safe_set
                    ),

                "true_minimum_set":
                    "|".join(
                        f"{level:.2f}"
                        for level
                        in true_set
                    ),

                "baseline_lambda":
                    baseline[
                        index
                    ],

                "responsive_model_lambda":
                    responsive_levels[
                        index
                    ],

                "responsive_oracle_lambda":
                    min(
                        true_set
                    ),

                "responsive_model_action":
                    responsive_actions[
                        index
                    ],

                "responsive_model_regret":
                    regret(
                        row,
                        responsive_actions[
                            index
                        ],
                    ),

                "responsive_model_in_true_set":
                    int(
                        responsive_levels[
                            index
                        ]
                        in true_set
                    ),

                "responsive_oracle_match":
                    int(
                        responsive_levels[
                            index
                        ]
                        == min(
                            true_set
                        )
                    ),

                "responsive_score_0.00":
                    responsive_scores[
                        index
                    ][
                        0.00
                    ],

                "responsive_score_0.10":
                    responsive_scores[
                        index
                    ][
                        0.10
                    ],

                "responsive_score_0.25":
                    responsive_scores[
                        index
                    ][
                        0.25
                    ],

                "responsive_score_1.00":
                    responsive_scores[
                        index
                    ][
                        1.00
                    ],
            }
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
        "LEARNED RESPONSIVE-OPTIMALITY "
        "SELECTION"
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
        f"responsive-training contexts="
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
        "RESPONSIVE SELECTION RECOVERY"
    )

    print(
        "baseline "
        f"mean_lambda="
        f"{baseline_recovery['mean_selected_lambda']:.4f} "
        f"minimum_set_recovery="
        f"{baseline_recovery['minimum_set_recovery']:.3%} "
        f"responsive_oracle_accuracy="
        f"{baseline_recovery['responsive_oracle_accuracy']:.3%} "
        f"regret="
        f"{baseline_result['mean_regret']:.6f} "
        f"entropy="
        f"{baseline_result['action_entropy']:.3f}"
    )

    print(
        "responsive model "
        f"mean_lambda="
        f"{responsive_recovery['mean_selected_lambda']:.4f} "
        f"minimum_set_recovery="
        f"{responsive_recovery['minimum_set_recovery']:.3%} "
        f"responsive_oracle_accuracy="
        f"{responsive_recovery['responsive_oracle_accuracy']:.3%} "
        f"regret="
        f"{responsive_result['mean_regret']:.6f} "
        f"under="
        f"{responsive_result['under_count']} "
        f"over="
        f"{responsive_result['over_count']} "
        f"entropy="
        f"{responsive_result['action_entropy']:.3f}"
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