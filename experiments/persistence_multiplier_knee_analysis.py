import csv
import math
import statistics
from pathlib import Path


INPUT_PATH = Path(
    "results/persistence_multiplier_operating_region.csv"
)

OUTPUT_PATH = Path(
    "results/persistence_multiplier_knee_analysis.csv"
)


POLICIES = [
    ("two_stage_0.10", 0.10),
    ("two_stage_0.25", 0.25),
    ("two_stage_0.35", 0.35),
    ("two_stage_0.50", 0.50),
    ("two_stage_0.65", 0.65),
    ("two_stage_0.80", 0.80),
    ("two_stage_1.00", 1.00),
]


METRICS = [
    "mean_regret",
    "under_count",
    "over_count",
    "action_entropy",
]


def load_rows() -> list[dict]:

    rows = []

    with INPUT_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(
            file
        )

        for row in reader:

            if row[
                "policy"
            ] not in {
                policy
                for policy, _
                in POLICIES
            }:
                continue

            record = dict(
                row
            )

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


def summarize_policies(
    rows: list[dict],
) -> list[dict]:

    summaries = []

    for policy, multiplier in POLICIES:

        policy_rows = [
            row
            for row in rows
            if row[
                "policy"
            ] == policy
        ]

        summary = {
            "policy":
                policy,

            "multiplier":
                multiplier,
        }

        for metric in METRICS:

            values = [
                float(
                    row[
                        metric
                    ]
                )
                for row in policy_rows
            ]

            summary[
                metric
            ] = statistics.mean(
                values
            )

        summaries.append(
            summary
        )

    return summaries


def normalize(
    value: float,
    minimum: float,
    maximum: float,
) -> float:

    if math.isclose(
        minimum,
        maximum,
    ):
        return 0.0

    return (
        value
        - minimum
    ) / (
        maximum
        - minimum
    )


def add_normalized_metrics(
    summaries: list[dict],
) -> None:

    ranges = {}

    for metric in METRICS:

        values = [
            float(
                row[
                    metric
                ]
            )
            for row in summaries
        ]

        ranges[
            metric
        ] = (
            min(
                values
            ),
            max(
                values
            ),
        )

    for row in summaries:

        regret_min, regret_max = ranges[
            "mean_regret"
        ]

        under_min, under_max = ranges[
            "under_count"
        ]

        over_min, over_max = ranges[
            "over_count"
        ]

        entropy_min, entropy_max = ranges[
            "action_entropy"
        ]

        row[
            "normalized_regret_cost"
        ] = normalize(
            row[
                "mean_regret"
            ],
            regret_min,
            regret_max,
        )

        row[
            "normalized_under_cost"
        ] = normalize(
            row[
                "under_count"
            ],
            under_min,
            under_max,
        )

        row[
            "normalized_over_cost"
        ] = normalize(
            row[
                "over_count"
            ],
            over_min,
            over_max,
        )

        row[
            "normalized_entropy_cost"
        ] = (
            1.0
            - normalize(
                row[
                    "action_entropy"
                ],
                entropy_min,
                entropy_max,
            )
        )

        row[
            "ideal_distance"
        ] = math.sqrt(
            (
                row[
                    "normalized_regret_cost"
                ]
                ** 2
            )
            + (
                row[
                    "normalized_under_cost"
                ]
                ** 2
            )
            + (
                row[
                    "normalized_over_cost"
                ]
                ** 2
            )
            + (
                row[
                    "normalized_entropy_cost"
                ]
                ** 2
            )
        )


def add_marginal_metrics(
    summaries: list[dict],
) -> None:

    for index, row in enumerate(
        summaries
    ):

        if index == 0:

            row[
                "delta_multiplier"
            ] = ""

            row[
                "delta_regret"
            ] = ""

            row[
                "delta_under"
            ] = ""

            row[
                "delta_over"
            ] = ""

            row[
                "delta_entropy"
            ] = ""

            row[
                "regret_gain_per_over"
            ] = ""

            row[
                "under_gain_per_entropy_loss"
            ] = ""

            continue

        previous = summaries[
            index - 1
        ]

        delta_multiplier = (
            row[
                "multiplier"
            ]
            - previous[
                "multiplier"
            ]
        )

        delta_regret = (
            row[
                "mean_regret"
            ]
            - previous[
                "mean_regret"
            ]
        )

        delta_under = (
            row[
                "under_count"
            ]
            - previous[
                "under_count"
            ]
        )

        delta_over = (
            row[
                "over_count"
            ]
            - previous[
                "over_count"
            ]
        )

        delta_entropy = (
            row[
                "action_entropy"
            ]
            - previous[
                "action_entropy"
            ]
        )

        row[
            "delta_multiplier"
        ] = delta_multiplier

        row[
            "delta_regret"
        ] = delta_regret

        row[
            "delta_under"
        ] = delta_under

        row[
            "delta_over"
        ] = delta_over

        row[
            "delta_entropy"
        ] = delta_entropy

        regret_gain = max(
            0.0,
            -delta_regret,
        )

        under_gain = max(
            0.0,
            -delta_under,
        )

        over_cost = max(
            0.0,
            delta_over,
        )

        entropy_cost = max(
            0.0,
            -delta_entropy,
        )

        row[
            "regret_gain_per_over"
        ] = (
            regret_gain
            / over_cost
            if over_cost > 0.0
            else float(
                "inf"
            )
        )

        row[
            "under_gain_per_entropy_loss"
        ] = (
            under_gain
            / entropy_cost
            if entropy_cost > 0.0
            else float(
                "inf"
            )
        )


def identify_candidates(
    summaries: list[dict],
) -> tuple[
    dict,
    dict,
]:

    minimum_distance = min(
        summaries,
        key=lambda row: (
            row[
                "ideal_distance"
            ],
            row[
                "multiplier"
            ],
        ),
    )

    marginal_rows = [
        row
        for row in summaries
        if row[
            "regret_gain_per_over"
        ] != ""
    ]

    best_marginal = max(
        marginal_rows,
        key=lambda row: (
            float(
                row[
                    "regret_gain_per_over"
                ]
            ),
            float(
                row[
                    "under_gain_per_entropy_loss"
                ]
            ),
        ),
    )

    return (
        minimum_distance,
        best_marginal,
    )


def save_results(
    summaries: list[dict],
) -> None:

    OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )

    fieldnames = [
        "policy",
        "multiplier",
        "mean_regret",
        "under_count",
        "over_count",
        "action_entropy",
        "normalized_regret_cost",
        "normalized_under_cost",
        "normalized_over_cost",
        "normalized_entropy_cost",
        "ideal_distance",
        "delta_multiplier",
        "delta_regret",
        "delta_under",
        "delta_over",
        "delta_entropy",
        "regret_gain_per_over",
        "under_gain_per_entropy_loss",
    ]

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(
            summaries
        )


def print_results(
    summaries: list[dict],
    minimum_distance: dict,
    best_marginal: dict,
) -> None:

    print(
        "=" * 140
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PERSISTENCE MULTIPLIER "
        "KNEE ANALYSIS"
    )

    print(
        "=" * 140
    )

    print()

    print(
        "OPERATING CURVE"
    )

    for row in summaries:

        marginal = (
            "n/a"
            if row[
                "regret_gain_per_over"
            ] == ""
            else (
                f"{float(row['regret_gain_per_over']):.8f}"
            )
        )

        print(
            f"{row['policy']:<18} "
            f"m={row['multiplier']:.2f} "
            f"R={row['mean_regret']:.6f} "
            f"under={row['under_count']:.2f} "
            f"over={row['over_count']:.2f} "
            f"H={row['action_entropy']:.3f} "
            f"D={row['ideal_distance']:.4f} "
            f"Rgain/over={marginal}"
        )

    print()
    print(
        "MINIMUM NORMALIZED IDEAL DISTANCE"
    )

    print(
        f"  policy="
        f"{minimum_distance['policy']}"
    )

    print(
        f"  multiplier="
        f"{minimum_distance['multiplier']:.2f}"
    )

    print(
        f"  distance="
        f"{minimum_distance['ideal_distance']:.6f}"
    )

    print()
    print(
        "BEST MARGINAL REGRET GAIN PER "
        "ADDITIONAL OVER-PERSISTENCE EVENT"
    )

    print(
        f"  policy="
        f"{best_marginal['policy']}"
    )

    print(
        f"  multiplier="
        f"{best_marginal['multiplier']:.2f}"
    )

    print(
        f"  efficiency="
        f"{float(best_marginal['regret_gain_per_over']):.8f}"
    )

    print()
    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


def main() -> None:

    rows = load_rows()

    summaries = summarize_policies(
        rows
    )

    add_normalized_metrics(
        summaries
    )

    add_marginal_metrics(
        summaries
    )

    (
        minimum_distance,
        best_marginal,
    ) = identify_candidates(
        summaries
    )

    save_results(
        summaries
    )

    print_results(
        summaries,
        minimum_distance,
        best_marginal,
    )


if __name__ == "__main__":
    main()
