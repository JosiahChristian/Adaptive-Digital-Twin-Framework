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
)


OUTPUT_PATH = Path(
    "results/"
    "cross_seed_harmful_expansion_feature_decomposition.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "cross_seed_harmful_expansion_feature_decomposition_events.csv"
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


def responsive_action(
    actions: set[int],
) -> int:

    return min(
        actions
    )


def pooled_std(
    beneficial: list[float],
    harmful: list[float],
) -> float:

    if (
        len(
            beneficial
        )
        < 2
        or len(
            harmful
        )
        < 2
    ):

        return 0.0

    variance_b = statistics.variance(
        beneficial
    )

    variance_h = statistics.variance(
        harmful
    )

    numerator = (
        (
            len(
                beneficial
            )
            - 1
        )
        * variance_b
        +
        (
            len(
                harmful
            )
            - 1
        )
        * variance_h
    )

    denominator = (
        len(
            beneficial
        )
        + len(
            harmful
        )
        - 2
    )

    if denominator <= 0:

        return 0.0

    return math.sqrt(
        max(
            0.0,
            numerator
            / denominator,
        )
    )


def standardized_effect(
    beneficial: list[float],
    harmful: list[float],
) -> float:

    if (
        not beneficial
        or not harmful
    ):

        return 0.0

    scale = pooled_std(
        beneficial,
        harmful,
    )

    if (
        scale
        <= FLOAT_TOLERANCE
    ):

        return 0.0

    return (
        statistics.mean(
            harmful
        )
        - statistics.mean(
            beneficial
        )
    ) / scale


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

    for row in rows:

        for field in fields:

            row.setdefault(
                field,
                "",
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

    event_rows = []

    diagnostic_names = [
        "safety_score",
        "downside_score",
        "support_distance",
        "action_step",
        "predicted_regret_margin",
        "predicted_under_risk",
        "predicted_loss_k1",
        "predicted_loss_k2",
        "predicted_loss_k3",
        "predicted_loss_k1_minus_k2",
        "predicted_loss_k1_minus_k3",
        "predicted_loss_k2_minus_k3",
        "primary_regret",
        "expanded_regret",
        "incremental_regret",
    ]

    diagnostic_names.extend(
        [
            f"context_{name}"
            for name in FEATURE_NAMES
        ]
    )

    print(
        "=" * 205
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "CROSS-SEED HARMFUL-EXPANSION "
        "FEATURE DECOMPOSITION"
    )

    print(
        "=" * 205
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
        f"support threshold="
        f"{SUPPORT_THRESHOLD:.2f}"
    )

    print()

    for generation_seed in (
        BASE_GENERATION_SEEDS
    ):

        print(
            f"running seed "
            f"{generation_seed}..."
        )

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

            expanded_set = set(
                primary_set
            )

            for action in (
                ACTIONS
            ):

                if action in expanded_set:
                    continue

                distance = mean_knn_distance(
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
                    and distance
                    <= SUPPORT_THRESHOLD
                ):

                    expanded_set.add(
                        action
                    )

            primary_action = responsive_action(
                primary_set
            )

            expanded_action = responsive_action(
                expanded_set
            )

            if (
                expanded_action
                == primary_action
            ):

                continue

            true_responsive_action = responsive_action(
                true_set
            )

            primary_regret = regret(
                row,
                primary_action,
            )

            expanded_regret = regret(
                row,
                expanded_action,
            )

            incremental_regret = (
                expanded_regret
                - primary_regret
            )

            if (
                expanded_action
                == true_responsive_action
                and incremental_regret
                <= FLOAT_TOLERANCE
            ):

                outcome = "beneficial"

            elif (
                incremental_regret
                > FLOAT_TOLERANCE
            ):

                outcome = "harmful"

            else:

                outcome = "neutral"

            expanded_support_distance = (
                mean_knn_distance(
                    support_objects[
                        expanded_action
                    ],
                    action_specific_features(
                        row,
                        test_risks[
                            index
                        ],
                        test_losses[
                            index
                        ],
                        expanded_action,
                    ),
                )
            )

            predicted_primary_regret = min(
                predicted_regrets[
                    index
                ][
                    risk_level
                ]
                for risk_level
                in primary_levels
            )

            expanded_action_regret_candidates = [
                predicted_regrets[
                    index
                ][
                    risk_level
                ]
                for risk_level
                in RISK_LEVELS
                if int(
                    candidates[
                        risk_level
                    ][index]
                )
                == expanded_action
            ]

            predicted_expanded_regret = (
                min(
                    expanded_action_regret_candidates
                )
                if expanded_action_regret_candidates
                else predicted_primary_regret
            )

            event = {
                "generation_seed":
                    generation_seed,

                "test_index":
                    index,

                "outcome":
                    outcome,

                "primary_action":
                    primary_action,

                "expanded_action":
                    expanded_action,

                "true_responsive_action":
                    true_responsive_action,

                "action_step":
                    (
                        primary_action
                        - expanded_action
                    ),

                "safety_score":
                    safety_scores[
                        index
                    ][
                        expanded_action
                    ],

                "downside_score":
                    downside_scores[
                        index
                    ][
                        expanded_action
                    ],

                "support_distance":
                    expanded_support_distance,

                "predicted_under_risk":
                    test_risks[
                        index
                    ],

                "predicted_loss_k1":
                    test_losses[
                        index
                    ][1],

                "predicted_loss_k2":
                    test_losses[
                        index
                    ][2],

                "predicted_loss_k3":
                    test_losses[
                        index
                    ][3],

                "predicted_loss_k1_minus_k2":
                    (
                        test_losses[
                            index
                        ][1]
                        - test_losses[
                            index
                        ][2]
                    ),

                "predicted_loss_k1_minus_k3":
                    (
                        test_losses[
                            index
                        ][1]
                        - test_losses[
                            index
                        ][3]
                    ),

                "predicted_loss_k2_minus_k3":
                    (
                        test_losses[
                            index
                        ][2]
                        - test_losses[
                            index
                        ][3]
                    ),

                "predicted_primary_regret":
                    predicted_primary_regret,

                "predicted_expanded_regret":
                    predicted_expanded_regret,

                "predicted_regret_margin":
                    (
                        predicted_expanded_regret
                        - predicted_primary_regret
                    ),

                "primary_regret":
                    primary_regret,

                "expanded_regret":
                    expanded_regret,

                "incremental_regret":
                    incremental_regret,
            }

            for feature_name in (
                FEATURE_NAMES
            ):

                event[
                    f"context_{feature_name}"
                ] = float(
                    row[
                        feature_name
                    ]
                )

            event_rows.append(
                event
            )

    beneficial_rows = [
        row
        for row in event_rows
        if row[
            "outcome"
        ]
        == "beneficial"
    ]

    harmful_rows = [
        row
        for row in event_rows
        if row[
            "outcome"
        ]
        == "harmful"
    ]

    neutral_rows = [
        row
        for row in event_rows
        if row[
            "outcome"
        ]
        == "neutral"
    ]

    summary_rows = []

    for diagnostic in (
        diagnostic_names
    ):

        beneficial_values = [
            float(
                row[
                    diagnostic
                ]
            )
            for row in beneficial_rows
        ]

        harmful_values = [
            float(
                row[
                    diagnostic
                ]
            )
            for row in harmful_rows
        ]

        if (
            not beneficial_values
            or not harmful_values
        ):

            continue

        summary_rows.append(
            {
                "diagnostic":
                    diagnostic,

                "beneficial_count":
                    len(
                        beneficial_values
                    ),

                "harmful_count":
                    len(
                        harmful_values
                    ),

                "beneficial_mean":
                    statistics.mean(
                        beneficial_values
                    ),

                "harmful_mean":
                    statistics.mean(
                        harmful_values
                    ),

                "beneficial_median":
                    statistics.median(
                        beneficial_values
                    ),

                "harmful_median":
                    statistics.median(
                        harmful_values
                    ),

                "beneficial_min":
                    min(
                        beneficial_values
                    ),

                "beneficial_max":
                    max(
                        beneficial_values
                    ),

                "harmful_min":
                    min(
                        harmful_values
                    ),

                "harmful_max":
                    max(
                        harmful_values
                    ),

                "mean_difference_harmful_minus_beneficial":
                    (
                        statistics.mean(
                            harmful_values
                        )
                        - statistics.mean(
                            beneficial_values
                        )
                    ),

                "standardized_effect_harmful_minus_beneficial":
                    standardized_effect(
                        beneficial_values,
                        harmful_values,
                    ),
            }
        )

    summary_rows.sort(
        key=lambda row: abs(
            float(
                row[
                    "standardized_effect_harmful_minus_beneficial"
                ]
            )
        ),
        reverse=True,
    )

    save_csv(
        OUTPUT_PATH,
        summary_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        event_rows,
    )

    print()

    print(
        "POOLED EVENT COUNTS"
    )

    print(
        f"beneficial="
        f"{len(beneficial_rows)}"
    )

    print(
        f"harmful="
        f"{len(harmful_rows)}"
    )

    print(
        f"neutral="
        f"{len(neutral_rows)}"
    )

    print(
        f"total_action_changes="
        f"{len(event_rows)}"
    )

    print()

    print(
        "TOP STANDARDIZED FEATURE SEPARATION"
    )

    for row in summary_rows[
        :15
    ]:

        print(
            f"{row['diagnostic']:<40} "
            f"beneficial_mean="
            f"{row['beneficial_mean']:.6f} "
            f"harmful_mean="
            f"{row['harmful_mean']:.6f} "
            f"effect="
            f"{row['standardized_effect_harmful_minus_beneficial']:+.3f} "
            f"harmful_range=["
            f"{row['harmful_min']:.6f},"
            f"{row['harmful_max']:.6f}"
            f"]"
        )

    print()

    print(
        "CORE GATE DIAGNOSTICS"
    )

    core_names = [
        "safety_score",
        "downside_score",
        "support_distance",
        "action_step",
        "predicted_regret_margin",
        "predicted_under_risk",
    ]

    for name in (
        core_names
    ):

        matching = [
            row
            for row in summary_rows
            if row[
                "diagnostic"
            ]
            == name
        ]

        if not matching:
            continue

        row = matching[
            0
        ]

        print(
            f"{name:<28} "
            f"beneficial="
            f"{row['beneficial_mean']:.6f} "
            f"harmful="
            f"{row['harmful_mean']:.6f} "
            f"effect="
            f"{row['standardized_effect_harmful_minus_beneficial']:+.3f}"
        )

    print()

    print(
        "HARMFUL EVENT DETAILS"
    )

    if not harmful_rows:

        print(
            "No harmful events."
        )

    else:

        for row in (
            harmful_rows
        ):

            print(
                f"seed="
                f"{row['generation_seed']} "
                f"index="
                f"{row['test_index']} "
                f"primary="
                f"{row['primary_action']} "
                f"expanded="
                f"{row['expanded_action']} "
                f"true_responsive="
                f"{row['true_responsive_action']} "
                f"step="
                f"{row['action_step']} "
                f"safety="
                f"{row['safety_score']:.3f} "
                f"downside="
                f"{row['downside_score']:.6f} "
                f"support="
                f"{row['support_distance']:.3f} "
                f"pred_margin="
                f"{row['predicted_regret_margin']:.6f} "
                f"incremental_regret="
                f"{row['incremental_regret']:.6f}"
            )

    print(
        "=" * 205
    )

    print(
        f"Feature summary saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Event-level results saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()