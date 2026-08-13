import csv
import math
import statistics
from pathlib import Path


INPUT_PATH = Path(
    "results/"
    "cross_block_constituent_stability_analysis_events.csv"
)

SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "block_to_block_error_dispersion_operating_point_transfer.csv"
)

THRESHOLD_OUTPUT_PATH = Path(
    "results/"
    "block_to_block_error_dispersion_operating_point_transfer_thresholds.csv"
)

PREDICTION_OUTPUT_PATH = Path(
    "results/"
    "block_to_block_error_dispersion_operating_point_transfer_predictions.csv"
)


BLOCKS = [
    "block_071_090",
    "block_091_110",
]

FEATURE = "local_error_std"

MINIMUM_HARMFUL_RECALL = 0.80

FLOAT_TOLERANCE = 1e-12


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

        copy[
            FEATURE
        ] = float(
            copy[
                FEATURE
            ]
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


def confusion_counts(
    rows,
    threshold,
):
    tp = 0
    fp = 0
    fn = 0
    tn = 0

    for row in rows:
        target = int(
            row[
                "harmful_target"
            ]
        )

        prediction = int(
            float(
                row[
                    FEATURE
                ]
            )
            >= threshold
        )

        if (
            target == 1
            and prediction == 1
        ):
            tp += 1

        elif (
            target == 0
            and prediction == 1
        ):
            fp += 1

        elif (
            target == 1
            and prediction == 0
        ):
            fn += 1

        else:
            tn += 1

    return (
        tp,
        fp,
        fn,
        tn,
    )


def evaluate_threshold(
    rows,
    threshold,
):
    (
        tp,
        fp,
        fn,
        tn,
    ) = confusion_counts(
        rows,
        threshold,
    )

    harmful_total = (
        tp
        + fn
    )

    beneficial_total = (
        tn
        + fp
    )

    harmful_recall = (
        tp
        / harmful_total
        if harmful_total
        > 0
        else float(
            "nan"
        )
    )

    harmful_precision = (
        tp
        / (
            tp
            + fp
        )
        if (
            tp
            + fp
        )
        > 0
        else 0.0
    )

    beneficial_specificity = (
        tn
        / beneficial_total
        if beneficial_total
        > 0
        else float(
            "nan"
        )
    )

    balanced_accuracy = (
        (
            harmful_recall
            + beneficial_specificity
        )
        / 2.0
        if (
            math.isfinite(
                harmful_recall
            )
            and math.isfinite(
                beneficial_specificity
            )
        )
        else float(
            "nan"
        )
    )

    flagged = (
        tp
        + fp
    )

    total = len(
        rows
    )

    return {
        "threshold":
            float(
                threshold
            ),

        "rows":
            total,

        "harmful":
            harmful_total,

        "beneficial":
            beneficial_total,

        "harmful_recall":
            harmful_recall,

        "harmful_precision":
            harmful_precision,

        "beneficial_specificity":
            beneficial_specificity,

        "balanced_accuracy":
            balanced_accuracy,

        "flagged":
            flagged,

        "flagged_fraction":
            (
                flagged
                / total
                if total
                > 0
                else float(
                    "nan"
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


def candidate_thresholds(
    rows,
):
    values = sorted(
        {
            float(
                row[
                    FEATURE
                ]
            )
            for row in rows
        }
    )

    return values


def choose_threshold(
    rows,
):
    thresholds = candidate_thresholds(
        rows
    )

    evaluations = [
        evaluate_threshold(
            rows,
            threshold,
        )
        for threshold in thresholds
    ]

    qualifying = [
        row
        for row in evaluations
        if (
            math.isfinite(
                row[
                    "harmful_recall"
                ]
            )
            and row[
                "harmful_recall"
            ]
            >= (
                MINIMUM_HARMFUL_RECALL
                - FLOAT_TOLERANCE
            )
        )
    ]

    if not qualifying:
        raise RuntimeError(
            "No threshold satisfies the "
            "minimum harmful-recall constraint."
        )

    selected = max(
        qualifying,
        key=lambda row: (
            row[
                "beneficial_specificity"
            ],
            row[
                "harmful_precision"
            ],
            row[
                "threshold"
            ],
        ),
    )

    for row in evaluations:
        row[
            "qualifies_recall_constraint"
        ] = int(
            row
            in qualifying
        )

        row[
            "selected_threshold"
        ] = int(
            abs(
                row[
                    "threshold"
                ]
                - selected[
                    "threshold"
                ]
            )
            <= FLOAT_TOLERANCE
        )

    return (
        selected,
        evaluations,
    )


def transfer_direction(
    rows,
    training_block,
    test_block,
):
    training_rows = [
        row
        for row in rows
        if row[
            "block"
        ]
        == training_block
    ]

    test_rows = [
        row
        for row in rows
        if row[
            "block"
        ]
        == test_block
    ]

    (
        selected,
        threshold_rows,
    ) = choose_threshold(
        training_rows
    )

    transferred = evaluate_threshold(
        test_rows,
        selected[
            "threshold"
        ],
    )

    transfer_name = (
        f"{training_block}"
        f"_to_"
        f"{test_block}"
    )

    for row in threshold_rows:
        row[
            "transfer"
        ] = transfer_name

        row[
            "training_block"
        ] = training_block

        row[
            "test_block"
        ] = test_block

    summary = {
        "transfer":
            transfer_name,

        "training_block":
            training_block,

        "test_block":
            test_block,

        "selected_threshold":
            selected[
                "threshold"
            ],

        "training_rows":
            selected[
                "rows"
            ],

        "training_harmful":
            selected[
                "harmful"
            ],

        "training_beneficial":
            selected[
                "beneficial"
            ],

        "training_harmful_recall":
            selected[
                "harmful_recall"
            ],

        "training_harmful_precision":
            selected[
                "harmful_precision"
            ],

        "training_beneficial_specificity":
            selected[
                "beneficial_specificity"
            ],

        "training_balanced_accuracy":
            selected[
                "balanced_accuracy"
            ],

        "training_flagged_fraction":
            selected[
                "flagged_fraction"
            ],

        "test_rows":
            transferred[
                "rows"
            ],

        "test_harmful":
            transferred[
                "harmful"
            ],

        "test_beneficial":
            transferred[
                "beneficial"
            ],

        "test_harmful_recall":
            transferred[
                "harmful_recall"
            ],

        "test_harmful_precision":
            transferred[
                "harmful_precision"
            ],

        "test_beneficial_specificity":
            transferred[
                "beneficial_specificity"
            ],

        "test_balanced_accuracy":
            transferred[
                "balanced_accuracy"
            ],

        "test_flagged_fraction":
            transferred[
                "flagged_fraction"
            ],

        "test_tp":
            transferred[
                "tp"
            ],

        "test_fp":
            transferred[
                "fp"
            ],

        "test_fn":
            transferred[
                "fn"
            ],

        "test_tn":
            transferred[
                "tn"
            ],
    }

    prediction_rows = []

    for row in test_rows:
        value = float(
            row[
                FEATURE
            ]
        )

        prediction_rows.append(
            {
                "transfer":
                    transfer_name,

                "training_block":
                    training_block,

                "test_block":
                    test_block,

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

                FEATURE:
                    value,

                "selected_threshold":
                    selected[
                        "threshold"
                    ],

                "predicted_harmful":
                    int(
                        value
                        >= selected[
                            "threshold"
                        ]
                    ),
            }
        )

    return (
        summary,
        threshold_rows,
        prediction_rows,
    )


def transfer_stability_summary(
    summaries,
):
    thresholds = [
        float(
            row[
                "selected_threshold"
            ]
        )
        for row in summaries
    ]

    test_recalls = [
        float(
            row[
                "test_harmful_recall"
            ]
        )
        for row in summaries
    ]

    test_specificities = [
        float(
            row[
                "test_beneficial_specificity"
            ]
        )
        for row in summaries
    ]

    test_balanced = [
        float(
            row[
                "test_balanced_accuracy"
            ]
        )
        for row in summaries
    ]

    return {
        "record_type":
            "transfer_stability",

        "directions":
            len(
                summaries
            ),

        "threshold_mean":
            statistics.mean(
                thresholds
            ),

        "threshold_min":
            min(
                thresholds
            ),

        "threshold_max":
            max(
                thresholds
            ),

        "threshold_absolute_difference":
            (
                abs(
                    thresholds[
                        0
                    ]
                    - thresholds[
                        1
                    ]
                )
                if len(
                    thresholds
                )
                == 2
                else float(
                    "nan"
                )
            ),

        "mean_test_harmful_recall":
            statistics.mean(
                test_recalls
            ),

        "min_test_harmful_recall":
            min(
                test_recalls
            ),

        "mean_test_beneficial_specificity":
            statistics.mean(
                test_specificities
            ),

        "min_test_beneficial_specificity":
            min(
                test_specificities
            ),

        "mean_test_balanced_accuracy":
            statistics.mean(
                test_balanced
            ),

        "min_test_balanced_accuracy":
            min(
                test_balanced
            ),
    }


def sensitivity_rows(
    rows,
    selected_threshold,
    transfer_name,
    test_block,
):
    values = sorted(
        {
            float(
                row[
                    FEATURE
                ]
            )
            for row in rows
        }
    )

    nearest = sorted(
        values,
        key=lambda value:
            abs(
                value
                - selected_threshold
            ),
    )[
        :7
    ]

    nearest = sorted(
        set(
            nearest
        )
    )

    output = []

    for threshold in nearest:
        metrics = evaluate_threshold(
            rows,
            threshold,
        )

        output.append(
            {
                "record_type":
                    "test_threshold_sensitivity",

                "transfer":
                    transfer_name,

                "test_block":
                    test_block,

                **metrics,
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
        "BLOCK-TO-BLOCK ERROR-DISPERSION "
        "OPERATING-POINT TRANSFER"
    )

    print(
        "=" * 210
    )

    print(
        f"input="
        f"{INPUT_PATH}"
    )

    print(
        f"feature="
        f"{FEATURE}"
    )

    print(
        f"minimum training harmful recall="
        f"{MINIMUM_HARMFUL_RECALL:.3%}"
    )

    print()

    rows = read_events()

    summaries = []
    threshold_rows = []
    prediction_rows = []
    sensitivity_output_rows = []

    transfer_pairs = [
        (
            "block_071_090",
            "block_091_110",
        ),
        (
            "block_091_110",
            "block_071_090",
        ),
    ]

    for (
        training_block,
        test_block,
    ) in transfer_pairs:

        (
            summary,
            transfer_threshold_rows,
            transfer_prediction_rows,
        ) = transfer_direction(
            rows,
            training_block,
            test_block,
        )

        summaries.append(
            summary
        )

        threshold_rows.extend(
            transfer_threshold_rows
        )

        prediction_rows.extend(
            transfer_prediction_rows
        )

        test_rows = [
            row
            for row in rows
            if row[
                "block"
            ]
            == test_block
        ]

        sensitivity_output_rows.extend(
            sensitivity_rows(
                test_rows,
                summary[
                    "selected_threshold"
                ],
                summary[
                    "transfer"
                ],
                test_block,
            )
        )

    stability = transfer_stability_summary(
        summaries
    )

    print(
        "BLOCK-TO-BLOCK OPERATING-POINT TRANSFER"
    )

    for row in summaries:
        print()

        print(
            row[
                "transfer"
            ]
        )

        print(
            f"  selected threshold="
            f"{row['selected_threshold']:.12f}"
        )

        print(
            f"  training harmful="
            f"{row['training_harmful']} "
            f"beneficial="
            f"{row['training_beneficial']}"
        )

        print(
            f"  training recall="
            f"{row['training_harmful_recall']:.3%} "
            f"specificity="
            f"{row['training_beneficial_specificity']:.3%} "
            f"precision="
            f"{row['training_harmful_precision']:.3%} "
            f"balanced="
            f"{row['training_balanced_accuracy']:.3%} "
            f"flagged="
            f"{row['training_flagged_fraction']:.3%}"
        )

        print(
            f"  TEST harmful="
            f"{row['test_harmful']} "
            f"beneficial="
            f"{row['test_beneficial']}"
        )

        print(
            f"  TEST recall="
            f"{row['test_harmful_recall']:.3%} "
            f"specificity="
            f"{row['test_beneficial_specificity']:.3%} "
            f"precision="
            f"{row['test_harmful_precision']:.3%} "
            f"balanced="
            f"{row['test_balanced_accuracy']:.3%} "
            f"flagged="
            f"{row['test_flagged_fraction']:.3%}"
        )

        print(
            f"  TEST TP="
            f"{row['test_tp']} "
            f"FP="
            f"{row['test_fp']} "
            f"FN="
            f"{row['test_fn']} "
            f"TN="
            f"{row['test_tn']}"
        )

    print()

    print(
        "THRESHOLD TRANSFER STABILITY"
    )

    print(
        f"threshold mean="
        f"{stability['threshold_mean']:.12f}"
    )

    print(
        f"threshold range=["
        f"{stability['threshold_min']:.12f},"
        f"{stability['threshold_max']:.12f}"
        f"]"
    )

    print(
        f"absolute threshold difference="
        f"{stability['threshold_absolute_difference']:.12f}"
    )

    print(
        f"mean transferred harmful recall="
        f"{stability['mean_test_harmful_recall']:.3%}"
    )

    print(
        f"minimum transferred harmful recall="
        f"{stability['min_test_harmful_recall']:.3%}"
    )

    print(
        f"mean transferred specificity="
        f"{stability['mean_test_beneficial_specificity']:.3%}"
    )

    print(
        f"minimum transferred specificity="
        f"{stability['min_test_beneficial_specificity']:.3%}"
    )

    print(
        f"mean transferred balanced accuracy="
        f"{stability['mean_test_balanced_accuracy']:.3%}"
    )

    print(
        f"minimum transferred balanced accuracy="
        f"{stability['min_test_balanced_accuracy']:.3%}"
    )

    print()

    print(
        "TEST-BLOCK LOCAL SENSITIVITY"
    )

    for transfer_name in [
        row[
            "transfer"
        ]
        for row in summaries
    ]:
        print()

        print(
            transfer_name
        )

        matching = [
            row
            for row in sensitivity_output_rows
            if row[
                "transfer"
            ]
            == transfer_name
        ]

        for row in matching:
            print(
                f"  threshold="
                f"{row['threshold']:.12f} "
                f"recall="
                f"{row['harmful_recall']:.3%} "
                f"specificity="
                f"{row['beneficial_specificity']:.3%} "
                f"precision="
                f"{row['harmful_precision']:.3%} "
                f"balanced="
                f"{row['balanced_accuracy']:.3%} "
                f"flagged="
                f"{row['flagged_fraction']:.3%}"
            )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 107 derives each error-dispersion threshold "
        "using only one historical block and evaluates it unchanged "
        "on the other block."
    )

    print(
        "The selected thresholds are historical diagnostic "
        "operating points only. They are not controller thresholds."
    )

    print(
        "No new prospective seed or controller intervention "
        "is introduced."
    )

    print(
        "Given only eight harmful events across both blocks, "
        "threshold transfer must be interpreted conservatively."
    )

    print(
        "=" * 210
    )

    summary_output_rows = []

    for row in summaries:
        copy = {
            "record_type":
                "transfer_summary"
        }

        copy.update(
            row
        )

        summary_output_rows.append(
            copy
        )

    summary_output_rows.append(
        stability
    )

    summary_output_rows.extend(
        sensitivity_output_rows
    )

    save_csv(
        SUMMARY_OUTPUT_PATH,
        summary_output_rows,
    )

    save_csv(
        THRESHOLD_OUTPUT_PATH,
        threshold_rows,
    )

    save_csv(
        PREDICTION_OUTPUT_PATH,
        prediction_rows,
    )

    print(
        f"Summary saved to: "
        f"{SUMMARY_OUTPUT_PATH}"
    )

    print(
        f"Training threshold sweeps saved to: "
        f"{THRESHOLD_OUTPUT_PATH}"
    )

    print(
        f"Transferred predictions saved to: "
        f"{PREDICTION_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()