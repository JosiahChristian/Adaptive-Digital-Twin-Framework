import csv
import statistics
from collections import defaultdict
from pathlib import Path

from experiments.adaptive_epistemic_memory_release_control import (
    ADOPTION_THRESHOLD,
    EVIDENCE_TIMES,
    build_release_training_rows,
    evaluate_trajectory,
    fit_binary_centroid_model,
    fit_models,
)

from experiments.benefit_aware_epistemic_memory_gating import (
    build_representation,
    generate_trajectories,
    gate_features,
    infer_epistemic,
    predict_benefit,
    split_trajectories,
)

from experiments.adaptive_epistemic_memory_release_control import (
    predict_release,
)


OUTPUT_PATH = Path(
    "results/"
    "persistent_adaptive_epistemic_memory_release_control.csv"
)


RELEASE_CONFIRMATION_LEVELS = [
    1,
    2,
    3,
]


def evaluate_persistent_release(
    *,
    item: dict,
    models: dict,
    release_model: dict,
    confirmation_required: int,
) -> list[dict]:

    rows = []

    memory_active = False

    release_evidence_run = 0

    release_count = 0
    transition_count = 0

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

        previous_memory = (
            memory_active
        )

        if not memory_active:

            release_evidence_run = 0

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
            ):

                release_evidence_run += 1

            elif predicted_release:

                release_evidence_run += 1

            else:

                release_evidence_run = 0

            if (
                release_evidence_run
                >= confirmation_required
            ):

                memory_active = False

                release_count += 1

                release_evidence_run = 0

        if (
            memory_active
            != previous_memory
        ):

            transition_count += 1

        selected_result = (
            event_result
            if memory_active
            else uniform_result
        )

        true_release_beneficial = (
            uniform_result[
                "marginal_mae"
            ]
            < event_result[
                "marginal_mae"
            ]
        )

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

        oracle_benefit_result = (
            event_result
            if oracle_benefit
            else uniform_result
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
                    (
                        "persistent_release_"
                        f"{confirmation_required}"
                    ),

                "confirmation_required":
                    confirmation_required,

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

                "release_evidence_run":
                    release_evidence_run,

                "adopted_event_memory":
                    memory_active,

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

                "oracle_event_mae":
                    oracle_result[
                        "marginal_mae"
                    ],

                "oracle_benefit_mae":
                    oracle_benefit_result[
                        "marginal_mae"
                    ],
            }
        )

    return rows


def evaluate_fixed_reference(
    *,
    item: dict,
    models: dict,
) -> list[dict]:

    return evaluate_trajectory(
        item=item,
        models=models,
        release_model=None,
    )


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

        for confirmation_required in (
            RELEASE_CONFIRMATION_LEVELS
        ):

            rows.extend(
                evaluate_persistent_release(
                    item=item,
                    models=models,
                    release_model=release_model,
                    confirmation_required=(
                        confirmation_required
                    ),
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
        "PERSISTENT ADAPTIVE "
        "EPISTEMIC MEMORY-RELEASE CONTROL"
    )

    print("=" * 118)

    groups = defaultdict(list)

    for row in rows:

        key = (
            int(
                row[
                    "evidence_time"
                ]
            ),
            int(
                row[
                    "confirmation_required"
                ]
            ),
        )

        groups[
            key
        ].append(
            row
        )

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        print()
        print(
            f"t={evidence_time}"
        )

        for confirmation_required in (
            RELEASE_CONFIRMATION_LEVELS
        ):

            group = groups[
                (
                    evidence_time,
                    confirmation_required,
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
                row[
                    "adopted_event_memory"
                ]
                is True
                for row in group
            ) / len(
                group
            )

            print(
                f"  confirm="
                f"{confirmation_required} "
                f"MAE="
                f"{mae:.4f} "
                f"adopt="
                f"{adoption:.3%}"
            )

    print()
    print(
        "FINAL PERSISTENCE SUMMARY"
    )

    final_time = max(
        EVIDENCE_TIMES
    )

    for confirmation_required in (
        RELEASE_CONFIRMATION_LEVELS
    ):

        group = groups[
            (
                final_time,
                confirmation_required,
            )
        ]

        mean_releases = (
            statistics.mean(
                int(
                    row[
                        "release_count"
                    ]
                )
                for row in group
            )
        )

        mean_transitions = (
            statistics.mean(
                int(
                    row[
                        "transition_count"
                    ]
                )
                for row in group
            )
        )

        print(
            f"  confirm="
            f"{confirmation_required} "
            f"mean releases="
            f"{mean_releases:.3f} "
            f"mean transitions="
            f"{mean_transitions:.3f}"
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