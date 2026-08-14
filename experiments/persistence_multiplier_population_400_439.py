import csv
import hashlib
import json
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)
from experiments.responsiveness_preserving_safe_persistence_control import (
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


OUTPUT_PATH = Path(
    "results/"
    "persistence_multiplier_population_400_439.csv"
)

FINGERPRINT_PATH = Path(
    "results/"
    "persistence_multiplier_population_400_439_fingerprints.csv"
)

SEEDS = list(range(400, 440))

FIXED_RISK_PENALTY = 0.010

POLICY_MULTIPLIERS = {
    "two_stage_0.25": 0.25,
    "two_stage_0.30": 0.30,
    "two_stage_0.35": 0.35,
    "two_stage_0.40": 0.40,
    "two_stage_0.45": 0.45,
    "two_stage_0.50": 0.50,
}


FINGERPRINT_FIELDS = [
    "loss_k1",
    "loss_k2",
    "loss_k3",
    "benefit_probability",
    "release_probability",
    "anchor_age",
    "trigger_score",
    "feature_distance",
    "current_mismatch_indicator",
    "current_parameter_estimate",
]


def seed_generation(
    seed: int,
) -> None:

    random.seed(
        seed
    )

    np.random.seed(
        seed
    )


def dataset_fingerprint(
    rows: list[dict],
) -> str:

    serializable = []

    for row in rows:

        serializable.append(
            [
                round(
                    float(
                        row[
                            field
                        ]
                    ),
                    12,
                )
                for field in FINGERPRINT_FIELDS
            ]
        )

    encoded = json.dumps(
        serializable,
        separators=(
            ",",
            ":",
        ),
    ).encode(
        "utf-8"
    )

    return hashlib.sha256(
        encoded
    ).hexdigest()


def generate_seed_dataset(
    seed: int,
) -> tuple[
    list[dict],
    str,
]:

    seed_generation(
        seed
    )

    rows = generate_analysis_rows(base_seed=seed)

    fingerprint = (
        dataset_fingerprint(
            rows
        )
    )

    return (
        rows,
        fingerprint,
    )


def adaptive_candidate(
    row: dict,
) -> bool:

    return row[
        "policy"
    ] in {
        "direct_loss",
        "fixed_risk_0.010",
        "two_stage_0.25",
        "two_stage_0.30",
        "two_stage_0.35",
        "two_stage_0.40",
        "two_stage_0.45",
        "two_stage_0.50",
    }


def dominates(
    left: dict,
    right: dict,
) -> bool:

    no_worse = (
        left[
            "mean_regret"
        ]
        <= right[
            "mean_regret"
        ]
        and left[
            "under_count"
        ]
        <= right[
            "under_count"
        ]
        and left[
            "over_count"
        ]
        <= right[
            "over_count"
        ]
        and left[
            "action_entropy"
        ]
        >= right[
            "action_entropy"
        ]
    )

    strictly_better = (
        left[
            "mean_regret"
        ]
        < right[
            "mean_regret"
        ]
        or left[
            "under_count"
        ]
        < right[
            "under_count"
        ]
        or left[
            "over_count"
        ]
        < right[
            "over_count"
        ]
        or left[
            "action_entropy"
        ]
        > right[
            "action_entropy"
        ]
    )

    return (
        no_worse
        and strictly_better
    )


def pareto_policies(
    rows: list[dict],
) -> set[str]:

    candidates = [
        row
        for row in rows
        if adaptive_candidate(
            row
        )
    ]

    frontier = set()

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

            frontier.add(
                candidate[
                    "policy"
                ]
            )

    return frontier


def evaluate_generated_dataset(
    rows: list[dict],
    seed: int,
    fingerprint: str,
) -> list[dict]:

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

    frontier = pareto_policies(
        evaluations
    )

    output = []

    for result in evaluations:

        record = dict(
            result
        )

        record[
            "seed"
        ] = seed

        record[
            "dataset_fingerprint"
        ] = fingerprint

        record[
            "context_count"
        ] = len(
            rows
        )

        record[
            "train_count"
        ] = len(
            train_rows
        )

        record[
            "test_count"
        ] = len(
            test_rows
        )

        record[
            "pareto_efficient"
        ] = int(
            result[
                "policy"
            ]
            in frontier
        )

        output.append(
            record
        )

    return output


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


def save_fingerprints(
    records: list[dict],
) -> None:

    FINGERPRINT_PATH.parent.mkdir(
        exist_ok=True
    )

    with FINGERPRINT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "seed",
                "context_count",
                "fingerprint",
            ],
        )

        writer.writeheader()
        writer.writerows(
            records
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


def print_fingerprint_summary(
    fingerprint_records: list[dict],
) -> None:

    fingerprints = [
        row[
            "fingerprint"
        ]
        for row in fingerprint_records
    ]

    unique = set(
        fingerprints
    )

    counts = Counter(
        fingerprints
    )

    print(
        "GENERATION DIVERSITY"
    )

    print(
        f"unique dataset fingerprints="
        f"{len(unique)}/"
        f"{len(fingerprints)}"
    )

    for index, (
        fingerprint,
        count,
    ) in enumerate(
        counts.most_common(),
        start=1,
    ):

        print(
            f"  fingerprint {index}: "
            f"{fingerprint[:16]}... "
            f"count={count}"
        )

    if len(unique) == 1:

        print()

        print(
            "WARNING: all seeds produced the "
            "same analysis dataset."
        )

        print(
            "The upstream trajectory generator "
            "appears internally deterministic or "
            "uses fixed seeds."
        )

        print(
            "This run does NOT establish true "
            "generative robustness."
        )

    else:

        print()

        print(
            "Independent seed values produced "
            "distinct analysis datasets."
        )


def main() -> None:

    all_results = []

    fingerprint_records = []

    for seed in SEEDS:

        (
            rows,
            fingerprint,
        ) = generate_seed_dataset(
            seed
        )

        fingerprint_records.append(
            {
                "seed":
                    seed,

                "context_count":
                    len(
                        rows
                    ),

                "fingerprint":
                    fingerprint,
            }
        )

        seed_results = (
            evaluate_generated_dataset(
                rows,
                seed,
                fingerprint,
            )
        )

        all_results.extend(
            seed_results
        )

    save_results(
        all_results
    )

    save_fingerprints(
        fingerprint_records
    )

    policies = [
        "direct_loss",
        "fixed_risk_0.010",
        "two_stage_0.25",
        "two_stage_0.30",
        "two_stage_0.35",
        "two_stage_0.40",
        "two_stage_0.45",
        "two_stage_0.50",
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

    print("=" * 180)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "MULTI-SEED GENERATIVE "
        "PERSISTENCE ROBUSTNESS"
    )

    print("=" * 180)

    print(
        f"seeds="
        f"{len(SEEDS)}"
    )

    print(
        f"seed values="
        f"{SEEDS}"
    )

    print()

    print_fingerprint_summary(
        fingerprint_records
    )

    print()

    print(
        "MULTI-SEED POLICY SUMMARY"
    )

    for summary in summaries:

        print_summary(
            summary
        )

    print("=" * 180)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Dataset fingerprints saved to: "
        f"{FINGERPRINT_PATH}"
    )


if __name__ == "__main__":
    main()