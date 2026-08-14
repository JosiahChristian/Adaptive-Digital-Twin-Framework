import csv
import math
from collections import Counter, defaultdict
from pathlib import Path


POPULATIONS = {
    "seed_100_139": Path(
        "results/persistence_multiplier_local_refinement.csv"
    ),
    "seed_200_239": Path(
        "results/persistence_multiplier_independent_validation.csv"
    ),
}

OUTPUT_PATH = Path(
    "results/persistence_multiplier_weight_space_map.csv"
)

SUMMARY_PATH = Path(
    "results/persistence_multiplier_weight_space_summary.csv"
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

PERFORMANCE_WEIGHTS = [
    round(
        0.25 + 0.05 * index,
        2,
    )
    for index in range(36)
]


def load_population(
    path: Path,
) -> list[dict]:

    rows = []

    valid = {
        policy
        for policy, _
        in POLICIES
    }

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

    summaries = []

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

        summaries.append(record)

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
        value - minimum
    ) / (
        maximum - minimum
    )


def normalized_costs(
    summaries: list[dict],
) -> list[dict]:

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

    output = []

    for row in summaries:

        record = dict(row)

        for metric in (
            "mean_regret",
            "under_count",
            "over_count",
        ):

            minimum, maximum = ranges[metric]

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

        output.append(record)

    return output


def weighted_distance(
    row: dict,
    performance_weight: float,
) -> float:

    responsiveness_weight = 1.0

    weighted_sum = (
        performance_weight
        * (
            row["cost_mean_regret"] ** 2
            + row["cost_under_count"] ** 2
        )
        + responsiveness_weight
        * (
            row["cost_over_count"] ** 2
            + row["cost_action_entropy"] ** 2
        )
    )

    total_weight = (
        2.0 * performance_weight
        + 2.0 * responsiveness_weight
    )

    return math.sqrt(
        weighted_sum
        / total_weight
    )


def evaluate_population(
    population: str,
    rows: list[dict],
) -> list[dict]:

    summaries = normalized_costs(
        summarize(rows)
    )

    output = []

    for performance_weight in PERFORMANCE_WEIGHTS:

        candidates = []

        for row in summaries:

            distance = weighted_distance(
                row,
                performance_weight,
            )

            candidates.append(
                {
                    "population":
                        population,

                    "performance_weight":
                        performance_weight,

                    "responsiveness_weight":
                        1.0,

                    "weight_ratio":
                        performance_weight,

                    "policy":
                        row["policy"],

                    "multiplier":
                        row["multiplier"],

                    "weighted_distance":
                        distance,
                }
            )

        selected = min(
            candidates,
            key=lambda row: (
                row["weighted_distance"],
                row["multiplier"],
            ),
        )

        for candidate in candidates:

            candidate[
                "selected"
            ] = int(
                candidate["policy"]
                == selected["policy"]
            )

            output.append(candidate)

    return output


def transition_summary(
    rows: list[dict],
) -> list[dict]:

    selected_rows = [
        row
        for row in rows
        if row["selected"] == 1
    ]

    output = []

    by_population = defaultdict(list)

    for row in selected_rows:
        by_population[
            row["population"]
        ].append(row)

    for population, population_rows in by_population.items():

        population_rows.sort(
            key=lambda row:
                row["performance_weight"]
        )

        start = population_rows[0]
        previous = start

        for current in population_rows[1:]:

            if (
                current["multiplier"]
                != previous["multiplier"]
            ):

                output.append(
                    {
                        "population":
                            population,

                        "selected_multiplier":
                            previous["multiplier"],

                        "weight_start":
                            start["performance_weight"],

                        "weight_end":
                            previous["performance_weight"],
                    }
                )

                start = current

            previous = current

        output.append(
            {
                "population":
                    population,

                "selected_multiplier":
                    previous["multiplier"],

                "weight_start":
                    start["performance_weight"],

                "weight_end":
                    previous["performance_weight"],
            }
        )

    return output


def save_map(
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
            "performance_weight",
            "responsiveness_weight",
            "weight_ratio",
            "policy",
            "multiplier",
            "weighted_distance",
            "selected",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)


def save_summary(
    rows: list[dict],
) -> None:

    with SUMMARY_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        fieldnames = [
            "population",
            "selected_multiplier",
            "weight_start",
            "weight_end",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)


def print_results(
    rows: list[dict],
    summary: list[dict],
) -> None:

    print("=" * 120)
    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PERSISTENCE MULTIPLIER "
        "WEIGHT-SPACE MAP"
    )
    print("=" * 120)
    print()

    for population in POPULATIONS:

        print(population)

        population_summary = [
            row
            for row in summary
            if row["population"]
            == population
        ]

        for row in population_summary:

            print(
                f"  weight=["
                f"{row['weight_start']:.2f}, "
                f"{row['weight_end']:.2f}] "
                f"-> m="
                f"{float(row['selected_multiplier']):.2f}"
            )

        print()

    selected_rows = [
        row
        for row in rows
        if row["selected"] == 1
    ]

    counts = Counter(
        row["multiplier"]
        for row in selected_rows
    )

    total = len(selected_rows)

    print(
        "SELECTION FREQUENCY ACROSS "
        "FULL WEIGHT GRID"
    )

    for multiplier in sorted(counts):

        count = counts[multiplier]

        print(
            f"  m={multiplier:.2f}: "
            f"{count}/{total} "
            f"({count / total:.1%})"
        )

    print()
    print(
        f"Map saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Boundary summary saved to: "
        f"{SUMMARY_PATH}"
    )


def main() -> None:

    all_rows = []

    for population, path in POPULATIONS.items():

        rows = load_population(path)

        all_rows.extend(
            evaluate_population(
                population,
                rows,
            )
        )

    summary = transition_summary(
        all_rows
    )

    save_map(
        all_rows
    )

    save_summary(
        summary
    )

    print_results(
        all_rows,
        summary,
    )


if __name__ == "__main__":
    main()
