import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    balanced_accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
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
)


EVENT_INPUT_PATH = Path(
    "results/"
    "cross_seed_harmful_expansion_feature_decomposition_events.csv"
)

OUTPUT_PATH = Path(
    "results/"
    "pre_action_consequence_underestimation_risk_analysis.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "pre_action_consequence_underestimation_risk_analysis_events.csv"
)

FOLD_OUTPUT_PATH = Path(
    "results/"
    "pre_action_consequence_underestimation_risk_analysis_folds.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "pre_action_consequence_underestimation_risk_analysis_coefficients.csv"
)


ANALYSIS_SEEDS = [
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

ACTIONS = [
    1,
    2,
    3,
]

UNDER_ESTIMATION_THRESHOLD = -0.05
CLASS_THRESHOLD = 0.50

FLOAT_TOLERANCE = 1e-12
RANDOM_STATE = 42


MODEL_SPECS = {
    "loss_floor_only": [
        "predicted_loss_floor",
    ],

    "loss_ceiling_only": [
        "predicted_loss_ceiling",
    ],

    "loss_spread_only": [
        "predicted_loss_spread",
    ],

    "predicted_action_loss_only": [
        "predicted_action_loss",
    ],

    "loss_surface_compact": [
        "predicted_loss_floor",
        "predicted_loss_ceiling",
        "predicted_loss_spread",
    ],

    "risk_stack": [
        "predicted_risk",
        "safety_score",
        "downside_score",
    ],

    "transient_state": [
        "current_mismatch_indicator",
        "anchor_age",
        "trigger_score",
    ],

    "loss_plus_risk": [
        "predicted_loss_ceiling",
        "predicted_loss_spread",
        "predicted_risk",
        "safety_score",
        "downside_score",
    ],

    "loss_plus_state": [
        "predicted_loss_ceiling",
        "predicted_loss_spread",
        "current_mismatch_indicator",
        "anchor_age",
        "trigger_score",
    ],

    "compact_all_preaction": [
        "predicted_loss_ceiling",
        "predicted_loss_spread",
        "predicted_risk",
        "safety_score",
        "downside_score",
        "current_mismatch_indicator",
        "anchor_age",
        "trigger_score",
    ],
}


def three_way_split(rows):
    test_start = int(
        len(rows) * (1.0 - TEST_FRACTION)
    )

    development_rows = rows[:test_start]
    test_rows = rows[test_start:]

    meta_start = int(
        len(development_rows) * (1.0 - META_FRACTION)
    )

    base_train_rows = development_rows[:meta_start]
    meta_train_rows = development_rows[meta_start:]

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


def read_expansion_events():
    with EVENT_INPUT_PATH.open(
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
        if row.get(
            "outcome",
            "",
        )
        in (
            "beneficial",
            "harmful",
        )
    ]


def event_seed(row):
    for field in [
        "generation_seed",
        "seed",
    ]:
        if (
            field in row
            and row[field]
            not in (
                "",
                None,
            )
        ):
            return int(
                float(
                    row[field]
                )
            )

    raise KeyError(
        "Could not locate generation seed."
    )


def event_test_index(row):
    for field in [
        "test_index",
        "context_index",
        "index",
    ]:
        if (
            field in row
            and row[field]
            not in (
                "",
                None,
            )
        ):
            return int(
                float(
                    row[field]
                )
            )

    raise KeyError(
        "Could not locate test index."
    )


def expansion_action_from_event(row):
    for field in [
        "expanded_action",
        "support_action",
        "baseline_action",
        "selected_action",
    ]:
        if (
            field in row
            and row[field]
            not in (
                "",
                None,
            )
        ):
            return int(
                float(
                    row[field]
                )
            )

    raise KeyError(
        "Could not locate expanded action."
    )


def train_action_safety_models(
    rows,
    predicted_losses,
):
    from sklearn.ensemble import RandomForestClassifier

    models = {}

    for action in ACTIONS:
        x = []
        y = []

        for index, row in enumerate(
            rows
        ):
            losses = predicted_losses[
                index
            ]

            predicted_values = [
                float(
                    losses[
                        candidate
                    ]
                )
                for candidate in ACTIONS
            ]

            predicted_floor = min(
                predicted_values
            )

            predicted_ceiling = max(
                predicted_values
            )

            predicted_spread = (
                predicted_ceiling
                - predicted_floor
            )

            features = (
                [
                    float(
                        row[name]
                    )
                    for name in FEATURE_NAMES
                ]
                + [
                    float(
                        losses[action]
                    ),
                    predicted_floor,
                    predicted_ceiling,
                    predicted_spread,
                    float(
                        action
                    ),
                ]
            )

            x.append(
                features
            )

            realized_regret = (
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

            y.append(
                int(
                    realized_regret
                    <= 0.0005
                )
            )

        model = RandomForestClassifier(
            n_estimators=500,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=(
                RANDOM_STATE
                + 1000
                + action
            ),
        )

        model.fit(
            x,
            y,
        )

        models[action] = model

    return models


def train_action_downside_models(
    rows,
    predicted_losses,
):
    from sklearn.ensemble import RandomForestRegressor

    models = {}

    for action in ACTIONS:
        x = []
        y = []

        for index, row in enumerate(
            rows
        ):
            losses = predicted_losses[
                index
            ]

            predicted_values = [
                float(
                    losses[
                        candidate
                    ]
                )
                for candidate in ACTIONS
            ]

            predicted_floor = min(
                predicted_values
            )

            predicted_ceiling = max(
                predicted_values
            )

            predicted_spread = (
                predicted_ceiling
                - predicted_floor
            )

            features = (
                [
                    float(
                        row[name]
                    )
                    for name in FEATURE_NAMES
                ]
                + [
                    float(
                        losses[action]
                    ),
                    predicted_floor,
                    predicted_ceiling,
                    predicted_spread,
                    float(
                        action
                    ),
                ]
            )

            x.append(
                features
            )

            realized_regret = max(
                0.0,
                selected_loss(
                    row,
                    action,
                )
                - float(
                    row[
                        "best_loss"
                    ]
                ),
            )

            y.append(
                realized_regret
            )

        model = RandomForestRegressor(
            n_estimators=500,
            min_samples_leaf=2,
            random_state=(
                RANDOM_STATE
                + 2000
                + action
            ),
        )

        model.fit(
            x,
            y,
        )

        models[action] = model

    return models


def action_model_features(
    row,
    predicted_losses,
    action,
):
    predicted_values = [
        float(
            predicted_losses[
                candidate
            ]
        )
        for candidate in ACTIONS
    ]

    predicted_floor = min(
        predicted_values
    )

    predicted_ceiling = max(
        predicted_values
    )

    predicted_spread = (
        predicted_ceiling
        - predicted_floor
    )

    return (
        [
            float(
                row[name]
            )
            for name in FEATURE_NAMES
        ]
        + [
            float(
                predicted_losses[
                    action
                ]
            ),
            predicted_floor,
            predicted_ceiling,
            predicted_spread,
            float(
                action
            ),
        ]
    )


def positive_probability(
    model,
    x,
):
    probabilities = model.predict_proba(
        [x]
    )[0]

    classes = list(
        model.classes_
    )

    if 1 not in classes:
        return 0.0

    return float(
        probabilities[
            classes.index(
                1
            )
        ]
    )


def reconstruct_seed(
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

    test_losses = predicted_loss_table(
        loss_models,
        test_rows,
    )

    test_risks = predict_two_stage_risk(
        occurrence_model,
        magnitude_model,
        test_rows,
    )

    safety_models = train_action_safety_models(
        meta_train_rows,
        meta_losses,
    )

    downside_models = train_action_downside_models(
        meta_train_rows,
        meta_losses,
    )

    return {
        "test_rows":
            test_rows,

        "test_losses":
            test_losses,

        "test_risks":
            test_risks,

        "safety_models":
            safety_models,

        "downside_models":
            downside_models,
    }


def standardized_difference(
    nonsevere_values,
    severe_values,
):
    if (
        len(
            nonsevere_values
        )
        < 2
        or len(
            severe_values
        )
        < 2
    ):
        return 0.0

    nonsevere_variance = statistics.variance(
        nonsevere_values
    )

    severe_variance = statistics.variance(
        severe_values
    )

    pooled_variance = (
        (
            (
                len(
                    nonsevere_values
                )
                - 1
            )
            * nonsevere_variance
        )
        +
        (
            (
                len(
                    severe_values
                )
                - 1
            )
            * severe_variance
        )
    ) / (
        len(
            nonsevere_values
        )
        + len(
            severe_values
        )
        - 2
    )

    if (
        pooled_variance
        <= FLOAT_TOLERANCE
    ):
        return 0.0

    return (
        statistics.mean(
            severe_values
        )
        - statistics.mean(
            nonsevere_values
        )
    ) / (
        pooled_variance
        ** 0.5
    )


def make_model():
    return Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "classifier",
                LogisticRegression(
                    class_weight="balanced",
                    l1_ratio=0,
                    C=1.0,
                    solver="liblinear",
                    random_state=RANDOM_STATE,
                    max_iter=5000,
                ),
            ),
        ]
    )


def build_matrix(
    rows,
    feature_names,
):
    return np.asarray(
        [
            [
                float(
                    row[
                        feature
                    ]
                )
                for feature in feature_names
            ]
            for row in rows
        ],
        dtype=float,
    )


def build_labels(rows):
    return np.asarray(
        [
            int(
                row[
                    "severe_underestimation"
                ]
            )
            for row in rows
        ],
        dtype=int,
    )


def safe_auc(
    y_true,
    probabilities,
):
    if (
        len(
            np.unique(
                y_true
            )
        )
        < 2
    ):
        return float(
            "nan"
        )

    return float(
        roc_auc_score(
            y_true,
            probabilities,
        )
    )


def specificity_score(
    y_true,
    predictions,
):
    mask = (
        y_true
        == 0
    )

    if not np.any(
        mask
    ):
        return float(
            "nan"
        )

    return float(
        np.mean(
            predictions[
                mask
            ]
            == 0
        )
    )


def finite_mean(values):
    valid = [
        value
        for value in values
        if math.isfinite(
            value
        )
    ]

    if not valid:
        return float(
            "nan"
        )

    return statistics.mean(
        valid
    )


def evaluate_model(
    rows,
    model_name,
    feature_names,
):
    seeds = sorted(
        {
            int(
                row[
                    "generation_seed"
                ]
            )
            for row in rows
        }
    )

    fold_rows = []
    coefficient_rows = []

    pooled_true = []
    pooled_predictions = []
    pooled_probabilities = []

    for held_out_seed in seeds:
        train_rows = [
            row
            for row in rows
            if int(
                row[
                    "generation_seed"
                ]
            )
            != held_out_seed
        ]

        test_rows = [
            row
            for row in rows
            if int(
                row[
                    "generation_seed"
                ]
            )
            == held_out_seed
        ]

        if not test_rows:
            continue

        x_train = build_matrix(
            train_rows,
            feature_names,
        )

        y_train = build_labels(
            train_rows
        )

        if (
            len(
                np.unique(
                    y_train
                )
            )
            < 2
        ):
            continue

        x_test = build_matrix(
            test_rows,
            feature_names,
        )

        y_test = build_labels(
            test_rows
        )

        model = make_model()

        model.fit(
            x_train,
            y_train,
        )

        probabilities = model.predict_proba(
            x_test
        )[
            :,
            1
        ]

        predictions = (
            probabilities
            >= CLASS_THRESHOLD
        ).astype(
            int
        )

        balanced_accuracy = (
            float(
                balanced_accuracy_score(
                    y_test,
                    predictions,
                )
            )
            if len(
                np.unique(
                    y_test
                )
            )
            == 2
            else float(
                "nan"
            )
        )

        fold_rows.append(
            {
                "model":
                    model_name,

                "held_out_seed":
                    held_out_seed,

                "test_events":
                    len(
                        test_rows
                    ),

                "test_severe":
                    int(
                        np.sum(
                            y_test
                            == 1
                        )
                    ),

                "test_nonsevere":
                    int(
                        np.sum(
                            y_test
                            == 0
                        )
                    ),

                "balanced_accuracy":
                    balanced_accuracy,

                "severe_recall":
                    float(
                        recall_score(
                            y_test,
                            predictions,
                            pos_label=1,
                            zero_division=0,
                        )
                    ),

                "severe_precision":
                    float(
                        precision_score(
                            y_test,
                            predictions,
                            pos_label=1,
                            zero_division=0,
                        )
                    ),

                "nonsevere_specificity":
                    specificity_score(
                        y_test,
                        predictions,
                    ),

                "roc_auc":
                    safe_auc(
                        y_test,
                        probabilities,
                    ),
            }
        )

        classifier = model.named_steps[
            "classifier"
        ]

        for feature, coefficient in zip(
            feature_names,
            classifier.coef_[
                0
            ],
        ):
            coefficient_rows.append(
                {
                    "model":
                        model_name,

                    "held_out_seed":
                        held_out_seed,

                    "feature":
                        feature,

                    "standardized_coefficient":
                        float(
                            coefficient
                        ),
                }
            )

        pooled_true.extend(
            y_test.tolist()
        )

        pooled_predictions.extend(
            predictions.tolist()
        )

        pooled_probabilities.extend(
            probabilities.tolist()
        )

    y_true = np.asarray(
        pooled_true,
        dtype=int,
    )

    y_pred = np.asarray(
        pooled_predictions,
        dtype=int,
    )

    probabilities = np.asarray(
        pooled_probabilities,
        dtype=float,
    )

    fold_balanced = [
        float(
            row[
                "balanced_accuracy"
            ]
        )
        for row in fold_rows
    ]

    fold_auc = [
        float(
            row[
                "roc_auc"
            ]
        )
        for row in fold_rows
    ]

    return {
        "model":
            model_name,

        "features":
            "|".join(
                feature_names
            ),

        "feature_count":
            len(
                feature_names
            ),

        "events":
            len(
                y_true
            ),

        "severe_events":
            int(
                np.sum(
                    y_true
                    == 1
                )
            ),

        "nonsevere_events":
            int(
                np.sum(
                    y_true
                    == 0
                )
            ),

        "balanced_accuracy":
            float(
                balanced_accuracy_score(
                    y_true,
                    y_pred,
                )
            ),

        "severe_recall":
            float(
                recall_score(
                    y_true,
                    y_pred,
                    pos_label=1,
                    zero_division=0,
                )
            ),

        "severe_precision":
            float(
                precision_score(
                    y_true,
                    y_pred,
                    pos_label=1,
                    zero_division=0,
                )
            ),

        "nonsevere_specificity":
            specificity_score(
                y_true,
                y_pred,
            ),

        "roc_auc":
            safe_auc(
                y_true,
                probabilities,
            ),

        "mean_fold_balanced_accuracy":
            finite_mean(
                fold_balanced
            ),

        "mean_fold_roc_auc":
            finite_mean(
                fold_auc
            ),
    }, fold_rows, coefficient_rows


def summarize_coefficients(rows):
    grouped = defaultdict(
        list
    )

    for row in rows:
        grouped[
            (
                row[
                    "model"
                ],
                row[
                    "feature"
                ],
            )
        ].append(
            float(
                row[
                    "standardized_coefficient"
                ]
            )
        )

    output = []

    for (
        model_name,
        feature,
    ), values in grouped.items():
        positive_fraction = statistics.mean(
            [
                float(
                    value > 0
                )
                for value in values
            ]
        )

        negative_fraction = statistics.mean(
            [
                float(
                    value < 0
                )
                for value in values
            ]
        )

        output.append(
            {
                "model":
                    model_name,

                "feature":
                    feature,

                "folds":
                    len(
                        values
                    ),

                "mean_coefficient":
                    statistics.mean(
                        values
                    ),

                "mean_absolute_coefficient":
                    statistics.mean(
                        abs(
                            value
                        )
                        for value in values
                    ),

                "positive_fraction":
                    positive_fraction,

                "negative_fraction":
                    negative_fraction,

                "dominant_sign_fraction":
                    max(
                        positive_fraction,
                        negative_fraction,
                    ),
            }
        )

    return output


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
    source_events = read_expansion_events()

    source_events = [
        row
        for row in source_events
        if event_seed(
            row
        )
        in ANALYSIS_SEEDS
    ]

    reconstructed = {}

    enriched_events = []

    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PRE-ACTION CONSEQUENCE-UNDERESTIMATION "
        "RISK ANALYSIS"
    )

    print(
        "=" * 210
    )

    print(
        f"input="
        f"{EVENT_INPUT_PATH}"
    )

    print(
        f"analysis seeds="
        f"{ANALYSIS_SEEDS}"
    )

    print(
        f"severe underestimation threshold="
        f"{UNDER_ESTIMATION_THRESHOLD:.3f}"
    )

    print(
        f"source events="
        f"{len(source_events)}"
    )

    print()

    for generation_seed in ANALYSIS_SEEDS:
        print(
            f"reconstructing seed "
            f"{generation_seed}..."
        )

        reconstructed[
            generation_seed
        ] = reconstruct_seed(
            generation_seed
        )

    for event in source_events:
        generation_seed = event_seed(
            event
        )

        test_index = event_test_index(
            event
        )

        expanded_action = (
            expansion_action_from_event(
                event
            )
        )

        geometry = reconstructed[
            generation_seed
        ]

        row = geometry[
            "test_rows"
        ][
            test_index
        ]

        predicted_losses = geometry[
            "test_losses"
        ][
            test_index
        ]

        predicted_risk = float(
            geometry[
                "test_risks"
            ][
                test_index
            ]
        )

        predicted_values = [
            float(
                predicted_losses[
                    action
                ]
            )
            for action in ACTIONS
        ]

        predicted_floor = min(
            predicted_values
        )

        predicted_ceiling = max(
            predicted_values
        )

        predicted_mean = statistics.mean(
            predicted_values
        )

        predicted_spread = (
            predicted_ceiling
            - predicted_floor
        )

        predicted_action_loss = float(
            predicted_losses[
                expanded_action
            ]
        )

        realized_action_loss = selected_loss(
            row,
            expanded_action,
        )

        action_loss_error = (
            predicted_action_loss
            - realized_action_loss
        )

        action_features = action_model_features(
            row,
            predicted_losses,
            expanded_action,
        )

        safety_score = positive_probability(
            geometry[
                "safety_models"
            ][
                expanded_action
            ],
            action_features,
        )

        downside_score = max(
            0.0,
            float(
                geometry[
                    "downside_models"
                ][
                    expanded_action
                ].predict(
                    [
                        action_features
                    ]
                )[
                    0
                ]
            ),
        )

        copy = dict(
            event
        )

        copy[
            "generation_seed"
        ] = generation_seed

        copy[
            "test_index"
        ] = test_index

        copy[
            "expanded_action_reconstructed"
        ] = expanded_action

        copy[
            "predicted_loss_floor"
        ] = predicted_floor

        copy[
            "predicted_loss_mean"
        ] = predicted_mean

        copy[
            "predicted_loss_ceiling"
        ] = predicted_ceiling

        copy[
            "predicted_loss_spread"
        ] = predicted_spread

        copy[
            "predicted_action_loss"
        ] = predicted_action_loss

        copy[
            "predicted_risk"
        ] = predicted_risk

        copy[
            "safety_score"
        ] = safety_score

        copy[
            "downside_score"
        ] = downside_score

        copy[
            "current_mismatch_indicator"
        ] = float(
            row[
                "current_mismatch_indicator"
            ]
        )

        copy[
            "anchor_age"
        ] = float(
            row[
                "anchor_age"
            ]
        )

        copy[
            "trigger_score"
        ] = float(
            row[
                "trigger_score"
            ]
        )

        copy[
            "realized_action_loss"
        ] = realized_action_loss

        copy[
            "expanded_action_loss_error"
        ] = action_loss_error

        copy[
            "severe_underestimation"
        ] = int(
            action_loss_error
            < UNDER_ESTIMATION_THRESHOLD
        )

        enriched_events.append(
            copy
        )

    severe_rows = [
        row
        for row in enriched_events
        if int(
            row[
                "severe_underestimation"
            ]
        )
        == 1
    ]

    nonsevere_rows = [
        row
        for row in enriched_events
        if int(
            row[
                "severe_underestimation"
            ]
        )
        == 0
    ]

    diagnostic_fields = [
        "predicted_loss_floor",
        "predicted_loss_mean",
        "predicted_loss_ceiling",
        "predicted_loss_spread",
        "predicted_action_loss",
        "predicted_risk",
        "safety_score",
        "downside_score",
        "current_mismatch_indicator",
        "anchor_age",
        "trigger_score",
    ]

    diagnostic_rows = []

    for field in diagnostic_fields:
        nonsevere_values = [
            float(
                row[
                    field
                ]
            )
            for row in nonsevere_rows
        ]

        severe_values = [
            float(
                row[
                    field
                ]
            )
            for row in severe_rows
        ]

        diagnostic_rows.append(
            {
                "record_type":
                    "diagnostic",

                "metric":
                    field,

                "nonsevere_count":
                    len(
                        nonsevere_values
                    ),

                "severe_count":
                    len(
                        severe_values
                    ),

                "nonsevere_mean":
                    statistics.mean(
                        nonsevere_values
                    ),

                "severe_mean":
                    statistics.mean(
                        severe_values
                    ),

                "difference_severe_minus_nonsevere":
                    (
                        statistics.mean(
                            severe_values
                        )
                        - statistics.mean(
                            nonsevere_values
                        )
                    ),

                "standardized_difference":
                    standardized_difference(
                        nonsevere_values,
                        severe_values,
                    ),
            }
        )

    model_summaries = []
    fold_rows = []
    coefficient_rows = []

    for (
        model_name,
        feature_names,
    ) in MODEL_SPECS.items():
        (
            summary,
            folds,
            coefficients,
        ) = evaluate_model(
            enriched_events,
            model_name,
            feature_names,
        )

        model_summaries.append(
            summary
        )

        fold_rows.extend(
            folds
        )

        coefficient_rows.extend(
            coefficients
        )

    model_summaries.sort(
        key=lambda row: (
            float(
                row[
                    "balanced_accuracy"
                ]
            ),
            float(
                row[
                    "roc_auc"
                ]
            ),
        ),
        reverse=True,
    )

    coefficient_summary = summarize_coefficients(
        coefficient_rows
    )

    output_rows = []

    for row in model_summaries:
        copy = {
            "record_type":
                "model_summary"
        }

        copy.update(
            row
        )

        output_rows.append(
            copy
        )

    output_rows.extend(
        diagnostic_rows
    )

    save_csv(
        OUTPUT_PATH,
        output_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        enriched_events,
    )

    save_csv(
        FOLD_OUTPUT_PATH,
        fold_rows,
    )

    save_csv(
        COEFFICIENT_OUTPUT_PATH,
        coefficient_summary,
    )

    print()

    print(
        "TARGET POPULATION"
    )

    print(
        f"nonsevere="
        f"{len(nonsevere_rows)}"
    )

    print(
        f"severe_underestimation="
        f"{len(severe_rows)}"
    )

    print(
        f"severe fraction="
        f"{len(severe_rows) / len(enriched_events):.3%}"
    )

    print()

    print(
        "PRE-ACTION FEATURE SEPARATION"
    )

    for row in diagnostic_rows:
        print(
            f"{row['metric']:<32} "
            f"nonsevere="
            f"{row['nonsevere_mean']:.6f} "
            f"severe="
            f"{row['severe_mean']:.6f} "
            f"delta="
            f"{row['difference_severe_minus_nonsevere']:+.6f} "
            f"effect="
            f"{row['standardized_difference']:+.3f}"
        )

    print()

    print(
        "LEAVE-ONE-SEED-OUT UNDER-ESTIMATION CLASSIFICATION"
    )

    for row in model_summaries:
        print(
            f"{row['model']:<30} "
            f"balanced_acc="
            f"{row['balanced_accuracy']:.3%} "
            f"severe_recall="
            f"{row['severe_recall']:.3%} "
            f"severe_precision="
            f"{row['severe_precision']:.3%} "
            f"nonsevere_specificity="
            f"{row['nonsevere_specificity']:.3%} "
            f"AUC="
            f"{row['roc_auc']:.3f} "
            f"mean_fold_bal_acc="
            f"{row['mean_fold_balanced_accuracy']:.3%} "
            f"mean_fold_AUC="
            f"{row['mean_fold_roc_auc']:.3f}"
        )

    print()

    print(
        "COEFFICIENT STABILITY"
    )

    for model_name in MODEL_SPECS:
        print()

        print(
            model_name
        )

        matching = [
            row
            for row in coefficient_summary
            if row[
                "model"
            ]
            == model_name
        ]

        matching.sort(
            key=lambda row: (
                float(
                    row[
                        "dominant_sign_fraction"
                    ]
                ),
                float(
                    row[
                        "mean_absolute_coefficient"
                    ]
                ),
            ),
            reverse=True,
        )

        for row in matching:
            print(
                f"  "
                f"{row['feature']:<32} "
                f"mean_coef="
                f"{row['mean_coefficient']:+.3f} "
                f"abs_coef="
                f"{row['mean_absolute_coefficient']:.3f} "
                f"sign_stability="
                f"{row['dominant_sign_fraction']:.3%}"
            )

    print()

    best = model_summaries[
        0
    ]

    print(
        "BEST PRE-ACTION CALIBRATION-RISK MODEL"
    )

    print(
        f"name="
        f"{best['model']}"
    )

    print(
        f"balanced_accuracy="
        f"{best['balanced_accuracy']:.3%}"
    )

    print(
        f"severe_recall="
        f"{best['severe_recall']:.3%}"
    )

    print(
        f"nonsevere_specificity="
        f"{best['nonsevere_specificity']:.3%}"
    )

    print(
        f"roc_auc="
        f"{best['roc_auc']:.3f}"
    )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 095 predicts a post-outcome calibration-failure "
        "target using pre-action information only. "
        "The target itself is retrospective, but all candidate "
        "predictors are available before action execution. "
        "No controller threshold is defined here."
    )

    print(
        "=" * 210
    )

    print(
        f"Summary saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Enriched event results saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )

    print(
        f"Fold results saved to: "
        f"{FOLD_OUTPUT_PATH}"
    )

    print(
        f"Coefficient stability saved to: "
        f"{COEFFICIENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()