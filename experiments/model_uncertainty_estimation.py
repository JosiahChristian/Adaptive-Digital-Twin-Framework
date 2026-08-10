import csv
import math
import random
from pathlib import Path

from simulation.uncertainty_aware_adaptive_estimator import (
    UncertaintyAwareAdaptiveEstimator,
)


TRUE_A = 0.92
INITIAL_PARAMETER_ESTIMATE = 0.50

PROCESS_INPUT = 1.0
STEPS = 100

PROCESS_NOISE_STD_DEV = 0.05
MEASUREMENT_NOISE_STD_DEV = 0.50

BASE_PROCESS_NOISE_VARIANCE = (
    PROCESS_NOISE_STD_DEV ** 2
)

MEASUREMENT_NOISE_VARIANCE = (
    MEASUREMENT_NOISE_STD_DEV ** 2
)

LEARNING_RATE = 0.08
NORMALIZATION_EPSILON = 1.0

INNOVATION_MEMORY = 0.90
INFLATION_STRENGTH = 0.05

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

    return math.sqrt(
        sum(
            error ** 2
            for error in errors
        )
        / len(errors)
    )


def calculate_window_rmse(
    records: list[dict],
    start: int,
    end: int,
) -> float:

    errors = [
        record["state_estimate"]
        - record["true_state"]
        for record in records[start:end]
    ]

    return calculate_rmse(
        errors
    )


def calculate_measurement_window_rmse(
    records: list[dict],
    start: int,
    end: int,
) -> float:

    errors = [
        record["measurement"]
        - record["true_state"]
        for record in records[start:end]
    ]

    return calculate_rmse(
        errors
    )


def run_experiment() -> tuple[
    list[dict],
    dict,
]:

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
                INNOVATION_MEMORY
            ),
            inflation_strength=(
                INFLATION_STRENGTH
            ),
            initial_state_estimate=0.0,
            initial_state_covariance=1.0,
        )
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

        result = estimator.step(
            control_input=PROCESS_INPUT,
            measurement=measurement,
        )

        measurement_error = (
            measurement
            - true_state
        )

        state_error = (
            result.state_estimate
            - true_state
        )

        measurement_errors.append(
            measurement_error
        )

        state_estimation_errors.append(
            state_error
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
                    result.state_estimate,
                "state_covariance":
                    result.state_covariance,
                "parameter_estimate":
                    result.parameter_estimate,
                "parameter_error":
                    (
                        TRUE_A
                        - result.parameter_estimate
                    ),
                "innovation":
                    result.innovation,
                "parameter_update":
                    result.parameter_update,
                "mismatch_indicator":
                    result.mismatch_indicator,
                "effective_process_noise_variance":
                    (
                        result
                        .effective_process_noise_variance
                    ),
            }
        )

    summary = {
        "measurement_rmse":
            calculate_rmse(
                measurement_errors
            ),
        "state_rmse_full":
            calculate_rmse(
                state_estimation_errors
            ),
        "state_rmse_0_24":
            calculate_window_rmse(
                records,
                0,
                25,
            ),
        "state_rmse_25_49":
            calculate_window_rmse(
                records,
                25,
                50,
            ),
        "state_rmse_50_99":
            calculate_window_rmse(
                records,
                50,
                100,
            ),
        "measurement_rmse_50_99":
            calculate_measurement_window_rmse(
                records,
                50,
                100,
            ),
        "final_parameter_estimate":
            records[-1][
                "parameter_estimate"
            ],
        "final_parameter_absolute_error":
            abs(
                TRUE_A
                - records[-1][
                    "parameter_estimate"
                ]
            ),
        "final_covariance":
            records[-1][
                "state_covariance"
            ],
        "final_mismatch_indicator":
            records[-1][
                "mismatch_indicator"
            ],
        "final_effective_q":
            records[-1][
                "effective_process_noise_variance"
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
        / "model_uncertainty_estimation.csv"
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

    print("=" * 82)
    print(
        "ADAPTIVE DIGITAL TWIN — "
        "MODEL-UNCERTAINTY-AWARE ESTIMATION"
    )
    print("=" * 82)

    print(
        f"Measurement RMSE:               "
        f"{summary['measurement_rmse']:.6f}"
    )

    print(
        f"State RMSE full:                "
        f"{summary['state_rmse_full']:.6f}"
    )

    print(
        f"State RMSE steps 0-24:          "
        f"{summary['state_rmse_0_24']:.6f}"
    )

    print(
        f"State RMSE steps 25-49:         "
        f"{summary['state_rmse_25_49']:.6f}"
    )

    print(
        f"State RMSE steps 50-99:         "
        f"{summary['state_rmse_50_99']:.6f}"
    )

    print(
        f"Measurement RMSE steps 50-99:   "
        f"{summary['measurement_rmse_50_99']:.6f}"
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
        f"Final covariance:               "
        f"{summary['final_covariance']:.6f}"
    )

    print(
        f"Final mismatch indicator:       "
        f"{summary['final_mismatch_indicator']:.6f}"
    )

    print(
        f"Final effective Q:               "
        f"{summary['final_effective_q']:.6f}"
    )

    print("=" * 82)


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