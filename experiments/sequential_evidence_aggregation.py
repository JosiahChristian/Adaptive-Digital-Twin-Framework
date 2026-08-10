import csv
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path


INPUT_PATH = Path(
    "results/cause_conditioned_evidence_validation.csv"
)

OUTPUT_PATH = Path(
    "results/sequential_evidence_aggregation.csv"
)


BATCH_SIZES = [
    1,
    2,
    5,
    10,
    20,
    50,
]

BOOTSTRAP_REPLICATES = 500

RANDOM_SEED = 28028


def load_rows() -> list[dict]:

    with INPUT_PATH.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def group_by_condition(
    rows: list[dict],
) -> dict[str, list[dict]]:

    groups = defaultdict(
        list
    )

    for row in rows:

        groups[
            row["condition"]
        ].append(
            row
        )

    return groups


def evidence_vote(
    row: dict,
) -> float:

    return (
        1.0
        if row[
            "predicted_evidence_sufficient"
        ]
        == "True"
        else 0.0
    )


def evidence_label(
    rows: list[dict],
) -> bool:

    return (
        rows[0][
            "operating_point_evidence_sufficient"
        ]
        == "True"
    )


def sample_batch_fraction(
    rows: list[dict],
    *,
    batch_size: int,
    rng: random.Random,
) -> float:

    sampled = rng.sample(
        rows,
        batch_size,
    )

    return statistics.mean(
        evidence_vote(
            row
        )
        for row in sampled
    )


def build_distribution(
    rows: list[dict],
    *,
    batch_size: int,
    rng: random.Random,
) -> list[float]:

    return [
        sample_batch_fraction(
            rows,
            batch_size=batch_size,
            rng=rng,
        )
        for _ in range(
            BOOTSTRAP_REPLICATES
        )
    ]


def standardized_separation(
    sufficient_values: list[float],
    insufficient_values: list[float],
) -> float:

    mean_difference = abs(
        statistics.mean(
            sufficient_values
        )
        -
        statistics.mean(
            insufficient_values
        )
    )

    variance_average = (
        statistics.variance(
            sufficient_values
        )
        +
        statistics.variance(
            insufficient_values
        )
    ) / 2.0

    if variance_average == 0.0:

        return 0.0

    return (
        mean_difference
        / math.sqrt(
            variance_average
        )
    )


def run_experiment() -> list[dict]:

    rows = load_rows()

    groups = group_by_condition(
        rows
    )

    rng = random.Random(
        RANDOM_SEED
    )

    output_rows = []

    for batch_size in BATCH_SIZES:

        sufficient_values = []
        insufficient_values = []

        condition_records = []

        for condition, condition_rows in (
            groups.items()
        ):

            distribution = (
                build_distribution(
                    condition_rows,
                    batch_size=batch_size,
                    rng=rng,
                )
            )

            label = evidence_label(
                condition_rows
            )

            if label:

                sufficient_values.extend(
                    distribution
                )

            else:

                insufficient_values.extend(
                    distribution
                )

            condition_records.append(
                {
                    "batch_size":
                        batch_size,

                    "condition":
                        condition,

                    "evidence_sufficient":
                        label,

                    "mean_vote_fraction":
                        statistics.mean(
                            distribution
                        ),

                    "std_vote_fraction":
                        statistics.stdev(
                            distribution
                        ),

                    "min_vote_fraction":
                        min(
                            distribution
                        ),

                    "max_vote_fraction":
                        max(
                            distribution
                        ),
                }
            )

        global_separation = (
            standardized_separation(
                sufficient_values,
                insufficient_values,
            )
        )

        sufficient_mean = (
            statistics.mean(
                sufficient_values
            )
        )

        insufficient_mean = (
            statistics.mean(
                insufficient_values
            )
        )

        sufficient_std = (
            statistics.stdev(
                sufficient_values
            )
        )

        insufficient_std = (
            statistics.stdev(
                insufficient_values
            )
        )

        for record in condition_records:

            output_rows.append(
                {
                    **record,

                    "global_sufficient_mean":
                        sufficient_mean,

                    "global_insufficient_mean":
                        insufficient_mean,

                    "global_sufficient_std":
                        sufficient_std,

                    "global_insufficient_std":
                        insufficient_std,

                    "global_standardized_separation":
                        global_separation,

                    "bootstrap_replicates":
                        BOOTSTRAP_REPLICATES,
                }
            )

    return output_rows


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


def print_summary(
    rows: list[dict],
) -> None:

    print("=" * 118)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "SEQUENTIAL EVIDENCE AGGREGATION"
    )

    print("=" * 118)

    seen = set()

    for row in rows:

        batch_size = int(
            row["batch_size"]
        )

        if batch_size in seen:
            continue

        seen.add(
            batch_size
        )

        print(
            f"n={batch_size:<3} "
            f"sufficient_mean="
            f"{float(row['global_sufficient_mean']):.4f} "
            f"sufficient_std="
            f"{float(row['global_sufficient_std']):.4f} "
            f"insufficient_mean="
            f"{float(row['global_insufficient_mean']):.4f} "
            f"insufficient_std="
            f"{float(row['global_insufficient_std']):.4f} "
            f"separation="
            f"{float(row['global_standardized_separation']):.4f}"
        )

    print("=" * 118)


def main() -> None:

    rows = run_experiment()

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