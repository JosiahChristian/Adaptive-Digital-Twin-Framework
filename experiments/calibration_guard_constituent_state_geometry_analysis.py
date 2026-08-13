import csv
import math
import statistics
from pathlib import Path

import numpy as np

from experiments.historical_local_calibration_risk_representation import (
    event_rows_for_seed,
)


SOURCE_EVENT_PATH = Path(
    "results/"
    "frozen_calibration_aware_controller_intervention_events.csv"
)

SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "calibration_guard_constituent_state_geometry_analysis.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "calibration_guard_constituent_state_geometry_analysis_events.csv"
)


CALIBRATION_FEATURES = [
    "predicted_action_loss",
    "local_mean_error",
    "local_error_std",
    "local_underestimate_fraction",
    "local_severe_underestimate_fraction",
]

CALIBRATION_PROBABILITY_FIELD = (
    "calibration_probability_baseline_action"
)

FLOAT_TOLERANCE = 1e-12


def read_csv(
    path,
):
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


def extract_veto_events():
    rows = read_csv(
        SOURCE_EVENT_PATH
    )

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

        veto_rows.append(
            dict(
                row
            )
        )

    return veto_rows


def reconstruct_calibration_lookup(
    seeds,
):
    lookup = {}

    for seed in seeds:
        print(
            f"reconstructing calibration state "
            f"for seed {seed}..."
        )

        rows = event_rows_for_seed(
            seed
        )

        for row in rows:
            key = (
                int(
                    row[
                        "generation_seed"
                    ]
                ),
                int(
                    row[
                        "test_index"
                    ]
                ),
                int(
                    row[
                        "action"
                    ]
                ),
            )

            lookup[
                key
            ] = row

    return lookup


def enrich_veto_events(
    veto_rows,
    calibration_lookup,
):
    output = []

    for row in veto_rows:
        seed = as_int(
            row,
            "generation_seed",
        )

        test_index = as_int(
            row,
            "test_index",
        )

        action = as_int(
            row,
            "support_baseline_action",
        )

        key = (
            seed,
            test_index,
            action,
        )

        if key not in calibration_lookup:
            raise KeyError(
                f"Missing reconstructed calibration "
                f"state for {key}"
            )

        calibration_row = (
            calibration_lookup[
                key
            ]
        )

        enriched = dict(
            row
        )

        enriched[
            "veto_class"
        ] = row[
            "baseline_expansion_outcome"
        ]

        for field in CALIBRATION_FEATURES:
            enriched[
                field
            ] = float(
                calibration_row[
                    field
                ]
            )

        enriched[
            "reconstructed_calibration_error"
        ] = float(
            calibration_row[
                "calibration_error"
            ]
        )

        enriched[
            "reconstructed_severe_underestimation"
        ] = int(
            calibration_row[
                "severe_underestimation"
            ]
        )

        output.append(
            enriched
        )

    return output


def describe_field(
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


def compare_groups(
    beneficial_rows,
    harmful_rows,
):
    fields = [
        CALIBRATION_PROBABILITY_FIELD,
        *CALIBRATION_FEATURES,
    ]

    output = []

    for field in fields:
        beneficial = describe_field(
            beneficial_rows,
            field,
        )

        harmful = describe_field(
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


def z_against_beneficial(
    harmful_value,
    beneficial_values,
):
    if len(
        beneficial_values
    ) < 2:
        return float(
            "nan"
        )

    std = statistics.stdev(
        beneficial_values
    )

    if std <= FLOAT_TOLERANCE:
        return float(
            "nan"
        )

    return (
        harmful_value
        - statistics.mean(
            beneficial_values
        )
    ) / std


def harmful_event_profiles(
    beneficial_rows,
    harmful_rows,
):
    output = []

    for harmful_row in harmful_rows:
        for field in CALIBRATION_FEATURES:
            harmful_value = as_float(
                harmful_row,
                field,
            )

            beneficial_values = finite_values(
                beneficial_rows,
                field,
            )

            less = sum(
                int(
                    value
                    < harmful_value
                )
                for value in beneficial_values
            )

            equal = sum(
                int(
                    abs(
                        value
                        - harmful_value
                    )
                    <= FLOAT_TOLERANCE
                )
                for value in beneficial_values
            )

            percentile = (
                less
                + 0.5
                * equal
            ) / len(
                beneficial_values
            )

            output.append(
                {
                    "generation_seed":
                        as_int(
                            harmful_row,
                            "generation_seed",
                        ),

                    "test_index":
                        as_int(
                            harmful_row,
                            "test_index",
                        ),

                    "metric":
                        field,

                    "harmful_value":
                        harmful_value,

                    "beneficial_mean":
                        safe_mean(
                            beneficial_values
                        ),

                    "beneficial_min":
                        safe_min(
                            beneficial_values
                        ),

                    "beneficial_max":
                        safe_max(
                            beneficial_values
                        ),

                    "percentile_vs_beneficial":
                        percentile,

                    "z_vs_beneficial":
                        z_against_beneficial(
                            harmful_value,
                            beneficial_values,
                        ),
                }
            )

    return output


def correlation_matrix_rows(
    rows,
):
    fields = [
        CALIBRATION_PROBABILITY_FIELD,
        *CALIBRATION_FEATURES,
    ]

    output = []

    for index_a, field_a in enumerate(
        fields
    ):
        for field_b in fields[
            index_a + 1:
        ]:
            values_a = np.asarray(
                finite_values(
                    rows,
                    field_a,
                ),
                dtype=float,
            )

            values_b = np.asarray(
                finite_values(
                    rows,
                    field_b,
                ),
                dtype=float,
            )

            if (
                len(
                    values_a
                )
                != len(
                    values_b
                )
                or len(
                    values_a
                )
                < 2
            ):
                correlation = float(
                    "nan"
                )

            elif (
                np.std(
                    values_a
                )
                <= FLOAT_TOLERANCE
                or np.std(
                    values_b
                )
                <= FLOAT_TOLERANCE
            ):
                correlation = float(
                    "nan"
                )

            else:
                correlation = float(
                    np.corrcoef(
                        values_a,
                        values_b,
                    )[
                        0,
                        1
                    ]
                )

            output.append(
                {
                    "metric_a":
                        field_a,

                    "metric_b":
                        field_b,

                    "correlation":
                        correlation,
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
    veto_rows = extract_veto_events()

    seeds = sorted(
        {
            as_int(
                row,
                "generation_seed",
            )
            for row in veto_rows
        }
    )

    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "CALIBRATION-GUARD CONSTITUENT "
        "STATE GEOMETRY ANALYSIS"
    )

    print(
        "=" * 210
    )

    print(
        f"source="
        f"{SOURCE_EVENT_PATH}"
    )

    print(
        f"veto events="
        f"{len(veto_rows)}"
    )

    print(
        f"veto seeds="
        f"{seeds}"
    )

    print()

    calibration_lookup = (
        reconstruct_calibration_lookup(
            seeds
        )
    )

    enriched_rows = enrich_veto_events(
        veto_rows,
        calibration_lookup,
    )

    beneficial_rows = [
        row
        for row in enriched_rows
        if row[
            "veto_class"
        ]
        == "beneficial"
    ]

    harmful_rows = [
        row
        for row in enriched_rows
        if row[
            "veto_class"
        ]
        == "harmful"
    ]

    comparison_rows = compare_groups(
        beneficial_rows,
        harmful_rows,
    )

    profile_rows = harmful_event_profiles(
        beneficial_rows,
        harmful_rows,
    )

    correlation_rows = correlation_matrix_rows(
        enriched_rows
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

    for row in profile_rows:
        copy = {
            "record_type":
                "harmful_event_profile"
        }

        copy.update(
            row
        )

        output_rows.append(
            copy
        )

    for row in correlation_rows:
        copy = {
            "record_type":
                "correlation"
        }

        copy.update(
            row
        )

        output_rows.append(
            copy
        )

    save_csv(
        SUMMARY_OUTPUT_PATH,
        output_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        enriched_rows,
    )

    print(
        "EVENT POPULATION"
    )

    print(
        f"beneficial vetoes="
        f"{len(beneficial_rows)}"
    )

    print(
        f"harmful vetoes="
        f"{len(harmful_rows)}"
    )

    print()

    print(
        "CONSTITUENT STATE SEPARATION"
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
            f"{row['metric']:<44} "
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
        "HARMFUL EVENT CONSTITUENT PROFILES"
    )

    for harmful_row in harmful_rows:
        seed = as_int(
            harmful_row,
            "generation_seed",
        )

        index = as_int(
            harmful_row,
            "test_index",
        )

        print()

        print(
            f"seed={seed} "
            f"index={index} "
            f"prob="
            f"{as_float(harmful_row, CALIBRATION_PROBABILITY_FIELD):.6f}"
        )

        matching = [
            row
            for row in profile_rows
            if (
                int(
                    row[
                        "generation_seed"
                    ]
                )
                == seed
                and int(
                    row[
                        "test_index"
                    ]
                )
                == index
            )
        ]

        for row in matching:
            z_value = row[
                "z_vs_beneficial"
            ]

            z_text = (
                f"{z_value:+.3f}"
                if math.isfinite(
                    z_value
                )
                else "n/a"
            )

            print(
                f"  "
                f"{row['metric']:<40} "
                f"value="
                f"{row['harmful_value']:.6f} "
                f"beneficial_range=["
                f"{row['beneficial_min']:.6f},"
                f"{row['beneficial_max']:.6f}"
                f"] "
                f"percentile="
                f"{row['percentile_vs_beneficial']:.3%} "
                f"z="
                f"{z_text}"
            )

    print()

    print(
        "CORRELATIONS WITH CALIBRATION PROBABILITY"
    )

    probability_correlations = [
        row
        for row in correlation_rows
        if (
            row[
                "metric_a"
            ]
            == CALIBRATION_PROBABILITY_FIELD
            or row[
                "metric_b"
            ]
            == CALIBRATION_PROBABILITY_FIELD
        )
    ]

    for row in probability_correlations:
        other = (
            row[
                "metric_b"
            ]
            if row[
                "metric_a"
            ]
            == CALIBRATION_PROBABILITY_FIELD
            else row[
                "metric_a"
            ]
        )

        correlation = row[
            "correlation"
        ]

        correlation_text = (
            f"{correlation:+.3f}"
            if math.isfinite(
                correlation
            )
            else "n/a"
        )

        print(
            f"{other:<40} "
            f"corr="
            f"{correlation_text}"
        )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 103 reconstructs the frozen constituent "
        "calibration-state features for the 22 Experiment 101 "
        "vetoes using already-consumed seeds only."
    )

    print(
        "No new classifier, threshold, intervention rule, "
        "or prospective seed is introduced."
    )

    print(
        "=" * 210
    )

    print(
        f"Summary saved to: "
        f"{SUMMARY_OUTPUT_PATH}"
    )

    print(
        f"Enriched veto events saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()