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

BASE_PROCESS_NOISE_STD = 0.05
BASE_MEASUREMENT_NOISE_STD = 0.50

BASE_INITIAL_PARAMETER_ESTIMATE = 0.50
LARGE_MISMATCH_INITIAL_ESTIMATE = 0.20

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

EPSILON = 1e-12


REGIMES = [
    "measurement_noise",
    "process_disturbance",
    "parameter_mismatch",
    "structural_change",
]


def create_estimator(
    *,
    initial_parameter_estimate: float,
    process_noise_std: float,
    measurement_noise_std: float,
):

    return NormalizedInnovationAdaptiveEstimator(
        initial_parameter_estimate=(
            initial_parameter_estimate
        ),
        learning_rate=(
            LEARNING_RATE
        ),
        normalization_epsilon=(
            NORMALIZATION_EPSILON
        ),
        base_process_noise_variance=(
            process_noise_std ** 2
        ),
        measurement_noise_variance=(
            measurement_noise_std ** 2
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


def lag_one_autocorrelation(
    values: list[float],
) -> float:

    if len(values) < 2:
        return 0.0

    mean_value = statistics.mean(
        values
    )

    denominator = sum(
        (
            value
            - mean_value
        ) ** 2
        for value in values
    )

    if denominator == 0.0:
        return 0.0

    numerator = sum(
        (
            values[index]
            - mean_value
        )
        * (
            values[index - 1]
            - mean_value
        )
        for index in range(
            1,
            len(values),
        )
    )

    return (
        numerator
        / denominator
    )


def longest_threshold_run(
    values: list[float],
    *,
    threshold: float,
) -> int:

    longest_run = 0
    current_run = 0

    for value in values:

        if value > threshold:
            current_run += 1

            longest_run = max(
                longest_run,
                current_run,
            )

        else:
            current_run = 0

    return longest_run


def window_values(
    values: list[float],
    indices,
) -> list[float]:

    return [
        values[index]
        for index in indices
    ]


def extract_temporal_features(
    *,
    innovations: list[float],
    nis_values: list[float],
) -> dict:

    pre_nis = window_values(
        nis_values,
        PRE_WINDOW,
    )

    event_nis = window_values(
        nis_values,
        EVENT_WINDOW,
    )

    post_nis = window_values(
        nis_values,
        POST_WINDOW,
    )

    pre_innovations = window_values(
        innovations,
        PRE_WINDOW,
    )

    event_innovations = window_values(
        innovations,
        EVENT_WINDOW,
    )

    post_innovations = window_values(
        innovations,
        POST_WINDOW,
    )

    mean_pre_nis = statistics.mean(
        pre_nis
    )

    mean_event_nis = statistics.mean(
        event_nis
    )

    mean_post_nis = statistics.mean(
        post_nis
    )

    mean_pre_abs_innovation = statistics.mean(
        abs(value)
        for value in pre_innovations
    )

    mean_event_abs_innovation = statistics.mean(
        abs(value)
        for value in event_innovations
    )

    mean_post_abs_innovation = statistics.mean(
        abs(value)
        for value in post_innovations
    )

    pre_autocorrelation = (
        lag_one_autocorrelation(
            pre_innovations
        )
    )

    event_autocorrelation = (
        lag_one_autocorrelation(
            event_innovations
        )
    )

    post_autocorrelation = (
        lag_one_autocorrelation(
            post_innovations
        )
    )

    return {
        "mean_pre_nis":
            mean_pre_nis,

        "mean_event_nis":
            mean_event_nis,

        "mean_post_nis":
            mean_post_nis,

        "delta_event_vs_pre_nis":
            (
                mean_event_nis
                - mean_pre_nis
            ),

        "delta_post_vs_pre_nis":
            (
                mean_post_nis
                - mean_pre_nis
            ),

        "recovery_ratio_nis":
            (
                mean_post_nis
                / (
                    mean_event_nis
                    + EPSILON
                )
            ),

        "event_max_nis":
            max(
                event_nis
            ),

        "post_max_nis":
            max(
                post_nis
            ),

        "event_longest_nis_run_above_1":
            longest_threshold_run(
                event_nis,
                threshold=1.0,
            ),

        "post_longest_nis_run_above_1":
            longest_threshold_run(
                post_nis,
                threshold=1.0,
            ),

        "mean_pre_absolute_innovation":
            mean_pre_abs_innovation,

        "mean_event_absolute_innovation":
            mean_event_abs_innovation,

        "mean_post_absolute_innovation":
            mean_post_abs_innovation,

        "delta_event_vs_pre_absolute_innovation":
            (
                mean_event_abs_innovation
                - mean_pre_abs_innovation
            ),

        "delta_post_vs_pre_absolute_innovation":
            (
                mean_post_abs_innovation
                - mean_pre_abs_innovation
            ),

        "pre_innovation_lag1_autocorrelation":
            pre_autocorrelation,

        "event_innovation_lag1_autocorrelation":
            event_autocorrelation,

        "post_innovation_lag1_autocorrelation":
            post_autocorrelation,

        "delta_event_vs_pre_autocorrelation":
            (
                event_autocorrelation
                - pre_autocorrelation
            ),

        "delta_post_vs_pre_autocorrelation":
            (
                post_autocorrelation
                - pre_autocorrelation
            ),
    }


def run_single_trajectory(
    *,
    regime: str,
    seed: int,
) -> dict:

    random.seed(
        seed
    )

    true_state = 0.0
    true_a = BASE_TRUE_A

    process_noise_std = (
        BASE_PROCESS_NOISE_STD
    )

    measurement_noise_std = (
        BASE_MEASUREMENT_NOISE_STD
    )

    initial_parameter_estimate = (
        BASE_INITIAL_PARAMETER_ESTIMATE
    )

    if regime == "measurement_noise":
        measurement_noise_std = 1.0

    elif regime == "parameter_mismatch":
        initial_parameter_estimate = (
            LARGE_MISMATCH_INITIAL_ESTIMATE
        )

    elif regime not in (
        "process_disturbance",
        "structural_change",
    ):
        raise ValueError(
            f"Unknown regime: {regime}"
        )

    estimator = create_estimator(
        initial_parameter_estimate=(
            initial_parameter_estimate
        ),
        process_noise_std=(
            process_noise_std
        ),
        measurement_noise_std=(
            measurement_noise_std
        ),
    )

    innovations = []
    nis_values = []

    for step in range(STEPS):

        if (
            regime == "structural_change"
            and step == EVENT_STEP
        ):
            true_a = CHANGED_TRUE_A

        process_noise = random.gauss(
            0.0,
            process_noise_std,
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
                measurement_noise_std,
            )
        )

        result = estimator.step(
            control_input=PROCESS_INPUT,
            measurement=measurement,
        )

        innovations.append(
            result.innovation
        )

        nis_values.append(
            result.normalized_innovation_squared
        )

    temporal_features = (
        extract_temporal_features(
            innovations=innovations,
            nis_values=nis_values,
        )
    )

    return {
        "regime":
            regime,
        "seed":
            seed,
        **temporal_features,
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
        / "temporal_residual_attribution.csv"
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

    key_features = [
        "mean_pre_nis",
        "mean_event_nis",
        "mean_post_nis",
        "delta_event_vs_pre_nis",
        "delta_post_vs_pre_nis",
        "recovery_ratio_nis",
        "event_max_nis",
        "post_longest_nis_run_above_1",
        "delta_event_vs_pre_autocorrelation",
        "delta_post_vs_pre_autocorrelation",
    ]

    print("=" * 112)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "TEMPORAL RESIDUAL ATTRIBUTION"
    )

    print("=" * 112)

    for regime in REGIMES:

        regime_rows = [
            row
            for row in rows
            if row["regime"] == regime
        ]

        print(
            f"\n{regime}"
        )

        for feature in key_features:

            values = [
                float(
                    row[feature]
                )
                for row in regime_rows
            ]

            print(
                f"  "
                f"{feature:<38}"
                f"mean="
                f"{statistics.mean(values):.6f} "
                f"std="
                f"{statistics.stdev(values):.6f}"
            )

    print("=" * 112)


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