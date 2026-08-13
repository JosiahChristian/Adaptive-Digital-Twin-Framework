import csv
import statistics
from collections import Counter, defaultdict
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
    direct_predictions,
    fixed_risk_predictions,
    adaptive_risk_predictions,
    fixed_predictions,
    oracle_predictions,
    evaluate_policy,
)


OUTPUT_PATH = Path(
    "results/"
    "multiseed_balanced_persistence_robustness.csv"
)

SEEDS = list(range(10))

TEST_FRACTION = 0.30

FIXED_RISK_PENALTY = 0.010

POLICY_MULTIPLIERS = {
    "two_stage_0.10": 0.10,
    "two_stage_0.25": 0.25,
    "two_stage_1.00": 1.00,
}


def seeded_split(
    rows: list[dict],
    seed: int,
) -> tuple[list[dict], list[dict]]:

    import random

    shuffled = list(rows)

    random.Random(
        seed
    ).shuffle(
        shuffled
    )

    split_index = int(
        len(shuffled)
        * (1.0 - TEST_FRACTION)
    )

    return (
        shuffled[:split_index],
        shuffled[split_index:],
    )


def evaluate_seed(
    rows: list[dict],
    seed: int,
) -> list[dict]:

    (
        train_rows,
        test_rows,
    ) = seeded_split(
        rows,
        seed,
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

    for (
        policy_name,
        multiplier,
    ) in POLICY_MULTIPLIERS.items():

        predictions = (
            adaptive_risk_predictions(
                predicted_losses,
                predicted_risks,
                multiplier,
            )
        )

        evaluations.append(
            evaluate_policy(
                name=policy_name,
                predictions=predictions,
                rows=test_rows,
                direct=direct,
            )
        )

    fixed_k3 = fixed_predictions(
        3,
        test_rows,
    )

    evaluations.append(
        evaluate_policy(
            name="fixed_k3",
            predictions=fixed_k3,
            rows=test_rows,
            direct=direct,
        )
    )

    oracle = oracle_predictions(
        test_rows
    )

    evaluations.append(
        evaluate_policy(
            name="oracle",
            predictions=oracle,
            rows=test_rows,
            direct=direct,
        )
    )

    output = []

    for result in evaluations:

        row = dict(
            result
        )

        row[
            "seed"
        ] = seed

        row[
            "train_count"
        ] = len(
            train_rows
        )

        row[
            "test_count"
        ] = len(
            test_rows
        )

        output.append(
            row
        )

    return output


def adaptive_candidate(
    row: dict,
) -> bool:

    return row[
        "policy"
    ] in {
        "direct_loss",
        "fixed_risk_0.010",
        "two_stage_0.10",
        "two_stage_0.25",
        "two_stage_1.00",
    }


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


def pareto_policies(
    seed_rows: list[dict],
) -> set[str]:

    candidates = [
        row
        for row in seed_rows
        if adaptive_candidate(
            row
        )
    ]

    front = set()

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

            front.add(
                candidate[
                    "policy"
                ]
            )

    return front


def add_pareto_flags(
    rows: list[dict],
) -> None:

    by_seed = defaultdict(
        list
    )

    for row in rows:

        by_seed[
            int(
                row[
                    "seed"
                ]
            )
        ].append(
            row
        )

    for seed_rows in (
        by_seed.values()
    ):

        front = pareto_policies(
            seed_rows
        )

        for row in seed_rows:

            row[
                "pareto_efficient"
            ] = int(
                row[
                    "policy"
                ]
                in front
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


def metric_values(
    rows: list[dict],
    policy: str,
    metric: str,
) -> list[float]:

    return [
        float(
            row[
                metric
            ]
        )
        for row in rows
        if row[
            "policy"
        ]
        == policy
    ]


def summarize_policy(
    rows: list[dict],
    policy: str,
) -> dict:

    regrets = metric_values(
        rows,
        policy,
        "mean_regret",
    )

    under = metric_values(
        rows,
        policy,
        "under_count",
    )

    over = metric_values(
        rows,
        policy,
        "over_count",
    )

    entropy = metric_values(
        rows,
        policy,
        "action_entropy",
    )

    pareto = metric_values(
        rows,
        policy,
        "pareto_efficient",
    )

    return {
        "policy":
            policy,

        "mean_regret":
            statistics.mean(
                regrets
            ),

        "std_regret":
            statistics.pstdev(
                regrets
            ),

        "median_regret":
            statistics.median(
                regrets
            ),

        "min_regret":
            min(
                regrets
            ),

        "max_regret":
            max(
                regrets
            ),

        "mean_under":
            statistics.mean(
                under
            ),

        "max_under":
            max(
                under
            ),

        "mean_over":
            statistics.mean(
                over
            ),

        "mean_entropy":
            statistics.mean(
                entropy
            ),

        "min_entropy":
            min(
                entropy
            ),

        "pareto_frequency":
            statistics.mean(
                pareto
            ),
    }


def selection_frequency(
    rows: list[dict],
) -> Counter:

    by_seed = defaultdict(
        list
    )

    for row in rows:

        if adaptive_candidate(
            row
        ):

            by_seed[
                int(
                    row[
                        "seed"
                    ]
                )
            ].append(
                row
            )

    winners = Counter()

    for seed_rows in (
        by_seed.values()
    ):

        feasible = [
            row
            for row in seed_rows
            if row[
                "action_entropy"
            ]
            >= 0.30
            and row[
                "dominant_action_fraction"
            ]
            <= 0.90
        ]

        if not feasible:
            continue

        winner = min(
            feasible,
            key=lambda row: (
                row[
                    "mean_regret"
                ],
                row[
                    "under_count"
                ],
                row[
                    "over_count"
                ],
                -row[
                    "action_entropy"
                ],
            ),
        )

        winners[
            winner[
                "policy"
            ]
        ] += 1

    return winners


def print_summary(
    summary: dict,
) -> None:

    print(
        f"{summary['policy']:<20} "
        f"mean_R="
        f"{summary['mean_regret']:.6f} "
        f"std_R="
        f"{summary['std_regret']:.6f} "
        f"median_R="
        f"{summary['median_regret']:.6f} "
        f"range=["
        f"{summary['min_regret']:.6f},"
        f"{summary['max_regret']:.6f}] "
        f"mean_under="
        f"{summary['mean_under']:.2f} "
        f"max_under="
        f"{summary['max_under']:.0f} "
        f"mean_over="
        f"{summary['mean_over']:.2f} "
        f"mean_H="
        f"{summary['mean_entropy']:.3f} "
        f"min_H="
        f"{summary['min_entropy']:.3f} "
        f"pareto="
        f"{summary['pareto_frequency']:.1%}"
    )


def main() -> None:

    rows = generate_analysis_rows()

    all_results = []

    for seed in SEEDS:

        seed_results = evaluate_seed(
            rows,
            seed,
        )

        all_results.extend(
            seed_results
        )

    add_pareto_flags(
        all_results
    )

    save_results(
        all_results
    )

    policies = [
        "direct_loss",
        "fixed_risk_0.010",
        "two_stage_0.10",
        "two_stage_0.25",
        "two_stage_1.00",
        "fixed_k3",
        "oracle",
    ]

    summaries = [
        summarize_policy(
            all_results,
            policy,
        )
        for policy in policies
    ]

    winners = selection_frequency(
        all_results
    )

    print("=" * 180)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "MULTI-SEED BALANCED "
        "PERSISTENCE ROBUSTNESS"
    )

    print("=" * 180)

    print(
        f"decision contexts="
        f"{len(rows)}"
    )

    print(
        f"seeds="
        f"{len(SEEDS)}"
    )

    print(
        f"seed values="
        f"{SEEDS}"
    )

    print()

    print(
        "MULTI-SEED POLICY SUMMARY"
    )

    for summary in summaries:

        print_summary(
            summary
        )

    print()

    print(
        "COLLAPSE-AWARE SELECTION "
        "FREQUENCY"
    )

    total_selected = sum(
        winners.values()
    )

    for policy, count in (
        winners.most_common()
    ):

        print(
            f"{policy:<20} "
            f"{count}/"
            f"{total_selected} "
            f"({count / total_selected:.1%})"
        )

    print("=" * 180)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()