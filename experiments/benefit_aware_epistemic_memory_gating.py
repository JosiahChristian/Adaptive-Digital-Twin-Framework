import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

from experiments.persistent_online_change_point_epistemic_memory import (
    EVIDENCE_TIMES,
    FEATURE_NAMES,
    REFERENCE_TARGETS,
    condition_weights,
    detect_persistent_event,
    extract_features,
    fit_centroids,
    generate_trajectories,
    estimate_target,
)

from experiments.selective_change_point_detection import (
    quantile,
)


OUTPUT_PATH = Path(
    "results/benefit_aware_epistemic_memory_gating.csv"
)


DETECTOR_THRESHOLD = 4.50
DETECTOR_PERSISTENCE = 1

SCORE_GATE_QUANTILE = 0.90


GATE_FEATURE_NAMES = [
    "candidate_exists",
    "trigger_score",
    "anchor_age",
    "feature_distance",
    "current_mismatch_indicator",
    "current_parameter_estimate",
]


def split_trajectories(
    trajectories: list[dict],
) -> tuple[
    list[dict],
    list[dict],
    list[dict],
]:

    memory_fit = []
    gate_train = []
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

            memory_fit.append(
                item
            )

        else:

            gate_train.append(
                item
            )

    return (
        memory_fit,
        gate_train,
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
        threshold=DETECTOR_THRESHOLD,
        persistence=DETECTOR_PERSISTENCE,
        evidence_time=evidence_time,
    )


def build_representation(
    *,
    item: dict,
    evidence_time: int,
    mode: str,
) -> dict:

    (
        detected_time,
        trigger_score,
    ) = detect_candidate(
        item=item,
        evidence_time=evidence_time,
    )

    candidate_exists = (
        detected_time is not None
    )

    if mode == "uniform":

        scheme = "uniform"
        anchor = None

    elif mode == "candidate_event":

        if candidate_exists:

            scheme = (
                "persistent_trigger"
            )

            anchor = detected_time

        else:

            scheme = "uniform"
            anchor = None

    elif mode == "oracle_event":

        scheme = "oracle_event"
        anchor = None

    else:

        raise ValueError(
            mode
        )

    features = extract_features(
        item["trajectory"],
        evidence_time=evidence_time,
        scheme=scheme,
        detected_event_time=anchor,
    )

    target = REFERENCE_TARGETS[
        item["condition"]
    ]

    return {
        "condition":
            item["condition"],

        "true_class":
            item["true_class"],

        "run_index":
            item["run_index"],

        "candidate_exists":
            candidate_exists,

        "detected_event_time":
            detected_time,

        "trigger_score":
            (
                float(
                    trigger_score
                )
                if candidate_exists
                else 0.0
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


def fit_memory_model(
    trajectories: list[dict],
    *,
    evidence_time: int,
    mode: str,
) -> dict:

    rows = [
        build_representation(
            item=item,
            evidence_time=evidence_time,
            mode=mode,
        )
        for item in trajectories
    ]

    return fit_centroids(
        rows
    )


def infer_epistemic(
    *,
    row: dict,
    model: dict,
) -> dict:

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

    return {
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
            statistics.mean(
                [
                    a_error,
                    c_error,
                    s_error,
                ]
            ),
    }


def representation_distance(
    uniform_row: dict,
    event_row: dict,
) -> float:

    squared = 0.0

    for feature in FEATURE_NAMES:

        difference = (
            float(
                event_row[
                    feature
                ]
            )
            - float(
                uniform_row[
                    feature
                ]
            )
        )

        squared += (
            difference ** 2
        )

    return math.sqrt(
        squared
    )


def gate_features(
    *,
    uniform_row: dict,
    event_row: dict,
    evidence_time: int,
) -> dict:

    candidate_exists = bool(
        event_row[
            "candidate_exists"
        ]
    )

    detected_time = (
        event_row[
            "detected_event_time"
        ]
    )

    if (
        candidate_exists
        and
        detected_time
        is not None
    ):

        anchor_age = (
            evidence_time
            - int(
                detected_time
            )
        )

    else:

        anchor_age = float(
            evidence_time
        )

    return {
        "candidate_exists":
            (
                1.0
                if candidate_exists
                else 0.0
            ),

        "trigger_score":
            float(
                event_row[
                    "trigger_score"
                ]
            ),

        "anchor_age":
            float(
                anchor_age
            ),

        "feature_distance":
            representation_distance(
                uniform_row,
                event_row,
            ),

        "current_mismatch_indicator":
            float(
                uniform_row[
                    "current_mismatch_indicator"
                ]
            ),

        "current_parameter_estimate":
            float(
                uniform_row[
                    "current_parameter_estimate"
                ]
            ),
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


def fit_benefit_gate(
    rows: list[dict],
) -> dict:

    scaling = {}

    for feature in (
        GATE_FEATURE_NAMES
    ):

        scaling[
            feature
        ] = standardize(
            [
                row[
                    feature
                ]
                for row in rows
            ]
        )

    groups = defaultdict(
        list
    )

    for row in rows:

        groups[
            int(
                row[
                    "beneficial"
                ]
            )
        ].append(
            row
        )

    centroids = {}

    for label in [
        0,
        1,
    ]:

        group = groups[
            label
        ]

        centroid = {}

        for feature in (
            GATE_FEATURE_NAMES
        ):

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
            label
        ] = centroid

    return {
        "scaling":
            scaling,

        "centroids":
            centroids,
    }


def predict_benefit(
    *,
    features: dict,
    model: dict,
) -> tuple[
    bool,
    float,
]:

    distances = {}

    for label in [
        0,
        1,
    ]:

        squared = 0.0

        centroid = model[
            "centroids"
        ][
            label
        ]

        for feature in (
            GATE_FEATURE_NAMES
        ):

            (
                mean_value,
                std_value,
            ) = model[
                "scaling"
            ][
                feature
            ]

            standardized = (
                (
                    features[
                        feature
                    ]
                    - mean_value
                )
                / std_value
            )

            difference = (
                standardized
                - centroid[
                    feature
                ]
            )

            squared += (
                difference ** 2
            )

        distances[
            label
        ] = math.sqrt(
            squared
        )

    similarities = {
        label:
            math.exp(
                -distance
            )
        for label, distance
        in distances.items()
    }

    total = sum(
        similarities.values()
    )

    p_beneficial = (
        similarities[1]
        / total
    )

    return (
        p_beneficial >= 0.50,
        p_beneficial,
    )


def build_gate_training_rows(
    *,
    trajectories: list[dict],
    uniform_model: dict,
    event_model: dict,
    evidence_time: int,
) -> list[dict]:

    rows = []

    for item in trajectories:

        uniform_row = (
            build_representation(
                item=item,
                evidence_time=evidence_time,
                mode="uniform",
            )
        )

        event_row = (
            build_representation(
                item=item,
                evidence_time=evidence_time,
                mode="candidate_event",
            )
        )

        uniform_result = (
            infer_epistemic(
                row=uniform_row,
                model=uniform_model,
            )
        )

        event_result = (
            infer_epistemic(
                row=event_row,
                model=event_model,
            )
        )

        features = gate_features(
            uniform_row=uniform_row,
            event_row=event_row,
            evidence_time=evidence_time,
        )

        beneficial = (
            event_result[
                "marginal_mae"
            ]
            < uniform_result[
                "marginal_mae"
            ]
        )

        rows.append(
            {
                **features,

                "beneficial":
                    beneficial,

                "uniform_mae":
                    uniform_result[
                        "marginal_mae"
                    ],

                "event_mae":
                    event_result[
                        "marginal_mae"
                    ],
            }
        )

    return rows


def score_acceptance_threshold(
    trajectories: list[dict],
    *,
    evidence_time: int,
) -> float:

    scores = []

    for item in trajectories:

        (
            detected_time,
            trigger_score,
        ) = detect_candidate(
            item=item,
            evidence_time=evidence_time,
        )

        if detected_time is not None:

            scores.append(
                float(
                    trigger_score
                )
            )

    return quantile(
        scores,
        SCORE_GATE_QUANTILE,
    )


def evaluate_test(
    *,
    item: dict,
    evidence_time: int,
    uniform_model: dict,
    event_model: dict,
    oracle_model: dict,
    benefit_model: dict,
    score_threshold: float,
) -> list[dict]:

    uniform_row = (
        build_representation(
            item=item,
            evidence_time=evidence_time,
            mode="uniform",
        )
    )

    event_row = (
        build_representation(
            item=item,
            evidence_time=evidence_time,
            mode="candidate_event",
        )
    )

    oracle_row = (
        build_representation(
            item=item,
            evidence_time=evidence_time,
            mode="oracle_event",
        )
    )

    uniform_result = infer_epistemic(
        row=uniform_row,
        model=uniform_model,
    )

    event_result = infer_epistemic(
        row=event_row,
        model=event_model,
    )

    oracle_result = infer_epistemic(
        row=oracle_row,
        model=oracle_model,
    )

    features = gate_features(
        uniform_row=uniform_row,
        event_row=event_row,
        evidence_time=evidence_time,
    )

    (
        predicted_benefit,
        p_beneficial,
    ) = predict_benefit(
        features=features,
        model=benefit_model,
    )

    candidate_exists = bool(
        event_row[
            "candidate_exists"
        ]
    )

    score_gate_accept = (
        candidate_exists
        and
        float(
            event_row[
                "trigger_score"
            ]
        )
        >= score_threshold
    )

    benefit_gate_accept = (
        candidate_exists
        and
        predicted_benefit
    )

    oracle_benefit_accept = (
        candidate_exists
        and
        event_result[
            "marginal_mae"
        ]
        < uniform_result[
            "marginal_mae"
        ]
    )

    schemes = {
        "uniform":
            (
                False,
                uniform_result,
            ),

        "oracle_event":
            (
                True,
                oracle_result,
            ),

        "always_candidate":
            (
                candidate_exists,
                (
                    event_result
                    if candidate_exists
                    else uniform_result
                ),
            ),

        "score_gate":
            (
                score_gate_accept,
                (
                    event_result
                    if score_gate_accept
                    else uniform_result
                ),
            ),

        "benefit_gate":
            (
                benefit_gate_accept,
                (
                    event_result
                    if benefit_gate_accept
                    else uniform_result
                ),
            ),

        "oracle_benefit":
            (
                oracle_benefit_accept,
                (
                    event_result
                    if oracle_benefit_accept
                    else uniform_result
                ),
            ),
    }

    rows = []

    for (
        scheme,
        (
            adopted_event_memory,
            result,
        ),
    ) in schemes.items():

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

                "evidence_time":
                    evidence_time,

                "scheme":
                    scheme,

                "candidate_exists":
                    candidate_exists,

                "adopted_event_memory":
                    adopted_event_memory,

                "trigger_score":
                    event_row[
                        "trigger_score"
                    ],

                "score_threshold":
                    score_threshold,

                "predicted_benefit_probability":
                    p_beneficial,

                "true_event_beneficial":
                    oracle_benefit_accept,

                "estimated_p_fail_A":
                    result[
                        "estimated_p_fail_A"
                    ],

                "estimated_p_fail_C":
                    result[
                        "estimated_p_fail_C"
                    ],

                "estimated_p_fail_S":
                    result[
                        "estimated_p_fail_S"
                    ],

                "A_mae":
                    result[
                        "A_mae"
                    ],

                "C_mae":
                    result[
                        "C_mae"
                    ],

                "S_mae":
                    result[
                        "S_mae"
                    ],

                "marginal_mae":
                    result[
                        "marginal_mae"
                    ],
            }
        )

    return rows


def run_experiment() -> list[dict]:

    trajectories = (
        generate_trajectories()
    )

    (
        memory_fit,
        gate_train,
        test,
    ) = split_trajectories(
        trajectories
    )

    output_rows = []

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        initial_uniform_model = (
            fit_memory_model(
                memory_fit,
                evidence_time=evidence_time,
                mode="uniform",
            )
        )

        initial_event_model = (
            fit_memory_model(
                memory_fit,
                evidence_time=evidence_time,
                mode="candidate_event",
            )
        )

        gate_rows = (
            build_gate_training_rows(
                trajectories=gate_train,
                uniform_model=(
                    initial_uniform_model
                ),
                event_model=(
                    initial_event_model
                ),
                evidence_time=(
                    evidence_time
                ),
            )
        )

        benefit_model = (
            fit_benefit_gate(
                gate_rows
            )
        )

        full_training = (
            memory_fit
            + gate_train
        )

        uniform_model = (
            fit_memory_model(
                full_training,
                evidence_time=evidence_time,
                mode="uniform",
            )
        )

        event_model = (
            fit_memory_model(
                full_training,
                evidence_time=evidence_time,
                mode="candidate_event",
            )
        )

        oracle_model = (
            fit_memory_model(
                full_training,
                evidence_time=evidence_time,
                mode="oracle_event",
            )
        )

        score_threshold = (
            score_acceptance_threshold(
                full_training,
                evidence_time=(
                    evidence_time
                ),
            )
        )

        for item in test:

            output_rows.extend(
                evaluate_test(
                    item=item,
                    evidence_time=(
                        evidence_time
                    ),
                    uniform_model=(
                        uniform_model
                    ),
                    event_model=(
                        event_model
                    ),
                    oracle_model=(
                        oracle_model
                    ),
                    benefit_model=(
                        benefit_model
                    ),
                    score_threshold=(
                        score_threshold
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
        "BENEFIT-AWARE EPISTEMIC MEMORY GATING"
    )

    print("=" * 126)

    schemes = [
        "uniform",
        "oracle_event",
        "always_candidate",
        "score_gate",
        "benefit_gate",
        "oracle_benefit",
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
                for row
                in group
            )

            adoption = (
                sum(
                    row[
                        "adopted_event_memory"
                    ]
                    == "True"
                    for row
                    in group
                )
                / len(
                    group
                )
            )

            print(
                f"  {scheme:<18}"
                f"MAE="
                f"{mae:.4f} "
                f"adopt="
                f"{adoption:.3%}"
            )

        gate_group = [
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
                == "benefit_gate"
            )
        ]

        correct = sum(
            (
                row[
                    "adopted_event_memory"
                ]
                == "True"
            )
            ==
            (
                row[
                    "true_event_beneficial"
                ]
                == "True"
            )
            for row in gate_group
        ) / len(
            gate_group
        )

        print(
            f"  benefit decision accuracy="
            f"{correct:.3%}"
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