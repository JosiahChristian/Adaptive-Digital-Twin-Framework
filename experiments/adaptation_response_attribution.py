import csv
import random
import statistics
from pathlib import Path

from simulation.normalized_innovation_estimator import (
    NormalizedInnovationAdaptiveEstimator,
)


BASE_TRUE_A = 0.92
CHANGED_TRUE_A = 0.80

PROCESS_INPUT = 1.0
STEPS = 100
EVENT_STEP = 50

PROCESS_NOISE_STD = 0.05
MEASUREMENT_NOISE_STD = 0.50

INITIAL_PARAMETER_ESTIMATE = 0.50

LEARNING_RATE = 0.08
NORMALIZATION_EPSILON = 1.0

INNOVATION_MEMORY = 0.50
MIN_INFLATION_STRENGTH = 0.05
MAX_INFLATION_STRENGTH = 0.20
TRANSITION_SCALE = 0.25

RUNS_PER_REGIME = 100

PRE_WINDOW = range(35, 50)
EVENT_WINDOW = range(50, 60)
POST_WINDOW = range(60, 80)

REGIMES = [
    "process_disturbance",
    "structural_change",
]


def create_estimator():

    return NormalizedInnovationAdaptiveEstimator(
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
            PROCESS_NOISE_STD ** 2
        ),
        measurement_noise_variance=(
            MEASUREMENT_NOISE_STD ** 2
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
        initial_state_estimate=0.0,
        initial_state_covariance=1.0,
    )


def window_values(
    values: list[float],
    indices,
) -> list[float]:

    return [
        values[index]
        for index in indices
    ]


def mean_absolute(
    values: list[float],
) -> float:

    return statistics.mean(
        abs(value)
        for value in values
    )


def extract_adaptation_features(
    *,
    parameter_estimates: list[float],
    parameter_updates: list[float],
    dynamic_lambdas: list[float],
    effective_q_values: list[float],
    nis_values: list[float],
) -> dict:

    pre_parameters = window_values(
        parameter_estimates,
        PRE_WINDOW,
    )

    event_parameters = window_values(
        parameter_estimates,
        EVENT_WINDOW,
    )

    post_parameters = window_values(
        parameter_estimates,
        POST_WINDOW,
    )

    event_updates = window_values(
        parameter_updates,
        EVENT_WINDOW,
    )

    post_updates = window_values(
        parameter_updates,
        POST_WINDOW,
    )

    event_lambdas = window_values(
        dynamic_lambdas,
        EVENT_WINDOW,
    )

    post_lambdas = window_values(
        dynamic_lambdas,
        POST_WINDOW,
    )

    event_q = window_values(
        effective_q_values,
        EVENT_WINDOW,
    )

    post_q = window_values(
        effective_q_values,
        POST_WINDOW,
    )

    event_nis = window_values(
        nis_values,
        EVENT_WINDOW,
    )

    post_nis = window_values(
        nis_values,
        POST_WINDOW,
    )

    pre_parameter_mean = statistics.mean(
        pre_parameters
    )

    event_parameter_mean = statistics.mean(
        event_parameters
    )

    post_parameter_mean = statistics.mean(
        post_parameters
    )

    return {
        "pre_parameter_mean":
            pre_parameter_mean,

        "event_parameter_mean":
            event_parameter_mean,

        "post_parameter_mean":
            post_parameter_mean,

        "parameter_shift_event_vs_pre":
            (
                event_parameter_mean
                - pre_parameter_mean
            ),

        "parameter_shift_post_vs_pre":
            (
                post_parameter_mean
                - pre_parameter_mean
            ),

        "final_parameter_estimate":
            parameter_estimates[-1],

        "event_mean_abs_parameter_update":
            mean_absolute(
                event_updates
            ),

        "post_mean_abs_parameter_update":
            mean_absolute(
                post_updates
            ),

        "event_cumulative_abs_parameter_update":
            sum(
                abs(value)
                for value in event_updates
            ),

        "post_cumulative_abs_parameter_update":
            sum(
                abs(value)
                for value in post_updates
            ),

        "event_mean_lambda":
            statistics.mean(
                event_lambdas
            ),

        "post_mean_lambda":
            statistics.mean(
                post_lambdas
            ),

        "event_mean_effective_q":
            statistics.mean(
                event_q
            ),

        "post_mean_effective_q":
            statistics.mean(
                post_q
            ),

        "event_mean_nis":
            statistics.mean(
                event_nis
            ),

        "post_mean_nis":
            statistics.mean(
                post_nis
            ),
    }


def run_single_trajectory(
    *,
    regime: str,
    seed: int,
) -> dict:

    random.seed(seed)

    true_state = 0.0
    true_a = BASE_TRUE_A

    estimator = create_estimator()

    parameter_estimates = []
    parameter_updates = []
    dynamic_lambdas = []
    effective_q_values = []
    nis_values = []

    for step in range(STEPS):

        if (
            regime == "structural_change"
            and step == EVENT_STEP
        ):
            true_a = CHANGED_TRUE_A

        process_noise = random.gauss(
            0.0,
            PROCESS_NOISE_STD,
        )

        true_state = (
            true_a
            * true_state
            + PROCESS_INPUT
            + process_noise
        )

        if (
            regime == "process_disturbance"
            and step == EVENT_STEP
        ):
            true_state += 3.0

        measurement = (
            true_state
            + random.gauss(
                0.0,
                MEASUREMENT_NOISE_STD,
            )
        )

        result = estimator.step(
            control_input=PROCESS_INPUT,
            measurement=measurement,
        )

        parameter_estimates.append(
            result.parameter_estimate
        )

        parameter_updates.append(
            result.parameter_update
        )

        dynamic_lambdas.append(
            result.dynamic_inflation_strength
        )

        effective_q_values.append(
            result.effective_process_noise_variance
        )

        nis_values.append(
            result.normalized_innovation_squared
        )

    features = extract_adaptation_features(
        parameter_estimates=(
            parameter_estimates
        ),
        parameter_updates=(
            parameter_updates
        ),
        dynamic_lambdas=(
            dynamic_lambdas
        ),
        effective_q_values=(
            effective_q_values
        ),
        nis_values=(
            nis_values
        ),
    )

    return {
        "regime":
            regime,
        "seed":
            seed,
        **features,
    }


def run_experiment() -> list[dict]:

    rows = []

    for regime in REGIMES:

        for seed in range(
            RUNS_PER_REGIME
        ):

            rows.append(
                run_single_trajectory(
                    regime=regime,
                    seed=seed,
                )
            )

    return rows


def save_results(
    rows: list[dict],
) -> Path:

    results_directory = Path(
        "results"
    )

    results_directory.mkdir(
        exist_ok=True
    )

    output_path = (
        results_directory
        / "adaptation_response_attribution.csv"
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(
            rows
        )

    return output_path


def summarize_by_regime(
    rows: list[dict],
) -> None:

    features = [
        "parameter_shift_event_vs_pre",
        "parameter_shift_post_vs_pre",
        "event_mean_abs_parameter_update",
        "post_mean_abs_parameter_update",
        "event_cumulative_abs_parameter_update",
        "post_cumulative_abs_parameter_update",
        "event_mean_lambda",
        "post_mean_lambda",
        "event_mean_effective_q",
        "post_mean_effective_q",
        "event_mean_nis",
        "post_mean_nis",
        "final_parameter_estimate",
    ]

    print("=" * 114)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "ADAPTATION-RESPONSE ATTRIBUTION"
    )

    print("=" * 114)

    for regime in REGIMES:

        regime_rows = [
            row
            for row in rows
            if row["regime"] == regime
        ]

        print(
            f"\n{regime}"
        )

        for feature in features:

            values = [
                float(
                    row[feature]
                )
                for row in regime_rows
            ]

            print(
                f"  "
                f"{feature:<42}"
                f"mean="
                f"{statistics.mean(values):.6f} "
                f"std="
                f"{statistics.stdev(values):.6f}"
            )

    print("=" * 114)


def main() -> None:

    rows = run_experiment()

    output_path = save_results(
        rows
    )

    summarize_by_regime(
        rows
    )

    print(
        f"Results saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()