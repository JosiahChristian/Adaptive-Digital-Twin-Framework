import csv
import math
from pathlib import Path


INPUT_PATH = Path(
    "results/persistence_boundary_three_population_analysis.csv"
)

OUTPUT_PATH = Path(
    "results/persistence_boundary_ratio_summary.csv"
)


def load_rows() -> list[dict]:
    rows = []

    with INPUT_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            record = dict(row)

            for field in (
                "lower_multiplier",
                "upper_multiplier",
                "performance_term",
                "responsiveness_term",
                "analytic_transition_weight",
            ):
                record[field] = float(
                    record[field]
                )

            rows.append(record)

    return rows


def summarize(
    rows: list[dict],
) -> list[dict]:

    output = []

    for row in rows:

        ratio = (
            abs(
                row["responsiveness_term"]
            )
            / row["performance_term"]
        )

        residual = (
            ratio
            - row[
                "analytic_transition_weight"
            ]
        )

        output.append(
            {
                "population":
                    row["population"],

                "transition":
                    (
                        f"{row['lower_multiplier']:.2f}"
                        "->"
                        f"{row['upper_multiplier']:.2f}"
                    ),

                "performance_term":
                    row["performance_term"],

                "responsiveness_magnitude":
                    abs(
                        row["responsiveness_term"]
                    ),

                "term_ratio":
                    ratio,

                "analytic_transition_weight":
                    row[
                        "analytic_transition_weight"
                    ],

                "ratio_residual":
                    residual,

                "equation_verified":
                    int(
                        math.isclose(
                            ratio,
                            row[
                                "analytic_transition_weight"
                            ],
                            rel_tol=1e-12,
                            abs_tol=1e-12,
                        )
                    ),
            }
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

        fieldnames = [
            "population",
            "transition",
            "performance_term",
            "responsiveness_magnitude",
            "term_ratio",
            "analytic_transition_weight",
            "ratio_residual",
            "equation_verified",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)


def print_results(
    rows: list[dict],
) -> None:

    print("=" * 120)
    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PERSISTENCE BOUNDARY RATIO SUMMARY"
    )
    print("=" * 120)
    print()

    for row in rows:

        print(
            f"{row['population']:<14} "
            f"{row['transition']:<10} "
            f"P={row['performance_term']:.6f} "
            f"|R|={row['responsiveness_magnitude']:.6f} "
            f"|R|/P={row['term_ratio']:.6f} "
            f"threshold="
            f"{row['analytic_transition_weight']:.6f} "
            f"residual="
            f"{row['ratio_residual']:+.3e}"
        )

    print()

    verified = sum(
        row["equation_verified"]
        for row in rows
    )

    print(
        "equation verification="
        f"{verified}/{len(rows)}"
    )

    print()

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


def main() -> None:

    rows = load_rows()

    summary = summarize(
        rows
    )

    save_results(
        summary
    )

    print_results(
        summary
    )


if __name__ == "__main__":
    main()
