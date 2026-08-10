import csv
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
    RANDOM_SEED,
    simulate_true_system,
    generate_measurement,
    calculate_rmse,
)

from simulation.uncertainty_aware_adaptive_estimator import (
    UncertaintyAwareAdaptiveEstimator,
)


BETA_VALUES = [
    0.50,
    0.70,
    0.90,
    0.95,
    0.99,
]

LAMBDA_VALUES = [
    0.00,
    0.01,
    0.025,
    0.05,
    0.10,
    0.20,
]


def run_condition(
    beta: float,
    inflation_strength: float,
) -> dict:

    import random

    random.seed(
        RANDOM_SEED
    )

    true_state = 0.0

    estimator = (
        UncertaintyAwareAdaptiveEstimator(
            initial_parameter_estimate=(
                INITIAL_PARAMETER_ESTIMATE
            ),
            learning_rate=(
                LEARNING_RATE
            ),
            normalization_epsilon=(
                NORMALIZATION_EPSILON
            ),
            base_process_noise_variance=(
                BASE_PROCESS_NOISE_VARIANCE
            ),
            measurement_noise_variance=(
                MEASUREMENT_NOISE_VARIANCE
            ),
            innovation_memory=(
                beta
            ),
            inflation_strength=(
                inflation_strength
            ),
            initial_state_estimate=0.0,
            initial_state_covariance=1.0,
        )
    )

    records = []

    state_errors = []

    for step in range(STEPS):

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

        state_error = (
            result.state_estimate
            - true_state
        )

        state_errors.append(
            state_error
        )

        records.append(
            {
                "step": step,
                "true_state": true_state,
                "measurement": measurement,
                "state_estimate":
                    result.state_estimate,
                "state_covariance":
                    result.state_covariance,
                "parameter_estimate":
                    result.parameter_estimate,
                "mismatch_indicator":
                    result.mismatch_indicator,
                "effective_q":
                    (
                        result
                        .effective_process_noise_variance
                    ),
            }
        )

    rmse_full = calculate_rmse(
        state_errors
    )

    rmse_0_24 = calculate_rmse(
        state_errors[0:25]
    )

    rmse_25_49 = calculate_rmse(
        state_errors[25:50]
    )

    rmse_50_99 = calculate_rmse(
        state_errors[50:100]
    )

    final_parameter_estimate = (
        records[-1]["parameter_estimate"]
    )

    return {
        "beta":
            beta,
        "lambda":
            inflation_strength,
        "state_rmse_full":
            rmse_full,
        "state_rmse_0_24":
            rmse_0_24,
        "state_rmse_25_49":
            rmse_25_49,
        "state_rmse_50_99":
            rmse_50_99,
        "final_parameter_estimate":
            final_parameter_estimate,
        "final_parameter_absolute_error":
            abs(
                TRUE_A
                - final_parameter_estimate
            ),
        "final_covariance":
            records[-1]["state_covariance"],
        "final_mismatch_indicator":
            records[-1]["mismatch_indicator"],
        "final_effective_q":
            records[-1]["effective_q"],
    }


def run_sweep() -> list[dict]:

    results = []

    for beta in BETA_VALUES:

        for inflation_strength in LAMBDA_VALUES:

            result = run_condition(
                beta,
                inflation_strength,
            )

            results.append(
                result
            )

    return results


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
        / "uncertainty_hyperparameter_sweep.csv"
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


def print_best_results(
    results: list[dict],
) -> None:

    best_full = min(
        results,
        key=lambda result:
            result["state_rmse_full"],
    )

    best_early = min(
        results,
        key=lambda result:
            result["state_rmse_0_24"],
    )

    best_late = min(
        results,
        key=lambda result:
            result["state_rmse_50_99"],
    )

    best_parameter = min(
        results,
        key=lambda result:
            result[
                "final_parameter_absolute_error"
            ],
    )

    print("=" * 92)
    print(
        "ADAPTIVE DIGITAL TWIN — "
        "UNCERTAINTY HYPERPARAMETER SWEEP"
    )
    print("=" * 92)

    print(
        "Best full-run state RMSE:"
    )

    print(
        f"  beta={best_full['beta']}, "
        f"lambda={best_full['lambda']}, "
        f"RMSE={best_full['state_rmse_full']:.6f}"
    )

    print(
        "Best early state RMSE:"
    )

    print(
        f"  beta={best_early['beta']}, "
        f"lambda={best_early['lambda']}, "
        f"RMSE={best_early['state_rmse_0_24']:.6f}"
    )

    print(
        "Best late state RMSE:"
    )

    print(
        f"  beta={best_late['beta']}, "
        f"lambda={best_late['lambda']}, "
        f"RMSE={best_late['state_rmse_50_99']:.6f}"
    )

    print(
        "Best final parameter error:"
    )

    print(
        f"  beta={best_parameter['beta']}, "
        f"lambda={best_parameter['lambda']}, "
        f"error="
        f"{best_parameter['final_parameter_absolute_error']:.6f}"
    )

    print("=" * 92)


def main() -> None:

    results = run_sweep()

    output_path = save_results(
        results
    )

    print_best_results(
        results
    )

    print(
        f"Results saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()