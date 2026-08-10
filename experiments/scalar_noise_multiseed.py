import csv
import statistics
from pathlib import Path

from simulation.adaptive_scalar_system import (
    TRUE_A,
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

SEEDS = range(50)


def run_noise_level(noise_std_dev: float) -> dict:
    parameter_errors = []
    prediction_rmses = []
    final_estimates = []
    bounded_runs = 0

    for seed in SEEDS:
        records = run_experiment(
            noise_std_dev=noise_std_dev,
            random_seed=seed,
        )

        summary = summarize_experiment(
            records,
            TRUE_A,
        )

        parameter_errors.append(
            summary["parameter_absolute_error"]
        )

        prediction_rmses.append(
            summary["prediction_rmse"]
        )

        final_estimates.append(
            summary["final_estimated_a"]
        )

        if summary["bounded"]:
            bounded_runs += 1

    return {
        "noise_std_dev": noise_std_dev,
        "runs": len(SEEDS),
        "mean_final_estimated_a":
            statistics.mean(final_estimates),
        "std_final_estimated_a":
            statistics.stdev(final_estimates),
        "mean_parameter_absolute_error":
            statistics.mean(parameter_errors),
        "std_parameter_absolute_error":
            statistics.stdev(parameter_errors),
        "mean_prediction_rmse":
            statistics.mean(prediction_rmses),
        "std_prediction_rmse":
            statistics.stdev(prediction_rmses),
        "bounded_runs": bounded_runs,
    }


def run_multiseed_sweep() -> list[dict]:
    return [
        run_noise_level(noise_std_dev)
        for noise_std_dev in NOISE_LEVELS
    ]


def save_results(results: list[dict]) -> Path:
    results_directory = Path("results")
    results_directory.mkdir(exist_ok=True)

    output_path = (
        results_directory
        / "scalar_noise_multiseed.csv"
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


def print_results(results: list[dict]) -> None:
    print("=" * 104)
    print(
        "ADAPTIVE DIGITAL TWIN — "
        "MULTI-SEED NOISE ROBUSTNESS EXPERIMENT"
    )
    print("=" * 104)

    print(
        f"{'Noise σ':<10}"
        f"{'Mean â':<12}"
        f"{'SD â':<12}"
        f"{'Mean |Δa|':<14}"
        f"{'SD |Δa|':<14}"
        f"{'Mean RMSE':<14}"
        f"{'Bounded':<10}"
    )

    print("-" * 104)

    for result in results:
        bounded = (
            f"{result['bounded_runs']}/"
            f"{result['runs']}"
        )

        print(
            f"{result['noise_std_dev']:<10.2f}"
            f"{result['mean_final_estimated_a']:<12.6f}"
            f"{result['std_final_estimated_a']:<12.6f}"
            f"{result['mean_parameter_absolute_error']:<14.6f}"
            f"{result['std_parameter_absolute_error']:<14.6f}"
            f"{result['mean_prediction_rmse']:<14.6f}"
            f"{bounded:<10}"
        )

    print("=" * 104)


def main() -> None:
    results = run_multiseed_sweep()

    output_path = save_results(results)

    print_results(results)

    print(
        f"Results saved to: {output_path}"
    )


if __name__ == "__main__":
    main()