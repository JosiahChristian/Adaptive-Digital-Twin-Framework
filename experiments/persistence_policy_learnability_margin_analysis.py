import csv
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from experiments.adaptive_release_persistence_policy import (
    PERSISTENCE_LEVELS,
    build_models,
    build_training_contexts,
)

from experiments.benefit_aware_epistemic_memory_gating import (
    generate_trajectories,
    split_trajectories,
)


OUTPUT_PATH = Path(
    "results/"
    "persistence_policy_learnability_margin_analysis.csv"
)


MARGIN_THRESHOLDS = [
    0.0000,
    0.0005,
    0.0010,
    0.0025,
    0.0050,
    0.0100,
]


def ranked_losses(
    row: dict,
) -> list[
    tuple[
        int,
        float,
    ]
]:

    values = [
        (
            1,
            float(
                row[
                    "loss_k1"
                ]
            ),
        ),
        (
            2,
            float(
                row[
                    "loss_k2"
                ]
            ),
        ),
        (
            3,
            float(
                row[
                    "loss_k3"
                ]
            ),
        ),
    ]

    return sorted(
        values,
        key=lambda item: (
            item[1],
            item[0],
        ),
    )


def enrich_rows(
    rows: list[dict],
) -> list[dict]:

    output = []

    for index, row in enumerate(
        rows
    ):

        ranked = ranked_losses(
            row
        )

        best_k, best_loss = ranked[
            0
        ]

        second_k, second_loss = ranked[
            1
        ]

        worst_k, worst_loss = ranked[
            2
        ]

        absolute_margin = (
            second_loss
            - best_loss
        )

        total_spread = (
            worst_loss
            - best_loss
        )

        relative_margin = (
            absolute_margin
            / (
                abs(
                    best_loss
                )
                + 1e-12
            )
        )

        relative_spread = (
            total_spread
            / (
                abs(
                    best_loss
                )
                + 1e-12
            )
        )

        output.append(
            {
                "context_index":
                    index,

                "best_persistence":
                    best_k,

                "second_persistence":
                    second_k,

                "worst_persistence":
                    worst_k,

                "loss_k1":
                    float(
                        row[
                            "loss_k1"
                        ]
                    ),

                "loss_k2":
                    float(
                        row[
                            "loss_k2"
                        ]
                    ),

                "loss_k3":
                    float(
                        row[
                            "loss_k3"
                        ]
                    ),

                "best_loss":
                    best_loss,

                "second_loss":
                    second_loss,

                "worst_loss":
                    worst_loss,

                "absolute_margin":
                    absolute_margin,

                "relative_margin":
                    relative_margin,

                "total_spread":
                    total_spread,

                "relative_spread":
                    relative_spread,

                "benefit_probability":
                    float(
                        row[
                            "benefit_probability"
                        ]
                    ),

                "release_probability":
                    float(
                        row[
                            "release_probability"
                        ]
                    ),

                "anchor_age":
                    float(
                        row[
                            "anchor_age"
                        ]
                    ),

                "trigger_score":
                    float(
                        row[
                            "trigger_score"
                        ]
                    ),

                "feature_distance":
                    float(
                        row[
                            "feature_distance"
                        ]
                    ),

                "current_mismatch_indicator":
                    float(
                        row[
                            "current_mismatch_indicator"
                        ]
                    ),

                "current_parameter_estimate":
                    float(
                        row[
                            "current_parameter_estimate"
                        ]
                    ),
            }
        )

    return output


def generate_analysis_rows(
    base_seed: int | None = None,
) -> list[dict]:

    trajectories = (
        generate_trajectories()
        if base_seed is None
        else generate_trajectories(
            base_seed=base_seed
        )
    )

    (
        memory_fit,
        gate_train,
        _,
    ) = split_trajectories(
        trajectories
    )

    (
        models,
        release_model,
    ) = build_models(
        memory_fit=memory_fit,
        gate_train=gate_train,
    )

    training_contexts = (
        build_training_contexts(
            trajectories=gate_train,
            models=models,
            release_model=release_model,
        )
    )

    return enrich_rows(
        training_contexts
    )


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


def print_distribution_summary(
    rows: list[dict],
) -> None:

    counts = Counter(
        int(
            row[
                "best_persistence"
            ]
        )
        for row in rows
    )

    print(
        "BEST-PERSISTENCE DISTRIBUTION"
    )

    for persistence in (
        PERSISTENCE_LEVELS
    ):

        count = counts[
            persistence
        ]

        fraction = (
            count
            / len(
                rows
            )
        )

        print(
            f"  k={persistence}: "
            f"{count} "
            f"({fraction:.3%})"
        )


def print_margin_summary(
    rows: list[dict],
) -> None:

    margins = [
        float(
            row[
                "absolute_margin"
            ]
        )
        for row in rows
    ]

    spreads = [
        float(
            row[
                "total_spread"
            ]
        )
        for row in rows
    ]

    relative_margins = [
        float(
            row[
                "relative_margin"
            ]
        )
        for row in rows
    ]

    print()
    print(
        "UTILITY MARGIN SUMMARY"
    )

    print(
        "mean best-vs-second margin="
        f"{statistics.mean(margins):.6f}"
    )

    print(
        "median best-vs-second margin="
        f"{statistics.median(margins):.6f}"
    )

    print(
        "mean best-vs-worst spread="
        f"{statistics.mean(spreads):.6f}"
    )

    print(
        "median best-vs-worst spread="
        f"{statistics.median(spreads):.6f}"
    )

    print(
        "mean relative margin="
        f"{statistics.mean(relative_margins):.3%}"
    )

    print(
        "median relative margin="
        f"{statistics.median(relative_margins):.3%}"
    )


def print_margin_thresholds(
    rows: list[dict],
) -> None:

    print()
    print(
        "MEANINGFUL-MARGIN PREVALENCE"
    )

    for threshold in (
        MARGIN_THRESHOLDS
    ):

        fraction = (
            sum(
                float(
                    row[
                        "absolute_margin"
                    ]
                )
                > threshold
                for row in rows
            )
            / len(
                rows
            )
        )

        print(
            f"  margin > "
            f"{threshold:.4f}: "
            f"{fraction:.3%}"
        )


def print_by_best_class(
    rows: list[dict],
) -> None:

    print()
    print(
        "MARGIN BY BEST PERSISTENCE"
    )

    groups = defaultdict(list)

    for row in rows:

        groups[
            int(
                row[
                    "best_persistence"
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

        margins = [
            float(
                row[
                    "absolute_margin"
                ]
            )
            for row in group
        ]

        spreads = [
            float(
                row[
                    "total_spread"
                ]
            )
            for row in group
        ]

        print(
            f"  k={persistence} "
            f"n={len(group)} "
            f"mean_margin="
            f"{statistics.mean(margins):.6f} "
            f"median_margin="
            f"{statistics.median(margins):.6f} "
            f"mean_spread="
            f"{statistics.mean(spreads):.6f}"
        )


def print_pairwise_preference(
    rows: list[dict],
) -> None:

    print()
    print(
        "PAIRWISE PREFERENCE FREQUENCIES"
    )

    pairs = [
        (
            1,
            2,
        ),
        (
            1,
            3,
        ),
        (
            2,
            3,
        ),
    ]

    for left, right in pairs:

        left_key = (
            f"loss_k{left}"
        )

        right_key = (
            f"loss_k{right}"
        )

        left_better = sum(
            float(
                row[
                    left_key
                ]
            )
            <
            float(
                row[
                    right_key
                ]
            )
            for row in rows
        )

        right_better = sum(
            float(
                row[
                    right_key
                ]
            )
            <
            float(
                row[
                    left_key
                ]
            )
            for row in rows
        )

        ties = (
            len(
                rows
            )
            - left_better
            - right_better
        )

        print(
            f"  k={left} vs k={right}: "
            f"k={left} better="
            f"{left_better / len(rows):.3%} "
            f"k={right} better="
            f"{right_better / len(rows):.3%} "
            f"tie="
            f"{ties / len(rows):.3%}"
        )


def print_regret_of_fixed_choices(
    rows: list[dict],
) -> None:

    print()
    print(
        "FIXED-POLICY ORACLE REGRET"
    )

    for persistence in (
        PERSISTENCE_LEVELS
    ):

        regrets = []

        for row in rows:

            selected_loss = float(
                row[
                    f"loss_k{persistence}"
                ]
            )

            best_loss = float(
                row[
                    "best_loss"
                ]
            )

            regrets.append(
                selected_loss
                - best_loss
            )

        print(
            f"  k={persistence}: "
            f"mean_regret="
            f"{statistics.mean(regrets):.6f} "
            f"median_regret="
            f"{statistics.median(regrets):.6f} "
            f"max_regret="
            f"{max(regrets):.6f}"
        )


def print_summary(
    rows: list[dict],
) -> None:

    print("=" * 126)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PERSISTENCE-POLICY LEARNABILITY "
        "AND MARGIN ANALYSIS"
    )

    print("=" * 126)

    print(
        f"decision contexts="
        f"{len(rows)}"
    )

    print_distribution_summary(
        rows
    )

    print_margin_summary(
        rows
    )

    print_margin_thresholds(
        rows
    )

    print_by_best_class(
        rows
    )

    print_pairwise_preference(
        rows
    )

    print_regret_of_fixed_choices(
        rows
    )

    print("=" * 126)


def main() -> None:

    rows = generate_analysis_rows()

    save_results(
        rows
    )

    print_summary(
        rows
    )

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()