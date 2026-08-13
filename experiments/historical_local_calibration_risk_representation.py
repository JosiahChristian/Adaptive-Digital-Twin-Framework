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
    predicted_loss_table,
)


OUTPUT_PATH = Path(
    "results/"
    "historical_local_calibration_risk_representation.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "historical_local_calibration_risk_representation_events.csv"
)

FOLD_OUTPUT_PATH = Path(
    "results/"
    "historical_local_calibration_risk_representation_folds.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "historical_local_calibration_risk_representation_coefficients.csv"
)


ANALYSIS_SEEDS = list(
    range(
        44001,
        44071,
    )
)

TEST_FRACTION = 0.30
META_FRACTION = 0.30

ACTIONS = [
    1,
    2,
    3,
]

K_NEIGHBORS = 7

SEVERE_UNDERESTIMATION_THRESHOLD = -0.050
CLASS_THRESHOLD = 0.50

FLOAT_TOLERANCE = 1e-12
RANDOM_STATE = 42


MODEL_SPECS = {
    "predicted_loss_only": [
        "predicted_action_loss",
    ],

    "local_mean_error_only": [
        "local_mean_error",
    ],

    "local_underestimate_fraction_only": [
        "local_underestimate_fraction",
    ],

    "local_severe_fraction_only": [
        "local_severe_underestimate_fraction",
    ],

    "local_error_std_only": [
        "local_error_std",
    ],

    "local_calibration_compact": [
        "local_mean_error",
        "local_error_std",
        "local_underestimate_fraction",
        "local_severe_underestimate_fraction",
    ],

    "loss_plus_local_calibration": [
        "predicted_action_loss",
        "local_mean_error",
        "local_error_std",
        "local_underestimate_fraction",
        "local_severe_underestimate_fraction",
    ],
}


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


def calibration_error(
    predicted_loss,
    realized_loss,
):
    return (
        float(
            predicted_loss
        )
        - float(
            realized_loss
        )
    )


def action_context_representation(
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

    predicted_mean = statistics.mean(
        predicted_values
    )

    predicted_spread = (
        predicted_ceiling
        - predicted_floor
    )

    predicted_action_loss = float(
        predicted_losses[
            action
        ]
    )

    return (
        [
            float(
                row[
                    name
                ]
            )
            for name in FEATURE_NAMES
        ]
        + [
            predicted_action_loss,
            predicted_floor,
            predicted_mean,
            predicted_ceiling,
            predicted_spread,
            predicted_action_loss
            - predicted_floor,
            float(
                action
            ),
        ]
    )


def build_historical_calibration_bank(
    rows,
    predicted_losses,
):
    raw = []
    errors = []
    actions = []

    for index, row in enumerate(
        rows
    ):
        for action in ACTIONS:
            predicted_action_loss = float(
                predicted_losses[
                    index
                ][
                    action
                ]
            )

            realized_action_loss = selected_loss(
                row,
                action,
            )

            error = calibration_error(
                predicted_action_loss,
                realized_action_loss,
            )

            raw.append(
                action_context_representation(
                    row,
                    predicted_losses[
                        index
                    ],
                    action,
                )
            )

            errors.append(
                error
            )

            actions.append(
                action
            )

    raw_matrix = np.asarray(
        raw,
        dtype=float,
    )

    scaler = StandardScaler()

    scaled_matrix = scaler.fit_transform(
        raw_matrix
    )

    return {
        "scaler":
            scaler,

        "matrix":
            scaled_matrix,

        "errors":
            np.asarray(
                errors,
                dtype=float,
            ),

        "actions":
            np.asarray(
                actions,
                dtype=int,
            ),
    }


def local_calibration_features(
    bank,
    row,
    predicted_losses,
    action,
):
    raw_sample = np.asarray(
        [
            action_context_representation(
                row,
                predicted_losses,
                action,
            )
        ],
        dtype=float,
    )

    scaled_sample = bank[
        "scaler"
    ].transform(
        raw_sample
    )[0]

    action_mask = (
        bank[
            "actions"
        ]
        == action
    )

    action_matrix = bank[
        "matrix"
    ][
        action_mask
    ]

    action_errors = bank[
        "errors"
    ][
        action_mask
    ]

    distances = np.sqrt(
        np.sum(
            (
                action_matrix
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

    nearest = order[
        :k
    ]

    local_errors = action_errors[
        nearest
    ]

    local_distances = distances[
        nearest
    ]

    mean_error = float(
        np.mean(
            local_errors
        )
    )

    error_std = float(
        np.std(
            local_errors
        )
    )

    underestimate_fraction = float(
        np.mean(
            local_errors
            < 0.0
        )
    )

    severe_underestimate_fraction = float(
        np.mean(
            local_errors
            < SEVERE_UNDERESTIMATION_THRESHOLD
        )
    )

    mean_distance = float(
        np.mean(
            local_distances
        )
    )

    minimum_error = float(
        np.min(
            local_errors
        )
    )

    median_error = float(
        np.median(
            local_errors
        )
    )

    return {
        "local_mean_error":
            mean_error,

        "local_median_error":
            median_error,

        "local_error_std":
            error_std,

        "local_underestimate_fraction":
            underestimate_fraction,

        "local_severe_underestimate_fraction":
            severe_underestimate_fraction,

        "local_neighbor_distance":
            mean_distance,

        "local_min_error":
            minimum_error,
    }


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

    meta_losses = predicted_loss_table(
        loss_models,
        meta_train_rows,
    )

    test_losses = predicted_loss_table(
        loss_models,
        test_rows,
    )

    bank = build_historical_calibration_bank(
        meta_train_rows,
        meta_losses,
    )

    return {
        "test_rows":
            test_rows,

        "test_losses":
            test_losses,

        "bank":
            bank,
    }


def event_rows_for_seed(
    generation_seed,
):
    geometry = reconstruct_seed(
        generation_seed
    )

    rows = geometry[
        "test_rows"
    ]

    predicted_losses = geometry[
        "test_losses"
    ]

    bank = geometry[
        "bank"
    ]

    output = []

    for index, row in enumerate(
        rows
    ):
        for action in ACTIONS:
            predicted_action_loss = float(
                predicted_losses[
                    index
                ][
                    action
                ]
            )

            realized_action_loss = selected_loss(
                row,
                action,
            )

            error = calibration_error(
                predicted_action_loss,
                realized_action_loss,
            )

            local_features = local_calibration_features(
                bank,
                row,
                predicted_losses[
                    index
                ],
                action,
            )

            copy = {
                "generation_seed":
                    generation_seed,

                "test_index":
                    index,

                "action":
                    action,

                "predicted_action_loss":
                    predicted_action_loss,

                "realized_action_loss":
                    realized_action_loss,

                "calibration_error":
                    error,

                "severe_underestimation":
                    int(
                        error
                        < SEVERE_UNDERESTIMATION_THRESHOLD
                    ),
            }

            copy.update(
                local_features
            )

            output.append(
                copy
            )

    return output


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

    if pooled_variance <= FLOAT_TOLERANCE:
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


def build_labels(
    rows,
):
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


def finite_mean(
    values,
):
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

        fold_rows.append(
            {
                "model":
                    model_name,

                "held_out_seed":
                    held_out_seed,

                "test_rows":
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
                    (
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
                    ),

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

        "rows":
            len(
                y_true
            ),

        "severe_rows":
            int(
                np.sum(
                    y_true
                    == 1
                )
            ),

        "nonsevere_rows":
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
                [
                    float(
                        row[
                            "balanced_accuracy"
                        ]
                    )
                    for row in fold_rows
                ]
            ),

        "mean_fold_roc_auc":
            finite_mean(
                [
                    float(
                        row[
                            "roc_auc"
                        ]
                    )
                    for row in fold_rows
                ]
            ),
    }, fold_rows, coefficient_rows


def summarize_coefficients(
    rows,
):
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
    event_rows = []

    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "HISTORICAL LOCAL CALIBRATION-RISK REPRESENTATION"
    )

    print(
        "=" * 210
    )

    print(
        f"analysis seeds="
        f"{ANALYSIS_SEEDS[0]}-"
        f"{ANALYSIS_SEEDS[-1]}"
    )

    print(
        f"local neighbors="
        f"{K_NEIGHBORS}"
    )

    print(
        f"severe underestimation threshold="
        f"{SEVERE_UNDERESTIMATION_THRESHOLD:.3f}"
    )

    print()

    for generation_seed in ANALYSIS_SEEDS:
        print(
            f"reconstructing seed "
            f"{generation_seed}..."
        )

        event_rows.extend(
            event_rows_for_seed(
                generation_seed
            )
        )

    severe_rows = [
        row
        for row in event_rows
        if int(
            row[
                "severe_underestimation"
            ]
        )
        == 1
    ]

    nonsevere_rows = [
        row
        for row in event_rows
        if int(
            row[
                "severe_underestimation"
            ]
        )
        == 0
    ]

    diagnostic_fields = [
        "predicted_action_loss",
        "local_mean_error",
        "local_median_error",
        "local_error_std",
        "local_underestimate_fraction",
        "local_severe_underestimate_fraction",
        "local_neighbor_distance",
        "local_min_error",
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
            event_rows,
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
        event_rows,
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
        "EVENT POPULATION"
    )

    print(
        f"action-context rows="
        f"{len(event_rows)}"
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
        f"{len(severe_rows) / len(event_rows):.3%}"
    )

    print()

    print(
        "LOCAL CALIBRATION FEATURE SEPARATION"
    )

    for row in diagnostic_rows:
        print(
            f"{row['metric']:<38} "
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
        "LEAVE-ONE-SEED-OUT SEVERE-UNDERESTIMATION CLASSIFICATION"
    )

    for row in model_summaries:
        print(
            f"{row['model']:<34} "
            f"balanced_acc="
            f"{row['balanced_accuracy']:.3%} "
            f"severe_recall="
            f"{row['severe_recall']:.3%} "
            f"severe_precision="
            f"{row['severe_precision']:.3%} "
            f"specificity="
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
            key=lambda row:
                float(
                    row[
                        "mean_absolute_coefficient"
                    ]
                ),
            reverse=True,
        )

        for row in matching:
            print(
                f"  "
                f"{row['feature']:<36} "
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
        "BEST HISTORICAL CALIBRATION-RISK MODEL"
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
        f"specificity="
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
        "Experiment 099 builds local calibration-risk features from "
        "historical prediction errors only. The current test outcome "
        "is used solely as the retrospective target and never enters "
        "the local representation used to predict that target."
    )

    print(
        "This is representation analysis, not a new controller guard."
    )

    print(
        "=" * 210
    )

    print(
        f"Summary saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Action-context results saved to: "
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