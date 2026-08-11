import csv
import math
import statistics
from pathlib import Path

from experiments.independent_aggregated_evidence_validation import (
    CONFIDENCE_THRESHOLD,
    VALIDATION_CONDITIONS,
    extract_features,
    run_trajectory,
)

from experiments.mismatch_classification import (
    classify_row,
)


POPULATION_SIZE = 100

POPULATION_REPLICATES = 100

BASE_SEED = 5000

SEED_STRIDE = 1000

OUTPUT_PATH = Path(
    "results/uncertainty_aware_evidence_sufficiency.csv"
)


def classify_population(
    *,
    condition: dict,
    replicate: int,
) -> list[dict]:

    classifications = []

    condition_index = (
        VALIDATION_CONDITIONS.index(
            condition
        )
    )

    replicate_base_seed = (
        BASE_SEED
        + condition_index
        * POPULATION_REPLICATES
        * SEED_STRIDE
        + replicate
        * SEED_STRIDE
    )

    for offset in range(
        POPULATION_SIZE
    ):

        seed = (
            replicate_base_seed
            + offset
        )

        trajectory = run_trajectory(
            condition=condition,
            seed=seed,
        )

        (
            global_features,
            temporal_features,
            adaptation_features,
        ) = extract_features(
            trajectory
        )

        classification = classify_row(
            regime=condition["class"],
            global_row=global_features,
            temporal_row=temporal_features,
            adaptation_row=adaptation_features,
        )

        classifications.append(
            classification
        )

    return classifications


def population_statistics(
    classifications: list[dict],
) -> dict:

    hard_accuracy = (
        sum(
            item["correct"]
            for item in classifications
        )
        / len(classifications)
    )

    accepted = [
        item
        for item in classifications
        if float(
            item[
                "classification_margin"
            ]
        )
        >= CONFIDENCE_THRESHOLD
    ]

    coverage = (
        len(accepted)
        / len(classifications)
    )

    if accepted:

        selective_accuracy = (
            sum(
                item["correct"]
                for item in accepted
            )
            / len(accepted)
        )

    else:

        selective_accuracy = 0.0

    evidence_sufficient = (
        hard_accuracy >= 0.90
        and
        coverage >= 0.80
        and
        selective_accuracy >= 0.95
    )

    return {
        "hard_accuracy":
            hard_accuracy,

        "coverage":
            coverage,

        "selective_accuracy":
            selective_accuracy,

        "evidence_sufficient":
            evidence_sufficient,
    }


def run_experiment() -> list[dict]:

    rows = []

    for condition in (
        VALIDATION_CONDITIONS
    ):

        for replicate in range(
            POPULATION_REPLICATES
        ):

            classifications = (
                classify_population(
                    condition=condition,
                    replicate=replicate,
                )
            )

            stats = (
                population_statistics(
                    classifications
                )
            )

            rows.append(
                {
                    "condition":
                        condition["name"],

                    "true_class":
                        condition["class"],

                    "replicate":
                        replicate,

                    "population_size":
                        POPULATION_SIZE,

                    **stats,
                }
            )

    return rows


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


def normal_interval(
    probability: float,
    n: int,
) -> tuple[
    float,
    float,
]:

    standard_error = math.sqrt(
        probability
        * (
            1.0
            - probability
        )
        / n
    )

    lower = max(
        0.0,
        probability
        - 1.96
        * standard_error,
    )

    upper = min(
        1.0,
        probability
        + 1.96
        * standard_error,
    )

    return (
        lower,
        upper,
    )


def print_summary(
    rows: list[dict],
) -> None:

    print("=" * 126)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "UNCERTAINTY-AWARE EVIDENCE SUFFICIENCY"
    )

    print("=" * 126)

    for condition in (
        VALIDATION_CONDITIONS
    ):

        condition_rows = [
            row
            for row in rows
            if row["condition"]
            == condition["name"]
        ]

        sufficient_count = sum(
            row[
                "evidence_sufficient"
            ]
            for row in condition_rows
        )

        q_hat = (
            sufficient_count
            / len(condition_rows)
        )

        (
            q_low,
            q_high,
        ) = normal_interval(
            q_hat,
            len(condition_rows),
        )

        hard_values = [
            float(
                row[
                    "hard_accuracy"
                ]
            )
            for row in condition_rows
        ]

        coverage_values = [
            float(
                row[
                    "coverage"
                ]
            )
            for row in condition_rows
        ]

        selective_values = [
            float(
                row[
                    "selective_accuracy"
                ]
            )
            for row in condition_rows
        ]

        print(
            f"{condition['name']:<34}"
            f"q={q_hat:<7.3f} "
            f"CI=[{q_low:.3f},{q_high:.3f}] "
            f"A="
            f"{statistics.mean(hard_values):.3f}"
            f"±"
            f"{statistics.stdev(hard_values):.3f} "
            f"C="
            f"{statistics.mean(coverage_values):.3f}"
            f"±"
            f"{statistics.stdev(coverage_values):.3f} "
            f"Sel="
            f"{statistics.mean(selective_values):.3f}"
            f"±"
            f"{statistics.stdev(selective_values):.3f}"
        )

    print("=" * 126)


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