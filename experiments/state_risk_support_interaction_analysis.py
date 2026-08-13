import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


INPUT_PATH = Path(
    "results/"
    "prospective_state_guard_selectivity_decomposition_events.csv"
)

OUTPUT_PATH = Path(
    "results/"
    "state_risk_support_interaction_analysis.csv"
)

FOLD_OUTPUT_PATH = Path(
    "results/"
    "state_risk_support_interaction_analysis_folds.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "state_risk_support_interaction_analysis_coefficients.csv"
)

PREDICTION_OUTPUT_PATH = Path(
    "results/"
    "state_risk_support_interaction_analysis_predictions.csv"
)

RANDOM_STATE = 42
CLASS_THRESHOLD = 0.50


MODEL_SPECS = {
    "state_only": [
        "state_harmful_probability",
    ],

    "support_only": [
        "support_distance_baseline_action",
    ],

    "state_plus_support": [
        "state_harmful_probability",
        "support_distance_baseline_action",
    ],

    "state_support_interaction": [
        "state_harmful_probability",
        "support_distance_baseline_action",
        "state_x_support",
    ],
}


def read_csv(
    path: Path,
) -> list[dict]:

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


def usable_veto_events(
    rows: list[dict],
) -> list[dict]:

    output = []

    for row in rows:

        event_class = row.get(
            "selectivity_class",
            "",
        )

        if event_class not in (
            "harmful_vetoed",
            "beneficial_vetoed",
        ):
            continue

        copy = dict(
            row
        )

        state_probability = float(
            copy[
                "state_harmful_probability"
            ]
        )

        support_distance = float(
            copy[
                "support_distance_baseline_action"
            ]
        )

        copy[
            "state_x_support"
        ] = (
            state_probability
            * support_distance
        )

        output.append(
            copy
        )

    return output


def label_for_row(
    row: dict,
) -> int:

    return int(
        row[
            "selectivity_class"
        ]
        == "harmful_vetoed"
    )


def build_matrix(
    rows: list[dict],
    feature_names: list[str],
) -> np.ndarray:

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
    rows: list[dict],
) -> np.ndarray:

    return np.asarray(
        [
            label_for_row(
                row
            )
            for row in rows
        ],
        dtype=int,
    )


def make_model() -> Pipeline:

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


def safe_auc(
    y_true: np.ndarray,
    probabilities: np.ndarray,
) -> float:

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


def specificity_score(
    y_true: np.ndarray,
    predictions: np.ndarray,
) -> float:

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


def confusion_counts(
    y_true: np.ndarray,
    predictions: np.ndarray,
) -> dict:

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

    return {
        "tp":
            tp,

        "tn":
            tn,

        "fp":
            fp,

        "fn":
            fn,
    }


def coefficient_rows_for_fold(
    model: Pipeline,
    model_name: str,
    feature_names: list[str],
    held_out_seed: int,
) -> list[dict]:

    classifier = model.named_steps[
        "classifier"
    ]

    coefficients = classifier.coef_[
        0
    ]

    output = []

    for feature, coefficient in zip(
        feature_names,
        coefficients,
    ):

        output.append(
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

    return output


def coefficient_stability(
    rows: list[dict],
) -> list[dict]:

    grouped = defaultdict(
        list
    )

    for row in rows:

        key = (
            row[
                "model"
            ],
            row[
                "feature"
            ],
        )

        grouped[
            key
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

                "median_coefficient":
                    statistics.median(
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


def finite_mean(
    values: list[float],
) -> float:

    finite = [
        value
        for value in values
        if math.isfinite(
            value
        )
    ]

    if not finite:

        return float(
            "nan"
        )

    return statistics.mean(
        finite
    )


def evaluate_model(
    events: list[dict],
    model_name: str,
    feature_names: list[str],
) -> tuple[
    dict,
    list[dict],
    list[dict],
    list[dict],
]:

    seeds = sorted(
        {
            int(
                row[
                    "generation_seed"
                ]
            )
            for row in events
        }
    )

    fold_rows = []
    coefficient_rows = []
    prediction_rows = []

    pooled_true = []
    pooled_predictions = []
    pooled_probabilities = []

    for held_out_seed in seeds:

        train_rows = [
            row
            for row in events
            if int(
                row[
                    "generation_seed"
                ]
            )
            != held_out_seed
        ]

        test_rows = [
            row
            for row in events
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

        if len(
            np.unique(
                y_train
            )
        ) < 2:
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

        counts = confusion_counts(
            y_test,
            predictions,
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

                "balanced_accuracy":
                    balanced_accuracy,

                "harmful_recall":
                    float(
                        recall_score(
                            y_test,
                            predictions,
                            pos_label=1,
                            zero_division=0,
                        )
                    ),

                "harmful_precision":
                    float(
                        precision_score(
                            y_test,
                            predictions,
                            pos_label=1,
                            zero_division=0,
                        )
                    ),

                "beneficial_specificity":
                    specificity_score(
                        y_test,
                        predictions,
                    ),

                "roc_auc":
                    safe_auc(
                        y_test,
                        probabilities,
                    ),

                "tp":
                    counts[
                        "tp"
                    ],

                "tn":
                    counts[
                        "tn"
                    ],

                "fp":
                    counts[
                        "fp"
                    ],

                "fn":
                    counts[
                        "fn"
                    ],
            }
        )

        coefficient_rows.extend(
            coefficient_rows_for_fold(
                model,
                model_name,
                feature_names,
                held_out_seed,
            )
        )

        for (
            row,
            true_label,
            predicted_label,
            probability,
        ) in zip(
            test_rows,
            y_test,
            predictions,
            probabilities,
        ):

            prediction_rows.append(
                {
                    "model":
                        model_name,

                    "generation_seed":
                        held_out_seed,

                    "test_index":
                        row[
                            "test_index"
                        ],

                    "selectivity_class":
                        row[
                            "selectivity_class"
                        ],

                    "true_harmful":
                        int(
                            true_label
                        ),

                    "predicted_harmful":
                        int(
                            predicted_label
                        ),

                    "predicted_harmful_probability":
                        float(
                            probability
                        ),

                    "state_harmful_probability":
                        float(
                            row[
                                "state_harmful_probability"
                            ]
                        ),

                    "support_distance":
                        float(
                            row[
                                "support_distance_baseline_action"
                            ]
                        ),

                    "state_x_support":
                        float(
                            row[
                                "state_x_support"
                            ]
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

    counts = confusion_counts(
        y_true,
        y_pred,
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

    valid_fold_balanced = [
        value
        for value in fold_balanced
        if math.isfinite(
            value
        )
    ]

    summary = {
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

        "harmful_events":
            int(
                np.sum(
                    y_true
                    == 1
                )
            ),

        "beneficial_events":
            int(
                np.sum(
                    y_true
                    == 0
                )
            ),

        "accuracy":
            float(
                accuracy_score(
                    y_true,
                    y_pred,
                )
            ),

        "balanced_accuracy":
            float(
                balanced_accuracy_score(
                    y_true,
                    y_pred,
                )
            ),

        "harmful_recall":
            float(
                recall_score(
                    y_true,
                    y_pred,
                    pos_label=1,
                    zero_division=0,
                )
            ),

        "harmful_precision":
            float(
                precision_score(
                    y_true,
                    y_pred,
                    pos_label=1,
                    zero_division=0,
                )
            ),

        "beneficial_specificity":
            specificity_score(
                y_true,
                y_pred,
            ),

        "roc_auc":
            safe_auc(
                y_true,
                probabilities,
            ),

        "tp":
            counts[
                "tp"
            ],

        "tn":
            counts[
                "tn"
            ],

        "fp":
            counts[
                "fp"
            ],

        "fn":
            counts[
                "fn"
            ],

        "mean_fold_balanced_accuracy":
            finite_mean(
                fold_balanced
            ),

        "min_fold_balanced_accuracy":
            (
                min(
                    valid_fold_balanced
                )
                if valid_fold_balanced
                else float(
                    "nan"
                )
            ),

        "mean_fold_roc_auc":
            finite_mean(
                fold_auc
            ),
    }

    return (
        summary,
        fold_rows,
        coefficient_rows,
        prediction_rows,
    )


def main() -> None:

    rows = read_csv(
        INPUT_PATH
    )

    events = usable_veto_events(
        rows
    )

    harmful = sum(
        int(
            row[
                "selectivity_class"
            ]
            == "harmful_vetoed"
        )
        for row in events
    )

    beneficial = sum(
        int(
            row[
                "selectivity_class"
            ]
            == "beneficial_vetoed"
        )
        for row in events
    )

    summaries = []
    all_fold_rows = []
    all_coefficient_rows = []
    all_prediction_rows = []

    print(
        "=" * 205
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "STATE-RISK x SUPPORT "
        "INTERACTION ANALYSIS"
    )

    print(
        "=" * 205
    )

    print(
        f"input="
        f"{INPUT_PATH}"
    )

    print(
        f"vetoed events="
        f"{len(events)}"
    )

    print(
        f"harmful vetoed="
        f"{harmful}"
    )

    print(
        f"beneficial vetoed="
        f"{beneficial}"
    )

    print(
        "validation="
        "leave-one-generation-seed-out"
    )

    print()

    for (
        model_name,
        feature_names,
    ) in MODEL_SPECS.items():

        (
            summary,
            fold_rows,
            coefficient_rows,
            prediction_rows,
        ) = evaluate_model(
            events,
            model_name,
            feature_names,
        )

        summaries.append(
            summary
        )

        all_fold_rows.extend(
            fold_rows
        )

        all_coefficient_rows.extend(
            coefficient_rows
        )

        all_prediction_rows.extend(
            prediction_rows
        )

    summaries.sort(
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

    coefficient_summary = (
        coefficient_stability(
            all_coefficient_rows
        )
    )

    save_csv(
        OUTPUT_PATH,
        summaries,
    )

    save_csv(
        FOLD_OUTPUT_PATH,
        all_fold_rows,
    )

    save_csv(
        COEFFICIENT_OUTPUT_PATH,
        coefficient_summary,
    )

    save_csv(
        PREDICTION_OUTPUT_PATH,
        all_prediction_rows,
    )

    print(
        "MODEL PERFORMANCE"
    )

    for row in summaries:

        print(
            f"{row['model']:<28} "
            f"features="
            f"{row['feature_count']} "
            f"balanced_acc="
            f"{row['balanced_accuracy']:.3%} "
            f"harmful_recall="
            f"{row['harmful_recall']:.3%} "
            f"harmful_precision="
            f"{row['harmful_precision']:.3%} "
            f"beneficial_specificity="
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
        "FOLD STABILITY"
    )

    for row in summaries:

        print(
            f"{row['model']:<28} "
            f"mean_fold_bal_acc="
            f"{row['mean_fold_balanced_accuracy']:.3%} "
            f"min_fold_bal_acc="
            f"{row['min_fold_balanced_accuracy']:.3%} "
            f"mean_fold_AUC="
            f"{row['mean_fold_roc_auc']:.3f}"
        )

    print()

    print(
        "COEFFICIENT STABILITY"
    )

    for model_name in (
        MODEL_SPECS
    ):

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
                f"{row['feature']:<40} "
                f"mean_coef="
                f"{row['mean_coefficient']:+.3f} "
                f"abs_coef="
                f"{row['mean_absolute_coefficient']:.3f} "
                f"sign_stability="
                f"{row['dominant_sign_fraction']:.3%}"
            )

    print()

    best = summaries[
        0
    ]

    print(
        "BEST RETROSPECTIVE SELECTIVITY MODEL"
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
        f"harmful_recall="
        f"{best['harmful_recall']:.3%}"
    )

    print(
        f"beneficial_specificity="
        f"{best['beneficial_specificity']:.3%}"
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
        "This is retrospective interaction analysis on the "
        "already-consumed 44011-44030 prospective seed block. "
        "No model or threshold identified here constitutes "
        "prospective validation."
    )

    print(
        "=" * 205
    )

    print(
        f"Summary saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Fold results saved to: "
        f"{FOLD_OUTPUT_PATH}"
    )

    print(
        f"Coefficient stability saved to: "
        f"{COEFFICIENT_OUTPUT_PATH}"
    )

    print(
        f"Predictions saved to: "
        f"{PREDICTION_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()