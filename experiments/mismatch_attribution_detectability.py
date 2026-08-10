import csv
import statistics
from pathlib import Path

from experiments.out_of_sample_attribution_generalization import (
    CONFIDENCE_THRESHOLD,
    run_single_trial,
)


RUNS_PER_MAGNITUDE = 50

OUTPUT_PATH = Path(
    "results/mismatch_attribution_detectability.csv"
)


SWEEPS = {
    "measurement_noise": [
        {
            "value": 0.55,
            "condition": {
                "class": "measurement_noise",
                "name": "measurement_noise_0.55",
                "measurement_noise_std": 0.55,
                "process_disturbance": 0.0,
                "initial_parameter_estimate": 0.50,
                "changed_true_a": None,
            },
        },
        {
            "value": 0.65,
            "condition": {
                "class": "measurement_noise",
                "name": "measurement_noise_0.65",
                "measurement_noise_std": 0.65,
                "process_disturbance": 0.0,
                "initial_parameter_estimate": 0.50,
                "changed_true_a": None,
            },
        },
        {
            "value": 0.75,
            "condition": {
                "class": "measurement_noise",
                "name": "measurement_noise_0.75",
                "measurement_noise_std": 0.75,
                "process_disturbance": 0.0,
                "initial_parameter_estimate": 0.50,
                "changed_true_a": None,
            },
        },
        {
            "value": 0.85,
            "condition": {
                "class": "measurement_noise",
                "name": "measurement_noise_0.85",
                "measurement_noise_std": 0.85,
                "process_disturbance": 0.0,
                "initial_parameter_estimate": 0.50,
                "changed_true_a": None,
            },
        },
        {
            "value": 1.00,
            "condition": {
                "class": "measurement_noise",
                "name": "measurement_noise_1.00",
                "measurement_noise_std": 1.00,
                "process_disturbance": 0.0,
                "initial_parameter_estimate": 0.50,
                "changed_true_a": None,
            },
        },
        {
            "value": 1.25,
            "condition": {
                "class": "measurement_noise",
                "name": "measurement_noise_1.25",
                "measurement_noise_std": 1.25,
                "process_disturbance": 0.0,
                "initial_parameter_estimate": 0.50,
                "changed_true_a": None,
            },
        },
        {
            "value": 1.50,
            "condition": {
                "class": "measurement_noise",
                "name": "measurement_noise_1.50",
                "measurement_noise_std": 1.50,
                "process_disturbance": 0.0,
                "initial_parameter_estimate": 0.50,
                "changed_true_a": None,
            },
        },
    ],

    "process_disturbance": [
        {
            "value": value,
            "condition": {
                "class": "process_disturbance",
                "name": f"process_disturbance_{value}",
                "measurement_noise_std": 0.50,
                "process_disturbance": value,
                "initial_parameter_estimate": 0.50,
                "changed_true_a": None,
            },
        }
        for value in [
            0.5,
            1.0,
            1.5,
            2.0,
            2.5,
            3.0,
            4.0,
        ]
    ],

    "parameter_mismatch": [
        {
            "value": abs(
                0.92 - estimate
            ),
            "condition": {
                "class": "parameter_mismatch",
                "name": f"parameter_mismatch_{estimate}",
                "measurement_noise_std": 0.50,
                "process_disturbance": 0.0,
                "initial_parameter_estimate": estimate,
                "changed_true_a": None,
            },
        }
        for estimate in [
            0.45,
            0.40,
            0.35,
            0.30,
            0.20,
            0.10,
        ]
    ],

    "structural_change": [
        {
            "value": abs(
                0.92 - changed_a
            ),
            "condition": {
                "class": "structural_change",
                "name": f"structural_change_{changed_a}",
                "measurement_noise_std": 0.50,
                "process_disturbance": 0.0,
                "initial_parameter_estimate": 0.50,
                "changed_true_a": changed_a,
            },
        }
        for changed_a in [
            0.90,
            0.88,
            0.85,
            0.82,
            0.80,
            0.75,
        ]
    ],
}


def summarize_operating_point(
    *,
    mismatch_class: str,
    mismatch_strength: float,
    condition: dict,
) -> dict:

    trials = [
        run_single_trial(
            condition=condition,
            seed=seed,
        )
        for seed in range(
            RUNS_PER_MAGNITUDE
        )
    ]

    correct_count = sum(
        trial["correct"]
        for trial in trials
    )

    accepted_trials = [
        trial
        for trial in trials
        if trial["accepted"]
    ]

    accepted_correct = sum(
        trial["accepted_correct"]
        for trial in accepted_trials
    )

    margins = [
        float(
            trial[
                "classification_margin"
            ]
        )
        for trial in trials
    ]

    if accepted_trials:

        selective_accuracy = (
            accepted_correct
            / len(accepted_trials)
        )

    else:

        selective_accuracy = None

    return {
        "mismatch_class":
            mismatch_class,

        "condition":
            condition["name"],

        "mismatch_strength":
            mismatch_strength,

        "runs":
            len(trials),

        "hard_accuracy":
            correct_count
            / len(trials),

        "selective_coverage":
            len(accepted_trials)
            / len(trials),

        "selective_accuracy":
            selective_accuracy,

        "mean_classification_margin":
            statistics.mean(
                margins
            ),

        "std_classification_margin":
            statistics.stdev(
                margins
            ),

        "confidence_threshold":
            CONFIDENCE_THRESHOLD,
    }


def run_experiment() -> list[dict]:

    rows = []

    for mismatch_class, sweep in (
        SWEEPS.items()
    ):

        for operating_point in sweep:

            rows.append(
                summarize_operating_point(
                    mismatch_class=(
                        mismatch_class
                    ),
                    mismatch_strength=(
                        operating_point[
                            "value"
                        ]
                    ),
                    condition=(
                        operating_point[
                            "condition"
                        ]
                    ),
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


def format_selective_accuracy(
    value,
) -> str:

    if value is None:
        return "N/A"

    return f"{value:.3%}"


def print_summary(
    rows: list[dict],
) -> None:

    print("=" * 118)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "MISMATCH ATTRIBUTION DETECTABILITY BOUNDARY"
    )

    print("=" * 118)

    for mismatch_class in SWEEPS:

        print(
            f"\n{mismatch_class}"
        )

        class_rows = [
            row
            for row in rows
            if row[
                "mismatch_class"
            ]
            == mismatch_class
        ]

        class_rows.sort(
            key=lambda row:
                row[
                    "mismatch_strength"
                ]
        )

        for row in class_rows:

            print(
                f"  "
                f"strength="
                f"{row['mismatch_strength']:<8.3f} "
                f"hard="
                f"{row['hard_accuracy']:<8.3%} "
                f"coverage="
                f"{row['selective_coverage']:<8.3%} "
                f"accepted="
                f"{format_selective_accuracy(row['selective_accuracy']):<9} "
                f"margin="
                f"{row['mean_classification_margin']:.4f}"
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