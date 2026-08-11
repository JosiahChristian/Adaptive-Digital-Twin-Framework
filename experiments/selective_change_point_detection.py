import csv
import statistics
from collections import defaultdict
from pathlib import Path

from experiments.utility_calibrated_change_point_detection import (
    EVENT_STEP,
    LATE_TOLERANCE,
)

from experiments.persistent_online_change_point_epistemic_memory import (
    EVIDENCE_TIMES,
    REFERENCE_TARGETS,
    condition_weights,
    detect_persistent_event,
    extract_features,
    fit_centroids,
    generate_trajectories,
    estimate_target,
)


OUTPUT_PATH = Path(
    "results/selective_change_point_detection.csv"
)


BASE_THRESHOLD = 4.50
BASE_PERSISTENCE = 1


ACCEPTANCE_SCORE_QUANTILES = [
    0.00,
    0.20,
    0.40,
    0.60,
    0.80,
    0.90,
]


def split_trajectories(
    trajectories: list[dict],
) -> tuple[
    list[dict],
    list[dict],
]:

    training = [
        item
        for item in trajectories
        if item["split"] == "train"
    ]

    test = [
        item
        for item in trajectories
        if item["split"] == "test"
    ]

    return (
        training,
        test,
    )


def detect_candidate(
    *,
    item: dict,
    evidence_time: int,
) -> tuple[
    int | None,
    float,
]:

    return detect_persistent_event(
        scores=item["scores"],
        threshold=BASE_THRESHOLD,
        persistence=BASE_PERSISTENCE,
        evidence_time=evidence_time,
    )


def quantile(
    values: list[float],
    q: float,
) -> float:

    if not values:
        return float("inf")

    ordered = sorted(
        values
    )

    if len(ordered) == 1:
        return ordered[0]

    position = (
        q
        * (
            len(ordered)
            - 1
        )
    )

    lower_index = int(
        position
    )

    upper_index = min(
        lower_index + 1,
        len(ordered) - 1,
    )

    fraction = (
        position
        - lower_index
    )

    return (
        ordered[lower_index]
        * (
            1.0 - fraction
        )
        +
        ordered[upper_index]
        * fraction
    )


def calibration_thresholds(
    training: list[dict],
) -> dict[
    int,
    dict[
        float,
        float,
    ],
]:

    thresholds = {}

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        trigger_scores = []

        for item in training:

            (
                detected_time,
                trigger_score,
            ) = detect_candidate(
                item=item,
                evidence_time=evidence_time,
            )

            if detected_time is not None:

                trigger_scores.append(
                    float(
                        trigger_score
                    )
                )

        thresholds[
            evidence_time
        ] = {}

        for q in (
            ACCEPTANCE_SCORE_QUANTILES
        ):

            thresholds[
                evidence_time
            ][
                q
            ] = quantile(
                trigger_scores,
                q,
            )

    return thresholds


def build_features(
    trajectories: list[dict],
    *,
    evidence_time: int,
    mode: str,
    acceptance_threshold: float | None,
) -> list[dict]:

    rows = []

    for item in trajectories:

        (
            detected_time,
            trigger_score,
        ) = detect_candidate(
            item=item,
            evidence_time=evidence_time,
        )

        candidate_exists = (
            detected_time
            is not None
        )

        if mode == "uniform":

            accepted = False
            feature_scheme = "uniform"
            feature_anchor = None

        elif mode == "oracle_event":

            accepted = True
            feature_scheme = "oracle_event"
            feature_anchor = None

        elif mode == "selective":

            if acceptance_threshold is None:

                raise ValueError(
                    "acceptance threshold required"
                )

            accepted = (
                candidate_exists
                and
                float(
                    trigger_score
                )
                >= acceptance_threshold
            )

            if accepted:

                feature_scheme = (
                    "persistent_trigger"
                )

                feature_anchor = (
                    detected_time
                )

            else:

                feature_scheme = (
                    "uniform"
                )

                feature_anchor = None

        else:

            raise ValueError(
                mode
            )

        features = extract_features(
            item["trajectory"],
            evidence_time=evidence_time,
            scheme=feature_scheme,
            detected_event_time=(
                feature_anchor
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

                "candidate_exists":
                    candidate_exists,

                "accepted":
                    accepted,

                "detected_event_time":
                    (
                        detected_time
                        if candidate_exists
                        else ""
                    ),

                "trigger_score":
                    (
                        float(
                            trigger_score
                        )
                        if candidate_exists
                        else ""
                    ),

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


def infer_rows(
    *,
    training_rows: list[dict],
    test_rows: list[dict],
) -> list[dict]:

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

        marginal_mae = (
            statistics.mean(
                [
                    a_error,
                    c_error,
                    s_error,
                ]
            )
        )

        candidate_exists = bool(
            row[
                "candidate_exists"
            ]
        )

        accepted = bool(
            row[
                "accepted"
            ]
        )

        detected_time = (
            int(
                row[
                    "detected_event_time"
                ]
            )
            if candidate_exists
            else None
        )

        event_time_error = (
            abs(
                detected_time
                - EVENT_STEP
            )
            if candidate_exists
            else None
        )

        output.append(
            {
                **row,

                "estimated_p_fail_A":
                    estimate_a,

                "estimated_p_fail_C":
                    estimate_c,

                "estimated_p_fail_S":
                    estimate_s,

                "A_mae":
                    a_error,

                "C_mae":
                    c_error,

                "S_mae":
                    s_error,

                "marginal_mae":
                    marginal_mae,

                "event_time_error":
                    (
                        event_time_error
                        if event_time_error
                        is not None
                        else ""
                    ),

                "within_3":
                    (
                        event_time_error <= 3
                        if event_time_error
                        is not None
                        else False
                    ),

                "exact":
                    (
                        event_time_error == 0
                        if event_time_error
                        is not None
                        else False
                    ),

                "late_trigger":
                    (
                        detected_time
                        > (
                            EVENT_STEP
                            + LATE_TOLERANCE
                        )
                        if detected_time
                        is not None
                        else False
                    ),
            }
        )

    return output


def evaluate_selective_setting(
    *,
    training: list[dict],
    test: list[dict],
    evidence_time: int,
    quantile_level: float,
    acceptance_threshold: float,
) -> list[dict]:

    training_rows = build_features(
        training,
        evidence_time=evidence_time,
        mode="selective",
        acceptance_threshold=(
            acceptance_threshold
        ),
    )

    test_rows = build_features(
        test,
        evidence_time=evidence_time,
        mode="selective",
        acceptance_threshold=(
            acceptance_threshold
        ),
    )

    inferred = infer_rows(
        training_rows=training_rows,
        test_rows=test_rows,
    )

    for row in inferred:

        row[
            "evidence_time"
        ] = evidence_time

        row[
            "scheme"
        ] = "selective"

        row[
            "acceptance_quantile"
        ] = quantile_level

        row[
            "acceptance_threshold"
        ] = acceptance_threshold

    return inferred


def evaluate_baseline_scheme(
    *,
    training: list[dict],
    test: list[dict],
    evidence_time: int,
    scheme: str,
) -> list[dict]:

    training_rows = build_features(
        training,
        evidence_time=evidence_time,
        mode=scheme,
        acceptance_threshold=None,
    )

    test_rows = build_features(
        test,
        evidence_time=evidence_time,
        mode=scheme,
        acceptance_threshold=None,
    )

    inferred = infer_rows(
        training_rows=training_rows,
        test_rows=test_rows,
    )

    for row in inferred:

        row[
            "evidence_time"
        ] = evidence_time

        row[
            "scheme"
        ] = scheme

        row[
            "acceptance_quantile"
        ] = ""

        row[
            "acceptance_threshold"
        ] = ""

    return inferred


def run_experiment() -> list[dict]:

    trajectories = (
        generate_trajectories()
    )

    (
        training,
        test,
    ) = split_trajectories(
        trajectories
    )

    thresholds = (
        calibration_thresholds(
            training
        )
    )

    output_rows = []

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        output_rows.extend(
            evaluate_baseline_scheme(
                training=training,
                test=test,
                evidence_time=evidence_time,
                scheme="uniform",
            )
        )

        output_rows.extend(
            evaluate_baseline_scheme(
                training=training,
                test=test,
                evidence_time=evidence_time,
                scheme="oracle_event",
            )
        )

        for quantile_level in (
            ACCEPTANCE_SCORE_QUANTILES
        ):

            acceptance_threshold = (
                thresholds[
                    evidence_time
                ][
                    quantile_level
                ]
            )

            output_rows.extend(
                evaluate_selective_setting(
                    training=training,
                    test=test,
                    evidence_time=evidence_time,
                    quantile_level=(
                        quantile_level
                    ),
                    acceptance_threshold=(
                        acceptance_threshold
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


def selective_summary(
    rows: list[dict],
) -> list[dict]:

    summaries = []

    groups = defaultdict(list)

    for row in rows:

        if row[
            "scheme"
        ] != "selective":

            continue

        key = (
            int(
                row[
                    "evidence_time"
                ]
            ),
            float(
                row[
                    "acceptance_quantile"
                ]
            ),
        )

        groups[
            key
        ].append(
            row
        )

    for (
        evidence_time,
        quantile_level,
    ), group in sorted(
        groups.items()
    ):

        accepted = [
            row
            for row in group
            if row[
                "accepted"
            ]
            == "True"
        ]

        coverage = (
            len(accepted)
            / len(group)
        )

        overall_mae = (
            statistics.mean(
                float(
                    row[
                        "marginal_mae"
                    ]
                )
                for row in group
            )
        )

        if accepted:

            accepted_mae = (
                statistics.mean(
                    float(
                        row[
                            "marginal_mae"
                        ]
                    )
                    for row
                    in accepted
                )
            )

            mean_dt = (
                statistics.mean(
                    float(
                        row[
                            "event_time_error"
                        ]
                    )
                    for row
                    in accepted
                )
            )

            within_3 = (
                sum(
                    row[
                        "within_3"
                    ]
                    == "True"
                    for row
                    in accepted
                )
                / len(
                    accepted
                )
            )

            exact = (
                sum(
                    row[
                        "exact"
                    ]
                    == "True"
                    for row
                    in accepted
                )
                / len(
                    accepted
                )
            )

            late = (
                sum(
                    row[
                        "late_trigger"
                    ]
                    == "True"
                    for row
                    in accepted
                )
                / len(
                    accepted
                )
            )

        else:

            accepted_mae = float(
                "nan"
            )

            mean_dt = float(
                "nan"
            )

            within_3 = 0.0
            exact = 0.0
            late = 0.0

        summaries.append(
            {
                "evidence_time":
                    evidence_time,

                "quantile":
                    quantile_level,

                "coverage":
                    coverage,

                "accepted_mae":
                    accepted_mae,

                "overall_mae":
                    overall_mae,

                "mean_abs_dt":
                    mean_dt,

                "within_3":
                    within_3,

                "exact":
                    exact,

                "late":
                    late,
            }
        )

    return summaries


def print_summary(
    rows: list[dict],
) -> None:

    print("=" * 132)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "SELECTIVE CHANGE-POINT DETECTION"
    )

    print("=" * 132)

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
                for row
                in group
            )

            print(
                f"  {scheme:<14}"
                f"MAE="
                f"{mae:.4f}"
            )

    print()
    print(
        "RISK-COVERAGE"
    )

    summaries = selective_summary(
        rows
    )

    print(
        f"{'t':>5}"
        f"{'q':>8}"
        f"{'coverage':>12}"
        f"{'accepted_MAE':>16}"
        f"{'overall_MAE':>14}"
        f"{'|dt|':>10}"
        f"{'within3':>12}"
        f"{'exact':>12}"
        f"{'late':>12}"
    )

    for row in summaries:

        print(
            f"{row['evidence_time']:>5}"
            f"{row['quantile']:>8.2f}"
            f"{row['coverage']:>12.3%}"
            f"{row['accepted_mae']:>16.4f}"
            f"{row['overall_mae']:>14.4f}"
            f"{row['mean_abs_dt']:>10.3f}"
            f"{row['within_3']:>12.3%}"
            f"{row['exact']:>12.3%}"
            f"{row['late']:>12.3%}"
        )

    print("=" * 132)


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