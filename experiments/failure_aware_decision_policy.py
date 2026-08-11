import csv
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
    "results/failure_aware_decision_policy.csv"
)

RUNS_PER_CONDITION = 100

BASE_SEED = 34000


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


def failure_state(
    *,
    classification_correct: bool,
    classification_margin: float,
) -> str:

    fail_a = (
        not classification_correct
    )

    fail_c = (
        classification_margin
        < 0.30
    )

    # At trajectory level we do not observe
    # population selective accuracy directly.
    #
    # Treat a high-confidence incorrect
    # classification as a selective-accuracy
    # failure proxy.
    fail_s = (
        classification_margin
        >= 0.30
        and
        not classification_correct
    )

    if (
        not fail_a
        and
        not fail_c
        and
        not fail_s
    ):
        return "pass"

    if (
        fail_a
        and fail_c
        and fail_s
    ):
        return "A_C_S"

    if fail_a and fail_c:
        return "A_C"

    if fail_a and fail_s:
        return "A_S"

    if fail_c and fail_s:
        return "C_S"

    if fail_a:
        return "A"

    if fail_c:
        return "C"

    if fail_s:
        return "S"

    return "pass"


def generic_policy(
    *,
    failure_mode: str,
) -> dict:

    if failure_mode == "pass":

        return {
            "adaptation_scale": 1.0,
            "uncertainty_scale": 1.0,
            "abstain": False,
        }

    return {
        "adaptation_scale": 0.25,
        "uncertainty_scale": 1.50,
        "abstain": True,
    }


def failure_aware_policy(
    *,
    failure_mode: str,
) -> dict:

    if failure_mode == "pass":

        return {
            "adaptation_scale": 1.0,
            "uncertainty_scale": 1.0,
            "abstain": False,
        }

    if failure_mode == "C":

        return {
            "adaptation_scale": 0.50,
            "uncertainty_scale": 1.15,
            "abstain": True,
        }

    if failure_mode == "A":

        return {
            "adaptation_scale": 0.20,
            "uncertainty_scale": 1.75,
            "abstain": True,
        }

    if failure_mode == "S":

        return {
            "adaptation_scale": 0.10,
            "uncertainty_scale": 1.25,
            "abstain": True,
        }

    if failure_mode in (
        "A_C",
        "A_S",
        "C_S",
    ):

        return {
            "adaptation_scale": 0.10,
            "uncertainty_scale": 2.00,
            "abstain": True,
        }

    return {
        "adaptation_scale": 0.0,
        "uncertainty_scale": 2.50,
        "abstain": True,
    }


def baseline_policy() -> dict:

    return {
        "adaptation_scale": 1.0,
        "uncertainty_scale": 1.0,
        "abstain": False,
    }


def policy_cost(
    *,
    classification_correct: bool,
    failure_mode: str,
    action: dict,
) -> dict:

    adaptation_scale = float(
        action["adaptation_scale"]
    )

    uncertainty_scale = float(
        action["uncertainty_scale"]
    )

    abstain = bool(
        action["abstain"]
    )

    # Proxy costs are intentionally explicit
    # and fixed before comparison.
    incorrect_commitment_cost = (
        1.0
        if (
            not classification_correct
            and not abstain
        )
        else 0.0
    )

    unnecessary_abstention_cost = (
        0.25
        if (
            classification_correct
            and abstain
        )
        else 0.0
    )

    adaptation_exposure = (
        adaptation_scale
        if not classification_correct
        else 0.0
    )

    uncertainty_cost = (
        max(
            0.0,
            uncertainty_scale - 1.0,
        )
        * 0.10
    )

    severe_failure = (
        failure_mode
        in (
            "A_C",
            "A_S",
            "C_S",
            "A_C_S",
        )
    )

    severe_failure_penalty = (
        0.50
        if (
            severe_failure
            and not abstain
        )
        else 0.0
    )

    total_cost = (
        incorrect_commitment_cost
        + unnecessary_abstention_cost
        + adaptation_exposure
        + uncertainty_cost
        + severe_failure_penalty
    )

    return {
        "incorrect_commitment_cost":
            incorrect_commitment_cost,

        "unnecessary_abstention_cost":
            unnecessary_abstention_cost,

        "adaptation_exposure":
            adaptation_exposure,

        "uncertainty_cost":
            uncertainty_cost,

        "severe_failure_penalty":
            severe_failure_penalty,

        "total_policy_cost":
            total_cost,
    }


def evaluate_policy(
    *,
    policy_name: str,
    action: dict,
    condition: dict,
    seed: int,
    classification: dict,
    failure_mode: str,
) -> dict:

    cost = policy_cost(
        classification_correct=(
            classification["correct"]
        ),
        failure_mode=failure_mode,
        action=action,
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
            classification["correct"],

        "classification_margin":
            float(
                classification[
                    "classification_margin"
                ]
            ),

        "failure_mode":
            failure_mode,

        "adaptation_scale":
            action[
                "adaptation_scale"
            ],

        "uncertainty_scale":
            action[
                "uncertainty_scale"
            ],

        "abstain":
            action[
                "abstain"
            ],

        **cost,
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

            mode = failure_state(
                classification_correct=(
                    classification[
                        "correct"
                    ]
                ),
                classification_margin=float(
                    classification[
                        "classification_margin"
                    ]
                ),
            )

            actions = {
                "baseline":
                    baseline_policy(),

                "generic_uncertainty":
                    generic_policy(
                        failure_mode=mode,
                    ),

                "failure_aware":
                    failure_aware_policy(
                        failure_mode=mode,
                    ),
            }

            for (
                policy_name,
                action,
            ) in actions.items():

                rows.append(
                    evaluate_policy(
                        policy_name=(
                            policy_name
                        ),
                        action=action,
                        condition=condition,
                        seed=seed,
                        classification=(
                            classification
                        ),
                        failure_mode=mode,
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
        "FAILURE-AWARE DECISION POLICY"
    )

    print("=" * 118)

    policies = [
        "baseline",
        "generic_uncertainty",
        "failure_aware",
    ]

    for policy in policies:

        group = [
            row
            for row in rows
            if row["policy"] == policy
        ]

        mean_cost = statistics.mean(
            float(
                row["total_policy_cost"]
            )
            for row in group
        )

        mean_incorrect_commitment = (
            statistics.mean(
                float(
                    row[
                        "incorrect_commitment_cost"
                    ]
                )
                for row in group
            )
        )

        mean_adaptation_exposure = (
            statistics.mean(
                float(
                    row[
                        "adaptation_exposure"
                    ]
                )
                for row in group
            )
        )

        print(
            f"{policy:<22}"
            f"mean_cost={mean_cost:.4f} "
            f"incorrect_commit="
            f"{mean_incorrect_commitment:.4f} "
            f"adapt_exposure="
            f"{mean_adaptation_exposure:.4f}"
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