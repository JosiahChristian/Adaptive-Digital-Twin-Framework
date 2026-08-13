import csv
import math
import statistics
from pathlib import Path

import numpy as np


EVENT_INPUT_PATH = Path(
    "results/"
    "frozen_loss_ceiling_calibration_guard_prospective_validation_events.csv"
)

OUTPUT_PATH = Path(
    "results/"
    "prospective_loss_ceiling_veto_selectivity_decomposition.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "prospective_loss_ceiling_veto_selectivity_decomposition_events.csv"
)


PRIMARY_CEILING_THRESHOLD = 0.155

FLOAT_TOLERANCE = 1e-12


DIAGNOSTIC_FIELDS = [
    "predicted_loss_ceiling",
    "context_support_distance",
    "predicted_baseline_action_loss",
    "baseline_action_loss_error",
    "baseline_regret",
]


OPTIONAL_FIELDS = [
    "predicted_loss_floor",
    "predicted_loss_mean",
    "predicted_loss_spread",
    "predicted_risk",
    "safety_score",
    "downside_score",
    "current_mismatch_indicator",
    "anchor_age",
    "trigger_score",
    "predicted_regret_margin",
    "action_step",
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
    if field not in row:
        return default

    value = row[
        field
    ]

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
        default=float(
            "nan"
        ),
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
    values = [
        as_float(
            row,
            field,
        )
        for row in rows
    ]

    return [
        value
        for value in values
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


def describe_group(
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


def field_present(
    rows,
    field,
):
    return any(
        math.isfinite(
            as_float(
                row,
                field,
            )
        )
        for row in rows
    )


def extract_primary_veto_events(
    rows,
):
    output = []

    for row in rows:
        if (
            as_int(
                row,
                "primary_ceiling_veto",
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

        output.append(
            copy
        )

    return output


def compare_fields(
    beneficial_rows,
    harmful_rows,
    fields,
):
    output = []

    for field in fields:
        beneficial = describe_group(
            beneficial_rows,
            field,
        )

        harmful = describe_group(
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
                        if (
                            math.isfinite(
                                harmful[
                                    "mean"
                                ]
                            )
                            and math.isfinite(
                                beneficial[
                                    "mean"
                                ]
                            )
                        )
                        else float(
                            "nan"
                        )
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


def rank_harmful_event_against_beneficial(
    harmful_row,
    beneficial_rows,
    fields,
):
    output = []

    for field in fields:
        harmful_value = as_float(
            harmful_row,
            field,
        )

        beneficial_values = finite_values(
            beneficial_rows,
            field,
        )

        if (
            not math.isfinite(
                harmful_value
            )
            or not beneficial_values
        ):
            continue

        less_count = sum(
            int(
                value
                < harmful_value
            )
            for value in beneficial_values
        )

        equal_count = sum(
            int(
                abs(
                    value
                    - harmful_value
                )
                <= FLOAT_TOLERANCE
            )
            for value in beneficial_values
        )

        greater_count = sum(
            int(
                value
                > harmful_value
            )
            for value in beneficial_values
        )

        percentile = (
            less_count
            + 0.5
            * equal_count
        ) / len(
            beneficial_values
        )

        beneficial_mean = safe_mean(
            beneficial_values
        )

        beneficial_std = (
            statistics.stdev(
                beneficial_values
            )
            if len(
                beneficial_values
            )
            >= 2
            else float(
                "nan"
            )
        )

        z_vs_beneficial = (
            (
                harmful_value
                - beneficial_mean
            )
            / beneficial_std
            if (
                math.isfinite(
                    beneficial_std
                )
                and beneficial_std
                > FLOAT_TOLERANCE
            )
            else float(
                "nan"
            )
        )

        output.append(
            {
                "metric":
                    field,

                "harmful_value":
                    harmful_value,

                "beneficial_mean":
                    beneficial_mean,

                "beneficial_min":
                    min(
                        beneficial_values
                    ),

                "beneficial_max":
                    max(
                        beneficial_values
                    ),

                "harmful_percentile_vs_beneficial":
                    percentile,

                "harmful_z_vs_beneficial":
                    z_vs_beneficial,

                "beneficial_less":
                    less_count,

                "beneficial_equal":
                    equal_count,

                "beneficial_greater":
                    greater_count,
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

    veto_rows = extract_primary_veto_events(
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

    available_optional_fields = [
        field
        for field in OPTIONAL_FIELDS
        if field_present(
            veto_rows,
            field,
        )
    ]

    analysis_fields = (
        DIAGNOSTIC_FIELDS
        + available_optional_fields
    )

    comparison_rows = compare_fields(
        beneficial_rows,
        harmful_rows,
        analysis_fields,
    )

    harmful_rank_rows = []

    if len(
        harmful_rows
    ) == 1:
        harmful_rank_rows = (
            rank_harmful_event_against_beneficial(
                harmful_rows[
                    0
                ],
                beneficial_rows,
                analysis_fields,
            )
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

    for row in harmful_rank_rows:
        copy = {
            "record_type":
                "harmful_rank_against_beneficial"
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
        "PROSPECTIVE LOSS-CEILING VETO "
        "SELECTIVITY DECOMPOSITION"
    )

    print(
        "=" * 210
    )

    print(
        f"input="
        f"{EVENT_INPUT_PATH}"
    )

    print(
        f"primary ceiling threshold="
        f"{PRIMARY_CEILING_THRESHOLD:.3f}"
    )

    print(
        f"primary vetoed expansion events="
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
        "AVAILABLE PRE/OUTCOME FIELDS"
    )

    for field in analysis_fields:
        print(
            field
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
            f"{row['metric']:<34} "
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

    if len(
        harmful_rows
    ) == 1:
        harmful_event = harmful_rows[
            0
        ]

        print(
            "HARMFUL VETO EVENT"
        )

        print(
            f"seed="
            f"{as_int(harmful_event, 'generation_seed')} "
            f"test_index="
            f"{as_int(harmful_event, 'test_index')} "
            f"primary_action="
            f"{as_int(harmful_event, 'primary_action')} "
            f"support_action="
            f"{as_int(harmful_event, 'support_baseline_action')} "
            f"ceiling="
            f"{as_float(harmful_event, 'predicted_loss_ceiling'):.6f} "
            f"support_distance="
            f"{as_float(harmful_event, 'context_support_distance'):.6f} "
            f"predicted_loss="
            f"{as_float(harmful_event, 'predicted_baseline_action_loss'):.6f} "
            f"realized_loss="
            f"{as_float(harmful_event, 'realized_baseline_action_loss'):.6f} "
            f"loss_error="
            f"{as_float(harmful_event, 'baseline_action_loss_error'):+.6f} "
            f"regret="
            f"{as_float(harmful_event, 'baseline_regret'):.6f}"
        )

        print()

        print(
            "HARMFUL EVENT RANK VS FOUR BENEFICIAL VETOES"
        )

        for row in harmful_rank_rows:
            z_value = row[
                "harmful_z_vs_beneficial"
            ]

            z_text = (
                f"{z_value:+.3f}"
                if math.isfinite(
                    z_value
                )
                else "n/a"
            )

            print(
                f"{row['metric']:<34} "
                f"harmful="
                f"{row['harmful_value']:.6f} "
                f"beneficial_range=["
                f"{row['beneficial_min']:.6f},"
                f"{row['beneficial_max']:.6f}"
                f"] "
                f"percentile="
                f"{row['harmful_percentile_vs_beneficial']:.3%} "
                f"z="
                f"{z_text}"
            )

    else:
        print(
            "A unique harmful veto event was not found; "
            "event-rank analysis skipped."
        )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 098 is descriptive because only five primary "
        "ceiling-veto events exist in the prospective block. "
        "No classifier, new threshold, or controller rule is fit."
    )

    print(
        "Standardized effect sizes are intentionally reported as "
        "not available when one group has fewer than two observations."
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