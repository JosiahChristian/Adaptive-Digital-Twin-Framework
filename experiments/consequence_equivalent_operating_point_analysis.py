import csv
from collections import Counter
from pathlib import Path

from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)
from experiments.responsiveness_preserving_safe_persistence_control import (
    train_loss_models,
    train_occurrence_model,
    train_magnitude_model,
    predicted_loss_table,
    predict_two_stage_risk,
    adaptive_risk_predictions,
    direct_predictions,
)


OUTPUT_PATH = Path(
    "results/"
    "consequence_equivalent_operating_point_analysis.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "consequence_equivalent_operating_point_analysis_contexts.csv"
)

BASE_GENERATION_SEED = 44000

TEST_FRACTION = 0.30
META_FRACTION = 0.30

RISK_LEVELS = [
    0.00,
    0.10,
    0.25,
    1.00,
]

EPSILONS = [
    0.000000,
    0.000100,
    0.000500,
    0.001000,
    0.002500,
    0.005000,
]

FLOAT_TOLERANCE = 1e-12


def three_way_split(
    rows: list[dict],
) -> tuple[
    list[dict],
    list[dict],
    list[dict],
]:

    test_start = int(
        len(rows)
        * (
            1.0
            - TEST_FRACTION
        )
    )

    development_rows = rows[
        :test_start
    ]

    test_rows = rows[
        test_start:
    ]

    meta_start = int(
        len(development_rows)
        * (
            1.0
            - META_FRACTION
        )
    )

    base_train_rows = development_rows[
        :meta_start
    ]

    meta_train_rows = development_rows[
        meta_start:
    ]

    return (
        base_train_rows,
        meta_train_rows,
        test_rows,
    )


def selected_loss(
    row: dict,
    persistence: int,
) -> float:

    return float(
        row[
            f"loss_k{persistence}"
        ]
    )


def regret(
    row: dict,
    persistence: int,
) -> float:

    return (
        selected_loss(
            row,
            persistence,
        )
        - float(
            row[
                "best_loss"
            ]
        )
    )


def candidate_predictions(
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict[
    float,
    list[int],
]:

    output = {
        0.00:
            direct_predictions(
                predicted_losses
            )
    }

    for risk_level in [
        0.10,
        0.25,
        1.00,
    ]:

        output[
            risk_level
        ] = adaptive_risk_predictions(
            predicted_losses,
            predicted_risks,
            risk_level,
        )

    return output


def candidate_regrets(
    row: dict,
    candidates: dict[
        float,
        list[int],
    ],
    index: int,
) -> dict[
    float,
    float,
]:

    return {
        risk_level:
            regret(
                row,
                candidates[
                    risk_level
                ][index],
            )
        for risk_level
        in RISK_LEVELS
    }


def exact_action_groups(
    candidates: dict[
        float,
        list[int],
    ],
    index: int,
) -> dict[
    int,
    list[float],
]:

    groups = {}

    for risk_level in (
        RISK_LEVELS
    ):

        action = int(
            candidates[
                risk_level
            ][index]
        )

        groups.setdefault(
            action,
            [],
        ).append(
            risk_level
        )

    return groups


def exact_regret_groups(
    regrets: dict[
        float,
        float,
    ],
) -> list[
    list[float]
]:

    groups = []

    unused = set(
        RISK_LEVELS
    )

    while unused:

        reference = min(
            unused
        )

        reference_regret = (
            regrets[
                reference
            ]
        )

        group = [
            risk_level
            for risk_level
            in sorted(
                unused
            )
            if abs(
                regrets[
                    risk_level
                ]
                - reference_regret
            )
            <= FLOAT_TOLERANCE
        ]

        groups.append(
            group
        )

        for risk_level in group:
            unused.remove(
                risk_level
            )

    return groups


def epsilon_equivalent_levels(
    regrets: dict[
        float,
        float,
    ],
    epsilon: float,
) -> list[float]:

    minimum_regret = min(
        regrets.values()
    )

    return [
        risk_level
        for risk_level
        in RISK_LEVELS
        if (
            regrets[
                risk_level
            ]
            <= (
                minimum_regret
                + epsilon
                + FLOAT_TOLERANCE
            )
        )
    ]


def lambda_text(
    levels: list[float],
) -> str:

    return "|".join(
        f"{level:.2f}"
        for level in levels
    )


def action_text(
    groups: dict[
        int,
        list[float],
    ],
) -> str:

    return ";".join(
        (
            f"k{action}:"
            f"{lambda_text(levels)}"
        )
        for action, levels
        in sorted(
            groups.items()
        )
    )


def regret_group_text(
    groups: list[
        list[float]
    ],
) -> str:

    return ";".join(
        lambda_text(
            group
        )
        for group in groups
    )


def save_csv(
    path: Path,
    rows: list[dict],
) -> None:

    path.parent.mkdir(
        exist_ok=True
    )

    if not rows:
        return

    fields = []

    for row in rows:

        for key in row.keys():

            if key not in fields:
                fields.append(
                    key
                )

    for row in rows:

        for field in fields:

            row.setdefault(
                field,
                ""
            )

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )

        writer.writeheader()
        writer.writerows(
            rows
        )


def percentage(
    numerator: int,
    denominator: int,
) -> float:

    if denominator == 0:
        return 0.0

    return (
        numerator
        / denominator
    )


def main() -> None:

    rows = generate_analysis_rows(
        base_seed=BASE_GENERATION_SEED
    )

    (
        base_train_rows,
        meta_train_rows,
        test_rows,
    ) = three_way_split(
        rows
    )

    loss_models = train_loss_models(
        base_train_rows
    )

    occurrence_model = (
        train_occurrence_model(
            base_train_rows
        )
    )

    magnitude_model = (
        train_magnitude_model(
            base_train_rows
        )
    )

    test_losses = predicted_loss_table(
        loss_models,
        test_rows,
    )

    test_risks = predict_two_stage_risk(
        occurrence_model,
        magnitude_model,
        test_rows,
    )

    candidates = candidate_predictions(
        test_losses,
        test_risks,
    )

    context_rows = []

    exact_action_equivalence_contexts = 0
    exact_regret_equivalence_contexts = 0

    all_action_equivalent = 0
    all_regret_equivalent = 0

    action_group_size_counts = Counter()
    regret_group_size_counts = Counter()

    epsilon_summary = {
        epsilon: {
            "multi_member":
                0,

            "less_conservative":
                0,

            "strictly_less_conservative":
                0,

            "mean_class_size_total":
                0,

            "lambda_reduction_total":
                0.0,

            "oracle_min_lambda_total":
                0.0,

            "responsive_lambda_total":
                0.0,
        }
        for epsilon in EPSILONS
    }

    for index, row in enumerate(
        test_rows
    ):

        regrets = candidate_regrets(
            row,
            candidates,
            index,
        )

        actions = {
            risk_level:
                int(
                    candidates[
                        risk_level
                    ][index]
                )
            for risk_level
            in RISK_LEVELS
        }

        action_groups = (
            exact_action_groups(
                candidates,
                index,
            )
        )

        regret_groups = (
            exact_regret_groups(
                regrets
            )
        )

        largest_action_group = max(
            len(levels)
            for levels
            in action_groups.values()
        )

        largest_regret_group = max(
            len(levels)
            for levels
            in regret_groups
        )

        action_group_size_counts[
            largest_action_group
        ] += 1

        regret_group_size_counts[
            largest_regret_group
        ] += 1

        if largest_action_group > 1:
            exact_action_equivalence_contexts += 1

        if largest_regret_group > 1:
            exact_regret_equivalence_contexts += 1

        if largest_action_group == len(
            RISK_LEVELS
        ):
            all_action_equivalent += 1

        if largest_regret_group == len(
            RISK_LEVELS
        ):
            all_regret_equivalent += 1

        minimum_regret = min(
            regrets.values()
        )

        exact_min_levels = [
            risk_level
            for risk_level
            in RISK_LEVELS
            if abs(
                regrets[
                    risk_level
                ]
                - minimum_regret
            )
            <= FLOAT_TOLERANCE
        ]

        conservative_exact_min = max(
            exact_min_levels
        )

        responsive_exact_min = min(
            exact_min_levels
        )

        context_record = {
            "test_index":
                index,

            "best_persistence":
                int(
                    row[
                        "best_persistence"
                    ]
                ),

            "predicted_under_risk":
                float(
                    test_risks[
                        index
                    ]
                ),

            "action_lambda_0.00":
                actions[
                    0.00
                ],

            "action_lambda_0.10":
                actions[
                    0.10
                ],

            "action_lambda_0.25":
                actions[
                    0.25
                ],

            "action_lambda_1.00":
                actions[
                    1.00
                ],

            "regret_lambda_0.00":
                regrets[
                    0.00
                ],

            "regret_lambda_0.10":
                regrets[
                    0.10
                ],

            "regret_lambda_0.25":
                regrets[
                    0.25
                ],

            "regret_lambda_1.00":
                regrets[
                    1.00
                ],

            "minimum_regret":
                minimum_regret,

            "exact_min_levels":
                lambda_text(
                    exact_min_levels
                ),

            "responsive_exact_min_lambda":
                responsive_exact_min,

            "conservative_exact_min_lambda":
                conservative_exact_min,

            "exact_min_lambda_span":
                (
                    conservative_exact_min
                    - responsive_exact_min
                ),

            "action_groups":
                action_text(
                    action_groups
                ),

            "regret_groups":
                regret_group_text(
                    regret_groups
                ),

            "largest_action_group":
                largest_action_group,

            "largest_regret_group":
                largest_regret_group,
        }

        for epsilon in (
            EPSILONS
        ):

            equivalent = (
                epsilon_equivalent_levels(
                    regrets,
                    epsilon,
                )
            )

            class_size = len(
                equivalent
            )

            responsive_lambda = min(
                equivalent
            )

            conservative_lambda = max(
                equivalent
            )

            exact_oracle_lambda = min(
                exact_min_levels
            )

            epsilon_summary[
                epsilon
            ][
                "mean_class_size_total"
            ] += class_size

            epsilon_summary[
                epsilon
            ][
                "oracle_min_lambda_total"
            ] += exact_oracle_lambda

            epsilon_summary[
                epsilon
            ][
                "responsive_lambda_total"
            ] += responsive_lambda

            epsilon_summary[
                epsilon
            ][
                "lambda_reduction_total"
            ] += (
                conservative_lambda
                - responsive_lambda
            )

            if class_size > 1:

                epsilon_summary[
                    epsilon
                ][
                    "multi_member"
                ] += 1

            if (
                responsive_lambda
                < conservative_lambda
            ):

                epsilon_summary[
                    epsilon
                ][
                    "less_conservative"
                ] += 1

            if (
                responsive_lambda
                < exact_oracle_lambda
            ):

                epsilon_summary[
                    epsilon
                ][
                    "strictly_less_conservative"
                ] += 1

            epsilon_name = (
                f"{epsilon:.6f}"
            )

            context_record[
                (
                    "epsilon_"
                    f"{epsilon_name}_levels"
                )
            ] = lambda_text(
                equivalent
            )

            context_record[
                (
                    "epsilon_"
                    f"{epsilon_name}_size"
                )
            ] = class_size

            context_record[
                (
                    "epsilon_"
                    f"{epsilon_name}_responsive_lambda"
                )
            ] = responsive_lambda

            context_record[
                (
                    "epsilon_"
                    f"{epsilon_name}_conservative_lambda"
                )
            ] = conservative_lambda

        context_rows.append(
            context_record
        )

    total = len(
        test_rows
    )

    summary_rows = []

    for epsilon in (
        EPSILONS
    ):

        stats = epsilon_summary[
            epsilon
        ]

        summary_rows.append(
            {
                "epsilon":
                    epsilon,

                "contexts":
                    total,

                "multi_member_contexts":
                    stats[
                        "multi_member"
                    ],

                "multi_member_fraction":
                    percentage(
                        stats[
                            "multi_member"
                        ],
                        total,
                    ),

                "less_conservative_available":
                    stats[
                        "less_conservative"
                    ],

                "less_conservative_fraction":
                    percentage(
                        stats[
                            "less_conservative"
                        ],
                        total,
                    ),

                "strictly_below_exact_oracle":
                    stats[
                        "strictly_less_conservative"
                    ],

                "strictly_below_exact_oracle_fraction":
                    percentage(
                        stats[
                            "strictly_less_conservative"
                        ],
                        total,
                    ),

                "mean_equivalence_class_size":
                    (
                        stats[
                            "mean_class_size_total"
                        ]
                        / total
                    ),

                "mean_lambda_span":
                    (
                        stats[
                            "lambda_reduction_total"
                        ]
                        / total
                    ),

                "mean_exact_oracle_lambda":
                    (
                        stats[
                            "oracle_min_lambda_total"
                        ]
                        / total
                    ),

                "mean_responsive_lambda":
                    (
                        stats[
                            "responsive_lambda_total"
                        ]
                        / total
                    ),

                "exact_action_equivalence_contexts":
                    exact_action_equivalence_contexts,

                "exact_action_equivalence_fraction":
                    percentage(
                        exact_action_equivalence_contexts,
                        total,
                    ),

                "exact_regret_equivalence_contexts":
                    exact_regret_equivalence_contexts,

                "exact_regret_equivalence_fraction":
                    percentage(
                        exact_regret_equivalence_contexts,
                        total,
                    ),

                "all_action_equivalent_contexts":
                    all_action_equivalent,

                "all_action_equivalent_fraction":
                    percentage(
                        all_action_equivalent,
                        total,
                    ),

                "all_regret_equivalent_contexts":
                    all_regret_equivalent,

                "all_regret_equivalent_fraction":
                    percentage(
                        all_regret_equivalent,
                        total,
                    ),
            }
        )

    save_csv(
        OUTPUT_PATH,
        summary_rows,
    )

    save_csv(
        CONTEXT_OUTPUT_PATH,
        context_rows,
    )

    print("=" * 180)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "CONSEQUENCE-EQUIVALENT "
        "OPERATING-POINT ANALYSIS"
    )

    print("=" * 180)

    print(
        f"generation seed="
        f"{BASE_GENERATION_SEED}"
    )

    print(
        f"total contexts="
        f"{len(rows)}"
    )

    print(
        f"base-training contexts="
        f"{len(base_train_rows)}"
    )

    print(
        f"unused meta contexts="
        f"{len(meta_train_rows)}"
    )

    print(
        f"test contexts="
        f"{len(test_rows)}"
    )

    print()

    print(
        "EXACT EQUIVALENCE"
    )

    print(
        "contexts with action-equivalent "
        "risk levels="
        f"{exact_action_equivalence_contexts}/"
        f"{total} "
        f"("
        f"{percentage(exact_action_equivalence_contexts, total):.3%}"
        f")"
    )

    print(
        "contexts with regret-equivalent "
        "risk levels="
        f"{exact_regret_equivalence_contexts}/"
        f"{total} "
        f"("
        f"{percentage(exact_regret_equivalence_contexts, total):.3%}"
        f")"
    )

    print(
        "all four risk levels action-equivalent="
        f"{all_action_equivalent}/"
        f"{total} "
        f"("
        f"{percentage(all_action_equivalent, total):.3%}"
        f")"
    )

    print(
        "all four risk levels regret-equivalent="
        f"{all_regret_equivalent}/"
        f"{total} "
        f"("
        f"{percentage(all_regret_equivalent, total):.3%}"
        f")"
    )

    print()

    print(
        "LARGEST EXACT ACTION-EQUIVALENCE CLASS"
    )

    for size in sorted(
        action_group_size_counts
    ):

        count = (
            action_group_size_counts[
                size
            ]
        )

        print(
            f"size={size}: "
            f"{count} "
            f"("
            f"{percentage(count, total):.3%}"
            f")"
        )

    print()

    print(
        "LARGEST EXACT REGRET-EQUIVALENCE CLASS"
    )

    for size in sorted(
        regret_group_size_counts
    ):

        count = (
            regret_group_size_counts[
                size
            ]
        )

        print(
            f"size={size}: "
            f"{count} "
            f"("
            f"{percentage(count, total):.3%}"
            f")"
        )

    print()

    print(
        "EPSILON-EQUIVALENCE SUMMARY"
    )

    for summary in (
        summary_rows
    ):

        print(
            f"epsilon="
            f"{summary['epsilon']:.6f} "
            f"multi="
            f"{summary['multi_member_contexts']:<2} "
            f"("
            f"{summary['multi_member_fraction']:.3%}"
            f") "
            f"less_conservative="
            f"{summary['less_conservative_available']:<2} "
            f"("
            f"{summary['less_conservative_fraction']:.3%}"
            f") "
            f"below_exact_oracle="
            f"{summary['strictly_below_exact_oracle']:<2} "
            f"("
            f"{summary['strictly_below_exact_oracle_fraction']:.3%}"
            f") "
            f"mean_size="
            f"{summary['mean_equivalence_class_size']:.3f} "
            f"mean_span="
            f"{summary['mean_lambda_span']:.4f} "
            f"responsive_mean_lambda="
            f"{summary['mean_responsive_lambda']:.4f}"
        )

    print()

    print(
        f"Summary results saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Context results saved to: "
        f"{CONTEXT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()