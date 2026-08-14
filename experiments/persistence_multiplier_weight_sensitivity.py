import csv
import math
from collections import Counter
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
    "results/persistence_multiplier_weight_sensitivity.csv"
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

WEIGHT_SCHEMES = {
    "equal": {
        "mean_regret": 1.0,
        "under_count": 1.0,
        "over_count": 1.0,
        "action_entropy": 1.0,
    },
    "regret_priority": {
        "mean_regret": 2.0,
        "under_count": 1.0,
        "over_count": 1.0,
        "action_entropy": 1.0,
    },
    "under_priority": {
        "mean_regret": 1.0,
        "under_count": 2.0,
        "over_count": 1.0,
        "action_entropy": 1.0,
    },
    "over_priority": {
        "mean_regret": 1.0,
        "under_count": 1.0,
        "over_count": 2.0,
        "action_entropy": 1.0,
    },
    "entropy_priority": {
        "mean_regret": 1.0,
        "under_count": 1.0,
        "over_count": 1.0,
        "action_entropy": 2.0,
    },
    "performance_priority": {
        "mean_regret": 2.0,
        "under_count": 2.0,
        "over_count": 1.0,
        "action_entropy": 1.0,
    },
    "responsiveness_priority": {
        "mean_regret": 1.0,
        "under_count": 1.0,
        "over_count": 2.0,
        "action_entropy": 2.0,
    },
    "regret_heavy": {
        "mean_regret": 4.0,
        "under_count": 1.0,
        "over_count": 1.0,
        "action_entropy": 1.0,
    },
    "responsiveness_heavy": {
        "mean_regret": 1.0,
        "under_count": 1.0,
        "over_count": 4.0,
        "action_entropy": 4.0,
    },
}


def load_population(
    path: Path,
) -> list[dict]:

    rows = []

    valid_policies = {
        policy
        for policy, _
        in POLICIES
    }

    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(
            file
        )

        for row in reader:

            if row["policy"] not in valid_policies:
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

        output.append(record)

    return output


def weighted_distance(
    row: dict,
    weights: dict,
) -> float:

    weighted_sum = 0.0
    total_weight = 0.0

    for metric, weight in weights.items():

        weighted_sum += (
            weight
            * (
                row[
                    f"cost_{metric}"
                ]
                ** 2
            )
        )

        total_weight += weight

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

    for scheme_name, weights in WEIGHT_SCHEMES.items():

        candidates = []

        for row in summaries:

            distance = weighted_distance(
                row,
                weights,
            )

            record = {
                "population": population,
                "weight_scheme": scheme_name,
                "policy": row["policy"],
                "multiplier": row["multiplier"],
                "weighted_distance": distance,
            }

            candidates.append(record)

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
            "weight_scheme",
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


def print_summary(
    rows: list[dict],
) -> None:

    selected_rows = [
        row
        for row in rows
        if row["selected"] == 1
    ]

    print("=" * 120)
    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PERSISTENCE MULTIPLIER "
        "WEIGHT SENSITIVITY"
    )
    print("=" * 120)
    print()

    for population in POPULATIONS:

        print(population)

        population_selected = [
            row
            for row in selected_rows
            if row["population"]
            == population
        ]

        for row in population_selected:

            print(
                f"  {row['weight_scheme']:<24} "
                f"m={row['multiplier']:.2f} "
                f"D={row['weighted_distance']:.6f}"
            )

        print()

    counts = Counter(
        row["multiplier"]
        for row in selected_rows
    )

    print("SELECTION FREQUENCY ACROSS ALL SCHEMES/POPULATIONS")

    total = len(selected_rows)

    for multiplier in sorted(counts):

        count = counts[multiplier]

        print(
            f"  m={multiplier:.2f}: "
            f"{count}/{total} "
            f"({count / total:.1%})"
        )

    print()

    forty_count = counts.get(
        0.40,
        0,
    )

    print(
        "0.40 selection frequency="
        f"{forty_count}/{total} "
        f"({forty_count / total:.1%})"
    )

    print()
    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


def main() -> None:

    all_results = []

    for population, path in POPULATIONS.items():

        rows = load_population(path)

        all_results.extend(
            evaluate_population(
                population,
                rows,
            )
        )

    save_results(
        all_results
    )

    print_summary(
        all_results
    )


if __name__ == "__main__":
    main()
