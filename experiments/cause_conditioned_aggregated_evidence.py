import csv
import random
from collections import defaultdict
from pathlib import Path


INPUT_PATH = Path(
    "results/balanced_evidence_boundary_sampling.csv"
)

OUTPUT_PATH = Path(
    "results/cause_conditioned_aggregated_evidence.csv"
)


BATCH_SIZES = [
    1,
    2,
    5,
    10,
    20,
    50,
]

BOOTSTRAP_REPLICATES = 500

RANDOM_SEED = 29029


CAUSES = [
    "measurement_noise",
    "process_disturbance",
    "parameter_mismatch",
    "structural_change",
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


def infer_cause(
    condition: str,
) -> str:

    for cause in CAUSES:

        prefix = (
            cause
            + "_"
        )

        if condition.startswith(
            prefix
        ):

            return cause

    raise ValueError(
        f"Unable to infer cause "
        f"from condition: "
        f"{condition}"
    )


def group_rows(
    rows: list[dict],
) -> dict:

    groups = defaultdict(
        list
    )

    for row in rows:

        key = (
            row["true_class"],
            row["condition"],
        )

        groups[key].append(
            row
        )

    return groups


def trajectory_vote(
    row: dict,
) -> float:

    cause = row[
        "true_class"
    ]

    classification_margin = float(
        row[
            "classification_margin"
        ]
    )

    recovery_ratio_nis = float(
        row[
            "recovery_ratio_nis"
        ]
    )

    parameter_shift = float(
        row[
            "parameter_shift_post_vs_pre"
        ]
    )

    cumulative_update = float(
        row[
            "post_cumulative_abs_parameter_update"
        ]
    )

    if cause == "measurement_noise":

        prediction = (
            classification_margin
            >= 0.5162128944351736
            and
            cumulative_update
            >= 0.09534309010684958
        )

    elif cause == "process_disturbance":

        prediction = (
            recovery_ratio_nis
            <= 0.34013237768129045
        )

    elif cause == "parameter_mismatch":

        prediction = (
            classification_margin
            >= 0.5733833425128738
        )

    elif cause == "structural_change":

        prediction = (
            parameter_shift
            <= -0.049260128858973906
        )

    else:

        raise ValueError(
            f"Unknown cause: "
            f"{cause}"
        )

    return (
        1.0
        if prediction
        else 0.0
    )

def condition_label(
    rows: list[dict],
) -> bool:

    return (
        rows[0][
            "evidence_sufficient"
        ]
        == "True"
    )

def sample_vote_fraction(
    rows: list[dict],
    *,
    batch_size: int,
    rng: random.Random,
) -> float:

    sample = rng.sample(
        rows,
        batch_size,
    )

    return (
        sum(
            trajectory_vote(
                row
            )
            for row in sample
        )
        / batch_size
    )


def build_cause_dataset(
    groups: dict,
    *,
    cause: str,
    batch_size: int,
    rng: random.Random,
) -> list[dict]:

    dataset = []

    for (
        group_cause,
        condition,
    ), rows in groups.items():

        if group_cause != cause:
            continue

        label = condition_label(
            rows
        )

        for _ in range(
            BOOTSTRAP_REPLICATES
        ):

            dataset.append(
                {
                    "cause":
                        cause,

                    "condition":
                        condition,

                    "batch_size":
                        batch_size,

                    "vote_fraction":
                        sample_vote_fraction(
                            rows,
                            batch_size=(
                                batch_size
                            ),
                            rng=rng,
                        ),

                    "evidence_sufficient":
                        label,
                }
            )

    return dataset


def threshold_candidates(
    values: list[float],
) -> list[float]:

    unique_values = sorted(
        set(
            values
        )
    )

    candidates = [
        0.0,
        1.0,
    ]

    candidates.extend(
        unique_values
    )

    for left, right in zip(
        unique_values,
        unique_values[1:],
    ):

        candidates.append(
            (
                left
                + right
            )
            / 2.0
        )

    return sorted(
        set(
            candidates
        )
    )


def evaluate_rule(
    rows: list[dict],
    *,
    threshold: float,
    direction: str,
) -> dict:

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for row in rows:

        value = float(
            row["vote_fraction"]
        )

        if direction == ">=":

            prediction = (
                value
                >= threshold
            )

        elif direction == "<=":

            prediction = (
                value
                <= threshold
            )

        else:

            raise ValueError(
                direction
            )

        actual = bool(
            row[
                "evidence_sufficient"
            ]
        )

        if prediction and actual:
            tp += 1

        elif (
            not prediction
            and not actual
        ):
            tn += 1

        elif prediction:
            fp += 1

        else:
            fn += 1

    recall = (
        tp
        / (tp + fn)
        if tp + fn
        else 0.0
    )

    specificity = (
        tn
        / (tn + fp)
        if tn + fp
        else 0.0
    )

    precision = (
        tp
        / (tp + fp)
        if tp + fp
        else 0.0
    )

    accuracy = (
        (tp + tn)
        / len(rows)
    )

    balanced_accuracy = (
        (
            recall
            + specificity
        )
        / 2.0
    )

    return {
        "accuracy":
            accuracy,

        "balanced_accuracy":
            balanced_accuracy,

        "precision":
            precision,

        "recall":
            recall,

        "specificity":
            specificity,

        "tp":
            tp,

        "tn":
            tn,

        "fp":
            fp,

        "fn":
            fn,
    }


def search_best_rule(
    rows: list[dict],
) -> dict:

    values = [
        float(
            row[
                "vote_fraction"
            ]
        )
        for row in rows
    ]

    candidates = []

    for threshold in (
        threshold_candidates(
            values
        )
    ):

        for direction in [
            ">=",
            "<=",
        ]:

            metrics = (
                evaluate_rule(
                    rows,
                    threshold=threshold,
                    direction=direction,
                )
            )

            candidates.append(
                {
                    "threshold":
                        threshold,

                    "direction":
                        direction,

                    **metrics,
                }
            )

    return max(
        candidates,
        key=lambda row: (
            row[
                "balanced_accuracy"
            ],
            row[
                "accuracy"
            ],
            min(
                row[
                    "precision"
                ],
                row[
                    "recall"
                ],
            ),
        ),
    )


def run_experiment() -> list[dict]:

    rows = load_rows()

    groups = group_rows(
        rows
    )

    rng = random.Random(
        RANDOM_SEED
    )

    results = []

    for cause in CAUSES:

        for batch_size in (
            BATCH_SIZES
        ):

            dataset = (
                build_cause_dataset(
                    groups,
                    cause=cause,
                    batch_size=(
                        batch_size
                    ),
                    rng=rng,
                )
            )

            sufficient_count = sum(
                row["evidence_sufficient"]
                for row in dataset
            )

            insufficient_count = (
                len(dataset)
                - sufficient_count
            )

            if (
                sufficient_count == 0
                or insufficient_count == 0
            ):

                raise RuntimeError(
                    f"Cause {cause!r}, "
                    f"n={batch_size}: "
                    f"expected both evidence classes; "
                    f"got sufficient="
                    f"{sufficient_count}, "
                    f"insufficient="
                    f"{insufficient_count}"
                )

            best = (
                search_best_rule(
                    dataset
                )
            )

            sufficient_values = [
                float(
                    row[
                        "vote_fraction"
                    ]
                )
                for row in dataset
                if row[
                    "evidence_sufficient"
                ]
            ]

            insufficient_values = [
                float(
                    row[
                        "vote_fraction"
                    ]
                )
                for row in dataset
                if not row[
                    "evidence_sufficient"
                ]
            ]

            results.append(
                {
                    "cause":
                        cause,

                    "batch_size":
                        batch_size,

                    "threshold":
                        best[
                            "threshold"
                        ],

                    "direction":
                        best[
                            "direction"
                        ],

                    "accuracy":
                        best[
                            "accuracy"
                        ],

                    "balanced_accuracy":
                        best[
                            "balanced_accuracy"
                        ],

                    "precision":
                        best[
                            "precision"
                        ],

                    "recall":
                        best[
                            "recall"
                        ],

                    "specificity":
                        best[
                            "specificity"
                        ],

                    "tp":
                        best[
                            "tp"
                        ],

                    "tn":
                        best[
                            "tn"
                        ],

                    "fp":
                        best[
                            "fp"
                        ],

                    "fn":
                        best[
                            "fn"
                        ],

                    "mean_vote_sufficient":
                        (
                            sum(
                                sufficient_values
                            )
                            / len(
                                sufficient_values
                            )
                        ),

                    "mean_vote_insufficient":
                        (
                            sum(
                                insufficient_values
                            )
                            / len(
                                insufficient_values
                            )
                        ),

                    "bootstrap_replicates":
                        BOOTSTRAP_REPLICATES,
                }
            )

    return results


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
        "ADAPTIVE DIGITAL TWIN — "
        "CAUSE-CONDITIONED AGGREGATED EVIDENCE"
    )

    print("=" * 118)

    for cause in CAUSES:

        print(
            f"\n{cause}"
        )

        cause_rows = [
            row
            for row in rows
            if row["cause"]
            == cause
        ]

        for row in cause_rows:

            print(
                f"  "
                f"n={int(row['batch_size']):<3} "
                f"acc="
                f"{float(row['accuracy']):<8.3%} "
                f"bal_acc="
                f"{float(row['balanced_accuracy']):<8.3%} "
                f"precision="
                f"{float(row['precision']):<8.3%} "
                f"recall="
                f"{float(row['recall']):<8.3%} "
                f"rule: "
                f"p "
                f"{row['direction']} "
                f"{float(row['threshold']):.4f}"
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