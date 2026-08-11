import csv
from pathlib import Path

from experiments.independent_aggregated_evidence_validation import (
    CONFIDENCE_THRESHOLD,
    extract_features,
    run_trajectory,
)

from experiments.mismatch_classification import (
    classify_row,
)


POPULATION_SIZE = 100
POPULATION_REPLICATES = 50

BASE_SEED = 33000
SEED_STRIDE = 1000

OUTPUT_PATH = Path(
    "results/criterion_failure_decomposition.csv"
)


CONDITIONS = [
    # Measurement-noise transition
    {
        "class": "measurement_noise",
        "name": "measurement_noise_0.850",
        "magnitude": 0.850,
        "measurement_noise_std": 0.850,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "measurement_noise",
        "name": "measurement_noise_0.900",
        "magnitude": 0.900,
        "measurement_noise_std": 0.900,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "measurement_noise",
        "name": "measurement_noise_0.950",
        "magnitude": 0.950,
        "measurement_noise_std": 0.950,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },

    # Process-disturbance transition
    *[
        {
            "class": "process_disturbance",
            "name": f"process_disturbance_{value:.2f}",
            "magnitude": value,
            "measurement_noise_std": 0.50,
            "process_disturbance": value,
            "initial_parameter_estimate": 0.50,
            "changed_true_a": None,
        }
        for value in [
            2.50,
            2.60,
            2.70,
            2.80,
            2.90,
        ]
    ],

    # Parameter-mismatch transition
    {
        "class": "parameter_mismatch",
        "name": "parameter_mismatch_delta_0.495",
        "magnitude": 0.495,
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.425,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "name": "parameter_mismatch_delta_0.520",
        "magnitude": 0.520,
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.400,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "name": "parameter_mismatch_delta_0.545",
        "magnitude": 0.545,
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.375,
        "changed_true_a": None,
    },

    # Structural-change transition
    *[
        {
            "class": "structural_change",
            "name": f"structural_change_delta_{delta:.3f}",
            "magnitude": delta,
            "measurement_noise_std": 0.50,
            "process_disturbance": 0.0,
            "initial_parameter_estimate": 0.50,
            "changed_true_a": 0.92 - delta,
        }
        for delta in [
            0.050,
            0.055,
            0.060,
            0.065,
            0.070,
            0.075,
        ]
    ],
]


def classify_population(
    *,
    condition: dict,
    condition_index: int,
    replicate: int,
) -> list[dict]:

    classifications = []

    base_seed = (
        BASE_SEED
        + condition_index
        * POPULATION_REPLICATES
        * SEED_STRIDE
        + replicate
        * SEED_STRIDE
    )

    for offset in range(
        POPULATION_SIZE
    ):

        trajectory = run_trajectory(
            condition=condition,
            seed=base_seed + offset,
        )

        (
            global_features,
            temporal_features,
            adaptation_features,
        ) = extract_features(
            trajectory
        )

        classification = classify_row(
            regime=condition["class"],
            global_row=global_features,
            temporal_row=temporal_features,
            adaptation_row=adaptation_features,
        )

        classifications.append(
            classification
        )

    return classifications


def population_failure_state(
    classifications: list[dict],
) -> dict:

    hard_accuracy = (
        sum(
            item["correct"]
            for item in classifications
        )
        / len(classifications)
    )

    accepted = [
        item
        for item in classifications
        if float(
            item["classification_margin"]
        )
        >= CONFIDENCE_THRESHOLD
    ]

    coverage = (
        len(accepted)
        / len(classifications)
    )

    if accepted:

        selective_accuracy = (
            sum(
                item["correct"]
                for item in accepted
            )
            / len(accepted)
        )

    else:
        selective_accuracy = 0.0

    fail_a = (
        hard_accuracy < 0.90
    )

    fail_c = (
        coverage < 0.80
    )

    fail_s = (
        selective_accuracy < 0.95
    )

    evidence_sufficient = not (
        fail_a
        or fail_c
        or fail_s
    )

    if evidence_sufficient:
        failure_mode = "pass_all"

    elif (
        fail_a
        and not fail_c
        and not fail_s
    ):
        failure_mode = "A_only"

    elif (
        fail_c
        and not fail_a
        and not fail_s
    ):
        failure_mode = "C_only"

    elif (
        fail_s
        and not fail_a
        and not fail_c
    ):
        failure_mode = "S_only"

    elif (
        fail_a
        and fail_c
        and not fail_s
    ):
        failure_mode = "A_and_C"

    elif (
        fail_a
        and fail_s
        and not fail_c
    ):
        failure_mode = "A_and_S"

    elif (
        fail_c
        and fail_s
        and not fail_a
    ):
        failure_mode = "C_and_S"

    else:
        failure_mode = "A_and_C_and_S"

    return {
        "hard_accuracy":
            hard_accuracy,

        "coverage":
            coverage,

        "selective_accuracy":
            selective_accuracy,

        "fail_A":
            fail_a,

        "fail_C":
            fail_c,

        "fail_S":
            fail_s,

        "evidence_sufficient":
            evidence_sufficient,

        "failure_mode":
            failure_mode,
    }


def run_experiment() -> list[dict]:

    rows = []

    for (
        condition_index,
        condition,
    ) in enumerate(
        CONDITIONS
    ):

        for replicate in range(
            POPULATION_REPLICATES
        ):

            classifications = (
                classify_population(
                    condition=condition,
                    condition_index=condition_index,
                    replicate=replicate,
                )
            )

            state = (
                population_failure_state(
                    classifications
                )
            )

            rows.append(
                {
                    "condition":
                        condition["name"],

                    "true_class":
                        condition["class"],

                    "magnitude":
                        condition["magnitude"],

                    "replicate":
                        replicate,

                    "population_size":
                        POPULATION_SIZE,

                    **state,
                }
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


def print_summary(
    rows: list[dict],
) -> None:

    modes = [
        "A_only",
        "C_only",
        "S_only",
        "A_and_C",
        "A_and_S",
        "C_and_S",
        "A_and_C_and_S",
    ]

    print("=" * 128)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "CRITERION-COMPONENT FAILURE DECOMPOSITION"
    )

    print("=" * 128)

    for condition in CONDITIONS:

        group = [
            row
            for row in rows
            if row["condition"]
            == condition["name"]
        ]

        q = (
            sum(
                row["evidence_sufficient"]
                for row in group
            )
            / len(group)
        )

        fail_a = (
            sum(
                row["fail_A"]
                for row in group
            )
            / len(group)
        )

        fail_c = (
            sum(
                row["fail_C"]
                for row in group
            )
            / len(group)
        )

        fail_s = (
            sum(
                row["fail_S"]
                for row in group
            )
            / len(group)
        )

        mode_counts = {
            mode: (
                sum(
                    row["failure_mode"]
                    == mode
                    for row in group
                )
                / len(group)
            )
            for mode in modes
        }

        dominant_mode = max(
            modes,
            key=lambda mode:
                mode_counts[mode],
        )

        print(
            f"{condition['name']:<36}"
            f"q={q:<6.3f} "
            f"P(FA)={fail_a:<6.3f} "
            f"P(FC)={fail_c:<6.3f} "
            f"P(FS)={fail_s:<6.3f} "
            f"dominant="
            f"{dominant_mode:<14} "
            f"p="
            f"{mode_counts[dominant_mode]:.3f}"
        )

    print("=" * 128)


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