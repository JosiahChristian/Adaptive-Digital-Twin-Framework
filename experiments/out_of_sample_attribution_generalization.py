import csv
import random
from pathlib import Path

from experiments.mismatch_classification import (
    classify_row,
)

from simulation.normalized_innovation_estimator import (
    NormalizedInnovationAdaptiveEstimator,
)


BASE_TRUE_A = 0.92

PROCESS_INPUT = 1.0
STEPS = 100
EVENT_STEP = 50

BASE_PROCESS_NOISE_STD = 0.05
BASE_MEASUREMENT_NOISE_STD = 0.50
BASE_INITIAL_PARAMETER_ESTIMATE = 0.50

LEARNING_RATE = 0.08
NORMALIZATION_EPSILON = 1.0

INNOVATION_MEMORY = 0.50
MIN_INFLATION_STRENGTH = 0.05
MAX_INFLATION_STRENGTH = 0.20
TRANSITION_SCALE = 0.25

RUNS_PER_CONDITION = 50

CONFIDENCE_THRESHOLD = 0.30

OUTPUT_PATH = Path(
    "results/out_of_sample_attribution_generalization.csv"
)


CONDITIONS = [
    {
        "class": "measurement_noise",
        "name": "measurement_noise_0.75",
        "measurement_noise_std": 0.75,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "measurement_noise",
        "name": "measurement_noise_1.25",
        "measurement_noise_std": 1.25,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "process_disturbance",
        "name": "process_disturbance_2.0",
        "measurement_noise_std": 0.50,
        "process_disturbance": 2.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "process_disturbance",
        "name": "process_disturbance_4.0",
        "measurement_noise_std": 0.50,
        "process_disturbance": 4.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "name": "parameter_mismatch_0.30",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.30,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "name": "parameter_mismatch_0.10",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.10,
        "changed_true_a": None,
    },
    {
        "class": "structural_change",
        "name": "structural_change_0.85",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": 0.85,
    },
    {
        "class": "structural_change",
        "name": "structural_change_0.75",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": 0.75,
    },
]


def create_estimator(
    *,
    initial_parameter_estimate: float,
    measurement_noise_std: float,
):

    return NormalizedInnovationAdaptiveEstimator(
        initial_parameter_estimate=(
            initial_parameter_estimate
        ),
        learning_rate=LEARNING_RATE,
        normalization_epsilon=(
            NORMALIZATION_EPSILON
        ),
        base_process_noise_variance=(
            BASE_PROCESS_NOISE_STD ** 2
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

    mean_value = sum(values) / len(values)

    denominator = sum(
        (value - mean_value) ** 2
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

    return numerator / denominator


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


def extract_global_features(
    innovations: list[float],
    nis_values: list[float],
) -> dict:

    return {
        "mean_absolute_innovation":
            sum(
                abs(value)
                for value in innovations
            )
            / len(innovations),

        "mean_nis":
            sum(nis_values)
            / len(nis_values),

        "longest_nis_run_above_1":
            longest_threshold_run(
                nis_values,
                threshold=1.0,
            ),

        "innovation_lag1_autocorrelation":
            lag_one_autocorrelation(
                innovations
            ),
    }


def extract_temporal_features(
    innovations: list[float],
    nis_values: list[float],
) -> dict:

    pre_indices = range(35, 50)
    event_indices = range(50, 60)
    post_indices = range(60, 80)

    pre_nis = [
        nis_values[index]
        for index in pre_indices
    ]

    event_nis = [
        nis_values[index]
        for index in event_indices
    ]

    post_nis = [
        nis_values[index]
        for index in post_indices
    ]

    pre_innovations = [
        innovations[index]
        for index in pre_indices
    ]

    event_innovations = [
        innovations[index]
        for index in event_indices
    ]

    mean_pre_nis = (
        sum(pre_nis)
        / len(pre_nis)
    )

    mean_event_nis = (
        sum(event_nis)
        / len(event_nis)
    )

    mean_post_nis = (
        sum(post_nis)
        / len(post_nis)
    )

    return {
        "delta_event_vs_pre_nis":
            (
                mean_event_nis
                - mean_pre_nis
            ),

        "recovery_ratio_nis":
            (
                mean_post_nis
                / (
                    mean_event_nis
                    + 1e-12
                )
            ),

        "event_max_nis":
            max(event_nis),

        "delta_event_vs_pre_autocorrelation":
            (
                lag_one_autocorrelation(
                    event_innovations
                )
                -
                lag_one_autocorrelation(
                    pre_innovations
                )
            ),
    }


def extract_adaptation_features(
    parameter_estimates: list[float],
    parameter_updates: list[float],
) -> dict:

    pre_indices = range(35, 50)
    post_indices = range(60, 80)

    pre_parameter_mean = (
        sum(
            parameter_estimates[index]
            for index in pre_indices
        )
        / len(pre_indices)
    )

    post_parameter_mean = (
        sum(
            parameter_estimates[index]
            for index in post_indices
        )
        / len(post_indices)
    )

    post_parameter_activity = sum(
        abs(
            parameter_updates[index]
        )
        for index in post_indices
    )

    return {
        "parameter_shift_post_vs_pre":
            (
                post_parameter_mean
                - pre_parameter_mean
            ),

        "post_cumulative_abs_parameter_update":
            post_parameter_activity,
    }


def run_single_trial(
    *,
    condition: dict,
    seed: int,
) -> dict:

    random.seed(seed)

    estimator = create_estimator(
        initial_parameter_estimate=(
            condition[
                "initial_parameter_estimate"
            ]
        ),
        measurement_noise_std=(
            condition[
                "measurement_noise_std"
            ]
        ),
    )

    true_state = 0.0
    true_a = BASE_TRUE_A

    innovations = []
    nis_values = []
    parameter_estimates = []
    parameter_updates = []

    for step in range(STEPS):

        if (
            condition["changed_true_a"]
            is not None
            and step == EVENT_STEP
        ):
            true_a = (
                condition[
                    "changed_true_a"
                ]
            )

        true_state = (
            true_a
            * true_state
            + PROCESS_INPUT
            + random.gauss(
                0.0,
                BASE_PROCESS_NOISE_STD,
            )
        )

        if (
            condition[
                "process_disturbance"
            ]
            != 0.0
            and step == EVENT_STEP
        ):
            true_state += (
                condition[
                    "process_disturbance"
                ]
            )

        measurement = (
            true_state
            + random.gauss(
                0.0,
                condition[
                    "measurement_noise_std"
                ],
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

        parameter_estimates.append(
            result.parameter_estimate
        )

        parameter_updates.append(
            result.parameter_update
        )

    global_features = (
        extract_global_features(
            innovations,
            nis_values,
        )
    )

    temporal_features = (
        extract_temporal_features(
            innovations,
            nis_values,
        )
    )

    adaptation_features = (
        extract_adaptation_features(
            parameter_estimates,
            parameter_updates,
        )
    )

    global_row = {
        "mean_absolute_innovation":
            global_features[
                "mean_absolute_innovation"
            ],

        "mean_nis":
            global_features[
                "mean_nis"
            ],

        "longest_nis_run_above_1":
            global_features[
                "longest_nis_run_above_1"
            ],

        "innovation_lag1_autocorrelation":
            global_features[
                "innovation_lag1_autocorrelation"
            ],
    }

    temporal_row = {
        "delta_event_vs_pre_nis":
            temporal_features[
                "delta_event_vs_pre_nis"
            ],

        "recovery_ratio_nis":
            temporal_features[
                "recovery_ratio_nis"
            ],

        "event_max_nis":
            temporal_features[
                "event_max_nis"
            ],

        "delta_event_vs_pre_autocorrelation":
            temporal_features[
                "delta_event_vs_pre_autocorrelation"
            ],
    }

    adaptation_row = {
        "parameter_shift_post_vs_pre":
            adaptation_features[
                "parameter_shift_post_vs_pre"
            ],

        "post_cumulative_abs_parameter_update":
            adaptation_features[
                "post_cumulative_abs_parameter_update"
            ],
    }

    classification = classify_row(
        regime=condition["class"],
        global_row=global_row,
        temporal_row=temporal_row,
        adaptation_row=adaptation_row,
    )

    margin = float(
        classification[
            "classification_margin"
        ]
    )

    accepted = (
        margin
        >= CONFIDENCE_THRESHOLD
    )

    return {
        "condition":
            condition["name"],

        "true_class":
            condition["class"],

        "seed":
            seed,

        "predicted_class":
            classification[
                "predicted_class"
            ],

        "classification_margin":
            margin,

        "correct":
            classification[
                "correct"
            ],

        "accepted":
            accepted,

        "accepted_correct":
            (
                accepted
                and classification[
                    "correct"
                ]
            ),

        "measurement_noise_score":
            classification[
                "measurement_noise_score"
            ],

        "process_disturbance_score":
            classification[
                "process_disturbance_score"
            ],

        "parameter_mismatch_score":
            classification[
                "parameter_mismatch_score"
            ],

        "structural_change_score":
            classification[
                "structural_change_score"
            ],
    }


def run_experiment() -> list[dict]:

    rows = []

    for condition in CONDITIONS:

        for seed in range(
            RUNS_PER_CONDITION
        ):

            rows.append(
                run_single_trial(
                    condition=condition,
                    seed=seed,
                )
            )

    return rows


def save_results(
    rows: list[dict],
) -> None:

    OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(rows)


def print_summary(
    rows: list[dict],
) -> None:

    total = len(rows)

    correct = sum(
        row["correct"]
        for row in rows
    )

    accepted = [
        row
        for row in rows
        if row["accepted"]
    ]

    accepted_correct = sum(
        row["accepted_correct"]
        for row in accepted
    )

    print("=" * 108)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "OUT-OF-SAMPLE ATTRIBUTION GENERALIZATION"
    )

    print("=" * 108)

    print(
        f"Hard accuracy: "
        f"{correct}/{total} "
        f"({correct / total:.3%})"
    )

    print(
        f"Selective coverage @ 0.30: "
        f"{len(accepted)}/{total} "
        f"({len(accepted) / total:.3%})"
    )

    print(
        f"Selective accuracy @ 0.30: "
        f"{accepted_correct}/"
        f"{len(accepted)} "
        f"({accepted_correct / len(accepted):.3%})"
    )

    print()

    for condition in CONDITIONS:

        name = condition["name"]

        condition_rows = [
            row
            for row in rows
            if row["condition"]
            == name
        ]

        condition_correct = sum(
            row["correct"]
            for row in condition_rows
        )

        condition_accepted = [
            row
            for row in condition_rows
            if row["accepted"]
        ]

        condition_accepted_correct = sum(
            row["accepted_correct"]
            for row in condition_accepted
        )

        print(
            f"{name:<32}"
            f"hard="
            f"{condition_correct / len(condition_rows):.3%} "
            f"coverage="
            f"{len(condition_accepted) / len(condition_rows):.3%} "
            f"accepted_acc="
            f"{condition_accepted_correct / len(condition_accepted):.3%}"
            if condition_accepted
            else
            f"{name:<32}"
            f"hard="
            f"{condition_correct / len(condition_rows):.3%} "
            f"coverage=0.000% "
            f"accepted_acc=N/A"
        )

    print("=" * 108)


def main() -> None:

    rows = run_experiment()

    save_results(rows)

    print_summary(rows)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()