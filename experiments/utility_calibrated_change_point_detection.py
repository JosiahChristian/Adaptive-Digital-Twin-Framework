import csv
import statistics
from pathlib import Path

from experiments.persistent_online_change_point_epistemic_memory import (
    EVIDENCE_TIMES,
    EVENT_STEP,
    REFERENCE_TARGETS,
    condition_weights,
    detect_persistent_event,
    extract_features,
    fit_centroids,
    generate_trajectories,
    estimate_target,
)


OUTPUT_PATH = Path(
    "results/utility_calibrated_change_point_detection.csv"
)


THRESHOLD_CANDIDATES = [
    2.0,
    2.5,
    3.0,
    3.5,
    4.0,
    4.5,
    5.0,
    5.5,
]


PERSISTENCE_CANDIDATES = [
    1,
    2,
    3,
    4,
]


CALIBRATION_OBJECTIVES = [
    "timing_only",
    "epistemic_only",
    "joint_utility",
]


LATE_TOLERANCE = 5


def split_trajectories(
    trajectories: list[dict],
) -> tuple[
    list[dict],
    list[dict],
    list[dict],
]:

    calibration_fit = []
    calibration_score = []
    test = []

    for item in trajectories:

        run_index = int(
            item["run_index"]
        )

        if item["split"] == "test":

            test.append(
                item
            )

        elif run_index < 50:

            calibration_fit.append(
                item
            )

        else:

            calibration_score.append(
                item
            )

    return (
        calibration_fit,
        calibration_score,
        test,
    )


def detect_for_trajectory(
    *,
    item: dict,
    threshold: float,
    persistence: int,
    evidence_time: int,
) -> tuple[
    int | None,
    float,
]:

    return detect_persistent_event(
        scores=item["scores"],
        threshold=threshold,
        persistence=persistence,
        evidence_time=evidence_time,
    )


def build_detector_features(
    trajectories: list[dict],
    *,
    threshold: float,
    persistence: int,
    evidence_time: int,
) -> list[dict]:

    rows = []

    for item in trajectories:

        (
            detected_time,
            trigger_score,
        ) = detect_for_trajectory(
            item=item,
            threshold=threshold,
            persistence=persistence,
            evidence_time=evidence_time,
        )

        features = extract_features(
            item["trajectory"],
            evidence_time=evidence_time,
            scheme="persistent_trigger",
            detected_event_time=detected_time,
        )

        target = REFERENCE_TARGETS[
            item["condition"]
        ]

        rows.append(
            {
                "condition":
                    item["condition"],

                "true_class":
                    item["true_class"],

                "run_index":
                    item["run_index"],

                "detected_event_time":
                    detected_time,

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


def epistemic_errors(
    *,
    model: dict,
    rows: list[dict],
) -> list[float]:

    errors = []

    for row in rows:

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

        errors.append(
            statistics.mean(
                [
                    a_error,
                    c_error,
                    s_error,
                ]
            )
        )

    return errors


def detector_statistics(
    *,
    rows: list[dict],
) -> dict:

    triggered = [
        row
        for row in rows
        if row[
            "detected_event_time"
        ]
        is not None
    ]

    trigger_rate = (
        len(triggered)
        / len(rows)
    )

    miss_rate = (
        1.0
        - trigger_rate
    )

    if triggered:

        timing_errors = [
            abs(
                int(
                    row[
                        "detected_event_time"
                    ]
                )
                - EVENT_STEP
            )
            for row in triggered
        ]

        mean_abs_dt = (
            statistics.mean(
                timing_errors
            )
        )

        exact_rate = (
            sum(
                error == 0
                for error
                in timing_errors
            )
            / len(
                timing_errors
            )
        )

        within_3_rate = (
            sum(
                error <= 3
                for error
                in timing_errors
            )
            / len(
                timing_errors
            )
        )

        late_rate = (
            sum(
                int(
                    row[
                        "detected_event_time"
                    ]
                )
                > (
                    EVENT_STEP
                    + LATE_TOLERANCE
                )
                for row
                in triggered
            )
            / len(
                triggered
            )
        )

    else:

        mean_abs_dt = 25.0
        exact_rate = 0.0
        within_3_rate = 0.0
        late_rate = 0.0

    return {
        "trigger_rate":
            trigger_rate,

        "miss_rate":
            miss_rate,

        "mean_abs_dt":
            mean_abs_dt,

        "exact_rate":
            exact_rate,

        "within_3_rate":
            within_3_rate,

        "late_rate":
            late_rate,
    }


def evaluate_candidate(
    *,
    calibration_fit: list[dict],
    calibration_score: list[dict],
    threshold: float,
    persistence: int,
) -> dict:

    epistemic_values = []

    detector_rows_all = []

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        fit_rows = (
            build_detector_features(
                calibration_fit,
                threshold=threshold,
                persistence=persistence,
                evidence_time=evidence_time,
            )
        )

        score_rows = (
            build_detector_features(
                calibration_score,
                threshold=threshold,
                persistence=persistence,
                evidence_time=evidence_time,
            )
        )

        model = fit_centroids(
            fit_rows
        )

        epistemic_values.extend(
            epistemic_errors(
                model=model,
                rows=score_rows,
            )
        )

        detector_rows_all.extend(
            score_rows
        )

    epistemic_mae = (
        statistics.mean(
            epistemic_values
        )
    )

    detector_stats = (
        detector_statistics(
            rows=detector_rows_all
        )
    )

    mean_abs_dt = (
        detector_stats[
            "mean_abs_dt"
        ]
    )

    miss_rate = (
        detector_stats[
            "miss_rate"
        ]
    )

    late_rate = (
        detector_stats[
            "late_rate"
        ]
    )

    timing_objective = (
        mean_abs_dt
        + 25.0
        * miss_rate
        + 10.0
        * late_rate
    )

    epistemic_objective = (
        epistemic_mae
    )

    joint_objective = (
        epistemic_mae
        + 0.0025
        * mean_abs_dt
        + 0.0500
        * miss_rate
        + 0.0250
        * late_rate
    )

    return {
        "threshold":
            threshold,

        "persistence":
            persistence,

        "epistemic_mae":
            epistemic_mae,

        "timing_objective":
            timing_objective,

        "epistemic_objective":
            epistemic_objective,

        "joint_objective":
            joint_objective,

        **detector_stats,
    }


def calibrate_detectors(
    *,
    calibration_fit: list[dict],
    calibration_score: list[dict],
) -> dict:

    candidates = []

    for threshold in (
        THRESHOLD_CANDIDATES
    ):

        for persistence in (
            PERSISTENCE_CANDIDATES
        ):

            candidates.append(
                evaluate_candidate(
                    calibration_fit=(
                        calibration_fit
                    ),
                    calibration_score=(
                        calibration_score
                    ),
                    threshold=threshold,
                    persistence=persistence,
                )
            )

    selected = {}

    selected[
        "timing_only"
    ] = min(
        candidates,
        key=lambda row: (
            row[
                "timing_objective"
            ],
            row[
                "threshold"
            ],
            row[
                "persistence"
            ],
        ),
    )

    selected[
        "epistemic_only"
    ] = min(
        candidates,
        key=lambda row: (
            row[
                "epistemic_objective"
            ],
            row[
                "threshold"
            ],
            row[
                "persistence"
            ],
        ),
    )

    selected[
        "joint_utility"
    ] = min(
        candidates,
        key=lambda row: (
            row[
                "joint_objective"
            ],
            row[
                "threshold"
            ],
            row[
                "persistence"
            ],
        ),
    )

    return selected


def build_memory_features(
    trajectories: list[dict],
    *,
    scheme: str,
    evidence_time: int,
    threshold: float | None = None,
    persistence: int | None = None,
) -> list[dict]:

    rows = []

    for item in trajectories:

        if scheme == "uniform":

            detected_time = None

            feature_scheme = (
                "uniform"
            )

        elif scheme == "oracle_event":

            detected_time = None

            feature_scheme = (
                "oracle_event"
            )

        else:

            if (
                threshold is None
                or persistence is None
            ):

                raise ValueError(
                    "Detector parameters required"
                )

            (
                detected_time,
                _,
            ) = detect_for_trajectory(
                item=item,
                threshold=threshold,
                persistence=persistence,
                evidence_time=evidence_time,
            )

            feature_scheme = (
                "persistent_trigger"
            )

        features = extract_features(
            item["trajectory"],
            evidence_time=evidence_time,
            scheme=feature_scheme,
            detected_event_time=(
                detected_time
            ),
        )

        target = REFERENCE_TARGETS[
            item["condition"]
        ]

        rows.append(
            {
                "condition":
                    item["condition"],

                "true_class":
                    item["true_class"],

                "run_index":
                    item["run_index"],

                "detected_event_time":
                    detected_time,

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


def evaluate_final_scheme(
    *,
    training_trajectories: list[dict],
    test_trajectories: list[dict],
    scheme: str,
    evidence_time: int,
    threshold: float | None = None,
    persistence: int | None = None,
) -> list[dict]:

    training_rows = (
        build_memory_features(
            training_trajectories,
            scheme=scheme,
            evidence_time=evidence_time,
            threshold=threshold,
            persistence=persistence,
        )
    )

    test_rows = (
        build_memory_features(
            test_trajectories,
            scheme=scheme,
            evidence_time=evidence_time,
            threshold=threshold,
            persistence=persistence,
        )
    )

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

        detected_time = (
            row[
                "detected_event_time"
            ]
        )

        triggered = (
            detected_time
            is not None
        )

        event_time_error = (
            abs(
                int(
                    detected_time
                )
                - EVENT_STEP
            )
            if triggered
            else ""
        )

        late_trigger = (
            (
                int(
                    detected_time
                )
                > (
                    EVENT_STEP
                    + LATE_TOLERANCE
                )
            )
            if triggered
            else False
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

                "threshold":
                    (
                        threshold
                        if threshold
                        is not None
                        else ""
                    ),

                "persistence":
                    (
                        persistence
                        if persistence
                        is not None
                        else ""
                    ),

                "detected_event_time":
                    (
                        detected_time
                        if triggered
                        else ""
                    ),

                "triggered":
                    triggered,

                "event_time_error":
                    event_time_error,

                "within_3":
                    (
                        event_time_error <= 3
                        if triggered
                        else False
                    ),

                "exact":
                    (
                        event_time_error == 0
                        if triggered
                        else False
                    ),

                "late_trigger":
                    late_trigger,

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

    (
        calibration_fit,
        calibration_score,
        test_trajectories,
    ) = split_trajectories(
        trajectories
    )

    full_training = (
        calibration_fit
        + calibration_score
    )

    selected = calibrate_detectors(
        calibration_fit=(
            calibration_fit
        ),
        calibration_score=(
            calibration_score
        ),
    )

    output_rows = []

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        output_rows.extend(
            evaluate_final_scheme(
                training_trajectories=(
                    full_training
                ),
                test_trajectories=(
                    test_trajectories
                ),
                scheme="uniform",
                evidence_time=(
                    evidence_time
                ),
            )
        )

        output_rows.extend(
            evaluate_final_scheme(
                training_trajectories=(
                    full_training
                ),
                test_trajectories=(
                    test_trajectories
                ),
                scheme="oracle_event",
                evidence_time=(
                    evidence_time
                ),
            )
        )

        for objective in (
            CALIBRATION_OBJECTIVES
        ):

            detector = selected[
                objective
            ]

            output_rows.extend(
                evaluate_final_scheme(
                    training_trajectories=(
                        full_training
                    ),
                    test_trajectories=(
                        test_trajectories
                    ),
                    scheme=objective,
                    evidence_time=(
                        evidence_time
                    ),
                    threshold=float(
                        detector[
                            "threshold"
                        ]
                    ),
                    persistence=int(
                        detector[
                            "persistence"
                        ]
                    ),
                )
            )

    return (
        output_rows,
        selected,
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


def print_detector_selection(
    selected: dict,
) -> None:

    print(
        "CALIBRATED DETECTORS"
    )

    for objective in (
        CALIBRATION_OBJECTIVES
    ):

        detector = selected[
            objective
        ]

        print(
            f"{objective:<18}"
            f"threshold="
            f"{detector['threshold']:.2f} "
            f"persistence="
            f"{detector['persistence']} "
            f"cal_epistemic="
            f"{detector['epistemic_mae']:.4f} "
            f"|dt|="
            f"{detector['mean_abs_dt']:.3f} "
            f"miss="
            f"{detector['miss_rate']:.3%} "
            f"late="
            f"{detector['late_rate']:.3%}"
        )


def print_summary(
    rows: list[dict],
    selected: dict,
) -> None:

    print("=" * 132)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "UTILITY-CALIBRATED CHANGE-POINT DETECTION"
    )

    print("=" * 132)

    print_detector_selection(
        selected
    )

    schemes = [
        "uniform",
        "oracle_event",
        "timing_only",
        "epistemic_only",
        "joint_utility",
    ]

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        print()
        print(
            f"t={evidence_time}"
        )

        for scheme in schemes:

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

            if scheme in {
                "uniform",
                "oracle_event",
            }:

                print(
                    f"  {scheme:<18}"
                    f"MAE={mae:.4f}"
                )

                continue

            triggered = [
                row
                for row in group
                if row[
                    "triggered"
                ]
                == "True"
            ]

            trigger_rate = (
                len(triggered)
                / len(group)
            )

            if triggered:

                mean_dt = (
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

                within_3 = (
                    sum(
                        row[
                            "within_3"
                        ]
                        == "True"
                        for row
                        in triggered
                    )
                    / len(
                        triggered
                    )
                )

                exact = (
                    sum(
                        row[
                            "exact"
                        ]
                        == "True"
                        for row
                        in triggered
                    )
                    / len(
                        triggered
                    )
                )

                late = (
                    sum(
                        row[
                            "late_trigger"
                        ]
                        == "True"
                        for row
                        in triggered
                    )
                    / len(
                        triggered
                    )
                )

            else:

                mean_dt = float(
                    "nan"
                )

                within_3 = 0.0
                exact = 0.0
                late = 0.0

            print(
                f"  {scheme:<18}"
                f"MAE={mae:.4f} "
                f"trigger="
                f"{trigger_rate:.3%} "
                f"|dt|="
                f"{mean_dt:.3f} "
                f"within3="
                f"{within_3:.3%} "
                f"exact="
                f"{exact:.3%} "
                f"late="
                f"{late:.3%}"
            )

    print("=" * 132)


def main() -> None:

    (
        rows,
        selected,
    ) = run_experiment()

    save_results(
        rows
    )

    print_summary(
        rows,
        selected,
    )

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()