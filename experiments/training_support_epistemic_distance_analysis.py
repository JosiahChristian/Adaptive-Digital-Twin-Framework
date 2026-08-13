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
    "training_support_epistemic_distance_analysis.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "training_support_epistemic_distance_analysis_contexts.csv"
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


def standardized_support_data(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
    action: int,
) -> tuple[
    StandardScaler,
    np.ndarray,
]:

    x = np.asarray(
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

    x_scaled = scaler.fit_transform(
        x
    )

    return (
        scaler,
        x_scaled,
    )


def euclidean_distances(
    training_matrix: np.ndarray,
    sample: np.ndarray,
) -> np.ndarray:

    return np.sqrt(
        np.sum(
            (
                training_matrix
                - sample
            )
            ** 2,
            axis=1,
        )
    )


def support_metrics(
    training_matrix: np.ndarray,
    training_labels: np.ndarray,
    sample: np.ndarray,
) -> dict:

    distances = euclidean_distances(
        training_matrix,
        sample,
    )

    order = np.argsort(
        distances
    )

    nearest_index = int(
        order[0]
    )

    k = min(
        K_NEIGHBORS,
        len(
            order
        ),
    )

    nearest_k = order[
        :k
    ]

    nearest_distance = float(
        distances[
            nearest_index
        ]
    )

    mean_knn_distance = float(
        np.mean(
            distances[
                nearest_k
            ]
        )
    )

    local_safe_fraction = float(
        np.mean(
            training_labels[
                nearest_k
            ]
        )
    )

    safe_mask = (
        training_labels
        == 1
    )

    unsafe_mask = (
        training_labels
        == 0
    )

    nearest_safe_distance = (
        float(
            np.min(
                distances[
                    safe_mask
                ]
            )
        )
        if np.any(
            safe_mask
        )
        else math.inf
    )

    nearest_unsafe_distance = (
        float(
            np.min(
                distances[
                    unsafe_mask
                ]
            )
        )
        if np.any(
            unsafe_mask
        )
        else math.inf
    )

    safe_distance_advantage = (
        nearest_unsafe_distance
        - nearest_safe_distance
    )

    return {
        "nearest_distance":
            nearest_distance,

        "mean_knn_distance":
            mean_knn_distance,

        "local_safe_fraction":
            local_safe_fraction,

        "nearest_safe_distance":
            nearest_safe_distance,

        "nearest_unsafe_distance":
            nearest_unsafe_distance,

        "safe_distance_advantage":
            safe_distance_advantage,
    }


def mahalanobis_setup(
    training_matrix: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:

    mean = np.mean(
        training_matrix,
        axis=0,
    )

    covariance = np.cov(
        training_matrix,
        rowvar=False,
    )

    covariance += (
        np.eye(
            covariance.shape[
                0
            ]
        )
        * 1e-6
    )

    inverse_covariance = np.linalg.pinv(
        covariance
    )

    return (
        mean,
        inverse_covariance,
    )


def mahalanobis_distance(
    sample: np.ndarray,
    mean: np.ndarray,
    inverse_covariance: np.ndarray,
) -> float:

    delta = (
        sample
        - mean
    )

    squared = float(
        delta.T
        @ inverse_covariance
        @ delta
    )

    return math.sqrt(
        max(
            0.0,
            squared,
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


def mean_field(
    records: list[dict],
    field: str,
) -> float:

    if not records:
        return 0.0

    return statistics.mean(
        float(
            record[
                field
            ]
        )
        for record in records
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

    support_objects = {}

    meta_true_regrets = true_regret_table(
        meta_train_rows,
        meta_candidates,
    )

    for action in (
        ACTIONS
    ):

        (
            scaler,
            training_matrix,
        ) = standardized_support_data(
            meta_train_rows,
            meta_losses,
            meta_risks,
            action,
        )

        training_labels = np.asarray(
            [
                int(
                    action
                    in true_safe_actions(
                        meta_true_regrets[
                            index
                        ],
                        meta_candidates,
                        index,
                    )
                )
                for index in range(
                    len(
                        meta_train_rows
                    )
                )
            ],
            dtype=int,
        )

        (
            mahalanobis_mean,
            inverse_covariance,
        ) = mahalanobis_setup(
            training_matrix
        )

        support_objects[
            action
        ] = {
            "scaler":
                scaler,

            "training_matrix":
                training_matrix,

            "training_labels":
                training_labels,

            "mahalanobis_mean":
                mahalanobis_mean,

            "inverse_covariance":
                inverse_covariance,
        }

    context_rows = []

    beneficial_rows = []
    neutral_rows = []
    harmful_rows = []

    for index, row in enumerate(
        test_rows
    ):

        primary_levels = predicted_safe_levels(
            predicted_regrets[
                index
            ]
        )

        primary_actions = action_set_from_levels(
            primary_levels,
            candidates,
            index,
        )

        true_actions = true_safe_actions(
            true_regrets[
                index
            ],
            candidates,
            index,
        )

        expanded_actions = set(
            primary_actions
        )

        added_actions = []

        for action in (
            ACTIONS
        ):

            if action in expanded_actions:
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

                expanded_actions.add(
                    action
                )

                added_actions.append(
                    action
                )

        primary_action = responsive_action(
            primary_actions
        )

        expanded_action = responsive_action(
            expanded_actions
        )

        true_responsive_action = responsive_action(
            true_actions
        )

        primary_regret = regret(
            row,
            primary_action,
        )

        expanded_regret = regret(
            row,
            expanded_action,
        )

        changed_action = (
            expanded_action
            != primary_action
        )

        if not changed_action:

            outcome = "neutral"

        elif (
            expanded_action
            == true_responsive_action
            and expanded_regret
            <= primary_regret
            + FLOAT_TOLERANCE
        ):

            outcome = "beneficial"

        elif (
            expanded_regret
            > primary_regret
            + FLOAT_TOLERANCE
        ):

            outcome = "harmful"

        else:

            outcome = "neutral"

        support = support_objects[
            expanded_action
        ]

        raw_sample = np.asarray(
            [
                action_specific_features(
                    row,
                    test_risks[
                        index
                    ],
                    test_losses[
                        index
                    ],
                    expanded_action,
                )
            ],
            dtype=float,
        )

        scaled_sample = support[
            "scaler"
        ].transform(
            raw_sample
        )[0]

        metrics = support_metrics(
            support[
                "training_matrix"
            ],
            support[
                "training_labels"
            ],
            scaled_sample,
        )

        mahalanobis = mahalanobis_distance(
            scaled_sample,
            support[
                "mahalanobis_mean"
            ],
            support[
                "inverse_covariance"
            ],
        )

        record = {
            "test_index":
                index,

            "outcome":
                outcome,

            "primary_actions":
                action_text(
                    primary_actions
                ),

            "expanded_actions":
                action_text(
                    expanded_actions
                ),

            "true_safe_actions":
                action_text(
                    true_actions
                ),

            "added_actions":
                action_text(
                    set(
                        added_actions
                    )
                ),

            "primary_action":
                primary_action,

            "expanded_action":
                expanded_action,

            "true_responsive_action":
                true_responsive_action,

            "primary_regret":
                primary_regret,

            "expanded_regret":
                expanded_regret,

            "incremental_regret":
                (
                    expanded_regret
                    - primary_regret
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

            "nearest_distance":
                metrics[
                    "nearest_distance"
                ],

            "mean_knn_distance":
                metrics[
                    "mean_knn_distance"
                ],

            "local_safe_fraction":
                metrics[
                    "local_safe_fraction"
                ],

            "nearest_safe_distance":
                metrics[
                    "nearest_safe_distance"
                ],

            "nearest_unsafe_distance":
                metrics[
                    "nearest_unsafe_distance"
                ],

            "safe_distance_advantage":
                metrics[
                    "safe_distance_advantage"
                ],

            "mahalanobis_distance":
                mahalanobis,
        }

        context_rows.append(
            record
        )

        if outcome == "beneficial":

            beneficial_rows.append(
                record
            )

        elif outcome == "harmful":

            harmful_rows.append(
                record
            )

        else:

            neutral_rows.append(
                record
            )

    summary_rows = []

    for label, records in [
        (
            "beneficial",
            beneficial_rows,
        ),
        (
            "neutral",
            neutral_rows,
        ),
        (
            "harmful",
            harmful_rows,
        ),
    ]:

        summary_rows.append(
            {
                "outcome":
                    label,

                "contexts":
                    len(
                        records
                    ),

                "fraction":
                    (
                        len(
                            records
                        )
                        / len(
                            test_rows
                        )
                    ),

                "mean_nearest_distance":
                    mean_field(
                        records,
                        "nearest_distance",
                    ),

                "mean_knn_distance":
                    mean_field(
                        records,
                        "mean_knn_distance",
                    ),

                "mean_local_safe_fraction":
                    mean_field(
                        records,
                        "local_safe_fraction",
                    ),

                "mean_nearest_safe_distance":
                    mean_field(
                        records,
                        "nearest_safe_distance",
                    ),

                "mean_nearest_unsafe_distance":
                    mean_field(
                        records,
                        "nearest_unsafe_distance",
                    ),

                "mean_safe_distance_advantage":
                    mean_field(
                        records,
                        "safe_distance_advantage",
                    ),

                "mean_mahalanobis_distance":
                    mean_field(
                        records,
                        "mahalanobis_distance",
                    ),

                "mean_safety_score":
                    mean_field(
                        records,
                        "safety_score",
                    ),

                "mean_downside_score":
                    mean_field(
                        records,
                        "downside_score",
                    ),

                "mean_realized_regret":
                    mean_field(
                        records,
                        "expanded_regret",
                    ),
            }
        )

    save_csv(
        OUTPUT_PATH,
        summary_rows,
    )

    save_csv(
        CONTEXT_OUTPUT_PATH,
        context_rows,
    )

    print("=" * 200)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "TRAINING-SUPPORT EPISTEMIC "
        "DISTANCE ANALYSIS"
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
        f"support-model contexts="
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
        "SUPPORT-DISTANCE SUMMARY"
    )

    for summary in (
        summary_rows
    ):

        print(
            f"{summary['outcome']:<12} "
            f"n="
            f"{summary['contexts']:<2} "
            f"NN="
            f"{summary['mean_nearest_distance']:.3f} "
            f"kNN="
            f"{summary['mean_knn_distance']:.3f} "
            f"local_safe="
            f"{summary['mean_local_safe_fraction']:.3f} "
            f"nearest_safe="
            f"{summary['mean_nearest_safe_distance']:.3f} "
            f"nearest_unsafe="
            f"{summary['mean_nearest_unsafe_distance']:.3f} "
            f"safe_advantage="
            f"{summary['mean_safe_distance_advantage']:.3f} "
            f"mahalanobis="
            f"{summary['mean_mahalanobis_distance']:.3f} "
            f"safety="
            f"{summary['mean_safety_score']:.3f} "
            f"downside="
            f"{summary['mean_downside_score']:.6f} "
            f"realized="
            f"{summary['mean_realized_regret']:.6f}"
        )

    print()

    print(
        "HARMFUL CONTEXT DETAILS"
    )

    if not harmful_rows:

        print(
            "No harmful expansion contexts."
        )

    else:

        for record in harmful_rows:

            print(
                f"test_index="
                f"{record['test_index']} "
                f"primary="
                f"{record['primary_action']} "
                f"expanded="
                f"{record['expanded_action']} "
                f"true_safe="
                f"{record['true_safe_actions']} "
                f"NN="
                f"{record['nearest_distance']:.3f} "
                f"kNN="
                f"{record['mean_knn_distance']:.3f} "
                f"local_safe="
                f"{record['local_safe_fraction']:.3f} "
                f"nearest_safe="
                f"{record['nearest_safe_distance']:.3f} "
                f"nearest_unsafe="
                f"{record['nearest_unsafe_distance']:.3f} "
                f"safe_advantage="
                f"{record['safe_distance_advantage']:.3f} "
                f"mahalanobis="
                f"{record['mahalanobis_distance']:.3f} "
                f"safety="
                f"{record['safety_score']:.3f} "
                f"downside="
                f"{record['downside_score']:.6f} "
                f"realized="
                f"{record['expanded_regret']:.6f}"
            )

    print("=" * 200)

    print(
        f"Summary results saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Context results saved to: "
        f"{CONTEXT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()