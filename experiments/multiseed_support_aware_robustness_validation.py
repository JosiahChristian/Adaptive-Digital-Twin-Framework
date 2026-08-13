import csv
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
    "multiseed_support_aware_robustness_validation.csv"
)

SEED_OUTPUT_PATH = Path(
    "results/"
    "multiseed_support_aware_robustness_validation_seeds.csv"
)

BASE_GENERATION_SEEDS = [
    44001,
    44002,
    44003,
    44004,
    44005,
    44006,
    44007,
    44008,
    44009,
    44010,
]

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
    3.50,
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


def evaluate_seed(
    generation_seed: int,
) -> list[dict]:

    rows = generate_analysis_rows(
        base_seed=generation_seed
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

        distances = {}

        for action in (
            ACTIONS
        ):

            distances[
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
            distances
        )

    seed_rows = []

    primary_actions = [
        responsive_action(
            action_set
        )
        for action_set
        in primary_sets
    ]

    primary_result = evaluate_policy(
        name="primary_baseline",
        predictions=primary_actions,
        rows=test_rows,
        direct=direct,
    )

    primary_result[
        "generation_seed"
    ] = generation_seed

    primary_result[
        "safe_action_recall"
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
        "safe_action_precision"
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

    seed_rows.append(
        primary_result
    )

    costaware_sets = []

    for index in range(
        len(
            test_rows
        )
    ):

        expanded = set(
            primary_sets[
                index
            ]
        )

        for action in (
            ACTIONS
        ):

            if action in expanded:
                continue

            if (
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
            ):

                expanded.add(
                    action
                )

        costaware_sets.append(
            expanded
        )

    costaware_actions = [
        responsive_action(
            action_set
        )
        for action_set
        in costaware_sets
    ]

    costaware_result = evaluate_policy(
        name="costaware",
        predictions=costaware_actions,
        rows=test_rows,
        direct=direct,
    )

    costaware_result[
        "generation_seed"
    ] = generation_seed

    costaware_result[
        "safe_action_recall"
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
                costaware_sets,
            )
        ]
    )

    costaware_result[
        "safe_action_precision"
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
                costaware_sets,
            )
        ]
    )

    costaware_result[
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
                costaware_sets,
            )
        ]
    )

    costaware_result[
        "expansion_contexts"
    ] = sum(
        int(
            costaware_sets[
                index
            ]
            != primary_sets[
                index
            ]
        )
        for index in range(
            len(
                test_rows
            )
        )
    )

    costaware_result[
        "recovered_responsive_contexts"
    ] = sum(
        int(
            responsive_action(
                true_sets[
                    index
                ]
            )
            not in primary_sets[
                index
            ]
            and responsive_action(
                true_sets[
                    index
                ]
            )
            in costaware_sets[
                index
            ]
        )
        for index in range(
            len(
                test_rows
            )
        )
    )

    costaware_result[
        "harmful_expansion_contexts"
    ] = sum(
        int(
            responsive_action(
                costaware_sets[
                    index
                ]
            )
            != responsive_action(
                primary_sets[
                    index
                ]
            )
            and regret(
                test_rows[
                    index
                ],
                responsive_action(
                    costaware_sets[
                        index
                    ]
                ),
            )
            >
            regret(
                test_rows[
                    index
                ],
                responsive_action(
                    primary_sets[
                        index
                    ]
                ),
            )
            + FLOAT_TOLERANCE
        )
        for index in range(
            len(
                test_rows
            )
        )
    )

    costaware_result[
        "beneficial_expansion_contexts"
    ] = sum(
        int(
            responsive_action(
                costaware_sets[
                    index
                ]
            )
            != responsive_action(
                primary_sets[
                    index
                ]
            )
            and responsive_action(
                costaware_sets[
                    index
                ]
            )
            ==
            responsive_action(
                true_sets[
                    index
                ]
            )
            and regret(
                test_rows[
                    index
                ],
                responsive_action(
                    costaware_sets[
                        index
                    ]
                ),
            )
            <=
            regret(
                test_rows[
                    index
                ],
                responsive_action(
                    primary_sets[
                        index
                    ]
                ),
            )
            + FLOAT_TOLERANCE
        )
        for index in range(
            len(
                test_rows
            )
        )
    )

    seed_rows.append(
        costaware_result
    )

    for support_threshold in (
        SUPPORT_THRESHOLDS
    ):

        expanded_sets = []

        for index, row in enumerate(
            test_rows
        ):

            expanded = set(
                primary_sets[
                    index
                ]
            )

            for action in (
                ACTIONS
            ):

                if action in expanded:
                    continue

                if (
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
                    and support_distances[
                        index
                    ][
                        action
                    ]
                    <= support_threshold
                ):

                    expanded.add(
                        action
                    )

            expanded_sets.append(
                expanded
            )

        selected_actions = [
            responsive_action(
                action_set
            )
            for action_set
            in expanded_sets
        ]

        result = evaluate_policy(
            name=(
                "support_"
                f"{support_threshold:.2f}"
            ),
            predictions=selected_actions,
            rows=test_rows,
            direct=direct,
        )

        result[
            "generation_seed"
        ] = generation_seed

        result[
            "safe_action_recall"
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
                    expanded_sets,
                )
            ]
        )

        result[
            "safe_action_precision"
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
                    expanded_sets,
                )
            ]
        )

        result[
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
                    expanded_sets,
                )
            ]
        )

        result[
            "expansion_contexts"
        ] = sum(
            int(
                expanded_sets[
                    index
                ]
                != primary_sets[
                    index
                ]
            )
            for index in range(
                len(
                    test_rows
                )
            )
        )

        result[
            "recovered_responsive_contexts"
        ] = sum(
            int(
                responsive_action(
                    true_sets[
                        index
                    ]
                )
                not in primary_sets[
                    index
                ]
                and responsive_action(
                    true_sets[
                        index
                    ]
                )
                in expanded_sets[
                    index
                ]
            )
            for index in range(
                len(
                    test_rows
                )
            )
        )

        result[
            "harmful_expansion_contexts"
        ] = sum(
            int(
                responsive_action(
                    expanded_sets[
                        index
                    ]
                )
                != responsive_action(
                    primary_sets[
                        index
                    ]
                )
                and regret(
                    test_rows[
                        index
                    ],
                    responsive_action(
                        expanded_sets[
                            index
                        ]
                    ),
                )
                >
                regret(
                    test_rows[
                        index
                    ],
                    responsive_action(
                        primary_sets[
                            index
                        ]
                    ),
                )
                + FLOAT_TOLERANCE
            )
            for index in range(
                len(
                    test_rows
                )
            )
        )

        result[
            "beneficial_expansion_contexts"
        ] = sum(
            int(
                responsive_action(
                    expanded_sets[
                        index
                    ]
                )
                != responsive_action(
                    primary_sets[
                        index
                    ]
                )
                and responsive_action(
                    expanded_sets[
                        index
                    ]
                )
                ==
                responsive_action(
                    true_sets[
                        index
                    ]
                )
                and regret(
                    test_rows[
                        index
                    ],
                    responsive_action(
                        expanded_sets[
                            index
                        ]
                    ),
                )
                <=
                regret(
                    test_rows[
                        index
                    ],
                    responsive_action(
                        primary_sets[
                            index
                        ]
                    ),
                )
                + FLOAT_TOLERANCE
            )
            for index in range(
                len(
                    test_rows
                )
            )
        )

        seed_rows.append(
            result
        )

    responsive_actions = [
        responsive_action(
            true_set
        )
        for true_set
        in true_sets
    ]

    responsive_oracle = evaluate_policy(
        name="responsive_action_oracle",
        predictions=responsive_actions,
        rows=test_rows,
        direct=direct,
    )

    responsive_oracle[
        "generation_seed"
    ] = generation_seed

    responsive_oracle[
        "safe_action_recall"
    ] = 1.0

    responsive_oracle[
        "safe_action_precision"
    ] = 1.0

    responsive_oracle[
        "responsive_action_retention"
    ] = 1.0

    seed_rows.append(
        responsive_oracle
    )

    fixed_k3 = evaluate_policy(
        name="fixed_k3",
        predictions=fixed_predictions(
            3,
            test_rows,
        ),
        rows=test_rows,
        direct=direct,
    )

    fixed_k3[
        "generation_seed"
    ] = generation_seed

    seed_rows.append(
        fixed_k3
    )

    action_oracle = evaluate_policy(
        name="action_oracle",
        predictions=oracle_predictions(
            test_rows
        ),
        rows=test_rows,
        direct=direct,
    )

    action_oracle[
        "generation_seed"
    ] = generation_seed

    seed_rows.append(
        action_oracle
    )

    return seed_rows


def aggregate_results(
    seed_rows: list[dict],
) -> list[dict]:

    policies = sorted(
        {
            row[
                "policy"
            ]
            for row in seed_rows
        }
    )

    aggregate = []

    for policy in policies:

        rows = [
            row
            for row in seed_rows
            if row[
                "policy"
            ]
            == policy
        ]

        mean_regrets = [
            float(
                row[
                    "mean_regret"
                ]
            )
            for row in rows
        ]

        under_counts = [
            int(
                row[
                    "under_count"
                ]
            )
            for row in rows
        ]

        over_counts = [
            int(
                row[
                    "over_count"
                ]
            )
            for row in rows
        ]

        entropy_values = [
            float(
                row[
                    "action_entropy"
                ]
            )
            for row in rows
        ]

        recalls = [
            float(
                row[
                    "safe_action_recall"
                ]
            )
            for row in rows
            if row.get(
                "safe_action_recall",
                ""
            )
            != ""
        ]

        precisions = [
            float(
                row[
                    "safe_action_precision"
                ]
            )
            for row in rows
            if row.get(
                "safe_action_precision",
                ""
            )
            != ""
        ]

        retentions = [
            float(
                row[
                    "responsive_action_retention"
                ]
            )
            for row in rows
            if row.get(
                "responsive_action_retention",
                ""
            )
            != ""
        ]

        harmful = [
            int(
                row[
                    "harmful_expansion_contexts"
                ]
            )
            for row in rows
            if row.get(
                "harmful_expansion_contexts",
                ""
            )
            != ""
        ]

        beneficial = [
            int(
                row[
                    "beneficial_expansion_contexts"
                ]
            )
            for row in rows
            if row.get(
                "beneficial_expansion_contexts",
                ""
            )
            != ""
        ]

        recovered = [
            int(
                row[
                    "recovered_responsive_contexts"
                ]
            )
            for row in rows
            if row.get(
                "recovered_responsive_contexts",
                ""
            )
            != ""
        ]

        aggregate.append(
            {
                "policy":
                    policy,

                "seeds":
                    len(
                        rows
                    ),

                "mean_regret":
                    statistics.mean(
                        mean_regrets
                    ),

                "std_regret":
                    statistics.pstdev(
                        mean_regrets
                    ),

                "median_regret":
                    statistics.median(
                        mean_regrets
                    ),

                "min_regret":
                    min(
                        mean_regrets
                    ),

                "max_regret":
                    max(
                        mean_regrets
                    ),

                "mean_under":
                    statistics.mean(
                        under_counts
                    ),

                "max_under":
                    max(
                        under_counts
                    ),

                "mean_over":
                    statistics.mean(
                        over_counts
                    ),

                "mean_entropy":
                    statistics.mean(
                        entropy_values
                    ),

                "mean_safe_action_recall":
                    (
                        statistics.mean(
                            recalls
                        )
                        if recalls
                        else ""
                    ),

                "mean_safe_action_precision":
                    (
                        statistics.mean(
                            precisions
                        )
                        if precisions
                        else ""
                    ),

                "mean_responsive_action_retention":
                    (
                        statistics.mean(
                            retentions
                        )
                        if retentions
                        else ""
                    ),

                "mean_harmful_expansions":
                    (
                        statistics.mean(
                            harmful
                        )
                        if harmful
                        else ""
                    ),

                "max_harmful_expansions":
                    (
                        max(
                            harmful
                        )
                        if harmful
                        else ""
                    ),

                "mean_beneficial_expansions":
                    (
                        statistics.mean(
                            beneficial
                        )
                        if beneficial
                        else ""
                    ),

                "mean_recovered_responsive":
                    (
                        statistics.mean(
                            recovered
                        )
                        if recovered
                        else ""
                    ),
            }
        )

    return aggregate


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

    seed_rows = []

    print(
        "=" * 200
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "MULTI-SEED SUPPORT-AWARE "
        "ROBUSTNESS VALIDATION"
    )

    print(
        "=" * 200
    )

    print(
        f"generation seeds="
        f"{BASE_GENERATION_SEEDS}"
    )

    print(
        f"safety threshold="
        f"{SAFETY_THRESHOLD:.2f}"
    )

    print(
        f"downside threshold="
        f"{DOWNSIDE_THRESHOLD:.3f}"
    )

    print(
        f"support thresholds="
        f"{SUPPORT_THRESHOLDS}"
    )

    print()

    for generation_seed in (
        BASE_GENERATION_SEEDS
    ):

        print(
            f"running seed "
            f"{generation_seed}..."
        )

        rows = evaluate_seed(
            generation_seed
        )

        seed_rows.extend(
            rows
        )

    aggregate = aggregate_results(
        seed_rows
    )

    print()

    print(
        "MULTI-SEED POLICY SUMMARY"
    )

    ordered_names = [
        "primary_baseline",
        "costaware",
        "support_2.50",
        "support_3.50",
        "responsive_action_oracle",
        "fixed_k3",
        "action_oracle",
    ]

    for name in ordered_names:

        matching = [
            row
            for row in aggregate
            if row[
                "policy"
            ]
            == name
        ]

        if not matching:
            continue

        row = matching[
            0
        ]

        extra = ""

        if (
            row[
                "mean_safe_action_recall"
            ]
            != ""
        ):

            extra += (
                f" recall="
                f"{float(row['mean_safe_action_recall']):.3%}"
                f" precision="
                f"{float(row['mean_safe_action_precision']):.3%}"
                f" retention="
                f"{float(row['mean_responsive_action_retention']):.3%}"
            )

        if (
            row[
                "mean_harmful_expansions"
            ]
            != ""
        ):

            extra += (
                f" harmful_mean="
                f"{float(row['mean_harmful_expansions']):.2f}"
                f" harmful_max="
                f"{int(row['max_harmful_expansions'])}"
                f" beneficial_mean="
                f"{float(row['mean_beneficial_expansions']):.2f}"
                f" recovered_mean="
                f"{float(row['mean_recovered_responsive']):.2f}"
            )

        print(
            f"{name:<28} "
            f"mean_R="
            f"{row['mean_regret']:.6f} "
            f"std_R="
            f"{row['std_regret']:.6f} "
            f"median_R="
            f"{row['median_regret']:.6f} "
            f"range=["
            f"{row['min_regret']:.6f},"
            f"{row['max_regret']:.6f}"
            f"] "
            f"mean_under="
            f"{row['mean_under']:.2f} "
            f"max_under="
            f"{row['max_under']} "
            f"mean_over="
            f"{row['mean_over']:.2f} "
            f"mean_H="
            f"{row['mean_entropy']:.3f}"
            f"{extra}"
        )

    save_csv(
        OUTPUT_PATH,
        aggregate,
    )

    save_csv(
        SEED_OUTPUT_PATH,
        seed_rows,
    )

    print()

    print(
        f"Aggregate results saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Seed-level results saved to: "
        f"{SEED_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()