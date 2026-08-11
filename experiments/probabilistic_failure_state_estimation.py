import csv
import math
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path


INPUT_PATH = Path(
    "results/criterion_failure_decomposition.csv"
)

OUTPUT_PATH = Path(
    "results/probabilistic_failure_state_estimation.csv"
)


BATCH_SIZES = [
    5,
    10,
    20,
    50,
]

BOOTSTRAP_REPLICATES = 500

RANDOM_SEED = 35035


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


def mode_distribution(
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


def marginal_failure_probabilities(
    rows: list[dict],
) -> dict:

    total = len(rows)

    p_a = (
        sum(
            row["fail_A"] == "True"
            for row in rows
        )
        / total
    )

    p_c = (
        sum(
            row["fail_C"] == "True"
            for row in rows
        )
        / total
    )

    p_s = (
        sum(
            row["fail_S"] == "True"
            for row in rows
        )
        / total
    )

    return {
        "p_fail_A":
            p_a,

        "p_fail_C":
            p_c,

        "p_fail_S":
            p_s,
    }


def l1_distance(
    estimate: dict[str, float],
    reference: dict[str, float],
) -> float:

    return sum(
        abs(
            estimate[mode]
            - reference[mode]
        )
        for mode in FAILURE_MODES
    )


def total_variation_distance(
    estimate: dict[str, float],
    reference: dict[str, float],
) -> float:

    return (
        0.5
        * l1_distance(
            estimate,
            reference,
        )
    )


def jensen_shannon_divergence(
    estimate: dict[str, float],
    reference: dict[str, float],
) -> float:

    midpoint = {
        mode:
            (
                estimate[mode]
                + reference[mode]
            )
            / 2.0
        for mode in FAILURE_MODES
    }

    def kl_divergence(
        p: dict[str, float],
        q: dict[str, float],
    ) -> float:

        total = 0.0

        for mode in FAILURE_MODES:

            p_value = p[mode]
            q_value = q[mode]

            if p_value <= 0.0:
                continue

            total += (
                p_value
                * math.log(
                    p_value
                    / q_value,
                    2,
                )
            )

        return total

    return (
        0.5
        * kl_divergence(
            estimate,
            midpoint,
        )
        +
        0.5
        * kl_divergence(
            reference,
            midpoint,
        )
    )


def sample_batch(
    rows: list[dict],
    *,
    batch_size: int,
    rng: random.Random,
) -> list[dict]:

    return rng.sample(
        rows,
        batch_size,
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

    for condition, group in groups.items():

        reference_distribution = (
            mode_distribution(
                group
            )
        )

        reference_marginals = (
            marginal_failure_probabilities(
                group
            )
        )

        for batch_size in BATCH_SIZES:

            for replicate in range(
                BOOTSTRAP_REPLICATES
            ):

                batch = sample_batch(
                    group,
                    batch_size=batch_size,
                    rng=rng,
                )

                estimated_distribution = (
                    mode_distribution(
                        batch
                    )
                )

                estimated_marginals = (
                    marginal_failure_probabilities(
                        batch
                    )
                )

                marginal_mae = statistics.mean(
                    [
                        abs(
                            estimated_marginals[
                                "p_fail_A"
                            ]
                            - reference_marginals[
                                "p_fail_A"
                            ]
                        ),
                        abs(
                            estimated_marginals[
                                "p_fail_C"
                            ]
                            - reference_marginals[
                                "p_fail_C"
                            ]
                        ),
                        abs(
                            estimated_marginals[
                                "p_fail_S"
                            ]
                            - reference_marginals[
                                "p_fail_S"
                            ]
                        ),
                    ]
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

                        "reference_p_fail_A":
                            reference_marginals[
                                "p_fail_A"
                            ],

                        "reference_p_fail_C":
                            reference_marginals[
                                "p_fail_C"
                            ],

                        "reference_p_fail_S":
                            reference_marginals[
                                "p_fail_S"
                            ],

                        "estimated_p_fail_A":
                            estimated_marginals[
                                "p_fail_A"
                            ],

                        "estimated_p_fail_C":
                            estimated_marginals[
                                "p_fail_C"
                            ],

                        "estimated_p_fail_S":
                            estimated_marginals[
                                "p_fail_S"
                            ],

                        "marginal_mae":
                            marginal_mae,

                        "joint_l1":
                            l1_distance(
                                estimated_distribution,
                                reference_distribution,
                            ),

                        "joint_total_variation":
                            total_variation_distance(
                                estimated_distribution,
                                reference_distribution,
                            ),

                        "joint_js_divergence":
                            jensen_shannon_divergence(
                                estimated_distribution,
                                reference_distribution,
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

    print("=" * 118)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PROBABILISTIC FAILURE-STATE ESTIMATION"
    )

    print("=" * 118)

    for batch_size in BATCH_SIZES:

        group = [
            row
            for row in rows
            if int(
                row["batch_size"]
            )
            == batch_size
        ]

        mean_marginal_mae = (
            statistics.mean(
                float(
                    row["marginal_mae"]
                )
                for row in group
            )
        )

        mean_total_variation = (
            statistics.mean(
                float(
                    row[
                        "joint_total_variation"
                    ]
                )
                for row in group
            )
        )

        mean_js_divergence = (
            statistics.mean(
                float(
                    row[
                        "joint_js_divergence"
                    ]
                )
                for row in group
            )
        )

        print(
            f"n={batch_size:<3} "
            f"marginal_MAE="
            f"{mean_marginal_mae:.4f} "
            f"TV="
            f"{mean_total_variation:.4f} "
            f"JS="
            f"{mean_js_divergence:.4f}"
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