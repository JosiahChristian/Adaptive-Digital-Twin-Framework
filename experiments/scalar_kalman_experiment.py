import csv
import math
import random
from pathlib import Path

from simulation.scalar_kalman_filter import (
    ScalarKalmanFilter,
)


TRUE_A = 0.92
PROCESS_INPUT = 1.0
STEPS = 60

PROCESS_NOISE_STD_DEV = 0.05
MEASUREMENT_NOISE_STD_DEV = 0.50

PROCESS_NOISE_VARIANCE = (
    PROCESS_NOISE_STD_DEV ** 2
)

MEASUREMENT_NOISE_VARIANCE = (
    MEASUREMENT_NOISE_STD_DEV ** 2
)

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

    kalman_filter = ScalarKalmanFilter(
        system_parameter=TRUE_A,
        process_noise_variance=(
            PROCESS_NOISE_VARIANCE
        ),
        measurement_noise_variance=(
            MEASUREMENT_NOISE_VARIANCE
        ),
        initial_estimate=0.0,
        initial_covariance=1.0,
    )

    records = []

    measurement_errors = []
    estimation_errors = []

    for step in range(STEPS):
        true_state = simulate_true_system(
            true_state
        )

        measurement = generate_measurement(
            true_state
        )

        estimated_state = (
            kalman_filter.step(
                control_input=PROCESS_INPUT,
                measurement=measurement,
            )
        )

        measurement_error = (
            measurement
            - true_state
        )

        estimation_error = (
            estimated_state.estimate
            - true_state
        )

        measurement_errors.append(
            measurement_error
        )

        estimation_errors.append(
            estimation_error
        )

        records.append(
            {
                "step":
                    step,
                "true_state":
                    true_state,
                "measurement":
                    measurement,
                "filtered_estimate":
                    estimated_state.estimate,
                "measurement_error":
                    measurement_error,
                "estimation_error":
                    estimation_error,
                "estimate_covariance":
                    estimated_state.covariance,
            }
        )

    summary = {
        "measurement_rmse":
            calculate_rmse(
                measurement_errors
            ),
        "filtered_estimate_rmse":
            calculate_rmse(
                estimation_errors
            ),
        "final_covariance":
            records[-1][
                "estimate_covariance"
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
        / "scalar_kalman_estimation.csv"
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
    print("=" * 72)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "SCALAR KALMAN STATE ESTIMATION"
    )

    print("=" * 72)

    print(
        f"Measurement RMSE:        "
        f"{summary['measurement_rmse']:.6f}"
    )

    print(
        f"Filtered estimate RMSE:  "
        f"{summary['filtered_estimate_rmse']:.6f}"
    )

    print(
        f"Final covariance:        "
        f"{summary['final_covariance']:.6f}"
    )

    print("=" * 72)


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