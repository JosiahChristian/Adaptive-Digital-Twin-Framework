import csv
import math
import statistics
from pathlib import Path

import numpy as np

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.preprocessing import StandardScaler

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
    "support_aware_safe_action_expansion.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "support_aware_safe_action_expansion_contexts.csv"
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

SAFETY_THRESHOLD = 0.60
DOWNSIDE_THRESHOLD = 0.020

SUPPORT_THRESHOLDS = [
    2.50,
    3.00,
    3.50,
    4.00,
    4.50,
    5.00,
    5.50,
]

K_NEIGHBORS = 5

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


def true_safe_actions(
    regret_row: dict,
    candidates: dict[
        float,
        list[int],
    ],
    index: int,
) -> set[int]:

    levels = true_minimum_levels(
        regret_row
    )

    return {
        int(
            candidates[
                risk_level
            ][index]
        )
        for risk_level
        in levels
    }


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


def train_action_downside_models(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
    candidates: dict[
        float,
        list[int],
    ],
) -> dict[
    int,
    RandomForestRegressor,
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

            safe_actions = true_safe_actions(
                true_regrets[
                    index
                ],
                candidates,
                index,
            )

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

            target = (
                0.0
                if action in safe_actions
                else max(
                    0.0,
                    regret(
                        row,
                        action,
                    ),
                )
            )

            y.append(
                target
            )

        model = RandomForestRegressor(
            n_estimators=800,
            min_samples_leaf=2,
            random_state=(
                RANDOM_STATE
                + 12000
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


def predict_action_downside(
    models: dict[
        int,
        RandomForestRegressor,
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

        predictions = models[
            action
        ].predict(
            x
        )

        for index, value in enumerate(
            predictions
        ):

            output[
                index
            ][
                action
            ] = max(
                0.0,
                float(
                    value
                ),
            )

    return output


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


def build_support_objects(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict:

    objects = {}

    for action in (
        ACTIONS
    ):

        matrix = np.asarray(
            [
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
            ],
            dtype=float,
        )

        scaler = StandardScaler()

        scaled = scaler.fit_transform(
            matrix
        )

        objects[
            action
        ] = {
            "scaler":
                scaler,

            "training_matrix":
                scaled,
        }

    return objects


def mean_knn_distance(
    support_object: dict,
    sample_features: list[float],
) -> float:

    sample = np.asarray(
        [
            sample_features
        ],
        dtype=float,
    )

    scaled_sample = support_object[
        "scaler"
    ].transform(
        sample
    )[0]

    matrix = support_object[
        "training_matrix"
    ]

    distances = np.sqrt(
        np.sum(
            (
                matrix
                - scaled_sample
            )
            ** 2,
            axis=1,
        )
    )

    order = np.argsort(
        distances
    )

    k = min(
        K_NEIGHBORS,
        len(
            order
        ),
    )

    return float(
        np.mean(
            distances[
                order[
                    :k
                ]
            ]
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

    safety_models = train_action_safety_models(
        meta_train_rows,
        meta_losses,
        meta_risks,
        meta_candidates,
    )

    downside_models = train_action_downside_models(
        meta_train_rows,
        meta_losses,
        meta_risks,
        meta_candidates,
    )

    support_objects = build_support_objects(
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

    predicted_regrets = predicted_regret_table(
        regret_models,
        test_rows,
        test_losses,
        test_risks,
    )

    safety_scores = predict_action_safety(
        safety_models,
        test_rows,
        test_losses,
        test_risks,
    )

    downside_scores = predict_action_downside(
        downside_models,
        test_rows,
        test_losses,
        test_risks,
    )

    true_regrets = true_regret_table(
        test_rows,
        candidates,
    )

    direct = candidates[
        0.00
    ]

    primary_sets = []
    true_sets = []

    support_distances = []

    for index, row in enumerate(
        test_rows
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

        primary_sets.append(
            primary_set
        )

        true_sets.append(
            true_set
        )

        action_distance_row = {}

        for action in (
            ACTIONS
        ):

            action_distance_row[
                action
            ] = mean_knn_distance(
                support_objects[
                    action
                ],
                action_specific_features(
                    row,
                    test_risks[
                        index
                    ],
                    test_losses[
                        index
                    ],
                    action,
                ),
            )

        support_distances.append(
            action_distance_row
        )

    primary_actions = [
        responsive_action(
            action_set
        )
        for action_set
        in primary_sets
    ]

    evaluations = []

    primary_result = evaluate_policy(
        name="primary_baseline",
        predictions=primary_actions,
        rows=test_rows,
        direct=direct,
    )

    primary_result[
        "support_threshold"
    ] = ""

    primary_result[
        "mean_safe_action_recall"
    ] = statistics.mean(
        [
            safe_action_recall(
                true_set,
                predicted_set,
            )
            for (
                true_set,
                predicted_set,
            ) in zip(
                true_sets,
                primary_sets,
            )
        ]
    )

    primary_result[
        "mean_safe_action_precision"
    ] = statistics.mean(
        [
            safe_action_precision(
                true_set,
                predicted_set,
            )
            for (
                true_set,
                predicted_set,
            ) in zip(
                true_sets,
                primary_sets,
            )
        ]
    )

    primary_result[
        "responsive_action_retention"
    ] = statistics.mean(
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
                true_sets,
                primary_sets,
            )
        ]
    )

    primary_result[
        "expansion_contexts"
    ] = 0

    primary_result[
        "recovered_responsive_contexts"
    ] = 0

    primary_result[
        "harmful_expansion_contexts"
    ] = 0

    primary_result[
        "beneficial_expansion_contexts"
    ] = 0

    evaluations.append(
        primary_result
    )

    context_rows = []

    for support_threshold in (
        SUPPORT_THRESHOLDS
    ):

        selected_actions = []

        recall_values = []
        precision_values = []
        retention_values = []

        expansion_contexts = 0
        recovered_responsive_contexts = 0
        harmful_expansion_contexts = 0
        beneficial_expansion_contexts = 0

        retained_from_costaware = 0

        for index, row in enumerate(
            test_rows
        ):

            primary_set = primary_sets[
                index
            ]

            true_set = true_sets[
                index
            ]

            expanded_set = set(
                primary_set
            )

            costaware_candidate_actions = []

            admitted_actions = []

            for action in (
                ACTIONS
            ):

                if action in expanded_set:
                    continue

                passes_costaware = (
                    safety_scores[
                        index
                    ][
                        action
                    ]
                    >= SAFETY_THRESHOLD
                    and downside_scores[
                        index
                    ][
                        action
                    ]
                    <= DOWNSIDE_THRESHOLD
                )

                if passes_costaware:

                    costaware_candidate_actions.append(
                        action
                    )

                    if (
                        support_distances[
                            index
                        ][
                            action
                        ]
                        <= support_threshold
                    ):

                        expanded_set.add(
                            action
                        )

                        admitted_actions.append(
                            action
                        )

            if costaware_candidate_actions:

                if admitted_actions:

                    retained_from_costaware += 1

            added_actions = (
                expanded_set
                - primary_set
            )

            if added_actions:
                expansion_contexts += 1

            primary_action = responsive_action(
                primary_set
            )

            selected_action = responsive_action(
                expanded_set
            )

            selected_actions.append(
                selected_action
            )

            true_responsive_action = responsive_action(
                true_set
            )

            primary_has_responsive = (
                true_responsive_action
                in primary_set
            )

            expanded_has_responsive = (
                true_responsive_action
                in expanded_set
            )

            if (
                not primary_has_responsive
                and expanded_has_responsive
            ):

                recovered_responsive_contexts += 1

            primary_regret = regret(
                row,
                primary_action,
            )

            selected_regret = regret(
                row,
                selected_action,
            )

            changed_action = (
                selected_action
                != primary_action
            )

            harmful = (
                changed_action
                and selected_regret
                > primary_regret
                + FLOAT_TOLERANCE
            )

            beneficial = (
                changed_action
                and selected_action
                == true_responsive_action
                and selected_regret
                <= primary_regret
                + FLOAT_TOLERANCE
            )

            if harmful:
                harmful_expansion_contexts += 1

            if beneficial:
                beneficial_expansion_contexts += 1

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

            retention_values.append(
                float(
                    true_responsive_action
                    in expanded_set
                )
            )

            context_rows.append(
                {
                    "support_threshold":
                        support_threshold,

                    "test_index":
                        index,

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

                    "primary_action":
                        primary_action,

                    "selected_action":
                        selected_action,

                    "true_responsive_action":
                        true_responsive_action,

                    "primary_regret":
                        primary_regret,

                    "selected_regret":
                        selected_regret,

                    "incremental_regret":
                        (
                            selected_regret
                            - primary_regret
                        ),

                    "beneficial_expansion":
                        int(
                            beneficial
                        ),

                    "harmful_expansion":
                        int(
                            harmful
                        ),

                    "responsive_recovered":
                        int(
                            (
                                not primary_has_responsive
                            )
                            and expanded_has_responsive
                        ),

                    "distance_action_1":
                        support_distances[
                            index
                        ][1],

                    "distance_action_2":
                        support_distances[
                            index
                        ][2],

                    "distance_action_3":
                        support_distances[
                            index
                        ][3],

                    "safety_score_1":
                        safety_scores[
                            index
                        ][1],

                    "safety_score_2":
                        safety_scores[
                            index
                        ][2],

                    "safety_score_3":
                        safety_scores[
                            index
                        ][3],

                    "downside_score_1":
                        downside_scores[
                            index
                        ][1],

                    "downside_score_2":
                        downside_scores[
                            index
                        ][2],

                    "downside_score_3":
                        downside_scores[
                            index
                        ][3],
                }
            )

        result = evaluate_policy(
            name=(
                "support_threshold_"
                f"{support_threshold:.2f}"
            ),
            predictions=selected_actions,
            rows=test_rows,
            direct=direct,
        )

        result[
            "support_threshold"
        ] = support_threshold

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
            retention_values
        )

        result[
            "expansion_contexts"
        ] = expansion_contexts

        result[
            "recovered_responsive_contexts"
        ] = recovered_responsive_contexts

        result[
            "harmful_expansion_contexts"
        ] = harmful_expansion_contexts

        result[
            "beneficial_expansion_contexts"
        ] = beneficial_expansion_contexts

        result[
            "retained_costaware_contexts"
        ] = retained_from_costaware

        evaluations.append(
            result
        )

    responsive_oracle_actions = [
        responsive_action(
            true_set
        )
        for true_set
        in true_sets
    ]

    responsive_oracle_result = evaluate_policy(
        name="responsive_action_oracle",
        predictions=responsive_oracle_actions,
        rows=test_rows,
        direct=direct,
    )

    responsive_oracle_result[
        "support_threshold"
    ] = ""

    responsive_oracle_result[
        "mean_safe_action_recall"
    ] = 1.0

    responsive_oracle_result[
        "mean_safe_action_precision"
    ] = 1.0

    responsive_oracle_result[
        "responsive_action_retention"
    ] = 1.0

    responsive_oracle_result[
        "expansion_contexts"
    ] = ""

    responsive_oracle_result[
        "recovered_responsive_contexts"
    ] = ""

    responsive_oracle_result[
        "harmful_expansion_contexts"
    ] = 0

    responsive_oracle_result[
        "beneficial_expansion_contexts"
    ] = ""

    evaluations.append(
        responsive_oracle_result
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

    print("=" * 200)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "SUPPORT-AWARE SAFE-ACTION "
        "EXPANSION"
    )

    print("=" * 200)

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
        f"support-training contexts="
        f"{len(meta_train_rows)}"
    )

    print(
        f"test contexts="
        f"{len(test_rows)}"
    )

    print(
        f"safety threshold="
        f"{SAFETY_THRESHOLD:.2f}"
    )

    print(
        f"downside threshold="
        f"{DOWNSIDE_THRESHOLD:.3f}"
    )

    print()

    print(
        "PRIMARY GATE"
    )

    print(
        f"recall="
        f"{primary_result['mean_safe_action_recall']:.3%} "
        f"precision="
        f"{primary_result['mean_safe_action_precision']:.3%} "
        f"retention="
        f"{primary_result['responsive_action_retention']:.3%} "
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
        "SUPPORT-AWARE SWEEP"
    )

    for result in evaluations:

        if not result[
            "policy"
        ].startswith(
            "support_threshold_"
        ):

            continue

        print(
            f"support="
            f"{float(result['support_threshold']):.2f} "
            f"recall="
            f"{float(result['mean_safe_action_recall']):.3%} "
            f"precision="
            f"{float(result['mean_safe_action_precision']):.3%} "
            f"retention="
            f"{float(result['responsive_action_retention']):.3%} "
            f"regret="
            f"{result['mean_regret']:.6f} "
            f"under="
            f"{result['under_count']} "
            f"over="
            f"{result['over_count']} "
            f"entropy="
            f"{result['action_entropy']:.3f} "
            f"expanded="
            f"{result['expansion_contexts']} "
            f"recovered="
            f"{result['recovered_responsive_contexts']} "
            f"beneficial="
            f"{result['beneficial_expansion_contexts']} "
            f"harmful="
            f"{result['harmful_expansion_contexts']}"
        )

    print()

    print(
        "RESPONSIVE ACTION ORACLE"
    )

    print(
        f"regret="
        f"{responsive_oracle_result['mean_regret']:.6f} "
        f"under="
        f"{responsive_oracle_result['under_count']} "
        f"over="
        f"{responsive_oracle_result['over_count']} "
        f"entropy="
        f"{responsive_oracle_result['action_entropy']:.3f}"
    )

    print("=" * 200)

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