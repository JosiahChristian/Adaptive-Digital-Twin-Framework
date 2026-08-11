import csv
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path


INPUT_PATH = Path(
    "results/criterion_failure_decomposition.csv"
)

OUTPUT_PATH = Path(
    "results/probabilistic_failure_aware_decision_policy.csv"
)


BATCH_SIZES = [
    5,
    10,
    20,
]

DECISION_REPLICATES = 500

RANDOM_SEED = 36036


FAILURE_MODES = [
    "pass_all",
    "A_only",
    "C_only",
    "S_only",
    "A_and_C",
    "A_and_S",
    "C_and_S",
    "A_and_C_and_S",
]


ACTIONS = {
    "normal": {
        "adaptation_scale": 1.00,
        "uncertainty_scale": 1.00,
        "abstain": False,
    },

    "coverage_wait": {
        "adaptation_scale": 0.50,
        "uncertainty_scale": 1.15,
        "abstain": True,
    },

    "accuracy_guard": {
        "adaptation_scale": 0.20,
        "uncertainty_scale": 1.75,
        "abstain": True,
    },

    "selective_guard": {
        "adaptation_scale": 0.10,
        "uncertainty_scale": 1.25,
        "abstain": True,
    },

    "coupled_guard": {
        "adaptation_scale": 0.10,
        "uncertainty_scale": 2.00,
        "abstain": True,
    },

    "full_fallback": {
        "adaptation_scale": 0.00,
        "uncertainty_scale": 2.50,
        "abstain": True,
    },
}


GENERIC_ACTION = {
    "adaptation_scale": 0.25,
    "uncertainty_scale": 1.50,
    "abstain": True,
}


def load_rows() -> list[dict]:

    with INPUT_PATH.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def group_rows(
    rows: list[dict],
) -> dict[str, list[dict]]:

    groups = defaultdict(
        list
    )

    for row in rows:

        groups[
            row["condition"]
        ].append(
            row
        )

    return groups


def distribution(
    rows: list[dict],
) -> dict[str, float]:

    counts = Counter(
        row["failure_mode"]
        for row in rows
    )

    total = len(rows)

    return {
        mode:
            counts[mode] / total
        for mode in FAILURE_MODES
    }


def contains_A(
    mode: str,
) -> bool:

    return mode in {
        "A_only",
        "A_and_C",
        "A_and_S",
        "A_and_C_and_S",
    }


def contains_S(
    mode: str,
) -> bool:

    return mode in {
        "S_only",
        "A_and_S",
        "C_and_S",
        "A_and_C_and_S",
    }


def is_multicomponent(
    mode: str,
) -> bool:

    return mode in {
        "A_and_C",
        "A_and_S",
        "C_and_S",
        "A_and_C_and_S",
    }


def state_loss(
    *,
    mode: str,
    action: dict,
) -> float:

    adaptation_scale = float(
        action["adaptation_scale"]
    )

    uncertainty_scale = float(
        action["uncertainty_scale"]
    )

    abstain = bool(
        action["abstain"]
    )

    if mode == "pass_all":

        unnecessary_abstention = (
            0.25
            if abstain
            else 0.0
        )

        uncertainty_cost = (
            max(
                0.0,
                uncertainty_scale - 1.0,
            )
            * 0.10
        )

        return (
            unnecessary_abstention
            + uncertainty_cost
        )

    incorrect_commitment = (
        1.0
        if not abstain
        else 0.0
    )

    adaptation_exposure = 0.0

    if contains_A(
        mode
    ):

        adaptation_exposure += (
            adaptation_scale
        )

    elif contains_S(
        mode
    ):

        adaptation_exposure += (
            0.50
            * adaptation_scale
        )

    uncertainty_cost = (
        max(
            0.0,
            uncertainty_scale - 1.0,
        )
        * 0.10
    )

    severe_failure_penalty = (
        0.50
        if (
            is_multicomponent(
                mode
            )
            and not abstain
        )
        else 0.0
    )

    return (
        incorrect_commitment
        + adaptation_exposure
        + uncertainty_cost
        + severe_failure_penalty
    )


def expected_loss(
    *,
    epistemic_distribution: dict[str, float],
    action: dict,
) -> float:

    return sum(
        epistemic_distribution[mode]
        * state_loss(
            mode=mode,
            action=action,
        )
        for mode in FAILURE_MODES
    )


def choose_probabilistic_action(
    estimated_distribution: dict[str, float],
) -> tuple[
    str,
    dict,
    float,
]:

    candidates = []

    for action_name, action in (
        ACTIONS.items()
    ):

        estimated_loss = expected_loss(
            epistemic_distribution=(
                estimated_distribution
            ),
            action=action,
        )

        candidates.append(
            (
                estimated_loss,
                action_name,
                action,
            )
        )

    estimated_loss, action_name, action = min(
        candidates,
        key=lambda item: (
            item[0],
            item[1],
        ),
    )

    return (
        action_name,
        action,
        estimated_loss,
    )


def choose_generic_action(
    estimated_distribution: dict[str, float],
) -> tuple[
    str,
    dict,
]:

    probability_failure = (
        1.0
        - estimated_distribution[
            "pass_all"
        ]
    )

    if probability_failure >= 0.50:

        return (
            "generic_conservative",
            GENERIC_ACTION,
        )

    return (
        "normal",
        ACTIONS["normal"],
    )


def reference_oracle_loss(
    reference_distribution: dict[str, float],
) -> float:

    losses = []

    for action in (
        ACTIONS.values()
    ):

        losses.append(
            expected_loss(
                epistemic_distribution=(
                    reference_distribution
                ),
                action=action,
            )
        )

    return min(
        losses
    )


def run_experiment() -> list[dict]:

    rows = load_rows()

    groups = group_rows(
        rows
    )

    rng = random.Random(
        RANDOM_SEED
    )

    output_rows = []

    for condition, group in (
        groups.items()
    ):

        reference_distribution = (
            distribution(
                group
            )
        )

        oracle_loss = (
            reference_oracle_loss(
                reference_distribution
            )
        )

        for batch_size in (
            BATCH_SIZES
        ):

            for replicate in range(
                DECISION_REPLICATES
            ):

                sample = rng.sample(
                    group,
                    batch_size,
                )

                estimated_distribution = (
                    distribution(
                        sample
                    )
                )

                (
                    probabilistic_action_name,
                    probabilistic_action,
                    estimated_probabilistic_loss,
                ) = (
                    choose_probabilistic_action(
                        estimated_distribution
                    )
                )

                (
                    generic_action_name,
                    generic_action,
                ) = choose_generic_action(
                    estimated_distribution
                )

                policy_actions = {
                    "baseline": (
                        "normal",
                        ACTIONS[
                            "normal"
                        ],
                    ),

                    "generic_uncertainty": (
                        generic_action_name,
                        generic_action,
                    ),

                    "probabilistic_failure_aware": (
                        probabilistic_action_name,
                        probabilistic_action,
                    ),
                }

                for (
                    policy_name,
                    (
                        action_name,
                        action,
                    ),
                ) in policy_actions.items():

                    realized_reference_loss = (
                        expected_loss(
                            epistemic_distribution=(
                                reference_distribution
                            ),
                            action=action,
                        )
                    )

                    estimated_decision_loss = (
                        expected_loss(
                            epistemic_distribution=(
                                estimated_distribution
                            ),
                            action=action,
                        )
                    )

                    output_rows.append(
                        {
                            "condition":
                                condition,

                            "true_class":
                                group[0][
                                    "true_class"
                                ],

                            "magnitude":
                                float(
                                    group[0][
                                        "magnitude"
                                    ]
                                ),

                            "batch_size":
                                batch_size,

                            "replicate":
                                replicate,

                            "policy":
                                policy_name,

                            "selected_action":
                                action_name,

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

                            "estimated_p_pass":
                                estimated_distribution[
                                    "pass_all"
                                ],

                            "estimated_p_fail_A":
                                (
                                    estimated_distribution[
                                        "A_only"
                                    ]
                                    +
                                    estimated_distribution[
                                        "A_and_C"
                                    ]
                                    +
                                    estimated_distribution[
                                        "A_and_S"
                                    ]
                                    +
                                    estimated_distribution[
                                        "A_and_C_and_S"
                                    ]
                                ),

                            "estimated_p_fail_C":
                                (
                                    estimated_distribution[
                                        "C_only"
                                    ]
                                    +
                                    estimated_distribution[
                                        "A_and_C"
                                    ]
                                    +
                                    estimated_distribution[
                                        "C_and_S"
                                    ]
                                    +
                                    estimated_distribution[
                                        "A_and_C_and_S"
                                    ]
                                ),

                            "estimated_p_fail_S":
                                (
                                    estimated_distribution[
                                        "S_only"
                                    ]
                                    +
                                    estimated_distribution[
                                        "A_and_S"
                                    ]
                                    +
                                    estimated_distribution[
                                        "C_and_S"
                                    ]
                                    +
                                    estimated_distribution[
                                        "A_and_C_and_S"
                                    ]
                                ),

                            "estimated_decision_loss":
                                estimated_decision_loss,

                            "reference_expected_loss":
                                realized_reference_loss,

                            "oracle_reference_loss":
                                oracle_loss,

                            "decision_regret":
                                (
                                    realized_reference_loss
                                    - oracle_loss
                                ),

                            "probabilistic_internal_loss":
                                (
                                    estimated_probabilistic_loss
                                    if policy_name
                                    == "probabilistic_failure_aware"
                                    else ""
                                ),
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

    print("=" * 122)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PROBABILISTIC FAILURE-AWARE DECISION POLICY"
    )

    print("=" * 122)

    policies = [
        "baseline",
        "generic_uncertainty",
        "probabilistic_failure_aware",
    ]

    for batch_size in BATCH_SIZES:

        print()
        print(
            f"n={batch_size}"
        )

        for policy in policies:

            group = [
                row
                for row in rows
                if (
                    int(
                        row["batch_size"]
                    )
                    == batch_size
                    and
                    row["policy"]
                    == policy
                )
            ]

            mean_loss = (
                statistics.mean(
                    float(
                        row[
                            "reference_expected_loss"
                        ]
                    )
                    for row in group
                )
            )

            mean_regret = (
                statistics.mean(
                    float(
                        row[
                            "decision_regret"
                        ]
                    )
                    for row in group
                )
            )

            print(
                f"  {policy:<29}"
                f"loss="
                f"{mean_loss:.4f} "
                f"regret="
                f"{mean_regret:.4f}"
            )

    print("=" * 122)


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