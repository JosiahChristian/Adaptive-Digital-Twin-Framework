import csv
import random
import statistics
from pathlib import Path

from experiments.model_uncertainty_estimation import (
    TRUE_A,
    INITIAL_PARAMETER_ESTIMATE,
    PROCESS_INPUT,
    STEPS,
    BASE_PROCESS_NOISE_VARIANCE,
    MEASUREMENT_NOISE_VARIANCE,
    LEARNING_RATE,
    NORMALIZATION_EPSILON,
    simulate_true_system,
    generate_measurement,
    calculate_rmse,
)

from simulation.uncertainty_aware_adaptive_estimator import (
    UncertaintyAwareAdaptiveEstimator,
)


CONFIGURATIONS = [
    {
        "name": "control_no_inflation",
        "beta": 0.50,
        "lambda": 0.00,
    },
    {
        "name": "original_exp006",
        "beta": 0.90,
        "lambda": 0.05,
    },
    {
        "name": "moderate_inflation",
        "beta": 0.50,
        "lambda": 0.10,
    },
    {
        "name": "strong_state_candidate",
        "beta": 0.50,
        "lambda": 0.20,
    },
    {
        "name": "high_memory_strong_inflation",
        "beta": 0.90,
        "lambda": 0.20,
    },
    {
        "name": "parameter_focused",
        "beta": 0.99,
        "lambda": 0.20,
    },
]

SEEDS = range(50)


def run_single_seed(
    *,
    beta: float,
    inflation_strength: float,
    seed: int,
) -> dict:

    random.seed(seed)

    true_state = 0.0

    estimator = (
        UncertaintyAwareAdaptiveEstimator(
            initial_parameter_estimate=(
                INITIAL_PARAMETER_ESTIMATE
            ),
            learning_rate=LEARNING_RATE,
            normalization_epsilon=(
                NORMALIZATION_EPSILON
            ),
            base_process_noise_variance=(
                BASE_PROCESS_NOISE_VARIANCE
            ),
            measurement_noise_variance=(
                MEASUREMENT_NOISE_VARIANCE
            ),
            innovation_memory=beta,
            inflation_strength=(
                inflation_strength
            ),
            initial_state_estimate=0.0,
            initial_state_covariance=1.0,
        )
    )

    state_errors = []

    for _ in range(STEPS):

        true_state = simulate_true_system(
            true_state
        )

        measurement = generate_measurement(
            true_state
        )

        result = estimator.step(
            control_input=PROCESS_INPUT,
            measurement=measurement,
        )

        state_errors.append(
            result.state_estimate
            - true_state
        )

    return {
        "state_rmse_full":
            calculate_rmse(
                state_errors
            ),
        "state_rmse_0_24":
            calculate_rmse(
                state_errors[0:25]
            ),
        "state_rmse_25_49":
            calculate_rmse(
                state_errors[25:50]
            ),
        "state_rmse_50_99":
            calculate_rmse(
                state_errors[50:100]
            ),
        "final_parameter_absolute_error":
            abs(
                TRUE_A
                - estimator.parameter_estimate
            ),
    }


def summarize_configuration(
    configuration: dict,
) -> dict:

    runs = [
        run_single_seed(
            beta=configuration["beta"],
            inflation_strength=(
                configuration["lambda"]
            ),
            seed=seed,
        )
        for seed in SEEDS
    ]

    full_rmses = [
        run["state_rmse_full"]
        for run in runs
    ]

    early_rmses = [
        run["state_rmse_0_24"]
        for run in runs
    ]

    middle_rmses = [
        run["state_rmse_25_49"]
        for run in runs
    ]

    late_rmses = [
        run["state_rmse_50_99"]
        for run in runs
    ]

    parameter_errors = [
        run[
            "final_parameter_absolute_error"
        ]
        for run in runs
    ]

    return {
        "name":
            configuration["name"],
        "beta":
            configuration["beta"],
        "lambda":
            configuration["lambda"],
        "runs":
            len(runs),

        "mean_state_rmse_full":
            statistics.mean(
                full_rmses
            ),
        "std_state_rmse_full":
            statistics.stdev(
                full_rmses
            ),

        "mean_state_rmse_0_24":
            statistics.mean(
                early_rmses
            ),
        "std_state_rmse_0_24":
            statistics.stdev(
                early_rmses
            ),

        "mean_state_rmse_25_49":
            statistics.mean(
                middle_rmses
            ),
        "std_state_rmse_25_49":
            statistics.stdev(
                middle_rmses
            ),

        "mean_state_rmse_50_99":
            statistics.mean(
                late_rmses
            ),
        "std_state_rmse_50_99":
            statistics.stdev(
                late_rmses
            ),

        "mean_parameter_absolute_error":
            statistics.mean(
                parameter_errors
            ),
        "std_parameter_absolute_error":
            statistics.stdev(
                parameter_errors
            ),
    }


def run_experiment() -> list[dict]:

    return [
        summarize_configuration(
            configuration
        )
        for configuration
        in CONFIGURATIONS
    ]


def save_results(
    results: list[dict],
) -> Path:

    results_directory = Path(
        "results"
    )

    results_directory.mkdir(
        exist_ok=True
    )

    output_path = (
        results_directory
        / "uncertainty_multiseed_robustness.csv"
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
        writer.writerows(
            results
        )

    return output_path


def print_results(
    results: list[dict],
) -> None:

    print("=" * 112)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "MULTI-SEED UNCERTAINTY ROBUSTNESS"
    )

    print("=" * 112)

    print(
        f"{'Configuration':<30}"
        f"{'Mean Full':<14}"
        f"{'Mean Early':<14}"
        f"{'Mean Late':<14}"
        f"{'Mean Param Err':<16}"
    )

    print("-" * 112)

    for result in results:

        print(
            f"{result['name']:<30}"
            f"{result['mean_state_rmse_full']:<14.6f}"
            f"{result['mean_state_rmse_0_24']:<14.6f}"
            f"{result['mean_state_rmse_50_99']:<14.6f}"
            f"{result['mean_parameter_absolute_error']:<16.6f}"
        )

    print("=" * 112)


def main() -> None:

    results = run_experiment()

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