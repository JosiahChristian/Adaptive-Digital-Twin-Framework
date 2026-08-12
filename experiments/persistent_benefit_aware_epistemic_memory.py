import csv
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
    "results/"
    "persistent_benefit_aware_epistemic_memory.csv"
)

EVIDENCE_TIMES = [
    60,
    70,
    80,
    100,
]

ADOPTION_THRESHOLD = 0.55
RELEASE_THRESHOLD = 0.45


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


def evaluate_trajectory(
    *,
    item: dict,
    models: dict,
) -> list[dict]:

    output_rows = []

    persistent_memory = False

    adoption_time = None
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
            model=model_set[
                "benefit_model"
            ],
        )

        candidate_exists = bool(
            event_row[
                "candidate_exists"
            ]
        )

        snapshot_adopt = (
            candidate_exists
            and
            predicted_benefit
        )

        previous_memory = (
            persistent_memory
        )

        if not persistent_memory:

            if (
                candidate_exists
                and
                p_beneficial
                >= ADOPTION_THRESHOLD
            ):

                persistent_memory = True

                if adoption_time is None:
                    adoption_time = (
                        evidence_time
                    )

        else:

            if (
                not candidate_exists
                or
                p_beneficial
                <= RELEASE_THRESHOLD
            ):

                persistent_memory = False
                release_count += 1

        if (
            persistent_memory
            != previous_memory
        ):
            transition_count += 1

        persistent_result = (
            event_result
            if persistent_memory
            else uniform_result
        )

        snapshot_result = (
            event_result
            if snapshot_adopt
            else uniform_result
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

            "snapshot_benefit":
                (
                    snapshot_adopt,
                    snapshot_result,
                ),

            "persistent_benefit":
                (
                    persistent_memory,
                    persistent_result,
                ),

            "oracle_benefit":
                (
                    oracle_benefit,
                    oracle_benefit_result,
                ),
        }

        for (
            scheme,
            (
                adopted,
                result,
            ),
        ) in schemes.items():

            output_rows.append(
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

                    "predicted_benefit_probability":
                        p_beneficial,

                    "snapshot_adopt":
                        snapshot_adopt,

                    "persistent_memory":
                        persistent_memory,

                    "adopted_event_memory":
                        adopted,

                    "adoption_time":
                        (
                            adoption_time
                            if adoption_time
                            is not None
                            else ""
                        ),

                    "release_count":
                        release_count,

                    "transition_count":
                        transition_count,

                    "true_event_beneficial":
                        oracle_benefit,

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

    return output_rows


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

    rows = []

    for item in test:

        rows.extend(
            evaluate_trajectory(
                item=item,
                models=models,
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

    print(
        "=" * 110
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PERSISTENT BENEFIT-AWARE "
        "EPISTEMIC MEMORY"
    )

    print(
        "=" * 110
    )

    schemes = [
        "uniform",
        "oracle_event",
        "snapshot_benefit",
        "persistent_benefit",
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

            adoption = sum(
                bool(
                    row[
                        "adopted_event_memory"
                    ]
                )
                for row
                in group
            ) / len(
                group
            )

            print(
                f"  {scheme:<20}"
                f"MAE={mae:.4f} "
                f"adopt="
                f"{adoption:.3%}"
            )

    persistent_rows = [
        row
        for row in rows
        if row[
            "scheme"
        ]
        == "persistent_benefit"
    ]

    final_rows = [
        row
        for row in persistent_rows
        if int(
            row[
                "evidence_time"
            ]
        )
        == max(
            EVIDENCE_TIMES
        )
    ]

    ever_adopted = sum(
        row[
            "adoption_time"
        ]
        != ""
        for row
        in final_rows
    ) / len(
        final_rows
    )

    mean_transitions = (
        statistics.mean(
            int(
                row[
                    "transition_count"
                ]
            )
            for row
            in final_rows
        )
    )

    mean_releases = (
        statistics.mean(
            int(
                row[
                    "release_count"
                ]
            )
            for row
            in final_rows
        )
    )

    adoption_times = [
        int(
            row[
                "adoption_time"
            ]
        )
        for row
        in final_rows
        if row[
            "adoption_time"
        ]
        != ""
    ]

    print()
    print(
        "PERSISTENCE SUMMARY"
    )

    print(
        f"ever adopted="
        f"{ever_adopted:.3%}"
    )

    print(
        f"mean transitions="
        f"{mean_transitions:.3f}"
    )

    print(
        f"mean releases="
        f"{mean_releases:.3f}"
    )

    if adoption_times:

        print(
            "mean first adoption time="
            f"{statistics.mean(adoption_times):.3f}"
        )

    print(
        "=" * 110
    )


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