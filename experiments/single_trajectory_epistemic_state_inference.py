import csv
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path

from experiments.independent_aggregated_evidence_validation import (
    BASE_PROCESS_NOISE_STD,
    BASE_TRUE_A,
    EVENT_STEP,
    PROCESS_INPUT,
    STEPS,
    create_estimator,
)


REFERENCE_PATH = Path(
    "results/criterion_failure_decomposition.csv"
)

OUTPUT_PATH = Path(
    "results/single_trajectory_epistemic_state_inference.csv"
)


EVIDENCE_TIMES = [
    60,
    70,
    80,
    100,
]

RUNS_PER_CONDITION = 200

BASE_SEED = 41000


CONDITIONS = [
    {
        "class": "measurement_noise",
        "reference_condition":
            "measurement_noise_0.850",
        "name":
            "measurement_noise_0.850",
        "measurement_noise_std": 0.85,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "process_disturbance",
        "reference_condition":
            "process_disturbance_2.70",
        "name":
            "process_disturbance_2.70",
        "measurement_noise_std": 0.50,
        "process_disturbance": 2.70,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "reference_condition":
            "parameter_mismatch_delta_0.520",
        "name":
            "parameter_mismatch_delta_0.520",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.40,
        "changed_true_a": None,
    },
    {
        "class": "structural_change",
        "reference_condition":
            "structural_change_delta_0.060",
        "name":
            "structural_change_delta_0.060",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": 0.86,
    },
]


FEATURE_NAMES = [
    "mean_abs_innovation",
    "mean_nis",
    "event_mean_nis",
    "event_max_nis",
    "post_mean_nis",
    "post_vs_event_nis_ratio",
    "recent_mean_nis",
    "recent_mean_abs_innovation",
    "recent_nis_fraction_above_1",
    "mismatch_indicator",
    "parameter_shift_from_pre",
    "cumulative_abs_parameter_update",
    "recent_abs_parameter_update",
]


def load_reference_targets() -> dict:

    with REFERENCE_PATH.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        rows = list(
            csv.DictReader(file)
        )

    groups = defaultdict(list)

    for row in rows:

        groups[
            row["condition"]
        ].append(
            row
        )

    targets = {}

    for condition, group in groups.items():

        total = len(group)

        targets[condition] = {
            "p_fail_A":
                sum(
                    row["fail_A"]
                    == "True"
                    for row in group
                )
                / total,

            "p_fail_C":
                sum(
                    row["fail_C"]
                    == "True"
                    for row in group
                )
                / total,

            "p_fail_S":
                sum(
                    row["fail_S"]
                    == "True"
                    for row in group
                )
                / total,
        }

    return targets


REFERENCE_TARGETS = (
    load_reference_targets()
)


def mean_or_zero(
    values: list[float],
) -> float:

    if not values:
        return 0.0

    return statistics.mean(
        values
    )


def extract_prefix_features(
    trajectory: dict,
    *,
    evidence_time: int,
) -> dict:

    innovations = trajectory[
        "innovations"
    ][
        :evidence_time
    ]

    nis_values = trajectory[
        "nis_values"
    ][
        :evidence_time
    ]

    parameter_estimates = trajectory[
        "parameter_estimates"
    ][
        :evidence_time
    ]

    parameter_updates = trajectory[
        "parameter_updates"
    ][
        :evidence_time
    ]

    mismatch_indicators = trajectory[
        "mismatch_indicators"
    ][
        :evidence_time
    ]

    pre_start = 35
    pre_end = min(
        50,
        evidence_time,
    )

    event_start = 50
    event_end = min(
        60,
        evidence_time,
    )

    post_start = 60
    post_end = evidence_time

    pre_parameters = (
        parameter_estimates[
            pre_start:pre_end
        ]
    )

    event_nis = nis_values[
        event_start:event_end
    ]

    post_nis = nis_values[
        post_start:post_end
    ]

    recent_start = max(
        0,
        evidence_time - 10,
    )

    recent_nis = nis_values[
        recent_start:evidence_time
    ]

    recent_innovations = innovations[
        recent_start:evidence_time
    ]

    recent_updates = parameter_updates[
        recent_start:evidence_time
    ]

    mean_event_nis = (
        mean_or_zero(
            event_nis
        )
    )

    mean_post_nis = (
        mean_or_zero(
            post_nis
        )
    )

    if pre_parameters:

        pre_parameter_mean = (
            statistics.mean(
                pre_parameters
            )
        )

    else:

        pre_parameter_mean = (
            parameter_estimates[0]
        )

    current_parameter = (
        parameter_estimates[-1]
    )

    recent_fraction_above_1 = (
        sum(
            value > 1.0
            for value in recent_nis
        )
        / len(recent_nis)
        if recent_nis
        else 0.0
    )

    return {
        "mean_abs_innovation":
            mean_or_zero(
                [
                    abs(value)
                    for value in innovations
                ]
            ),

        "mean_nis":
            mean_or_zero(
                nis_values
            ),

        "event_mean_nis":
            mean_event_nis,

        "event_max_nis":
            (
                max(event_nis)
                if event_nis
                else 0.0
            ),

        "post_mean_nis":
            mean_post_nis,

        "post_vs_event_nis_ratio":
            (
                mean_post_nis
                / (
                    mean_event_nis
                    + 1e-12
                )
                if post_nis
                else 0.0
            ),

        "recent_mean_nis":
            mean_or_zero(
                recent_nis
            ),

        "recent_mean_abs_innovation":
            mean_or_zero(
                [
                    abs(value)
                    for value
                    in recent_innovations
                ]
            ),

        "recent_nis_fraction_above_1":
            recent_fraction_above_1,

        "mismatch_indicator":
            mismatch_indicators[-1],

        "parameter_shift_from_pre":
            (
                current_parameter
                - pre_parameter_mean
            ),

        "cumulative_abs_parameter_update":
            sum(
                abs(value)
                for value
                in parameter_updates
            ),

        "recent_abs_parameter_update":
            sum(
                abs(value)
                for value
                in recent_updates
            ),
    }


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
    mismatch_indicators = []
    parameter_estimates = []
    parameter_updates = []

    for step in range(
        STEPS
    ):

        if (
            condition[
                "changed_true_a"
            ]
            is not None
            and step == EVENT_STEP
        ):

            true_a = condition[
                "changed_true_a"
            ]

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

        mismatch_indicators.append(
            result.mismatch_indicator
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

        "mismatch_indicators":
            mismatch_indicators,

        "parameter_estimates":
            parameter_estimates,

        "parameter_updates":
            parameter_updates,
    }


def standardize(
    values: list[float],
) -> tuple[
    float,
    float,
]:

    mean_value = (
        statistics.mean(
            values
        )
    )

    if len(values) > 1:

        std_value = (
            statistics.stdev(
                values
            )
        )

    else:

        std_value = 0.0

    if std_value < 1e-12:
        std_value = 1.0

    return (
        mean_value,
        std_value,
    )


def fit_nearest_centroid_model(
    training_rows: list[dict],
) -> dict:

    scaling = {}

    for feature in FEATURE_NAMES:

        values = [
            row[feature]
            for row in training_rows
        ]

        scaling[feature] = (
            standardize(
                values
            )
        )

    class_groups = defaultdict(list)

    for row in training_rows:

        class_groups[
            row["condition"]
        ].append(
            row
        )

    centroids = {}

    for condition, group in (
        class_groups.items()
    ):

        centroid = {}

        for feature in FEATURE_NAMES:

            feature_mean = (
                statistics.mean(
                    row[feature]
                    for row in group
                )
            )

            scale_mean, scale_std = (
                scaling[
                    feature
                ]
            )

            centroid[feature] = (
                (
                    feature_mean
                    - scale_mean
                )
                / scale_std
            )

        centroids[
            condition
        ] = centroid

    return {
        "scaling":
            scaling,

        "centroids":
            centroids,
    }


def infer_epistemic_state(
    *,
    features: dict,
    model: dict,
) -> dict:

    distances = {}

    for condition, centroid in (
        model[
            "centroids"
        ].items()
    ):

        squared_distance = 0.0

        for feature in FEATURE_NAMES:

            mean_value, std_value = (
                model[
                    "scaling"
                ][
                    feature
                ]
            )

            standardized_value = (
                (
                    features[
                        feature
                    ]
                    - mean_value
                )
                / std_value
            )

            difference = (
                standardized_value
                - centroid[
                    feature
                ]
            )

            squared_distance += (
                difference ** 2
            )

        distances[
            condition
        ] = math.sqrt(
            squared_distance
        )

    similarities = {
        condition:
            math.exp(
                -distance
            )
        for condition, distance
        in distances.items()
    }

    total_similarity = sum(
        similarities.values()
    )

    weights = {
        condition:
            (
                similarity
                / total_similarity
            )
        for condition, similarity
        in similarities.items()
    }

    p_fail_a = sum(
        weight
        * REFERENCE_TARGETS[
            condition
        ][
            "p_fail_A"
        ]
        for condition, weight
        in weights.items()
    )

    p_fail_c = sum(
        weight
        * REFERENCE_TARGETS[
            condition
        ][
            "p_fail_C"
        ]
        for condition, weight
        in weights.items()
    )

    p_fail_s = sum(
        weight
        * REFERENCE_TARGETS[
            condition
        ][
            "p_fail_S"
        ]
        for condition, weight
        in weights.items()
    )

    predicted_condition = max(
        weights,
        key=weights.get,
    )

    return {
        "predicted_condition":
            predicted_condition,

        "p_fail_A":
            p_fail_a,

        "p_fail_C":
            p_fail_c,

        "p_fail_S":
            p_fail_s,
    }


def run_experiment() -> list[dict]:

    all_rows = []

    for condition_index, condition in enumerate(
        CONDITIONS
    ):

        target = REFERENCE_TARGETS[
            condition[
                "reference_condition"
            ]
        ]

        for run_index in range(
            RUNS_PER_CONDITION
        ):

            seed = (
                BASE_SEED
                + condition_index
                * RUNS_PER_CONDITION
                + run_index
            )

            trajectory = run_trajectory(
                condition=condition,
                seed=seed,
            )

            split = (
                "train"
                if run_index
                < RUNS_PER_CONDITION // 2
                else "test"
            )

            for evidence_time in (
                EVIDENCE_TIMES
            ):

                features = (
                    extract_prefix_features(
                        trajectory,
                        evidence_time=(
                            evidence_time
                        ),
                    )
                )

                all_rows.append(
                    {
                        "condition":
                            condition[
                                "reference_condition"
                            ],

                        "true_class":
                            condition[
                                "class"
                            ],

                        "run_index":
                            run_index,

                        "seed":
                            seed,

                        "split":
                            split,

                        "evidence_time":
                            evidence_time,

                        "target_p_fail_A":
                            target[
                                "p_fail_A"
                            ],

                        "target_p_fail_C":
                            target[
                                "p_fail_C"
                            ],

                        "target_p_fail_S":
                            target[
                                "p_fail_S"
                            ],

                        **features,
                    }
                )

    output_rows = []

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        training_rows = [
            row
            for row in all_rows
            if (
                row["split"]
                == "train"
                and
                row[
                    "evidence_time"
                ]
                == evidence_time
            )
        ]

        test_rows = [
            row
            for row in all_rows
            if (
                row["split"]
                == "test"
                and
                row[
                    "evidence_time"
                ]
                == evidence_time
            )
        ]

        model = (
            fit_nearest_centroid_model(
                training_rows
            )
        )

        for row in test_rows:

            inference = (
                infer_epistemic_state(
                    features=row,
                    model=model,
                )
            )

            abs_error_a = abs(
                inference[
                    "p_fail_A"
                ]
                - row[
                    "target_p_fail_A"
                ]
            )

            abs_error_c = abs(
                inference[
                    "p_fail_C"
                ]
                - row[
                    "target_p_fail_C"
                ]
            )

            abs_error_s = abs(
                inference[
                    "p_fail_S"
                ]
                - row[
                    "target_p_fail_S"
                ]
            )

            marginal_mae = (
                statistics.mean(
                    [
                        abs_error_a,
                        abs_error_c,
                        abs_error_s,
                    ]
                )
            )

            output_rows.append(
                {
                    "condition":
                        row[
                            "condition"
                        ],

                    "true_class":
                        row[
                            "true_class"
                        ],

                    "run_index":
                        row[
                            "run_index"
                        ],

                    "seed":
                        row[
                            "seed"
                        ],

                    "evidence_time":
                        evidence_time,

                    "predicted_condition":
                        inference[
                            "predicted_condition"
                        ],

                    "condition_correct":
                        (
                            inference[
                                "predicted_condition"
                            ]
                            == row[
                                "condition"
                            ]
                        ),

                    "target_p_fail_A":
                        row[
                            "target_p_fail_A"
                        ],

                    "target_p_fail_C":
                        row[
                            "target_p_fail_C"
                        ],

                    "target_p_fail_S":
                        row[
                            "target_p_fail_S"
                        ],

                    "estimated_p_fail_A":
                        inference[
                            "p_fail_A"
                        ],

                    "estimated_p_fail_C":
                        inference[
                            "p_fail_C"
                        ],

                    "estimated_p_fail_S":
                        inference[
                            "p_fail_S"
                        ],

                    "marginal_mae":
                        marginal_mae,
                }
            )

    return output_rows


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

    print("=" * 118)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "SINGLE-TRAJECTORY EPISTEMIC-STATE INFERENCE"
    )

    print("=" * 118)

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        group = [
            row
            for row in rows
            if int(
                row[
                    "evidence_time"
                ]
            )
            == evidence_time
        ]

        condition_accuracy = (
            sum(
                row[
                    "condition_correct"
                ]
                for row in group
            )
            / len(group)
        )

        mean_mae = (
            statistics.mean(
                float(
                    row[
                        "marginal_mae"
                    ]
                )
                for row in group
            )
        )

        print(
            f"t={evidence_time:<3} "
            f"condition_accuracy="
            f"{condition_accuracy:.3%} "
            f"epistemic_MAE="
            f"{mean_mae:.4f}"
        )

    print("=" * 118)


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