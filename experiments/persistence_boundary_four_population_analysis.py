import csv
import math
from pathlib import Path


POPULATIONS = {
    "seed_100_139": Path(
        "results/persistence_multiplier_local_refinement.csv"
    ),
    "seed_200_239": Path(
        "results/persistence_multiplier_independent_validation.csv"
    ),
    "seed_300_339": Path(
        "results/persistence_multiplier_population_300_339.csv"
    ),
    "seed_400_439": Path(
        "results/persistence_multiplier_population_400_439.csv"
    ),
}

OUTPUT_PATH = Path(
    "results/persistence_boundary_four_population_analysis.csv"
)

POLICIES = [
    ("two_stage_0.25", 0.25),
    ("two_stage_0.30", 0.30),
    ("two_stage_0.35", 0.35),
    ("two_stage_0.40", 0.40),
    ("two_stage_0.45", 0.45),
    ("two_stage_0.50", 0.50),
]

METRICS = [
    "mean_regret",
    "under_count",
    "over_count",
    "action_entropy",
]

BOUNDARIES = [
    (
        "two_stage_0.30",
        "two_stage_0.35",
    ),
    (
        "two_stage_0.35",
        "two_stage_0.40",
    ),
]


def load_population(
    path: Path,
) -> list[dict]:

    valid = {
        policy
        for policy, _
        in POLICIES
    }

    rows = []

    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["policy"] not in valid:
                continue

            record = dict(row)

            for metric in METRICS:
                record[metric] = float(
                    record[metric]
                )

            rows.append(record)

    return rows


def summarize(
    rows: list[dict],
) -> list[dict]:

    output = []

    for policy, multiplier in POLICIES:

        policy_rows = [
            row
            for row in rows
            if row["policy"] == policy
        ]

        record = {
            "policy": policy,
            "multiplier": multiplier,
        }

        for metric in METRICS:

            values = [
                row[metric]
                for row in policy_rows
            ]

            record[metric] = (
                sum(values)
                / len(values)
            )

        output.append(record)

    return output


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
        value - minimum
    ) / (
        maximum - minimum
    )


def normalized_costs(
    summaries: list[dict],
) -> dict[str, dict]:

    ranges = {}

    for metric in METRICS:

        values = [
            row[metric]
            for row in summaries
        ]

        ranges[metric] = (
            min(values),
            max(values),
        )

    output = {}

    for row in summaries:

        record = dict(row)

        for metric in (
            "mean_regret",
            "under_count",
            "over_count",
        ):

            minimum, maximum = ranges[
                metric
            ]

            record[
                f"cost_{metric}"
            ] = normalize(
                row[metric],
                minimum,
                maximum,
            )

        entropy_min, entropy_max = ranges[
            "action_entropy"
        ]

        record[
            "cost_action_entropy"
        ] = (
            1.0
            - normalize(
                row["action_entropy"],
                entropy_min,
                entropy_max,
            )
        )

        output[
            row["policy"]
        ] = record

    return output


def square_difference(
    left: float,
    right: float,
) -> float:

    return (
        left ** 2
        - right ** 2
    )


def analyze_boundary(
    population: str,
    costs: dict[str, dict],
    lower_policy: str,
    upper_policy: str,
) -> dict:

    lower = costs[
        lower_policy
    ]

    upper = costs[
        upper_policy
    ]

    regret_term = square_difference(
        lower["cost_mean_regret"],
        upper["cost_mean_regret"],
    )

    under_term = square_difference(
        lower["cost_under_count"],
        upper["cost_under_count"],
    )

    over_term = square_difference(
        lower["cost_over_count"],
        upper["cost_over_count"],
    )

    entropy_term = square_difference(
        lower["cost_action_entropy"],
        upper["cost_action_entropy"],
    )

    performance_term = (
        regret_term
        + under_term
    )

    responsiveness_term = (
        over_term
        + entropy_term
    )

    if math.isclose(
        performance_term,
        0.0,
    ):
        threshold = float(
            "nan"
        )
    else:
        threshold = (
            -responsiveness_term
            / performance_term
        )

    return {
        "population":
            population,

        "lower_policy":
            lower_policy,

        "upper_policy":
            upper_policy,

        "lower_multiplier":
            lower["multiplier"],

        "upper_multiplier":
            upper["multiplier"],

        "regret_term":
            regret_term,

        "under_term":
            under_term,

        "over_term":
            over_term,

        "entropy_term":
            entropy_term,

        "performance_term":
            performance_term,

        "responsiveness_term":
            responsiveness_term,

        "analytic_transition_weight":
            threshold,
    }


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
            "population",
            "lower_policy",
            "upper_policy",
            "lower_multiplier",
            "upper_multiplier",
            "regret_term",
            "under_term",
            "over_term",
            "entropy_term",
            "performance_term",
            "responsiveness_term",
            "analytic_transition_weight",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)


def print_results(
    rows: list[dict],
) -> None:

    print("=" * 130)
    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PERSISTENCE BOUNDARY "
        "VARIABILITY DECOMPOSITION"
    )
    print("=" * 130)
    print()

    for population in POPULATIONS:

        print(population)

        population_rows = [
            row
            for row in rows
            if row["population"]
            == population
        ]

        for row in population_rows:

            print(
                f"  "
                f"{float(row['lower_multiplier']):.2f}"
                f" -> "
                f"{float(row['upper_multiplier']):.2f}"
            )

            print(
                f"    analytic threshold="
                f"{float(row['analytic_transition_weight']):.6f}"
            )

            print(
                f"    performance term="
                f"{float(row['performance_term']):+.6f}"
            )

            print(
                f"      regret="
                f"{float(row['regret_term']):+.6f}"
            )

            print(
                f"      under="
                f"{float(row['under_term']):+.6f}"
            )

            print(
                f"    responsiveness term="
                f"{float(row['responsiveness_term']):+.6f}"
            )

            print(
                f"      over="
                f"{float(row['over_term']):+.6f}"
            )

            print(
                f"      entropy="
                f"{float(row['entropy_term']):+.6f}"
            )

        print()

    second_boundary = [
        row
        for row in rows
        if math.isclose(
            float(
                row[
                    "lower_multiplier"
                ]
            ),
            0.35,
        )
        and math.isclose(
            float(
                row[
                    "upper_multiplier"
                ]
            ),
            0.40,
        )
    ]

    if len(second_boundary) == 2:

        first = second_boundary[0]
        second = second_boundary[1]

        shift = (
            float(
                second[
                    "analytic_transition_weight"
                ]
            )
            - float(
                first[
                    "analytic_transition_weight"
                ]
            )
        )

        print(
            "0.35 -> 0.40 "
            "BOUNDARY SHIFT"
        )

        print(
            f"  population difference="
            f"{shift:+.6f}"
        )

    print()
    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


def main() -> None:

    results = []

    for population, path in POPULATIONS.items():

        rows = load_population(
            path
        )

        summaries = summarize(
            rows
        )

        costs = normalized_costs(
            summaries
        )

        for (
            lower_policy,
            upper_policy,
        ) in BOUNDARIES:

            results.append(
                analyze_boundary(
                    population,
                    costs,
                    lower_policy,
                    upper_policy,
                )
            )

    save_results(
        results
    )

    print_results(
        results
    )


if __name__ == "__main__":
    main()
