import csv
import hashlib
import json
from pathlib import Path

from experiments.persistent_online_change_point_epistemic_memory import (
    BASE_SEED,
    generate_trajectories,
)


OUTPUT_PATH = Path(
    "results/"
    "generative_seed_control_validation.csv"
)

TEST_SEEDS = [
    BASE_SEED,
    BASE_SEED,
    BASE_SEED + 1,
    BASE_SEED + 2,
    BASE_SEED + 100,
]


FINGERPRINT_FIELDS = [
    "condition",
    "true_class",
    "run_index",
    "split",
]


def trajectory_fingerprint(
    trajectories: list[dict],
) -> str:

    serializable = []

    for row in trajectories:

        record = {}

        for key, value in row.items():

            if isinstance(
                value,
                (
                    int,
                    float,
                    str,
                    bool,
                    type(None),
                ),
            ):

                record[
                    key
                ] = value

            elif isinstance(
                value,
                list,
            ):

                record[
                    key
                ] = [
                    (
                        round(
                            float(item),
                            12,
                        )
                        if isinstance(
                            item,
                            (
                                int,
                                float,
                            ),
                        )
                        else item
                    )
                    for item in value
                ]

        serializable.append(
            record
        )

    encoded = json.dumps(
        serializable,
        sort_keys=True,
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


def generate_record(
    requested_seed: int,
    execution_index: int,
) -> dict:

    trajectories = (
        generate_trajectories(
            base_seed=requested_seed
        )
    )

    fingerprint = (
        trajectory_fingerprint(
            trajectories
        )
    )

    return {
        "execution_index":
            execution_index,

        "requested_seed":
            requested_seed,

        "trajectory_count":
            len(
                trajectories
            ),

        "fingerprint":
            fingerprint,
    }


def save_results(
    records: list[dict],
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
            fieldnames=records[0].keys(),
        )

        writer.writeheader()

        writer.writerows(
            records
        )


def validate_same_seed(
    records: list[dict],
) -> bool:

    baseline = [
        row
        for row in records
        if row[
            "requested_seed"
        ]
        == BASE_SEED
    ]

    fingerprints = {
        row[
            "fingerprint"
        ]
        for row in baseline
    }

    return (
        len(
            fingerprints
        )
        == 1
    )


def validate_different_seeds(
    records: list[dict],
) -> bool:

    by_seed = {}

    for row in records:

        seed = int(
            row[
                "requested_seed"
            ]
        )

        by_seed.setdefault(
            seed,
            set(),
        ).add(
            row[
                "fingerprint"
            ]
        )

    representative_fingerprints = {
        next(
            iter(
                fingerprints
            )
        )
        for fingerprints
        in by_seed.values()
    }

    return (
        len(
            representative_fingerprints
        )
        == len(
            by_seed
        )
    )


def print_records(
    records: list[dict],
) -> None:

    print(
        "GENERATION RECORDS"
    )

    for row in records:

        print(
            f"execution="
            f"{row['execution_index']} "
            f"seed="
            f"{row['requested_seed']} "
            f"trajectories="
            f"{row['trajectory_count']} "
            f"fingerprint="
            f"{row['fingerprint'][:16]}..."
        )


def main() -> None:

    records = []

    for (
        execution_index,
        requested_seed,
    ) in enumerate(
        TEST_SEEDS,
        start=1,
    ):

        records.append(
            generate_record(
                requested_seed=requested_seed,
                execution_index=execution_index,
            )
        )

    save_results(
        records
    )

    same_seed_ok = (
        validate_same_seed(
            records
        )
    )

    different_seed_ok = (
        validate_different_seeds(
            records
        )
    )

    print("=" * 140)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "GENERATIVE SEED-CONTROL VALIDATION"
    )

    print("=" * 140)

    print(
        f"default base seed="
        f"{BASE_SEED}"
    )

    print(
        f"test seeds="
        f"{TEST_SEEDS}"
    )

    print()

    print_records(
        records
    )

    print()

    print(
        "SEED-CONTROL VALIDATION"
    )

    print(
        "same seed -> same fingerprint: "
        f"{same_seed_ok}"
    )

    print(
        "different seeds -> "
        "different fingerprints: "
        f"{different_seed_ok}"
    )

    print()

    if (
        same_seed_ok
        and different_seed_ok
    ):

        print(
            "GENERATOR SEED CONTROL: PASS"
        )

    else:

        print(
            "GENERATOR SEED CONTROL: FAIL"
        )

    print("=" * 140)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()