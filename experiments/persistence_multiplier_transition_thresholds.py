import csv
import math
from collections import defaultdict
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
    "results/persistence_multiplier_transition_thresholds.csv"
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
        0.30 + 0.005 * index,
        3,
    )
    for index in range(181)
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


def distance(
    row: dict,
    performance_weight: float,
) -> float:

    weighted_sum = (
        performance_weight
        * (
            row["cost_mean_regret"] ** 2
            + row["cost_under_count"] ** 2
        )
        + (
            row["cost_over_count"] ** 2
            + row["cost_action_entropy"] ** 2
        )
    )

    total_weight = (
        2.0 * performance_weight
        + 2.0
    )

    return math.sqrt(
        weighted_sum
        / total_weight
    )


def selected_policy(
    summaries: list[dict],
    performance_weight: float,
) -> dict:

    candidates = []

    for row in summaries:

        candidates.append(
            {
                "policy":
                    row["policy"],

                "multiplier":
                    row["multiplier"],

                "distance":
                    distance(
                        row,
                        performance_weight,
                    ),
            }
        )

    return min(
        candidates,
        key=lambda row: (
            row["distance"],
            row["multiplier"],
        ),
    )


def evaluate_population(
    population: str,
    path: Path,
) -> list[dict]:

    summaries = normalized_costs(
        summarize(
            load_population(path)
        )
    )

    output = []

    for weight in PERFORMANCE_WEIGHTS:

        selected = selected_policy(
            summaries,
            weight,
        )

        output.append(
            {
                "population":
                    population,

                "performance_weight":
                    weight,

                "selected_policy":
                    selected["policy"],

                "selected_multiplier":
                    selected["multiplier"],

                "selected_distance":
                    selected["distance"],
            }
        )

    return output


def extract_intervals(
    rows: list[dict],
) -> list[dict]:

    grouped = defaultdict(list)

    for row in rows:
        grouped[
            row["population"]
        ].append(row)

    output = []

    for population, population_rows in grouped.items():

        population_rows.sort(
            key=lambda row:
                row["performance_weight"]
        )

        start = population_rows[0]
        previous = start

        for current in population_rows[1:]:

            if (
                current["selected_multiplier"]
                != previous["selected_multiplier"]
            ):

                output.append(
                    {
                        "population":
                            population,

                        "selected_multiplier":
                            previous["selected_multiplier"],

                        "weight_start":
                            start["performance_weight"],

                        "weight_end":
                            previous["performance_weight"],

                        "next_multiplier":
                            current["selected_multiplier"],

                        "transition_lower":
                            previous["performance_weight"],

                        "transition_upper":
                            current["performance_weight"],
                    }
                )

                start = current

            previous = current

        output.append(
            {
                "population":
                    population,

                "selected_multiplier":
                    previous["selected_multiplier"],

                "weight_start":
                    start["performance_weight"],

                "weight_end":
                    previous["performance_weight"],

                "next_multiplier":
                    "",

                "transition_lower":
                    "",

                "transition_upper":
                    "",
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
            "population",
            "selected_multiplier",
            "weight_start",
            "weight_end",
            "next_multiplier",
            "transition_lower",
            "transition_upper",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)


def print_results(
    intervals: list[dict],
) -> None:

    print("=" * 120)
    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PERSISTENCE MULTIPLIER "
        "TRANSITION THRESHOLDS"
    )
    print("=" * 120)
    print()

    for population in POPULATIONS:

        print(population)

        population_rows = [
            row
            for row in intervals
            if row["population"] == population
        ]

        for row in population_rows:

            print(
                f"  m="
                f"{float(row['selected_multiplier']):.2f} "
                f"for weight=["
                f"{float(row['weight_start']):.3f}, "
                f"{float(row['weight_end']):.3f}]"
            )

            if row["next_multiplier"] != "":

                midpoint = (
                    float(row["transition_lower"])
                    + float(row["transition_upper"])
                ) / 2.0

                print(
                    f"    transition -> "
                    f"{float(row['next_multiplier']):.2f} "
                    f"between "
                    f"{float(row['transition_lower']):.3f} "
                    f"and "
                    f"{float(row['transition_upper']):.3f} "
                    f"(midpoint≈{midpoint:.4f})"
                )

        print()

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


def main() -> None:

    rows = []

    for population, path in POPULATIONS.items():

        rows.extend(
            evaluate_population(
                population,
                path,
            )
        )

    intervals = extract_intervals(
        rows
    )

    save_results(
        intervals
    )

    print_results(
        intervals
    )


if __name__ == "__main__":
    main()
