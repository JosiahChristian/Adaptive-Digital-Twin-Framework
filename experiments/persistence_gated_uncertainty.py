import csv
import math
import random
from pathlib import Path

from simulation.persistence_gated_estimator import (
    PersistenceGatedAdaptiveEstimator,
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

INNOVATION_MEMORY = 0.50
MIN_INFLATION_STRENGTH = 0.05
MAX_INFLATION_STRENGTH = 0.20
TRANSITION_SCALE = 0.25

CONSISTENCY_THRESHOLD = 1.0
REQUIRED_CONSISTENCY_STEPS = 3
CONSISTENCY_DECAY = 0.70

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


def run_experiment() -> tuple[
    list[dict],
    dict,
]:
    random.seed(
        RANDOM_SEED
    )

    true_state = 0.0

    estimator = (
        PersistenceGatedAdaptiveEstimator(
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
            min_inflation_strength=(
                MIN_INFLATION_STRENGTH
            ),
            max_inflation_strength=(
                MAX_INFLATION_STRENGTH
            ),
            transition_scale=(
                TRANSITION_SCALE
            ),
            consistency_threshold=(
                CONSISTENCY_THRESHOLD
            ),
            required_consistency_steps=(
                REQUIRED_CONSISTENCY_STEPS
            ),
            consistency_decay=(
                CONSISTENCY_DECAY
            ),
            initial_state_estimate=0.0,
            initial_state_covariance=1.0,
        )
    )

    records = []

    state_errors = []
    measurement_errors = []
    nis_values = []

    gate_activations = 0
    max_consistency_count = 0

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

        measurement_error = (
            measurement
            - true_state
        )

        state_errors.append(
            state_error
        )

        measurement_errors.append(
            measurement_error
        )

        nis_values.append(
            result.normalized_innovation_squared
        )

        if result.persistence_gate_active:
            gate_activations += 1

        max_consistency_count = max(
            max_consistency_count,
            result.consistency_count,
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
                "innovation_covariance":
                    result.innovation_covariance,
                "nis":
                    (
                        result
                        .normalized_innovation_squared
                    ),
                "excess_nis":
                    (
                        result
                        .excess_normalized_innovation
                    ),
                "mismatch_indicator":
                    result.mismatch_indicator,
                "dynamic_lambda":
                    (
                        result
                        .dynamic_inflation_strength
                    ),
                "effective_q":
                    (
                        result
                        .effective_process_noise_variance
                    ),
                "parameter_update":
                    result.parameter_update,
                "consistency_count":
                    result.consistency_count,
                "persistence_gate_active":
                    result.persistence_gate_active,
            }
        )

    summary = {
        "measurement_rmse":
            calculate_rmse(
                measurement_errors
            ),
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
        "measurement_rmse_50_99":
            calculate_rmse(
                measurement_errors[50:100]
            ),
        "mean_nis_full":
            sum(nis_values)
            / len(nis_values),
        "mean_nis_50_99":
            sum(
                nis_values[50:100]
            )
            / len(
                nis_values[50:100]
            ),
        "gate_activations":
            gate_activations,
        "gate_activation_fraction":
            gate_activations
            / STEPS,
        "max_consistency_count":
            max_consistency_count,
        "final_consistency_count":
            records[-1][
                "consistency_count"
            ],
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
        "final_dynamic_lambda":
            records[-1][
                "dynamic_lambda"
            ],
        "final_effective_q":
            records[-1][
                "effective_q"
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
        / "persistence_gated_uncertainty.csv"
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

    print("=" * 88)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "PERSISTENCE-GATED UNCERTAINTY"
    )

    print("=" * 88)

    for key, value in summary.items():

        if isinstance(value, int):
            print(
                f"{key:<38}: "
                f"{value}"
            )
        else:
            print(
                f"{key:<38}: "
                f"{value:.6f}"
            )

    print("=" * 88)


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