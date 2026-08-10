import csv
from pathlib import Path

from simulation.adaptive_scalar_system import (
    LEARNING_RATE,
    NORMALIZATION_EPSILON,
    PROCESS_INPUT,
    STEPS,
    TRUE_A,
    INITIAL_TWIN_A,
    run_experiment,
    summarize_experiment,
)


NOISE_LEVELS = [
    0.00,
    0.05,
    0.15,
    0.30,
    0.50,
    1.00,
]

RANDOM_SEED = 42


def run_noise_condition(
    noise_std_dev: float,
) -> dict:

    records = run_experiment(
        true_a=TRUE_A,
        initial_twin_a=INITIAL_TWIN_A,
        learning_rate=LEARNING_RATE,
        normalization_epsilon=NORMALIZATION_EPSILON,
        process_input=PROCESS_INPUT,
        noise_std_dev=noise_std_dev,
        steps=STEPS,
        random_seed=RANDOM_SEED,
    )

    summary = summarize_experiment(
        records,
        TRUE_A,
    )

    return {
        "noise_std_dev":
            noise_std_dev,
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
    }


def run_sweep() -> list[dict]:

    return [
        run_noise_condition(
            noise_std_dev
        )
        for noise_std_dev in NOISE_LEVELS
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
        / "scalar_noise_sweep.csv"
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

    print("=" * 88)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "MEASUREMENT NOISE ROBUSTNESS SWEEP"
    )

    print("=" * 88)

    print(
        f"{'Noise σ':<12}"
        f"{'Final a':<14}"
        f"{'Abs Error':<14}"
        f"{'Rel Error':<14}"
        f"{'Pred RMSE':<14}"
        f"{'Bounded':<10}"
    )

    print("-" * 88)

    for result in results:

        print(
            f"{result['noise_std_dev']:<12.2f}"
            f"{result['final_estimated_a']:<14.6f}"
            f"{result['parameter_absolute_error']:<14.6f}"
            f"{result['parameter_relative_error']:<14.6f}"
            f"{result['prediction_rmse']:<14.6f}"
            f"{str(result['bounded']):<10}"
        )

    print("=" * 88)


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