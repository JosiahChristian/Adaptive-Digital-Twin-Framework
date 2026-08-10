import csv
import math
from pathlib import Path


ARCHITECTURES = [
    {
        "experiment": "005",
        "name": "Integrated baseline",
        "result_file":
            "integrated_adaptive_estimation.csv",
        "mismatch_field": None,
        "lambda_field": None,
        "fixed_lambda": None,
        "effective_q_field": None,
    },
    {
        "experiment": "006",
        "name": "Fixed uncertainty inflation",
        "result_file":
            "model_uncertainty_estimation.csv",
        "mismatch_field":
            "mismatch_indicator",
        "lambda_field": None,
        "fixed_lambda": 0.05,
        "effective_q_field":
            "effective_process_noise_variance",
    },
    {
        "experiment": "009",
        "name": "Dynamic raw-innovation policy",
        "result_file":
            "dynamic_uncertainty_management.csv",
        "mismatch_field":
            "mismatch_indicator",
        "lambda_field":
            "dynamic_lambda",
        "fixed_lambda": None,
        "effective_q_field":
            "effective_q",
    },
    {
        "experiment": "010",
        "name": "Normalized innovation policy",
        "result_file":
            "normalized_innovation_uncertainty.csv",
        "mismatch_field":
            "mismatch_indicator",
        "lambda_field":
            "dynamic_lambda",
        "fixed_lambda": None,
        "effective_q_field":
            "effective_q",
    },
    {
        "experiment": "011",
        "name": "Instant consistency gate",
        "result_file":
            "consistency_gated_uncertainty.csv",
        "mismatch_field":
            "mismatch_indicator",
        "lambda_field":
            "dynamic_lambda",
        "fixed_lambda": None,
        "effective_q_field":
            "effective_q",
    },
    {
        "experiment": "012",
        "name": "Persistence consistency gate",
        "result_file":
            "persistence_gated_uncertainty.csv",
        "mismatch_field":
            "mismatch_indicator",
        "lambda_field":
            "dynamic_lambda",
        "fixed_lambda": None,
        "effective_q_field":
            "effective_q",
    },
]


def calculate_rmse(
    values: list[float],
) -> float:

    return math.sqrt(
        sum(
            value ** 2
            for value in values
        )
        / len(values)
    )


def load_records(
    filename: str,
) -> list[dict]:

    path = (
        Path("results")
        / filename
    )

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def calculate_state_errors(
    records: list[dict],
) -> list[float]:

    return [
        float(record["state_estimate"])
        - float(record["true_state"])
        for record in records
    ]


def calculate_measurement_errors(
    records: list[dict],
) -> list[float]:

    return [
        float(record["measurement"])
        - float(record["true_state"])
        for record in records
    ]


def optional_final_value(
    records: list[dict],
    field: str | None,
) -> float | None:

    if field is None:
        return None

    value = records[-1].get(field)

    if value in (
        None,
        "",
    ):
        return None

    return float(value)


def summarize_architecture(
    architecture: dict,
) -> dict:

    records = load_records(
        architecture["result_file"]
    )

    state_errors = (
        calculate_state_errors(
            records
        )
    )

    measurement_errors = (
        calculate_measurement_errors(
            records
        )
    )

    final_parameter_estimate = float(
        records[-1]["parameter_estimate"]
    )

    true_parameter = 0.92

    final_lambda = (
        architecture["fixed_lambda"]
    )

    if architecture["lambda_field"] is not None:
        final_lambda = optional_final_value(
            records,
            architecture["lambda_field"],
        )

    return {
        "experiment":
            architecture["experiment"],
        "architecture":
            architecture["name"],

        "state_rmse_full":
            calculate_rmse(
                state_errors
            ),

        "state_rmse_0_24":
            calculate_rmse(
                state_errors[0:25]
            ),

        "state_rmse_25_49":
            calculate_rmse(
                state_errors[25:50]
            ),

        "state_rmse_50_99":
            calculate_rmse(
                state_errors[50:100]
            ),

        "measurement_rmse_full":
            calculate_rmse(
                measurement_errors
            ),

        "measurement_rmse_50_99":
            calculate_rmse(
                measurement_errors[50:100]
            ),

        "final_parameter_estimate":
            final_parameter_estimate,

        "final_parameter_absolute_error":
            abs(
                true_parameter
                - final_parameter_estimate
            ),

        "final_covariance":
            float(
                records[-1][
                    "state_covariance"
                ]
            ),

        "final_mismatch_indicator":
            optional_final_value(
                records,
                architecture[
                    "mismatch_field"
                ],
            ),

        "final_inflation_strength":
            final_lambda,

        "final_effective_q":
            optional_final_value(
                records,
                architecture[
                    "effective_q_field"
                ],
            ),
    }


def run_comparison() -> list[dict]:

    return [
        summarize_architecture(
            architecture
        )
        for architecture
        in ARCHITECTURES
    ]


def save_results(
    results: list[dict],
) -> Path:

    output_path = (
        Path("results")
        / "uncertainty_architecture_comparison.csv"
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
        writer.writerows(
            results
        )

    return output_path


def print_results(
    results: list[dict],
) -> None:

    print("=" * 118)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "UNCERTAINTY ARCHITECTURE COMPARISON"
    )

    print("=" * 118)

    print(
        f"{'Exp':<6}"
        f"{'Architecture':<34}"
        f"{'Full RMSE':<14}"
        f"{'Early':<14}"
        f"{'Late':<14}"
        f"{'Param Err':<14}"
    )

    print("-" * 118)

    for result in results:

        print(
            f"{result['experiment']:<6}"
            f"{result['architecture']:<34}"
            f"{result['state_rmse_full']:<14.6f}"
            f"{result['state_rmse_0_24']:<14.6f}"
            f"{result['state_rmse_50_99']:<14.6f}"
            f"{result['final_parameter_absolute_error']:<14.6f}"
        )

    print("=" * 118)


def main() -> None:

    results = run_comparison()

    output_path = save_results(
        results
    )

    print_results(
        results
    )

    print(
        f"Results saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()