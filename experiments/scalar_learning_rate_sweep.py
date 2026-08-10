import csv
from pathlib import Path

from simulation.adaptive_scalar_system import (
    TRUE_A,
    run_experiment,
    summarize_experiment,
)


LEARNING_RATES = [
    0.01,
    0.02,
    0.04,
    0.08,
    0.12,
    0.20,
    0.40,
]

NOISE_STD_DEV = 0.0
RANDOM_SEED = 42

CONVERGENCE_TOLERANCE = 0.01


def calculate_convergence_step(
    records: list[dict],
    true_a: float,
    tolerance: float,
) -> int | None:
    """
    Returns the first step at which the parameter estimate enters
    the specified absolute-error tolerance and remains inside it
    for the rest of the experiment.

    Returns None if sustained convergence is not achieved.
    """

    for index, record in enumerate(records):

        remaining_records = records[index:]

        remains_within_tolerance = all(
            abs(
                true_a
                - remaining_record["estimated_a"]
            )
            <= tolerance
            for remaining_record in remaining_records
        )

        if remains_within_tolerance:
            return record["step"]

    return None


def run_learning_rate_condition(
    learning_rate: float,
) -> dict:

    records = run_experiment(
        noise_std_dev=NOISE_STD_DEV,
        random_seed=RANDOM_SEED,
        learning_rate=learning_rate,
    )

    summary = summarize_experiment(
        records,
        TRUE_A,
    )

    convergence_step = calculate_convergence_step(
        records,
        TRUE_A,
        CONVERGENCE_TOLERANCE,
    )

    return {
        "learning_rate":
            learning_rate,
        "final_estimated_a":
            summary["final_estimated_a"],
        "parameter_absolute_error":
            summary["parameter_absolute_error"],
        "parameter_relative_error":
            summary["parameter_relative_error"],
        "prediction_rmse":
            summary["prediction_rmse"],
        "bounded":
            summary["bounded"],
        "convergence_step":
            convergence_step,
    }


def run_sweep() -> list[dict]:

    return [
        run_learning_rate_condition(
            learning_rate
        )
        for learning_rate in LEARNING_RATES
    ]


def save_results(
    results: list[dict],
) -> Path:

    results_directory = Path("results")
    results_directory.mkdir(
        exist_ok=True
    )

    output_path = (
        results_directory
        / "scalar_learning_rate_sweep.csv"
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys(),
        )

        writer.writeheader()
        writer.writerows(results)

    return output_path


def print_results(
    results: list[dict],
) -> None:

    print("=" * 102)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "LEARNING-RATE SENSITIVITY SWEEP"
    )

    print("=" * 102)

    print(
        f"{'η':<10}"
        f"{'Final a':<14}"
        f"{'Abs Error':<14}"
        f"{'Rel Error':<14}"
        f"{'Pred RMSE':<14}"
        f"{'Bounded':<12}"
        f"{'Conv Step':<12}"
    )

    print("-" * 102)

    for result in results:

        convergence_step = (
            result["convergence_step"]
            if result["convergence_step"] is not None
            else "None"
        )

        print(
            f"{result['learning_rate']:<10.2f}"
            f"{result['final_estimated_a']:<14.6f}"
            f"{result['parameter_absolute_error']:<14.6f}"
            f"{result['parameter_relative_error']:<14.6f}"
            f"{result['prediction_rmse']:<14.6f}"
            f"{str(result['bounded']):<12}"
            f"{str(convergence_step):<12}"
        )

    print("=" * 102)


def main() -> None:

    results = run_sweep()

    output_path = save_results(
        results
    )

    print_results(
        results
    )

    print(
        f"Results saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()