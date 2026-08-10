import csv
import math
import random
import statistics
from pathlib import Path

from simulation.dynamic_uncertainty_estimator import (
    DynamicUncertaintyAdaptiveEstimator,
)

from simulation.normalized_innovation_estimator import (
    NormalizedInnovationAdaptiveEstimator,
)

from simulation.persistence_gated_estimator import (
    PersistenceGatedAdaptiveEstimator,
)


BASE_TRUE_A = 0.92
PROCESS_INPUT = 1.0
STEPS = 100

BASE_PROCESS_NOISE_STD = 0.05
BASE_MEASUREMENT_NOISE_STD = 0.50

BASE_INITIAL_PARAMETER_ESTIMATE = 0.50

LEARNING_RATE = 0.08
NORMALIZATION_EPSILON = 1.0

SEEDS = range(50)


ARCHITECTURES = [
    "dynamic_raw",
    "normalized_innovation",
    "persistence_gated",
]


REGIMES = [
    {
        "name": "nominal",
        "process_noise_std": 0.05,
        "measurement_noise_std": 0.50,
        "initial_parameter_estimate": 0.50,
        "parameter_change": False,
        "transient_disturbance": False,
    },
    {
        "name": "high_measurement_noise",
        "process_noise_std": 0.05,
        "measurement_noise_std": 1.00,
        "initial_parameter_estimate": 0.50,
        "parameter_change": False,
        "transient_disturbance": False,
    },
    {
        "name": "high_process_noise",
        "process_noise_std": 0.20,
        "measurement_noise_std": 0.50,
        "initial_parameter_estimate": 0.50,
        "parameter_change": False,
        "transient_disturbance": False,
    },
    {
        "name": "large_initial_parameter_mismatch",
        "process_noise_std": 0.05,
        "measurement_noise_std": 0.50,
        "initial_parameter_estimate": 0.20,
        "parameter_change": False,
        "transient_disturbance": False,
    },
    {
        "name": "abrupt_parameter_change",
        "process_noise_std": 0.05,
        "measurement_noise_std": 0.50,
        "initial_parameter_estimate": 0.50,
        "parameter_change": True,
        "transient_disturbance": False,
    },
    {
        "name": "transient_disturbance",
        "process_noise_std": 0.05,
        "measurement_noise_std": 0.50,
        "initial_parameter_estimate": 0.50,
        "parameter_change": False,
        "transient_disturbance": True,
    },
]


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


def create_estimator(
    architecture: str,
    *,
    initial_parameter_estimate: float,
    process_noise_variance: float,
    measurement_noise_variance: float,
):

    common = {
        "initial_parameter_estimate":
            initial_parameter_estimate,
        "learning_rate":
            LEARNING_RATE,
        "normalization_epsilon":
            NORMALIZATION_EPSILON,
        "base_process_noise_variance":
            process_noise_variance,
        "measurement_noise_variance":
            measurement_noise_variance,
        "innovation_memory":
            0.50,
        "min_inflation_strength":
            0.05,
        "max_inflation_strength":
            0.20,
        "transition_scale":
            0.25,
        "initial_state_estimate":
            0.0,
        "initial_state_covariance":
            1.0,
    }

    if architecture == "dynamic_raw":
        return DynamicUncertaintyAdaptiveEstimator(
            initial_parameter_estimate=(
                common[
                    "initial_parameter_estimate"
                ]
            ),
            learning_rate=(
                common["learning_rate"]
            ),
            normalization_epsilon=(
                common[
                    "normalization_epsilon"
                ]
            ),
            base_process_noise_variance=(
                common[
                    "base_process_noise_variance"
                ]
            ),
            measurement_noise_variance=(
                common[
                    "measurement_noise_variance"
                ]
            ),
            innovation_memory=(
                common["innovation_memory"]
            ),
            min_inflation_strength=(
                common[
                    "min_inflation_strength"
                ]
            ),
            max_inflation_strength=(
                common[
                    "max_inflation_strength"
                ]
            ),
            transition_scale=(
                common["transition_scale"]
            ),
            initial_state_estimate=0.0,
            initial_state_covariance=1.0,
        )

    if architecture == "normalized_innovation":
        return NormalizedInnovationAdaptiveEstimator(
            **common
        )

    if architecture == "persistence_gated":
        return PersistenceGatedAdaptiveEstimator(
            **common,
            consistency_threshold=1.0,
            required_consistency_steps=3,
            consistency_decay=0.70,
        )

    raise ValueError(
        f"Unknown architecture: {architecture}"
    )


def run_single_trial(
    *,
    architecture: str,
    regime: dict,
    seed: int,
) -> dict:

    random.seed(seed)

    process_noise_std = (
        regime["process_noise_std"]
    )

    measurement_noise_std = (
        regime["measurement_noise_std"]
    )

    estimator = create_estimator(
        architecture,
        initial_parameter_estimate=(
            regime[
                "initial_parameter_estimate"
            ]
        ),
        process_noise_variance=(
            process_noise_std ** 2
        ),
        measurement_noise_variance=(
            measurement_noise_std ** 2
        ),
    )

    true_state = 0.0
    true_a = BASE_TRUE_A

    state_errors = []
    parameter_errors = []

    for step in range(STEPS):

        if (
            regime["parameter_change"]
            and step == 50
        ):
            true_a = 0.80

        process_noise = random.gauss(
            0.0,
            process_noise_std,
        )

        true_state = (
            true_a * true_state
            + PROCESS_INPUT
            + process_noise
        )

        if (
            regime["transient_disturbance"]
            and step == 50
        ):
            true_state += 3.0

        measurement = (
            true_state
            + random.gauss(
                0.0,
                measurement_noise_std,
            )
        )

        result = estimator.step(
            control_input=PROCESS_INPUT,
            measurement=measurement,
        )

        state_errors.append(
            result.state_estimate
            - true_state
        )

        parameter_errors.append(
            abs(
                true_a
                - result.parameter_estimate
            )
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
        "final_parameter_error":
            parameter_errors[-1],
    }


def summarize_condition(
    *,
    architecture: str,
    regime: dict,
) -> dict:

    trials = [
        run_single_trial(
            architecture=architecture,
            regime=regime,
            seed=seed,
        )
        for seed in SEEDS
    ]

    full_rmse = [
        trial["state_rmse_full"]
        for trial in trials
    ]

    early_rmse = [
        trial["state_rmse_0_24"]
        for trial in trials
    ]

    middle_rmse = [
        trial["state_rmse_25_49"]
        for trial in trials
    ]

    late_rmse = [
        trial["state_rmse_50_99"]
        for trial in trials
    ]

    parameter_error = [
        trial["final_parameter_error"]
        for trial in trials
    ]

    return {
        "architecture":
            architecture,
        "regime":
            regime["name"],
        "runs":
            len(trials),

        "mean_state_rmse_full":
            statistics.mean(
                full_rmse
            ),
        "std_state_rmse_full":
            statistics.stdev(
                full_rmse
            ),

        "mean_state_rmse_0_24":
            statistics.mean(
                early_rmse
            ),

        "mean_state_rmse_25_49":
            statistics.mean(
                middle_rmse
            ),

        "mean_state_rmse_50_99":
            statistics.mean(
                late_rmse
            ),

        "mean_final_parameter_error":
            statistics.mean(
                parameter_error
            ),
        "std_final_parameter_error":
            statistics.stdev(
                parameter_error
            ),
    }


def run_experiment() -> list[dict]:

    results = []

    for regime in REGIMES:

        for architecture in ARCHITECTURES:

            results.append(
                summarize_condition(
                    architecture=architecture,
                    regime=regime,
                )
            )

    return results


def save_results(
    results: list[dict],
) -> Path:

    output_path = (
        Path("results")
        / "robustness_regime_comparison.csv"
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

    print("=" * 120)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "ROBUSTNESS REGIME COMPARISON"
    )

    print("=" * 120)

    for result in results:

        print(
            f"{result['regime']:<34}"
            f"{result['architecture']:<24}"
            f"RMSE="
            f"{result['mean_state_rmse_full']:.6f} "
            f"Late="
            f"{result['mean_state_rmse_50_99']:.6f} "
            f"Param="
            f"{result['mean_final_parameter_error']:.6f}"
        )

    print("=" * 120)


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