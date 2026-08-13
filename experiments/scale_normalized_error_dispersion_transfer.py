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
    "scale_normalized_error_dispersion_transfer.csv"
)

THRESHOLD_OUTPUT_PATH = Path(
    "results/"
    "scale_normalized_error_dispersion_transfer_thresholds.csv"
)

PREDICTION_OUTPUT_PATH = Path(
    "results/"
    "scale_normalized_error_dispersion_transfer_predictions.csv"
)


BLOCKS = [
    "block_071_090",
    "block_091_110",
]

RAW_FEATURE = "local_error_std"

MINIMUM_HARMFUL_RECALL = 0.80

FLOAT_TOLERANCE = 1e-12


REPRESENTATIONS = [
    "raw",
    "zscore",
    "robust_z",
    "percentile",
]


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
            RAW_FEATURE
        ] = float(
            copy[
                RAW_FEATURE
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


def training_reference(
    rows,
):
    values = sorted(
        float(
            row[
                RAW_FEATURE
            ]
        )
        for row in rows
    )

    mean = statistics.mean(
        values
    )

    std = statistics.pstdev(
        values
    )

    median = statistics.median(
        values
    )

    absolute_deviations = [
        abs(
            value
            - median
        )
        for value in values
    ]

    mad = statistics.median(
        absolute_deviations
    )

    return {
        "values":
            values,

        "mean":
            mean,

        "std":
            std,

        "median":
            median,

        "mad":
            mad,
    }


def empirical_percentile(
    value,
    reference_values,
):
    if not reference_values:
        return float(
            "nan"
        )

    less = sum(
        int(
            candidate
            < value
        )
        for candidate in reference_values
    )

    equal = sum(
        int(
            abs(
                candidate
                - value
            )
            <= FLOAT_TOLERANCE
        )
        for candidate in reference_values
    )

    return (
        less
        + 0.5
        * equal
    ) / len(
        reference_values
    )


def transform_value(
    value,
    representation,
    reference,
):
    if representation == "raw":
        return value

    if representation == "zscore":
        if reference[
            "std"
        ] <= FLOAT_TOLERANCE:
            return 0.0

        return (
            value
            - reference[
                "mean"
            ]
        ) / reference[
            "std"
        ]

    if representation == "robust_z":
        mad = reference[
            "mad"
        ]

        if mad <= FLOAT_TOLERANCE:
            return 0.0

        return (
            value
            - reference[
                "median"
            ]
        ) / (
            1.4826
            * mad
        )

    if representation == "percentile":
        return empirical_percentile(
            value,
            reference[
                "values"
            ],
        )

    raise ValueError(
        f"Unknown representation: "
        f"{representation}"
    )


def transform_rows(
    rows,
    representation,
    reference,
):
    output = []

    for row in rows:
        copy = dict(
            row
        )

        copy[
            "transformed_value"
        ] = transform_value(
            float(
                row[
                    RAW_FEATURE
                ]
            ),
            representation,
            reference,
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
                    "transformed_value"
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

    specificity = (
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
            + specificity
        )
        / 2.0
        if (
            math.isfinite(
                harmful_recall
            )
            and math.isfinite(
                specificity
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

    return {
        "threshold":
            float(
                threshold
            ),

        "harmful_recall":
            harmful_recall,

        "harmful_precision":
            harmful_precision,

        "beneficial_specificity":
            specificity,

        "balanced_accuracy":
            balanced_accuracy,

        "flagged":
            flagged,

        "flagged_fraction":
            (
                flagged
                / len(
                    rows
                )
                if rows
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


def choose_threshold(
    rows,
):
    thresholds = sorted(
        {
            float(
                row[
                    "transformed_value"
                ]
            )
            for row in rows
        }
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
            "No threshold satisfies "
            "the harmful-recall constraint."
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


def evaluate_transfer(
    rows,
    representation,
    training_block,
    test_block,
):
    training_raw = [
        row
        for row in rows
        if row[
            "block"
        ]
        == training_block
    ]

    test_raw = [
        row
        for row in rows
        if row[
            "block"
        ]
        == test_block
    ]

    reference = training_reference(
        training_raw
    )

    training_rows = transform_rows(
        training_raw,
        representation,
        reference,
    )

    test_rows = transform_rows(
        test_raw,
        representation,
        reference,
    )

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
            "representation"
        ] = representation

        row[
            "transfer"
        ] = transfer_name

        row[
            "training_block"
        ] = training_block

        row[
            "test_block"
        ] = test_block

    prediction_rows = []

    for row in test_rows:
        prediction_rows.append(
            {
                "representation":
                    representation,

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

                "raw_local_error_std":
                    float(
                        row[
                            RAW_FEATURE
                        ]
                    ),

                "transformed_value":
                    float(
                        row[
                            "transformed_value"
                        ]
                    ),

                "selected_threshold":
                    float(
                        selected[
                            "threshold"
                        ]
                    ),

                "predicted_harmful":
                    int(
                        float(
                            row[
                                "transformed_value"
                            ]
                        )
                        >= float(
                            selected[
                                "threshold"
                            ]
                        )
                    ),
            }
        )

    return {
        "representation":
            representation,

        "transfer":
            transfer_name,

        "training_block":
            training_block,

        "test_block":
            test_block,

        "selected_threshold":
            float(
                selected[
                    "threshold"
                ]
            ),

        "training_harmful_recall":
            float(
                selected[
                    "harmful_recall"
                ]
            ),

        "training_specificity":
            float(
                selected[
                    "beneficial_specificity"
                ]
            ),

        "training_precision":
            float(
                selected[
                    "harmful_precision"
                ]
            ),

        "training_balanced_accuracy":
            float(
                selected[
                    "balanced_accuracy"
                ]
            ),

        "test_harmful_recall":
            float(
                transferred[
                    "harmful_recall"
                ]
            ),

        "test_specificity":
            float(
                transferred[
                    "beneficial_specificity"
                ]
            ),

        "test_precision":
            float(
                transferred[
                    "harmful_precision"
                ]
            ),

        "test_balanced_accuracy":
            float(
                transferred[
                    "balanced_accuracy"
                ]
            ),

        "test_flagged_fraction":
            float(
                transferred[
                    "flagged_fraction"
                ]
            ),

        "test_tp":
            int(
                transferred[
                    "tp"
                ]
            ),

        "test_fp":
            int(
                transferred[
                    "fp"
                ]
            ),

        "test_fn":
            int(
                transferred[
                    "fn"
                ]
            ),

        "test_tn":
            int(
                transferred[
                    "tn"
                ]
            ),

        "reference_mean":
            float(
                reference[
                    "mean"
                ]
            ),

        "reference_std":
            float(
                reference[
                    "std"
                ]
            ),

        "reference_median":
            float(
                reference[
                    "median"
                ]
            ),

        "reference_mad":
            float(
                reference[
                    "mad"
                ]
            ),
    }, threshold_rows, prediction_rows


def summarize_representation(
    transfer_rows,
    representation,
):
    rows = [
        row
        for row in transfer_rows
        if row[
            "representation"
        ]
        == representation
    ]

    thresholds = [
        float(
            row[
                "selected_threshold"
            ]
        )
        for row in rows
    ]

    recalls = [
        float(
            row[
                "test_harmful_recall"
            ]
        )
        for row in rows
    ]

    specificities = [
        float(
            row[
                "test_specificity"
            ]
        )
        for row in rows
    ]

    balanced = [
        float(
            row[
                "test_balanced_accuracy"
            ]
        )
        for row in rows
    ]

    return {
        "record_type":
            "representation_summary",

        "representation":
            representation,

        "directions":
            len(
                rows
            ),

        "mean_selected_threshold":
            statistics.mean(
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
                recalls
            ),

        "min_test_harmful_recall":
            min(
                recalls
            ),

        "mean_test_specificity":
            statistics.mean(
                specificities
            ),

        "min_test_specificity":
            min(
                specificities
            ),

        "mean_test_balanced_accuracy":
            statistics.mean(
                balanced
            ),

        "min_test_balanced_accuracy":
            min(
                balanced
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
    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "SCALE-NORMALIZED ERROR-DISPERSION TRANSFER"
    )

    print(
        "=" * 210
    )

    print(
        f"input="
        f"{INPUT_PATH}"
    )

    print(
        f"representations="
        f"{REPRESENTATIONS}"
    )

    print(
        f"minimum harmful recall="
        f"{MINIMUM_HARMFUL_RECALL:.3%}"
    )

    print()

    rows = read_events()

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

    transfer_rows = []
    threshold_rows = []
    prediction_rows = []

    for representation in REPRESENTATIONS:
        print()

        print(
            f"REPRESENTATION: "
            f"{representation}"
        )

        for (
            training_block,
            test_block,
        ) in transfer_pairs:

            (
                summary,
                transfer_threshold_rows,
                transfer_prediction_rows,
            ) = evaluate_transfer(
                rows,
                representation,
                training_block,
                test_block,
            )

            transfer_rows.append(
                summary
            )

            threshold_rows.extend(
                transfer_threshold_rows
            )

            prediction_rows.extend(
                transfer_prediction_rows
            )

            print(
                f"{summary['transfer']}"
            )

            print(
                f"  selected threshold="
                f"{summary['selected_threshold']:.12f}"
            )

            print(
                f"  training recall="
                f"{summary['training_harmful_recall']:.3%} "
                f"specificity="
                f"{summary['training_specificity']:.3%} "
                f"balanced="
                f"{summary['training_balanced_accuracy']:.3%}"
            )

            print(
                f"  TEST recall="
                f"{summary['test_harmful_recall']:.3%} "
                f"specificity="
                f"{summary['test_specificity']:.3%} "
                f"precision="
                f"{summary['test_precision']:.3%} "
                f"balanced="
                f"{summary['test_balanced_accuracy']:.3%}"
            )

            print(
                f"  TEST TP="
                f"{summary['test_tp']} "
                f"FP="
                f"{summary['test_fp']} "
                f"FN="
                f"{summary['test_fn']} "
                f"TN="
                f"{summary['test_tn']}"
            )

    representation_summaries = [
        summarize_representation(
            transfer_rows,
            representation,
        )
        for representation in REPRESENTATIONS
    ]

    representation_summaries.sort(
        key=lambda row: (
            float(
                row[
                    "min_test_harmful_recall"
                ]
            ),
            float(
                row[
                    "mean_test_balanced_accuracy"
                ]
            ),
            float(
                row[
                    "mean_test_specificity"
                ]
            ),
        ),
        reverse=True,
    )

    print()

    print(
        "REPRESENTATION TRANSFER SUMMARY"
    )

    for row in representation_summaries:
        print(
            f"{row['representation']:<14} "
            f"threshold_diff="
            f"{row['threshold_absolute_difference']:.6f} "
            f"mean_recall="
            f"{row['mean_test_harmful_recall']:.3%} "
            f"min_recall="
            f"{row['min_test_harmful_recall']:.3%} "
            f"mean_specificity="
            f"{row['mean_test_specificity']:.3%} "
            f"min_specificity="
            f"{row['min_test_specificity']:.3%} "
            f"mean_balanced="
            f"{row['mean_test_balanced_accuracy']:.3%} "
            f"min_balanced="
            f"{row['min_test_balanced_accuracy']:.3%}"
        )

    best = representation_summaries[
        0
    ]

    print()

    print(
        "BEST HISTORICAL TRANSFER REPRESENTATION"
    )

    print(
        f"name="
        f"{best['representation']}"
    )

    print(
        f"minimum transferred harmful recall="
        f"{best['min_test_harmful_recall']:.3%}"
    )

    print(
        f"mean transferred harmful recall="
        f"{best['mean_test_harmful_recall']:.3%}"
    )

    print(
        f"mean transferred specificity="
        f"{best['mean_test_specificity']:.3%}"
    )

    print(
        f"mean transferred balanced accuracy="
        f"{best['mean_test_balanced_accuracy']:.3%}"
    )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "All normalization parameters are fit exclusively "
        "from the training block and then applied unchanged "
        "to the opposite block."
    )

    print(
        "The experiment tests representation transfer only. "
        "No normalized threshold is authorized for controller use."
    )

    print(
        "A normalization method is useful only if it improves "
        "cross-block operating-point behavior rather than merely "
        "renaming the same raw ordering."
    )

    print(
        "No new prospective seed or controller intervention "
        "is introduced."
    )

    print(
        "=" * 210
    )

    summary_rows = []

    summary_rows.extend(
        representation_summaries
    )

    for row in transfer_rows:
        copy = {
            "record_type":
                "transfer"
        }

        copy.update(
            row
        )

        summary_rows.append(
            copy
        )

    save_csv(
        SUMMARY_OUTPUT_PATH,
        summary_rows,
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
        f"Threshold sweeps saved to: "
        f"{THRESHOLD_OUTPUT_PATH}"
    )

    print(
        f"Transferred predictions saved to: "
        f"{PREDICTION_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()