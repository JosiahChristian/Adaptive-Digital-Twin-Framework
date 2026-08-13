import csv
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from experiments.adaptive_release_persistence_policy import (
    PERSISTENCE_LEVELS,
)
from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)


OUTPUT_PATH = Path(
    "results/"
    "directional_regret_asymmetry_analysis.csv"
)

CONSEQUENTIAL_REGRET_THRESHOLD = 0.005


def selected_loss(
    row: dict,
    persistence: int,
) -> float:

    return float(
        row[
            f"loss_k{persistence}"
        ]
    )


def regret(
    row: dict,
    persistence: int,
) -> float:

    return (
        selected_loss(
            row,
            persistence,
        )
        - float(
            row[
                "best_loss"
            ]
        )
    )


def directional_category(
    selected: int,
    optimal: int,
) -> str:

    if selected < optimal:
        return "insufficient_persistence"

    if selected > optimal:
        return "excessive_persistence"

    return "optimal"


def generate_directional_rows() -> list[dict]:

    rows = generate_analysis_rows()

    output = []

    for row in rows:

        optimal = int(
            row[
                "best_persistence"
            ]
        )

        for selected in (
            PERSISTENCE_LEVELS
        ):

            selected_regret = regret(
                row,
                selected,
            )

            output.append(
                {
                    "context_index":
                        int(
                            row[
                                "context_index"
                            ]
                        ),

                    "optimal_persistence":
                        optimal,

                    "selected_persistence":
                        selected,

                    "direction":
                        directional_category(
                            selected,
                            optimal,
                        ),

                    "best_loss":
                        float(
                            row[
                                "best_loss"
                            ]
                        ),

                    "selected_loss":
                        selected_loss(
                            row,
                            selected,
                        ),

                    "regret":
                        selected_regret,

                    "consequential_regret":
                        int(
                            selected_regret
                            >
                            CONSEQUENTIAL_REGRET_THRESHOLD
                        ),

                    "absolute_margin":
                        float(
                            row[
                                "absolute_margin"
                            ]
                        ),

                    "total_spread":
                        float(
                            row[
                                "total_spread"
                            ]
                        ),
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

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()

        writer.writerows(
            rows
        )


def summarize_regrets(
    rows: list[dict],
) -> dict:

    regrets = [
        float(
            row[
                "regret"
            ]
        )
        for row in rows
    ]

    consequential_fraction = (
        sum(
            int(
                row[
                    "consequential_regret"
                ]
            )
            for row in rows
        )
        / len(rows)
    )

    positive_fraction = (
        sum(
            value > 1e-12
            for value in regrets
        )
        / len(regrets)
    )

    return {
        "n":
            len(
                rows
            ),

        "mean_regret":
            statistics.mean(
                regrets
            ),

        "median_regret":
            statistics.median(
                regrets
            ),

        "max_regret":
            max(
                regrets
            ),

        "positive_regret_fraction":
            positive_fraction,

        "consequential_regret_fraction":
            consequential_fraction,
    }


def print_summary_line(
    label: str,
    summary: dict,
) -> None:

    print(
        f"{label:<28} "
        f"n="
        f"{summary['n']:<4} "
        f"mean_regret="
        f"{summary['mean_regret']:.6f} "
        f"median_regret="
        f"{summary['median_regret']:.6f} "
        f"max_regret="
        f"{summary['max_regret']:.6f} "
        f"positive_regret="
        f"{summary['positive_regret_fraction']:.3%} "
        f"regret>0.005="
        f"{summary['consequential_regret_fraction']:.3%}"
    )


def print_directional_summary(
    rows: list[dict],
) -> None:

    print()
    print(
        "DIRECTIONAL REGRET SUMMARY"
    )

    groups = defaultdict(list)

    for row in rows:

        groups[
            row[
                "direction"
            ]
        ].append(
            row
        )

    for direction in (
        "insufficient_persistence",
        "excessive_persistence",
        "optimal",
    ):

        group = groups[
            direction
        ]

        if not group:
            continue

        print_summary_line(
            direction,
            summarize_regrets(
                group
            ),
        )


def print_action_pair_summary(
    rows: list[dict],
) -> None:

    print()
    print(
        "ACTION-PAIR REGRET"
    )

    groups = defaultdict(list)

    for row in rows:

        optimal = int(
            row[
                "optimal_persistence"
            ]
        )

        selected = int(
            row[
                "selected_persistence"
            ]
        )

        if selected == optimal:
            continue

        groups[
            (
                optimal,
                selected,
            )
        ].append(
            row
        )

    for optimal in (
        PERSISTENCE_LEVELS
    ):

        for selected in (
            PERSISTENCE_LEVELS
        ):

            if selected == optimal:
                continue

            group = groups[
                (
                    optimal,
                    selected,
                )
            ]

            if not group:
                continue

            print_summary_line(
                (
                    f"k*={optimal} -> "
                    f"k={selected}"
                ),
                summarize_regrets(
                    group
                ),
            )


def print_by_optimal_persistence(
    rows: list[dict],
) -> None:

    print()
    print(
        "REGRET BY TRUE OPTIMAL PERSISTENCE"
    )

    groups = defaultdict(list)

    for row in rows:

        if (
            int(
                row[
                    "selected_persistence"
                ]
            )
            ==
            int(
                row[
                    "optimal_persistence"
                ]
            )
        ):
            continue

        groups[
            int(
                row[
                    "optimal_persistence"
                ]
            )
        ].append(
            row
        )

    for persistence in (
        PERSISTENCE_LEVELS
    ):

        group = groups[
            persistence
        ]

        if not group:
            continue

        print_summary_line(
            f"optimal k={persistence}",
            summarize_regrets(
                group
            ),
        )


def print_direction_counts(
    rows: list[dict],
) -> None:

    print()
    print(
        "DIRECTION COUNTS"
    )

    counts = Counter(
        row[
            "direction"
        ]
        for row in rows
    )

    total = len(
        rows
    )

    for direction in (
        "insufficient_persistence",
        "excessive_persistence",
        "optimal",
    ):

        count = counts[
            direction
        ]

        print(
            f"{direction:<28} "
            f"{count} "
            f"({count / total:.3%})"
        )


def compute_asymmetry_ratio(
    rows: list[dict],
) -> None:

    insufficient = [
        row
        for row in rows
        if row[
            "direction"
        ]
        ==
        "insufficient_persistence"
    ]

    excessive = [
        row
        for row in rows
        if row[
            "direction"
        ]
        ==
        "excessive_persistence"
    ]

    insufficient_summary = (
        summarize_regrets(
            insufficient
        )
    )

    excessive_summary = (
        summarize_regrets(
            excessive
        )
    )

    insufficient_mean = (
        insufficient_summary[
            "mean_regret"
        ]
    )

    excessive_mean = (
        excessive_summary[
            "mean_regret"
        ]
    )

    print()
    print(
        "ASYMMETRY METRICS"
    )

    print(
        "mean insufficient-persistence "
        "regret="
        f"{insufficient_mean:.6f}"
    )

    print(
        "mean excessive-persistence "
        "regret="
        f"{excessive_mean:.6f}"
    )

    if excessive_mean > 0:

        ratio = (
            insufficient_mean
            / excessive_mean
        )

        print(
            "mean regret asymmetry ratio "
            "(insufficient/excessive)="
            f"{ratio:.3f}"
        )

    else:

        print(
            "mean regret asymmetry ratio "
            "(insufficient/excessive)="
            "undefined"
        )

    insufficient_consequential = (
        insufficient_summary[
            "consequential_regret_fraction"
        ]
    )

    excessive_consequential = (
        excessive_summary[
            "consequential_regret_fraction"
        ]
    )

    print(
        "consequential insufficient "
        "fraction="
        f"{insufficient_consequential:.3%}"
    )

    print(
        "consequential excessive "
        "fraction="
        f"{excessive_consequential:.3%}"
    )


def main() -> None:

    rows = (
        generate_directional_rows()
    )

    save_results(
        rows
    )

    print("=" * 150)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "DIRECTIONAL REGRET "
        "ASYMMETRY ANALYSIS"
    )

    print("=" * 150)

    context_count = len(
        {
            int(
                row[
                    "context_index"
                ]
            )
            for row in rows
        }
    )

    print(
        f"decision contexts="
        f"{context_count}"
    )

    print(
        f"evaluated action decisions="
        f"{len(rows)}"
    )

    print_direction_counts(
        rows
    )

    print_directional_summary(
        rows
    )

    print_action_pair_summary(
        rows
    )

    print_by_optimal_persistence(
        rows
    )

    compute_asymmetry_ratio(
        rows
    )

    print("=" * 150)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()