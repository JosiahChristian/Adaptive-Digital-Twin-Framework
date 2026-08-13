import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

import numpy as np


EVENT_INPUT_PATH = Path(
    "results/"
    "pre_action_consequence_underestimation_risk_analysis_events.csv"
)

OUTPUT_PATH = Path(
    "results/"
    "loss_ceiling_threshold_geometry_analysis.csv"
)

SEED_OUTPUT_PATH = Path(
    "results/"
    "loss_ceiling_threshold_geometry_analysis_seeds.csv"
)

QUANTILE_OUTPUT_PATH = Path(
    "results/"
    "loss_ceiling_threshold_geometry_analysis_quantiles.csv"
)


CEILING_FIELD = "predicted_loss_ceiling"

SEVERE_FIELD = "severe_underestimation"

OUTCOME_FIELD = "outcome"

SEED_FIELD = "generation_seed"


THRESHOLD_MIN = 0.10
THRESHOLD_MAX = 0.22
THRESHOLD_STEP = 0.005


UPPER_TAIL_FRACTIONS = [
    0.50,
    0.40,
    0.30,
    0.20,
    0.10,
]


FLOAT_TOLERANCE = 1e-12


def read_events():
    with EVENT_INPUT_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        rows = list(
            csv.DictReader(
                file
            )
        )

    return rows


def build_thresholds():
    count = int(
        round(
            (
                THRESHOLD_MAX
                - THRESHOLD_MIN
            )
            / THRESHOLD_STEP
        )
    )

    return [
        round(
            THRESHOLD_MIN
            + index
            * THRESHOLD_STEP,
            6,
        )
        for index in range(
            count + 1
        )
    ]


def safe_divide(
    numerator,
    denominator,
    default=0.0,
):
    if denominator == 0:
        return default

    return (
        numerator
        / denominator
    )


def evaluate_threshold(
    rows,
    threshold,
):
    severe_total = sum(
        int(
            row[
                SEVERE_FIELD
            ]
        )
        for row in rows
    )

    nonsevere_total = (
        len(
            rows
        )
        - severe_total
    )

    harmful_total = sum(
        int(
            row[
                OUTCOME_FIELD
            ]
            == "harmful"
        )
        for row in rows
    )

    beneficial_total = sum(
        int(
            row[
                OUTCOME_FIELD
            ]
            == "beneficial"
        )
        for row in rows
    )

    flagged_rows = [
        row
        for row in rows
        if float(
            row[
                CEILING_FIELD
            ]
        )
        >= (
            threshold
            - FLOAT_TOLERANCE
        )
    ]

    unflagged_rows = [
        row
        for row in rows
        if float(
            row[
                CEILING_FIELD
            ]
        )
        < (
            threshold
            - FLOAT_TOLERANCE
        )
    ]

    severe_flagged = sum(
        int(
            row[
                SEVERE_FIELD
            ]
        )
        for row in flagged_rows
    )

    nonsevere_flagged = (
        len(
            flagged_rows
        )
        - severe_flagged
    )

    severe_unflagged = sum(
        int(
            row[
                SEVERE_FIELD
            ]
        )
        for row in unflagged_rows
    )

    nonsevere_unflagged = (
        len(
            unflagged_rows
        )
        - severe_unflagged
    )

    harmful_flagged = sum(
        int(
            row[
                OUTCOME_FIELD
            ]
            == "harmful"
        )
        for row in flagged_rows
    )

    beneficial_flagged = sum(
        int(
            row[
                OUTCOME_FIELD
            ]
            == "beneficial"
        )
        for row in flagged_rows
    )

    beneficial_unflagged = (
        beneficial_total
        - beneficial_flagged
    )

    severe_recall = safe_divide(
        severe_flagged,
        severe_total,
    )

    nonsevere_specificity = safe_divide(
        nonsevere_unflagged,
        nonsevere_total,
    )

    severe_precision = safe_divide(
        severe_flagged,
        len(
            flagged_rows
        ),
    )

    flagged_fraction = safe_divide(
        len(
            flagged_rows
        ),
        len(
            rows
        ),
    )

    harmful_recall = safe_divide(
        harmful_flagged,
        harmful_total,
    )

    beneficial_preservation = safe_divide(
        beneficial_unflagged,
        beneficial_total,
        default=1.0,
    )

    balanced_accuracy = (
        severe_recall
        + nonsevere_specificity
    ) / 2.0

    risk_lift = safe_divide(
        severe_precision,
        safe_divide(
            severe_total,
            len(
                rows
            ),
        ),
    )

    return {
        "threshold":
            threshold,

        "events":
            len(
                rows
            ),

        "flagged_events":
            len(
                flagged_rows
            ),

        "flagged_fraction":
            flagged_fraction,

        "severe_total":
            severe_total,

        "severe_flagged":
            severe_flagged,

        "severe_unflagged":
            severe_unflagged,

        "nonsevere_total":
            nonsevere_total,

        "nonsevere_flagged":
            nonsevere_flagged,

        "nonsevere_unflagged":
            nonsevere_unflagged,

        "severe_recall":
            severe_recall,

        "nonsevere_specificity":
            nonsevere_specificity,

        "severe_precision":
            severe_precision,

        "balanced_accuracy":
            balanced_accuracy,

        "risk_lift":
            risk_lift,

        "harmful_total":
            harmful_total,

        "harmful_flagged":
            harmful_flagged,

        "harmful_recall":
            harmful_recall,

        "beneficial_total":
            beneficial_total,

        "beneficial_flagged":
            beneficial_flagged,

        "beneficial_preservation":
            beneficial_preservation,
    }


def evaluate_seed_thresholds(
    rows,
    thresholds,
):
    grouped = defaultdict(
        list
    )

    for row in rows:
        grouped[
            int(
                float(
                    row[
                        SEED_FIELD
                    ]
                )
            )
        ].append(
            row
        )

    output = []

    for seed in sorted(
        grouped
    ):
        seed_rows = grouped[
            seed
        ]

        for threshold in thresholds:
            result = evaluate_threshold(
                seed_rows,
                threshold,
            )

            result[
                "generation_seed"
            ] = seed

            output.append(
                result
            )

    return output


def aggregate_seed_stability(
    seed_rows,
    thresholds,
):
    output = []

    for threshold in thresholds:
        matching = [
            row
            for row in seed_rows
            if abs(
                float(
                    row[
                        "threshold"
                    ]
                )
                - threshold
            )
            <= FLOAT_TOLERANCE
        ]

        severe_seed_rows = [
            row
            for row in matching
            if int(
                row[
                    "severe_total"
                ]
            )
            > 0
        ]

        harmful_seed_rows = [
            row
            for row in matching
            if int(
                row[
                    "harmful_total"
                ]
            )
            > 0
        ]

        beneficial_seed_rows = [
            row
            for row in matching
            if int(
                row[
                    "beneficial_total"
                ]
            )
            > 0
        ]

        def values(
            rows_,
            field,
        ):
            return [
                float(
                    row[
                        field
                    ]
                )
                for row in rows_
            ]

        severe_recall_values = values(
            severe_seed_rows,
            "severe_recall",
        )

        specificity_values = values(
            matching,
            "nonsevere_specificity",
        )

        harmful_recall_values = values(
            harmful_seed_rows,
            "harmful_recall",
        )

        beneficial_preservation_values = values(
            beneficial_seed_rows,
            "beneficial_preservation",
        )

        output.append(
            {
                "threshold":
                    threshold,

                "evaluated_seeds":
                    len(
                        matching
                    ),

                "seeds_with_severe_events":
                    len(
                        severe_seed_rows
                    ),

                "seeds_with_harmful_events":
                    len(
                        harmful_seed_rows
                    ),

                "mean_seed_severe_recall":
                    (
                        statistics.mean(
                            severe_recall_values
                        )
                        if severe_recall_values
                        else float(
                            "nan"
                        )
                    ),

                "min_seed_severe_recall":
                    (
                        min(
                            severe_recall_values
                        )
                        if severe_recall_values
                        else float(
                            "nan"
                        )
                    ),

                "mean_seed_specificity":
                    statistics.mean(
                        specificity_values
                    ),

                "min_seed_specificity":
                    min(
                        specificity_values
                    ),

                "mean_seed_harmful_recall":
                    (
                        statistics.mean(
                            harmful_recall_values
                        )
                        if harmful_recall_values
                        else float(
                            "nan"
                        )
                    ),

                "mean_seed_beneficial_preservation":
                    (
                        statistics.mean(
                            beneficial_preservation_values
                        )
                        if beneficial_preservation_values
                        else float(
                            "nan"
                        )
                    ),

                "seeds_flagging_any_event":
                    sum(
                        int(
                            int(
                                row[
                                    "flagged_events"
                                ]
                            )
                            > 0
                        )
                        for row in matching
                    ),

                "seeds_flagging_all_events":
                    sum(
                        int(
                            int(
                                row[
                                    "flagged_events"
                                ]
                            )
                            == int(
                                row[
                                    "events"
                                ]
                            )
                        )
                        for row in matching
                    ),
            }
        )

    return output


def quantile_threshold(
    values,
    upper_tail_fraction,
):
    quantile = (
        1.0
        - upper_tail_fraction
    )

    return float(
        np.quantile(
            np.asarray(
                values,
                dtype=float,
            ),
            quantile,
        )
    )


def evaluate_quantile_concentration(
    rows,
):
    ceiling_values = [
        float(
            row[
                CEILING_FIELD
            ]
        )
        for row in rows
    ]

    output = []

    for tail_fraction in UPPER_TAIL_FRACTIONS:
        threshold = quantile_threshold(
            ceiling_values,
            tail_fraction,
        )

        result = evaluate_threshold(
            rows,
            threshold,
        )

        result[
            "upper_tail_fraction"
        ] = tail_fraction

        output.append(
            result
        )

    return output


def safe_numeric_mean(
    values,
):
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


def choose_descriptive_thresholds(
    pooled_rows,
):
    ranked_by_balanced = sorted(
        pooled_rows,
        key=lambda row: (
            float(
                row[
                    "balanced_accuracy"
                ]
            ),
            float(
                row[
                    "severe_recall"
                ]
            ),
            -float(
                row[
                    "flagged_fraction"
                ]
            ),
        ),
        reverse=True,
    )

    best_balanced = ranked_by_balanced[
        0
    ]

    recall_80_candidates = [
        row
        for row in pooled_rows
        if float(
            row[
                "severe_recall"
            ]
        )
        >= 0.80
    ]

    best_80_recall = (
        max(
            recall_80_candidates,
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
            ),
        )
        if recall_80_candidates
        else None
    )

    recall_67_candidates = [
        row
        for row in pooled_rows
        if float(
            row[
                "severe_recall"
            ]
        )
        >= (
            2.0
            / 3.0
        )
    ]

    best_67_recall = (
        max(
            recall_67_candidates,
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
            ),
        )
        if recall_67_candidates
        else None
    )

    return (
        best_balanced,
        best_80_recall,
        best_67_recall,
    )


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
    rows = read_events()

    thresholds = build_thresholds()

    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "LOSS-CEILING THRESHOLD GEOMETRY "
        "AND EVENT-CONCENTRATION ANALYSIS"
    )

    print(
        "=" * 210
    )

    print(
        f"input="
        f"{EVENT_INPUT_PATH}"
    )

    print(
        f"events="
        f"{len(rows)}"
    )

    print(
        f"threshold range="
        f"[{THRESHOLD_MIN:.3f}, "
        f"{THRESHOLD_MAX:.3f}]"
    )

    print(
        f"threshold step="
        f"{THRESHOLD_STEP:.3f}"
    )

    print()

    pooled_rows = [
        evaluate_threshold(
            rows,
            threshold,
        )
        for threshold in thresholds
    ]

    seed_rows = evaluate_seed_thresholds(
        rows,
        thresholds,
    )

    seed_stability_rows = aggregate_seed_stability(
        seed_rows,
        thresholds,
    )

    stability_lookup = {
        float(
            row[
                "threshold"
            ]
        ):
            row
        for row in seed_stability_rows
    }

    output_rows = []

    for row in pooled_rows:
        copy = dict(
            row
        )

        stability = stability_lookup[
            float(
                row[
                    "threshold"
                ]
            )
        ]

        for key, value in stability.items():
            if key == "threshold":
                continue

            copy[
                key
            ] = value

        output_rows.append(
            copy
        )

    quantile_rows = evaluate_quantile_concentration(
        rows
    )

    (
        best_balanced,
        best_80_recall,
        best_67_recall,
    ) = choose_descriptive_thresholds(
        pooled_rows
    )

    save_csv(
        OUTPUT_PATH,
        output_rows,
    )

    save_csv(
        SEED_OUTPUT_PATH,
        seed_rows,
    )

    save_csv(
        QUANTILE_OUTPUT_PATH,
        quantile_rows,
    )

    severe_total = sum(
        int(
            row[
                SEVERE_FIELD
            ]
        )
        for row in rows
    )

    harmful_total = sum(
        int(
            row[
                OUTCOME_FIELD
            ]
            == "harmful"
        )
        for row in rows
    )

    beneficial_total = sum(
        int(
            row[
                OUTCOME_FIELD
            ]
            == "beneficial"
        )
        for row in rows
    )

    print(
        "EVENT POPULATION"
    )

    print(
        f"severe_underestimation="
        f"{severe_total}/"
        f"{len(rows)} "
        f"("
        f"{severe_total / len(rows):.3%}"
        f")"
    )

    print(
        f"harmful_expansion="
        f"{harmful_total}/"
        f"{len(rows)} "
        f"("
        f"{harmful_total / len(rows):.3%}"
        f")"
    )

    print(
        f"beneficial_expansion="
        f"{beneficial_total}/"
        f"{len(rows)} "
        f"("
        f"{beneficial_total / len(rows):.3%}"
        f")"
    )

    print()

    print(
        "THRESHOLD SWEEP"
    )

    for row in output_rows:
        print(
            f"threshold="
            f"{row['threshold']:.3f} "
            f"flagged="
            f"{row['flagged_events']}/"
            f"{row['events']} "
            f"("
            f"{row['flagged_fraction']:.3%}"
            f") "
            f"severe_recall="
            f"{row['severe_recall']:.3%} "
            f"specificity="
            f"{row['nonsevere_specificity']:.3%} "
            f"precision="
            f"{row['severe_precision']:.3%} "
            f"balanced="
            f"{row['balanced_accuracy']:.3%} "
            f"lift="
            f"{row['risk_lift']:.3f} "
            f"harmful_recall="
            f"{row['harmful_recall']:.3%} "
            f"beneficial_preservation="
            f"{row['beneficial_preservation']:.3%}"
        )

    print()

    print(
        "UPPER-TAIL CONCENTRATION"
    )

    for row in quantile_rows:
        print(
            f"upper_tail="
            f"{row['upper_tail_fraction']:.0%} "
            f"threshold="
            f"{row['threshold']:.6f} "
            f"flagged="
            f"{row['flagged_fraction']:.3%} "
            f"severe_recall="
            f"{row['severe_recall']:.3%} "
            f"precision="
            f"{row['severe_precision']:.3%} "
            f"lift="
            f"{row['risk_lift']:.3f} "
            f"harmful_recall="
            f"{row['harmful_recall']:.3%} "
            f"beneficial_preservation="
            f"{row['beneficial_preservation']:.3%}"
        )

    print()

    print(
        "DESCRIPTIVE OPERATING POINTS"
    )

    def print_point(
        label,
        row,
    ):
        if row is None:
            print(
                f"{label}: none"
            )
            return

        print(
            f"{label}: "
            f"threshold="
            f"{row['threshold']:.3f} "
            f"balanced="
            f"{row['balanced_accuracy']:.3%} "
            f"severe_recall="
            f"{row['severe_recall']:.3%} "
            f"specificity="
            f"{row['nonsevere_specificity']:.3%} "
            f"precision="
            f"{row['severe_precision']:.3%} "
            f"flagged="
            f"{row['flagged_fraction']:.3%}"
        )

    print_point(
        "best pooled balanced accuracy",
        best_balanced,
    )

    print_point(
        "best specificity with severe recall >= 80%",
        best_80_recall,
    )

    print_point(
        "best specificity with severe recall >= 66.7%",
        best_67_recall,
    )

    print()

    print(
        "SEED-STABILITY SNAPSHOTS"
    )

    snapshot_thresholds = sorted(
        {
            float(
                best_balanced[
                    "threshold"
                ]
            ),
            *(
                [
                    float(
                        best_80_recall[
                            "threshold"
                        ]
                    )
                ]
                if best_80_recall
                is not None
                else []
            ),
            *(
                [
                    float(
                        best_67_recall[
                            "threshold"
                        ]
                    )
                ]
                if best_67_recall
                is not None
                else []
            ),
        }
    )

    for threshold in snapshot_thresholds:
        row = stability_lookup[
            threshold
        ]

        print(
            f"threshold="
            f"{threshold:.3f} "
            f"severe_seeds="
            f"{row['seeds_with_severe_events']} "
            f"mean_seed_severe_recall="
            f"{row['mean_seed_severe_recall']:.3%} "
            f"min_seed_severe_recall="
            f"{row['min_seed_severe_recall']:.3%} "
            f"mean_seed_specificity="
            f"{row['mean_seed_specificity']:.3%} "
            f"min_seed_specificity="
            f"{row['min_seed_specificity']:.3%} "
            f"mean_seed_harmful_recall="
            f"{row['mean_seed_harmful_recall']:.3%} "
            f"mean_seed_beneficial_preservation="
            f"{row['mean_seed_beneficial_preservation']:.3%}"
        )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 096 is retrospective threshold-geometry analysis. "
        "Thresholds are swept descriptively over already-consumed events. "
        "No threshold selected here should be described as prospectively "
        "validated or deployed as a controller guard."
    )

    print(
        "=" * 210
    )

    print(
        f"Threshold summary saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Seed-level threshold results saved to: "
        f"{SEED_OUTPUT_PATH}"
    )

    print(
        f"Quantile concentration results saved to: "
        f"{QUANTILE_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()