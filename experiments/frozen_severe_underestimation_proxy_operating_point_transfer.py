import csv
import math
import statistics
from pathlib import Path


INPUT_PATH = Path(
    "results/"
    "frozen_pre_action_calibration_proxy_support_expansion_transfer_events.csv"
)

SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "frozen_severe_underestimation_proxy_operating_point_transfer.csv"
)

THRESHOLD_OUTPUT_PATH = Path(
    "results/"
    "frozen_severe_underestimation_proxy_operating_point_transfer_thresholds.csv"
)

PREDICTION_OUTPUT_PATH = Path(
    "results/"
    "frozen_severe_underestimation_proxy_operating_point_transfer_predictions.csv"
)


BLOCKS = [
    "block_071_090",
    "block_091_110",
]

MODEL_NAME = "severe_proxy_only"

FEATURE = "severe_underestimation_probability"

MINIMUM_HARMFUL_RECALL = 0.80

FLOAT_TOLERANCE = 1e-12


# Experiment 107 historical benchmark.
ERROR_STD_BENCHMARK = {
    "mean_transferred_harmful_recall":
        0.75,

    "minimum_transferred_harmful_recall":
        0.50,

    "mean_transferred_specificity":
        0.70773,

    "minimum_transferred_specificity":
        0.60465,

    "mean_transferred_balanced_accuracy":
        0.72887,

    "minimum_transferred_balanced_accuracy":
        0.65541,
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
        if row.get(
            "model",
            "",
        ) != MODEL_NAME:
            continue

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
                "harmful_target"
            ]
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
            specificity,

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
    return sorted(
        {
            float(
                row[
                    FEATURE
                ]
            )
            for row in rows
        }
    )


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
            "No threshold satisfies "
            "the minimum harmful-recall constraint."
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
            "held_out_block"
        ]
        == training_block
    ]

    test_rows = [
        row
        for row in rows
        if row[
            "held_out_block"
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
        "record_type":
            "transfer_summary",

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
                        "true_class"
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

    recalls = [
        float(
            row[
                "test_harmful_recall"
            ]
        )
        for row in summaries
    ]

    specificities = [
        float(
            row[
                "test_beneficial_specificity"
            ]
        )
        for row in summaries
    ]

    balanced = [
        float(
            row[
                "test_balanced_accuracy"
            ]
        )
        for row in summaries
    ]

    flagged = [
        float(
            row[
                "test_flagged_fraction"
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
                recalls
            ),

        "minimum_test_harmful_recall":
            min(
                recalls
            ),

        "mean_test_specificity":
            statistics.mean(
                specificities
            ),

        "minimum_test_specificity":
            min(
                specificities
            ),

        "mean_test_balanced_accuracy":
            statistics.mean(
                balanced
            ),

        "minimum_test_balanced_accuracy":
            min(
                balanced
            ),

        "mean_test_flagged_fraction":
            statistics.mean(
                flagged
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
        :9
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


def benchmark_comparison(
    stability,
):
    return {
        "record_type":
            "experiment_107_benchmark_comparison",

        "proxy_mean_recall":
            stability[
                "mean_test_harmful_recall"
            ],

        "error_std_mean_recall":
            ERROR_STD_BENCHMARK[
                "mean_transferred_harmful_recall"
            ],

        "delta_mean_recall":
            (
                stability[
                    "mean_test_harmful_recall"
                ]
                - ERROR_STD_BENCHMARK[
                    "mean_transferred_harmful_recall"
                ]
            ),

        "proxy_minimum_recall":
            stability[
                "minimum_test_harmful_recall"
            ],

        "error_std_minimum_recall":
            ERROR_STD_BENCHMARK[
                "minimum_transferred_harmful_recall"
            ],

        "delta_minimum_recall":
            (
                stability[
                    "minimum_test_harmful_recall"
                ]
                - ERROR_STD_BENCHMARK[
                    "minimum_transferred_harmful_recall"
                ]
            ),

        "proxy_mean_specificity":
            stability[
                "mean_test_specificity"
            ],

        "error_std_mean_specificity":
            ERROR_STD_BENCHMARK[
                "mean_transferred_specificity"
            ],

        "delta_mean_specificity":
            (
                stability[
                    "mean_test_specificity"
                ]
                - ERROR_STD_BENCHMARK[
                    "mean_transferred_specificity"
                ]
            ),

        "proxy_mean_balanced_accuracy":
            stability[
                "mean_test_balanced_accuracy"
            ],

        "error_std_mean_balanced_accuracy":
            ERROR_STD_BENCHMARK[
                "mean_transferred_balanced_accuracy"
            ],

        "delta_mean_balanced_accuracy":
            (
                stability[
                    "mean_test_balanced_accuracy"
                ]
                - ERROR_STD_BENCHMARK[
                    "mean_transferred_balanced_accuracy"
                ]
            ),

        "proxy_minimum_balanced_accuracy":
            stability[
                "minimum_test_balanced_accuracy"
            ],

        "error_std_minimum_balanced_accuracy":
            ERROR_STD_BENCHMARK[
                "minimum_transferred_balanced_accuracy"
            ],

        "delta_minimum_balanced_accuracy":
            (
                stability[
                    "minimum_test_balanced_accuracy"
                ]
                - ERROR_STD_BENCHMARK[
                    "minimum_transferred_balanced_accuracy"
                ]
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
        "FROZEN SEVERE-UNDERESTIMATION PROXY "
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
        f"model="
        f"{MODEL_NAME}"
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

    print(
        "EVENT POPULATION"
    )

    print(
        f"rows="
        f"{len(rows)}"
    )

    print(
        f"harmful="
        f"{sum(row['harmful_target'] for row in rows)}"
    )

    print(
        f"beneficial="
        f"{sum(1 - row['harmful_target'] for row in rows)}"
    )

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

    summaries = []
    threshold_rows = []
    prediction_rows = []
    sensitivity_output_rows = []

    for (
        training_block,
        test_block,
    ) in transfer_pairs:

        (
            summary,
            local_threshold_rows,
            local_prediction_rows,
        ) = transfer_direction(
            rows,
            training_block,
            test_block,
        )

        summaries.append(
            summary
        )

        threshold_rows.extend(
            local_threshold_rows
        )

        prediction_rows.extend(
            local_prediction_rows
        )

        test_rows = [
            row
            for row in rows
            if row[
                "held_out_block"
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

    benchmark = benchmark_comparison(
        stability
    )

    print()

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
        "TRANSFER STABILITY"
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
        f"threshold absolute difference="
        f"{stability['threshold_absolute_difference']:.12f}"
    )

    print(
        f"mean transferred harmful recall="
        f"{stability['mean_test_harmful_recall']:.3%}"
    )

    print(
        f"minimum transferred harmful recall="
        f"{stability['minimum_test_harmful_recall']:.3%}"
    )

    print(
        f"mean transferred specificity="
        f"{stability['mean_test_specificity']:.3%}"
    )

    print(
        f"minimum transferred specificity="
        f"{stability['minimum_test_specificity']:.3%}"
    )

    print(
        f"mean transferred balanced accuracy="
        f"{stability['mean_test_balanced_accuracy']:.3%}"
    )

    print(
        f"minimum transferred balanced accuracy="
        f"{stability['minimum_test_balanced_accuracy']:.3%}"
    )

    print(
        f"mean transferred flagged fraction="
        f"{stability['mean_test_flagged_fraction']:.3%}"
    )

    print()

    print(
        "EXPERIMENT 107 ERROR-DISPERSION BENCHMARK"
    )

    print(
        f"dMeanRecall="
        f"{benchmark['delta_mean_recall']:+.3%}"
    )

    print(
        f"dMinimumRecall="
        f"{benchmark['delta_minimum_recall']:+.3%}"
    )

    print(
        f"dMeanSpecificity="
        f"{benchmark['delta_mean_specificity']:+.3%}"
    )

    print(
        f"dMeanBalancedAccuracy="
        f"{benchmark['delta_mean_balanced_accuracy']:+.3%}"
    )

    print(
        f"dMinimumBalancedAccuracy="
        f"{benchmark['delta_minimum_balanced_accuracy']:+.3%}"
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
        "Experiment 112 applies the same safety-oriented "
        "historical threshold-selection rule used in Experiment 107."
    )

    print(
        "Each threshold is selected using only one historical "
        "support-expansion block and is evaluated unchanged on the "
        "opposite block."
    )

    print(
        "The severe-underestimation probability itself was frozen "
        "from Experiment 110 before this operating-point experiment."
    )

    print(
        "No new prospective seed or controller intervention "
        "is introduced."
    )

    print(
        "Given only eight harmful support expansions, even improved "
        "transfer must remain provisional."
    )

    print(
        "=" * 210
    )

    summary_output_rows = []

    summary_output_rows.extend(
        summaries
    )

    summary_output_rows.append(
        stability
    )

    summary_output_rows.append(
        benchmark
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
        f"Threshold sweeps saved to: "
        f"{THRESHOLD_OUTPUT_PATH}"
    )

    print(
        f"Transferred predictions saved to: "
        f"{PREDICTION_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()