import csv
import math
from pathlib import Path

from scipy.stats import fisher_exact


INPUT_PATH = Path(
    "results/"
    "harmful_expansion_action_conditioned_epistemic_excess_analysis_events.csv"
)

SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "independent_historical_action_harm_replication.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "independent_historical_action_harm_replication_events.csv"
)


EXPECTED_SEED_MIN = 44001
EXPECTED_SEED_MAX = 44010

ACTIONS = [
    1,
    2,
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
        seed = int(
            float(
                row[
                    "generation_seed"
                ]
            )
        )

        expanded_action = int(
            float(
                row[
                    "expanded_action"
                ]
            )
        )

        reconstructed_action = int(
            float(
                row[
                    "expanded_action_reconstructed"
                ]
            )
        )

        if expanded_action != reconstructed_action:
            raise RuntimeError(
                "expanded_action does not match "
                "expanded_action_reconstructed for "
                f"seed={seed}, "
                f"test_index={row['test_index']}"
            )

        outcome = row[
            "outcome"
        ]

        if outcome not in {
            "beneficial",
            "harmful",
        }:
            raise RuntimeError(
                f"Unexpected outcome label: {outcome}"
            )

        copy = dict(
            row
        )

        copy[
            "generation_seed"
        ] = seed

        copy[
            "expanded_action"
        ] = expanded_action

        copy[
            "expanded_action_reconstructed"
        ] = reconstructed_action

        copy[
            "harmful_target"
        ] = int(
            outcome
            == "harmful"
        )

        output.append(
            copy
        )

    seeds = sorted(
        {
            row[
                "generation_seed"
            ]
            for row in output
        }
    )

    if not seeds:
        raise RuntimeError(
            "No replication events found."
        )

    if min(
        seeds
    ) != EXPECTED_SEED_MIN:
        raise RuntimeError(
            "Unexpected minimum seed: "
            f"{min(seeds)}"
        )

    if max(
        seeds
    ) != EXPECTED_SEED_MAX:
        raise RuntimeError(
            "Unexpected maximum seed: "
            f"{max(seeds)}"
        )

    return output


def wilson_interval(
    successes,
    total,
    z=1.959963984540054,
):
    if total == 0:
        return (
            float(
                "nan"
            ),
            float(
                "nan"
            ),
        )

    p = (
        successes
        / total
    )

    denominator = (
        1.0
        + (
            z
            * z
        )
        / total
    )

    center = (
        p
        + (
            z
            * z
        )
        / (
            2.0
            * total
        )
    ) / denominator

    margin = (
        z
        * math.sqrt(
            (
                p
                * (
                    1.0
                    - p
                )
                / total
            )
            + (
                z
                * z
            )
            / (
                4.0
                * total
                * total
            )
        )
        / denominator
    )

    return (
        max(
            0.0,
            center
            - margin
        ),
        min(
            1.0,
            center
            + margin
        ),
    )


def action_summary(
    rows,
    action,
):
    matching = [
        row
        for row in rows
        if int(
            row[
                "expanded_action"
            ]
        )
        == action
    ]

    harmful = sum(
        int(
            row[
                "harmful_target"
            ]
        )
        for row in matching
    )

    beneficial = (
        len(
            matching
        )
        - harmful
    )

    harmful_rate = (
        harmful
        / len(
            matching
        )
        if matching
        else float(
            "nan"
        )
    )

    (
        ci_low,
        ci_high,
    ) = wilson_interval(
        harmful,
        len(
            matching
        ),
    )

    harmful_seeds = sorted(
        {
            int(
                row[
                    "generation_seed"
                ]
            )
            for row in matching
            if int(
                row[
                    "harmful_target"
                ]
            )
            == 1
        }
    )

    return {
        "record_type":
            "action_summary",

        "action":
            action,

        "rows":
            len(
                matching
            ),

        "harmful":
            harmful,

        "beneficial":
            beneficial,

        "harmful_rate":
            harmful_rate,

        "harmful_rate_ci_low":
            ci_low,

        "harmful_rate_ci_high":
            ci_high,

        "harmful_seed_count":
            len(
                harmful_seeds
            ),

        "harmful_seeds":
            "|".join(
                str(
                    seed
                )
                for seed in harmful_seeds
            ),
    }


def fisher_test(
    action_1,
    action_2,
):
    table = [
        [
            int(
                action_1[
                    "harmful"
                ]
            ),
            int(
                action_1[
                    "beneficial"
                ]
            ),
        ],
        [
            int(
                action_2[
                    "harmful"
                ]
            ),
            int(
                action_2[
                    "beneficial"
                ]
            ),
        ],
    ]

    odds_ratio, p_value = fisher_exact(
        table,
        alternative="two-sided",
    )

    return (
        float(
            odds_ratio
        ),
        float(
            p_value
        ),
    )


def replication_classification(
    action_1,
    action_2,
):
    rate_1 = float(
        action_1[
            "harmful_rate"
        ]
    )

    rate_2 = float(
        action_2[
            "harmful_rate"
        ]
    )

    total_harmful = (
        int(
            action_1[
                "harmful"
            ]
        )
        + int(
            action_2[
                "harmful"
            ]
        )
    )

    if total_harmful == 0:
        return (
            "uninformative",
            "No harmful support expansions were observed "
            "in the independent replication population.",
        )

    if not (
        math.isfinite(
            rate_1
        )
        and math.isfinite(
            rate_2
        )
    ):
        return (
            "uninformative",
            "One action had no observed support expansions, "
            "so directional harmful-rate replication cannot "
            "be evaluated.",
        )

    if rate_1 > rate_2:
        return (
            "replicated",
            "The preregistered direction replicated: "
            "action 1 has a higher harmful-expansion rate "
            "than action 2.",
        )

    if rate_1 < rate_2:
        return (
            "directionally_contradicted",
            "The preregistered direction was contradicted: "
            "action 2 has a higher harmful-expansion rate "
            "than action 1.",
        )

    return (
        "uninformative",
        "The two actions have equal observed harmful-expansion "
        "rates in the replication population.",
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
    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "INDEPENDENT HISTORICAL ACTION-HARM REPLICATION"
    )

    print(
        "=" * 210
    )

    print(
        f"input="
        f"{INPUT_PATH}"
    )

    print(
        f"expected seed range="
        f"{EXPECTED_SEED_MIN}-"
        f"{EXPECTED_SEED_MAX}"
    )

    print(
        "primary directional replication criterion:"
    )

    print(
        "harmful expansion rate(action 1) "
        "> harmful expansion rate(action 2)"
    )

    print()

    rows = read_events()

    seeds = sorted(
        {
            int(
                row[
                    "generation_seed"
                ]
            )
            for row in rows
        }
    )

    print(
        "REPLICATION POPULATION"
    )

    print(
        f"rows="
        f"{len(rows)}"
    )

    print(
        f"seed_count="
        f"{len(seeds)}"
    )

    print(
        f"seed_range="
        f"{min(seeds)}-"
        f"{max(seeds)}"
    )

    print(
        f"total harmful="
        f"{sum(row['harmful_target'] for row in rows)}"
    )

    print(
        f"total beneficial="
        f"{sum(1 - row['harmful_target'] for row in rows)}"
    )

    print()

    summaries = {
        action:
            action_summary(
                rows,
                action,
            )
        for action in ACTIONS
    }

    print(
        "PREREGISTERED ACTION-SPECIFIC ENDPOINTS"
    )

    for action in ACTIONS:
        row = summaries[
            action
        ]

        print()

        print(
            f"action={action}"
        )

        print(
            f"  expansions="
            f"{row['rows']}"
        )

        print(
            f"  harmful="
            f"{row['harmful']}"
        )

        print(
            f"  beneficial="
            f"{row['beneficial']}"
        )

        print(
            f"  harmful_rate="
            f"{row['harmful_rate']:.3%}"
        )

        print(
            f"  95% Wilson CI=["
            f"{row['harmful_rate_ci_low']:.3%},"
            f"{row['harmful_rate_ci_high']:.3%}"
            f"]"
        )

        print(
            f"  harmful_seed_count="
            f"{row['harmful_seed_count']}"
        )

        print(
            f"  harmful_seeds="
            f"{row['harmful_seeds']}"
        )

    action_1 = summaries[
        1
    ]

    action_2 = summaries[
        2
    ]

    rate_difference = (
        float(
            action_1[
                "harmful_rate"
            ]
        )
        - float(
            action_2[
                "harmful_rate"
            ]
        )
    )

    print()

    print(
        "ACTION-HARM EFFECT"
    )

    print(
        f"harmful rate difference "
        f"(action1-action2)="
        f"{rate_difference:+.3%}"
    )

    (
        odds_ratio,
        fisher_p,
    ) = fisher_test(
        action_1,
        action_2,
    )

    print(
        f"Fisher exact odds ratio="
        f"{odds_ratio}"
    )

    print(
        f"Fisher exact two-sided p="
        f"{fisher_p:.6f}"
    )

    (
        replication_status,
        interpretation,
    ) = replication_classification(
        action_1,
        action_2,
    )

    print()

    print(
        "PRIMARY REPLICATION RESULT"
    )

    print(
        f"status="
        f"{replication_status}"
    )

    print(
        interpretation
    )

    action_2_zero_harm = int(
        int(
            action_2[
                "harmful"
            ]
        )
        == 0
    )

    print()

    print(
        "SECONDARY EXACT-PATTERN CHECK"
    )

    print(
        f"action 2 zero harmful events="
        f"{bool(action_2_zero_harm)}"
    )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 116 uses an independent earlier historical "
        "population selected before harmful-by-action counts were "
        "inspected."
    )

    print(
        "The primary replication criterion is directional: "
        "action 1 harmful-expansion rate must exceed action 2."
    )

    print(
        "Reproduction of the exact Experiment 115 pattern "
        "(zero harmful action-2 events) is secondary and was "
        "not required for directional replication."
    )

    print(
        "No risk threshold, controller intervention, prospective "
        "seed, or action-conditioned policy is introduced."
    )

    print(
        "=" * 210
    )

    output_rows = []

    output_rows.extend(
        summaries[
            action
        ]
        for action in ACTIONS
    )

    output_rows.append(
        {
            "record_type":
                "replication_summary",

            "seed_min":
                min(
                    seeds
                ),

            "seed_max":
                max(
                    seeds
                ),

            "rows":
                len(
                    rows
                ),

            "action1_harmful_rate":
                action_1[
                    "harmful_rate"
                ],

            "action2_harmful_rate":
                action_2[
                    "harmful_rate"
                ],

            "harmful_rate_difference_action1_minus_action2":
                rate_difference,

            "fisher_odds_ratio":
                odds_ratio,

            "fisher_two_sided_p":
                fisher_p,

            "directional_replication_status":
                replication_status,

            "action2_zero_harmful_events":
                action_2_zero_harm,
        }
    )

    save_csv(
        SUMMARY_OUTPUT_PATH,
        output_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        rows,
    )

    print(
        f"Summary saved to: "
        f"{SUMMARY_OUTPUT_PATH}"
    )

    print(
        f"Replication events saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()