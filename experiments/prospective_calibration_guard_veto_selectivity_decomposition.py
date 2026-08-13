import csv
import math
import statistics
from pathlib import Path

import numpy as np


EVENT_INPUT_PATH = Path(
    "results/"
    "frozen_calibration_aware_controller_intervention_events.csv"
)

OUTPUT_PATH = Path(
    "results/"
    "prospective_calibration_guard_veto_selectivity_decomposition.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "prospective_calibration_guard_veto_selectivity_decomposition_events.csv"
)


CALIBRATION_THRESHOLD = 0.468010308717

FLOAT_TOLERANCE = 1e-12


CORE_FIELDS = [
    "calibration_probability_baseline_action",
    "context_support_distance",
    "predicted_baseline_action_loss",
    "baseline_action_loss_error",
    "baseline_regret",
]


def read_events():
    with EVENT_INPUT_PATH.open(
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


def finite_values(
    rows,
    field,
):
    return [
        value
        for value in (
            as_float(
                row,
                field,
            )
            for row in rows
        )
        if math.isfinite(
            value
        )
    ]


def safe_mean(
    values,
):
    if not values:
        return float(
            "nan"
        )

    return statistics.mean(
        values
    )


def safe_median(
    values,
):
    if not values:
        return float(
            "nan"
        )

    return statistics.median(
        values
    )


def safe_min(
    values,
):
    if not values:
        return float(
            "nan"
        )

    return min(
        values
    )


def safe_max(
    values,
):
    if not values:
        return float(
            "nan"
        )

    return max(
        values
    )


def standardized_difference(
    beneficial_values,
    harmful_values,
):
    if (
        len(
            beneficial_values
        )
        < 2
        or len(
            harmful_values
        )
        < 2
    ):
        return float(
            "nan"
        )

    beneficial_variance = statistics.variance(
        beneficial_values
    )

    harmful_variance = statistics.variance(
        harmful_values
    )

    pooled_variance = (
        (
            (
                len(
                    beneficial_values
                )
                - 1
            )
            * beneficial_variance
        )
        +
        (
            (
                len(
                    harmful_values
                )
                - 1
            )
            * harmful_variance
        )
    ) / (
        len(
            beneficial_values
        )
        + len(
            harmful_values
        )
        - 2
    )

    if pooled_variance <= FLOAT_TOLERANCE:
        return 0.0

    return (
        safe_mean(
            harmful_values
        )
        - safe_mean(
            beneficial_values
        )
    ) / (
        pooled_variance
        ** 0.5
    )


def extract_veto_events(
    rows,
):
    veto_rows = []

    for row in rows:
        if (
            as_int(
                row,
                "guard_changed_support_action",
            )
            != 1
        ):
            continue

        outcome = row.get(
            "baseline_expansion_outcome",
            "",
        )

        if outcome not in (
            "beneficial",
            "harmful",
        ):
            continue

        copy = dict(
            row
        )

        copy[
            "veto_class"
        ] = outcome

        veto_rows.append(
            copy
        )

    return veto_rows


def describe(
    rows,
    field,
):
    values = finite_values(
        rows,
        field,
    )

    return {
        "count":
            len(
                values
            ),

        "mean":
            safe_mean(
                values
            ),

        "median":
            safe_median(
                values
            ),

        "min":
            safe_min(
                values
            ),

        "max":
            safe_max(
                values
            ),
    }


def compare_fields(
    beneficial_rows,
    harmful_rows,
):
    output = []

    for field in CORE_FIELDS:
        beneficial = describe(
            beneficial_rows,
            field,
        )

        harmful = describe(
            harmful_rows,
            field,
        )

        beneficial_values = finite_values(
            beneficial_rows,
            field,
        )

        harmful_values = finite_values(
            harmful_rows,
            field,
        )

        output.append(
            {
                "metric":
                    field,

                "beneficial_count":
                    beneficial[
                        "count"
                    ],

                "harmful_count":
                    harmful[
                        "count"
                    ],

                "beneficial_mean":
                    beneficial[
                        "mean"
                    ],

                "harmful_mean":
                    harmful[
                        "mean"
                    ],

                "difference_harmful_minus_beneficial":
                    (
                        harmful[
                            "mean"
                        ]
                        - beneficial[
                            "mean"
                        ]
                    ),

                "beneficial_median":
                    beneficial[
                        "median"
                    ],

                "harmful_median":
                    harmful[
                        "median"
                    ],

                "beneficial_min":
                    beneficial[
                        "min"
                    ],

                "beneficial_max":
                    beneficial[
                        "max"
                    ],

                "harmful_min":
                    harmful[
                        "min"
                    ],

                "harmful_max":
                    harmful[
                        "max"
                    ],

                "standardized_difference":
                    standardized_difference(
                        beneficial_values,
                        harmful_values,
                    ),
            }
        )

    return output


def rank_events(
    veto_rows,
):
    output = []

    for field in CORE_FIELDS:
        values = finite_values(
            veto_rows,
            field,
        )

        if not values:
            continue

        sorted_values = sorted(
            values
        )

        for row in veto_rows:
            value = as_float(
                row,
                field,
            )

            if not math.isfinite(
                value
            ):
                continue

            less = sum(
                int(
                    candidate
                    < value
                )
                for candidate in sorted_values
            )

            equal = sum(
                int(
                    abs(
                        candidate
                        - value
                    )
                    <= FLOAT_TOLERANCE
                )
                for candidate in sorted_values
            )

            percentile = (
                less
                + 0.5
                * equal
            ) / len(
                sorted_values
            )

            output.append(
                {
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

                    "veto_class":
                        row[
                            "veto_class"
                        ],

                    "metric":
                        field,

                    "value":
                        value,

                    "percentile_among_vetoes":
                        percentile,
                }
            )

    return output


def calibration_probability_bands(
    beneficial_rows,
    harmful_rows,
):
    all_rows = (
        beneficial_rows
        + harmful_rows
    )

    probabilities = finite_values(
        all_rows,
        "calibration_probability_baseline_action",
    )

    if not probabilities:
        return []

    thresholds = sorted(
        {
            CALIBRATION_THRESHOLD,
            0.50,
            0.60,
            0.70,
            0.80,
            0.90,
            *[
                float(
                    np.quantile(
                        probabilities,
                        quantile,
                    )
                )
                for quantile in [
                    0.25,
                    0.50,
                    0.75,
                ]
            ],
        }
    )

    output = []

    for threshold in thresholds:
        flagged = [
            row
            for row in all_rows
            if as_float(
                row,
                "calibration_probability_baseline_action",
            )
            >= threshold
        ]

        beneficial_flagged = sum(
            int(
                row[
                    "veto_class"
                ]
                == "beneficial"
            )
            for row in flagged
        )

        harmful_flagged = sum(
            int(
                row[
                    "veto_class"
                ]
                == "harmful"
            )
            for row in flagged
        )

        harmful_total = len(
            harmful_rows
        )

        beneficial_total = len(
            beneficial_rows
        )

        output.append(
            {
                "threshold":
                    threshold,

                "flagged_events":
                    len(
                        flagged
                    ),

                "harmful_flagged":
                    harmful_flagged,

                "beneficial_flagged":
                    beneficial_flagged,

                "harmful_recall":
                    (
                        harmful_flagged
                        / harmful_total
                        if harmful_total
                        > 0
                        else 0.0
                    ),

                "beneficial_preservation":
                    (
                        (
                            beneficial_total
                            - beneficial_flagged
                        )
                        / beneficial_total
                        if beneficial_total
                        > 0
                        else 1.0
                    ),

                "harmful_precision":
                    (
                        harmful_flagged
                        / len(
                            flagged
                        )
                        if flagged
                        else 0.0
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
    rows = read_events()

    veto_rows = extract_veto_events(
        rows
    )

    beneficial_rows = [
        row
        for row in veto_rows
        if row[
            "veto_class"
        ]
        == "beneficial"
    ]

    harmful_rows = [
        row
        for row in veto_rows
        if row[
            "veto_class"
        ]
        == "harmful"
    ]

    comparison_rows = compare_fields(
        beneficial_rows,
        harmful_rows,
    )

    rank_rows = rank_events(
        veto_rows
    )

    band_rows = calibration_probability_bands(
        beneficial_rows,
        harmful_rows,
    )

    output_rows = []

    for row in comparison_rows:
        copy = {
            "record_type":
                "group_comparison"
        }

        copy.update(
            row
        )

        output_rows.append(
            copy
        )

    for row in band_rows:
        copy = {
            "record_type":
                "probability_band"
        }

        copy.update(
            row
        )

        output_rows.append(
            copy
        )

    for row in rank_rows:
        copy = {
            "record_type":
                "event_rank"
        }

        copy.update(
            row
        )

        output_rows.append(
            copy
        )

    save_csv(
        OUTPUT_PATH,
        output_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        veto_rows,
    )

    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PROSPECTIVE CALIBRATION-GUARD "
        "VETO SELECTIVITY DECOMPOSITION"
    )

    print(
        "=" * 210
    )

    print(
        f"input="
        f"{EVENT_INPUT_PATH}"
    )

    print(
        f"frozen calibration threshold="
        f"{CALIBRATION_THRESHOLD:.12f}"
    )

    print(
        f"vetoed support-expansion events="
        f"{len(veto_rows)}"
    )

    print(
        f"beneficial vetoed="
        f"{len(beneficial_rows)}"
    )

    print(
        f"harmful vetoed="
        f"{len(harmful_rows)}"
    )

    print()

    print(
        "GROUP COMPARISONS"
    )

    for row in comparison_rows:
        effect = row[
            "standardized_difference"
        ]

        effect_text = (
            f"{effect:+.3f}"
            if math.isfinite(
                effect
            )
            else "n/a"
        )

        print(
            f"{row['metric']:<42} "
            f"beneficial="
            f"{row['beneficial_mean']:.6f} "
            f"harmful="
            f"{row['harmful_mean']:.6f} "
            f"delta="
            f"{row['difference_harmful_minus_beneficial']:+.6f} "
            f"effect="
            f"{effect_text}"
        )

    print()

    print(
        "CALIBRATION-PROBABILITY BAND DIAGNOSTICS"
    )

    for row in band_rows:
        print(
            f"threshold="
            f"{row['threshold']:.6f} "
            f"flagged="
            f"{row['flagged_events']} "
            f"harmful="
            f"{row['harmful_flagged']} "
            f"beneficial="
            f"{row['beneficial_flagged']} "
            f"harmful_recall="
            f"{row['harmful_recall']:.3%} "
            f"beneficial_preservation="
            f"{row['beneficial_preservation']:.3%} "
            f"harmful_precision="
            f"{row['harmful_precision']:.3%}"
        )

    print()

    print(
        "VETO EVENT DETAILS"
    )

    for row in veto_rows:
        print(
            f"seed="
            f"{as_int(row, 'generation_seed')} "
            f"index="
            f"{as_int(row, 'test_index')} "
            f"class="
            f"{row['veto_class']} "
            f"prob="
            f"{as_float(row, 'calibration_probability_baseline_action'):.6f} "
            f"support="
            f"{as_float(row, 'context_support_distance'):.6f} "
            f"predicted_loss="
            f"{as_float(row, 'predicted_baseline_action_loss'):.6f} "
            f"loss_error="
            f"{as_float(row, 'baseline_action_loss_error'):+.6f} "
            f"regret="
            f"{as_float(row, 'baseline_regret'):.6f}"
        )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 102 is diagnostic only. "
        "It analyzes the 22 veto events already produced by "
        "Experiment 101 and does not touch new seeds."
    )

    print(
        "No classifier, threshold replacement, or new controller "
        "rule is fit from these events."
    )

    print(
        "=" * 210
    )

    print(
        f"Summary saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Veto-event results saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()