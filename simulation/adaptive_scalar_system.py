import csv
import math
import random
from pathlib import Path


TRUE_A = 0.92
INITIAL_TWIN_A = 0.50

LEARNING_RATE = 0.08
NORMALIZATION_EPSILON = 1.0

PROCESS_INPUT = 1.0
NOISE_STD_DEV = 0.15
STEPS = 60

RANDOM_SEED = 42


def simulate_true_system(
    state: float,
    control_input: float,
    true_a: float = TRUE_A,
) -> float:
    """
    Evolves the true scalar dynamical system:

        x_(k+1) = a * x_k + u_k
    """
    return true_a * state + control_input


def generate_observation(
    true_state: float,
    noise_std_dev: float,
) -> float:
    """
    Generates a noisy observation:

        y_k = x_k + v_k
    """
    noise = random.gauss(
        0.0,
        noise_std_dev,
    )

    return true_state + noise


def predict_twin_state(
    estimated_state: float,
    estimated_a: float,
    control_input: float,
) -> float:
    """
    Predicts the next state using the digital twin:

        x_hat_(k+1) = a_hat_k * x_hat_k + u_k
    """
    return (
        estimated_a
        * estimated_state
        + control_input
    )


def update_parameter(
    estimated_a: float,
    prediction_error: float,
    previous_estimated_state: float,
    learning_rate: float,
    normalization_epsilon: float,
) -> float:
    """
    Performs normalized online parameter adaptation:

        a_hat_(k+1)
            =
        a_hat_k
        +
        eta *
        (error * x_hat_k)
        /
        (epsilon + x_hat_k^2)
    """

    normalization = (
        normalization_epsilon
        + previous_estimated_state ** 2
    )

    parameter_update = (
        learning_rate
        * prediction_error
        * previous_estimated_state
        / normalization
    )

    return estimated_a + parameter_update


def run_experiment(
    *,
    true_a: float = TRUE_A,
    initial_twin_a: float = INITIAL_TWIN_A,
    learning_rate: float = LEARNING_RATE,
    normalization_epsilon: float = NORMALIZATION_EPSILON,
    process_input: float = PROCESS_INPUT,
    noise_std_dev: float = NOISE_STD_DEV,
    steps: int = STEPS,
    random_seed: int = RANDOM_SEED,
) -> list[dict]:

    random.seed(random_seed)

    true_state = 0.0
    estimated_state = 0.0
    estimated_a = initial_twin_a

    records = []

    for step in range(steps):

        true_state = simulate_true_system(
            true_state,
            process_input,
            true_a,
        )

        observation = generate_observation(
            true_state,
            noise_std_dev,
        )

        previous_estimated_state = (
            estimated_state
        )

        predicted_state = predict_twin_state(
            estimated_state,
            estimated_a,
            process_input,
        )

        prediction_error = (
            observation
            - predicted_state
        )

        previous_a = estimated_a

        estimated_a = update_parameter(
            estimated_a,
            prediction_error,
            previous_estimated_state,
            learning_rate,
            normalization_epsilon,
        )

        parameter_update = (
            estimated_a
            - previous_a
        )

        estimated_state = observation

        records.append(
            {
                "step": step,
                "true_state": true_state,
                "observation": observation,
                "predicted_state": predicted_state,
                "prediction_error": prediction_error,
                "parameter_update": parameter_update,
                "estimated_a": estimated_a,
                "true_a": true_a,
            }
        )

    return records


def calculate_prediction_rmse(
    records: list[dict],
) -> float:

    squared_errors = [
        record["prediction_error"] ** 2
        for record in records
    ]

    mean_squared_error = (
        sum(squared_errors)
        / len(squared_errors)
    )

    return math.sqrt(
        mean_squared_error
    )


def calculate_parameter_error(
    records: list[dict],
    true_a: float,
) -> float:

    final_estimated_a = (
        records[-1]["estimated_a"]
    )

    return abs(
        true_a
        - final_estimated_a
    )


def summarize_experiment(
    records: list[dict],
    true_a: float,
) -> dict:

    final_estimated_a = (
        records[-1]["estimated_a"]
    )

    absolute_error = (
        calculate_parameter_error(
            records,
            true_a,
        )
    )

    relative_error = (
        absolute_error
        / abs(true_a)
    )

    prediction_rmse = (
        calculate_prediction_rmse(
            records
        )
    )

    bounded = all(
        abs(record["estimated_a"]) < 2.0
        for record in records
    )

    return {
        "final_estimated_a":
            final_estimated_a,
        "parameter_absolute_error":
            absolute_error,
        "parameter_relative_error":
            relative_error,
        "prediction_rmse":
            prediction_rmse,
        "bounded":
            bounded,
    }


def save_results(
    records: list[dict],
    filename: str = "adaptive_scalar_normalized.csv",
) -> Path:

    results_directory = Path("results")

    results_directory.mkdir(
        exist_ok=True
    )

    output_path = (
        results_directory
        / filename
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
        writer.writerows(records)

    return output_path


def print_summary(
    summary: dict,
    true_a: float,
    initial_twin_a: float,
) -> None:

    print("=" * 68)
    print(
        "ADAPTIVE DIGITAL TWIN — "
        "NORMALIZED ADAPTATION EXPERIMENT"
    )
    print("=" * 68)

    print(
        f"True system parameter a:        "
        f"{true_a:.6f}"
    )

    print(
        f"Initial twin parameter a:       "
        f"{initial_twin_a:.6f}"
    )

    print(
        f"Final estimated parameter a:    "
        f"{summary['final_estimated_a']:.6f}"
    )

    print(
        f"Final parameter absolute error: "
        f"{summary['parameter_absolute_error']:.6f}"
    )

    print(
        f"Prediction RMSE:                 "
        f"{summary['prediction_rmse']:.6f}"
    )

    print(
        f"Adaptation remained bounded:    "
        f"{summary['bounded']}"
    )

    print("=" * 68)


def main() -> None:

    records = run_experiment()

    summary = summarize_experiment(
        records,
        TRUE_A,
    )

    output_path = save_results(
        records
    )

    print_summary(
        summary,
        TRUE_A,
        INITIAL_TWIN_A,
    )

    print(
        f"Results saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()