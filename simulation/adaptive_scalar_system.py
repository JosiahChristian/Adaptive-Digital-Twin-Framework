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
    control_input: float
) -> float:
    """
    Evolves the true scalar dynamical system:

        x_(k+1) = a * x_k + u_k
    """
    return TRUE_A * state + control_input


def generate_observation(
    true_state: float
) -> float:
    """
    Generates a noisy observation:

        y_k = x_k + v_k
    """
    noise = random.gauss(
        0.0,
        NOISE_STD_DEV
    )

    return true_state + noise


def predict_twin_state(
    estimated_state: float,
    estimated_a: float,
    control_input: float
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
    previous_estimated_state: float
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

    The normalization reduces sensitivity to large
    state magnitudes.
    """

    normalization = (
        NORMALIZATION_EPSILON
        + previous_estimated_state ** 2
    )

    parameter_update = (
        LEARNING_RATE
        * prediction_error
        * previous_estimated_state
        / normalization
    )

    return estimated_a + parameter_update


def run_experiment() -> list[dict]:
    random.seed(RANDOM_SEED)

    true_state = 0.0
    estimated_state = 0.0
    estimated_a = INITIAL_TWIN_A

    records = []

    for step in range(STEPS):

        true_state = simulate_true_system(
            true_state,
            PROCESS_INPUT
        )

        observation = generate_observation(
            true_state
        )

        previous_estimated_state = (
            estimated_state
        )

        predicted_state = predict_twin_state(
            estimated_state,
            estimated_a,
            PROCESS_INPUT
        )

        prediction_error = (
            observation
            - predicted_state
        )

        previous_a = estimated_a

        estimated_a = update_parameter(
            estimated_a,
            prediction_error,
            previous_estimated_state
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
                "true_a": TRUE_A,
            }
        )

    return records


def calculate_rmse(
    records: list[dict]
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


def save_results(
    records: list[dict]
) -> Path:

    results_directory = Path("results")
    results_directory.mkdir(
        exist_ok=True
    )

    output_path = (
        results_directory
        / "adaptive_scalar_normalized.csv"
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=records[0].keys()
        )

        writer.writeheader()
        writer.writerows(records)

    return output_path


def print_summary(
    records: list[dict]
) -> None:

    final_record = records[-1]

    final_parameter_error = abs(
        TRUE_A
        - final_record["estimated_a"]
    )

    prediction_rmse = calculate_rmse(
        records
    )

    print("=" * 68)
    print(
        "ADAPTIVE DIGITAL TWIN — "
        "NORMALIZED ADAPTATION EXPERIMENT"
    )
    print("=" * 68)

    print(
        f"True system parameter a:        "
        f"{TRUE_A:.6f}"
    )

    print(
        f"Initial twin parameter a:       "
        f"{INITIAL_TWIN_A:.6f}"
    )

    print(
        f"Final estimated parameter a:    "
        f"{final_record['estimated_a']:.6f}"
    )

    print(
        f"Final parameter absolute error: "
        f"{final_parameter_error:.6f}"
    )

    print(
        f"Prediction RMSE:                 "
        f"{prediction_rmse:.6f}"
    )

    print(
        f"Final prediction error:          "
        f"{final_record['prediction_error']:.6f}"
    )

    print("=" * 68)


def main() -> None:

    records = run_experiment()

    output_path = save_results(
        records
    )

    print_summary(
        records
    )

    print(
        f"Results saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()