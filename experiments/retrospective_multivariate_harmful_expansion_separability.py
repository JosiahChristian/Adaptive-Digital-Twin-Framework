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
    "cross_seed_harmful_expansion_feature_decomposition_events.csv"
)

OUTPUT_PATH = Path(
    "results/"
    "retrospective_multivariate_harmful_expansion_separability.csv"
)

FOLD_OUTPUT_PATH = Path(
    "results/"
    "retrospective_multivariate_harmful_expansion_separability_folds.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "retrospective_multivariate_harmful_expansion_separability_coefficients.csv"
)

PREDICTION_OUTPUT_PATH = Path(
    "results/"
    "retrospective_multivariate_harmful_expansion_separability_predictions.csv"
)

RANDOM_STATE = 42
CLASS_THRESHOLD = 0.50
FLOAT_TOLERANCE = 1e-12


FEATURE_SETS = {
    "gate": [
        "support_distance",
        "downside_score",
        "predicted_regret_margin",
        "action_step",
    ],

    "state": [
        "context_current_mismatch_indicator",
        "context_anchor_age",
        "context_trigger_score",
    ],

    "loss_geometry": [
        "predicted_loss_k1",
        "predicted_loss_k2",
        "predicted_loss_k3",
        "predicted_loss_k1_minus_k2",
        "predicted_loss_k1_minus_k3",
        "predicted_loss_k2_minus_k3",
    ],

    "combined_compact": [
        "predicted_loss_k3",
        "context_current_mismatch_indicator",
        "context_anchor_age",
        "support_distance",
        "predicted_regret_margin",
        "action_step",
        "downside_score",
    ],

    "combined_extended": [
        "predicted_loss_k1",
        "predicted_loss_k2",
        "predicted_loss_k3",
        "predicted_loss_k1_minus_k2",
        "predicted_loss_k1_minus_k3",
        "predicted_loss_k2_minus_k3",
        "context_current_mismatch_indicator",
        "context_anchor_age",
        "context_trigger_score",
        "support_distance",
        "predicted_regret_margin",
        "action_step",
        "downside_score",
        "predicted_under_risk",
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


def usable_events(
    rows: list[dict],
) -> list[dict]:

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


def label_for_row(
    row: dict,
) -> int:

    return int(
        row[
            "outcome"
        ]
        == "harmful"
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


def safe_auc(
    y_true: np.ndarray,
    probabilities: np.ndarray,
) -> float:

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
    y_true: np.ndarray,
    y_pred: np.ndarray,
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
            y_pred[
                negative_mask
            ]
            == 0
        )
    )


def confusion_counts(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> dict:

    tp = int(
        np.sum(
            (
                y_true
                == 1
            )
            & (
                y_pred
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
                y_pred
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
                y_pred
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
                y_pred
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


def coefficient_rows_for_fold(
    model: Pipeline,
    feature_set_name: str,
    feature_names: list[str],
    held_out_seed: int,
) -> list[dict]:

    classifier = model.named_steps[
        "classifier"
    ]

    coefficients = classifier.coef_[
        0
    ]

    rows = []

    for feature_name, coefficient in zip(
        feature_names,
        coefficients,
    ):

        rows.append(
            {
                "feature_set":
                    feature_set_name,

                "held_out_seed":
                    held_out_seed,

                "feature":
                    feature_name,

                "standardized_coefficient":
                    float(
                        coefficient
                    ),
            }
        )

    return rows


def coefficient_stability_summary(
    coefficient_rows: list[dict],
) -> list[dict]:

    grouped = defaultdict(
        list
    )

    for row in coefficient_rows:

        grouped[
            (
                row[
                    "feature_set"
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

    summary = []

    for (
        feature_set_name,
        feature_name,
    ), values in grouped.items():

        mean_value = statistics.mean(
            values
        )

        median_value = statistics.median(
            values
        )

        positive_fraction = statistics.mean(
            [
                float(
                    value
                    > 0
                )
                for value in values
            ]
        )

        negative_fraction = statistics.mean(
            [
                float(
                    value
                    < 0
                )
                for value in values
            ]
        )

        dominant_sign_fraction = max(
            positive_fraction,
            negative_fraction,
        )

        summary.append(
            {
                "feature_set":
                    feature_set_name,

                "feature":
                    feature_name,

                "folds":
                    len(
                        values
                    ),

                "mean_standardized_coefficient":
                    mean_value,

                "median_standardized_coefficient":
                    median_value,

                "std_standardized_coefficient":
                    (
                        statistics.pstdev(
                            values
                        )
                        if len(
                            values
                        )
                        > 1
                        else 0.0
                    ),

                "positive_fraction":
                    positive_fraction,

                "negative_fraction":
                    negative_fraction,

                "dominant_sign_fraction":
                    dominant_sign_fraction,

                "mean_absolute_coefficient":
                    statistics.mean(
                        abs(
                            value
                        )
                        for value in values
                    ),
            }
        )

    summary.sort(
        key=lambda row: (
            row[
                "feature_set"
            ],
            -float(
                row[
                    "mean_absolute_coefficient"
                ]
            ),
        )
    )

    return summary


def evaluate_feature_set(
    events: list[dict],
    feature_set_name: str,
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
    pooled_pred = []
    pooled_probability = []

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

        x_test = build_matrix(
            test_rows,
            feature_names,
        )

        y_test = build_labels(
            test_rows
        )

        if len(
            np.unique(
                y_train
            )
        ) < 2:

            continue

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
                "feature_set":
                    feature_set_name,

                "held_out_seed":
                    held_out_seed,

                "train_events":
                    len(
                        train_rows
                    ),

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

                "accuracy":
                    float(
                        accuracy_score(
                            y_test,
                            predictions,
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
                feature_set_name,
                feature_names,
                held_out_seed,
            )
        )

        for local_index, (
            row,
            true_label,
            predicted_label,
            probability,
        ) in enumerate(
            zip(
                test_rows,
                y_test,
                predictions,
                probabilities,
            )
        ):

            prediction_rows.append(
                {
                    "feature_set":
                        feature_set_name,

                    "generation_seed":
                        held_out_seed,

                    "test_index":
                        row[
                            "test_index"
                        ],

                    "true_outcome":
                        row[
                            "outcome"
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
                }
            )

        pooled_true.extend(
            y_test.tolist()
        )

        pooled_pred.extend(
            predictions.tolist()
        )

        pooled_probability.extend(
            probabilities.tolist()
        )

    y_true = np.asarray(
        pooled_true,
        dtype=int,
    )

    y_pred = np.asarray(
        pooled_pred,
        dtype=int,
    )

    probabilities = np.asarray(
        pooled_probability,
        dtype=float,
    )

    counts = confusion_counts(
        y_true,
        y_pred,
    )

    summary = {
        "feature_set":
            feature_set_name,

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
    }

    return (
        summary,
        fold_rows,
        coefficient_rows,
        prediction_rows,
    )


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


def add_fold_stability_metrics(
    summaries: list[dict],
    fold_rows: list[dict],
) -> None:

    for summary in summaries:

        name = summary[
            "feature_set"
        ]

        matching = [
            row
            for row in fold_rows
            if row[
                "feature_set"
            ]
            == name
        ]

        balanced = [
            float(
                row[
                    "balanced_accuracy"
                ]
            )
            for row in matching
        ]

        recall = [
            float(
                row[
                    "harmful_recall"
                ]
            )
            for row in matching
        ]

        specificity = [
            float(
                row[
                    "beneficial_specificity"
                ]
            )
            for row in matching
        ]

        auc_values = [
            float(
                row[
                    "roc_auc"
                ]
            )
            for row in matching
        ]

        summary[
            "mean_fold_balanced_accuracy"
        ] = finite_mean(
            balanced
        )

        summary[
            "mean_fold_harmful_recall"
        ] = finite_mean(
            recall
        )

        summary[
            "mean_fold_beneficial_specificity"
        ] = finite_mean(
            specificity
        )

        summary[
            "mean_fold_roc_auc"
        ] = finite_mean(
            auc_values
        )

        valid_balanced = [
            value
            for value in balanced
            if math.isfinite(
                value
            )
        ]

        summary[
            "min_fold_balanced_accuracy"
        ] = (
            min(
                valid_balanced
            )
            if valid_balanced
            else float(
                "nan"
            )
        )


def main() -> None:

    rows = read_csv(
        INPUT_PATH
    )

    events = usable_events(
        rows
    )

    beneficial_count = sum(
        int(
            row[
                "outcome"
            ]
            == "beneficial"
        )
        for row in events
    )

    harmful_count = sum(
        int(
            row[
                "outcome"
            ]
            == "harmful"
        )
        for row in events
    )

    print(
        "=" * 205
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "RETROSPECTIVE MULTIVARIATE "
        "HARMFUL-EXPANSION SEPARABILITY"
    )

    print(
        "=" * 205
    )

    print(
        f"input="
        f"{INPUT_PATH}"
    )

    print(
        f"usable events="
        f"{len(events)}"
    )

    print(
        f"beneficial="
        f"{beneficial_count}"
    )

    print(
        f"harmful="
        f"{harmful_count}"
    )

    print(
        "validation="
        "leave-one-generation-seed-out"
    )

    print()

    summaries = []
    all_fold_rows = []
    all_coefficient_rows = []
    all_prediction_rows = []

    for (
        feature_set_name,
        feature_names,
    ) in FEATURE_SETS.items():

        (
            summary,
            fold_rows,
            coefficient_rows,
            prediction_rows,
        ) = evaluate_feature_set(
            events,
            feature_set_name,
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

    add_fold_stability_metrics(
        summaries,
        all_fold_rows,
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
        coefficient_stability_summary(
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
        "FEATURE-SET PERFORMANCE"
    )

    for row in summaries:

        print(
            f"{row['feature_set']:<20} "
            f"features="
            f"{row['feature_count']:<2} "
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
            f"{row['feature_set']:<20} "
            f"mean_fold_bal_acc="
            f"{row['mean_fold_balanced_accuracy']:.3%} "
            f"min_fold_bal_acc="
            f"{row['min_fold_balanced_accuracy']:.3%} "
            f"mean_fold_harmful_recall="
            f"{row['mean_fold_harmful_recall']:.3%} "
            f"mean_fold_specificity="
            f"{row['mean_fold_beneficial_specificity']:.3%} "
            f"mean_fold_AUC="
            f"{row['mean_fold_roc_auc']:.3f}"
        )

    print()

    print(
        "MOST STABLE COEFFICIENTS"
    )

    for feature_set_name in (
        FEATURE_SETS
    ):

        print()

        print(
            feature_set_name
        )

        matching = [
            row
            for row in coefficient_summary
            if row[
                "feature_set"
            ]
            == feature_set_name
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

        for row in matching[
            :8
        ]:

            print(
                f"  "
                f"{row['feature']:<40} "
                f"mean_coef="
                f"{row['mean_standardized_coefficient']:+.3f} "
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
        "BEST RETROSPECTIVE FEATURE SET"
    )

    print(
        f"name="
        f"{best['feature_set']}"
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
        "This experiment is retrospective hypothesis generation. "
        "No feature set or coefficient from these validation seeds "
        "constitutes prospective controller validation."
    )

    print(
        "=" * 205
    )

    print(
        f"Summary results saved to: "
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