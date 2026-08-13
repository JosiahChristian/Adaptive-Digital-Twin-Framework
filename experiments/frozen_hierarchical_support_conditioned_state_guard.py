import csv
import statistics
from pathlib import Path

import numpy as np

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LogisticRegression
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
    evaluate_policy,
)


RETROSPECTIVE_EVENT_PATH = Path(
    "results/"
    "cross_seed_harmful_expansion_feature_decomposition_events.csv"
)

OUTPUT_PATH = Path(
    "results/"
    "frozen_hierarchical_support_conditioned_state_guard.csv"
)

SEED_OUTPUT_PATH = Path(
    "results/"
    "frozen_hierarchical_support_conditioned_state_guard_seeds.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "frozen_hierarchical_support_conditioned_state_guard_events.csv"
)


PROSPECTIVE_SEEDS = list(
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

SUPPORT_ADMISSION_THRESHOLD = 2.50
SELECTIVE_SUPPORT_THRESHOLD = 2.00
STATE_THRESHOLD = 0.50

STATE_FEATURES = [
    "current_mismatch_indicator",
    "anchor_age",
    "trigger_score",
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


def read_retrospective_events() -> list[dict]:

    with RETROSPECTIVE_EVENT_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        rows = list(
            csv.DictReader(
                file
            )
        )

    return [
        row
        for row in rows
        if row[
            "outcome"
        ]
        in (
            "beneficial",
            "harmful",
        )
    ]


def train_frozen_state_model() -> tuple[
    StandardScaler,
    LogisticRegression,
]:

    rows = read_retrospective_events()

    x = np.asarray(
        [
            [
                float(
                    row[
                        f"context_{feature}"
                    ]
                )
                for feature in STATE_FEATURES
            ]
            for row in rows
        ],
        dtype=float,
    )

    y = np.asarray(
        [
            int(
                row[
                    "outcome"
                ]
                == "harmful"
            )
            for row in rows
        ],
        dtype=int,
    )

    scaler = StandardScaler()

    x_scaled = scaler.fit_transform(
        x
    )

    model = LogisticRegression(
        class_weight="balanced",
        l1_ratio=0,
        C=1.0,
        solver="liblinear",
        random_state=RANDOM_STATE,
        max_iter=5000,
    )

    model.fit(
        x_scaled,
        y,
    )

    return (
        scaler,
        model,
    )


def state_harmful_probability(
    scaler: StandardScaler,
    model: LogisticRegression,
    row: dict,
) -> float:

    x = np.asarray(
        [
            [
                float(
                    row[
                        feature
                    ]
                )
                for feature in STATE_FEATURES
            ]
        ],
        dtype=float,
    )

    x_scaled = scaler.transform(
        x
    )

    return float(
        model.predict_proba(
            x_scaled
        )[
            0,
            1
        ]
    )


def expansion_outcome(
    row: dict,
    primary_action: int,
    expanded_action: int,
    true_responsive_action: int,
) -> str:

    if (
        expanded_action
        == primary_action
    ):

        return "none"

    primary_regret = regret(
        row,
        primary_action,
    )

    expanded_regret = regret(
        row,
        expanded_action,
    )

    incremental = (
        expanded_regret
        - primary_regret
    )

    if (
        expanded_action
        == true_responsive_action
        and incremental
        <= FLOAT_TOLERANCE
    ):

        return "beneficial"

    if (
        incremental
        > FLOAT_TOLERANCE
    ):

        return "harmful"

    return "neutral"


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


def policy_metrics(
    name: str,
    action_sets: list[set[int]],
    rows: list[dict],
    direct: list[int],
    true_sets: list[set[int]],
    primary_sets: list[set[int]],
) -> dict:

    actions = [
        responsive_action(
            action_set
        )
        for action_set in action_sets
    ]

    result = evaluate_policy(
        name=name,
        predictions=actions,
        rows=rows,
        direct=direct,
    )

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
                action_sets,
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
                action_sets,
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
                action_sets,
            )
        ]
    )

    outcomes = []

    for index, row in enumerate(
        rows
    ):

        outcomes.append(
            expansion_outcome(
                row,
                responsive_action(
                    primary_sets[
                        index
                    ]
                ),
                responsive_action(
                    action_sets[
                        index
                    ]
                ),
                responsive_action(
                    true_sets[
                        index
                    ]
                ),
            )
        )

    result[
        "expansion_contexts"
    ] = sum(
        int(
            outcome
            != "none"
        )
        for outcome in outcomes
    )

    result[
        "beneficial_expansions"
    ] = sum(
        int(
            outcome
            == "beneficial"
        )
        for outcome in outcomes
    )

    result[
        "harmful_expansions"
    ] = sum(
        int(
            outcome
            == "harmful"
        )
        for outcome in outcomes
    )

    result[
        "neutral_expansions"
    ] = sum(
        int(
            outcome
            == "neutral"
        )
        for outcome in outcomes
    )

    return result


def evaluate_seed(
    generation_seed: int,
    state_scaler: StandardScaler,
    state_model: LogisticRegression,
) -> tuple[
    list[dict],
    list[dict],
]:

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
    baseline_sets = []
    unconditional_sets = []
    hierarchical_sets = []

    event_rows = []

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

        baseline_set = set(
            primary_set
        )

        action_distances = {}

        for action in ACTIONS:

            action_distances[
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

            if action in baseline_set:
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
                and action_distances[
                    action
                ]
                <= SUPPORT_ADMISSION_THRESHOLD
            ):

                baseline_set.add(
                    action
                )

        primary_action = responsive_action(
            primary_set
        )

        baseline_action = responsive_action(
            baseline_set
        )

        q_state = state_harmful_probability(
            state_scaler,
            state_model,
            row,
        )

        baseline_distance = action_distances[
            baseline_action
        ]

        unconditional_set = set(
            baseline_set
        )

        unconditional_veto = False

        if (
            baseline_action
            != primary_action
            and q_state
            >= STATE_THRESHOLD
        ):

            unconditional_set = set(
                primary_set
            )

            unconditional_veto = True

        hierarchical_set = set(
            baseline_set
        )

        hierarchical_veto = False

        if (
            baseline_action
            != primary_action
            and q_state
            >= STATE_THRESHOLD
            and baseline_distance
            > SELECTIVE_SUPPORT_THRESHOLD
        ):

            hierarchical_set = set(
                primary_set
            )

            hierarchical_veto = True

        primary_sets.append(
            primary_set
        )

        true_sets.append(
            true_set
        )

        baseline_sets.append(
            baseline_set
        )

        unconditional_sets.append(
            unconditional_set
        )

        hierarchical_sets.append(
            hierarchical_set
        )

        true_responsive_action = responsive_action(
            true_set
        )

        baseline_outcome = expansion_outcome(
            row,
            primary_action,
            baseline_action,
            true_responsive_action,
        )

        event_rows.append(
            {
                "generation_seed":
                    generation_seed,

                "test_index":
                    index,

                "primary_action":
                    primary_action,

                "baseline_action":
                    baseline_action,

                "unconditional_action":
                    responsive_action(
                        unconditional_set
                    ),

                "hierarchical_action":
                    responsive_action(
                        hierarchical_set
                    ),

                "true_responsive_action":
                    true_responsive_action,

                "baseline_expansion":
                    int(
                        baseline_action
                        != primary_action
                    ),

                "baseline_outcome":
                    baseline_outcome,

                "state_harmful_probability":
                    q_state,

                "support_distance_baseline_action":
                    baseline_distance,

                "unconditional_veto":
                    int(
                        unconditional_veto
                    ),

                "hierarchical_veto":
                    int(
                        hierarchical_veto
                    ),

                "hierarchical_support_condition":
                    int(
                        baseline_distance
                        > SELECTIVE_SUPPORT_THRESHOLD
                    ),

                "current_mismatch_indicator":
                    float(
                        row[
                            "current_mismatch_indicator"
                        ]
                    ),

                "anchor_age":
                    float(
                        row[
                            "anchor_age"
                        ]
                    ),

                "trigger_score":
                    float(
                        row[
                            "trigger_score"
                        ]
                    ),

                "safety_score_baseline_action":
                    safety_scores[
                        index
                    ][
                        baseline_action
                    ],

                "downside_score_baseline_action":
                    downside_scores[
                        index
                    ][
                        baseline_action
                    ],

                "baseline_regret":
                    regret(
                        row,
                        baseline_action,
                    ),

                "unconditional_regret":
                    regret(
                        row,
                        responsive_action(
                            unconditional_set
                        ),
                    ),

                "hierarchical_regret":
                    regret(
                        row,
                        responsive_action(
                            hierarchical_set
                        ),
                    ),
            }
        )

    seed_results = []

    baseline_result = policy_metrics(
        name="support_baseline",
        action_sets=baseline_sets,
        rows=test_rows,
        direct=direct,
        true_sets=true_sets,
        primary_sets=primary_sets,
    )

    unconditional_result = policy_metrics(
        name="state_guard_0.50",
        action_sets=unconditional_sets,
        rows=test_rows,
        direct=direct,
        true_sets=true_sets,
        primary_sets=primary_sets,
    )

    hierarchical_result = policy_metrics(
        name="hierarchical_guard",
        action_sets=hierarchical_sets,
        rows=test_rows,
        direct=direct,
        true_sets=true_sets,
        primary_sets=primary_sets,
    )

    for result in [
        baseline_result,
        unconditional_result,
        hierarchical_result,
    ]:

        result[
            "generation_seed"
        ] = generation_seed

    baseline_expansion_rows = [
        row
        for row in event_rows
        if row[
            "baseline_expansion"
        ]
        == 1
    ]

    baseline_harmful = sum(
        int(
            row[
                "baseline_outcome"
            ]
            == "harmful"
        )
        for row in baseline_expansion_rows
    )

    baseline_beneficial = sum(
        int(
            row[
                "baseline_outcome"
            ]
            == "beneficial"
        )
        for row in baseline_expansion_rows
    )

    for (
        result,
        veto_field,
    ) in [
        (
            unconditional_result,
            "unconditional_veto",
        ),
        (
            hierarchical_result,
            "hierarchical_veto",
        ),
    ]:

        veto_rows = [
            row
            for row in baseline_expansion_rows
            if row[
                veto_field
            ]
            == 1
        ]

        harmful_vetoed = sum(
            int(
                row[
                    "baseline_outcome"
                ]
                == "harmful"
            )
            for row in veto_rows
        )

        beneficial_vetoed = sum(
            int(
                row[
                    "baseline_outcome"
                ]
                == "beneficial"
            )
            for row in veto_rows
        )

        result[
            "veto_count"
        ] = len(
            veto_rows
        )

        result[
            "harmful_vetoed"
        ] = harmful_vetoed

        result[
            "beneficial_vetoed"
        ] = beneficial_vetoed

        result[
            "harmful_veto_recall"
        ] = (
            harmful_vetoed
            / baseline_harmful
            if baseline_harmful
            > 0
            else 0.0
        )

        result[
            "beneficial_preservation"
        ] = (
            (
                baseline_beneficial
                - beneficial_vetoed
            )
            / baseline_beneficial
            if baseline_beneficial
            > 0
            else 1.0
        )

    baseline_result[
        "veto_count"
    ] = 0

    baseline_result[
        "harmful_vetoed"
    ] = 0

    baseline_result[
        "beneficial_vetoed"
    ] = 0

    baseline_result[
        "harmful_veto_recall"
    ] = 0.0

    baseline_result[
        "beneficial_preservation"
    ] = 1.0

    seed_results.extend(
        [
            baseline_result,
            unconditional_result,
            hierarchical_result,
        ]
    )

    return (
        seed_results,
        event_rows,
    )


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

    output = []

    numeric_fields = [
        "mean_regret",
        "under_count",
        "over_count",
        "action_entropy",
        "safe_action_recall",
        "safe_action_precision",
        "responsive_action_retention",
        "expansion_contexts",
        "beneficial_expansions",
        "harmful_expansions",
        "neutral_expansions",
        "veto_count",
        "harmful_vetoed",
        "beneficial_vetoed",
        "harmful_veto_recall",
        "beneficial_preservation",
    ]

    for policy in policies:

        rows = [
            row
            for row in seed_rows
            if row[
                "policy"
            ]
            == policy
        ]

        result = {
            "policy":
                policy,

            "seeds":
                len(
                    rows
                ),
        }

        for field in numeric_fields:

            values = [
                float(
                    row[
                        field
                    ]
                )
                for row in rows
                if row.get(
                    field,
                    "",
                )
                not in (
                    "",
                    None,
                )
            ]

            if not values:
                continue

            result[
                f"mean_{field}"
            ] = statistics.mean(
                values
            )

            result[
                f"median_{field}"
            ] = statistics.median(
                values
            )

            result[
                f"min_{field}"
            ] = min(
                values
            )

            result[
                f"max_{field}"
            ] = max(
                values
            )

        output.append(
            result
        )

    return output


def paired_summary(
    seed_rows: list[dict],
    comparison_policy: str,
) -> dict:

    by_seed = {}

    for row in seed_rows:

        seed = int(
            row[
                "generation_seed"
            ]
        )

        by_seed.setdefault(
            seed,
            {}
        )

        by_seed[
            seed
        ][
            row[
                "policy"
            ]
        ] = row

    delta_regret = []
    delta_under = []
    delta_harmful = []
    delta_beneficial = []
    delta_retention = []

    regret_improved = 0
    regret_unchanged = 0
    regret_degraded = 0

    harmful_improved = 0
    harmful_unchanged = 0
    harmful_degraded = 0

    for seed in sorted(
        by_seed
    ):

        baseline = by_seed[
            seed
        ][
            "support_baseline"
        ]

        comparison = by_seed[
            seed
        ][
            comparison_policy
        ]

        d_regret = (
            float(
                comparison[
                    "mean_regret"
                ]
            )
            - float(
                baseline[
                    "mean_regret"
                ]
            )
        )

        d_under = (
            int(
                comparison[
                    "under_count"
                ]
            )
            - int(
                baseline[
                    "under_count"
                ]
            )
        )

        d_harmful = (
            int(
                comparison[
                    "harmful_expansions"
                ]
            )
            - int(
                baseline[
                    "harmful_expansions"
                ]
            )
        )

        d_beneficial = (
            int(
                comparison[
                    "beneficial_expansions"
                ]
            )
            - int(
                baseline[
                    "beneficial_expansions"
                ]
            )
        )

        d_retention = (
            float(
                comparison[
                    "responsive_action_retention"
                ]
            )
            - float(
                baseline[
                    "responsive_action_retention"
                ]
            )
        )

        delta_regret.append(
            d_regret
        )

        delta_under.append(
            float(
                d_under
            )
        )

        delta_harmful.append(
            float(
                d_harmful
            )
        )

        delta_beneficial.append(
            float(
                d_beneficial
            )
        )

        delta_retention.append(
            d_retention
        )

        if d_regret < -FLOAT_TOLERANCE:
            regret_improved += 1
        elif d_regret > FLOAT_TOLERANCE:
            regret_degraded += 1
        else:
            regret_unchanged += 1

        if d_harmful < 0:
            harmful_improved += 1
        elif d_harmful > 0:
            harmful_degraded += 1
        else:
            harmful_unchanged += 1

    return {
        "comparison_policy":
            comparison_policy,

        "mean_delta_regret":
            statistics.mean(
                delta_regret
            ),

        "median_delta_regret":
            statistics.median(
                delta_regret
            ),

        "min_delta_regret":
            min(
                delta_regret
            ),

        "max_delta_regret":
            max(
                delta_regret
            ),

        "mean_delta_under":
            statistics.mean(
                delta_under
            ),

        "mean_delta_harmful":
            statistics.mean(
                delta_harmful
            ),

        "mean_delta_beneficial":
            statistics.mean(
                delta_beneficial
            ),

        "mean_delta_retention":
            statistics.mean(
                delta_retention
            ),

        "regret_improved":
            regret_improved,

        "regret_unchanged":
            regret_unchanged,

        "regret_degraded":
            regret_degraded,

        "harmful_improved":
            harmful_improved,

        "harmful_unchanged":
            harmful_unchanged,

        "harmful_degraded":
            harmful_degraded,
    }


def main() -> None:

    state_scaler, state_model = (
        train_frozen_state_model()
    )

    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "FROZEN HIERARCHICAL SUPPORT-CONDITIONED "
        "STATE GUARD"
    )

    print(
        "=" * 210
    )

    print(
        f"prospective seeds="
        f"{PROSPECTIVE_SEEDS}"
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
        f"support admission threshold="
        f"{SUPPORT_ADMISSION_THRESHOLD:.2f}"
    )

    print(
        f"state threshold="
        f"{STATE_THRESHOLD:.2f}"
    )

    print(
        f"hierarchical support threshold="
        f"{SELECTIVE_SUPPORT_THRESHOLD:.2f}"
    )

    print()

    all_seed_rows = []
    all_event_rows = []

    for generation_seed in (
        PROSPECTIVE_SEEDS
    ):

        print(
            f"running prospective seed "
            f"{generation_seed}..."
        )

        (
            seed_rows,
            event_rows,
        ) = evaluate_seed(
            generation_seed,
            state_scaler,
            state_model,
        )

        all_seed_rows.extend(
            seed_rows
        )

        all_event_rows.extend(
            event_rows
        )

    aggregate = aggregate_results(
        all_seed_rows
    )

    unconditional_pair = paired_summary(
        all_seed_rows,
        "state_guard_0.50",
    )

    hierarchical_pair = paired_summary(
        all_seed_rows,
        "hierarchical_guard",
    )

    save_csv(
        OUTPUT_PATH,
        aggregate,
    )

    save_csv(
        SEED_OUTPUT_PATH,
        all_seed_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        all_event_rows,
    )

    print()

    print(
        "PROSPECTIVE POLICY SUMMARY"
    )

    ordered = [
        "support_baseline",
        "state_guard_0.50",
        "hierarchical_guard",
    ]

    for policy in ordered:

        matching = [
            row
            for row in aggregate
            if row[
                "policy"
            ]
            == policy
        ]

        if not matching:
            continue

        row = matching[
            0
        ]

        print(
            f"{policy:<22} "
            f"mean_R="
            f"{row['mean_mean_regret']:.6f} "
            f"mean_under="
            f"{row['mean_under_count']:.2f} "
            f"mean_over="
            f"{row['mean_over_count']:.2f} "
            f"mean_H="
            f"{row['mean_action_entropy']:.3f} "
            f"recall="
            f"{row['mean_safe_action_recall']:.3%} "
            f"precision="
            f"{row['mean_safe_action_precision']:.3%} "
            f"retention="
            f"{row['mean_responsive_action_retention']:.3%} "
            f"beneficial="
            f"{row['mean_beneficial_expansions']:.2f} "
            f"harmful="
            f"{row['mean_harmful_expansions']:.2f} "
            f"veto="
            f"{row['mean_veto_count']:.2f}"
        )

        if (
            policy
            != "support_baseline"
        ):

            print(
                f"{'':<22} "
                f"mean_harmful_veto_recall="
                f"{row['mean_harmful_veto_recall']:.3%} "
                f"mean_beneficial_preservation="
                f"{row['mean_beneficial_preservation']:.3%}"
            )

    print()

    print(
        "PAIRED CHANGE VS SUPPORT BASELINE"
    )

    for pair in [
        unconditional_pair,
        hierarchical_pair,
    ]:

        print()

        print(
            pair[
                "comparison_policy"
            ]
        )

        print(
            f"mean dHarmful="
            f"{pair['mean_delta_harmful']:+.3f}"
        )

        print(
            f"harmful improved/unchanged/degraded="
            f"{pair['harmful_improved']}/"
            f"{pair['harmful_unchanged']}/"
            f"{pair['harmful_degraded']}"
        )

        print(
            f"mean dR="
            f"{pair['mean_delta_regret']:+.6f}"
        )

        print(
            f"median dR="
            f"{pair['median_delta_regret']:+.6f}"
        )

        print(
            f"range dR=["
            f"{pair['min_delta_regret']:+.6f},"
            f"{pair['max_delta_regret']:+.6f}"
            f"]"
        )

        print(
            f"regret improved/unchanged/degraded="
            f"{pair['regret_improved']}/"
            f"{pair['regret_unchanged']}/"
            f"{pair['regret_degraded']}"
        )

        print(
            f"mean dUnder="
            f"{pair['mean_delta_under']:+.3f}"
        )

        print(
            f"mean dBeneficial="
            f"{pair['mean_delta_beneficial']:+.3f}"
        )

        print(
            f"mean dRetention="
            f"{pair['mean_delta_retention']:+.3%}"
        )

    print()

    print(
        "PREREGISTERED HIERARCHICAL RULE"
    )

    print(
        "An expansion is vetoed only when:"
    )

    print(
        f"state probability >= "
        f"{STATE_THRESHOLD:.2f}"
    )

    print(
        "AND"
    )

    print(
        f"support distance > "
        f"{SELECTIVE_SUPPORT_THRESHOLD:.2f}"
    )

    print()

    print(
        "The 2.00 selective-support boundary is frozen "
        "before observing seeds 44031-44050."
    )

    print(
        "=" * 210
    )

    print(
        f"Aggregate results saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Seed-level results saved to: "
        f"{SEED_OUTPUT_PATH}"
    )

    print(
        f"Event-level results saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()