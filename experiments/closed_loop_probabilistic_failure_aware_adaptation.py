import csv
import math
import random
import statistics
from pathlib import Path

from experiments.independent_aggregated_evidence_validation import (
    extract_features,
    run_trajectory,
)

from experiments.mismatch_classification import (
    classify_row,
)


OUTPUT_PATH = Path(
    "results/closed_loop_probabilistic_failure_aware_adaptation.csv"
)


RUNS_PER_CONDITION = 100
BASE_SEED = 37000

EVENT_STEP = 50
STEPS = 100


CONDITIONS = [
    {
        "class": "measurement_noise",
        "name": "measurement_noise_boundary",
        "measurement_noise_std": 0.85,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "process_disturbance",
        "name": "process_disturbance_boundary",
        "measurement_noise_std": 0.50,
        "process_disturbance": 2.70,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "name": "parameter_mismatch_boundary",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.40,
        "changed_true_a": None,
    },
    {
        "class": "structural_change",
        "name": "structural_change_boundary",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": 0.86,
    },
]


POLICY_ACTIONS = {
    "baseline": {
        "adaptation_scale": 1.00,
        "uncertainty_scale": 1.00,
    },

    "generic_uncertainty": {
        "adaptation_scale": 0.25,
        "uncertainty_scale": 1.50,
    },

    "probabilistic_failure_aware": {
        "adaptation_scale": 0.10,
        "uncertainty_scale": 1.25,
    },
}


def rmse(
    values: list[float],
) -> float:

    return math.sqrt(
        sum(
            value ** 2
            for value in values
        )
        / len(values)
    )


def recovery_time(
    errors: list[float],
    *,
    threshold: float,
    start_index: int,
    required_run: int = 5,
) -> int | None:

    run = 0

    for index in range(
        start_index,
        len(errors),
    ):

        if abs(
            errors[index]
        ) <= threshold:

            run += 1

            if run >= required_run:

                return (
                    index
                    - required_run
                    + 1
                    - start_index
                )

        else:
            run = 0

    return None


def evaluate_policy_trajectory(
    *,
    condition: dict,
    seed: int,
    policy_name: str,
) -> dict:

    action = POLICY_ACTIONS[
        policy_name
    ]

    trajectory = run_trajectory(
        condition=condition,
        seed=seed,
    )

    (
        global_features,
        temporal_features,
        adaptation_features,
    ) = extract_features(
        trajectory
    )

    classification = classify_row(
        regime=condition["class"],
        global_row=global_features,
        temporal_row=temporal_features,
        adaptation_row=adaptation_features,
    )

    innovations = trajectory[
        "innovations"
    ]

    parameter_estimates = trajectory[
        "parameter_estimates"
    ]

    parameter_updates = trajectory[
        "parameter_updates"
    ]

    scaled_parameter_updates = [
        update
        * action[
            "adaptation_scale"
        ]
        for update in parameter_updates
    ]

    adjusted_parameter_estimates = []

    estimate = (
        condition[
            "initial_parameter_estimate"
        ]
    )

    for update in scaled_parameter_updates:

        estimate += update

        adjusted_parameter_estimates.append(
            estimate
        )

    if condition[
        "changed_true_a"
    ] is not None:

        target_parameter = (
            condition[
                "changed_true_a"
            ]
        )

    else:

        target_parameter = 0.92

    parameter_errors = [
        estimate_value
        - target_parameter
        for estimate_value
        in adjusted_parameter_estimates
    ]

    post_event_errors = (
        parameter_errors[
            EVENT_STEP:
        ]
    )

    post_event_innovations = (
        innovations[
            EVENT_STEP:
        ]
    )

    state_proxy_errors = [
        innovation
        / math.sqrt(
            action[
                "uncertainty_scale"
            ]
        )
        for innovation
        in post_event_innovations
    ]

    rec_time = recovery_time(
        parameter_errors,
        threshold=0.05,
        start_index=EVENT_STEP,
    )

    return {
        "condition":
            condition["name"],

        "true_class":
            condition["class"],

        "seed":
            seed,

        "policy":
            policy_name,

        "classification_correct":
            classification[
                "correct"
            ],

        "classification_margin":
            float(
                classification[
                    "classification_margin"
                ]
            ),

        "adaptation_scale":
            action[
                "adaptation_scale"
            ],

        "uncertainty_scale":
            action[
                "uncertainty_scale"
            ],

        "post_event_state_proxy_rmse":
            rmse(
                state_proxy_errors
            ),

        "post_event_parameter_rmse":
            rmse(
                post_event_errors
            ),

        "final_parameter_error":
            abs(
                parameter_errors[-1]
            ),

        "cumulative_abs_parameter_update":
            sum(
                abs(update)
                for update
                in scaled_parameter_updates
            ),

        "recovery_time":
            (
                rec_time
                if rec_time is not None
                else ""
            ),

        "recovered":
            rec_time
            is not None,

        "intervened":
            policy_name
            != "baseline",
    }


def run_experiment() -> list[dict]:

    rows = []

    for condition_index, condition in enumerate(
        CONDITIONS
    ):

        for seed_offset in range(
            RUNS_PER_CONDITION
        ):

            seed = (
                BASE_SEED
                + condition_index
                * RUNS_PER_CONDITION
                + seed_offset
            )

            for policy_name in [
                "baseline",
                "generic_uncertainty",
                "probabilistic_failure_aware",
            ]:

                rows.append(
                    evaluate_policy_trajectory(
                        condition=condition,
                        seed=seed,
                        policy_name=policy_name,
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
        "CLOSED-LOOP PROBABILISTIC FAILURE-AWARE ADAPTATION"
    )

    print("=" * 118)

    for policy in [
        "baseline",
        "generic_uncertainty",
        "probabilistic_failure_aware",
    ]:

        group = [
            row
            for row in rows
            if row[
                "policy"
            ]
            == policy
        ]

        mean_state_rmse = statistics.mean(
            float(
                row[
                    "post_event_state_proxy_rmse"
                ]
            )
            for row in group
        )

        mean_parameter_rmse = statistics.mean(
            float(
                row[
                    "post_event_parameter_rmse"
                ]
            )
            for row in group
        )

        mean_final_parameter_error = (
            statistics.mean(
                float(
                    row[
                        "final_parameter_error"
                    ]
                )
                for row in group
            )
        )

        recovery_fraction = (
            sum(
                row[
                    "recovered"
                ]
                for row in group
            )
            / len(group)
        )

        print(
            f"{policy:<30}"
            f"state_rmse="
            f"{mean_state_rmse:.4f} "
            f"parameter_rmse="
            f"{mean_parameter_rmse:.4f} "
            f"final_parameter_error="
            f"{mean_final_parameter_error:.4f} "
            f"recovery="
            f"{recovery_fraction:.3%}"
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