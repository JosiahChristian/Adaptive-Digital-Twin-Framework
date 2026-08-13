import csv
import math
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

from experiments.historical_local_calibration_risk_representation import (
    event_rows_for_seed,
)


SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "frozen_calibration_risk_threshold_selection.csv"
)

PREDICTION_OUTPUT_PATH = Path(
    "results/"
    "frozen_calibration_risk_threshold_selection_predictions.csv"
)

THRESHOLD_OUTPUT_PATH = Path(
    "results/"
    "frozen_calibration_risk_threshold_selection_thresholds.csv"
)


HISTORICAL_SEEDS = list(
    range(
        44001,
        44091,
    )
)

FEATURE_NAMES = [
    "predicted_action_loss",
    "local_mean_error",
    "local_error_std",
    "local_underestimate_fraction",
    "local_severe_underestimate_fraction",
]

SEVERE_UNDERESTIMATION_THRESHOLD = -0.050

MINIMUM_SEVERE_RECALL = 0.80

RANDOM_STATE = 42

FLOAT_TOLERANCE = 1e-12


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
):
    return np.asarray(
        [
            [
                float(
                    row[
                        feature
                    ]
                )
                for feature in FEATURE_NAMES
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
                float(
                    row[
                        "calibration_error"
                    ]
                )
                <= SEVERE_UNDERESTIMATION_THRESHOLD
            )
            for row in rows
        ],
        dtype=int,
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


def evaluate_threshold(
    y_true,
    probabilities,
    threshold,
):
    predictions = (
        probabilities
        >= threshold
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

    severe_recall = float(
        recall_score(
            y_true,
            predictions,
            pos_label=1,
            zero_division=0,
        )
    )

    severe_precision = float(
        precision_score(
            y_true,
            predictions,
            pos_label=1,
            zero_division=0,
        )
    )

    specificity = specificity_score(
        y_true,
        predictions,
    )

    balanced_accuracy = float(
        balanced_accuracy_score(
            y_true,
            predictions,
        )
    )

    return {
        "threshold":
            float(
                threshold
            ),

        "balanced_accuracy":
            balanced_accuracy,

        "severe_recall":
            severe_recall,

        "severe_precision":
            severe_precision,

        "nonsevere_specificity":
            specificity,

        "flagged":
            int(
                np.sum(
                    predictions
                    == 1
                )
            ),

        "flagged_fraction":
            float(
                np.mean(
                    predictions
                    == 1
                )
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


def reconstruct_historical_population():
    rows = []

    for seed in HISTORICAL_SEEDS:
        print(
            f"reconstructing historical seed "
            f"{seed}..."
        )

        rows.extend(
            event_rows_for_seed(
                seed
            )
        )

    return rows


def generate_oof_predictions(
    rows,
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

    output = []

    for held_out_seed in seeds:
        print(
            f"OOF held-out seed "
            f"{held_out_seed}..."
        )

        training_rows = [
            row
            for row in rows
            if int(
                row[
                    "generation_seed"
                ]
            )
            != held_out_seed
        ]

        held_out_rows = [
            row
            for row in rows
            if int(
                row[
                    "generation_seed"
                ]
            )
            == held_out_seed
        ]

        x_train = build_matrix(
            training_rows
        )

        y_train = build_labels(
            training_rows
        )

        x_test = build_matrix(
            held_out_rows
        )

        y_test = build_labels(
            held_out_rows
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

        for (
            row,
            target,
            probability,
        ) in zip(
            held_out_rows,
            y_test,
            probabilities,
        ):
            output.append(
                {
                    "generation_seed":
                        held_out_seed,

                    "test_index":
                        int(
                            row[
                                "test_index"
                            ]
                        ),

                    "action":
                        int(
                            row[
                                "action"
                            ]
                        ),

                    "severe_underestimation":
                        int(
                            target
                        ),

                    "calibration_error":
                        float(
                            row[
                                "calibration_error"
                            ]
                        ),

                    "predicted_probability":
                        float(
                            probability
                        ),

                    "predicted_action_loss":
                        float(
                            row[
                                "predicted_action_loss"
                            ]
                        ),

                    "local_mean_error":
                        float(
                            row[
                                "local_mean_error"
                            ]
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

                    "local_severe_underestimate_fraction":
                        float(
                            row[
                                "local_severe_underestimate_fraction"
                            ]
                        ),
                }
            )

    return output


def candidate_thresholds(
    probabilities,
):
    unique_values = sorted(
        {
            float(
                value
            )
            for value in probabilities
            if math.isfinite(
                float(
                    value
                )
            )
        }
    )

    return unique_values


def choose_threshold(
    threshold_rows,
):
    qualifying = [
        row
        for row in threshold_rows
        if float(
            row[
                "severe_recall"
            ]
        )
        >= (
            MINIMUM_SEVERE_RECALL
            - FLOAT_TOLERANCE
        )
    ]

    if not qualifying:
        raise RuntimeError(
            "No candidate probability threshold "
            "achieved the preregistered minimum "
            "severe-underestimation recall."
        )

    best = max(
        qualifying,
        key=lambda row: (
            float(
                row[
                    "nonsevere_specificity"
                ]
            ),
            float(
                row[
                    "severe_precision"
                ]
            ),
            float(
                row[
                    "threshold"
                ]
            ),
        ),
    )

    return best


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
        "FROZEN CALIBRATION-RISK THRESHOLD SELECTION"
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
        f"features="
        f"{FEATURE_NAMES}"
    )

    print(
        f"severe underestimation threshold="
        f"{SEVERE_UNDERESTIMATION_THRESHOLD:.3f}"
    )

    print(
        f"minimum severe recall="
        f"{MINIMUM_SEVERE_RECALL:.3%}"
    )

    print()

    historical_rows = (
        reconstruct_historical_population()
    )

    print()

    print(
        "GENERATING LEAVE-ONE-SEED-OUT "
        "OUT-OF-FOLD PROBABILITIES"
    )

    prediction_rows = (
        generate_oof_predictions(
            historical_rows
        )
    )

    y_true = np.asarray(
        [
            int(
                row[
                    "severe_underestimation"
                ]
            )
            for row in prediction_rows
        ],
        dtype=int,
    )

    probabilities = np.asarray(
        [
            float(
                row[
                    "predicted_probability"
                ]
            )
            for row in prediction_rows
        ],
        dtype=float,
    )

    severe_total = int(
        np.sum(
            y_true
            == 1
        )
    )

    nonsevere_total = int(
        np.sum(
            y_true
            == 0
        )
    )

    print()

    print(
        "OUT-OF-FOLD POPULATION"
    )

    print(
        f"rows="
        f"{len(y_true)}"
    )

    print(
        f"severe="
        f"{severe_total}"
    )

    print(
        f"nonsevere="
        f"{nonsevere_total}"
    )

    print(
        f"severe fraction="
        f"{severe_total / len(y_true):.3%}"
    )

    print(
        f"OOF ROC AUC="
        f"{roc_auc_score(y_true, probabilities):.3f}"
    )

    thresholds = candidate_thresholds(
        probabilities
    )

    print(
        f"candidate thresholds="
        f"{len(thresholds)}"
    )

    threshold_rows = [
        evaluate_threshold(
            y_true,
            probabilities,
            threshold,
        )
        for threshold in thresholds
    ]

    selected = choose_threshold(
        threshold_rows
    )

    for row in threshold_rows:
        row[
            "qualifies_recall_constraint"
        ] = int(
            float(
                row[
                    "severe_recall"
                ]
            )
            >= (
                MINIMUM_SEVERE_RECALL
                - FLOAT_TOLERANCE
            )
        )

        row[
            "selected_primary_threshold"
        ] = int(
            abs(
                float(
                    row[
                        "threshold"
                    ]
                )
                - float(
                    selected[
                        "threshold"
                    ]
                )
            )
            <= FLOAT_TOLERANCE
        )

    qualifying_rows = [
        row
        for row in threshold_rows
        if int(
            row[
                "qualifies_recall_constraint"
            ]
        )
        == 1
    ]

    print()

    print(
        "PREREGISTERED THRESHOLD SELECTION"
    )

    print(
        f"qualifying thresholds="
        f"{len(qualifying_rows)}"
    )

    print(
        f"SELECTED tau_cal="
        f"{selected['threshold']:.12f}"
    )

    print(
        f"severe recall="
        f"{selected['severe_recall']:.3%}"
    )

    print(
        f"nonsevere specificity="
        f"{selected['nonsevere_specificity']:.3%}"
    )

    print(
        f"severe precision="
        f"{selected['severe_precision']:.3%}"
    )

    print(
        f"balanced accuracy="
        f"{selected['balanced_accuracy']:.3%}"
    )

    print(
        f"flagged fraction="
        f"{selected['flagged_fraction']:.3%}"
    )

    print(
        f"TP="
        f"{selected['tp']} "
        f"FP="
        f"{selected['fp']} "
        f"FN="
        f"{selected['fn']} "
        f"TN="
        f"{selected['tn']}"
    )

    summary_rows = [
        {
            "historical_seed_start":
                HISTORICAL_SEEDS[
                    0
                ],

            "historical_seed_end":
                HISTORICAL_SEEDS[
                    -1
                ],

            "historical_rows":
                len(
                    y_true
                ),

            "severe_rows":
                severe_total,

            "nonsevere_rows":
                nonsevere_total,

            "severe_fraction":
                severe_total
                / len(
                    y_true
                ),

            "oof_roc_auc":
                float(
                    roc_auc_score(
                        y_true,
                        probabilities,
                    )
                ),

            "minimum_required_severe_recall":
                MINIMUM_SEVERE_RECALL,

            "candidate_threshold_count":
                len(
                    thresholds
                ),

            "qualifying_threshold_count":
                len(
                    qualifying_rows
                ),

            "selected_tau_cal":
                float(
                    selected[
                        "threshold"
                    ]
                ),

            "selected_balanced_accuracy":
                float(
                    selected[
                        "balanced_accuracy"
                    ]
                ),

            "selected_severe_recall":
                float(
                    selected[
                        "severe_recall"
                    ]
                ),

            "selected_severe_precision":
                float(
                    selected[
                        "severe_precision"
                    ]
                ),

            "selected_nonsevere_specificity":
                float(
                    selected[
                        "nonsevere_specificity"
                    ]
                ),

            "selected_flagged_fraction":
                float(
                    selected[
                        "flagged_fraction"
                    ]
                ),

            "selected_tp":
                int(
                    selected[
                        "tp"
                    ]
                ),

            "selected_fp":
                int(
                    selected[
                        "fp"
                    ]
                ),

            "selected_fn":
                int(
                    selected[
                        "fn"
                    ]
                ),

            "selected_tn":
                int(
                    selected[
                        "tn"
                    ]
                ),
        }
    ]

    save_csv(
        SUMMARY_OUTPUT_PATH,
        summary_rows,
    )

    save_csv(
        PREDICTION_OUTPUT_PATH,
        prediction_rows,
    )

    save_csv(
        THRESHOLD_OUTPUT_PATH,
        threshold_rows,
    )

    print()

    print(
        "FROZEN INTERPRETATION"
    )

    print(
        "The selected tau_cal was determined exclusively "
        "from leave-one-generation-seed-out predictions on "
        "historical seeds 44001-44090."
    )

    print(
        "No Experiment 101 prospective seed "
        "44091-44110 has been evaluated."
    )

    print(
        "This selected threshold must be recorded and "
        "committed before prospective controller execution."
    )

    print(
        "=" * 210
    )

    print(
        f"Summary saved to: "
        f"{SUMMARY_OUTPUT_PATH}"
    )

    print(
        f"OOF predictions saved to: "
        f"{PREDICTION_OUTPUT_PATH}"
    )

    print(
        f"Threshold sweep saved to: "
        f"{THRESHOLD_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()