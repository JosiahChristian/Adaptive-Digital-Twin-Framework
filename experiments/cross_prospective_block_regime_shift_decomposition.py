import csv
import statistics
from collections import Counter
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
)


OUTPUT_PATH = Path(
    "results/"
    "cross_prospective_block_regime_shift_decomposition.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "cross_prospective_block_regime_shift_decomposition_contexts.csv"
)

BLOCK_A_SEEDS = list(
    range(
        44011,
        44031,
    )
)

BLOCK_B_SEEDS = list(
    range(
        44031,
        44051,
    )
)

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
SUPPORT_THRESHOLD = 2.50

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
            row[
                name
            ]
        )
        for name in FEATURE_NAMES
    ]

    loss_k1 = float(
        predicted_losses[
            1
        ]
    )

    loss_k2 = float(
        predicted_losses[
            2
        ]
    )

    loss_k3 = float(
        predicted_losses[
            3
        ]
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
                for risk_level in RISK_LEVELS
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
        for risk_level in RISK_LEVELS
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
        for risk_level in levels
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

    for risk_level in RISK_LEVELS:

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
        for risk_level in RISK_LEVELS
    }

    output = []

    for index in range(
        len(
            rows
        )
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
                for risk_level in RISK_LEVELS
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
        for risk_level in RISK_LEVELS
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
        for risk_level in levels
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

    for action in ACTIONS:

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

    for action in ACTIONS:

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

    for action in ACTIONS:

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

    for action in ACTIONS:

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


def build_support_objects(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict:

    objects = {}

    for action in ACTIONS:

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


def responsive_action(
    actions: set[int],
) -> int:

    return min(
        actions
    )


def baseline_support_set(
    index: int,
    row: dict,
    primary_set: set[int],
    predicted_risk: float,
    predicted_losses: dict,
    safety_scores: dict,
    downside_scores: dict,
    support_objects: dict,
) -> tuple[
    set[int],
    dict[int, float],
]:

    expanded = set(
        primary_set
    )

    distances = {}

    for action in ACTIONS:

        distances[
            action
        ] = mean_knn_distance(
            support_objects[
                action
            ],
            action_specific_features(
                row,
                predicted_risk,
                predicted_losses,
                action,
            ),
        )

        if action in expanded:
            continue

        if (
            safety_scores[
                action
            ]
            >= SAFETY_THRESHOLD
            and downside_scores[
                action
            ]
            <= DOWNSIDE_THRESHOLD
            and distances[
                action
            ]
            <= SUPPORT_THRESHOLD
        ):

            expanded.add(
                action
            )

    return (
        expanded,
        distances,
    )


def evaluate_seed(
    generation_seed: int,
    block_name: str,
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

    output = []

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

        (
            support_set,
            support_distances,
        ) = baseline_support_set(
            index,
            row,
            primary_set,
            test_risks[
                index
            ],
            test_losses[
                index
            ],
            safety_scores[
                index
            ],
            downside_scores[
                index
            ],
            support_objects,
        )

        primary_action = responsive_action(
            primary_set
        )

        support_action = responsive_action(
            support_set
        )

        true_responsive_action = responsive_action(
            true_set
        )

        true_action_losses = {
            action:
                selected_loss(
                    row,
                    action,
                )
            for action in ACTIONS
        }

        true_best_action = min(
            ACTIONS,
            key=lambda action:
                true_action_losses[
                    action
                ],
        )

        true_best_loss = min(
            true_action_losses.values()
        )

        true_loss_spread = (
            max(
                true_action_losses.values()
            )
            - min(
                true_action_losses.values()
            )
        )

        predicted_loss_spread = (
            max(
                float(
                    test_losses[
                        index
                    ][
                        action
                    ]
                )
                for action in ACTIONS
            )
            - min(
                float(
                    test_losses[
                        index
                    ][
                        action
                    ]
                )
                for action in ACTIONS
            )
        )

        support_regret = regret(
            row,
            support_action,
        )

        primary_regret = regret(
            row,
            primary_action,
        )

        support_under = int(
            support_action
            < true_best_action
        )

        support_over = int(
            support_action
            > true_best_action
        )

        output_row = {
            "block":
                block_name,

            "generation_seed":
                generation_seed,

            "test_index":
                index,

            "predicted_risk":
                float(
                    test_risks[
                        index
                    ]
                ),

            "predicted_loss_k1":
                float(
                    test_losses[
                        index
                    ][1]
                ),

            "predicted_loss_k2":
                float(
                    test_losses[
                        index
                    ][2]
                ),

            "predicted_loss_k3":
                float(
                    test_losses[
                        index
                    ][3]
                ),

            "predicted_loss_spread":
                predicted_loss_spread,

            "true_loss_k1":
                true_action_losses[
                    1
                ],

            "true_loss_k2":
                true_action_losses[
                    2
                ],

            "true_loss_k3":
                true_action_losses[
                    3
                ],

            "true_best_loss":
                true_best_loss,

            "true_loss_spread":
                true_loss_spread,

            "true_best_action":
                true_best_action,

            "true_responsive_action":
                true_responsive_action,

            "true_safe_action_count":
                len(
                    true_set
                ),

            "primary_safe_action_count":
                len(
                    primary_set
                ),

            "support_safe_action_count":
                len(
                    support_set
                ),

            "primary_action":
                primary_action,

            "support_action":
                support_action,

            "primary_regret":
                primary_regret,

            "support_regret":
                support_regret,

            "support_under":
                support_under,

            "support_over":
                support_over,

            "support_distance_k1":
                support_distances[
                    1
                ],

            "support_distance_k2":
                support_distances[
                    2
                ],

            "support_distance_k3":
                support_distances[
                    3
                ],

            "support_distance_selected":
                support_distances[
                    support_action
                ],

            "safety_score_selected":
                safety_scores[
                    index
                ][
                    support_action
                ],

            "downside_score_selected":
                downside_scores[
                    index
                ][
                    support_action
                ],
        }

        for feature_name in FEATURE_NAMES:

            output_row[
                f"context_{feature_name}"
            ] = float(
                row[
                    feature_name
                ]
            )

        output.append(
            output_row
        )

    return output


def summarize_numeric(
    rows: list[dict],
    block_name: str,
    field: str,
) -> dict:

    values = [
        float(
            row[
                field
            ]
        )
        for row in rows
        if row[
            "block"
        ]
        == block_name
    ]

    return {
        "count":
            len(
                values
            ),

        "mean":
            statistics.mean(
                values
            ),

        "median":
            statistics.median(
                values
            ),

        "min":
            min(
                values
            ),

        "max":
            max(
                values
            ),

        "std":
            statistics.pstdev(
                values
            )
            if len(
                values
            )
            > 1
            else 0.0,
    }


def standardized_difference(
    a_values: list[float],
    b_values: list[float],
) -> float:

    if (
        len(
            a_values
        )
        < 2
        or len(
            b_values
        )
        < 2
    ):

        return 0.0

    var_a = statistics.variance(
        a_values
    )

    var_b = statistics.variance(
        b_values
    )

    pooled_variance = (
        (
            (
                len(
                    a_values
                )
                - 1
            )
            * var_a
        )
        +
        (
            (
                len(
                    b_values
                )
                - 1
            )
            * var_b
        )
    ) / (
        len(
            a_values
        )
        + len(
            b_values
        )
        - 2
    )

    if (
        pooled_variance
        <= FLOAT_TOLERANCE
    ):

        return 0.0

    pooled_std = (
        pooled_variance
        ** 0.5
    )

    return (
        statistics.mean(
            b_values
        )
        - statistics.mean(
            a_values
        )
    ) / pooled_std


def build_summary(
    rows: list[dict],
) -> list[dict]:

    excluded = {
        "block",
        "generation_seed",
        "test_index",
    }

    numeric_fields = [
        field
        for field in rows[
            0
        ].keys()
        if field not in excluded
    ]

    summary_rows = []

    for field in numeric_fields:

        a_values = [
            float(
                row[
                    field
                ]
            )
            for row in rows
            if row[
                "block"
            ]
            == "block_086"
        ]

        b_values = [
            float(
                row[
                    field
                ]
            )
            for row in rows
            if row[
                "block"
            ]
            == "block_089"
        ]

        summary_rows.append(
            {
                "metric":
                    field,

                "block_086_mean":
                    statistics.mean(
                        a_values
                    ),

                "block_089_mean":
                    statistics.mean(
                        b_values
                    ),

                "difference_089_minus_086":
                    (
                        statistics.mean(
                            b_values
                        )
                        - statistics.mean(
                            a_values
                        )
                    ),

                "standardized_difference":
                    standardized_difference(
                        a_values,
                        b_values,
                    ),

                "block_086_median":
                    statistics.median(
                        a_values
                    ),

                "block_089_median":
                    statistics.median(
                        b_values
                    ),

                "block_086_min":
                    min(
                        a_values
                    ),

                "block_086_max":
                    max(
                        a_values
                    ),

                "block_089_min":
                    min(
                        b_values
                    ),

                "block_089_max":
                    max(
                        b_values
                    ),
            }
        )

    summary_rows.sort(
        key=lambda row: abs(
            float(
                row[
                    "standardized_difference"
                ]
            )
        ),
        reverse=True,
    )

    return summary_rows


def distribution_summary(
    rows: list[dict],
    block_name: str,
    field: str,
) -> Counter:

    return Counter(
        int(
            row[
                field
            ]
        )
        for row in rows
        if row[
            "block"
        ]
        == block_name
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

        for key in row:

            if key not in fields:
                fields.append(
                    key
                )

    normalized = []

    for row in rows:

        copy = dict(
            row
        )

        for field in fields:

            copy.setdefault(
                field,
                "",
            )

        normalized.append(
            copy
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
            normalized
        )


def main() -> None:

    all_rows = []

    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "CROSS-PROSPECTIVE-BLOCK "
        "REGIME-SHIFT DECOMPOSITION"
    )

    print(
        "=" * 210
    )

    print(
        f"Experiment 086 seeds="
        f"{BLOCK_A_SEEDS}"
    )

    print(
        f"Experiment 089 seeds="
        f"{BLOCK_B_SEEDS}"
    )

    print()

    for seed in BLOCK_A_SEEDS:

        print(
            f"reconstructing block 086 seed "
            f"{seed}..."
        )

        all_rows.extend(
            evaluate_seed(
                seed,
                "block_086",
            )
        )

    for seed in BLOCK_B_SEEDS:

        print(
            f"reconstructing block 089 seed "
            f"{seed}..."
        )

        all_rows.extend(
            evaluate_seed(
                seed,
                "block_089",
            )
        )

    summary_rows = build_summary(
        all_rows
    )

    save_csv(
        OUTPUT_PATH,
        summary_rows,
    )

    save_csv(
        CONTEXT_OUTPUT_PATH,
        all_rows,
    )

    block_086_rows = [
        row
        for row in all_rows
        if row[
            "block"
        ]
        == "block_086"
    ]

    block_089_rows = [
        row
        for row in all_rows
        if row[
            "block"
        ]
        == "block_089"
    ]

    print()

    print(
        "BLOCK SIZES"
    )

    print(
        f"block_086 contexts="
        f"{len(block_086_rows)}"
    )

    print(
        f"block_089 contexts="
        f"{len(block_089_rows)}"
    )

    print()

    print(
        "KEY CONSEQUENCE METRICS"
    )

    key_metrics = [
        "support_regret",
        "support_under",
        "support_over",
        "true_best_loss",
        "true_loss_spread",
        "predicted_risk",
        "predicted_loss_spread",
        "true_safe_action_count",
        "primary_safe_action_count",
        "support_safe_action_count",
        "support_distance_selected",
        "safety_score_selected",
        "downside_score_selected",
    ]

    summary_lookup = {
        row[
            "metric"
        ]:
            row
        for row in summary_rows
    }

    for metric in key_metrics:

        row = summary_lookup[
            metric
        ]

        print(
            f"{metric:<32} "
            f"086="
            f"{row['block_086_mean']:.6f} "
            f"089="
            f"{row['block_089_mean']:.6f} "
            f"delta="
            f"{row['difference_089_minus_086']:+.6f} "
            f"effect="
            f"{row['standardized_difference']:+.3f}"
        )

    print()

    print(
        "TRUE BEST-ACTION DISTRIBUTION"
    )

    for block_name in [
        "block_086",
        "block_089",
    ]:

        counts = distribution_summary(
            all_rows,
            block_name,
            "true_best_action",
        )

        total = sum(
            counts.values()
        )

        print(
            f"{block_name}: "
            f"k1="
            f"{counts.get(1, 0)} "
            f"({counts.get(1, 0) / total:.3%}) "
            f"k2="
            f"{counts.get(2, 0)} "
            f"({counts.get(2, 0) / total:.3%}) "
            f"k3="
            f"{counts.get(3, 0)} "
            f"({counts.get(3, 0) / total:.3%})"
        )

    print()

    print(
        "TRUE SAFE-ACTION-SET SIZE DISTRIBUTION"
    )

    for block_name in [
        "block_086",
        "block_089",
    ]:

        counts = distribution_summary(
            all_rows,
            block_name,
            "true_safe_action_count",
        )

        total = sum(
            counts.values()
        )

        print(
            f"{block_name}: "
            f"size1="
            f"{counts.get(1, 0)} "
            f"({counts.get(1, 0) / total:.3%}) "
            f"size2="
            f"{counts.get(2, 0)} "
            f"({counts.get(2, 0) / total:.3%}) "
            f"size3="
            f"{counts.get(3, 0)} "
            f"({counts.get(3, 0) / total:.3%})"
        )

    print()

    print(
        "TOP CONTEXT / MODEL SHIFTS"
    )

    filtered = [
        row
        for row in summary_rows
        if (
            row[
                "metric"
            ].startswith(
                "context_"
            )
            or row[
                "metric"
            ].startswith(
                "predicted_"
            )
            or row[
                "metric"
            ].startswith(
                "support_distance_"
            )
        )
    ]

    for row in filtered[
        :20
    ]:

        print(
            f"{row['metric']:<42} "
            f"086="
            f"{row['block_086_mean']:.6f} "
            f"089="
            f"{row['block_089_mean']:.6f} "
            f"effect="
            f"{row['standardized_difference']:+.3f}"
        )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 090 is diagnostic only. "
        "It compares two already-consumed prospective seed blocks "
        "and does not define or validate a new controller."
    )

    print(
        "=" * 210
    )

    print(
        f"Summary saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Context-level results saved to: "
        f"{CONTEXT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()