import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

from experiments.benefit_aware_epistemic_memory_gating import (
    build_gate_training_rows,
    build_representation,
    fit_benefit_gate,
    fit_memory_model,
    gate_features,
    generate_trajectories,
    infer_epistemic,
    predict_benefit,
    split_trajectories,
)


OUTPUT_PATH = Path(
    "results/adaptive_epistemic_memory_release_control.csv"
)


EVIDENCE_TIMES = [
    60,
    70,
    80,
    100,
]


ADOPTION_THRESHOLD = 0.55
FIXED_RELEASE_THRESHOLD = 0.45


RELEASE_FEATURE_NAMES = [
    "benefit_probability",
    "anchor_age",
    "trigger_score",
    "feature_distance",
    "current_mismatch_indicator",
    "current_parameter_estimate",
]


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


def fit_binary_centroid_model(
    rows: list[dict],
) -> dict:

    scaling = {}

    for feature in (
        RELEASE_FEATURE_NAMES
    ):

        scaling[
            feature
        ] = standardize(
            [
                row[feature]
                for row in rows
            ]
        )

    groups = defaultdict(list)

    for row in rows:

        groups[
            int(
                row[
                    "release_beneficial"
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
            RELEASE_FEATURE_NAMES
        ):

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
            label
        ] = centroid

    return {
        "scaling":
            scaling,

        "centroids":
            centroids,
    }


def predict_release(
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
            RELEASE_FEATURE_NAMES
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

    p_release = (
        similarities[1]
        / total
    )

    return (
        p_release >= 0.50,
        p_release,
    )


def fit_models(
    *,
    memory_fit: list[dict],
    gate_train: list[dict],
    evidence_time: int,
) -> dict:

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
            evidence_time=evidence_time,
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

    return {
        "uniform_model":
            uniform_model,

        "event_model":
            event_model,

        "oracle_model":
            oracle_model,

        "benefit_model":
            benefit_model,
    }


def build_release_training_rows(
    *,
    trajectories: list[dict],
    models: dict,
) -> list[dict]:

    rows = []

    for item in trajectories:

        memory_active = False

        for evidence_time in (
            EVIDENCE_TIMES
        ):

            model_set = models[
                evidence_time
            ]

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
                    model=model_set[
                        "uniform_model"
                    ],
                )
            )

            event_result = (
                infer_epistemic(
                    row=event_row,
                    model=model_set[
                        "event_model"
                    ],
                )
            )

            benefit_features = (
                gate_features(
                    uniform_row=uniform_row,
                    event_row=event_row,
                    evidence_time=evidence_time,
                )
            )

            (
                predicted_benefit,
                p_beneficial,
            ) = predict_benefit(
                features=benefit_features,
                model=model_set[
                    "benefit_model"
                ],
            )

            candidate_exists = bool(
                event_row[
                    "candidate_exists"
                ]
            )

            if not memory_active:

                if (
                    candidate_exists
                    and
                    p_beneficial
                    >= ADOPTION_THRESHOLD
                ):

                    memory_active = True

            else:

                release_beneficial = (
                    uniform_result[
                        "marginal_mae"
                    ]
                    < event_result[
                        "marginal_mae"
                    ]
                )

                rows.append(
                    {
                        "benefit_probability":
                            p_beneficial,

                        "anchor_age":
                            benefit_features[
                                "anchor_age"
                            ],

                        "trigger_score":
                            benefit_features[
                                "trigger_score"
                            ],

                        "feature_distance":
                            benefit_features[
                                "feature_distance"
                            ],

                        "current_mismatch_indicator":
                            benefit_features[
                                "current_mismatch_indicator"
                            ],

                        "current_parameter_estimate":
                            benefit_features[
                                "current_parameter_estimate"
                            ],

                        "release_beneficial":
                            release_beneficial,
                    }
                )

    return rows


def evaluate_trajectory(
    *,
    item: dict,
    models: dict,
    release_model: dict,
) -> list[dict]:

    rows = []

    fixed_memory = False
    learned_memory = False

    fixed_transition_count = 0
    learned_transition_count = 0

    fixed_release_count = 0
    learned_release_count = 0

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        model_set = models[
            evidence_time
        ]

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

        uniform_result = (
            infer_epistemic(
                row=uniform_row,
                model=model_set[
                    "uniform_model"
                ],
            )
        )

        event_result = (
            infer_epistemic(
                row=event_row,
                model=model_set[
                    "event_model"
                ],
            )
        )

        oracle_result = (
            infer_epistemic(
                row=oracle_row,
                model=model_set[
                    "oracle_model"
                ],
            )
        )

        benefit_features = (
            gate_features(
                uniform_row=uniform_row,
                event_row=event_row,
                evidence_time=evidence_time,
            )
        )

        (
            predicted_benefit,
            p_beneficial,
        ) = predict_benefit(
            features=benefit_features,
            model=model_set[
                "benefit_model"
            ],
        )

        candidate_exists = bool(
            event_row[
                "candidate_exists"
            ]
        )

        previous_fixed = (
            fixed_memory
        )

        if not fixed_memory:

            if (
                candidate_exists
                and
                p_beneficial
                >= ADOPTION_THRESHOLD
            ):

                fixed_memory = True

        else:

            if (
                not candidate_exists
                or
                p_beneficial
                <= FIXED_RELEASE_THRESHOLD
            ):

                fixed_memory = False
                fixed_release_count += 1

        if fixed_memory != previous_fixed:

            fixed_transition_count += 1

        release_features = {
            "benefit_probability":
                p_beneficial,

            "anchor_age":
                benefit_features[
                    "anchor_age"
                ],

            "trigger_score":
                benefit_features[
                    "trigger_score"
                ],

            "feature_distance":
                benefit_features[
                    "feature_distance"
                ],

            "current_mismatch_indicator":
                benefit_features[
                    "current_mismatch_indicator"
                ],

            "current_parameter_estimate":
                benefit_features[
                    "current_parameter_estimate"
                ],
        }

        (
            predicted_release,
            p_release,
        ) = predict_release(
            features=release_features,
            model=release_model,
        )

        previous_learned = (
            learned_memory
        )

        if not learned_memory:

            if (
                candidate_exists
                and
                p_beneficial
                >= ADOPTION_THRESHOLD
            ):

                learned_memory = True

        else:

            if (
                not candidate_exists
                or
                predicted_release
            ):

                learned_memory = False
                learned_release_count += 1

        if learned_memory != previous_learned:

            learned_transition_count += 1

        oracle_benefit = (
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

            "fixed_release":
                (
                    fixed_memory,
                    (
                        event_result
                        if fixed_memory
                        else uniform_result
                    ),
                ),

            "learned_release":
                (
                    learned_memory,
                    (
                        event_result
                        if learned_memory
                        else uniform_result
                    ),
                ),

            "oracle_benefit":
                (
                    oracle_benefit,
                    (
                        event_result
                        if oracle_benefit
                        else uniform_result
                    ),
                ),
        }

        true_release_beneficial = (
            uniform_result[
                "marginal_mae"
            ]
            < event_result[
                "marginal_mae"
            ]
        )

        for (
            scheme,
            (
                adopted,
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

                    "benefit_probability":
                        p_beneficial,

                    "release_probability":
                        p_release,

                    "predicted_release":
                        predicted_release,

                    "true_release_beneficial":
                        true_release_beneficial,

                    "adopted_event_memory":
                        adopted,

                    "fixed_transition_count":
                        fixed_transition_count,

                    "learned_transition_count":
                        learned_transition_count,

                    "fixed_release_count":
                        fixed_release_count,

                    "learned_release_count":
                        learned_release_count,

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

    models = {}

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        models[
            evidence_time
        ] = fit_models(
            memory_fit=memory_fit,
            gate_train=gate_train,
            evidence_time=evidence_time,
        )

    release_training_rows = (
        build_release_training_rows(
            trajectories=gate_train,
            models=models,
        )
    )

    release_model = (
        fit_binary_centroid_model(
            release_training_rows
        )
    )

    rows = []

    for item in test:

        rows.extend(
            evaluate_trajectory(
                item=item,
                models=models,
                release_model=release_model,
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

    print("=" * 118)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "ADAPTIVE EPISTEMIC MEMORY-RELEASE CONTROL"
    )

    print("=" * 118)

    schemes = [
        "uniform",
        "oracle_event",
        "fixed_release",
        "learned_release",
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
                for row in group
            )

            adoption = sum(
                bool(
                    row[
                        "adopted_event_memory"
                    ]
                )
                for row in group
            ) / len(group)

            print(
                f"  {scheme:<18}"
                f"MAE={mae:.4f} "
                f"adopt="
                f"{adoption:.3%}"
            )

    final_fixed = [
        row
        for row in rows
        if (
            row["scheme"]
            == "fixed_release"
            and
            int(
                row[
                    "evidence_time"
                ]
            )
            == 100
        )
    ]

    final_learned = [
        row
        for row in rows
        if (
            row["scheme"]
            == "learned_release"
            and
            int(
                row[
                    "evidence_time"
                ]
            )
            == 100
        )
    ]

    print()
    print(
        "RELEASE SUMMARY"
    )

    fixed_mean_releases = (
        statistics.mean(
            int(
                row[
                    "fixed_release_count"
                ]
            )
            for row in final_fixed
        )
    )

    learned_mean_releases = (
        statistics.mean(
            int(
                row[
                    "learned_release_count"
                ]
            )
            for row in final_learned
        )
    )

    fixed_mean_transitions = (
        statistics.mean(
            int(
                row[
                    "fixed_transition_count"
                ]
            )
            for row in final_fixed
        )
    )

    learned_mean_transitions = (
        statistics.mean(
            int(
                row[
                    "learned_transition_count"
                ]
            )
            for row in final_learned
        )
    )

    print(
        "fixed mean releases="
        f"{fixed_mean_releases:.3f}"
    )

    print(
        "learned mean releases="
        f"{learned_mean_releases:.3f}"
    )

    print(
        "fixed mean transitions="
        f"{fixed_mean_transitions:.3f}"
    )

    print(
        "learned mean transitions="
        f"{learned_mean_transitions:.3f}"
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