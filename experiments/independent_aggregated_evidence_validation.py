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

LEARNING_RATE = 0.08
NORMALIZATION_EPSILON = 1.0

INNOVATION_MEMORY = 0.50
MIN_INFLATION_STRENGTH = 0.05
MAX_INFLATION_STRENGTH = 0.20
TRANSITION_SCALE = 0.25

RUNS_PER_CONDITION = 100

CONFIDENCE_THRESHOLD = 0.30

BATCH_SIZE = 50
BATCH_REPLICATES = 500

RANDOM_SEED = 30030

OUTPUT_PATH = Path(
    "results/independent_aggregated_evidence_validation.csv"
)


VALIDATION_CONDITIONS = [
    {
        "class": "measurement_noise",
        "name": "measurement_noise_0.875",
        "measurement_noise_std": 0.875,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "measurement_noise",
        "name": "measurement_noise_0.975",
        "measurement_noise_std": 0.975,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "process_disturbance",
        "name": "process_disturbance_2.60",
        "measurement_noise_std": 0.50,
        "process_disturbance": 2.60,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "process_disturbance",
        "name": "process_disturbance_2.90",
        "measurement_noise_std": 0.50,
        "process_disturbance": 2.90,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "name": "parameter_mismatch_0.435",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.435,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "name": "parameter_mismatch_0.395",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.395,
        "changed_true_a": None,
    },
    {
        "class": "structural_change",
        "name": "structural_change_0.875",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": 0.875,
    },
    {
        "class": "structural_change",
        "name": "structural_change_0.855",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": 0.855,
    },
]


AGGREGATE_THRESHOLDS = {
    "measurement_noise": 0.44,
    "process_disturbance": 0.59,
    "parameter_mismatch": 0.50,
    "structural_change": 0.51,
}


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

    mean_value = (
        sum(values)
        / len(values)
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


def run_trajectory(
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


def extract_features(
    trajectory: dict,
) -> tuple[
    dict,
    dict,
    dict,
]:

    innovations = trajectory[
        "innovations"
    ]

    nis_values = trajectory[
        "nis_values"
    ]

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

    global_features = {
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

    pre_nis = nis_values[35:50]
    event_nis = nis_values[50:60]
    post_nis = nis_values[60:80]

    pre_innovations = (
        innovations[35:50]
    )

    event_innovations = (
        innovations[50:60]
    )

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

    temporal_features = {
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
            max(
                event_nis
            ),

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

    pre_parameter_mean = (
        sum(
            parameter_estimates[35:50]
        )
        / 15
    )

    post_parameter_mean = (
        sum(
            parameter_estimates[60:80]
        )
        / 20
    )

    adaptation_features = {
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

    return (
        global_features,
        temporal_features,
        adaptation_features,
    )


def frozen_trajectory_vote(
    *,
    cause: str,
    classification_margin: float,
    recovery_ratio_nis: float,
    parameter_shift_post_vs_pre: float,
    post_cumulative_abs_parameter_update: float,
) -> bool:

    if cause == "measurement_noise":

        return (
            classification_margin
            >= 0.5162128944351736
            and
            post_cumulative_abs_parameter_update
            >= 0.09534309010684958
        )

    if cause == "process_disturbance":

        return (
            recovery_ratio_nis
            <= 0.34013237768129045
        )

    if cause == "parameter_mismatch":

        return (
            classification_margin
            >= 0.5733833425128738
        )

    if cause == "structural_change":

        return (
            parameter_shift_post_vs_pre
            <= -0.049260128858973906
        )

    raise ValueError(
        cause
    )


def generate_condition_population(
    condition: dict,
) -> list[dict]:

    records = []

    for seed_offset in range(
        RUNS_PER_CONDITION
    ):

        seed = (
            4000
            + seed_offset
        )

        trajectory = run_trajectory(
            condition=condition,
            seed=seed,
        )

        (
            global_features,
            temporal_features,
            adaptation_features,
        ) = extract_features(
            trajectory
        )

        classification = classify_row(
            regime=condition["class"],
            global_row=global_features,
            temporal_row=temporal_features,
            adaptation_row=adaptation_features,
        )

        vote = frozen_trajectory_vote(
            cause=condition["class"],
            classification_margin=float(
                classification[
                    "classification_margin"
                ]
            ),
            recovery_ratio_nis=(
                temporal_features[
                    "recovery_ratio_nis"
                ]
            ),
            parameter_shift_post_vs_pre=(
                adaptation_features[
                    "parameter_shift_post_vs_pre"
                ]
            ),
            post_cumulative_abs_parameter_update=(
                adaptation_features[
                    "post_cumulative_abs_parameter_update"
                ]
            ),
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

                "trajectory_evidence_vote":
                    vote,
            }
        )

    return records


def operating_point_label(
    records: list[dict],
) -> bool:

    hard_accuracy = (
        sum(
            record[
                "classification_correct"
            ]
            for record in records
        )
        / len(records)
    )

    accepted = [
        record
        for record in records
        if float(
            record[
                "classification_margin"
            ]
        )
        >= CONFIDENCE_THRESHOLD
    ]

    coverage = (
        len(accepted)
        / len(records)
    )

    if accepted:

        selective_accuracy = (
            sum(
                record[
                    "classification_correct"
                ]
                for record in accepted
            )
            / len(accepted)
        )

    else:

        selective_accuracy = 0.0

    label = (
        hard_accuracy >= 0.90
        and
        coverage >= 0.80
        and
        selective_accuracy >= 0.95
    )

    return (
        label,
        hard_accuracy,
        coverage,
        selective_accuracy,
    )


def validate_condition(
    *,
    condition: dict,
    rng: random.Random,
) -> list[dict]:

    population = (
        generate_condition_population(
            condition
        )
    )

    (
        label,
        hard_accuracy,
        coverage,
        selective_accuracy,
    ) = operating_point_label(
        population
    )

    aggregate_threshold = (
        AGGREGATE_THRESHOLDS[
            condition["class"]
        ]
    )

    rows = []

    for replicate in range(
        BATCH_REPLICATES
    ):

        batch = rng.sample(
            population,
            BATCH_SIZE,
        )

        vote_fraction = (
            sum(
                1.0
                if record[
                    "trajectory_evidence_vote"
                ]
                else 0.0
                for record in batch
            )
            / BATCH_SIZE
        )

        prediction = (
            vote_fraction
            >= aggregate_threshold
        )

        rows.append(
            {
                "condition":
                    condition["name"],

                "true_class":
                    condition["class"],

                "replicate":
                    replicate,

                "batch_size":
                    BATCH_SIZE,

                "aggregate_vote_fraction":
                    vote_fraction,

                "aggregate_threshold":
                    aggregate_threshold,

                "predicted_evidence_sufficient":
                    prediction,

                "operating_point_evidence_sufficient":
                    label,

                "prediction_correct":
                    prediction
                    == label,

                "operating_point_hard_accuracy":
                    hard_accuracy,

                "operating_point_coverage":
                    coverage,

                "operating_point_selective_accuracy":
                    selective_accuracy,
            }
        )

    return rows


def run_experiment() -> list[dict]:

    rng = random.Random(
        RANDOM_SEED
    )

    rows = []

    for condition in (
        VALIDATION_CONDITIONS
    ):

        rows.extend(
            validate_condition(
                condition=condition,
                rng=rng,
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


def print_summary(
    rows: list[dict],
) -> None:

    print("=" * 120)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "INDEPENDENT AGGREGATED EVIDENCE VALIDATION"
    )

    print("=" * 120)

    overall_correct = sum(
        row[
            "prediction_correct"
        ]
        for row in rows
    )

    print(
        f"Overall aggregate accuracy: "
        f"{overall_correct}/{len(rows)} "
        f"({overall_correct / len(rows):.3%})"
    )

    print()

    for cause in [
        "measurement_noise",
        "process_disturbance",
        "parameter_mismatch",
        "structural_change",
    ]:

        cause_rows = [
            row
            for row in rows
            if row[
                "true_class"
            ]
            == cause
        ]

        correct = sum(
            row[
                "prediction_correct"
            ]
            for row in cause_rows
        )

        print(
            f"{cause:<24}"
            f"accuracy="
            f"{correct / len(cause_rows):.3%}"
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