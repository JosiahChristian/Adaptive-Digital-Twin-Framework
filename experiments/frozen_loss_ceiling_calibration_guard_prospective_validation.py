import csv
import statistics
from pathlib import Path

import numpy as np

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
)

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


AGGREGATE_OUTPUT_PATH = Path(
    "results/"
    "frozen_loss_ceiling_calibration_guard_prospective_validation.csv"
)

SEED_OUTPUT_PATH = Path(
    "results/"
    "frozen_loss_ceiling_calibration_guard_prospective_validation_seeds.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "frozen_loss_ceiling_calibration_guard_prospective_validation_events.csv"
)


PROSPECTIVE_SEEDS = list(
    range(
        44051,
        44071,
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

CONTEXT_SUPPORT_THRESHOLD = 2.50

PRIMARY_CEILING_THRESHOLD = 0.155

SENSITIVITY_CEILING_THRESHOLD = 0.135

SEVERE_UNDERESTIMATION_THRESHOLD = -0.050

K_NEIGHBORS = 5

FLOAT_TOLERANCE = 1e-12
RANDOM_STATE = 42


def three_way_split(
    rows,
):
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
    row,
    action,
):
    return float(
        row[
            f"loss_k{action}"
        ]
    )


def regret(
    row,
    action,
):
    return (
        selected_loss(
            row,
            action,
        )
        - float(
            row[
                "best_loss"
            ]
        )
    )


def feature_vector(
    row,
    predicted_risk,
    predicted_losses,
):
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
    row,
    predicted_risk,
    predicted_losses,
    action,
):
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
    predicted_losses,
    predicted_risks,
):
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
    rows,
    candidates,
):
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
                        ][
                            index
                        ],
                    )
                for risk_level in RISK_LEVELS
            }
        )

    return output


def true_minimum_levels(
    regret_row,
):
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
    regret_row,
    candidates,
    index,
):
    levels = true_minimum_levels(
        regret_row
    )

    return {
        int(
            candidates[
                risk_level
            ][
                index
            ]
        )
        for risk_level in levels
    }


def train_regret_models(
    rows,
    predicted_losses,
    predicted_risks,
):
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
                ][
                    index
                ],
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
    models,
    rows,
    predicted_losses,
    predicted_risks,
):
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
                            ][
                                index
                            ]
                        ),
                    )
                for risk_level in RISK_LEVELS
            }
        )

    return output


def predicted_safe_levels(
    predicted_regret_row,
):
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
    levels,
    candidates,
    index,
):
    return {
        int(
            candidates[
                risk_level
            ][
                index
            ]
        )
        for risk_level in levels
    }


def train_action_safety_models(
    rows,
    predicted_losses,
    predicted_risks,
    candidates,
):
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
    rows,
    predicted_losses,
    predicted_risks,
    candidates,
):
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
                if action
                in safe_actions
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
    model,
    x,
):
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
    models,
    rows,
    predicted_losses,
    predicted_risks,
):
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
    models,
    rows,
    predicted_losses,
    predicted_risks,
):
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


def build_context_support(
    rows,
    predicted_losses,
    predicted_risks,
):
    matrix = np.asarray(
        [
            feature_vector(
                row,
                predicted_risks[
                    index
                ],
                predicted_losses[
                    index
                ],
            )
            for index, row in enumerate(
                rows
            )
        ],
        dtype=float,
    )

    mean = np.mean(
        matrix,
        axis=0,
    )

    std = np.std(
        matrix,
        axis=0,
    )

    std = np.where(
        std
        <= FLOAT_TOLERANCE,
        1.0,
        std,
    )

    scaled = (
        matrix
        - mean
    ) / std

    return {
        "mean":
            mean,

        "std":
            std,

        "training_matrix":
            scaled,
    }


def mean_knn_distance(
    training_matrix,
    sample,
):
    distances = np.sqrt(
        np.sum(
            (
                training_matrix
                - sample
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


def context_support_distance(
    support_object,
    row,
    predicted_risk,
    predicted_losses,
):
    sample = np.asarray(
        feature_vector(
            row,
            predicted_risk,
            predicted_losses,
        ),
        dtype=float,
    )

    scaled = (
        sample
        - support_object[
            "mean"
        ]
    ) / support_object[
        "std"
    ]

    return mean_knn_distance(
        support_object[
            "training_matrix"
        ],
        scaled,
    )


def responsive_action(
    action_set,
):
    return min(
        action_set
    )


def support_expand_set(
    row,
    primary_set,
    predicted_risk,
    predicted_losses,
    safety_scores,
    downside_scores,
    support_object,
):
    expanded = set(
        primary_set
    )

    support_distance = context_support_distance(
        support_object,
        row,
        predicted_risk,
        predicted_losses,
    )

    newly_added = []

    for action in ACTIONS:
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
            and support_distance
            <= CONTEXT_SUPPORT_THRESHOLD
        ):
            expanded.add(
                action
            )

            newly_added.append(
                action
            )

    return (
        expanded,
        newly_added,
        support_distance,
    )


def apply_ceiling_guard(
    primary_set,
    support_set,
    newly_added,
    predicted_loss_ceiling,
    threshold,
):
    guarded = set(
        support_set
    )

    vetoed = []

    if (
        predicted_loss_ceiling
        >= threshold
    ):
        for action in newly_added:
            if action in guarded:
                guarded.remove(
                    action
                )

                vetoed.append(
                    action
                )

    if not guarded:
        guarded = set(
            primary_set
        )

    return (
        guarded,
        vetoed,
    )


def entropy_from_action_counts(
    actions,
):
    if not actions:
        return 0.0

    counts = {
        action:
            actions.count(
                action
            )
        for action in ACTIONS
    }

    total = len(
        actions
    )

    entropy = 0.0

    for count in counts.values():
        if count <= 0:
            continue

        probability = (
            count
            / total
        )

        entropy -= (
            probability
            * np.log2(
                probability
            )
        )

    return float(
        entropy
    )


def evaluate_policy(
    rows,
    selected_actions,
    true_best_actions,
    true_responsive_actions,
):
    regrets = [
        regret(
            row,
            action,
        )
        for row, action in zip(
            rows,
            selected_actions,
        )
    ]

    under = sum(
        int(
            action
            < true_best
        )
        for (
            action,
            true_best,
        ) in zip(
            selected_actions,
            true_best_actions,
        )
    )

    over = sum(
        int(
            action
            > true_best
        )
        for (
            action,
            true_best,
        ) in zip(
            selected_actions,
            true_best_actions,
        )
    )

    retained = sum(
        int(
            action
            == true_responsive
        )
        for (
            action,
            true_responsive,
        ) in zip(
            selected_actions,
            true_responsive_actions,
        )
    )

    return {
        "mean_regret":
            statistics.mean(
                regrets
            ),

        "under":
            under,

        "over":
            over,

        "entropy":
            entropy_from_action_counts(
                selected_actions
            ),

        "retention":
            (
                retained
                / len(
                    selected_actions
                )
            ),
    }


def evaluate_seed(
    generation_seed,
):
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

    support_object = build_context_support(
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

    baseline_actions = []

    primary_guard_actions = []

    sensitivity_guard_actions = []

    true_best_actions = []

    true_responsive_actions = []

    event_rows = []

    baseline_beneficial = 0
    baseline_harmful = 0

    primary_beneficial = 0
    primary_harmful = 0

    sensitivity_beneficial = 0
    sensitivity_harmful = 0

    primary_veto_count = 0
    sensitivity_veto_count = 0

    primary_harmful_vetoed = 0
    primary_beneficial_vetoed = 0

    sensitivity_harmful_vetoed = 0
    sensitivity_beneficial_vetoed = 0

    baseline_severe_underestimation = 0

    primary_severe_vetoed = 0
    sensitivity_severe_vetoed = 0

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
            newly_added,
            support_distance,
        ) = support_expand_set(
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
            support_object,
        )

        predicted_values = [
            float(
                test_losses[
                    index
                ][
                    action
                ]
            )
            for action in ACTIONS
        ]

        predicted_loss_ceiling = max(
            predicted_values
        )

        (
            primary_guard_set,
            primary_vetoed,
        ) = apply_ceiling_guard(
            primary_set,
            support_set,
            newly_added,
            predicted_loss_ceiling,
            PRIMARY_CEILING_THRESHOLD,
        )

        (
            sensitivity_guard_set,
            sensitivity_vetoed,
        ) = apply_ceiling_guard(
            primary_set,
            support_set,
            newly_added,
            predicted_loss_ceiling,
            SENSITIVITY_CEILING_THRESHOLD,
        )

        baseline_action = responsive_action(
            support_set
        )

        primary_guard_action = responsive_action(
            primary_guard_set
        )

        sensitivity_guard_action = responsive_action(
            sensitivity_guard_set
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

        baseline_regret = regret(
            row,
            baseline_action,
        )

        primary_regret = regret(
            row,
            primary_guard_action,
        )

        sensitivity_regret = regret(
            row,
            sensitivity_guard_action,
        )

        primary_action = responsive_action(
            primary_set
        )

        changed_by_support = (
            baseline_action
            != primary_action
        )

        baseline_outcome = "neutral"

        if changed_by_support:
            if (
                baseline_regret
                <= (
                    regret(
                        row,
                        primary_action,
                    )
                    + FLOAT_TOLERANCE
                )
            ):
                baseline_outcome = "beneficial"
                baseline_beneficial += 1

            else:
                baseline_outcome = "harmful"
                baseline_harmful += 1

        predicted_baseline_loss = float(
            test_losses[
                index
            ][
                baseline_action
            ]
        )

        realized_baseline_loss = selected_loss(
            row,
            baseline_action,
        )

        baseline_loss_error = (
            predicted_baseline_loss
            - realized_baseline_loss
        )

        severe_underestimation = int(
            changed_by_support
            and baseline_loss_error
            < SEVERE_UNDERESTIMATION_THRESHOLD
        )

        baseline_severe_underestimation += (
            severe_underestimation
        )

        primary_changed = (
            primary_guard_action
            != primary_action
        )

        sensitivity_changed = (
            sensitivity_guard_action
            != primary_action
        )

        if primary_changed:
            if (
                primary_regret
                <= (
                    regret(
                        row,
                        primary_action,
                    )
                    + FLOAT_TOLERANCE
                )
            ):
                primary_beneficial += 1
            else:
                primary_harmful += 1

        if sensitivity_changed:
            if (
                sensitivity_regret
                <= (
                    regret(
                        row,
                        primary_action,
                    )
                    + FLOAT_TOLERANCE
                )
            ):
                sensitivity_beneficial += 1
            else:
                sensitivity_harmful += 1

        primary_vetoed_event = int(
            bool(
                primary_vetoed
            )
            and changed_by_support
        )

        sensitivity_vetoed_event = int(
            bool(
                sensitivity_vetoed
            )
            and changed_by_support
        )

        primary_veto_count += (
            primary_vetoed_event
        )

        sensitivity_veto_count += (
            sensitivity_vetoed_event
        )

        if primary_vetoed_event:
            if baseline_outcome == "harmful":
                primary_harmful_vetoed += 1

            if baseline_outcome == "beneficial":
                primary_beneficial_vetoed += 1

            if severe_underestimation:
                primary_severe_vetoed += 1

        if sensitivity_vetoed_event:
            if baseline_outcome == "harmful":
                sensitivity_harmful_vetoed += 1

            if baseline_outcome == "beneficial":
                sensitivity_beneficial_vetoed += 1

            if severe_underestimation:
                sensitivity_severe_vetoed += 1

        baseline_actions.append(
            baseline_action
        )

        primary_guard_actions.append(
            primary_guard_action
        )

        sensitivity_guard_actions.append(
            sensitivity_guard_action
        )

        true_best_actions.append(
            true_best_action
        )

        true_responsive_actions.append(
            true_responsive_action
        )

        event_rows.append(
            {
                "generation_seed":
                    generation_seed,

                "test_index":
                    index,

                "predicted_loss_ceiling":
                    predicted_loss_ceiling,

                "context_support_distance":
                    support_distance,

                "primary_action":
                    primary_action,

                "support_baseline_action":
                    baseline_action,

                "primary_ceiling_guard_action":
                    primary_guard_action,

                "sensitivity_ceiling_guard_action":
                    sensitivity_guard_action,

                "support_changed_action":
                    int(
                        changed_by_support
                    ),

                "baseline_expansion_outcome":
                    baseline_outcome,

                "baseline_regret":
                    baseline_regret,

                "primary_guard_regret":
                    primary_regret,

                "sensitivity_guard_regret":
                    sensitivity_regret,

                "primary_ceiling_veto":
                    primary_vetoed_event,

                "sensitivity_ceiling_veto":
                    sensitivity_vetoed_event,

                "predicted_baseline_action_loss":
                    predicted_baseline_loss,

                "realized_baseline_action_loss":
                    realized_baseline_loss,

                "baseline_action_loss_error":
                    baseline_loss_error,

                "severe_underestimation":
                    severe_underestimation,

                "true_best_action":
                    true_best_action,

                "true_responsive_action":
                    true_responsive_action,
            }
        )

    baseline_metrics = evaluate_policy(
        test_rows,
        baseline_actions,
        true_best_actions,
        true_responsive_actions,
    )

    primary_metrics = evaluate_policy(
        test_rows,
        primary_guard_actions,
        true_best_actions,
        true_responsive_actions,
    )

    sensitivity_metrics = evaluate_policy(
        test_rows,
        sensitivity_guard_actions,
        true_best_actions,
        true_responsive_actions,
    )

    seed_rows = []

    policy_payloads = [
        (
            "support_baseline",
            baseline_metrics,
            baseline_beneficial,
            baseline_harmful,
            0,
            0,
            0,
            0,
        ),
        (
            "ceiling_guard_0.155",
            primary_metrics,
            primary_beneficial,
            primary_harmful,
            primary_veto_count,
            primary_harmful_vetoed,
            primary_beneficial_vetoed,
            primary_severe_vetoed,
        ),
        (
            "ceiling_guard_0.135_sensitivity",
            sensitivity_metrics,
            sensitivity_beneficial,
            sensitivity_harmful,
            sensitivity_veto_count,
            sensitivity_harmful_vetoed,
            sensitivity_beneficial_vetoed,
            sensitivity_severe_vetoed,
        ),
    ]

    for (
        policy_name,
        metrics,
        beneficial,
        harmful,
        veto_count,
        harmful_vetoed,
        beneficial_vetoed,
        severe_vetoed,
    ) in policy_payloads:
        seed_rows.append(
            {
                "generation_seed":
                    generation_seed,

                "policy":
                    policy_name,

                "test_contexts":
                    len(
                        test_rows
                    ),

                "mean_regret":
                    metrics[
                        "mean_regret"
                    ],

                "under":
                    metrics[
                        "under"
                    ],

                "over":
                    metrics[
                        "over"
                    ],

                "entropy":
                    metrics[
                        "entropy"
                    ],

                "retention":
                    metrics[
                        "retention"
                    ],

                "beneficial":
                    beneficial,

                "harmful":
                    harmful,

                "veto":
                    veto_count,

                "baseline_harmful_vetoed":
                    harmful_vetoed,

                "baseline_beneficial_vetoed":
                    beneficial_vetoed,

                "baseline_severe_underestimation":
                    baseline_severe_underestimation,

                "baseline_severe_vetoed":
                    severe_vetoed,
            }
        )

    return (
        seed_rows,
        event_rows,
    )


def aggregate_policy_rows(
    seed_rows,
):
    policies = [
        "support_baseline",
        "ceiling_guard_0.155",
        "ceiling_guard_0.135_sensitivity",
    ]

    output = []

    for policy in policies:
        rows = [
            row
            for row in seed_rows
            if row[
                "policy"
            ]
            == policy
        ]

        output.append(
            {
                "policy":
                    policy,

                "seeds":
                    len(
                        rows
                    ),

                "mean_regret":
                    statistics.mean(
                        float(
                            row[
                                "mean_regret"
                            ]
                        )
                        for row in rows
                    ),

                "mean_under":
                    statistics.mean(
                        float(
                            row[
                                "under"
                            ]
                        )
                        for row in rows
                    ),

                "mean_over":
                    statistics.mean(
                        float(
                            row[
                                "over"
                            ]
                        )
                        for row in rows
                    ),

                "mean_entropy":
                    statistics.mean(
                        float(
                            row[
                                "entropy"
                            ]
                        )
                        for row in rows
                    ),

                "mean_retention":
                    statistics.mean(
                        float(
                            row[
                                "retention"
                            ]
                        )
                        for row in rows
                    ),

                "mean_beneficial":
                    statistics.mean(
                        float(
                            row[
                                "beneficial"
                            ]
                        )
                        for row in rows
                    ),

                "mean_harmful":
                    statistics.mean(
                        float(
                            row[
                                "harmful"
                            ]
                        )
                        for row in rows
                    ),

                "mean_veto":
                    statistics.mean(
                        float(
                            row[
                                "veto"
                            ]
                        )
                        for row in rows
                    ),

                "total_baseline_harmful_vetoed":
                    sum(
                        int(
                            row[
                                "baseline_harmful_vetoed"
                            ]
                        )
                        for row in rows
                    ),

                "total_baseline_beneficial_vetoed":
                    sum(
                        int(
                            row[
                                "baseline_beneficial_vetoed"
                            ]
                        )
                        for row in rows
                    ),

                "total_baseline_severe":
                    sum(
                        int(
                            row[
                                "baseline_severe_underestimation"
                            ]
                        )
                        for row in rows
                    ),

                "total_baseline_severe_vetoed":
                    sum(
                        int(
                            row[
                                "baseline_severe_vetoed"
                            ]
                        )
                        for row in rows
                    ),
            }
        )

    return output


def paired_comparison(
    seed_rows,
    guarded_policy,
):
    baseline_lookup = {
        int(
            row[
                "generation_seed"
            ]
        ):
            row
        for row in seed_rows
        if row[
            "policy"
        ]
        == "support_baseline"
    }

    guard_lookup = {
        int(
            row[
                "generation_seed"
            ]
        ):
            row
        for row in seed_rows
        if row[
            "policy"
        ]
        == guarded_policy
    }

    seeds = sorted(
        set(
            baseline_lookup
        )
        & set(
            guard_lookup
        )
    )

    regret_deltas = []
    harmful_deltas = []
    under_deltas = []
    beneficial_deltas = []
    retention_deltas = []

    harmful_improved = 0
    harmful_unchanged = 0
    harmful_degraded = 0

    regret_improved = 0
    regret_unchanged = 0
    regret_degraded = 0

    for seed in seeds:
        baseline = baseline_lookup[
            seed
        ]

        guard = guard_lookup[
            seed
        ]

        d_regret = (
            float(
                guard[
                    "mean_regret"
                ]
            )
            - float(
                baseline[
                    "mean_regret"
                ]
            )
        )

        d_harmful = (
            float(
                guard[
                    "harmful"
                ]
            )
            - float(
                baseline[
                    "harmful"
                ]
            )
        )

        regret_deltas.append(
            d_regret
        )

        harmful_deltas.append(
            d_harmful
        )

        under_deltas.append(
            float(
                guard[
                    "under"
                ]
            )
            - float(
                baseline[
                    "under"
                ]
            )
        )

        beneficial_deltas.append(
            float(
                guard[
                    "beneficial"
                ]
            )
            - float(
                baseline[
                    "beneficial"
                ]
            )
        )

        retention_deltas.append(
            float(
                guard[
                    "retention"
                ]
            )
            - float(
                baseline[
                    "retention"
                ]
            )
        )

        if d_harmful < 0:
            harmful_improved += 1
        elif d_harmful > 0:
            harmful_degraded += 1
        else:
            harmful_unchanged += 1

        if d_regret < -FLOAT_TOLERANCE:
            regret_improved += 1
        elif d_regret > FLOAT_TOLERANCE:
            regret_degraded += 1
        else:
            regret_unchanged += 1

    return {
        "mean_d_regret":
            statistics.mean(
                regret_deltas
            ),

        "median_d_regret":
            statistics.median(
                regret_deltas
            ),

        "min_d_regret":
            min(
                regret_deltas
            ),

        "max_d_regret":
            max(
                regret_deltas
            ),

        "mean_d_harmful":
            statistics.mean(
                harmful_deltas
            ),

        "harmful_improved":
            harmful_improved,

        "harmful_unchanged":
            harmful_unchanged,

        "harmful_degraded":
            harmful_degraded,

        "regret_improved":
            regret_improved,

        "regret_unchanged":
            regret_unchanged,

        "regret_degraded":
            regret_degraded,

        "mean_d_under":
            statistics.mean(
                under_deltas
            ),

        "mean_d_beneficial":
            statistics.mean(
                beneficial_deltas
            ),

        "mean_d_retention":
            statistics.mean(
                retention_deltas
            ),
    }


def save_csv(
    path,
    rows,
):
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


def main():
    all_seed_rows = []
    all_event_rows = []

    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "FROZEN LOSS-CEILING CALIBRATION GUARD "
        "PROSPECTIVE VALIDATION"
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
        f"context support threshold="
        f"{CONTEXT_SUPPORT_THRESHOLD:.2f}"
    )

    print(
        f"PRIMARY ceiling threshold="
        f"{PRIMARY_CEILING_THRESHOLD:.3f}"
    )

    print(
        f"sensitivity ceiling threshold="
        f"{SENSITIVITY_CEILING_THRESHOLD:.3f}"
    )

    print(
        f"severe underestimation threshold="
        f"{SEVERE_UNDERESTIMATION_THRESHOLD:.3f}"
    )

    print()

    for generation_seed in PROSPECTIVE_SEEDS:
        print(
            f"running prospective seed "
            f"{generation_seed}..."
        )

        (
            seed_rows,
            event_rows,
        ) = evaluate_seed(
            generation_seed
        )

        all_seed_rows.extend(
            seed_rows
        )

        all_event_rows.extend(
            event_rows
        )

    aggregate_rows = aggregate_policy_rows(
        all_seed_rows
    )

    primary_comparison = paired_comparison(
        all_seed_rows,
        "ceiling_guard_0.155",
    )

    sensitivity_comparison = paired_comparison(
        all_seed_rows,
        "ceiling_guard_0.135_sensitivity",
    )

    save_csv(
        AGGREGATE_OUTPUT_PATH,
        aggregate_rows,
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

    for row in aggregate_rows:
        severe_recall = (
            row[
                "total_baseline_severe_vetoed"
            ]
            / row[
                "total_baseline_severe"
            ]
            if row[
                "total_baseline_severe"
            ]
            > 0
            else 0.0
        )

        print(
            f"{row['policy']:<34} "
            f"mean_R="
            f"{row['mean_regret']:.6f} "
            f"mean_under="
            f"{row['mean_under']:.2f} "
            f"mean_over="
            f"{row['mean_over']:.2f} "
            f"mean_H="
            f"{row['mean_entropy']:.3f} "
            f"retention="
            f"{row['mean_retention']:.3%} "
            f"beneficial="
            f"{row['mean_beneficial']:.2f} "
            f"harmful="
            f"{row['mean_harmful']:.2f} "
            f"veto="
            f"{row['mean_veto']:.2f} "
            f"harmful_vetoed="
            f"{row['total_baseline_harmful_vetoed']} "
            f"beneficial_vetoed="
            f"{row['total_baseline_beneficial_vetoed']} "
            f"severe_veto_recall="
            f"{severe_recall:.3%}"
        )

    print()

    print(
        "PRIMARY PREREGISTERED COMPARISON"
    )

    print(
        "ceiling_guard_0.155 "
        "- support_baseline"
    )

    print(
        f"mean dHarmful="
        f"{primary_comparison['mean_d_harmful']:+.3f}"
    )

    print(
        "harmful improved/unchanged/degraded="
        f"{primary_comparison['harmful_improved']}/"
        f"{primary_comparison['harmful_unchanged']}/"
        f"{primary_comparison['harmful_degraded']}"
    )

    print(
        f"mean dR="
        f"{primary_comparison['mean_d_regret']:+.6f}"
    )

    print(
        f"median dR="
        f"{primary_comparison['median_d_regret']:+.6f}"
    )

    print(
        f"range dR="
        f"["
        f"{primary_comparison['min_d_regret']:+.6f},"
        f"{primary_comparison['max_d_regret']:+.6f}"
        f"]"
    )

    print(
        "regret improved/unchanged/degraded="
        f"{primary_comparison['regret_improved']}/"
        f"{primary_comparison['regret_unchanged']}/"
        f"{primary_comparison['regret_degraded']}"
    )

    print(
        f"mean dUnder="
        f"{primary_comparison['mean_d_under']:+.3f}"
    )

    print(
        f"mean dBeneficial="
        f"{primary_comparison['mean_d_beneficial']:+.3f}"
    )

    print(
        f"mean dRetention="
        f"{primary_comparison['mean_d_retention']:+.3%}"
    )

    print()

    print(
        "SECONDARY SENSITIVITY COMPARISON"
    )

    print(
        "ceiling_guard_0.135_sensitivity "
        "- support_baseline"
    )

    print(
        f"mean dHarmful="
        f"{sensitivity_comparison['mean_d_harmful']:+.3f}"
    )

    print(
        "harmful improved/unchanged/degraded="
        f"{sensitivity_comparison['harmful_improved']}/"
        f"{sensitivity_comparison['harmful_unchanged']}/"
        f"{sensitivity_comparison['harmful_degraded']}"
    )

    print(
        f"mean dR="
        f"{sensitivity_comparison['mean_d_regret']:+.6f}"
    )

    print(
        f"median dR="
        f"{sensitivity_comparison['median_d_regret']:+.6f}"
    )

    print(
        f"range dR="
        f"["
        f"{sensitivity_comparison['min_d_regret']:+.6f},"
        f"{sensitivity_comparison['max_d_regret']:+.6f}"
        f"]"
    )

    print(
        "regret improved/unchanged/degraded="
        f"{sensitivity_comparison['regret_improved']}/"
        f"{sensitivity_comparison['regret_unchanged']}/"
        f"{sensitivity_comparison['regret_degraded']}"
    )

    print(
        f"mean dUnder="
        f"{sensitivity_comparison['mean_d_under']:+.3f}"
    )

    print(
        f"mean dBeneficial="
        f"{sensitivity_comparison['mean_d_beneficial']:+.3f}"
    )

    print(
        f"mean dRetention="
        f"{sensitivity_comparison['mean_d_retention']:+.3%}"
    )

    print()

    print(
        "PREREGISTERED PRIMARY RULE"
    )

    print(
        "A support-admitted responsive expansion is vetoed "
        "only when:"
    )

    print(
        f"predicted loss ceiling >= "
        f"{PRIMARY_CEILING_THRESHOLD:.3f}"
    )

    print()

    print(
        "The 0.155 ceiling boundary and prospective seed block "
        "44051-44070 are frozen before observing these outcomes."
    )

    print()

    print(
        "The 0.135 result is secondary sensitivity analysis only "
        "and must not replace the preregistered 0.155 primary result."
    )

    print(
        "=" * 210
    )

    print(
        f"Aggregate results saved to: "
        f"{AGGREGATE_OUTPUT_PATH}"
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