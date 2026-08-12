import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

from experiments.adaptive_epistemic_memory_release_control import (
    ADOPTION_THRESHOLD,
    EVIDENCE_TIMES,
    build_release_training_rows,
    fit_binary_centroid_model,
    fit_models,
    predict_release,
)

from experiments.benefit_aware_epistemic_memory_gating import (
    build_representation,
    generate_trajectories,
    gate_features,
    infer_epistemic,
    predict_benefit,
    split_trajectories,
)


OUTPUT_PATH = Path(
    "results/adaptive_release_persistence_policy.csv"
)


PERSISTENCE_LEVELS = [
    1,
    2,
    3,
]


PERSISTENCE_FEATURE_NAMES = [
    "benefit_probability",
    "release_probability",
    "anchor_age",
    "trigger_score",
    "feature_distance",
    "current_mismatch_indicator",
    "current_parameter_estimate",
]


TRANSITION_PENALTY = 0.0010
RELEASE_PENALTY = 0.0010


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


def fit_multiclass_centroid_model(
    rows: list[dict],
) -> dict:

    scaling = {}

    for feature in (
        PERSISTENCE_FEATURE_NAMES
    ):

        scaling[
            feature
        ] = standardize(
            [
                float(
                    row[
                        feature
                    ]
                )
                for row in rows
            ]
        )

    groups = defaultdict(list)

    for row in rows:

        groups[
            int(
                row[
                    "best_persistence"
                ]
            )
        ].append(
            row
        )

    centroids = {}

    for label in (
        PERSISTENCE_LEVELS
    ):

        group = groups[
            label
        ]

        if not group:
            continue

        centroid = {}

        for feature in (
            PERSISTENCE_FEATURE_NAMES
        ):

            feature_mean = (
                statistics.mean(
                    float(
                        row[
                            feature
                        ]
                    )
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


def predict_persistence(
    *,
    features: dict,
    model: dict,
) -> tuple[
    int,
    dict,
]:

    distances = {}

    for label, centroid in (
        model[
            "centroids"
        ].items()
    ):

        squared = 0.0

        for feature in (
            PERSISTENCE_FEATURE_NAMES
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
                    float(
                        features[
                            feature
                        ]
                    )
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

    selected = min(
        distances,
        key=distances.get,
    )

    return (
        int(
            selected
        ),
        distances,
    )


def build_models(
    *,
    memory_fit: list[dict],
    gate_train: list[dict],
) -> tuple[
    dict,
    dict,
]:

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

    return (
        models,
        release_model,
    )


def decision_context(
    *,
    item: dict,
    evidence_time: int,
    model_set: dict,
    release_model: dict,
) -> dict:

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
        _,
        p_beneficial,
    ) = predict_benefit(
        features=benefit_features,
        model=model_set[
            "benefit_model"
        ],
    )

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

    return {
        "candidate_exists":
            bool(
                event_row[
                    "candidate_exists"
                ]
            ),

        "uniform_result":
            uniform_result,

        "event_result":
            event_result,

        "predicted_release":
            predicted_release,

        "benefit_probability":
            p_beneficial,

        "release_probability":
            p_release,

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


def simulate_fixed_persistence_from_index(
    *,
    contexts: list[dict],
    start_index: int,
    initial_memory: bool,
    initial_release_run: int,
    persistence: int,
) -> float:

    memory_active = (
        initial_memory
    )

    release_run = (
        initial_release_run
    )

    total_loss = 0.0

    for index in range(
        start_index,
        len(
            contexts
        ),
    ):

        context = contexts[
            index
        ]

        candidate_exists = (
            context[
                "candidate_exists"
            ]
        )

        p_beneficial = (
            context[
                "benefit_probability"
            ]
        )

        predicted_release = (
            context[
                "predicted_release"
            ]
        )

        previous_memory = (
            memory_active
        )

        was_active = (
            memory_active
        )

        released_this_step = False

        if not was_active:

            release_run = 0

            if (
                candidate_exists
                and
                p_beneficial
                >= ADOPTION_THRESHOLD
            ):

                memory_active = True

        else:

            if (
                not candidate_exists
                or
                predicted_release
            ):

                release_run += 1

            else:

                release_run = 0

            if (
                release_run
                >= persistence
            ):

                memory_active = False
                release_run = 0
                released_this_step = True

        selected_result = (
            context[
                "event_result"
            ]
            if memory_active
            else context[
                "uniform_result"
            ]
        )

        total_loss += float(
            selected_result[
                "marginal_mae"
            ]
        )

        if (
            memory_active
            != previous_memory
        ):

            total_loss += (
                TRANSITION_PENALTY
            )

        if released_this_step:

            total_loss += (
                RELEASE_PENALTY
            )

    return total_loss


def build_training_contexts(
    *,
    trajectories: list[dict],
    models: dict,
    release_model: dict,
) -> list[dict]:

    rows = []

    for item in trajectories:

        contexts = []

        for evidence_time in (
            EVIDENCE_TIMES
        ):

            contexts.append(
                decision_context(
                    item=item,
                    evidence_time=evidence_time,
                    model_set=models[
                        evidence_time
                    ],
                    release_model=release_model,
                )
            )

        memory_active = False
        release_run = 0

        for index, evidence_time in enumerate(
            EVIDENCE_TIMES
        ):

            context = contexts[
                index
            ]

            candidate_exists = (
                context[
                    "candidate_exists"
                ]
            )

            p_beneficial = (
                context[
                    "benefit_probability"
                ]
            )

            was_active = (
                memory_active
            )

            if not was_active:

                release_run = 0

                if (
                    candidate_exists
                    and
                    p_beneficial
                    >= ADOPTION_THRESHOLD
                ):

                    memory_active = True

            if memory_active:

                candidate_losses = {}

                for persistence in (
                    PERSISTENCE_LEVELS
                ):

                    candidate_losses[
                        persistence
                    ] = (
                        simulate_fixed_persistence_from_index(
                            contexts=contexts,
                            start_index=index,
                            initial_memory=memory_active,
                            initial_release_run=release_run,
                            persistence=persistence,
                        )
                    )

                best_persistence = min(
                    candidate_losses,
                    key=lambda k: (
                        candidate_losses[
                            k
                        ],
                        k,
                    ),
                )

                rows.append(
                    {
                        "benefit_probability":
                            context[
                                "benefit_probability"
                            ],

                        "release_probability":
                            context[
                                "release_probability"
                            ],

                        "anchor_age":
                            context[
                                "anchor_age"
                            ],

                        "trigger_score":
                            context[
                                "trigger_score"
                            ],

                        "feature_distance":
                            context[
                                "feature_distance"
                            ],

                        "current_mismatch_indicator":
                            context[
                                "current_mismatch_indicator"
                            ],

                        "current_parameter_estimate":
                            context[
                                "current_parameter_estimate"
                            ],

                        "best_persistence":
                            best_persistence,

                        "loss_k1":
                            candidate_losses[
                                1
                            ],

                        "loss_k2":
                            candidate_losses[
                                2
                            ],

                        "loss_k3":
                            candidate_losses[
                                3
                            ],
                    }
                )

            if (
                was_active
                and
                memory_active
            ):

                if (
                    not candidate_exists
                    or
                    context[
                        "predicted_release"
                    ]
                ):

                    release_run += 1

                else:

                    release_run = 0

                if release_run >= 1:

                    memory_active = False
                    release_run = 0

    return rows


def evaluate_policy(
    *,
    item: dict,
    models: dict,
    release_model: dict,
    persistence_model: dict,
) -> list[dict]:

    rows = []

    memory_active = False
    release_run = 0

    release_count = 0
    transition_count = 0

    selected_persistence = 1

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        context = decision_context(
            item=item,
            evidence_time=evidence_time,
            model_set=models[
                evidence_time
            ],
            release_model=release_model,
        )

        candidate_exists = (
            context[
                "candidate_exists"
            ]
        )

        previous_memory = (
            memory_active
        )

        was_active = (
            memory_active
        )

        persistence_distances = {}

        if not was_active:

            release_run = 0

            if (
                candidate_exists
                and
                context[
                    "benefit_probability"
                ]
                >= ADOPTION_THRESHOLD
            ):

                memory_active = True

                policy_features = {
                    feature:
                        context[
                            feature
                        ]
                    for feature in (
                        PERSISTENCE_FEATURE_NAMES
                    )
                }

                (
                    selected_persistence,
                    persistence_distances,
                ) = predict_persistence(
                    features=policy_features,
                    model=persistence_model,
                )

        else:

            policy_features = {
                feature:
                    context[
                        feature
                    ]
                for feature in (
                    PERSISTENCE_FEATURE_NAMES
                )
            }

            (
                selected_persistence,
                persistence_distances,
            ) = predict_persistence(
                features=policy_features,
                model=persistence_model,
            )

            if (
                not candidate_exists
                or
                context[
                    "predicted_release"
                ]
            ):

                release_run += 1

            else:

                release_run = 0

            if (
                release_run
                >= selected_persistence
            ):

                memory_active = False
                release_count += 1
                release_run = 0

        if (
            memory_active
            != previous_memory
        ):

            transition_count += 1

        selected_result = (
            context[
                "event_result"
            ]
            if memory_active
            else context[
                "uniform_result"
            ]
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

                "evidence_time":
                    evidence_time,

                "scheme":
                    "adaptive_persistence",

                "candidate_exists":
                    candidate_exists,

                "benefit_probability":
                    context[
                        "benefit_probability"
                    ],

                "release_probability":
                    context[
                        "release_probability"
                    ],

                "predicted_release":
                    context[
                        "predicted_release"
                    ],

                "selected_persistence":
                    (
                        selected_persistence
                        if memory_active
                        or previous_memory
                        else ""
                    ),

                "persistence_distance_1":
                    persistence_distances.get(
                        1,
                        "",
                    ),

                "persistence_distance_2":
                    persistence_distances.get(
                        2,
                        "",
                    ),

                "persistence_distance_3":
                    persistence_distances.get(
                        3,
                        "",
                    ),

                "adopted_event_memory":
                    memory_active,

                "release_evidence_run":
                    release_run,

                "release_count":
                    release_count,

                "transition_count":
                    transition_count,

                "estimated_p_fail_A":
                    selected_result[
                        "estimated_p_fail_A"
                    ],

                "estimated_p_fail_C":
                    selected_result[
                        "estimated_p_fail_C"
                    ],

                "estimated_p_fail_S":
                    selected_result[
                        "estimated_p_fail_S"
                    ],

                "A_mae":
                    selected_result[
                        "A_mae"
                    ],

                "C_mae":
                    selected_result[
                        "C_mae"
                    ],

                "S_mae":
                    selected_result[
                        "S_mae"
                    ],

                "marginal_mae":
                    selected_result[
                        "marginal_mae"
                    ],
            }
        )

    return rows


def evaluate_fixed_policy(
    *,
    item: dict,
    models: dict,
    release_model: dict,
    persistence: int,
) -> list[dict]:

    rows = []

    memory_active = False
    release_run = 0

    release_count = 0
    transition_count = 0

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        context = decision_context(
            item=item,
            evidence_time=evidence_time,
            model_set=models[
                evidence_time
            ],
            release_model=release_model,
        )

        candidate_exists = (
            context[
                "candidate_exists"
            ]
        )

        previous_memory = (
            memory_active
        )

        was_active = (
            memory_active
        )

        if not was_active:

            release_run = 0

            if (
                candidate_exists
                and
                context[
                    "benefit_probability"
                ]
                >= ADOPTION_THRESHOLD
            ):

                memory_active = True

        else:

            if (
                not candidate_exists
                or
                context[
                    "predicted_release"
                ]
            ):

                release_run += 1

            else:

                release_run = 0

            if (
                release_run
                >= persistence
            ):

                memory_active = False
                release_count += 1
                release_run = 0

        if (
            memory_active
            != previous_memory
        ):

            transition_count += 1

        selected_result = (
            context[
                "event_result"
            ]
            if memory_active
            else context[
                "uniform_result"
            ]
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

                "evidence_time":
                    evidence_time,

                "scheme":
                    f"fixed_{persistence}",

                "candidate_exists":
                    candidate_exists,

                "benefit_probability":
                    context[
                        "benefit_probability"
                    ],

                "release_probability":
                    context[
                        "release_probability"
                    ],

                "predicted_release":
                    context[
                        "predicted_release"
                    ],

                "selected_persistence":
                    persistence,

                "persistence_distance_1":
                    "",

                "persistence_distance_2":
                    "",

                "persistence_distance_3":
                    "",

                "adopted_event_memory":
                    memory_active,

                "release_evidence_run":
                    release_run,

                "release_count":
                    release_count,

                "transition_count":
                    transition_count,

                "estimated_p_fail_A":
                    selected_result[
                        "estimated_p_fail_A"
                    ],

                "estimated_p_fail_C":
                    selected_result[
                        "estimated_p_fail_C"
                    ],

                "estimated_p_fail_S":
                    selected_result[
                        "estimated_p_fail_S"
                    ],

                "A_mae":
                    selected_result[
                        "A_mae"
                    ],

                "C_mae":
                    selected_result[
                        "C_mae"
                    ],

                "S_mae":
                    selected_result[
                        "S_mae"
                    ],

                "marginal_mae":
                    selected_result[
                        "marginal_mae"
                    ],
            }
        )

    return rows


def run_experiment() -> tuple[
    list[dict],
    list[dict],
]:

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

    (
        models,
        release_model,
    ) = build_models(
        memory_fit=memory_fit,
        gate_train=gate_train,
    )

    persistence_training_rows = (
        build_training_contexts(
            trajectories=gate_train,
            models=models,
            release_model=release_model,
        )
    )

    persistence_model = (
        fit_multiclass_centroid_model(
            persistence_training_rows
        )
    )

    rows = []

    for item in test:

        for persistence in (
            PERSISTENCE_LEVELS
        ):

            rows.extend(
                evaluate_fixed_policy(
                    item=item,
                    models=models,
                    release_model=release_model,
                    persistence=persistence,
                )
            )

        rows.extend(
            evaluate_policy(
                item=item,
                models=models,
                release_model=release_model,
                persistence_model=persistence_model,
            )
        )

    return (
        rows,
        persistence_training_rows,
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
    training_rows: list[dict],
) -> None:

    print("=" * 126)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "ADAPTIVE RELEASE-PERSISTENCE POLICY"
    )

    print("=" * 126)

    label_counts = defaultdict(
        int
    )

    for row in training_rows:

        label_counts[
            int(
                row[
                    "best_persistence"
                ]
            )
        ] += 1

    print(
        "TRAINING TARGET DISTRIBUTION"
    )

    for persistence in (
        PERSISTENCE_LEVELS
    ):

        print(
            f"  k={persistence}: "
            f"{label_counts[persistence]}"
        )

    schemes = [
        "fixed_1",
        "fixed_2",
        "fixed_3",
        "adaptive_persistence",
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
            ) / len(
                group
            )

            print(
                f"  {scheme:<22}"
                f"MAE={mae:.4f} "
                f"adopt="
                f"{adoption:.3%}"
            )

    adaptive_rows = [
        row
        for row in rows
        if row[
            "scheme"
        ]
        == "adaptive_persistence"
    ]

    selection_counts = defaultdict(
        int
    )

    for row in adaptive_rows:

        value = row[
            "selected_persistence"
        ]

        if value != "":

            selection_counts[
                int(
                    value
                )
            ] += 1

    print()
    print(
        "ADAPTIVE PERSISTENCE SELECTION"
    )

    for persistence in (
        PERSISTENCE_LEVELS
    ):

        print(
            f"  k={persistence}: "
            f"{selection_counts[persistence]}"
        )

    final_rows = [
        row
        for row in adaptive_rows
        if int(
            row[
                "evidence_time"
            ]
        )
        == 100
    ]

    mean_releases = (
        statistics.mean(
            int(
                row[
                    "release_count"
                ]
            )
            for row in final_rows
        )
    )

    mean_transitions = (
        statistics.mean(
            int(
                row[
                    "transition_count"
                ]
            )
            for row in final_rows
        )
    )

    print()
    print(
        "ADAPTIVE FINAL SUMMARY"
    )

    print(
        f"mean releases="
        f"{mean_releases:.3f}"
    )

    print(
        f"mean transitions="
        f"{mean_transitions:.3f}"
    )

    print("=" * 126)


def main() -> None:

    (
        rows,
        training_rows,
    ) = run_experiment()

    save_results(
        rows
    )

    print_summary(
        rows,
        training_rows,
    )

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()