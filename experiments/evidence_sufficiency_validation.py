import csv
import statistics
from pathlib import Path

from experiments.out_of_sample_attribution_generalization import (
    CONFIDENCE_THRESHOLD,
    run_single_trial,
)


RUNS_PER_CONDITION = 60

MARGIN_THRESHOLD = 0.20
SCORE_SPREAD_THRESHOLD = 1.00

OUTPUT_PATH = Path(
    "results/evidence_sufficiency_validation.csv"
)


VALIDATION_CONDITIONS = [
    {
        "class": "measurement_noise",
        "name": "measurement_noise_0.90",
        "measurement_noise_std": 0.90,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "measurement_noise",
        "name": "measurement_noise_1.10",
        "measurement_noise_std": 1.10,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "process_disturbance",
        "name": "process_disturbance_2.25",
        "measurement_noise_std": 0.50,
        "process_disturbance": 2.25,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "process_disturbance",
        "name": "process_disturbance_2.75",
        "measurement_noise_std": 0.50,
        "process_disturbance": 2.75,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "name": "parameter_mismatch_0.375",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.375,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "name": "parameter_mismatch_0.325",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.325,
        "changed_true_a": None,
    },
    {
        "class": "structural_change",
        "name": "structural_change_0.865",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": 0.865,
    },
    {
        "class": "structural_change",
        "name": "structural_change_0.845",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": 0.845,
    },
]


def evidence_prediction(
    trial: dict,
) -> bool:

    scores = [
        float(
            trial[
                "measurement_noise_score"
            ]
        ),
        float(
            trial[
                "process_disturbance_score"
            ]
        ),
        float(
            trial[
                "parameter_mismatch_score"
            ]
        ),
        float(
            trial[
                "structural_change_score"
            ]
        ),
    ]

    score_spread = (
        max(scores)
        - min(scores)
    )

    margin = float(
        trial[
            "classification_margin"
        ]
    )

    return (
        margin
        >= MARGIN_THRESHOLD
        and
        score_spread
        >= SCORE_SPREAD_THRESHOLD
    )


def operating_point_label(
    trials: list[dict],
) -> bool:

    hard_accuracy = (
        sum(
            trial["correct"]
            for trial in trials
        )
        / len(trials)
    )

    accepted = [
        trial
        for trial in trials
        if trial["accepted"]
    ]

    coverage = (
        len(accepted)
        / len(trials)
    )

    if accepted:

        selective_accuracy = (
            sum(
                trial[
                    "accepted_correct"
                ]
                for trial in accepted
            )
            / len(accepted)
        )

    else:

        selective_accuracy = 0.0

    return (
        hard_accuracy
        >= 0.90
        and
        coverage
        >= 0.80
        and
        selective_accuracy
        >= 0.95
    )


def summarize_condition(
    condition: dict,
) -> tuple[
    list[dict],
    dict,
]:

    trials = [
        run_single_trial(
            condition=condition,
            seed=(
                1000 + seed
            ),
        )
        for seed in range(
            RUNS_PER_CONDITION
        )
    ]

    label = operating_point_label(
        trials
    )

    rows = []

    for trial in trials:

        predicted_sufficient = (
            evidence_prediction(
                trial
            )
        )

        scores = [
            float(
                trial[
                    "measurement_noise_score"
                ]
            ),
            float(
                trial[
                    "process_disturbance_score"
                ]
            ),
            float(
                trial[
                    "parameter_mismatch_score"
                ]
            ),
            float(
                trial[
                    "structural_change_score"
                ]
            ),
        ]

        rows.append(
            {
                "condition":
                    condition["name"],

                "true_class":
                    condition["class"],

                "seed":
                    trial["seed"],

                "operating_point_evidence_sufficient":
                    label,

                "predicted_evidence_sufficient":
                    predicted_sufficient,

                "evidence_prediction_correct":
                    predicted_sufficient
                    == label,

                "classification_correct":
                    trial["correct"],

                "classification_margin":
                    trial[
                        "classification_margin"
                    ],

                "score_spread":
                    (
                        max(scores)
                        - min(scores)
                    ),
            }
        )

    hard_accuracy = (
        sum(
            trial["correct"]
            for trial in trials
        )
        / len(trials)
    )

    accepted = [
        trial
        for trial in trials
        if trial["accepted"]
    ]

    if accepted:

        selective_accuracy = (
            sum(
                trial[
                    "accepted_correct"
                ]
                for trial in accepted
            )
            / len(accepted)
        )

    else:

        selective_accuracy = 0.0

    predicted_fraction = (
        sum(
            row[
                "predicted_evidence_sufficient"
            ]
            for row in rows
        )
        / len(rows)
    )

    summary = {
        "condition":
            condition["name"],

        "true_class":
            condition["class"],

        "runs":
            len(trials),

        "hard_accuracy":
            hard_accuracy,

        "selective_coverage":
            len(accepted)
            / len(trials),

        "selective_accuracy":
            selective_accuracy,

        "operating_point_evidence_sufficient":
            label,

        "predicted_sufficient_fraction":
            predicted_fraction,

        "mean_margin":
            statistics.mean(
                float(
                    row[
                        "classification_margin"
                    ]
                )
                for row in rows
            ),

        "mean_score_spread":
            statistics.mean(
                float(
                    row[
                        "score_spread"
                    ]
                )
                for row in rows
            ),
    }

    return rows, summary


def run_experiment() -> tuple[
    list[dict],
    list[dict],
]:

    all_rows = []
    summaries = []

    for condition in (
        VALIDATION_CONDITIONS
    ):

        rows, summary = (
            summarize_condition(
                condition
            )
        )

        all_rows.extend(
            rows
        )

        summaries.append(
            summary
        )

    return (
        all_rows,
        summaries,
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


def print_summary(
    rows: list[dict],
    summaries: list[dict],
) -> None:

    correct = sum(
        row[
            "evidence_prediction_correct"
        ]
        for row in rows
    )

    tp = sum(
        row[
            "predicted_evidence_sufficient"
        ]
        and
        row[
            "operating_point_evidence_sufficient"
        ]
        for row in rows
    )

    tn = sum(
        not row[
            "predicted_evidence_sufficient"
        ]
        and
        not row[
            "operating_point_evidence_sufficient"
        ]
        for row in rows
    )

    fp = sum(
        row[
            "predicted_evidence_sufficient"
        ]
        and
        not row[
            "operating_point_evidence_sufficient"
        ]
        for row in rows
    )

    fn = sum(
        not row[
            "predicted_evidence_sufficient"
        ]
        and
        row[
            "operating_point_evidence_sufficient"
        ]
        for row in rows
    )

    precision = (
        tp / (tp + fp)
        if tp + fp
        else 0.0
    )

    recall = (
        tp / (tp + fn)
        if tp + fn
        else 0.0
    )

    print("=" * 118)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "INDEPENDENT EVIDENCE-SUFFICIENCY VALIDATION"
    )

    print("=" * 118)

    print(
        f"Evidence-estimator accuracy: "
        f"{correct}/{len(rows)} "
        f"({correct / len(rows):.3%})"
    )

    print(
        f"Precision: "
        f"{precision:.3%}"
    )

    print(
        f"Recall: "
        f"{recall:.3%}"
    )

    print(
        f"TP={tp} "
        f"TN={tn} "
        f"FP={fp} "
        f"FN={fn}"
    )

    print()

    for summary in summaries:

        print(
            f"{summary['condition']:<32}"
            f"label="
            f"{str(summary['operating_point_evidence_sufficient']):<6} "
            f"pred_frac="
            f"{summary['predicted_sufficient_fraction']:<8.3%} "
            f"hard="
            f"{summary['hard_accuracy']:<8.3%} "
            f"coverage="
            f"{summary['selective_coverage']:<8.3%} "
            f"sel_acc="
            f"{summary['selective_accuracy']:<8.3%}"
        )

    print("=" * 118)


def main() -> None:

    rows, summaries = (
        run_experiment()
    )

    save_results(
        rows
    )

    print_summary(
        rows,
        summaries,
    )

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()