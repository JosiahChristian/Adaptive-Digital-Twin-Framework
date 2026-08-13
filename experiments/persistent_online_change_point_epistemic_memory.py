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
    "results/persistent_online_change_point_epistemic_memory.csv"
)

EVIDENCE_TIMES = [
    60,
    70,
    80,
    100,
]

BASE_SEED = 44000

ROLLING_BASELINE_WINDOW = 20

DETECTOR_START = 25

MEMORY_TAU = 8.0


THRESHOLD_CANDIDATES = [
    2.5,
    3.0,
    3.5,
    4.0,
    4.5,
    5.0,
]

PERSISTENCE_CANDIDATES = [
    1,
    2,
    3,
]


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


def robust_location_scale(
    values: list[float],
) -> tuple[
    float,
    float,
]:

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

    return (
        median_value,
        scale,
    )


def robust_positive_z(
    value: float,
    baseline: list[float],
) -> float:

    location, scale = (
        robust_location_scale(
            baseline
        )
    )

    return max(
        0.0,
        (
            value
            - location
        )
        / scale,
    )


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


def online_anomaly_scores(
    trajectory: dict,
) -> list[float]:

    innovations = [
        abs(value)
        for value in trajectory[
            "innovations"
        ]
    ]

    nis_values = trajectory[
        "nis_values"
    ]

    mismatch_values = trajectory[
        "mismatch_indicators"
    ]

    update_values = [
        abs(value)
        for value in trajectory[
            "parameter_updates"
        ]
    ]

    scores = [
        0.0
        for _ in range(
            len(
                nis_values
            )
        )
    ]

    for step in range(
        DETECTOR_START,
        len(
            nis_values
        ),
    ):

        baseline_start = max(
            0,
            step
            - ROLLING_BASELINE_WINDOW,
        )

        baseline_end = step

        baseline_nis = nis_values[
            baseline_start:baseline_end
        ]

        baseline_mismatch = (
            mismatch_values[
                baseline_start:baseline_end
            ]
        )

        baseline_updates = (
            update_values[
                baseline_start:baseline_end
            ]
        )

        baseline_innovations = (
            innovations[
                baseline_start:baseline_end
            ]
        )

        z_nis = robust_positive_z(
            nis_values[
                step
            ],
            baseline_nis,
        )

        z_mismatch = robust_positive_z(
            mismatch_values[
                step
            ],
            baseline_mismatch,
        )

        z_update = robust_positive_z(
            update_values[
                step
            ],
            baseline_updates,
        )

        z_innovation = robust_positive_z(
            innovations[
                step
            ],
            baseline_innovations,
        )

        scores[
            step
        ] = statistics.mean(
            [
                z_nis,
                z_mismatch,
                z_update,
                z_innovation,
            ]
        )

    return scores


def detect_persistent_event(
    *,
    scores: list[float],
    threshold: float,
    persistence: int,
    evidence_time: int,
) -> tuple[
    int | None,
    float,
]:

    run_length = 0
    run_start = None

    for step in range(
        DETECTOR_START,
        evidence_time,
    ):

        if scores[
            step
        ] >= threshold:

            if run_length == 0:
                run_start = step

            run_length += 1

            if run_length >= persistence:

                anchor = (
                    run_start
                    if run_start
                    is not None
                    else step
                )

                return (
                    anchor,
                    scores[
                        step
                    ],
                )

        else:

            run_length = 0
            run_start = None

    return (
        None,
        0.0,
    )


def detector_training_loss(
    *,
    trajectories: list[dict],
    threshold: float,
    persistence: int,
) -> float:

    losses = []

    for item in trajectories:

        scores = item[
            "scores"
        ]

        (
            detected_time,
            _,
        ) = detect_persistent_event(
            scores=scores,
            threshold=threshold,
            persistence=persistence,
            evidence_time=STEPS,
        )

        if detected_time is None:

            # Missing a real experimental event
            # receives a strong penalty.
            loss = 25.0

        else:

            timing_error = abs(
                detected_time
                - EVENT_STEP
            )

            early_penalty = (
                10.0
                if detected_time
                < EVENT_STEP - 5
                else 0.0
            )

            loss = (
                timing_error
                + early_penalty
            )

        losses.append(
            loss
        )

    return statistics.mean(
        losses
    )


def select_detector_parameters(
    training_trajectories: list[dict],
) -> tuple[
    float,
    int,
    float,
]:

    candidates = []

    for threshold in (
        THRESHOLD_CANDIDATES
    ):

        for persistence in (
            PERSISTENCE_CANDIDATES
        ):

            loss = detector_training_loss(
                trajectories=(
                    training_trajectories
                ),
                threshold=threshold,
                persistence=persistence,
            )

            candidates.append(
                (
                    loss,
                    threshold,
                    persistence,
                )
            )

    (
        best_loss,
        best_threshold,
        best_persistence,
    ) = min(
        candidates,
        key=lambda item: (
            item[0],
            item[1],
            item[2],
        ),
    )

    return (
        best_threshold,
        best_persistence,
        best_loss,
    )


def temporal_weights(
    *,
    evidence_time: int,
    scheme: str,
    detected_event_time: (
        int | None
    ),
) -> list[float]:

    weights = []

    for step in range(
        evidence_time
    ):

        if scheme == "uniform":

            weight = 1.0

        elif scheme == "oracle_event":

            distance = abs(
                step
                - EVENT_STEP
            )

            weight = math.exp(
                -distance
                / MEMORY_TAU
            )

        elif scheme == "persistent_trigger":

            if detected_event_time is None:

                # Before a trigger occurs, retain
                # ordinary uniform evidence.
                weight = 1.0

            else:

                distance = abs(
                    step
                    - detected_event_time
                )

                weight = math.exp(
                    -distance
                    / MEMORY_TAU
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
    detected_event_time: (
        int | None
    ),
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

    std_value = (
        statistics.stdev(
            values
        )
        if len(values) > 1
        else 0.0
    )

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

        scaling[
            feature
        ] = standardize(
            [
                row[
                    feature
                ]
                for row
                in training_rows
            ]
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
                    row[
                        feature
                    ]
                    for row
                    in group
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


def generate_trajectories(
    base_seed: int = BASE_SEED,
) -> list[dict]:
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

        for run_index in range(
            RUNS_PER_CONDITION
        ):

            seed = (
                base_seed
                + condition_index
                * RUNS_PER_CONDITION
                + run_index
            )

            trajectory = run_trajectory(
                condition=condition,
                seed=seed,
            )

            scores = (
                online_anomaly_scores(
                    trajectory
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
                        (
                            "train"
                            if run_index
                            < RUNS_PER_CONDITION // 2
                            else "test"
                        ),

                    "trajectory":
                        trajectory,

                    "scores":
                        scores,
                }
            )

    return rows


def build_feature_rows(
    trajectories: list[dict],
    *,
    threshold: float,
    persistence: int,
) -> list[dict]:

    rows = []

    for item in trajectories:

        target = REFERENCE_TARGETS[
            item[
                "condition"
            ]
        ]

        for evidence_time in (
            EVIDENCE_TIMES
        ):

            (
                detected_time,
                trigger_score,
            ) = detect_persistent_event(
                scores=item[
                    "scores"
                ],
                threshold=threshold,
                persistence=persistence,
                evidence_time=(
                    evidence_time
                ),
            )

            for scheme in [
                "uniform",
                "oracle_event",
                "persistent_trigger",
            ]:

                features = (
                    extract_features(
                        item[
                            "trajectory"
                        ],
                        evidence_time=(
                            evidence_time
                        ),
                        scheme=scheme,
                        detected_event_time=(
                            detected_time
                        ),
                    )
                )

                rows.append(
                    {
                        "condition":
                            item[
                                "condition"
                            ],

                        "true_class":
                            item[
                                "true_class"
                            ],

                        "run_index":
                            item[
                                "run_index"
                            ],

                        "split":
                            item[
                                "split"
                            ],

                        "evidence_time":
                            evidence_time,

                        "scheme":
                            scheme,

                        "detected_event_time":
                            (
                                detected_time
                                if detected_time
                                is not None
                                else ""
                            ),

                        "triggered":
                            (
                                detected_time
                                is not None
                            ),

                        "event_time_error":
                            (
                                abs(
                                    detected_time
                                    - EVENT_STEP
                                )
                                if detected_time
                                is not None
                                else ""
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
            row[
                "split"
            ]
            == "train"
            and
            row[
                "scheme"
            ]
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
            row[
                "split"
            ]
            == "test"
            and
            row[
                "scheme"
            ]
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

                "triggered":
                    row[
                        "triggered"
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


def run_experiment() -> tuple[
    list[dict],
    dict,
]:

    trajectories = (
        generate_trajectories()
    )

    training_trajectories = [
        item
        for item in trajectories
        if item[
            "split"
        ]
        == "train"
    ]

    (
        threshold,
        persistence,
        training_loss,
    ) = select_detector_parameters(
        training_trajectories
    )

    feature_rows = build_feature_rows(
        trajectories,
        threshold=threshold,
        persistence=persistence,
    )

    output_rows = []

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        for scheme in [
            "uniform",
            "oracle_event",
            "persistent_trigger",
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

    detector_info = {
        "threshold":
            threshold,

        "persistence":
            persistence,

        "training_loss":
            training_loss,
    }

    return (
        output_rows,
        detector_info,
    )


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
    detector_info: dict,
) -> None:

    print("=" * 126)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PERSISTENT ONLINE CHANGE-POINT EPISTEMIC MEMORY"
    )

    print("=" * 126)

    print(
        "Detector: "
        f"threshold="
        f"{detector_info['threshold']:.2f} "
        f"persistence="
        f"{detector_info['persistence']} "
        f"training_loss="
        f"{detector_info['training_loss']:.3f}"
    )

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
            "persistent_trigger",
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
                f"  {scheme:<20}"
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
                == "persistent_trigger"
            )
        ]

        triggered = [
            row
            for row in trigger_group
            if row[
                "triggered"
            ]
            == "True"
        ]

        trigger_rate = (
            len(
                triggered
            )
            / len(
                trigger_group
            )
        )

        if triggered:

            mean_event_error = (
                statistics.mean(
                    float(
                        row[
                            "event_time_error"
                        ]
                    )
                    for row
                    in triggered
                )
            )

            exact = (
                sum(
                    float(
                        row[
                            "event_time_error"
                        ]
                    )
                    == 0.0
                    for row
                    in triggered
                )
                / len(
                    triggered
                )
            )

        else:

            mean_event_error = float(
                "nan"
            )

            exact = 0.0

        print(
            f"  trigger_rate="
            f"{trigger_rate:.3%} "
            f"mean |dt|="
            f"{mean_event_error:.3f} "
            f"exact="
            f"{exact:.3%}"
        )

    print("=" * 126)


def main() -> None:

    (
        rows,
        detector_info,
    ) = run_experiment()

    save_results(
        rows
    )

    print_summary(
        rows,
        detector_info,
    )

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()