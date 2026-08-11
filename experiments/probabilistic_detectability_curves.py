import csv
import math
import statistics
from pathlib import Path

from experiments.independent_aggregated_evidence_validation import (
    CONFIDENCE_THRESHOLD,
    extract_features,
    run_trajectory,
)

from experiments.mismatch_classification import (
    classify_row,
)


POPULATION_SIZE = 100

POPULATION_REPLICATES = 50

BASE_SEED = 32000

SEED_STRIDE = 1000

OUTPUT_PATH = Path(
    "results/probabilistic_detectability_curves.csv"
)


MEASUREMENT_NOISE_GRID = [
    0.75,
    0.80,
    0.85,
    0.90,
    0.95,
    1.00,
    1.05,
    1.10,
]

PROCESS_DISTURBANCE_GRID = [
    2.20,
    2.30,
    2.40,
    2.50,
    2.60,
    2.70,
    2.80,
    2.90,
    3.00,
    3.10,
    3.20,
]

PARAMETER_ESTIMATE_GRID = [
    0.35,
    0.375,
    0.40,
    0.425,
    0.45,
    0.475,
]

STRUCTURAL_CHANGE_GRID = [
    0.84,
    0.845,
    0.85,
    0.855,
    0.86,
    0.865,
    0.87,
    0.875,
    0.88,
    0.885,
    0.89,
]


def build_conditions() -> list[dict]:

    conditions = []

    for value in MEASUREMENT_NOISE_GRID:

        conditions.append(
            {
                "class":
                    "measurement_noise",

                "name":
                    (
                        "measurement_noise_"
                        f"{value:.3f}"
                    ),

                "magnitude":
                    value,

                "measurement_noise_std":
                    value,

                "process_disturbance":
                    0.0,

                "initial_parameter_estimate":
                    0.50,

                "changed_true_a":
                    None,
            }
        )

    for value in PROCESS_DISTURBANCE_GRID:

        conditions.append(
            {
                "class":
                    "process_disturbance",

                "name":
                    (
                        "process_disturbance_"
                        f"{value:.2f}"
                    ),

                "magnitude":
                    value,

                "measurement_noise_std":
                    0.50,

                "process_disturbance":
                    value,

                "initial_parameter_estimate":
                    0.50,

                "changed_true_a":
                    None,
            }
        )

    for value in PARAMETER_ESTIMATE_GRID:

        mismatch_magnitude = (
            0.92
            - value
        )

        conditions.append(
            {
                "class":
                    "parameter_mismatch",

                "name":
                    (
                        "parameter_mismatch_"
                        f"{value:.3f}"
                    ),

                "magnitude":
                    mismatch_magnitude,

                "raw_parameter_value":
                    value,

                "measurement_noise_std":
                    0.50,

                "process_disturbance":
                    0.0,

                "initial_parameter_estimate":
                    value,

                "changed_true_a":
                    None,
            }
        )

    for value in STRUCTURAL_CHANGE_GRID:

        mismatch_magnitude = (
            0.92
            - value
        )

        conditions.append(
            {
                "class":
                    "structural_change",

                "name":
                    (
                        "structural_change_"
                        f"{value:.3f}"
                    ),

                "magnitude":
                    mismatch_magnitude,

                "raw_parameter_value":
                    value,

                "measurement_noise_std":
                    0.50,

                "process_disturbance":
                    0.0,

                "initial_parameter_estimate":
                    0.50,

                "changed_true_a":
                    value,
            }
        )

    return conditions


CONDITIONS = build_conditions()


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


def classify_population(
    *,
    condition: dict,
    condition_index: int,
    replicate: int,
) -> list[dict]:

    classifications = []

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


def wilson_interval(
    successes: int,
    trials: int,
    *,
    z: float = 1.96,
) -> tuple[
    float,
    float,
]:

    if trials == 0:
        return (
            0.0,
            0.0,
        )

    proportion = (
        successes
        / trials
    )

    z_squared = (
        z ** 2
    )

    denominator = (
        1.0
        + z_squared
        / trials
    )

    center = (
        proportion
        + z_squared
        / (
            2.0
            * trials
        )
    )

    adjustment = (
        z
        * math.sqrt(
            (
                proportion
                * (
                    1.0
                    - proportion
                )
                / trials
            )
            +
            (
                z_squared
                / (
                    4.0
                    * trials ** 2
                )
            )
        )
    )

    lower = (
        center
        - adjustment
    ) / denominator

    upper = (
        center
        + adjustment
    ) / denominator

    return (
        max(
            0.0,
            lower,
        ),
        min(
            1.0,
            upper,
        ),
    )


def summarize_condition(
    *,
    condition: dict,
    condition_index: int,
) -> dict:

    population_rows = []

    for replicate in range(
        POPULATION_REPLICATES
    ):

        classifications = (
            classify_population(
                condition=condition,
                condition_index=(
                    condition_index
                ),
                replicate=replicate,
            )
        )

        stats = (
            population_statistics(
                classifications
            )
        )

        population_rows.append(
            stats
        )

    sufficient_count = sum(
        row[
            "evidence_sufficient"
        ]
        for row in population_rows
    )

    q_hat = (
        sufficient_count
        / POPULATION_REPLICATES
    )

    (
        q_low,
        q_high,
    ) = wilson_interval(
        sufficient_count,
        POPULATION_REPLICATES,
    )

    hard_values = [
        row[
            "hard_accuracy"
        ]
        for row in population_rows
    ]

    coverage_values = [
        row[
            "coverage"
        ]
        for row in population_rows
    ]

    selective_values = [
        row[
            "selective_accuracy"
        ]
        for row in population_rows
    ]

    fail_hard_fraction = (
        sum(
            value < 0.90
            for value in hard_values
        )
        / POPULATION_REPLICATES
    )

    fail_coverage_fraction = (
        sum(
            value < 0.80
            for value in coverage_values
        )
        / POPULATION_REPLICATES
    )

    fail_selective_fraction = (
        sum(
            value < 0.95
            for value in selective_values
        )
        / POPULATION_REPLICATES
    )

    return {
        "condition":
            condition["name"],

        "true_class":
            condition["class"],

        "magnitude":
            condition[
                "magnitude"
            ],

        "raw_parameter_value":
            condition.get(
                "raw_parameter_value",
                "",
            ),

        "population_size":
            POPULATION_SIZE,

        "population_replicates":
            POPULATION_REPLICATES,

        "q_hat":
            q_hat,

        "q_wilson_low":
            q_low,

        "q_wilson_high":
            q_high,

        "mean_hard_accuracy":
            statistics.mean(
                hard_values
            ),

        "std_hard_accuracy":
            statistics.stdev(
                hard_values
            ),

        "mean_coverage":
            statistics.mean(
                coverage_values
            ),

        "std_coverage":
            statistics.stdev(
                coverage_values
            ),

        "mean_selective_accuracy":
            statistics.mean(
                selective_values
            ),

        "std_selective_accuracy":
            statistics.stdev(
                selective_values
            ),

        "fail_hard_fraction":
            fail_hard_fraction,

        "fail_coverage_fraction":
            fail_coverage_fraction,

        "fail_selective_fraction":
            fail_selective_fraction,
    }


def run_experiment() -> list[dict]:

    rows = []

    for (
        condition_index,
        condition,
    ) in enumerate(
        CONDITIONS
    ):

        rows.append(
            summarize_condition(
                condition=condition,
                condition_index=(
                    condition_index
                ),
            )
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


def print_summary(
    rows: list[dict],
) -> None:

    print("=" * 126)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PROBABILISTIC DETECTABILITY CURVES"
    )

    print("=" * 126)

    for cause in [
        "measurement_noise",
        "process_disturbance",
        "parameter_mismatch",
        "structural_change",
    ]:

        print()
        print(
            cause
        )

        cause_rows = [
            row
            for row in rows
            if row[
                "true_class"
            ]
            == cause
        ]

        cause_rows = sorted(
            cause_rows,
            key=lambda row:
                float(
                    row[
                        "magnitude"
                    ]
                ),
        )

        for row in cause_rows:

            print(
                f"  "
                f"delta="
                f"{float(row['magnitude']):<8.4f} "
                f"q="
                f"{float(row['q_hat']):<6.3f} "
                f"Wilson=["
                f"{float(row['q_wilson_low']):.3f},"
                f"{float(row['q_wilson_high']):.3f}] "
                f"A="
                f"{float(row['mean_hard_accuracy']):.3f} "
                f"C="
                f"{float(row['mean_coverage']):.3f} "
                f"Sel="
                f"{float(row['mean_selective_accuracy']):.3f}"
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