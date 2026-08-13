import csv
import math
import statistics
from pathlib import Path


INPUT_PATH = Path(
    "results/"
    "frozen_transient_state_guard_prospective_validation_events.csv"
)

OUTPUT_PATH = Path(
    "results/"
    "prospective_state_guard_selectivity_decomposition.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "prospective_state_guard_selectivity_decomposition_events.csv"
)

PRIMARY_STATE_THRESHOLD = 0.50
FLOAT_TOLERANCE = 1e-12


def read_csv(
    path: Path,
) -> list[dict]:

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


def save_csv(
    path: Path,
    rows: list[dict],
) -> None:

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

    normalized_rows = []

    for row in rows:

        copy = dict(
            row
        )

        for field in fields:

            copy.setdefault(
                field,
                "",
            )

        normalized_rows.append(
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
            normalized_rows
        )


def as_float(
    row: dict,
    field: str,
) -> float:

    return float(
        row[
            field
        ]
    )


def as_int(
    row: dict,
    field: str,
) -> int:

    return int(
        float(
            row[
                field
            ]
        )
    )


def is_primary_threshold(
    row: dict,
) -> bool:

    threshold = as_float(
        row,
        "state_threshold",
    )

    return (
        abs(
            threshold
            - PRIMARY_STATE_THRESHOLD
        )
        <= FLOAT_TOLERANCE
    )


def classify_event(
    row: dict,
) -> str:

    outcome = row[
        "baseline_outcome"
    ]

    vetoed = (
        as_int(
            row,
            "vetoed",
        )
        == 1
    )

    if outcome == "harmful":

        if vetoed:

            return "harmful_vetoed"

        return "harmful_preserved"

    if outcome == "beneficial":

        if vetoed:

            return "beneficial_vetoed"

        return "beneficial_preserved"

    if outcome == "neutral":

        if vetoed:

            return "neutral_vetoed"

        return "neutral_preserved"

    return "none"


def pooled_std(
    first: list[float],
    second: list[float],
) -> float:

    if (
        len(first) < 2
        or len(second) < 2
    ):

        return 0.0

    variance_first = statistics.variance(
        first
    )

    variance_second = statistics.variance(
        second
    )

    numerator = (
        (
            len(first)
            - 1
        )
        * variance_first
        +
        (
            len(second)
            - 1
        )
        * variance_second
    )

    denominator = (
        len(first)
        + len(second)
        - 2
    )

    if denominator <= 0:

        return 0.0

    return math.sqrt(
        max(
            0.0,
            numerator
            / denominator,
        )
    )


def standardized_difference(
    first: list[float],
    second: list[float],
) -> float:

    if (
        not first
        or not second
    ):

        return 0.0

    scale = pooled_std(
        first,
        second,
    )

    if (
        scale
        <= FLOAT_TOLERANCE
    ):

        return 0.0

    return (
        statistics.mean(
            first
        )
        - statistics.mean(
            second
        )
    ) / scale


def summarize_group(
    name: str,
    rows: list[dict],
    diagnostics: list[str],
) -> list[dict]:

    output = []

    for diagnostic in diagnostics:

        values = [
            as_float(
                row,
                diagnostic,
            )
            for row in rows
        ]

        if not values:
            continue

        output.append(
            {
                "record_type":
                    "group_summary",

                "group":
                    name,

                "diagnostic":
                    diagnostic,

                "count":
                    len(
                        values
                    ),

                "mean":
                    statistics.mean(
                        values
                    ),

                "median":
                    statistics.median(
                        values
                    ),

                "min":
                    min(
                        values
                    ),

                "max":
                    max(
                        values
                    ),
            }
        )

    return output


def comparison_rows(
    first_name: str,
    first_rows: list[dict],
    second_name: str,
    second_rows: list[dict],
    diagnostics: list[str],
) -> list[dict]:

    output = []

    for diagnostic in diagnostics:

        first_values = [
            as_float(
                row,
                diagnostic,
            )
            for row in first_rows
        ]

        second_values = [
            as_float(
                row,
                diagnostic,
            )
            for row in second_rows
        ]

        if (
            not first_values
            or not second_values
        ):

            continue

        output.append(
            {
                "record_type":
                    "comparison",

                "group":
                    (
                        f"{first_name}"
                        "_vs_"
                        f"{second_name}"
                    ),

                "diagnostic":
                    diagnostic,

                "count":
                    (
                        len(
                            first_values
                        )
                        + len(
                            second_values
                        )
                    ),

                "mean":
                    (
                        statistics.mean(
                            first_values
                        )
                        - statistics.mean(
                            second_values
                        )
                    ),

                "median":
                    "",

                "min":
                    "",

                "max":
                    "",

                "first_count":
                    len(
                        first_values
                    ),

                "second_count":
                    len(
                        second_values
                    ),

                "first_mean":
                    statistics.mean(
                        first_values
                    ),

                "second_mean":
                    statistics.mean(
                        second_values
                    ),

                "standardized_difference":
                    standardized_difference(
                        first_values,
                        second_values,
                    ),
            }
        )

    return output


def main() -> None:

    rows = read_csv(
        INPUT_PATH
    )

    primary_rows = [
        row
        for row in rows
        if is_primary_threshold(
            row
        )
    ]

    baseline_expansion_rows = [
        row
        for row in primary_rows
        if as_int(
            row,
            "baseline_expansion",
        )
        == 1
    ]

    event_rows = []

    for row in baseline_expansion_rows:

        event_class = classify_event(
            row
        )

        event = dict(
            row
        )

        event[
            "selectivity_class"
        ] = event_class

        event_rows.append(
            event
        )

    grouped = {
        "harmful_vetoed": [
            row
            for row in event_rows
            if row[
                "selectivity_class"
            ]
            == "harmful_vetoed"
        ],

        "harmful_preserved": [
            row
            for row in event_rows
            if row[
                "selectivity_class"
            ]
            == "harmful_preserved"
        ],

        "beneficial_vetoed": [
            row
            for row in event_rows
            if row[
                "selectivity_class"
            ]
            == "beneficial_vetoed"
        ],

        "beneficial_preserved": [
            row
            for row in event_rows
            if row[
                "selectivity_class"
            ]
            == "beneficial_preserved"
        ],

        "neutral_vetoed": [
            row
            for row in event_rows
            if row[
                "selectivity_class"
            ]
            == "neutral_vetoed"
        ],

        "neutral_preserved": [
            row
            for row in event_rows
            if row[
                "selectivity_class"
            ]
            == "neutral_preserved"
        ],
    }

    diagnostics = [
        "state_harmful_probability",
        "current_mismatch_indicator",
        "anchor_age",
        "trigger_score",
        "support_distance_baseline_action",
        "safety_score_baseline_action",
        "downside_score_baseline_action",
        "baseline_regret",
        "regret_difference_guard_minus_baseline",
    ]

    summary_rows = []

    for (
        group_name,
        group_rows,
    ) in grouped.items():

        summary_rows.extend(
            summarize_group(
                group_name,
                group_rows,
                diagnostics,
            )
        )

    key_comparisons = [
        (
            "harmful_vetoed",
            "beneficial_vetoed",
        ),
        (
            "harmful_vetoed",
            "beneficial_preserved",
        ),
        (
            "harmful_preserved",
            "beneficial_preserved",
        ),
        (
            "beneficial_vetoed",
            "beneficial_preserved",
        ),
    ]

    for (
        first_name,
        second_name,
    ) in key_comparisons:

        summary_rows.extend(
            comparison_rows(
                first_name,
                grouped[
                    first_name
                ],
                second_name,
                grouped[
                    second_name
                ],
                diagnostics,
            )
        )

    save_csv(
        OUTPUT_PATH,
        summary_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        event_rows,
    )

    total_expansions = len(
        event_rows
    )

    total_harmful = (
        len(
            grouped[
                "harmful_vetoed"
            ]
        )
        + len(
            grouped[
                "harmful_preserved"
            ]
        )
    )

    total_beneficial = (
        len(
            grouped[
                "beneficial_vetoed"
            ]
        )
        + len(
            grouped[
                "beneficial_preserved"
            ]
        )
    )

    harmful_vetoed = len(
        grouped[
            "harmful_vetoed"
        ]
    )

    beneficial_vetoed = len(
        grouped[
            "beneficial_vetoed"
        ]
    )

    harmful_veto_recall = (
        harmful_vetoed
        / total_harmful
        if total_harmful
        > 0
        else 0.0
    )

    beneficial_preservation = (
        len(
            grouped[
                "beneficial_preserved"
            ]
        )
        / total_beneficial
        if total_beneficial
        > 0
        else 0.0
    )

    veto_rows = [
        row
        for row in event_rows
        if as_int(
            row,
            "vetoed",
        )
        == 1
    ]

    preserved_rows = [
        row
        for row in event_rows
        if as_int(
            row,
            "vetoed",
        )
        == 0
    ]

    print(
        "=" * 205
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PROSPECTIVE STATE-GUARD "
        "SELECTIVITY DECOMPOSITION"
    )

    print(
        "=" * 205
    )

    print(
        f"input="
        f"{INPUT_PATH}"
    )

    print(
        f"primary threshold="
        f"{PRIMARY_STATE_THRESHOLD:.2f}"
    )

    print(
        f"baseline expansion events="
        f"{total_expansions}"
    )

    print()

    print(
        "SELECTIVITY COUNTS"
    )

    for group_name in [
        "harmful_vetoed",
        "harmful_preserved",
        "beneficial_vetoed",
        "beneficial_preserved",
        "neutral_vetoed",
        "neutral_preserved",
    ]:

        print(
            f"{group_name:<24} "
            f"n="
            f"{len(grouped[group_name])}"
        )

    print()

    print(
        f"pooled harmful veto recall="
        f"{harmful_veto_recall:.3%}"
    )

    print(
        f"pooled beneficial preservation="
        f"{beneficial_preservation:.3%}"
    )

    print(
        f"total vetoed events="
        f"{len(veto_rows)}"
    )

    print(
        f"total preserved events="
        f"{len(preserved_rows)}"
    )

    print()

    print(
        "GROUP DIAGNOSTICS"
    )

    core_diagnostics = [
        "state_harmful_probability",
        "current_mismatch_indicator",
        "anchor_age",
        "trigger_score",
        "support_distance_baseline_action",
        "safety_score_baseline_action",
        "downside_score_baseline_action",
    ]

    for group_name in [
        "harmful_vetoed",
        "harmful_preserved",
        "beneficial_vetoed",
        "beneficial_preserved",
    ]:

        group_rows = grouped[
            group_name
        ]

        print()

        print(
            f"{group_name} "
            f"(n={len(group_rows)})"
        )

        if not group_rows:

            print(
                "  no events"
            )

            continue

        for diagnostic in (
            core_diagnostics
        ):

            values = [
                as_float(
                    row,
                    diagnostic,
                )
                for row in group_rows
            ]

            print(
                f"  {diagnostic:<36} "
                f"mean="
                f"{statistics.mean(values):.6f} "
                f"median="
                f"{statistics.median(values):.6f} "
                f"range=["
                f"{min(values):.6f},"
                f"{max(values):.6f}"
                f"]"
            )

    print()

    print(
        "KEY STANDARDIZED COMPARISONS"
    )

    comparison_lookup = {
        (
            row[
                "group"
            ],
            row[
                "diagnostic"
            ],
        ):
            row
        for row in summary_rows
        if row[
            "record_type"
        ]
        == "comparison"
    }

    for comparison_name in [
        "harmful_vetoed_vs_beneficial_vetoed",
        "harmful_vetoed_vs_beneficial_preserved",
        "beneficial_vetoed_vs_beneficial_preserved",
    ]:

        print()

        print(
            comparison_name
        )

        available = []

        for diagnostic in (
            core_diagnostics
        ):

            key = (
                comparison_name,
                diagnostic,
            )

            if (
                key
                not in comparison_lookup
            ):

                continue

            row = comparison_lookup[
                key
            ]

            available.append(
                (
                    diagnostic,
                    float(
                        row[
                            "standardized_difference"
                        ]
                    ),
                    float(
                        row[
                            "first_mean"
                        ]
                    ),
                    float(
                        row[
                            "second_mean"
                        ]
                    ),
                )
            )

        available.sort(
            key=lambda item: abs(
                item[
                    1
                ]
            ),
            reverse=True,
        )

        for (
            diagnostic,
            effect,
            first_mean,
            second_mean,
        ) in available:

            print(
                f"  {diagnostic:<36} "
                f"effect="
                f"{effect:+.3f} "
                f"first="
                f"{first_mean:.6f} "
                f"second="
                f"{second_mean:.6f}"
            )

    print()

    print(
        "HARMFUL EVENTS"
    )

    harmful_rows = (
        grouped[
            "harmful_vetoed"
        ]
        + grouped[
            "harmful_preserved"
        ]
    )

    if not harmful_rows:

        print(
            "No harmful baseline expansion events."
        )

    else:

        harmful_rows.sort(
            key=lambda row: (
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
            )
        )

        for row in harmful_rows:

            print(
                f"seed="
                f"{row['generation_seed']} "
                f"index="
                f"{row['test_index']} "
                f"class="
                f"{row['selectivity_class']} "
                f"q="
                f"{as_float(row, 'state_harmful_probability'):.3f} "
                f"mismatch="
                f"{as_float(row, 'current_mismatch_indicator'):.3f} "
                f"anchor_age="
                f"{as_float(row, 'anchor_age'):.1f} "
                f"trigger="
                f"{as_float(row, 'trigger_score'):.3f} "
                f"support="
                f"{as_float(row, 'support_distance_baseline_action'):.3f} "
                f"safety="
                f"{as_float(row, 'safety_score_baseline_action'):.3f} "
                f"downside="
                f"{as_float(row, 'downside_score_baseline_action'):.6f}"
            )

    print(
        "=" * 205
    )

    print(
        f"Summary saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Event decomposition saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()