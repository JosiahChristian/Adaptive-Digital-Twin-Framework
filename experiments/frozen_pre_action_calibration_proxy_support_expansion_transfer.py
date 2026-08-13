import csv
import math
import statistics
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


SUPPORT_EVENT_PATH = Path(
    "results/"
    "cross_block_constituent_stability_analysis_events.csv"
)

PROXY_EVENT_PATH = Path(
    "results/"
    "pre_action_impending_calibration_error_prediction_events.csv"
)

SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "frozen_pre_action_calibration_proxy_support_expansion_transfer.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "frozen_pre_action_calibration_proxy_support_expansion_transfer_events.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "frozen_pre_action_calibration_proxy_support_expansion_transfer_coefficients.csv"
)


BLOCKS = [
    "block_071_090",
    "block_091_110",
]

SEVERE_PROXY_ANALYSIS = "severe_underestimate_target"
SEVERE_PROXY_MODEL = "expanded_historical_state"

SIGNED_PROXY_ANALYSIS = "signed_calibration_error"
SIGNED_PROXY_MODEL = "expanded_historical_regression"

CLASSIFICATION_THRESHOLD = 0.50

RANDOM_STATE = 42

FLOAT_TOLERANCE = 1e-12


MODEL_SPECS = {
    "error_std_only": [
        "local_error_std",
    ],

    "severe_proxy_only": [
        "severe_underestimation_probability",
    ],

    "signed_error_proxy_only": [
        "predicted_underestimation_magnitude",
    ],

    "error_std_plus_severe_proxy": [
        "local_error_std",
        "severe_underestimation_probability",
    ],

    "error_std_plus_signed_error_proxy": [
        "local_error_std",
        "predicted_underestimation_magnitude",
    ],

    "two_frozen_proxies": [
        "severe_underestimation_probability",
        "predicted_underestimation_magnitude",
    ],

    "error_std_plus_two_proxies": [
        "local_error_std",
        "severe_underestimation_probability",
        "predicted_underestimation_magnitude",
    ],
}


def read_csv(
    path,
):
    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        return list(
            csv.DictReader(
                file
            )
        )


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


def as_int(
    row,
    field,
    default=0,
):
    value = as_float(
        row,
        field,
    )

    if not math.isfinite(
        value
    ):
        return default

    return int(
        value
    )


def support_key(
    row,
):
    return (
        as_int(
            row,
            "generation_seed",
        ),
        as_int(
            row,
            "test_index",
        ),
        as_int(
            row,
            "support_baseline_action",
        ),
    )


def proxy_key(
    row,
):
    return (
        as_int(
            row,
            "generation_seed",
        ),
        as_int(
            row,
            "test_index",
        ),
        as_int(
            row,
            "action",
        ),
    )


def build_proxy_lookup(
    proxy_rows,
):
    severe_lookup = {}
    signed_lookup = {}

    for row in proxy_rows:
        analysis = row.get(
            "analysis",
            "",
        )

        model = row.get(
            "model",
            "",
        )

        key = proxy_key(
            row
        )

        if (
            analysis
            == SEVERE_PROXY_ANALYSIS
            and model
            == SEVERE_PROXY_MODEL
        ):
            probability = as_float(
                row,
                "probability",
            )

            if math.isfinite(
                probability
            ):
                severe_lookup[
                    key
                ] = probability

        if (
            analysis
            == SIGNED_PROXY_ANALYSIS
            and model
            == SIGNED_PROXY_MODEL
        ):
            prediction = as_float(
                row,
                "predicted_calibration_error",
            )

            if math.isfinite(
                prediction
            ):
                signed_lookup[
                    key
                ] = prediction

    return (
        severe_lookup,
        signed_lookup,
    )


def join_support_events():
    support_rows = read_csv(
        SUPPORT_EVENT_PATH
    )

    proxy_rows = read_csv(
        PROXY_EVENT_PATH
    )

    (
        severe_lookup,
        signed_lookup,
    ) = build_proxy_lookup(
        proxy_rows
    )

    output = []

    missing_severe = []
    missing_signed = []

    for row in support_rows:
        key = support_key(
            row
        )

        if key not in severe_lookup:
            missing_severe.append(
                key
            )
            continue

        if key not in signed_lookup:
            missing_signed.append(
                key
            )
            continue

        copy = dict(
            row
        )

        signed_error_prediction = signed_lookup[
            key
        ]

        copy[
            "severe_underestimation_probability"
        ] = severe_lookup[
            key
        ]

        copy[
            "predicted_signed_calibration_error"
        ] = signed_error_prediction

        # More negative predicted calibration error means greater
        # predicted underestimation. Negating it gives a natural
        # harmful-high orientation without fitting anything to the
        # support-expansion labels.
        copy[
            "predicted_underestimation_magnitude"
        ] = (
            -signed_error_prediction
        )

        copy[
            "harmful_target"
        ] = int(
            copy.get(
                "class",
                "",
            )
            == "harmful"
        )

        output.append(
            copy
        )

    if missing_severe:
        raise KeyError(
            "Missing severe-underestimation proxy rows for "
            f"{len(missing_severe)} support events. "
            f"First missing key={missing_severe[0]}"
        )

    if missing_signed:
        raise KeyError(
            "Missing signed-error proxy rows for "
            f"{len(missing_signed)} support events. "
            f"First missing key={missing_signed[0]}"
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


def build_labels(
    rows,
):
    return np.asarray(
        [
            int(
                row[
                    "harmful_target"
                ]
            )
            for row in rows
        ],
        dtype=int,
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


def safe_auc(
    y_true,
    scores,
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
            scores,
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


def evaluate_probabilities(
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

        "harmful_recall":
            float(
                recall_score(
                    y_true,
                    predictions,
                    pos_label=1,
                    zero_division=0,
                )
            ),

        "harmful_precision":
            float(
                precision_score(
                    y_true,
                    predictions,
                    pos_label=1,
                    zero_division=0,
                )
            ),

        "beneficial_specificity":
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


def raw_signal_geometry(
    rows,
):
    signals = {
        "local_error_std":
            "local_error_std",

        "severe_underestimation_probability":
            "severe_underestimation_probability",

        "predicted_underestimation_magnitude":
            "predicted_underestimation_magnitude",
    }

    output = []

    for block in BLOCKS:
        block_rows = [
            row
            for row in rows
            if row[
                "block"
            ]
            == block
        ]

        y_true = build_labels(
            block_rows
        )

        for signal_name, field in signals.items():
            scores = np.asarray(
                [
                    float(
                        row[
                            field
                        ]
                    )
                    for row in block_rows
                ],
                dtype=float,
            )

            beneficial_scores = [
                float(
                    row[
                        field
                    ]
                )
                for row in block_rows
                if int(
                    row[
                        "harmful_target"
                    ]
                )
                == 0
            ]

            harmful_scores = [
                float(
                    row[
                        field
                    ]
                )
                for row in block_rows
                if int(
                    row[
                        "harmful_target"
                    ]
                )
                == 1
            ]

            output.append(
                {
                    "block":
                        block,

                    "signal":
                        signal_name,

                    "beneficial_mean":
                        statistics.mean(
                            beneficial_scores
                        ),

                    "harmful_mean":
                        statistics.mean(
                            harmful_scores
                        ),

                    "difference_harmful_minus_beneficial":
                        (
                            statistics.mean(
                                harmful_scores
                            )
                            - statistics.mean(
                                beneficial_scores
                            )
                        ),

                    "rank_auc_harmful_high":
                        safe_auc(
                            y_true,
                            scores,
                        ),
                }
            )

    return output


def reciprocal_block_evaluation(
    rows,
):
    fold_rows = []
    prediction_rows = []
    coefficient_rows = []

    for model_name, features in MODEL_SPECS.items():

        for held_out_block in BLOCKS:
            training_rows = [
                row
                for row in rows
                if row[
                    "block"
                ]
                != held_out_block
            ]

            test_rows = [
                row
                for row in rows
                if row[
                    "block"
                ]
                == held_out_block
            ]

            x_train = build_matrix(
                training_rows,
                features,
            )

            y_train = build_labels(
                training_rows
            )

            x_test = build_matrix(
                test_rows,
                features,
            )

            y_test = build_labels(
                test_rows
            )

            if len(
                np.unique(
                    y_train
                )
            ) < 2:
                raise RuntimeError(
                    f"Training population for {held_out_block} "
                    "contains only one class."
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

            metrics = evaluate_probabilities(
                y_test,
                probabilities,
            )

            fold_rows.append(
                {
                    "model":
                        model_name,

                    "features":
                        "|".join(
                            features
                        ),

                    "held_out_block":
                        held_out_block,

                    "training_rows":
                        len(
                            training_rows
                        ),

                    "training_harmful":
                        int(
                            np.sum(
                                y_train
                                == 1
                            )
                        ),

                    "test_rows":
                        len(
                            test_rows
                        ),

                    "test_harmful":
                        int(
                            np.sum(
                                y_test
                                == 1
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
                        "model":
                            model_name,

                        "held_out_block":
                            held_out_block,

                        "feature":
                            feature,

                        "coefficient":
                            float(
                                coefficient
                            ),
                    }
                )

            predictions = (
                probabilities
                >= CLASSIFICATION_THRESHOLD
            ).astype(
                int
            )

            for (
                row,
                probability,
                prediction,
            ) in zip(
                test_rows,
                probabilities,
                predictions,
            ):
                prediction_rows.append(
                    {
                        "model":
                            model_name,

                        "held_out_block":
                            held_out_block,

                        "generation_seed":
                            as_int(
                                row,
                                "generation_seed",
                            ),

                        "test_index":
                            as_int(
                                row,
                                "test_index",
                            ),

                        "support_baseline_action":
                            as_int(
                                row,
                                "support_baseline_action",
                            ),

                        "true_class":
                            row[
                                "class"
                            ],

                        "harmful_target":
                            int(
                                row[
                                    "harmful_target"
                                ]
                            ),

                        "predicted_probability":
                            float(
                                probability
                            ),

                        "predicted_class":
                            int(
                                prediction
                            ),

                        "local_error_std":
                            float(
                                row[
                                    "local_error_std"
                                ]
                            ),

                        "severe_underestimation_probability":
                            float(
                                row[
                                    "severe_underestimation_probability"
                                ]
                            ),

                        "predicted_signed_calibration_error":
                            float(
                                row[
                                    "predicted_signed_calibration_error"
                                ]
                            ),

                        "predicted_underestimation_magnitude":
                            float(
                                row[
                                    "predicted_underestimation_magnitude"
                                ]
                            ),
                    }
                )

    return (
        fold_rows,
        prediction_rows,
        coefficient_rows,
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


def summarize_models(
    fold_rows,
):
    output = []

    for model_name in MODEL_SPECS:
        matching = [
            row
            for row in fold_rows
            if row[
                "model"
            ]
            == model_name
        ]

        aucs = [
            float(
                row[
                    "roc_auc"
                ]
            )
            for row in matching
        ]

        balanced = [
            float(
                row[
                    "balanced_accuracy"
                ]
            )
            for row in matching
        ]

        recalls = [
            float(
                row[
                    "harmful_recall"
                ]
            )
            for row in matching
        ]

        specificities = [
            float(
                row[
                    "beneficial_specificity"
                ]
            )
            for row in matching
        ]

        output.append(
            {
                "record_type":
                    "model_summary",

                "model":
                    model_name,

                "features":
                    "|".join(
                        MODEL_SPECS[
                            model_name
                        ]
                    ),

                "mean_auc":
                    finite_mean(
                        aucs
                    ),

                "min_auc":
                    min(
                        aucs
                    ),

                "max_auc":
                    max(
                        aucs
                    ),

                "mean_balanced_accuracy":
                    finite_mean(
                        balanced
                    ),

                "min_balanced_accuracy":
                    min(
                        balanced
                    ),

                "mean_harmful_recall":
                    finite_mean(
                        recalls
                    ),

                "min_harmful_recall":
                    min(
                        recalls
                    ),

                "mean_specificity":
                    finite_mean(
                        specificities
                    ),
            }
        )

    output.sort(
        key=lambda row: (
            float(
                row[
                    "mean_auc"
                ]
            ),
            float(
                row[
                    "min_auc"
                ]
            ),
        ),
        reverse=True,
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
        "FROZEN PRE-ACTION CALIBRATION-PROXY "
        "SUPPORT-EXPANSION TRANSFER"
    )

    print(
        "=" * 210
    )

    print(
        f"support events="
        f"{SUPPORT_EVENT_PATH}"
    )

    print(
        f"frozen proxy events="
        f"{PROXY_EVENT_PATH}"
    )

    print(
        f"severe proxy="
        f"{SEVERE_PROXY_MODEL}"
    )

    print(
        f"signed-error proxy="
        f"{SIGNED_PROXY_MODEL}"
    )

    print()

    rows = join_support_events()

    harmful = sum(
        int(
            row[
                "harmful_target"
            ]
        )
        for row in rows
    )

    beneficial = (
        len(
            rows
        )
        - harmful
    )

    print(
        "JOINED SUPPORT-EXPANSION POPULATION"
    )

    print(
        f"rows="
        f"{len(rows)}"
    )

    print(
        f"beneficial="
        f"{beneficial}"
    )

    print(
        f"harmful="
        f"{harmful}"
    )

    print()

    geometry_rows = raw_signal_geometry(
        rows
    )

    print(
        "FROZEN PROXY RAW SIGNAL GEOMETRY"
    )

    for block in BLOCKS:
        print()

        print(
            block
        )

        matching = [
            row
            for row in geometry_rows
            if row[
                "block"
            ]
            == block
        ]

        for row in matching:
            print(
                f"  "
                f"{row['signal']:<42} "
                f"beneficial="
                f"{row['beneficial_mean']:.6f} "
                f"harmful="
                f"{row['harmful_mean']:.6f} "
                f"delta="
                f"{row['difference_harmful_minus_beneficial']:+.6f} "
                f"rank_AUC="
                f"{row['rank_auc_harmful_high']:.3f}"
            )

    (
        fold_rows,
        prediction_rows,
        coefficient_rows,
    ) = reciprocal_block_evaluation(
        rows
    )

    summary_rows = summarize_models(
        fold_rows
    )

    coefficient_summary_rows = (
        coefficient_stability(
            coefficient_rows
        )
    )

    print()

    print(
        "RECIPROCAL BLOCK-HELD-OUT TRANSFER"
    )

    for model_name in MODEL_SPECS:
        print()

        print(
            model_name
        )

        matching = [
            row
            for row in fold_rows
            if row[
                "model"
            ]
            == model_name
        ]

        for row in matching:
            print(
                f"  held_out="
                f"{row['held_out_block']:<16} "
                f"train_harmful="
                f"{row['training_harmful']} "
                f"test_harmful="
                f"{row['test_harmful']} "
                f"balanced_acc="
                f"{row['balanced_accuracy']:.3%} "
                f"harmful_recall="
                f"{row['harmful_recall']:.3%} "
                f"precision="
                f"{row['harmful_precision']:.3%} "
                f"specificity="
                f"{row['beneficial_specificity']:.3%} "
                f"AUC="
                f"{row['roc_auc']:.3f} "
                f"TP="
                f"{row['tp']} "
                f"FP="
                f"{row['fp']} "
                f"FN="
                f"{row['fn']} "
                f"TN="
                f"{row['tn']}"
            )

    print()

    print(
        "MODEL TRANSFER SUMMARY"
    )

    for row in summary_rows:
        print(
            f"{row['model']:<38} "
            f"mean_AUC="
            f"{row['mean_auc']:.3f} "
            f"min_AUC="
            f"{row['min_auc']:.3f} "
            f"mean_bal_acc="
            f"{row['mean_balanced_accuracy']:.3%} "
            f"min_bal_acc="
            f"{row['min_balanced_accuracy']:.3%} "
            f"mean_recall="
            f"{row['mean_harmful_recall']:.3%} "
            f"min_recall="
            f"{row['min_harmful_recall']:.3%} "
            f"mean_specificity="
            f"{row['mean_specificity']:.3%}"
        )

    error_std_summary = next(
        row
        for row in summary_rows
        if row[
            "model"
        ]
        == "error_std_only"
    )

    severe_proxy_summary = next(
        row
        for row in summary_rows
        if row[
            "model"
        ]
        == "severe_proxy_only"
    )

    signed_proxy_summary = next(
        row
        for row in summary_rows
        if row[
            "model"
        ]
        == "signed_error_proxy_only"
    )

    print()

    print(
        "FROZEN PROXY VALUE-ADD CHECK"
    )

    print(
        f"error_std_only mean AUC="
        f"{error_std_summary['mean_auc']:.3f}"
    )

    print(
        f"severe_proxy_only mean AUC="
        f"{severe_proxy_summary['mean_auc']:.3f} "
        f"dAUC="
        f"{severe_proxy_summary['mean_auc'] - error_std_summary['mean_auc']:+.3f}"
    )

    print(
        f"signed_error_proxy_only mean AUC="
        f"{signed_proxy_summary['mean_auc']:.3f} "
        f"dAUC="
        f"{signed_proxy_summary['mean_auc'] - error_std_summary['mean_auc']:+.3f}"
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
            for row in coefficient_summary_rows
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
                f"{row['feature']:<42} "
                f"mean_coef="
                f"{row['mean_coefficient']:+.3f} "
                f"abs_coef="
                f"{row['mean_absolute_coefficient']:.3f} "
                f"sign_stability="
                f"{row['sign_stability']:.3%}"
            )

    best = summary_rows[
        0
    ]

    print()

    print(
        "BEST SUPPORT-EXPANSION TRANSFER MODEL"
    )

    print(
        f"name="
        f"{best['model']}"
    )

    print(
        f"mean_AUC="
        f"{best['mean_auc']:.3f}"
    )

    print(
        f"minimum_AUC="
        f"{best['min_auc']:.3f}"
    )

    print(
        f"mean_balanced_accuracy="
        f"{best['mean_balanced_accuracy']:.3%}"
    )

    print(
        f"mean_harmful_recall="
        f"{best['mean_harmful_recall']:.3%}"
    )

    print()

    print(
        "TEMPORAL AND REPRESENTATION VALIDITY NOTE"
    )

    print(
        "The Experiment 110 severe-underestimation and signed-error "
        "proxy outputs are imported from their previously generated "
        "leave-one-seed-out predictions."
    )

    print(
        "Their feature definitions are not modified using the "
        "support-expansion harmful/beneficial labels."
    )

    print(
        "The support-expansion logistic comparisons are trained "
        "reciprocally by block only to test whether the frozen "
        "proxy outputs contain transferable selectivity information."
    )

    print(
        "The signed-error proxy is multiplied by -1 only to express "
        "greater predicted underestimation in a harmful-high direction; "
        "this orientation follows the calibration-error definition and "
        "is not fitted from support-expansion outcomes."
    )

    print(
        "No new prospective seed, intervention threshold, or controller "
        "modification is introduced."
    )

    print(
        "With only eight harmful support expansions, positive results "
        "must remain provisional."
    )

    print(
        "=" * 210
    )

    combined_summary_rows = []

    for row in summary_rows:
        combined_summary_rows.append(
            row
        )

    for row in fold_rows:
        copy = {
            "record_type":
                "held_out_fold"
        }

        copy.update(
            row
        )

        combined_summary_rows.append(
            copy
        )

    for row in geometry_rows:
        copy = {
            "record_type":
                "raw_signal_geometry"
        }

        copy.update(
            row
        )

        combined_summary_rows.append(
            copy
        )

    save_csv(
        SUMMARY_OUTPUT_PATH,
        combined_summary_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        prediction_rows,
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
        f"Held-out predictions saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )

    print(
        f"Coefficient stability saved to: "
        f"{COEFFICIENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()