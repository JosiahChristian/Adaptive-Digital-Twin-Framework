import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path


SMALL_PATH = Path(
    "results/multiseed_generative_persistence_robustness.csv"
)

EXPANDED_PATH = Path(
    "results/expanded_multiseed_generative_persistence_robustness.csv"
)

OUTPUT_PATH = Path(
    "results/cross_population_generative_persistence_statistics.csv"
)


POLICIES = [
    "direct_loss",
    "fixed_risk_0.010",
    "two_stage_0.10",
    "two_stage_0.25",
    "two_stage_1.00",
    "fixed_k3",
    "oracle",
]

METRICS = [
    "mean_regret",
    "under_count",
    "over_count",
    "action_entropy",
    "pareto_efficient",
]


def load_rows(
    path: Path,
    population: str,
) -> list[dict]:

    rows = []

    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(
            file
        )

        for row in reader:

            record = dict(
                row
            )

            record[
                "population"
            ] = population

            record[
                "seed"
            ] = int(
                record[
                    "seed"
                ]
            )

            for metric in METRICS:

                record[
                    metric
                ] = float(
                    record[
                        metric
                    ]
                )

            rows.append(
                record
            )

    return rows


def mean_ci_95(
    values: list[float],
) -> tuple[
    float,
    float,
    float,
]:

    n = len(
        values
    )

    mean_value = statistics.mean(
        values
    )

    if n < 2:

        return (
            mean_value,
            mean_value,
            mean_value,
        )

    std = statistics.stdev(
        values
    )

    standard_error = (
        std
        / math.sqrt(
            n
        )
    )

    margin = (
        1.96
        * standard_error
    )

    return (
        mean_value,
        mean_value - margin,
        mean_value + margin,
    )


def population_policy_rows(
    rows: list[dict],
) -> dict[
    tuple[
        str,
        str,
    ],
    list[dict],
]:

    grouped = defaultdict(
        list
    )

    for row in rows:

        key = (
            row[
                "population"
            ],
            row[
                "policy"
            ],
        )

        grouped[
            key
        ].append(
            row
        )

    return grouped


def summarize_population_policy(
    grouped: dict,
) -> list[dict]:

    output = []

    for population in (
        "seed_000_009",
        "seed_100_139",
    ):

        for policy in POLICIES:

            rows = grouped[
                (
                    population,
                    policy,
                )
            ]

            for metric in METRICS:

                values = [
                    float(
                        row[
                            metric
                        ]
                    )
                    for row in rows
                ]

                (
                    mean_value,
                    ci_low,
                    ci_high,
                ) = mean_ci_95(
                    values
                )

                output.append(
                    {
                        "analysis":
                            "population_summary",

                        "population":
                            population,

                        "policy":
                            policy,

                        "reference_policy":
                            "",

                        "metric":
                            metric,

                        "n":
                            len(
                                values
                            ),

                        "mean":
                            mean_value,

                        "ci95_low":
                            ci_low,

                        "ci95_high":
                            ci_high,

                        "mean_delta":
                            "",

                        "win_rate":
                            "",

                        "direction_agreement":
                            "",
                    }
                )

    return output


def paired_policy_comparison(
    grouped: dict,
    reference_policy: str,
) -> list[dict]:

    output = []

    for population in (
        "seed_000_009",
        "seed_100_139",
    ):

        reference_rows = {
            row[
                "seed"
            ]: row
            for row in grouped[
                (
                    population,
                    reference_policy,
                )
            ]
        }

        for policy in POLICIES:

            if (
                policy
                == reference_policy
            ):
                continue

            policy_rows = {
                row[
                    "seed"
                ]: row
                for row in grouped[
                    (
                        population,
                        policy,
                    )
                ]
            }

            shared_seeds = sorted(
                set(
                    reference_rows
                )
                & set(
                    policy_rows
                )
            )

            for metric in METRICS:

                deltas = []

                wins = 0

                for seed in shared_seeds:

                    policy_value = float(
                        policy_rows[
                            seed
                        ][
                            metric
                        ]
                    )

                    reference_value = float(
                        reference_rows[
                            seed
                        ][
                            metric
                        ]
                    )

                    delta = (
                        policy_value
                        - reference_value
                    )

                    deltas.append(
                        delta
                    )

                    if metric in {
                        "mean_regret",
                        "under_count",
                        "over_count",
                    }:

                        if (
                            policy_value
                            < reference_value
                        ):
                            wins += 1

                    else:

                        if (
                            policy_value
                            > reference_value
                        ):
                            wins += 1

                (
                    mean_delta,
                    ci_low,
                    ci_high,
                ) = mean_ci_95(
                    deltas
                )

                output.append(
                    {
                        "analysis":
                            "paired_comparison",

                        "population":
                            population,

                        "policy":
                            policy,

                        "reference_policy":
                            reference_policy,

                        "metric":
                            metric,

                        "n":
                            len(
                                deltas
                            ),

                        "mean":
                            "",

                        "ci95_low":
                            ci_low,

                        "ci95_high":
                            ci_high,

                        "mean_delta":
                            mean_delta,

                        "win_rate":
                            (
                                wins
                                / len(
                                    shared_seeds
                                )
                            ),

                        "direction_agreement":
                            "",
                    }
                )

    return output


def cross_population_direction_stability(
    paired_rows: list[dict],
) -> list[dict]:

    indexed = defaultdict(
        dict
    )

    for row in paired_rows:

        key = (
            row[
                "policy"
            ],
            row[
                "reference_policy"
            ],
            row[
                "metric"
            ],
        )

        indexed[
            key
        ][
            row[
                "population"
            ]
        ] = row

    output = []

    for key, populations in indexed.items():

        if (
            "seed_000_009"
            not in populations
            or
            "seed_100_139"
            not in populations
        ):
            continue

        first = populations[
            "seed_000_009"
        ]

        second = populations[
            "seed_100_139"
        ]

        first_delta = float(
            first[
                "mean_delta"
            ]
        )

        second_delta = float(
            second[
                "mean_delta"
            ]
        )

        same_direction = int(
            (
                first_delta == 0.0
                and second_delta == 0.0
            )
            or (
                first_delta > 0.0
                and second_delta > 0.0
            )
            or (
                first_delta < 0.0
                and second_delta < 0.0
            )
        )

        (
            policy,
            reference_policy,
            metric,
        ) = key

        output.append(
            {
                "analysis":
                    "cross_population_stability",

                "population":
                    "combined",

                "policy":
                    policy,

                "reference_policy":
                    reference_policy,

                "metric":
                    metric,

                "n":
                    2,

                "mean":
                    "",

                "ci95_low":
                    "",

                "ci95_high":
                    "",

                "mean_delta":
                    statistics.mean(
                        [
                            first_delta,
                            second_delta,
                        ]
                    ),

                "win_rate":
                    statistics.mean(
                        [
                            float(
                                first[
                                    "win_rate"
                                ]
                            ),
                            float(
                                second[
                                    "win_rate"
                                ]
                            ),
                        ]
                    ),

                "direction_agreement":
                    same_direction,
            }
        )

    return output


def save_results(
    rows: list[dict],
) -> None:

    OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        fieldnames = [
            "analysis",
            "population",
            "policy",
            "reference_policy",
            "metric",
            "n",
            "mean",
            "ci95_low",
            "ci95_high",
            "mean_delta",
            "win_rate",
            "direction_agreement",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(
            rows
        )


def print_key_results(
    rows: list[dict],
) -> None:

    print(
        "=" * 120
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "CROSS-POPULATION GENERATIVE "
        "PERSISTENCE STATISTICS"
    )

    print(
        "=" * 120
    )

    print()

    print(
        "REFERENCE: direct_loss"
    )

    for row in rows:

        if (
            row[
                "analysis"
            ]
            != "paired_comparison"
        ):
            continue

        if (
            row[
                "reference_policy"
            ]
            != "direct_loss"
        ):
            continue

        if (
            row[
                "policy"
            ]
            != "two_stage_1.00"
        ):
            continue

        if row[
            "metric"
        ] not in {
            "mean_regret",
            "under_count",
            "over_count",
            "action_entropy",
        }:
            continue

        print(
            f"{row['population']:<15} "
            f"{row['metric']:<15} "
            f"delta="
            f"{float(row['mean_delta']):+.6f} "
            f"95%CI=["
            f"{float(row['ci95_low']):+.6f},"
            f"{float(row['ci95_high']):+.6f}] "
            f"win_rate="
            f"{float(row['win_rate']):.1%}"
        )

    print()
    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


def main() -> None:

    rows = []

    rows.extend(
        load_rows(
            SMALL_PATH,
            "seed_000_009",
        )
    )

    rows.extend(
        load_rows(
            EXPANDED_PATH,
            "seed_100_139",
        )
    )

    grouped = (
        population_policy_rows(
            rows
        )
    )

    population_summary = (
        summarize_population_policy(
            grouped
        )
    )

    paired_direct = (
        paired_policy_comparison(
            grouped,
            "direct_loss",
        )
    )

    paired_two_stage = (
        paired_policy_comparison(
            grouped,
            "two_stage_1.00",
        )
    )

    paired_rows = (
        paired_direct
        + paired_two_stage
    )

    stability = (
        cross_population_direction_stability(
            paired_rows
        )
    )

    output = (
        population_summary
        + paired_rows
        + stability
    )

    save_results(
        output
    )

    print_key_results(
        output
    )


if __name__ == "__main__":
    main()
