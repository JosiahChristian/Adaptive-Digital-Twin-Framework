import csv
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
)

from experiments.online_failure_state_conditioned_estimator_control import (
    CONDITIONS,
    baseline_control,
    create_estimator,
    failure_aware_control,
    recovery_time,
    rmse,
)


REFERENCE_PATH = Path(
    "results/criterion_failure_decomposition.csv"
)

OUTPUT_PATH = Path(
    "results/sequential_epistemic_inference_control.csv"
)


EVIDENCE_BUDGETS = [
    5,
    10,
    20,
]

SEQUENCE_REPLICATES = 100

RANDOM_SEED = 40040

BASE_TRAJECTORY_SEED = 400000


def load_reference_rows() -> list[dict]:

    with REFERENCE_PATH.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def group_reference_rows(
    rows: list[dict],
) -> dict[str, list[dict]]:

    groups = defaultdict(list)

    for row in rows:

        groups[
            row["condition"]
        ].append(
            row
        )

    return groups


def epistemic_marginals(
    rows: list[dict],
) -> dict:

    total = len(rows)

    p_fail_a = (
        sum(
            row["fail_A"] == "True"
            for row in rows
        )
        / total
    )

    p_fail_c = (
        sum(
            row["fail_C"] == "True"
            for row in rows
        )
        / total
    )

    p_fail_s = (
        sum(
            row["fail_S"] == "True"
            for row in rows
        )
        / total
    )

    p_pass = (
        sum(
            row[
                "evidence_sufficient"
            ]
            == "True"
            for row in rows
        )
        / total
    )

    return {
        "p_pass":
            p_pass,

        "p_fail_A":
            p_fail_a,

        "p_fail_C":
            p_fail_c,

        "p_fail_S":
            p_fail_s,
    }


def run_controlled_trajectory(
    *,
    condition: dict,
    seed: int,
    control,
) -> dict:

    random.seed(
        seed
    )

    estimator = create_estimator(
        condition
    )

    true_state = 0.0
    true_a = BASE_TRUE_A

    true_states = []
    state_estimates = []
    parameter_estimates = []
    parameter_updates = []
    nis_values = []

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

        result = estimator.controlled_step(
            control_input=PROCESS_INPUT,
            measurement=measurement,
            control=control,
        )

        true_states.append(
            true_state
        )

        state_estimates.append(
            result[
                "state_estimate"
            ]
        )

        parameter_estimates.append(
            result[
                "parameter_estimate"
            ]
        )

        parameter_updates.append(
            result[
                "parameter_update"
            ]
        )

        nis_values.append(
            result[
                "normalized_innovation_squared"
            ]
        )

    target_parameters = [
        (
            BASE_TRUE_A
            if (
                condition[
                    "changed_true_a"
                ]
                is None
                or step < EVENT_STEP
            )
            else condition[
                "changed_true_a"
            ]
        )
        for step in range(
            STEPS
        )
    ]

    state_errors = [
        estimate - truth
        for estimate, truth in zip(
            state_estimates,
            true_states,
        )
    ]

    parameter_errors = [
        estimate - target
        for estimate, target in zip(
            parameter_estimates,
            target_parameters,
        )
    ]

    post_state_errors = (
        state_errors[
            EVENT_STEP:
        ]
    )

    post_parameter_errors = (
        parameter_errors[
            EVENT_STEP:
        ]
    )

    rec_time = recovery_time(
        post_parameter_errors
    )

    return {
        "post_event_state_rmse":
            rmse(
                post_state_errors
            ),

        "post_event_parameter_rmse":
            rmse(
                post_parameter_errors
            ),

        "final_parameter_error":
            abs(
                parameter_errors[-1]
            ),

        "cumulative_abs_parameter_update":
            sum(
                abs(update)
                for update
                in parameter_updates
            ),

        "mean_post_event_nis":
            statistics.mean(
                nis_values[
                    EVENT_STEP:
                ]
            ),

        "recovered":
            rec_time is not None,

        "recovery_time":
            (
                rec_time
                if rec_time is not None
                else ""
            ),
    }


def run_experiment() -> list[dict]:

    reference_rows = (
        load_reference_rows()
    )

    reference_groups = (
        group_reference_rows(
            reference_rows
        )
    )

    rng = random.Random(
        RANDOM_SEED
    )

    output_rows = []

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

        reference_group = (
            reference_groups[
                reference_condition
            ]
        )

        reference_epistemic_state = (
            epistemic_marginals(
                reference_group
            )
        )

        reference_control = (
            failure_aware_control(
                reference_epistemic_state
            )
        )

        for replicate in range(
            SEQUENCE_REPLICATES
        ):

            sequence = list(
                reference_group
            )

            rng.shuffle(
                sequence
            )

            trajectory_seed = (
                BASE_TRAJECTORY_SEED
                + condition_index
                * SEQUENCE_REPLICATES
                + replicate
            )

            for evidence_budget in (
                EVIDENCE_BUDGETS
            ):

                observed = sequence[
                    :evidence_budget
                ]

                inferred_epistemic_state = (
                    epistemic_marginals(
                        observed
                    )
                )

                inferred_control = (
                    failure_aware_control(
                        inferred_epistemic_state
                    )
                )

                policy_controls = {
                    "baseline":
                        baseline_control(),

                    "reference_aware":
                        reference_control,

                    "inferred_failure_aware":
                        inferred_control,
                }

                for (
                    policy,
                    control,
                ) in (
                    policy_controls.items()
                ):

                    dynamics = (
                        run_controlled_trajectory(
                            condition=condition,
                            seed=trajectory_seed,
                            control=control,
                        )
                    )

                    output_rows.append(
                        {
                            "condition":
                                condition[
                                    "name"
                                ],

                            "true_class":
                                condition[
                                    "class"
                                ],

                            "sequence_replicate":
                                replicate,

                            "evidence_budget":
                                evidence_budget,

                            "policy":
                                policy,

                            "selected_action":
                                control.action_name,

                            "reference_action":
                                reference_control.action_name,

                            "action_matches_reference":
                                (
                                    control.action_name
                                    == reference_control.action_name
                                ),

                            "parameter_learning_scale":
                                control.parameter_learning_scale,

                            "process_uncertainty_scale":
                                control.process_uncertainty_scale,

                            "allow_commitment":
                                control.allow_commitment,

                            "allow_structural_intervention":
                                control.allow_structural_intervention,

                            "estimated_p_pass":
                                inferred_epistemic_state[
                                    "p_pass"
                                ],

                            "estimated_p_fail_A":
                                inferred_epistemic_state[
                                    "p_fail_A"
                                ],

                            "estimated_p_fail_C":
                                inferred_epistemic_state[
                                    "p_fail_C"
                                ],

                            "estimated_p_fail_S":
                                inferred_epistemic_state[
                                    "p_fail_S"
                                ],

                            "reference_p_pass":
                                reference_epistemic_state[
                                    "p_pass"
                                ],

                            "reference_p_fail_A":
                                reference_epistemic_state[
                                    "p_fail_A"
                                ],

                            "reference_p_fail_C":
                                reference_epistemic_state[
                                    "p_fail_C"
                                ],

                            "reference_p_fail_S":
                                reference_epistemic_state[
                                    "p_fail_S"
                                ],

                            **dynamics,
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

    print("=" * 126)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "SEQUENTIAL EPISTEMIC INFERENCE CONTROL"
    )

    print("=" * 126)

    for evidence_budget in (
        EVIDENCE_BUDGETS
    ):

        print()
        print(
            f"n={evidence_budget}"
        )

        for policy in [
            "baseline",
            "reference_aware",
            "inferred_failure_aware",
        ]:

            group = [
                row
                for row in rows
                if (
                    int(
                        row[
                            "evidence_budget"
                        ]
                    )
                    == evidence_budget
                    and
                    row[
                        "policy"
                    ]
                    == policy
                )
            ]

            state_rmse = (
                statistics.mean(
                    float(
                        row[
                            "post_event_state_rmse"
                        ]
                    )
                    for row in group
                )
            )

            parameter_rmse = (
                statistics.mean(
                    float(
                        row[
                            "post_event_parameter_rmse"
                        ]
                    )
                    for row in group
                )
            )

            recovery = (
                sum(
                    row[
                        "recovered"
                    ]
                    for row in group
                )
                / len(group)
            )

            print(
                f"  {policy:<24}"
                f"state_rmse="
                f"{state_rmse:.4f} "
                f"param_rmse="
                f"{parameter_rmse:.4f} "
                f"recovery="
                f"{recovery:.3%}"
            )

        inferred_group = [
            row
            for row in rows
            if (
                int(
                    row[
                        "evidence_budget"
                    ]
                )
                == evidence_budget
                and
                row[
                    "policy"
                ]
                == "inferred_failure_aware"
            )
        ]

        action_match = (
            sum(
                row[
                    "action_matches_reference"
                ]
                for row in inferred_group
            )
            / len(
                inferred_group
            )
        )

        print(
            f"  inferred action match="
            f"{action_match:.3%}"
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