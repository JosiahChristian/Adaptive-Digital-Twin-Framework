import csv
import math
from pathlib import Path

from simulation.adaptive_scalar_system import (
    TRUE_A,
    run_experiment,
    summarize_experiment,
)


LEARNING_RATES = [
    2.00,
    2.01,
    2.02,
    2.03,
    2.04,
    2.05,
    2.06,
    2.07,
    2.08,
    2.09,
    2.10,
    2.11,
    2.12,
    2.13,
    2.14,
    2.15,
    2.16,
    2.17,
    2.18,
    2.19,
    2.20,
]

NOISE_STD_DEV = 0.0
RANDOM_SEED = 42

CONVERGENCE_TOLERANCE = 0.01
PARAMETER_BOUND = 2.0


def calculate_convergence_step(
    records: list[dict],
) -> int | None:

    for index, record in enumerate(records):

        remaining_records = records[index:]

        if all(
            abs(TRUE_A - item["estimated_a"])
            <= CONVERGENCE_TOLERANCE
            for item in remaining_records
        ):
            return record["step"]

    return None


def calculate_max_parameter_error(
    records: list[dict],
) -> float:

    return max(
        abs(TRUE_A - record["estimated_a"])
        for record in records
    )


def calculate_sign_changes(
    records: list[dict],
) -> int:
    """
    Counts changes in the sign of parameter estimation error.

    Repeated sign changes provide a simple indicator of
    oscillation around the true parameter.
    """

    errors = [
        record["estimated_a"] - TRUE_A
        for record in records
    ]

    sign_changes = 0
    previous_sign = None

    for error in errors:

        if math.isclose(error, 0.0, abs_tol=1e-12):
            continue

        current_sign = (
            1 if error > 0.0 else -1
        )

        if (
            previous_sign is not None
            and current_sign != previous_sign
        ):
            sign_changes += 1

        previous_sign = current_sign

    return sign_changes


def classify_behavior(
    records: list[dict],
    convergence_step: int | None,
    sign_changes: int,
) -> str:

    finite = all(
        math.isfinite(record["estimated_a"])
        and math.isfinite(record["prediction_error"])
        for record in records
    )

    if not finite:
        return "non-finite"

    bounded = all(
        abs(record["estimated_a"])
        < PARAMETER_BOUND
        for record in records
    )

    if not bounded:
        return "unbounded"

    if convergence_step is not None:

        if sign_changes >= 4:
            return "convergent-oscillatory"

        return "convergent"

    if sign_changes >= 4:
        return "bounded-oscillatory"

    return "bounded-nonconvergent"


def run_condition(
    learning_rate: float,
) -> dict:

    records = run_experiment(
        learning_rate=learning_rate,
        noise_std_dev=NOISE_STD_DEV,
        random_seed=RANDOM_SEED,
    )

    summary = summarize_experiment(
        records,
        TRUE_A,
    )

    convergence_step = (
        calculate_convergence_step(records)
    )

    sign_changes = (
        calculate_sign_changes(records)
    )

    max_parameter_error = (
        calculate_max_parameter_error(records)
    )

    behavior = classify_behavior(
        records,
        convergence_step,
        sign_changes,
    )

    return {
        "learning_rate":
            learning_rate,
        "final_estimated_a":
            summary["final_estimated_a"],
        "parameter_absolute_error":
            summary["parameter_absolute_error"],
        "prediction_rmse":
            summary["prediction_rmse"],
        "max_parameter_error":
            max_parameter_error,
        "sign_changes":
            sign_changes,
        "convergence_step":
            convergence_step,
        "behavior":
            behavior,
    }


def run_sweep() -> list[dict]:

    return [
        run_condition(rate)
        for rate in LEARNING_RATES
    ]


def save_results(
    results: list[dict],
) -> Path:

    results_directory = Path("results")
    results_directory.mkdir(exist_ok=True)

    output_path = (
        results_directory
        / "scalar_learning_rate_boundary.csv"
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys(),
        )

        writer.writeheader()
        writer.writerows(results)

    return output_path


def print_results(
    results: list[dict],
) -> None:

    print("=" * 118)
    print(
        "ADAPTIVE DIGITAL TWIN — "
        "LEARNING-RATE STABILITY BOUNDARY"
    )
    print("=" * 118)

    for result in results:

        print(
            f"eta={result['learning_rate']:<5.2f} "
            f"final_a={result['final_estimated_a']:<12.6f} "
            f"error={result['parameter_absolute_error']:<12.6g} "
            f"RMSE={result['prediction_rmse']:<10.6f} "
            f"sign_changes={result['sign_changes']:<3} "
            f"conv={str(result['convergence_step']):<5} "
            f"{result['behavior']}"
        )

    print("=" * 118)


def main() -> None:

    results = run_sweep()

    output_path = save_results(results)

    print_results(results)

    print(
        f"Results saved to: {output_path}"
    )


if __name__ == "__main__":
    main()