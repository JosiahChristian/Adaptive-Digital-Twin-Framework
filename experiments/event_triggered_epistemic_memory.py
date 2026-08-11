import csv
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path

from experiments.single_trajectory_epistemic_state_inference import (
    BASE_PROCESS_NOISE_STD,
    BASE_TRUE_A,
    CONDITIONS,
    EVENT_STEP,
    PROCESS_INPUT,
    REFERENCE_TARGETS,
    RUNS_PER_CONDITION,
    STEPS,
    create_estimator,
)


OUTPUT_PATH = Path(
    "results/event_triggered_epistemic_memory.csv"
)

EVIDENCE_TIMES = [
    60,
    70,
    80,
    100,
]

BASE_SEED = 43000

TRIGGER_SEARCH_START = 30

EVENT_MEMORY_TAU = 8.0


FEATURE_NAMES = [
    "weighted_abs_innovation",
    "weighted_nis",
    "weighted_nis_above_1",
    "weighted_mismatch_indicator",
    "weighted_parameter_estimate",
    "weighted_abs_parameter_update",
    "current_parameter_estimate",
    "current_mismatch_indicator",
]


def mean_or_zero(
    values: list[float],
) -> float:

    if not values:
        return 0.0

    return statistics.mean(
        values
    )


def weighted_mean(
    values: list[float],
    weights: list[float],
) -> float:

    if not values:
        return 0.0

    total_weight = sum(
        weights
    )

    if total_weight <= 0.0:
        return mean_or_zero(
            values
        )

    return sum(
        value * weight
        for value, weight
        in zip(
            values,
            weights,
        )
    ) / total_weight


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
    excess_nis_values = []
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

        excess_nis_values.append(
            result.excess_normalized_innovation
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

        "excess_nis_values":
            excess_nis_values,

        "mismatch_indicators":
            mismatch_indicators,

        "parameter_estimates":
            parameter_estimates,

        "parameter_updates":
            parameter_updates,
    }


def robust_standardize(
    values: list[float],
) -> list[float]:

    if not values:
        return []

    median_value = statistics.median(
        values
    )

    deviations = [
        abs(
            value - median_value
        )
        for value in values
    ]

    mad = statistics.median(
        deviations
    )

    scale = (
        1.4826
        * mad
    )

    if scale < 1e-12:

        scale = (
            statistics.stdev(
                values
            )
            if len(values) > 1
            else 1.0
        )

    if scale < 1e-12:
        scale = 1.0

    return [
        (
            value - median_value
        )
        / scale
        for value in values
    ]


def detect_event_time(
    trajectory: dict,
    *,
    evidence_time: int,
) -> tuple[
    int,
    float,
]:

    nis_values = trajectory[
        "nis_values"
    ][
        :evidence_time
    ]

    mismatch_values = trajectory[
        "mismatch_indicators"
    ][
        :evidence_time
    ]

    update_values = [
        abs(value)
        for value in trajectory[
            "parameter_updates"
        ][
            :evidence_time
        ]
    ]

    innovation_values = [
        abs(value)
        for value in trajectory[
            "innovations"
        ][
            :evidence_time
        ]
    ]

    baseline_end = min(
        EVENT_STEP,
        evidence_time,
    )

    baseline_start = max(
        0,
        baseline_end - 20,
    )

    baseline_nis = nis_values[
        baseline_start:baseline_end
    ]

    baseline_mismatch = mismatch_values[
        baseline_start:baseline_end
    ]

    baseline_updates = update_values[
        baseline_start:baseline_end
    ]

    baseline_innovations = (
        innovation_values[
            baseline_start:baseline_end
        ]
    )

    nis_reference = (
        statistics.median(
            baseline_nis
        )
        if baseline_nis
        else 0.0
    )

    mismatch_reference = (
        statistics.median(
            baseline_mismatch
        )
        if baseline_mismatch
        else 0.0
    )

    update_reference = (
        statistics.median(
            baseline_updates
        )
        if baseline_updates
        else 0.0
    )

    innovation_reference = (
        statistics.median(
            baseline_innovations
        )
        if baseline_innovations
        else 0.0
    )

    raw_scores = []

    candidate_steps = list(
        range(
            TRIGGER_SEARCH_START,
            evidence_time,
        )
    )

    for step in candidate_steps:

        nis_component = max(
            0.0,
            nis_values[step]
            - nis_reference,
        )

        mismatch_component = max(
            0.0,
            mismatch_values[step]
            - mismatch_reference,
        )

        update_component = max(
            0.0,
            update_values[step]
            - update_reference,
        )

        innovation_component = max(
            0.0,
            innovation_values[step]
            - innovation_reference,
        )

        raw_score = (
            nis_component
            + mismatch_component
            + update_component
            + innovation_component
        )

        raw_scores.append(
            raw_score
        )

    standardized_scores = (
        robust_standardize(
            raw_scores
        )
    )

    if not standardized_scores:

        return (
            TRIGGER_SEARCH_START,
            0.0,
        )

    best_index = max(
        range(
            len(
                standardized_scores
            )
        ),
        key=lambda index:
            standardized_scores[
                index
            ],
    )

    detected_step = (
        candidate_steps[
            best_index
        ]
    )

    detected_score = (
        standardized_scores[
            best_index
        ]
    )

    return (
        detected_step,
        detected_score,
    )


def temporal_weights(
    *,
    evidence_time: int,
    scheme: str,
    detected_event_time: int | None,
) -> list[float]:

    weights = []

    for step in range(
        evidence_time
    ):

        if scheme == "uniform":

            weight = 1.0

        elif scheme == "oracle_event":

            distance = abs(
                step - EVENT_STEP
            )

            weight = math.exp(
                -distance
                / EVENT_MEMORY_TAU
            )

        elif scheme == "triggered_event":

            if detected_event_time is None:

                raise ValueError(
                    "detected event required"
                )

            distance = abs(
                step
                - detected_event_time
            )

            weight = math.exp(
                -distance
                / EVENT_MEMORY_TAU
            )

        else:

            raise ValueError(
                scheme
            )

        weights.append(
            weight
        )

    return weights


def extract_features(
    trajectory: dict,
    *,
    evidence_time: int,
    scheme: str,
    detected_event_time: int | None,
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

    mismatch_indicators = trajectory[
        "mismatch_indicators"
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

    weights = temporal_weights(
        evidence_time=evidence_time,
        scheme=scheme,
        detected_event_time=(
            detected_event_time
        ),
    )

    absolute_innovations = [
        abs(value)
        for value in innovations
    ]

    absolute_updates = [
        abs(value)
        for value in parameter_updates
    ]

    nis_above_one = [
        1.0
        if value > 1.0
        else 0.0
        for value in nis_values
    ]

    return {
        "weighted_abs_innovation":
            weighted_mean(
                absolute_innovations,
                weights,
            ),

        "weighted_nis":
            weighted_mean(
                nis_values,
                weights,
            ),

        "weighted_nis_above_1":
            weighted_mean(
                nis_above_one,
                weights,
            ),

        "weighted_mismatch_indicator":
            weighted_mean(
                mismatch_indicators,
                weights,
            ),

        "weighted_parameter_estimate":
            weighted_mean(
                parameter_estimates,
                weights,
            ),

        "weighted_abs_parameter_update":
            weighted_mean(
                absolute_updates,
                weights,
            ),

        "current_parameter_estimate":
            parameter_estimates[-1],

        "current_mismatch_indicator":
            mismatch_indicators[-1],
    }


def standardize(
    values: list[float],
) -> tuple[
    float,
    float,
]:

    mean_value = statistics.mean(
        values
    )

    if len(values) > 1:

        std_value = statistics.stdev(
            values
        )

    else:

        std_value = 0.0

    if std_value < 1e-12:
        std_value = 1.0

    return (
        mean_value,
        std_value,
    )


def fit_centroids(
    training_rows: list[dict],
) -> dict:

    scaling = {}

    for feature in FEATURE_NAMES:

        scaling[feature] = (
            standardize(
                [
                    row[feature]
                    for row
                    in training_rows
                ]
            )
        )

    groups = defaultdict(list)

    for row in training_rows:

        groups[
            row["condition"]
        ].append(
            row
        )

    centroids = {}

    for condition, group in (
        groups.items()
    ):

        centroid = {}

        for feature in FEATURE_NAMES:

            feature_mean = (
                statistics.mean(
                    row[feature]
                    for row in group
                )
            )

            (
                scale_mean,
                scale_std,
            ) = scaling[
                feature
            ]

            centroid[
                feature
            ] = (
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


def condition_weights(
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

            (
                mean_value,
                std_value,
            ) = model[
                "scaling"
            ][
                feature
            ]

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

    return {
        condition:
            similarity
            / total_similarity
        for condition, similarity
        in similarities.items()
    }


def estimate_target(
    *,
    weights: dict,
    target_name: str,
) -> float:

    return sum(
        weight
        * REFERENCE_TARGETS[
            condition
        ][
            target_name
        ]
        for condition, weight
        in weights.items()
    )


def build_rows() -> list[dict]:

    rows = []

    for (
        condition_index,
        condition,
    ) in enumerate(
        CONDITIONS
    ):

        reference_condition = (
            condition[
                "reference_condition"
            ]
        )

        target = REFERENCE_TARGETS[
            reference_condition
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

                (
                    detected_event_time,
                    trigger_score,
                ) = detect_event_time(
                    trajectory,
                    evidence_time=(
                        evidence_time
                    ),
                )

                for scheme in [
                    "uniform",
                    "oracle_event",
                    "triggered_event",
                ]:

                    features = (
                        extract_features(
                            trajectory,
                            evidence_time=(
                                evidence_time
                            ),
                            scheme=scheme,
                            detected_event_time=(
                                detected_event_time
                            ),
                        )
                    )

                    rows.append(
                        {
                            "condition":
                                reference_condition,

                            "true_class":
                                condition[
                                    "class"
                                ],

                            "run_index":
                                run_index,

                            "split":
                                split,

                            "evidence_time":
                                evidence_time,

                            "scheme":
                                scheme,

                            "detected_event_time":
                                detected_event_time,

                            "event_time_error":
                                abs(
                                    detected_event_time
                                    - EVENT_STEP
                                ),

                            "trigger_score":
                                trigger_score,

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

    return rows


def evaluate_scheme(
    *,
    rows: list[dict],
    scheme: str,
    evidence_time: int,
) -> list[dict]:

    training_rows = [
        row
        for row in rows
        if (
            row["split"]
            == "train"
            and
            row["scheme"]
            == scheme
            and
            row[
                "evidence_time"
            ]
            == evidence_time
        )
    ]

    test_rows = [
        row
        for row in rows
        if (
            row["split"]
            == "test"
            and
            row["scheme"]
            == scheme
            and
            row[
                "evidence_time"
            ]
            == evidence_time
        )
    ]

    model = fit_centroids(
        training_rows
    )

    output = []

    for row in test_rows:

        weights = condition_weights(
            features=row,
            model=model,
        )

        estimate_a = estimate_target(
            weights=weights,
            target_name="p_fail_A",
        )

        estimate_c = estimate_target(
            weights=weights,
            target_name="p_fail_C",
        )

        estimate_s = estimate_target(
            weights=weights,
            target_name="p_fail_S",
        )

        a_error = abs(
            estimate_a
            - row[
                "target_p_fail_A"
            ]
        )

        c_error = abs(
            estimate_c
            - row[
                "target_p_fail_C"
            ]
        )

        s_error = abs(
            estimate_s
            - row[
                "target_p_fail_S"
            ]
        )

        output.append(
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

                "evidence_time":
                    evidence_time,

                "scheme":
                    scheme,

                "detected_event_time":
                    row[
                        "detected_event_time"
                    ],

                "event_time_error":
                    row[
                        "event_time_error"
                    ],

                "trigger_score":
                    row[
                        "trigger_score"
                    ],

                "estimated_p_fail_A":
                    estimate_a,

                "estimated_p_fail_C":
                    estimate_c,

                "estimated_p_fail_S":
                    estimate_s,

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

                "A_mae":
                    a_error,

                "C_mae":
                    c_error,

                "S_mae":
                    s_error,

                "marginal_mae":
                    statistics.mean(
                        [
                            a_error,
                            c_error,
                            s_error,
                        ]
                    ),
            }
        )

    return output


def run_experiment() -> list[dict]:

    feature_rows = build_rows()

    output_rows = []

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        for scheme in [
            "uniform",
            "oracle_event",
            "triggered_event",
        ]:

            output_rows.extend(
                evaluate_scheme(
                    rows=feature_rows,
                    scheme=scheme,
                    evidence_time=(
                        evidence_time
                    ),
                )
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

    print("=" * 126)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "EVENT-TRIGGERED EPISTEMIC MEMORY"
    )

    print("=" * 126)

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        print()
        print(
            f"t={evidence_time}"
        )

        for scheme in [
            "uniform",
            "oracle_event",
            "triggered_event",
        ]:

            group = [
                row
                for row in rows
                if (
                    int(
                        row[
                            "evidence_time"
                        ]
                    )
                    == evidence_time
                    and
                    row[
                        "scheme"
                    ]
                    == scheme
                )
            ]

            mae = statistics.mean(
                float(
                    row[
                        "marginal_mae"
                    ]
                )
                for row in group
            )

            print(
                f"  {scheme:<18}"
                f"MAE={mae:.4f}"
            )

        trigger_group = [
            row
            for row in rows
            if (
                int(
                    row[
                        "evidence_time"
                    ]
                )
                == evidence_time
                and
                row[
                    "scheme"
                ]
                == "triggered_event"
            )
        ]

        mean_event_error = (
            statistics.mean(
                float(
                    row[
                        "event_time_error"
                    ]
                )
                for row in trigger_group
            )
        )

        exact_trigger = (
            sum(
                int(
                    float(
                        row[
                            "event_time_error"
                        ]
                    )
                )
                == 0
                for row
                in trigger_group
            )
            / len(
                trigger_group
            )
        )

        print(
            f"  trigger mean |dt|="
            f"{mean_event_error:.3f} "
            f"exact="
            f"{exact_trigger:.3%}"
        )

    print("=" * 126)


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