import csv
import math
import statistics
from pathlib import Path

import numpy as np

from sklearn.linear_model import (
    LogisticRegression,
    Ridge,
)
from sklearn.metrics import (
    balanced_accuracy_score,
    mean_absolute_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from experiments.historical_local_calibration_risk_representation import (
    event_rows_for_seed,
)


SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "pre_action_impending_calibration_error_prediction.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "pre_action_impending_calibration_error_prediction_events.csv"
)

FOLD_OUTPUT_PATH = Path(
    "results/"
    "pre_action_impending_calibration_error_prediction_folds.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "pre_action_impending_calibration_error_prediction_coefficients.csv"
)


# All of these seeds have already been consumed by prior experiments.
# No new prospective block is touched in Experiment 110.
HISTORICAL_SEEDS = list(
    range(
        44001,
        44111,
    )
)


SEVERE_UNDERESTIMATION_THRESHOLD = -0.050

RANDOM_STATE = 42

CLASSIFICATION_THRESHOLD = 0.50

FLOAT_TOLERANCE = 1e-12


# Strictly pre-action historical/local representation fields.
PREACTION_FEATURES = [
    "predicted_action_loss",
    "local_mean_error",
    "local_median_error",
    "local_error_std",
    "local_underestimate_fraction",
    "local_severe_underestimate_fraction",
    "local_neighbor_distance",
    "local_min_error",
]


CLASSIFICATION_MODELS = {
    "predicted_loss_only": [
        "predicted_action_loss",
    ],

    "historical_mean_only": [
        "local_mean_error",
    ],

    "error_dispersion_only": [
        "local_error_std",
    ],

    "underestimate_fraction_only": [
        "local_underestimate_fraction",
    ],

    "five_feature_calibration_state": [
        "predicted_action_loss",
        "local_mean_error",
        "local_error_std",
        "local_underestimate_fraction",
        "local_severe_underestimate_fraction",
    ],

    "expanded_historical_state": PREACTION_FEATURES,
}


REGRESSION_MODELS = {
    "predicted_loss_only_regression": [
        "predicted_action_loss",
    ],

    "five_feature_calibration_regression": [
        "predicted_action_loss",
        "local_mean_error",
        "local_error_std",
        "local_underestimate_fraction",
        "local_severe_underestimate_fraction",
    ],

    "expanded_historical_regression": PREACTION_FEATURES,
}


def as_float(
    row,
    field,
    default=float("nan"),
):
    value = row.get(
        field,
        "",
    )

    if value in (
        "",
        None,
    ):
        return default

    try:
        return float(
            value
        )

    except (
        TypeError,
        ValueError,
    ):
        return default


def reconstruct_population():
    rows = []

    for seed in HISTORICAL_SEEDS:
        print(
            f"reconstructing historical seed "
            f"{seed}..."
        )

        seed_rows = event_rows_for_seed(
            seed
        )

        for row in seed_rows:
            copy = dict(
                row
            )

            copy[
                "generation_seed"
            ] = int(
                seed
            )

            calibration_error = float(
                row[
                    "calibration_error"
                ]
            )

            copy[
                "calibration_error"
            ] = calibration_error

            copy[
                "underestimate_target"
            ] = int(
                calibration_error
                < 0.0
            )

            copy[
                "severe_underestimate_target"
            ] = int(
                calibration_error
                <= SEVERE_UNDERESTIMATION_THRESHOLD
            )

            rows.append(
                copy
            )

    return rows


def finite_rows(
    rows,
    features,
):
    output = []

    for row in rows:
        valid = True

        for feature in features:
            if not math.isfinite(
                as_float(
                    row,
                    feature,
                )
            ):
                valid = False
                break

        if valid:
            output.append(
                row
            )

    return output


def build_matrix(
    rows,
    features,
):
    return np.asarray(
        [
            [
                float(
                    row[
                        feature
                    ]
                )
                for feature in features
            ]
            for row in rows
        ],
        dtype=float,
    )


def classification_labels(
    rows,
    target,
):
    return np.asarray(
        [
            int(
                row[
                    target
                ]
            )
            for row in rows
        ],
        dtype=int,
    )


def regression_labels(
    rows,
):
    return np.asarray(
        [
            float(
                row[
                    "calibration_error"
                ]
            )
            for row in rows
        ],
        dtype=float,
    )


def make_classifier():
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


def make_regressor():
    return Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "regressor",
                Ridge(
                    alpha=1.0,
                ),
            ),
        ]
    )


def specificity_score(
    y_true,
    predictions,
):
    negative_mask = (
        y_true
        == 0
    )

    if not np.any(
        negative_mask
    ):
        return float(
            "nan"
        )

    return float(
        np.mean(
            predictions[
                negative_mask
            ]
            == 0
        )
    )


def safe_auc(
    y_true,
    probabilities,
):
    if len(
        np.unique(
            y_true
        )
    ) < 2:
        return float(
            "nan"
        )

    return float(
        roc_auc_score(
            y_true,
            probabilities,
        )
    )


def confusion_counts(
    y_true,
    predictions,
):
    tp = int(
        np.sum(
            (
                y_true
                == 1
            )
            & (
                predictions
                == 1
            )
        )
    )

    fp = int(
        np.sum(
            (
                y_true
                == 0
            )
            & (
                predictions
                == 1
            )
        )
    )

    fn = int(
        np.sum(
            (
                y_true
                == 1
            )
            & (
                predictions
                == 0
            )
        )
    )

    tn = int(
        np.sum(
            (
                y_true
                == 0
            )
            & (
                predictions
                == 0
            )
        )
    )

    return (
        tp,
        fp,
        fn,
        tn,
    )


def classification_metrics(
    y_true,
    probabilities,
):
    predictions = (
        probabilities
        >= CLASSIFICATION_THRESHOLD
    ).astype(
        int
    )

    (
        tp,
        fp,
        fn,
        tn,
    ) = confusion_counts(
        y_true,
        predictions,
    )

    return {
        "balanced_accuracy":
            float(
                balanced_accuracy_score(
                    y_true,
                    predictions,
                )
            ),

        "positive_recall":
            float(
                recall_score(
                    y_true,
                    predictions,
                    pos_label=1,
                    zero_division=0,
                )
            ),

        "positive_precision":
            float(
                precision_score(
                    y_true,
                    predictions,
                    pos_label=1,
                    zero_division=0,
                )
            ),

        "negative_specificity":
            specificity_score(
                y_true,
                predictions,
            ),

        "roc_auc":
            safe_auc(
                y_true,
                probabilities,
            ),

        "tp":
            tp,

        "fp":
            fp,

        "fn":
            fn,

        "tn":
            tn,
    }


def safe_correlation(
    true_values,
    predicted_values,
):
    if (
        len(
            true_values
        )
        < 2
        or np.std(
            true_values
        )
        <= FLOAT_TOLERANCE
        or np.std(
            predicted_values
        )
        <= FLOAT_TOLERANCE
    ):
        return float(
            "nan"
        )

    return float(
        np.corrcoef(
            true_values,
            predicted_values,
        )[
            0,
            1
        ]
    )


def classification_loso(
    rows,
    target,
):
    fold_rows = []
    event_rows = []
    coefficient_rows = []

    for model_name, features in CLASSIFICATION_MODELS.items():

        usable_rows = finite_rows(
            rows,
            features,
        )

        for held_out_seed in HISTORICAL_SEEDS:
            training_rows = [
                row
                for row in usable_rows
                if int(
                    row[
                        "generation_seed"
                    ]
                )
                != held_out_seed
            ]

            test_rows = [
                row
                for row in usable_rows
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
                training_rows,
                features,
            )

            y_train = classification_labels(
                training_rows,
                target,
            )

            x_test = build_matrix(
                test_rows,
                features,
            )

            y_test = classification_labels(
                test_rows,
                target,
            )

            if len(
                np.unique(
                    y_train
                )
            ) < 2:
                continue

            model = make_classifier()

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

            metrics = classification_metrics(
                y_test,
                probabilities,
            )

            fold_rows.append(
                {
                    "analysis":
                        target,

                    "model":
                        model_name,

                    "features":
                        "|".join(
                            features
                        ),

                    "held_out_seed":
                        held_out_seed,

                    "test_rows":
                        len(
                            test_rows
                        ),

                    "test_positive":
                        int(
                            np.sum(
                                y_test
                                == 1
                            )
                        ),

                    "test_negative":
                        int(
                            np.sum(
                                y_test
                                == 0
                            )
                        ),

                    **metrics,
                }
            )

            classifier = model.named_steps[
                "classifier"
            ]

            for feature, coefficient in zip(
                features,
                classifier.coef_[
                    0
                ],
            ):
                coefficient_rows.append(
                    {
                        "analysis":
                            target,

                        "model":
                            model_name,

                        "held_out_seed":
                            held_out_seed,

                        "feature":
                            feature,

                        "coefficient":
                            float(
                                coefficient
                            ),
                    }
                )

            for (
                row,
                true_target,
                probability,
            ) in zip(
                test_rows,
                y_test,
                probabilities,
            ):
                event_rows.append(
                    {
                        "analysis":
                            target,

                        "model":
                            model_name,

                        "generation_seed":
                            held_out_seed,

                        "test_index":
                            int(
                                float(
                                    row[
                                        "test_index"
                                    ]
                                )
                            ),

                        "action":
                            int(
                                float(
                                    row[
                                        "action"
                                    ]
                                )
                            ),

                        "true_target":
                            int(
                                true_target
                            ),

                        "probability":
                            float(
                                probability
                            ),

                        "predicted_class":
                            int(
                                probability
                                >= CLASSIFICATION_THRESHOLD
                            ),

                        "calibration_error":
                            float(
                                row[
                                    "calibration_error"
                                ]
                            ),
                    }
                )

    return (
        fold_rows,
        event_rows,
        coefficient_rows,
    )


def regression_loso(
    rows,
):
    fold_rows = []
    event_rows = []
    coefficient_rows = []

    for model_name, features in REGRESSION_MODELS.items():

        usable_rows = finite_rows(
            rows,
            features,
        )

        for held_out_seed in HISTORICAL_SEEDS:
            training_rows = [
                row
                for row in usable_rows
                if int(
                    row[
                        "generation_seed"
                    ]
                )
                != held_out_seed
            ]

            test_rows = [
                row
                for row in usable_rows
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
                training_rows,
                features,
            )

            y_train = regression_labels(
                training_rows
            )

            x_test = build_matrix(
                test_rows,
                features,
            )

            y_test = regression_labels(
                test_rows
            )

            model = make_regressor()

            model.fit(
                x_train,
                y_train,
            )

            predictions = model.predict(
                x_test
            )

            correlation = safe_correlation(
                y_test,
                predictions,
            )

            fold_rows.append(
                {
                    "analysis":
                        "signed_calibration_error",

                    "model":
                        model_name,

                    "features":
                        "|".join(
                            features
                        ),

                    "held_out_seed":
                        held_out_seed,

                    "test_rows":
                        len(
                            test_rows
                        ),

                    "mae":
                        float(
                            mean_absolute_error(
                                y_test,
                                predictions,
                            )
                        ),

                    "r2":
                        float(
                            r2_score(
                                y_test,
                                predictions,
                            )
                        ),

                    "correlation":
                        correlation,
                }
            )

            regressor = model.named_steps[
                "regressor"
            ]

            for feature, coefficient in zip(
                features,
                regressor.coef_,
            ):
                coefficient_rows.append(
                    {
                        "analysis":
                            "signed_calibration_error",

                        "model":
                            model_name,

                        "held_out_seed":
                            held_out_seed,

                        "feature":
                            feature,

                        "coefficient":
                            float(
                                coefficient
                            ),
                    }
                )

            for (
                row,
                true_error,
                predicted_error,
            ) in zip(
                test_rows,
                y_test,
                predictions,
            ):
                event_rows.append(
                    {
                        "analysis":
                            "signed_calibration_error",

                        "model":
                            model_name,

                        "generation_seed":
                            held_out_seed,

                        "test_index":
                            int(
                                float(
                                    row[
                                        "test_index"
                                    ]
                                )
                            ),

                        "action":
                            int(
                                float(
                                    row[
                                        "action"
                                    ]
                                )
                            ),

                        "true_calibration_error":
                            float(
                                true_error
                            ),

                        "predicted_calibration_error":
                            float(
                                predicted_error
                            ),

                        "true_underestimate":
                            int(
                                true_error
                                < 0.0
                            ),

                        "true_severe_underestimate":
                            int(
                                true_error
                                <= SEVERE_UNDERESTIMATION_THRESHOLD
                            ),
                    }
                )

    return (
        fold_rows,
        event_rows,
        coefficient_rows,
    )


def aggregate_classification_predictions(
    event_rows,
    target,
    model_name,
):
    matching = [
        row
        for row in event_rows
        if (
            row[
                "analysis"
            ]
            == target
            and row[
                "model"
            ]
            == model_name
        )
    ]

    y_true = np.asarray(
        [
            int(
                row[
                    "true_target"
                ]
            )
            for row in matching
        ],
        dtype=int,
    )

    probabilities = np.asarray(
        [
            float(
                row[
                    "probability"
                ]
            )
            for row in matching
        ],
        dtype=float,
    )

    return classification_metrics(
        y_true,
        probabilities,
    )


def aggregate_regression_predictions(
    event_rows,
    model_name,
):
    matching = [
        row
        for row in event_rows
        if (
            row[
                "analysis"
            ]
            == "signed_calibration_error"
            and row[
                "model"
            ]
            == model_name
        )
    ]

    true_values = np.asarray(
        [
            float(
                row[
                    "true_calibration_error"
                ]
            )
            for row in matching
        ],
        dtype=float,
    )

    predicted_values = np.asarray(
        [
            float(
                row[
                    "predicted_calibration_error"
                ]
            )
            for row in matching
        ],
        dtype=float,
    )

    return {
        "mae":
            float(
                mean_absolute_error(
                    true_values,
                    predicted_values,
                )
            ),

        "r2":
            float(
                r2_score(
                    true_values,
                    predicted_values,
                )
            ),

        "correlation":
            safe_correlation(
                true_values,
                predicted_values,
            ),
    }


def finite_mean(
    values,
):
    values = [
        value
        for value in values
        if math.isfinite(
            value
        )
    ]

    if not values:
        return float(
            "nan"
        )

    return statistics.mean(
        values
    )


def summarize_classification(
    fold_rows,
    event_rows,
):
    output = []

    for target in [
        "underestimate_target",
        "severe_underestimate_target",
    ]:
        for model_name in CLASSIFICATION_MODELS:
            folds = [
                row
                for row in fold_rows
                if (
                    row[
                        "analysis"
                    ]
                    == target
                    and row[
                        "model"
                    ]
                    == model_name
                )
            ]

            aggregate = aggregate_classification_predictions(
                event_rows,
                target,
                model_name,
            )

            output.append(
                {
                    "record_type":
                        "classification_summary",

                    "analysis":
                        target,

                    "model":
                        model_name,

                    "features":
                        "|".join(
                            CLASSIFICATION_MODELS[
                                model_name
                            ]
                        ),

                    "pooled_balanced_accuracy":
                        aggregate[
                            "balanced_accuracy"
                        ],

                    "pooled_positive_recall":
                        aggregate[
                            "positive_recall"
                        ],

                    "pooled_positive_precision":
                        aggregate[
                            "positive_precision"
                        ],

                    "pooled_negative_specificity":
                        aggregate[
                            "negative_specificity"
                        ],

                    "pooled_auc":
                        aggregate[
                            "roc_auc"
                        ],

                    "mean_fold_balanced_accuracy":
                        finite_mean(
                            [
                                float(
                                    row[
                                        "balanced_accuracy"
                                    ]
                                )
                                for row in folds
                            ]
                        ),

                    "mean_fold_auc":
                        finite_mean(
                            [
                                float(
                                    row[
                                        "roc_auc"
                                    ]
                                )
                                for row in folds
                            ]
                        ),

                    "minimum_fold_auc":
                        min(
                            float(
                                row[
                                    "roc_auc"
                                ]
                            )
                            for row in folds
                            if math.isfinite(
                                float(
                                    row[
                                        "roc_auc"
                                    ]
                                )
                            )
                        ),
                }
            )

    return output


def summarize_regression(
    fold_rows,
    event_rows,
):
    output = []

    for model_name in REGRESSION_MODELS:
        folds = [
            row
            for row in fold_rows
            if (
                row[
                    "analysis"
                ]
                == "signed_calibration_error"
                and row[
                    "model"
                ]
                == model_name
            )
        ]

        aggregate = aggregate_regression_predictions(
            event_rows,
            model_name,
        )

        output.append(
            {
                "record_type":
                    "regression_summary",

                "analysis":
                    "signed_calibration_error",

                "model":
                    model_name,

                "features":
                    "|".join(
                        REGRESSION_MODELS[
                            model_name
                        ]
                    ),

                "pooled_mae":
                    aggregate[
                        "mae"
                    ],

                "pooled_r2":
                    aggregate[
                        "r2"
                    ],

                "pooled_correlation":
                    aggregate[
                        "correlation"
                    ],

                "mean_fold_mae":
                    finite_mean(
                        [
                            float(
                                row[
                                    "mae"
                                ]
                            )
                            for row in folds
                        ]
                    ),

                "mean_fold_r2":
                    finite_mean(
                        [
                            float(
                                row[
                                    "r2"
                                ]
                            )
                            for row in folds
                        ]
                    ),

                "mean_fold_correlation":
                    finite_mean(
                        [
                            float(
                                row[
                                    "correlation"
                                ]
                            )
                            for row in folds
                        ]
                    ),
            }
        )

    return output


def coefficient_stability(
    coefficient_rows,
):
    output = []

    keys = sorted(
        {
            (
                row[
                    "analysis"
                ],
                row[
                    "model"
                ],
                row[
                    "feature"
                ],
            )
            for row in coefficient_rows
        }
    )

    for (
        analysis,
        model_name,
        feature,
    ) in keys:

        values = [
            float(
                row[
                    "coefficient"
                ]
            )
            for row in coefficient_rows
            if (
                row[
                    "analysis"
                ]
                == analysis
                and row[
                    "model"
                ]
                == model_name
                and row[
                    "feature"
                ]
                == feature
            )
        ]

        positive_fraction = statistics.mean(
            int(
                value
                > 0
            )
            for value in values
        )

        negative_fraction = statistics.mean(
            int(
                value
                < 0
            )
            for value in values
        )

        output.append(
            {
                "analysis":
                    analysis,

                "model":
                    model_name,

                "feature":
                    feature,

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

                "sign_stability":
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
    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PRE-ACTION IMPENDING CALIBRATION-ERROR PREDICTION"
    )

    print(
        "=" * 210
    )

    print(
        f"historical seeds="
        f"{HISTORICAL_SEEDS[0]}-"
        f"{HISTORICAL_SEEDS[-1]}"
    )

    print(
        f"severe underestimation threshold="
        f"{SEVERE_UNDERESTIMATION_THRESHOLD:.3f}"
    )

    print(
        f"pre-action features="
        f"{PREACTION_FEATURES}"
    )

    print()

    print(
        "RECONSTRUCTING HISTORICAL ACTION-CONTEXT POPULATION"
    )

    rows = reconstruct_population()

    under_count = sum(
        int(
            row[
                "underestimate_target"
            ]
        )
        for row in rows
    )

    severe_count = sum(
        int(
            row[
                "severe_underestimate_target"
            ]
        )
        for row in rows
    )

    print()

    print(
        "TARGET POPULATION"
    )

    print(
        f"rows="
        f"{len(rows)}"
    )

    print(
        f"underestimation="
        f"{under_count} "
        f"("
        f"{under_count / len(rows):.3%}"
        f")"
    )

    print(
        f"severe_underestimation="
        f"{severe_count} "
        f"("
        f"{severe_count / len(rows):.3%}"
        f")"
    )

    print()

    print(
        "RUNNING LEAVE-ONE-SEED-OUT "
        "UNDER-ESTIMATION CLASSIFICATION"
    )

    (
        under_fold_rows,
        under_event_rows,
        under_coefficient_rows,
    ) = classification_loso(
        rows,
        "underestimate_target",
    )

    print()

    print(
        "RUNNING LEAVE-ONE-SEED-OUT "
        "SEVERE-UNDER-ESTIMATION CLASSIFICATION"
    )

    (
        severe_fold_rows,
        severe_event_rows,
        severe_coefficient_rows,
    ) = classification_loso(
        rows,
        "severe_underestimate_target",
    )

    print()

    print(
        "RUNNING LEAVE-ONE-SEED-OUT "
        "SIGNED CALIBRATION-ERROR REGRESSION"
    )

    (
        regression_fold_rows,
        regression_event_rows,
        regression_coefficient_rows,
    ) = regression_loso(
        rows
    )

    all_classification_fold_rows = (
        under_fold_rows
        + severe_fold_rows
    )

    all_classification_event_rows = (
        under_event_rows
        + severe_event_rows
    )

    classification_summary_rows = (
        summarize_classification(
            all_classification_fold_rows,
            all_classification_event_rows,
        )
    )

    regression_summary_rows = (
        summarize_regression(
            regression_fold_rows,
            regression_event_rows,
        )
    )

    all_coefficient_rows = (
        under_coefficient_rows
        + severe_coefficient_rows
        + regression_coefficient_rows
    )

    coefficient_summary_rows = (
        coefficient_stability(
            all_coefficient_rows
        )
    )

    print()

    print(
        "UNDER-ESTIMATION CLASSIFICATION SUMMARY"
    )

    under_summaries = [
        row
        for row in classification_summary_rows
        if row[
            "analysis"
        ]
        == "underestimate_target"
    ]

    under_summaries.sort(
        key=lambda row:
            float(
                row[
                    "pooled_auc"
                ]
            ),
        reverse=True,
    )

    for row in under_summaries:
        print(
            f"{row['model']:<36} "
            f"bal_acc="
            f"{row['pooled_balanced_accuracy']:.3%} "
            f"recall="
            f"{row['pooled_positive_recall']:.3%} "
            f"precision="
            f"{row['pooled_positive_precision']:.3%} "
            f"specificity="
            f"{row['pooled_negative_specificity']:.3%} "
            f"AUC="
            f"{row['pooled_auc']:.3f} "
            f"mean_fold_AUC="
            f"{row['mean_fold_auc']:.3f}"
        )

    print()

    print(
        "SEVERE-UNDER-ESTIMATION CLASSIFICATION SUMMARY"
    )

    severe_summaries = [
        row
        for row in classification_summary_rows
        if row[
            "analysis"
        ]
        == "severe_underestimate_target"
    ]

    severe_summaries.sort(
        key=lambda row:
            float(
                row[
                    "pooled_auc"
                ]
            ),
        reverse=True,
    )

    for row in severe_summaries:
        print(
            f"{row['model']:<36} "
            f"bal_acc="
            f"{row['pooled_balanced_accuracy']:.3%} "
            f"recall="
            f"{row['pooled_positive_recall']:.3%} "
            f"precision="
            f"{row['pooled_positive_precision']:.3%} "
            f"specificity="
            f"{row['pooled_negative_specificity']:.3%} "
            f"AUC="
            f"{row['pooled_auc']:.3f} "
            f"mean_fold_AUC="
            f"{row['mean_fold_auc']:.3f}"
        )

    print()

    print(
        "SIGNED CALIBRATION-ERROR REGRESSION SUMMARY"
    )

    regression_summary_rows.sort(
        key=lambda row:
            float(
                row[
                    "pooled_correlation"
                ]
            ),
        reverse=True,
    )

    for row in regression_summary_rows:
        print(
            f"{row['model']:<40} "
            f"MAE="
            f"{row['pooled_mae']:.6f} "
            f"R2="
            f"{row['pooled_r2']:+.3f} "
            f"corr="
            f"{row['pooled_correlation']:+.3f} "
            f"mean_fold_corr="
            f"{row['mean_fold_correlation']:+.3f}"
        )

    print()

    print(
        "COEFFICIENT STABILITY"
    )

    for analysis in [
        "underestimate_target",
        "severe_underestimate_target",
        "signed_calibration_error",
    ]:
        print()

        print(
            analysis
        )

        matching = [
            row
            for row in coefficient_summary_rows
            if row[
                "analysis"
            ]
            == analysis
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
                f"{row['model']:<36} "
                f"{row['feature']:<38} "
                f"coef="
                f"{row['mean_coefficient']:+.3f} "
                f"abs="
                f"{row['mean_absolute_coefficient']:.3f} "
                f"sign_stability="
                f"{row['sign_stability']:.3%}"
            )

    best_severe = severe_summaries[
        0
    ]

    best_regression = regression_summary_rows[
        0
    ]

    print()

    print(
        "BEST PRE-ACTION SEVERE-UNDER-ESTIMATION MODEL"
    )

    print(
        f"name="
        f"{best_severe['model']}"
    )

    print(
        f"pooled_AUC="
        f"{best_severe['pooled_auc']:.3f}"
    )

    print(
        f"mean_fold_AUC="
        f"{best_severe['mean_fold_auc']:.3f}"
    )

    print(
        f"balanced_accuracy="
        f"{best_severe['pooled_balanced_accuracy']:.3%}"
    )

    print(
        f"severe_recall="
        f"{best_severe['pooled_positive_recall']:.3%}"
    )

    print()

    print(
        "BEST SIGNED-ERROR REGRESSION MODEL"
    )

    print(
        f"name="
        f"{best_regression['model']}"
    )

    print(
        f"correlation="
        f"{best_regression['pooled_correlation']:+.3f}"
    )

    print(
        f"R2="
        f"{best_regression['pooled_r2']:+.3f}"
    )

    print(
        f"MAE="
        f"{best_regression['pooled_mae']:.6f}"
    )

    print()

    print(
        "TEMPORAL VALIDITY NOTE"
    )

    print(
        "All predictor features in Experiment 110 are "
        "constructed from historical or current prediction-time "
        "information available before the evaluated action outcome."
    )

    print(
        "The current calibration_error is used only as the "
        "retrospective target and never enters that event's "
        "predictor representation."
    )

    print(
        "Experiment 110 is representation analysis only. "
        "No controller threshold, intervention, or new prospective "
        "seed is introduced."
    )

    print(
        "=" * 210
    )

    summary_rows = (
        classification_summary_rows
        + regression_summary_rows
    )

    fold_rows = (
        all_classification_fold_rows
        + regression_fold_rows
    )

    event_rows = (
        all_classification_event_rows
        + regression_event_rows
    )

    save_csv(
        SUMMARY_OUTPUT_PATH,
        summary_rows,
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
        coefficient_summary_rows,
    )

    print(
        f"Summary saved to: "
        f"{SUMMARY_OUTPUT_PATH}"
    )

    print(
        f"Out-of-fold event predictions saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )

    print(
        f"Seed-fold results saved to: "
        f"{FOLD_OUTPUT_PATH}"
    )

    print(
        f"Coefficient stability saved to: "
        f"{COEFFICIENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()