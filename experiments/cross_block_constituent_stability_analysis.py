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
    "cross_block_constituent_stability_analysis.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "cross_block_constituent_stability_analysis_events.csv"
)

BLOCK_OUTPUT_PATH = Path(
    "results/"
    "cross_block_constituent_stability_analysis_blocks.csv"
)


BLOCKS = {
    "block_071_090":
        list(
            range(
                44071,
                44091,
            )
        ),

    "block_091_110":
        list(
            range(
                44091,
                44111,
            )
        ),
}


CALIBRATION_FEATURES = [
    "predicted_action_loss",
    "local_mean_error",
    "local_error_std",
    "local_underestimate_fraction",
    "local_severe_underestimate_fraction",
]

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

            if harmful_value > beneficial_value:
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


def reconstruct_block_events(
    block_name,
    seeds,
    calibration_model,
):
    output = []

    for seed in seeds:
        print(
            f"{block_name}: reconstructing seed "
            f"{seed}..."
        )

        (
            _seed_rows,
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
                    f"Missing calibration row "
                    f"for seed={seed}, "
                    f"index={test_index}, "
                    f"action={action}"
                )

            calibration_row = calibration_lookup[
                key
            ]

            enriched = dict(
                controller_row
            )

            enriched[
                "block"
            ] = block_name

            enriched[
                "class"
            ] = outcome

            for field in CALIBRATION_FEATURES:
                enriched[
                    field
                ] = float(
                    calibration_row[
                        field
                    ]
                )

            output.append(
                enriched
            )

    return output


def block_feature_rows(
    block_name,
    rows,
):
    beneficial_rows = [
        row
        for row in rows
        if row[
            "class"
        ]
        == "beneficial"
    ]

    harmful_rows = [
        row
        for row in rows
        if row[
            "class"
        ]
        == "harmful"
    ]

    output = []

    for field in CALIBRATION_FEATURES:
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
                "block":
                    block_name,

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

                "standardized_difference":
                    standardized_difference(
                        beneficial_values,
                        harmful_values,
                    ),

                "rank_auc_harmful_high":
                    rank_auc(
                        beneficial_values,
                        harmful_values,
                    ),

                "harmful_higher":
                    int(
                        math.isfinite(
                            delta
                        )
                        and delta
                        > FLOAT_TOLERANCE
                    ),
            }
        )

    return output


def stability_summary(
    block_rows,
):
    output = []

    for field in CALIBRATION_FEATURES:
        matching = [
            row
            for row in block_rows
            if row[
                "metric"
            ]
            == field
        ]

        finite_effects = [
            float(
                row[
                    "standardized_difference"
                ]
            )
            for row in matching
            if math.isfinite(
                float(
                    row[
                        "standardized_difference"
                    ]
                )
            )
        ]

        finite_aucs = [
            float(
                row[
                    "rank_auc_harmful_high"
                ]
            )
            for row in matching
            if math.isfinite(
                float(
                    row[
                        "rank_auc_harmful_high"
                    ]
                )
            )
        ]

        harmful_higher_count = sum(
            int(
                row[
                    "harmful_higher"
                ]
            )
            for row in matching
        )

        output.append(
            {
                "metric":
                    field,

                "blocks":
                    len(
                        matching
                    ),

                "harmful_higher_blocks":
                    harmful_higher_count,

                "direction_stability":
                    (
                        harmful_higher_count
                        / len(
                            matching
                        )
                        if matching
                        else float(
                            "nan"
                        )
                    ),

                "mean_standardized_difference":
                    (
                        safe_mean(
                            finite_effects
                        )
                        if finite_effects
                        else float(
                            "nan"
                        )
                    ),

                "min_standardized_difference":
                    (
                        min(
                            finite_effects
                        )
                        if finite_effects
                        else float(
                            "nan"
                        )
                    ),

                "max_standardized_difference":
                    (
                        max(
                            finite_effects
                        )
                        if finite_effects
                        else float(
                            "nan"
                        )
                    ),

                "mean_rank_auc":
                    (
                        safe_mean(
                            finite_aucs
                        )
                        if finite_aucs
                        else float(
                            "nan"
                        )
                    ),

                "min_rank_auc":
                    (
                        min(
                            finite_aucs
                        )
                        if finite_aucs
                        else float(
                            "nan"
                        )
                    ),

                "max_rank_auc":
                    (
                        max(
                            finite_aucs
                        )
                        if finite_aucs
                        else float(
                            "nan"
                        )
                    ),
            }
        )

    return output


def block_population_rows(
    all_events,
):
    output = []

    for block_name in BLOCKS:
        rows = [
            row
            for row in all_events
            if row[
                "block"
            ]
            == block_name
        ]

        beneficial = sum(
            int(
                row[
                    "class"
                ]
                == "beneficial"
            )
            for row in rows
        )

        harmful = sum(
            int(
                row[
                    "class"
                ]
                == "harmful"
            )
            for row in rows
        )

        seeds_with_harmful = len(
            {
                as_int(
                    row,
                    "generation_seed",
                )
                for row in rows
                if row[
                    "class"
                ]
                == "harmful"
            }
        )

        output.append(
            {
                "block":
                    block_name,

                "beneficial":
                    beneficial,

                "harmful":
                    harmful,

                "total":
                    beneficial
                    + harmful,

                "seeds_with_harmful":
                    seeds_with_harmful,
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
        "CROSS-BLOCK CONSTITUENT STABILITY ANALYSIS"
    )

    print(
        "=" * 210
    )

    print(
        f"blocks="
        f"{list(BLOCKS.keys())}"
    )

    print()

    print(
        "RECONSTRUCTING FROZEN HISTORICAL "
        "CALIBRATION MODEL"
    )

    calibration_model = (
        train_calibration_model()
    )

    all_events = []
    all_block_feature_rows = []

    print()

    print(
        "RECONSTRUCTING BLOCKS"
    )

    for (
        block_name,
        seeds,
    ) in BLOCKS.items():

        block_events = reconstruct_block_events(
            block_name,
            seeds,
            calibration_model,
        )

        all_events.extend(
            block_events
        )

        all_block_feature_rows.extend(
            block_feature_rows(
                block_name,
                block_events,
            )
        )

    population_rows = block_population_rows(
        all_events
    )

    stability_rows = stability_summary(
        all_block_feature_rows
    )

    print()

    print(
        "BLOCK POPULATIONS"
    )

    for row in population_rows:
        print(
            f"{row['block']:<20} "
            f"beneficial="
            f"{row['beneficial']} "
            f"harmful="
            f"{row['harmful']} "
            f"total="
            f"{row['total']} "
            f"harmful_seeds="
            f"{row['seeds_with_harmful']}"
        )

    print()

    print(
        "BLOCK-LEVEL FEATURE EFFECTS"
    )

    for block_name in BLOCKS:
        print()

        print(
            block_name
        )

        matching = [
            row
            for row in all_block_feature_rows
            if row[
                "block"
            ]
            == block_name
        ]

        for row in matching:
            effect = row[
                "standardized_difference"
            ]

            auc = row[
                "rank_auc_harmful_high"
            ]

            effect_text = (
                f"{effect:+.3f}"
                if math.isfinite(
                    effect
                )
                else "n/a"
            )

            auc_text = (
                f"{auc:.3f}"
                if math.isfinite(
                    auc
                )
                else "n/a"
            )

            print(
                f"  "
                f"{row['metric']:<40} "
                f"delta="
                f"{row['difference_harmful_minus_beneficial']:+.6f} "
                f"effect="
                f"{effect_text} "
                f"rank_AUC="
                f"{auc_text} "
                f"harmful_higher="
                f"{bool(row['harmful_higher'])}"
            )

    print()

    print(
        "CROSS-BLOCK STABILITY"
    )

    for row in stability_rows:
        print(
            f"{row['metric']:<40} "
            f"harmful_higher_blocks="
            f"{row['harmful_higher_blocks']}/"
            f"{row['blocks']} "
            f"direction_stability="
            f"{row['direction_stability']:.3%} "
            f"mean_effect="
            f"{row['mean_standardized_difference']:+.3f} "
            f"effect_range=["
            f"{row['min_standardized_difference']:+.3f},"
            f"{row['max_standardized_difference']:+.3f}"
            f"] "
            f"mean_rank_AUC="
            f"{row['mean_rank_auc']:.3f}"
        )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 105 evaluates block-to-block consistency "
        "rather than selecting a new controller feature."
    )

    print(
        "No new threshold, classifier, controller intervention, "
        "or prospective seed is introduced."
    )

    print(
        "A feature should not be considered stable merely because "
        "its pooled or average effect is large if its direction "
        "changes between blocks."
    )

    print(
        "=" * 210
    )

    summary_rows = []

    for row in stability_rows:
        copy = {
            "record_type":
                "stability_summary"
        }

        copy.update(
            row
        )

        summary_rows.append(
            copy
        )

    for row in all_block_feature_rows:
        copy = {
            "record_type":
                "block_feature"
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
        all_events,
    )

    save_csv(
        BLOCK_OUTPUT_PATH,
        population_rows,
    )

    print(
        f"Summary saved to: "
        f"{SUMMARY_OUTPUT_PATH}"
    )

    print(
        f"Cross-block events saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )

    print(
        f"Block populations saved to: "
        f"{BLOCK_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()