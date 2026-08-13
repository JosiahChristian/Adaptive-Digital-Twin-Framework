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


INPUT_PATH = Path(
    "results/"
    "cross_block_constituent_stability_analysis_events.csv"
)

SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "block_held_out_two_feature_decision_geometry.csv"
)

PREDICTION_OUTPUT_PATH = Path(
    "results/"
    "block_held_out_two_feature_decision_geometry_predictions.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "block_held_out_two_feature_decision_geometry_coefficients.csv"
)


BLOCKS = [
    "block_071_090",
    "block_091_110",
]

CLASS_THRESHOLD = 0.50

RANDOM_STATE = 42

FLOAT_TOLERANCE = 1e-12


MODEL_SPECS = {
    "error_std_only": [
        "local_error_std",
    ],

    "underestimate_fraction_only": [
        "local_underestimate_fraction",
    ],

    "two_feature_compact": [
        "local_error_std",
        "local_underestimate_fraction",
    ],

    "two_feature_interaction": [
        "local_error_std",
        "local_underestimate_fraction",
        "error_std_x_underestimate_fraction",
    ],
}


def read_events():
    with INPUT_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        rows = list(
            csv.DictReader(
                file
            )
        )

    output = []

    for row in rows:
        copy = dict(
            row
        )

        error_std = float(
            copy[
                "local_error_std"
            ]
        )

        underestimate_fraction = float(
            copy[
                "local_underestimate_fraction"
            ]
        )

        copy[
            "error_std_x_underestimate_fraction"
        ] = (
            error_std
            * underestimate_fraction
        )

        copy[
            "harmful_target"
        ] = int(
            copy[
                "class"
            ]
            == "harmful"
        )

        output.append(
            copy
        )

    return output


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


def evaluate_predictions(
    y_true,
    probabilities,
):
    predictions = (
        probabilities
        >= CLASS_THRESHOLD
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


def block_held_out_evaluation(
    rows,
):
    fold_rows = []
    prediction_rows = []
    coefficient_rows = []

    for model_name, feature_names in MODEL_SPECS.items():

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
                feature_names,
            )

            y_train = build_labels(
                training_rows
            )

            x_test = build_matrix(
                test_rows,
                feature_names,
            )

            y_test = build_labels(
                test_rows
            )

            if (
                len(
                    np.unique(
                        y_train
                    )
                )
                < 2
            ):
                raise RuntimeError(
                    f"Training block for {held_out_block} "
                    f"contains only one class."
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

            metrics = evaluate_predictions(
                y_test,
                probabilities,
            )

            fold_rows.append(
                {
                    "record_type":
                        "held_out_fold",

                    "model":
                        model_name,

                    "features":
                        "|".join(
                            feature_names
                        ),

                    "held_out_block":
                        held_out_block,

                    "training_block":
                        "|".join(
                            block
                            for block in BLOCKS
                            if block
                            != held_out_block
                        ),

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

                    "training_beneficial":
                        int(
                            np.sum(
                                y_train
                                == 0
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

                    "test_beneficial":
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
                feature_names,
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

                        "standardized_coefficient":
                            float(
                                coefficient
                            ),
                    }
                )

            predictions = (
                probabilities
                >= CLASS_THRESHOLD
            ).astype(
                int
            )

            for (
                row,
                target,
                probability,
                prediction,
            ) in zip(
                test_rows,
                y_test,
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
                            int(
                                float(
                                    row[
                                        "generation_seed"
                                    ]
                                )
                            ),

                        "test_index":
                            int(
                                float(
                                    row[
                                        "test_index"
                                    ]
                                )
                            ),

                        "support_baseline_action":
                            int(
                                float(
                                    row[
                                        "support_baseline_action"
                                    ]
                                )
                            ),

                        "true_class":
                            row[
                                "class"
                            ],

                        "harmful_target":
                            int(
                                target
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

                        "local_underestimate_fraction":
                            float(
                                row[
                                    "local_underestimate_fraction"
                                ]
                            ),

                        "error_std_x_underestimate_fraction":
                            float(
                                row[
                                    "error_std_x_underestimate_fraction"
                                ]
                            ),
                    }
                )

    return (
        fold_rows,
        prediction_rows,
        coefficient_rows,
    )


def summarize_models(
    fold_rows,
):
    output = []

    for model_name in MODEL_SPECS:
        rows = [
            row
            for row in fold_rows
            if row[
                "model"
            ]
            == model_name
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

                "folds":
                    len(
                        rows
                    ),

                "mean_balanced_accuracy":
                    finite_mean(
                        [
                            float(
                                row[
                                    "balanced_accuracy"
                                ]
                            )
                            for row in rows
                        ]
                    ),

                "min_balanced_accuracy":
                    min(
                        float(
                            row[
                                "balanced_accuracy"
                            ]
                        )
                        for row in rows
                    ),

                "max_balanced_accuracy":
                    max(
                        float(
                            row[
                                "balanced_accuracy"
                            ]
                        )
                        for row in rows
                    ),

                "mean_harmful_recall":
                    finite_mean(
                        [
                            float(
                                row[
                                    "harmful_recall"
                                ]
                            )
                            for row in rows
                        ]
                    ),

                "min_harmful_recall":
                    min(
                        float(
                            row[
                                "harmful_recall"
                            ]
                        )
                        for row in rows
                    ),

                "mean_beneficial_specificity":
                    finite_mean(
                        [
                            float(
                                row[
                                    "beneficial_specificity"
                                ]
                            )
                            for row in rows
                        ]
                    ),

                "mean_roc_auc":
                    finite_mean(
                        [
                            float(
                                row[
                                    "roc_auc"
                                ]
                            )
                            for row in rows
                        ]
                    ),

                "min_roc_auc":
                    min(
                        float(
                            row[
                                "roc_auc"
                            ]
                        )
                        for row in rows
                    ),

                "max_roc_auc":
                    max(
                        float(
                            row[
                                "roc_auc"
                            ]
                        )
                        for row in rows
                    ),
            }
        )

    output.sort(
        key=lambda row: (
            float(
                row[
                    "mean_roc_auc"
                ]
            ),
            float(
                row[
                    "mean_balanced_accuracy"
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

    for model_name, feature in keys:
        values = [
            float(
                row[
                    "standardized_coefficient"
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
        "BLOCK-HELD-OUT TWO-FEATURE DECISION GEOMETRY"
    )

    print(
        "=" * 210
    )

    print(
        f"input="
        f"{INPUT_PATH}"
    )

    print(
        f"blocks="
        f"{BLOCKS}"
    )

    print(
        "primary constituent features="
        "['local_error_std', "
        "'local_underestimate_fraction']"
    )

    print()

    rows = read_events()

    harmful_total = sum(
        int(
            row[
                "harmful_target"
            ]
        )
        for row in rows
    )

    beneficial_total = (
        len(
            rows
        )
        - harmful_total
    )

    print(
        "EVENT POPULATION"
    )

    print(
        f"rows="
        f"{len(rows)}"
    )

    print(
        f"beneficial="
        f"{beneficial_total}"
    )

    print(
        f"harmful="
        f"{harmful_total}"
    )

    print()

    (
        fold_rows,
        prediction_rows,
        coefficient_rows,
    ) = block_held_out_evaluation(
        rows
    )

    model_summary_rows = summarize_models(
        fold_rows
    )

    coefficient_summary_rows = (
        coefficient_stability(
            coefficient_rows
        )
    )

    print(
        "BLOCK-HELD-OUT PERFORMANCE"
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
                f"harmful_precision="
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
        "MODEL STABILITY SUMMARY"
    )

    for row in model_summary_rows:
        print(
            f"{row['model']:<34} "
            f"mean_bal_acc="
            f"{row['mean_balanced_accuracy']:.3%} "
            f"min_bal_acc="
            f"{row['min_balanced_accuracy']:.3%} "
            f"mean_harmful_recall="
            f"{row['mean_harmful_recall']:.3%} "
            f"mean_specificity="
            f"{row['mean_beneficial_specificity']:.3%} "
            f"mean_AUC="
            f"{row['mean_roc_auc']:.3f} "
            f"min_AUC="
            f"{row['min_roc_auc']:.3f}"
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

    best = model_summary_rows[
        0
    ]

    compact = next(
        row
        for row in model_summary_rows
        if row[
            "model"
        ]
        == "two_feature_compact"
    )

    error_only = next(
        row
        for row in model_summary_rows
        if row[
            "model"
        ]
        == "error_std_only"
    )

    underestimate_only = next(
        row
        for row in model_summary_rows
        if row[
            "model"
        ]
        == "underestimate_fraction_only"
    )

    print()

    print(
        "TWO-FEATURE VALUE-ADD CHECK"
    )

    print(
        f"compact mean AUC="
        f"{compact['mean_roc_auc']:.3f}"
    )

    print(
        f"error_std_only mean AUC="
        f"{error_only['mean_roc_auc']:.3f}"
    )

    print(
        f"underestimate_fraction_only mean AUC="
        f"{underestimate_only['mean_roc_auc']:.3f}"
    )

    print(
        f"compact dAUC vs error_std="
        f"{compact['mean_roc_auc'] - error_only['mean_roc_auc']:+.3f}"
    )

    print(
        f"compact dAUC vs underestimate_fraction="
        f"{compact['mean_roc_auc'] - underestimate_only['mean_roc_auc']:+.3f}"
    )

    print()

    print(
        "BEST BLOCK-HELD-OUT MODEL"
    )

    print(
        f"name="
        f"{best['model']}"
    )

    print(
        f"mean_balanced_accuracy="
        f"{best['mean_balanced_accuracy']:.3%}"
    )

    print(
        f"min_balanced_accuracy="
        f"{best['min_balanced_accuracy']:.3%}"
    )

    print(
        f"mean_harmful_recall="
        f"{best['mean_harmful_recall']:.3%}"
    )

    print(
        f"mean_roc_auc="
        f"{best['mean_roc_auc']:.3f}"
    )

    print(
        f"min_roc_auc="
        f"{best['min_roc_auc']:.3f}"
    )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 106 evaluates historical decision geometry "
        "only. Each block is evaluated by a model trained entirely "
        "on the other block."
    )

    print(
        "The 0.50 classification threshold is used only for "
        "descriptive classifier metrics and is not a proposed "
        "controller threshold."
    )

    print(
        "No prospective seed, controller intervention, or "
        "new safety rule is introduced."
    )

    print(
        "Given only eight harmful events total, positive results "
        "remain provisional and must not be treated as sufficient "
        "prospective validation."
    )

    print(
        "=" * 210
    )

    summary_output_rows = []

    summary_output_rows.extend(
        model_summary_rows
    )

    summary_output_rows.extend(
        fold_rows
    )

    save_csv(
        SUMMARY_OUTPUT_PATH,
        summary_output_rows,
    )

    save_csv(
        PREDICTION_OUTPUT_PATH,
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
        f"{PREDICTION_OUTPUT_PATH}"
    )

    print(
        f"Coefficient stability saved to: "
        f"{COEFFICIENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()