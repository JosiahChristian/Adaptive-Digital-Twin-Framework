import csv
import math
import random
from pathlib import Path

from simulation.integrated_adaptive_estimator import (
    IntegratedAdaptiveEstimator,
)


TRUE_A = 0.92
INITIAL_PARAMETER_ESTIMATE = 0.50

PROCESS_INPUT = 1.0
STEPS = 100

PROCESS_NOISE_STD_DEV = 0.05
MEASUREMENT_NOISE_STD_DEV = 0.50

PROCESS_NOISE_VARIANCE = (
    PROCESS_NOISE_STD_DEV ** 2
)

MEASUREMENT_NOISE_VARIANCE = (
    MEASUREMENT_NOISE_STD_DEV ** 2
)

LEARNING_RATE = 0.08
NORMALIZATION_EPSILON = 1.0

RANDOM_SEED = 42


def simulate_true_system(
    state: float,
) -> float:

    process_noise = random.gauss(
        0.0,
        PROCESS_NOISE_STD_DEV,
    )

    return (
        TRUE_A * state
        + PROCESS_INPUT
        + process_noise
    )


def generate_measurement(
    true_state: float,
) -> float:

    measurement_noise = random.gauss(
        0.0,
        MEASUREMENT_NOISE_STD_DEV,
    )

    return (
        true_state
        + measurement_noise
    )


def calculate_rmse(
    errors: list[float],
) -> float:

    mean_squared_error = (
        sum(
            error ** 2
            for error in errors
        )
        / len(errors)
    )

    return math.sqrt(
        mean_squared_error
    )


def run_experiment() -> tuple[
    list[dict],
    dict,
]:

    random.seed(
        RANDOM_SEED
    )

    true_state = 0.0

    estimator = IntegratedAdaptiveEstimator(
        initial_parameter_estimate=(
            INITIAL_PARAMETER_ESTIMATE
        ),
        learning_rate=(
            LEARNING_RATE
        ),
        normalization_epsilon=(
            NORMALIZATION_EPSILON
        ),
        process_noise_variance=(
            PROCESS_NOISE_VARIANCE
        ),
        measurement_noise_variance=(
            MEASUREMENT_NOISE_VARIANCE
        ),
        initial_state_estimate=0.0,
        initial_state_covariance=1.0,
    )

    records = []

    measurement_errors = []
    state_estimation_errors = []

    for step in range(STEPS):

        true_state = simulate_true_system(
            true_state
        )

        measurement = generate_measurement(
            true_state
        )

        adaptive_estimate = estimator.step(
            control_input=PROCESS_INPUT,
            measurement=measurement,
        )

        measurement_error = (
            measurement
            - true_state
        )

        state_estimation_error = (
            adaptive_estimate.state_estimate
            - true_state
        )

        parameter_error = (
            TRUE_A
            - adaptive_estimate.parameter_estimate
        )

        measurement_errors.append(
            measurement_error
        )

        state_estimation_errors.append(
            state_estimation_error
        )

        records.append(
            {
                "step":
                    step,
                "true_state":
                    true_state,
                "measurement":
                    measurement,
                "state_estimate":
                    adaptive_estimate.state_estimate,
                "state_covariance":
                    adaptive_estimate.state_covariance,
                "parameter_estimate":
                    adaptive_estimate.parameter_estimate,
                "parameter_error":
                    parameter_error,
                "innovation":
                    adaptive_estimate.innovation,
                "parameter_update":
                    adaptive_estimate.parameter_update,
            }
        )

    final_record = records[-1]

    summary = {
        "measurement_rmse":
            calculate_rmse(
                measurement_errors
            ),
        "state_estimation_rmse":
            calculate_rmse(
                state_estimation_errors
            ),
        "final_parameter_estimate":
            final_record[
                "parameter_estimate"
            ],
        "final_parameter_absolute_error":
            abs(
                TRUE_A
                - final_record[
                    "parameter_estimate"
                ]
            ),
        "final_state_covariance":
            final_record[
                "state_covariance"
            ],
    }

    return records, summary


def save_results(
    records: list[dict],
) -> Path:

    results_directory = Path(
        "results"
    )

    results_directory.mkdir(
        exist_ok=True
    )

    output_path = (
        results_directory
        / "integrated_adaptive_estimation.csv"
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=records[0].keys(),
        )

        writer.writeheader()
        writer.writerows(
            records
        )

    return output_path


def print_summary(
    summary: dict,
) -> None:

    print("=" * 76)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "INTEGRATED STATE + PARAMETER ESTIMATION"
    )

    print("=" * 76)

    print(
        f"Measurement RMSE:               "
        f"{summary['measurement_rmse']:.6f}"
    )

    print(
        f"State estimation RMSE:          "
        f"{summary['state_estimation_rmse']:.6f}"
    )

    print(
        f"Final parameter estimate:       "
        f"{summary['final_parameter_estimate']:.6f}"
    )

    print(
        f"Final parameter absolute error: "
        f"{summary['final_parameter_absolute_error']:.6f}"
    )

    print(
        f"Final state covariance:         "
        f"{summary['final_state_covariance']:.6f}"
    )

    print("=" * 76)


def main() -> None:

    records, summary = (
        run_experiment()
    )

    output_path = save_results(
        records
    )

    print_summary(
        summary
    )

    print(
        f"Results saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()