import csv
from pathlib import Path

from experiments.responsiveness_preserving_safe_persistence_control import (
    RISK_MULTIPLIERS,
    deterministic_split,
    train_loss_models,
    train_occurrence_model,
    train_magnitude_model,
    predicted_loss_table,
    predict_two_stage_risk,
    direct_predictions,
    fixed_risk_predictions,
    adaptive_risk_predictions,
    fixed_predictions,
    oracle_predictions,
    evaluate_policy,
)
from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)


OUTPUT_PATH = Path(
    "results/"
    "pareto_safe_responsive_persistence_analysis.csv"
)

FIXED_RISK_PENALTY = 0.010


def dominates(
    left: dict,
    right: dict,
) -> bool:

    no_worse = (
        left["mean_regret"]
        <= right["mean_regret"]
        and left["under_count"]
        <= right["under_count"]
        and left["over_count"]
        <= right["over_count"]
        and left["action_entropy"]
        >= right["action_entropy"]
    )

    strictly_better = (
        left["mean_regret"]
        < right["mean_regret"]
        or left["under_count"]
        < right["under_count"]
        or left["over_count"]
        < right["over_count"]
        or left["action_entropy"]
        > right["action_entropy"]
    )

    return (
        no_worse
        and strictly_better
    )


def adaptive_policy(
    result: dict,
) -> bool:

    return (
        result["policy"]
        == "direct_loss"
        or result["policy"]
        == "fixed_risk_0.010"
        or result["policy"].startswith(
            "two_stage_"
        )
    )


def pareto_front(
    evaluations: list[dict],
) -> list[dict]:

    candidates = [
        result
        for result in evaluations
        if adaptive_policy(
            result
        )
    ]

    front = []

    for candidate in candidates:

        dominated = any(
            dominates(
                other,
                candidate,
            )
            for other in candidates
            if other is not candidate
        )

        if not dominated:

            front.append(
                candidate
            )

    return sorted(
        front,
        key=lambda result: (
            result["under_count"],
            result["mean_regret"],
            -result["action_entropy"],
        ),
    )


def regret_equivalent_pairs(
    evaluations: list[dict],
    tolerance: float = 1e-12,
) -> list[tuple[dict, dict]]:

    candidates = [
        result
        for result in evaluations
        if adaptive_policy(
            result
        )
    ]

    pairs = []

    for index, left in enumerate(
        candidates
    ):

        for right in candidates[
            index + 1:
        ]:

            if (
                abs(
                    left["mean_regret"]
                    - right["mean_regret"]
                )
                <= tolerance
                and abs(
                    left["action_entropy"]
                    - right["action_entropy"]
                )
                > 1e-12
            ):

                pairs.append(
                    (
                        left,
                        right,
                    )
                )

    return pairs


def safety_levels(
    evaluations: list[dict],
) -> list[dict]:

    candidates = [
        result
        for result in evaluations
        if adaptive_policy(
            result
        )
    ]

    unique_under_counts = sorted(
        {
            int(
                result[
                    "under_count"
                ]
            )
            for result in candidates
        }
    )

    output = []

    for under_limit in (
        unique_under_counts
    ):

        feasible = [
            result
            for result in candidates
            if result[
                "under_count"
            ]
            <= under_limit
        ]

        best_regret = min(
            feasible,
            key=lambda result: (
                result[
                    "mean_regret"
                ],
                -result[
                    "action_entropy"
                ],
                result[
                    "over_count"
                ],
            ),
        )

        most_responsive = max(
            feasible,
            key=lambda result: (
                result[
                    "action_entropy"
                ],
                -result[
                    "mean_regret"
                ],
                -result[
                    "over_count"
                ],
            ),
        )

        output.append(
            {
                "under_limit":
                    under_limit,

                "best_regret_policy":
                    best_regret[
                        "policy"
                    ],

                "best_regret":
                    best_regret[
                        "mean_regret"
                    ],

                "best_regret_entropy":
                    best_regret[
                        "action_entropy"
                    ],

                "responsive_policy":
                    most_responsive[
                        "policy"
                    ],

                "responsive_regret":
                    most_responsive[
                        "mean_regret"
                    ],

                "responsive_entropy":
                    most_responsive[
                        "action_entropy"
                    ],
            }
        )

    return output


def marginal_safety_cost(
    evaluations: list[dict],
) -> list[dict]:

    adaptive = sorted(
        [
            result
            for result in evaluations
            if result[
                "policy"
            ].startswith(
                "two_stage_"
            )
        ],
        key=lambda result: (
            -result[
                "under_count"
            ],
            -result[
                "action_entropy"
            ],
        ),
    )

    output = []

    for left, right in zip(
        adaptive,
        adaptive[
            1:
        ],
    ):

        under_reduction = (
            left[
                "under_count"
            ]
            - right[
                "under_count"
            ]
        )

        if under_reduction <= 0:
            continue

        entropy_cost = (
            left[
                "action_entropy"
            ]
            - right[
                "action_entropy"
            ]
        )

        regret_change = (
            right[
                "mean_regret"
            ]
            - left[
                "mean_regret"
            ]
        )

        output.append(
            {
                "from_policy":
                    left[
                        "policy"
                    ],

                "to_policy":
                    right[
                        "policy"
                    ],

                "under_reduction":
                    under_reduction,

                "entropy_cost":
                    entropy_cost,

                "entropy_cost_per_under":
                    (
                        entropy_cost
                        / under_reduction
                    ),

                "regret_change":
                    regret_change,
            }
        )

    return output


def composite_knee_score(
    result: dict,
    max_regret: float,
    max_under: int,
) -> float:

    regret_term = (
        result[
            "mean_regret"
        ]
        / max_regret
        if max_regret > 0
        else 0.0
    )

    under_term = (
        result[
            "under_count"
        ]
        / max_under
        if max_under > 0
        else 0.0
    )

    responsiveness_loss = (
        1.0
        - result[
            "action_entropy"
        ]
    )

    return (
        regret_term
        + under_term
        + responsiveness_loss
    )


def identify_knee(
    evaluations: list[dict],
) -> dict:

    candidates = [
        result
        for result in evaluations
        if adaptive_policy(
            result
        )
    ]

    max_regret = max(
        result[
            "mean_regret"
        ]
        for result in candidates
    )

    max_under = max(
        result[
            "under_count"
        ]
        for result in candidates
    )

    return min(
        candidates,
        key=lambda result:
            composite_knee_score(
                result,
                max_regret,
                max_under,
            ),
    )


def save_analysis(
    evaluations: list[dict],
    pareto: list[dict],
) -> None:

    OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )

    pareto_names = {
        result[
            "policy"
        ]
        for result in pareto
    }

    rows = []

    for result in evaluations:

        row = dict(
            result
        )

        row[
            "adaptive_candidate"
        ] = int(
            adaptive_policy(
                result
            )
        )

        row[
            "pareto_efficient"
        ] = int(
            result[
                "policy"
            ]
            in pareto_names
        )

        rows.append(
            row
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


def print_policy(
    result: dict,
) -> None:

    print(
        f"{result['policy']:<24} "
        f"regret="
        f"{result['mean_regret']:.6f} "
        f"under="
        f"{result['under_count']:<2} "
        f"over="
        f"{result['over_count']:<2} "
        f"entropy="
        f"{result['action_entropy']:.3f} "
        f"dominant="
        f"{result['dominant_action_fraction']:.3%}"
    )


def main() -> None:

    rows = generate_analysis_rows()

    (
        train_rows,
        test_rows,
    ) = deterministic_split(
        rows
    )

    loss_models = train_loss_models(
        train_rows
    )

    occurrence_model = (
        train_occurrence_model(
            train_rows
        )
    )

    magnitude_model = (
        train_magnitude_model(
            train_rows
        )
    )

    predicted_losses = (
        predicted_loss_table(
            loss_models,
            test_rows,
        )
    )

    predicted_risks = (
        predict_two_stage_risk(
            occurrence_model,
            magnitude_model,
            test_rows,
        )
    )

    direct = direct_predictions(
        predicted_losses
    )

    evaluations = []

    for persistence in (
        1,
        2,
        3,
    ):

        evaluations.append(
            evaluate_policy(
                name=(
                    f"fixed_k"
                    f"{persistence}"
                ),
                predictions=fixed_predictions(
                    persistence,
                    test_rows,
                ),
                rows=test_rows,
                direct=direct,
            )
        )

    evaluations.append(
        evaluate_policy(
            name="direct_loss",
            predictions=direct,
            rows=test_rows,
            direct=direct,
        )
    )

    fixed_risk = (
        fixed_risk_predictions(
            predicted_losses,
            FIXED_RISK_PENALTY,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="fixed_risk_0.010",
            predictions=fixed_risk,
            rows=test_rows,
            direct=direct,
        )
    )

    for multiplier in (
        RISK_MULTIPLIERS
    ):

        predictions = (
            adaptive_risk_predictions(
                predicted_losses,
                predicted_risks,
                multiplier,
            )
        )

        evaluations.append(
            evaluate_policy(
                name=(
                    "two_stage_"
                    f"{multiplier:.2f}"
                ),
                predictions=predictions,
                rows=test_rows,
                direct=direct,
            )
        )

    evaluations.append(
        evaluate_policy(
            name="oracle",
            predictions=oracle_predictions(
                test_rows
            ),
            rows=test_rows,
            direct=direct,
        )
    )

    pareto = pareto_front(
        evaluations
    )

    equivalent_pairs = (
        regret_equivalent_pairs(
            evaluations
        )
    )

    levels = safety_levels(
        evaluations
    )

    marginal_costs = (
        marginal_safety_cost(
            evaluations
        )
    )

    knee = identify_knee(
        evaluations
    )

    save_analysis(
        evaluations,
        pareto,
    )

    print("=" * 175)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PARETO SAFETY / REGRET / "
        "RESPONSIVENESS ANALYSIS"
    )

    print("=" * 175)

    print(
        f"total contexts="
        f"{len(rows)}"
    )

    print(
        f"training contexts="
        f"{len(train_rows)}"
    )

    print(
        f"test contexts="
        f"{len(test_rows)}"
    )

    print()

    print(
        "PARETO-EFFICIENT "
        "ADAPTIVE POLICIES"
    )

    for result in pareto:

        print_policy(
            result
        )

    print()

    print(
        "COMPOSITE KNEE POLICY"
    )

    print_policy(
        knee
    )

    print()

    print(
        "SAFETY-CONSTRAINED "
        "OPERATING POINTS"
    )

    for level in levels:

        print(
            f"under<="
            f"{level['under_limit']:<2} "
            f"best_regret="
            f"{level['best_regret_policy']:<22} "
            f"R="
            f"{level['best_regret']:.6f} "
            f"H="
            f"{level['best_regret_entropy']:.3f} "
            f"most_responsive="
            f"{level['responsive_policy']:<22} "
            f"R="
            f"{level['responsive_regret']:.6f} "
            f"H="
            f"{level['responsive_entropy']:.3f}"
        )

    print()

    print(
        "REGRET-EQUIVALENT "
        "RESPONSIVENESS DIFFERENCES"
    )

    for left, right in equivalent_pairs:

        print(
            f"{left['policy']:<22} "
            f"vs "
            f"{right['policy']:<22} "
            f"regret="
            f"{left['mean_regret']:.6f} "
            f"entropy="
            f"{left['action_entropy']:.3f}"
            f" vs "
            f"{right['action_entropy']:.3f}"
        )

    print()

    print(
        "MARGINAL RESPONSIVENESS "
        "COST OF SAFETY"
    )

    for item in marginal_costs:

        print(
            f"{item['from_policy']:<22} "
            f"-> "
            f"{item['to_policy']:<22} "
            f"under_reduction="
            f"{item['under_reduction']} "
            f"entropy_cost="
            f"{item['entropy_cost']:.3f} "
            f"cost_per_under="
            f"{item['entropy_cost_per_under']:.3f} "
            f"regret_change="
            f"{item['regret_change']:.6f}"
        )

    print("=" * 175)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()