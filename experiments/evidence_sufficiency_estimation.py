import csv
import statistics
from pathlib import Path


DETECTABILITY_PATH = Path(
    "results/mismatch_attribution_detectability.csv"
)

CLASSIFICATION_PATH = Path(
    "results/out_of_sample_attribution_generalization.csv"
)

OUTPUT_PATH = Path(
    "results/evidence_sufficiency_estimation.csv"
)


MIN_HARD_ACCURACY = 0.90
MIN_COVERAGE = 0.80
MIN_SELECTIVE_ACCURACY = 0.95


def load_csv(
    path: Path,
) -> list[dict]:

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def is_evidence_sufficient(
    operating_point: dict,
) -> bool:

    selective_accuracy = (
        operating_point[
            "selective_accuracy"
        ]
    )

    if selective_accuracy in (
        "",
        "None",
    ):
        return False

    return (
        float(
            operating_point[
                "hard_accuracy"
            ]
        )
        >= MIN_HARD_ACCURACY
        and
        float(
            operating_point[
                "selective_coverage"
            ]
        )
        >= MIN_COVERAGE
        and
        float(
            selective_accuracy
        )
        >= MIN_SELECTIVE_ACCURACY
    )


def build_operating_point_labels(
    rows: list[dict],
) -> dict:

    labels = {}

    for row in rows:

        labels[
            row["condition"]
        ] = (
            is_evidence_sufficient(
                row
            )
        )

    return labels


def derive_observable_features(
    row: dict,
) -> dict:

    scores = [
        float(
            row[
                "measurement_noise_score"
            ]
        ),
        float(
            row[
                "process_disturbance_score"
            ]
        ),
        float(
            row[
                "parameter_mismatch_score"
            ]
        ),
        float(
            row[
                "structural_change_score"
            ]
        ),
    ]

    ordered_scores = sorted(
        scores,
        reverse=True,
    )

    top_score = (
        ordered_scores[0]
    )

    second_score = (
        ordered_scores[1]
    )

    mean_score = (
        statistics.mean(
            scores
        )
    )

    score_spread = (
        max(scores)
        - min(scores)
    )

    return {
        "classification_margin":
            float(
                row[
                    "classification_margin"
                ]
            ),

        "top_score":
            top_score,

        "second_score":
            second_score,

        "mean_score":
            mean_score,

        "score_spread":
            score_spread,

        "top_to_second_ratio":
            (
                top_score
                / (
                    second_score
                    + 1e-12
                )
            ),
    }


def build_dataset() -> list[dict]:

    detectability_rows = load_csv(
        DETECTABILITY_PATH
    )

    classification_rows = load_csv(
        CLASSIFICATION_PATH
    )

    labels = (
        build_operating_point_labels(
            detectability_rows
        )
    )

    output_rows = []

    for row in classification_rows:

        condition = row[
            "condition"
        ]

        if condition not in labels:
            continue

        features = (
            derive_observable_features(
                row
            )
        )

        output_rows.append(
            {
                "condition":
                    condition,

                "true_class":
                    row[
                        "true_class"
                    ],

                "seed":
                    int(
                        row["seed"]
                    ),

                "evidence_sufficient":
                    labels[
                        condition
                    ],

                "classification_correct":
                    (
                        row[
                            "correct"
                        ]
                        == "True"
                    ),

                **features,
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


def summarize_feature(
    rows: list[dict],
    *,
    feature: str,
    label: bool,
) -> tuple[
    float,
    float,
]:

    values = [
        float(
            row[feature]
        )
        for row in rows
        if row[
            "evidence_sufficient"
        ]
        == label
    ]

    return (
        statistics.mean(
            values
        ),
        statistics.stdev(
            values
        ),
    )


def print_summary(
    rows: list[dict],
) -> None:

    sufficient_rows = [
        row
        for row in rows
        if row[
            "evidence_sufficient"
        ]
    ]

    insufficient_rows = [
        row
        for row in rows
        if not row[
            "evidence_sufficient"
        ]
    ]

    features = [
        "classification_margin",
        "top_score",
        "second_score",
        "mean_score",
        "score_spread",
        "top_to_second_ratio",
    ]

    print("=" * 112)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "EVIDENCE SUFFICIENCY ESTIMATION"
    )

    print("=" * 112)

    print(
        f"Evidence-sufficient trajectories: "
        f"{len(sufficient_rows)}"
    )

    print(
        f"Evidence-insufficient trajectories: "
        f"{len(insufficient_rows)}"
    )

    print()

    for feature in features:

        sufficient_mean, sufficient_std = (
            summarize_feature(
                rows,
                feature=feature,
                label=True,
            )
        )

        insufficient_mean, insufficient_std = (
            summarize_feature(
                rows,
                feature=feature,
                label=False,
            )
        )

        print(
            f"{feature:<28}"
            f"sufficient="
            f"{sufficient_mean:.6f}"
            f" ± "
            f"{sufficient_std:.6f} "
            f"insufficient="
            f"{insufficient_mean:.6f}"
            f" ± "
            f"{insufficient_std:.6f}"
        )

    print("=" * 112)


def main() -> None:

    rows = build_dataset()

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