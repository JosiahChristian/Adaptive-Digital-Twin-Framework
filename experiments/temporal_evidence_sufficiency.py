import csv
import random
import statistics
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

LEARNING_RATE = 0.08
NORMALIZATION_EPSILON = 1.0

INNOVATION_MEMORY = 0.50
MIN_INFLATION_STRENGTH = 0.05
MAX_INFLATION_STRENGTH = 0.20
TRANSITION_SCALE = 0.25

RUNS_PER_CONDITION = 60

CONFIDENCE_THRESHOLD = 0.30

OUTPUT_PATH = Path(
    "results/temporal_evidence_sufficiency.csv"
)


VALIDATION_CONDITIONS = [
    {
        "class": "measurement_noise",
        "name": "measurement_noise_0.90",
        "measurement_noise_std": 0.90,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "measurement_noise",
        "name": "measurement_noise_1.10",
        "measurement_noise_std": 1.10,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "process_disturbance",
        "name": "process_disturbance_2.25",
        "measurement_noise_std": 0.50,
        "process_disturbance": 2.25,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "process_disturbance",
        "name": "process_disturbance_2.75",
        "measurement_noise_std": 0.50,
        "process_disturbance": 2.75,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "name": "parameter_mismatch_0.375",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.375,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "name": "parameter_mismatch_0.325",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.325,
        "changed_true_a": None,
    },
    {
        "class": "structural_change",
        "name": "structural_change_0.865",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": 0.865,
    },
    {
        "class": "structural_change",
        "name": "structural_change_0.845",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": 0.845,
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


def mean_window(
    values: list[float],
    start: int,
    stop: int,
) -> float:

    return statistics.mean(
        values[start:stop]
    )


def run_raw_trajectory(
    *,
    condition: dict,
    seed: int,
) -> dict:

    random.seed(
        seed
    )

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

    return {
        "innovations":
            innovations,
        "nis_values":
            nis_values,
        "parameter_estimates":
            parameter_estimates,
        "parameter_updates":
            parameter_updates,
    }


def extract_global_features(
    trajectory: dict,
) -> dict:

    innovations = trajectory[
        "innovations"
    ]

    nis_values = trajectory[
        "nis_values"
    ]

    return {
        "mean_absolute_innovation":
            statistics.mean(
                abs(value)
                for value in innovations
            ),

        "mean_nis":
            statistics.mean(
                nis_values
            ),

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
    trajectory: dict,
) -> dict:

    innovations = trajectory[
        "innovations"
    ]

    nis_values = trajectory[
        "nis_values"
    ]

    pre_nis = nis_values[35:50]
    event_nis = nis_values[50:60]
    post_nis = nis_values[60:80]

    pre_innovation = (
        innovations[35:50]
    )

    event_innovation = (
        innovations[50:60]
    )

    post_innovation = (
        innovations[60:80]
    )

    mean_pre_nis = (
        statistics.mean(
            pre_nis
        )
    )

    mean_event_nis = (
        statistics.mean(
            event_nis
        )
    )

    mean_post_nis = (
        statistics.mean(
            post_nis
        )
    )

    return {
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
                    + 1e-12
                )
            ),

        "event_max_nis":
            max(
                event_nis
            ),

        "post_longest_nis_run_above_1":
            longest_threshold_run(
                post_nis,
                threshold=1.0,
            ),

        "delta_event_vs_pre_autocorrelation":
            (
                lag_one_autocorrelation(
                    event_innovation
                )
                -
                lag_one_autocorrelation(
                    pre_innovation
                )
            ),

        "delta_post_vs_pre_autocorrelation":
            (
                lag_one_autocorrelation(
                    post_innovation
                )
                -
                lag_one_autocorrelation(
                    pre_innovation
                )
            ),
    }


def extract_adaptation_features(
    trajectory: dict,
) -> dict:

    parameter_estimates = (
        trajectory[
            "parameter_estimates"
        ]
    )

    parameter_updates = (
        trajectory[
            "parameter_updates"
        ]
    )

    pre_parameter_mean = (
        mean_window(
            parameter_estimates,
            35,
            50,
        )
    )

    post_parameter_mean = (
        mean_window(
            parameter_estimates,
            60,
            80,
        )
    )

    return {
        "parameter_shift_post_vs_pre":
            (
                post_parameter_mean
                - pre_parameter_mean
            ),

        "post_cumulative_abs_parameter_update":
            sum(
                abs(value)
                for value
                in parameter_updates[
                    60:80
                ]
            ),
    }


def classify_trajectory(
    *,
    condition: dict,
    global_features: dict,
    temporal_features: dict,
    adaptation_features: dict,
) -> dict:

    return classify_row(
        regime=condition["class"],
        global_row=global_features,
        temporal_row=temporal_features,
        adaptation_row=adaptation_features,
    )


def operating_point_label(
    classifications: list[dict],
) -> bool:

    hard_accuracy = (
        sum(
            item["correct"]
            for item in classifications
        )
        / len(classifications)
    )

    accepted = [
        item
        for item in classifications
        if float(
            item[
                "classification_margin"
            ]
        )
        >= CONFIDENCE_THRESHOLD
    ]

    coverage = (
        len(accepted)
        / len(classifications)
    )

    if accepted:

        selective_accuracy = (
            sum(
                item["correct"]
                for item in accepted
            )
            / len(accepted)
        )

    else:

        selective_accuracy = 0.0

    return (
        hard_accuracy >= 0.90
        and
        coverage >= 0.80
        and
        selective_accuracy >= 0.95
    )


def generate_condition_rows(
    condition: dict,
) -> list[dict]:

    records = []

    classifications = []

    for seed_offset in range(
        RUNS_PER_CONDITION
    ):

        seed = (
            1000
            + seed_offset
        )

        trajectory = (
            run_raw_trajectory(
                condition=condition,
                seed=seed,
            )
        )

        global_features = (
            extract_global_features(
                trajectory
            )
        )

        temporal_features = (
            extract_temporal_features(
                trajectory
            )
        )

        adaptation_features = (
            extract_adaptation_features(
                trajectory
            )
        )

        classification = (
            classify_trajectory(
                condition=condition,
                global_features=(
                    global_features
                ),
                temporal_features=(
                    temporal_features
                ),
                adaptation_features=(
                    adaptation_features
                ),
            )
        )

        scores = [
            float(
                classification[
                    "measurement_noise_score"
                ]
            ),
            float(
                classification[
                    "process_disturbance_score"
                ]
            ),
            float(
                classification[
                    "parameter_mismatch_score"
                ]
            ),
            float(
                classification[
                    "structural_change_score"
                ]
            ),
        ]

        classifications.append(
            classification
        )

        records.append(
            {
                "condition":
                    condition["name"],

                "true_class":
                    condition["class"],

                "seed":
                    seed,

                "classification_correct":
                    classification[
                        "correct"
                    ],

                "classification_margin":
                    float(
                        classification[
                            "classification_margin"
                        ]
                    ),

                "score_spread":
                    (
                        max(scores)
                        - min(scores)
                    ),

                **temporal_features,
                **adaptation_features,
            }
        )

    label = operating_point_label(
        classifications
    )

    for record in records:

        record[
            "evidence_sufficient"
        ] = label

    return records


def run_experiment() -> list[dict]:

    rows = []

    for condition in (
        VALIDATION_CONDITIONS
    ):

        rows.extend(
            generate_condition_rows(
                condition
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
        writer.writerows(
            rows
        )


def standardized_separation(
    sufficient: list[float],
    insufficient: list[float],
) -> float:

    difference = abs(
        statistics.mean(
            sufficient
        )
        -
        statistics.mean(
            insufficient
        )
    )

    pooled_scale = (
        (
            statistics.variance(
                sufficient
            )
            +
            statistics.variance(
                insufficient
            )
        )
        / 2.0
    ) ** 0.5

    if pooled_scale == 0.0:
        return 0.0

    return (
        difference
        / pooled_scale
    )


def print_summary(
    rows: list[dict],
) -> None:

    features = [
        "classification_margin",
        "score_spread",
        "delta_event_vs_pre_nis",
        "delta_post_vs_pre_nis",
        "recovery_ratio_nis",
        "event_max_nis",
        "post_longest_nis_run_above_1",
        "delta_event_vs_pre_autocorrelation",
        "delta_post_vs_pre_autocorrelation",
        "parameter_shift_post_vs_pre",
        "post_cumulative_abs_parameter_update",
    ]

    print("=" * 120)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "TEMPORAL EVIDENCE SUFFICIENCY"
    )

    print("=" * 120)

    print(
        "feature                               "
        "sufficient_mean  insufficient_mean  "
        "separation"
    )

    for feature in features:

        sufficient = [
            float(
                row[feature]
            )
            for row in rows
            if row[
                "evidence_sufficient"
            ]
        ]

        insufficient = [
            float(
                row[feature]
            )
            for row in rows
            if not row[
                "evidence_sufficient"
            ]
        ]

        separation = (
            standardized_separation(
                sufficient,
                insufficient,
            )
        )

        print(
            f"{feature:<38}"
            f"{statistics.mean(sufficient):<17.6f}"
            f"{statistics.mean(insufficient):<19.6f}"
            f"{separation:.4f}"
        )

    print("=" * 120)


def main() -> None:

    rows = run_experiment()

    save_results(
        rows
    )

    print_summary(
        rows
    )

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()