import csv
import math
import statistics
from pathlib import Path

import numpy as np

from experiments.frozen_calibration_aware_controller_intervention import (
    evaluate_seed,
    train_calibration_model,
)

from experiments.historical_local_calibration_risk_representation import (
    event_rows_for_seed,
)


SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "historical_support_expansion_constituent_geometry_replication.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "historical_support_expansion_constituent_geometry_replication_events.csv"
)

SEED_OUTPUT_PATH = Path(
    "results/"
    "historical_support_expansion_constituent_geometry_replication_seeds.csv"
)


# These seeds were consumed prospectively by Experiment 100.
# They are independent of the Experiment 101 veto population
# used to discover the constituent geometry in Experiment 103.
REPLICATION_SEEDS = list(
    range(
        44071,
        44091,
    )
)


CALIBRATION_FEATURES = [
    "predicted_action_loss",
    "local_mean_error",
    "local_error_std",
    "local_underestimate_fraction",
    "local_severe_underestimate_fraction",
]

PRIMARY_REPLICATION_FEATURES = [
    "local_error_std",
    "local_severe_underestimate_fraction",
]

DISCOVERY_EFFECT_DIRECTIONS = {
    "local_error_std":
        +1,

    "local_severe_underestimate_fraction":
        +1,
}


FLOAT_TOLERANCE = 1e-12


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


def rank_auc(
    beneficial_values,
    harmful_values,
):
    """
    Probability that a randomly selected harmful event
    has a larger feature value than a randomly selected
    beneficial event, with ties receiving half credit.
    """
    if (
        not beneficial_values
        or not harmful_values
    ):
        return float(
            "nan"
        )

    favorable = 0.0
    total = 0

    for harmful_value in harmful_values:
        for beneficial_value in beneficial_values:
            total += 1

            if (
                harmful_value
                > beneficial_value
            ):
                favorable += 1.0

            elif abs(
                harmful_value
                - beneficial_value
            ) <= FLOAT_TOLERANCE:
                favorable += 0.5

    return (
        favorable
        / total
    )


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


def reconstruct_baseline_expansions(
    calibration_model,
):
    event_rows = []
    seed_summary_rows = []

    for seed in REPLICATION_SEEDS:
        print(
            f"reconstructing replication seed "
            f"{seed}..."
        )

        (
            _seed_policy_rows,
            controller_event_rows,
        ) = evaluate_seed(
            seed,
            calibration_model,
        )

        calibration_rows = event_rows_for_seed(
            seed
        )

        calibration_lookup = {
            (
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
            ):
                row
            for row in calibration_rows
        }

        seed_beneficial = 0
        seed_harmful = 0

        for controller_row in controller_event_rows:
            if (
                as_int(
                    controller_row,
                    "support_changed_action",
                )
                != 1
            ):
                continue

            outcome = controller_row.get(
                "baseline_expansion_outcome",
                "",
            )

            if outcome not in (
                "beneficial",
                "harmful",
            ):
                continue

            test_index = as_int(
                controller_row,
                "test_index",
            )

            action = as_int(
                controller_row,
                "support_baseline_action",
            )

            key = (
                test_index,
                action,
            )

            if key not in calibration_lookup:
                raise KeyError(
                    "Missing calibration-state reconstruction "
                    f"for seed={seed}, "
                    f"test_index={test_index}, "
                    f"action={action}"
                )

            calibration_row = calibration_lookup[
                key
            ]

            enriched = dict(
                controller_row
            )

            enriched[
                "replication_class"
            ] = outcome

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

            event_rows.append(
                enriched
            )

            if outcome == "beneficial":
                seed_beneficial += 1

            elif outcome == "harmful":
                seed_harmful += 1

        seed_summary_rows.append(
            {
                "generation_seed":
                    seed,

                "beneficial_expansions":
                    seed_beneficial,

                "harmful_expansions":
                    seed_harmful,

                "total_labeled_expansions":
                    (
                        seed_beneficial
                        + seed_harmful
                    ),

                "contains_harmful":
                    int(
                        seed_harmful
                        > 0
                    ),
            }
        )

    return (
        event_rows,
        seed_summary_rows,
    )


def compare_groups(
    beneficial_rows,
    harmful_rows,
):
    output = []

    for field in CALIBRATION_FEATURES:
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

        effect = standardized_difference(
            beneficial_values,
            harmful_values,
        )

        auc = rank_auc(
            beneficial_values,
            harmful_values,
        )

        discovery_direction = (
            DISCOVERY_EFFECT_DIRECTIONS.get(
                field,
                0,
            )
        )

        if discovery_direction == 0:
            direction_replication = ""
        else:
            delta = (
                harmful[
                    "mean"
                ]
                - beneficial[
                    "mean"
                ]
            )

            direction_replication = int(
                (
                    delta
                    > FLOAT_TOLERANCE
                    and discovery_direction
                    > 0
                )
                or (
                    delta
                    < -FLOAT_TOLERANCE
                    and discovery_direction
                    < 0
                )
            )

        output.append(
            {
                "metric":
                    field,

                "primary_replication_feature":
                    int(
                        field
                        in PRIMARY_REPLICATION_FEATURES
                    ),

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
                    effect,

                "rank_auc_harmful_high":
                    auc,

                "discovery_direction":
                    discovery_direction,

                "direction_replication":
                    direction_replication,
            }
        )

    return output


def seed_level_feature_replication(
    event_rows,
):
    output = []

    for seed in REPLICATION_SEEDS:
        seed_rows = [
            row
            for row in event_rows
            if as_int(
                row,
                "generation_seed",
            )
            == seed
        ]

        beneficial_rows = [
            row
            for row in seed_rows
            if row[
                "replication_class"
            ]
            == "beneficial"
        ]

        harmful_rows = [
            row
            for row in seed_rows
            if row[
                "replication_class"
            ]
            == "harmful"
        ]

        if (
            not beneficial_rows
            or not harmful_rows
        ):
            continue

        for field in PRIMARY_REPLICATION_FEATURES:
            beneficial_values = finite_values(
                beneficial_rows,
                field,
            )

            harmful_values = finite_values(
                harmful_rows,
                field,
            )

            beneficial_mean = safe_mean(
                beneficial_values
            )

            harmful_mean = safe_mean(
                harmful_values
            )

            delta = (
                harmful_mean
                - beneficial_mean
            )

            output.append(
                {
                    "generation_seed":
                        seed,

                    "metric":
                        field,

                    "beneficial_count":
                        len(
                            beneficial_values
                        ),

                    "harmful_count":
                        len(
                            harmful_values
                        ),

                    "beneficial_mean":
                        beneficial_mean,

                    "harmful_mean":
                        harmful_mean,

                    "difference_harmful_minus_beneficial":
                        delta,

                    "direction_replication":
                        int(
                            delta
                            > FLOAT_TOLERANCE
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
    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "HISTORICAL SUPPORT-EXPANSION "
        "CONSTITUENT GEOMETRY REPLICATION"
    )

    print(
        "=" * 210
    )

    print(
        f"replication seeds="
        f"{REPLICATION_SEEDS[0]}-"
        f"{REPLICATION_SEEDS[-1]}"
    )

    print(
        "discovery sample excluded="
        "Experiment 101 seeds 44091-44110"
    )

    print()

    print(
        "RECONSTRUCTING FROZEN HISTORICAL "
        "CALIBRATION MODEL"
    )

    # evaluate_seed requires the calibration model because it
    # reconstructs both policies. The replication target below,
    # however, uses only the support-baseline policy and therefore
    # does not depend on whether the calibration guard vetoed it.
    calibration_model = (
        train_calibration_model()
    )

    print()

    print(
        "RECONSTRUCTING SUPPORT-BASELINE EXPANSIONS"
    )

    (
        event_rows,
        seed_summary_rows,
    ) = reconstruct_baseline_expansions(
        calibration_model
    )

    beneficial_rows = [
        row
        for row in event_rows
        if row[
            "replication_class"
        ]
        == "beneficial"
    ]

    harmful_rows = [
        row
        for row in event_rows
        if row[
            "replication_class"
        ]
        == "harmful"
    ]

    comparison_rows = compare_groups(
        beneficial_rows,
        harmful_rows,
    )

    seed_feature_rows = (
        seed_level_feature_replication(
            event_rows
        )
    )

    print()

    print(
        "REPLICATION EVENT POPULATION"
    )

    print(
        f"labeled support expansions="
        f"{len(event_rows)}"
    )

    print(
        f"beneficial="
        f"{len(beneficial_rows)}"
    )

    print(
        f"harmful="
        f"{len(harmful_rows)}"
    )

    harmful_seeds = sum(
        int(
            row[
                "contains_harmful"
            ]
        )
        for row in seed_summary_rows
    )

    print(
        f"seeds with harmful expansions="
        f"{harmful_seeds}/"
        f"{len(REPLICATION_SEEDS)}"
    )

    print()

    print(
        "CONSTITUENT GEOMETRY REPLICATION"
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

        auc = row[
            "rank_auc_harmful_high"
        ]

        auc_text = (
            f"{auc:.3f}"
            if math.isfinite(
                auc
            )
            else "n/a"
        )

        replication_text = (
            str(
                bool(
                    row[
                        "direction_replication"
                    ]
                )
            )
            if row[
                "direction_replication"
            ]
            != ""
            else "n/a"
        )

        print(
            f"{row['metric']:<40} "
            f"beneficial="
            f"{row['beneficial_mean']:.6f} "
            f"harmful="
            f"{row['harmful_mean']:.6f} "
            f"delta="
            f"{row['difference_harmful_minus_beneficial']:+.6f} "
            f"effect="
            f"{effect_text} "
            f"rank_AUC="
            f"{auc_text} "
            f"direction_replication="
            f"{replication_text}"
        )

    print()

    print(
        "PRIMARY EXPERIMENT 103 REPLICATION CHECK"
    )

    primary_rows = [
        row
        for row in comparison_rows
        if int(
            row[
                "primary_replication_feature"
            ]
        )
        == 1
    ]

    for row in primary_rows:
        print(
            f"{row['metric']:<40} "
            f"discovery_direction=harmful_higher "
            f"replicated="
            f"{bool(row['direction_replication'])} "
            f"effect="
            f"{row['standardized_difference']:+.3f}"
        )

    replicated_count = sum(
        int(
            row[
                "direction_replication"
            ]
        )
        for row in primary_rows
    )

    print()

    print(
        f"primary directions replicated="
        f"{replicated_count}/"
        f"{len(primary_rows)}"
    )

    print()

    print(
        "SEED-LEVEL DIRECTION STABILITY"
    )

    for field in PRIMARY_REPLICATION_FEATURES:
        matching = [
            row
            for row in seed_feature_rows
            if row[
                "metric"
            ]
            == field
        ]

        replicated = sum(
            int(
                row[
                    "direction_replication"
                ]
            )
            for row in matching
        )

        print(
            f"{field:<40} "
            f"informative_seeds="
            f"{len(matching)} "
            f"harmful_higher_seeds="
            f"{replicated}"
        )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 104 tests the Experiment 103 constituent "
        "geometry on already-consumed seeds 44071-44090, "
        "excluding the Experiment 101 veto sample that generated "
        "the discovery."
    )

    print(
        "Only support-baseline beneficial/harmful expansion labels "
        "are analyzed. No new controller threshold, classifier, "
        "or prospective seed is introduced."
    )

    print(
        "The reconstructed calibration model is required by the "
        "shared controller reconstruction code, but the primary "
        "replication outcome does not depend on whether that guard "
        "would veto the support-baseline action."
    )

    print(
        "=" * 210
    )

    summary_rows = []

    for row in comparison_rows:
        copy = {
            "record_type":
                "group_comparison"
        }

        copy.update(
            row
        )

        summary_rows.append(
            copy
        )

    for row in seed_feature_rows:
        copy = {
            "record_type":
                "seed_feature_replication"
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
        EVENT_OUTPUT_PATH,
        event_rows,
    )

    save_csv(
        SEED_OUTPUT_PATH,
        seed_summary_rows,
    )

    print(
        f"Summary saved to: "
        f"{SUMMARY_OUTPUT_PATH}"
    )

    print(
        f"Expansion events saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )

    print(
        f"Seed results saved to: "
        f"{SEED_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()