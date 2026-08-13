import csv
import statistics
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

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
    "calibrated_asymmetric_safe_action_expansion.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "calibrated_asymmetric_safe_action_expansion_contexts.csv"
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

ACTIONS = [
    1,
    2,
    3,
]

PRIMARY_EPSILON = 0.0005

EXPANSION_THRESHOLDS = [
    0.50,
    0.60,
    0.70,
    0.80,
    0.90,
    0.95,
]

FLOAT_TOLERANCE = 1e-12
RANDOM_STATE = 42


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


def action_specific_features(
    row: dict,
    predicted_risk: float,
    predicted_losses: dict,
    action: int,
) -> list[float]:

    return (
        feature_vector(
            row,
            predicted_risk,
            predicted_losses,
        )
        + [
            float(
                action
            ),
            float(
                action - 1
            ),
            float(
                3 - action
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


def true_minimum_levels(
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


def predicted_safe_levels(
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


def action_set_from_levels(
    levels: list[float],
    candidates: dict[
        float,
        list[int],
    ],
    index: int,
) -> set[int]:

    return {
        int(
            candidates[
                risk_level
            ][index]
        )
        for risk_level
        in levels
    }


def true_safe_actions(
    true_regret_row: dict,
    candidates: dict[
        float,
        list[int],
    ],
    index: int,
) -> set[int]:

    return action_set_from_levels(
        true_minimum_levels(
            true_regret_row
        ),
        candidates,
        index,
    )


def train_action_safety_models(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
    candidates: dict[
        float,
        list[int],
    ],
) -> dict[
    int,
    RandomForestClassifier,
]:

    true_regrets = true_regret_table(
        rows,
        candidates,
    )

    models = {}

    for action in (
        ACTIONS
    ):

        x = []
        y = []

        for index, row in enumerate(
            rows
        ):

            x.append(
                action_specific_features(
                    row,
                    predicted_risks[
                        index
                    ],
                    predicted_losses[
                        index
                    ],
                    action,
                )
            )

            safe_actions = true_safe_actions(
                true_regrets[
                    index
                ],
                candidates,
                index,
            )

            y.append(
                int(
                    action
                    in safe_actions
                )
            )

        model = RandomForestClassifier(
            n_estimators=800,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=(
                RANDOM_STATE
                + 9000
                + action
            ),
        )

        model.fit(
            x,
            y,
        )

        models[
            action
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


def predict_action_safety(
    models: dict[
        int,
        RandomForestClassifier,
    ],
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> list[dict]:

    output = [
        {}
        for _ in rows
    ]

    for action in (
        ACTIONS
    ):

        x = [
            action_specific_features(
                row,
                predicted_risks[
                    index
                ],
                predicted_losses[
                    index
                ],
                action,
            )
            for index, row in enumerate(
                rows
            )
        ]

        scores = positive_probability(
            models[
                action
            ],
            x,
        )

        for index, score in enumerate(
            scores
        ):

            output[
                index
            ][
                action
            ] = score

    return output


def expand_safe_actions(
    primary_actions: set[int],
    action_safety_scores: dict,
    threshold: float,
) -> set[int]:

    expanded = set(
        primary_actions
    )

    for action in (
        ACTIONS
    ):

        if action in expanded:
            continue

        if (
            action_safety_scores[
                action
            ]
            >= threshold
        ):

            expanded.add(
                action
            )

    return expanded


def responsive_action(
    actions: set[int],
) -> int:

    return min(
        actions
    )


def safe_action_recall(
    true_actions: set[int],
    predicted_actions: set[int],
) -> float:

    return (
        len(
            true_actions
            & predicted_actions
        )
        / len(
            true_actions
        )
    )


def safe_action_precision(
    true_actions: set[int],
    predicted_actions: set[int],
) -> float:

    return (
        len(
            true_actions
            & predicted_actions
        )
        / len(
            predicted_actions
        )
    )


def evaluate_action_policy(
    name: str,
    actions: list[int],
    rows: list[dict],
    direct: list[int],
) -> dict:

    return evaluate_policy(
        name=name,
        predictions=actions,
        rows=rows,
        direct=direct,
    )


def action_text(
    actions: set[int],
) -> str:

    return "|".join(
        str(
            action
        )
        for action in sorted(
            actions
        )
    )


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

    meta_candidates = candidate_predictions(
        meta_losses,
        meta_risks,
    )

    regret_models = train_regret_models(
        meta_train_rows,
        meta_losses,
        meta_risks,
    )

    action_safety_models = (
        train_action_safety_models(
            meta_train_rows,
            meta_losses,
            meta_risks,
            meta_candidates,
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

    true_regrets = true_regret_table(
        test_rows,
        candidates,
    )

    action_safety_scores = predict_action_safety(
        action_safety_models,
        test_rows,
        test_losses,
        test_risks,
    )

    direct = candidates[
        0.00
    ]

    primary_action_sets = []

    true_action_sets = []

    primary_actions = []

    for index in range(
        len(
            test_rows
        )
    ):

        primary_levels = predicted_safe_levels(
            predicted_regrets[
                index
            ]
        )

        primary_set = action_set_from_levels(
            primary_levels,
            candidates,
            index,
        )

        true_set = true_safe_actions(
            true_regrets[
                index
            ],
            candidates,
            index,
        )

        primary_action_sets.append(
            primary_set
        )

        true_action_sets.append(
            true_set
        )

        primary_actions.append(
            responsive_action(
                primary_set
            )
        )

    evaluations = []

    primary_result = evaluate_action_policy(
        name="primary_baseline",
        actions=primary_actions,
        rows=test_rows,
        direct=direct,
    )

    primary_recall = statistics.mean(
        [
            safe_action_recall(
                true_set,
                predicted_set,
            )
            for (
                true_set,
                predicted_set,
            ) in zip(
                true_action_sets,
                primary_action_sets,
            )
        ]
    )

    primary_precision = statistics.mean(
        [
            safe_action_precision(
                true_set,
                predicted_set,
            )
            for (
                true_set,
                predicted_set,
            ) in zip(
                true_action_sets,
                primary_action_sets,
            )
        ]
    )

    primary_retention = statistics.mean(
        [
            float(
                responsive_action(
                    true_set
                )
                in predicted_set
            )
            for (
                true_set,
                predicted_set,
            ) in zip(
                true_action_sets,
                primary_action_sets,
            )
        ]
    )

    primary_result[
        "threshold"
    ] = ""

    primary_result[
        "mean_safe_action_recall"
    ] = primary_recall

    primary_result[
        "mean_safe_action_precision"
    ] = primary_precision

    primary_result[
        "responsive_action_retention"
    ] = primary_retention

    primary_result[
        "false_safe_context_fraction"
    ] = statistics.mean(
        [
            float(
                bool(
                    predicted_set
                    - true_set
                )
            )
            for (
                true_set,
                predicted_set,
            ) in zip(
                true_action_sets,
                primary_action_sets,
            )
        ]
    )

    primary_result[
        "mean_false_safe_regret"
    ] = ""

    primary_result[
        "max_false_safe_regret"
    ] = ""

    evaluations.append(
        primary_result
    )

    context_rows = []

    for threshold in (
        EXPANSION_THRESHOLDS
    ):

        expanded_sets = []

        selected_actions = []

        recall_values = []
        precision_values = []

        responsive_retained = []

        false_safe_contexts = 0

        false_safe_regrets = []

        expansion_count = 0

        recovered_responsive_count = 0

        harmful_expansion_contexts = 0

        for index, row in enumerate(
            test_rows
        ):

            primary_set = primary_action_sets[
                index
            ]

            true_set = true_action_sets[
                index
            ]

            expanded_set = expand_safe_actions(
                primary_set,
                action_safety_scores[
                    index
                ],
                threshold,
            )

            expanded_sets.append(
                expanded_set
            )

            selected_action = responsive_action(
                expanded_set
            )

            selected_actions.append(
                selected_action
            )

            recall_values.append(
                safe_action_recall(
                    true_set,
                    expanded_set,
                )
            )

            precision_values.append(
                safe_action_precision(
                    true_set,
                    expanded_set,
                )
            )

            responsive_retained.append(
                float(
                    responsive_action(
                        true_set
                    )
                    in expanded_set
                )
            )

            added_actions = (
                expanded_set
                - primary_set
            )

            if added_actions:
                expansion_count += 1

            primary_had_responsive = (
                responsive_action(
                    true_set
                )
                in primary_set
            )

            expanded_has_responsive = (
                responsive_action(
                    true_set
                )
                in expanded_set
            )

            if (
                not primary_had_responsive
                and expanded_has_responsive
            ):

                recovered_responsive_count += 1

            false_safe = (
                expanded_set
                - true_set
            )

            if false_safe:

                false_safe_contexts += 1

                harmful_expansion_contexts += int(
                    bool(
                        false_safe
                        - (
                            primary_set
                            - true_set
                        )
                    )
                )

                for false_action in (
                    false_safe
                ):

                    false_safe_regrets.append(
                        regret(
                            row,
                            false_action,
                        )
                    )

            context_rows.append(
                {
                    "threshold":
                        threshold,

                    "test_index":
                        index,

                    "best_persistence":
                        int(
                            row[
                                "best_persistence"
                            ]
                        ),

                    "primary_actions":
                        action_text(
                            primary_set
                        ),

                    "expanded_actions":
                        action_text(
                            expanded_set
                        ),

                    "true_safe_actions":
                        action_text(
                            true_set
                        ),

                    "selected_action":
                        selected_action,

                    "true_responsive_action":
                        responsive_action(
                            true_set
                        ),

                    "selected_regret":
                        regret(
                            row,
                            selected_action,
                        ),

                    "responsive_retained":
                        int(
                            responsive_action(
                                true_set
                            )
                            in expanded_set
                        ),

                    "responsive_recovered_by_expansion":
                        int(
                            (
                                responsive_action(
                                    true_set
                                )
                                not in primary_set
                            )
                            and (
                                responsive_action(
                                    true_set
                                )
                                in expanded_set
                            )
                        ),

                    "safe_action_recall":
                        safe_action_recall(
                            true_set,
                            expanded_set,
                        ),

                    "safe_action_precision":
                        safe_action_precision(
                            true_set,
                            expanded_set,
                        ),

                    "false_safe_actions":
                        action_text(
                            expanded_set
                            - true_set
                        ),

                    "score_action_1":
                        action_safety_scores[
                            index
                        ][1],

                    "score_action_2":
                        action_safety_scores[
                            index
                        ][2],

                    "score_action_3":
                        action_safety_scores[
                            index
                        ][3],
                }
            )

        result = evaluate_action_policy(
            name=(
                "expanded_threshold_"
                f"{threshold:.2f}"
            ),
            actions=selected_actions,
            rows=test_rows,
            direct=direct,
        )

        result[
            "threshold"
        ] = threshold

        result[
            "mean_safe_action_recall"
        ] = statistics.mean(
            recall_values
        )

        result[
            "mean_safe_action_precision"
        ] = statistics.mean(
            precision_values
        )

        result[
            "responsive_action_retention"
        ] = statistics.mean(
            responsive_retained
        )

        result[
            "false_safe_context_fraction"
        ] = (
            false_safe_contexts
            / len(
                test_rows
            )
        )

        result[
            "mean_false_safe_regret"
        ] = (
            statistics.mean(
                false_safe_regrets
            )
            if false_safe_regrets
            else 0.0
        )

        result[
            "max_false_safe_regret"
        ] = (
            max(
                false_safe_regrets
            )
            if false_safe_regrets
            else 0.0
        )

        result[
            "expansion_contexts"
        ] = expansion_count

        result[
            "recovered_responsive_contexts"
        ] = recovered_responsive_count

        result[
            "harmful_expansion_contexts"
        ] = harmful_expansion_contexts

        evaluations.append(
            result
        )

    true_responsive_actions = [
        responsive_action(
            true_set
        )
        for true_set
        in true_action_sets
    ]

    oracle_result = evaluate_action_policy(
        name="responsive_action_oracle",
        actions=true_responsive_actions,
        rows=test_rows,
        direct=direct,
    )

    oracle_result[
        "threshold"
    ] = ""

    oracle_result[
        "mean_safe_action_recall"
    ] = 1.0

    oracle_result[
        "mean_safe_action_precision"
    ] = 1.0

    oracle_result[
        "responsive_action_retention"
    ] = 1.0

    oracle_result[
        "false_safe_context_fraction"
    ] = 0.0

    oracle_result[
        "mean_false_safe_regret"
    ] = 0.0

    oracle_result[
        "max_false_safe_regret"
    ] = 0.0

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

    print("=" * 195)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "CALIBRATED ASYMMETRIC "
        "SAFE-ACTION EXPANSION"
    )

    print("=" * 195)

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
        f"expansion-training contexts="
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
        "PRIMARY GATE"
    )

    print(
        f"recall="
        f"{primary_recall:.3%} "
        f"precision="
        f"{primary_precision:.3%} "
        f"responsive_retention="
        f"{primary_retention:.3%} "
        f"regret="
        f"{primary_result['mean_regret']:.6f} "
        f"under="
        f"{primary_result['under_count']} "
        f"over="
        f"{primary_result['over_count']} "
        f"entropy="
        f"{primary_result['action_entropy']:.3f}"
    )

    print()

    print(
        "EXPANSION SWEEP"
    )

    for result in evaluations:

        if not result[
            "policy"
        ].startswith(
            "expanded_threshold_"
        ):

            continue

        print(
            f"threshold="
            f"{float(result['threshold']):.2f} "
            f"recall="
            f"{float(result['mean_safe_action_recall']):.3%} "
            f"precision="
            f"{float(result['mean_safe_action_precision']):.3%} "
            f"responsive_retention="
            f"{float(result['responsive_action_retention']):.3%} "
            f"regret="
            f"{result['mean_regret']:.6f} "
            f"under="
            f"{result['under_count']} "
            f"over="
            f"{result['over_count']} "
            f"entropy="
            f"{result['action_entropy']:.3f} "
            f"false_safe_contexts="
            f"{float(result['false_safe_context_fraction']):.3%} "
            f"mean_false_regret="
            f"{float(result['mean_false_safe_regret']):.6f} "
            f"max_false_regret="
            f"{float(result['max_false_safe_regret']):.6f} "
            f"expanded="
            f"{result['expansion_contexts']} "
            f"recovered="
            f"{result['recovered_responsive_contexts']} "
            f"harmful="
            f"{result['harmful_expansion_contexts']}"
        )

    print()

    print(
        "RESPONSIVE ACTION ORACLE"
    )

    print(
        f"regret="
        f"{oracle_result['mean_regret']:.6f} "
        f"under="
        f"{oracle_result['under_count']} "
        f"over="
        f"{oracle_result['over_count']} "
        f"entropy="
        f"{oracle_result['action_entropy']:.3f}"
    )

    print("=" * 195)

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