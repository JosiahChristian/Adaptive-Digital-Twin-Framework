import csv
import statistics
from collections import defaultdict
from pathlib import Path


INPUT_PATH = Path(
    "results/persistence_boundary_eight_population_analysis.csv"
)

OUTPUT_PATH = Path(
    "results/persistence_boundary_eight_population_statistics.csv"
)


FIELDS = [
    "analytic_transition_weight",
    "performance_term",
    "responsiveness_term",
    "regret_term",
    "under_term",
    "over_term",
    "entropy_term",
]


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
                *FIELDS,
            ):
                record[field] = float(
                    record[field]
                )

            rows.append(record)

    return rows


def transition_name(
    row: dict,
) -> str:

    return (
        f"{row['lower_multiplier']:.2f}"
        "->"
        f"{row['upper_multiplier']:.2f}"
    )


def coefficient_of_variation(
    values: list[float],
) -> float:

    mean_value = statistics.mean(
        values
    )

    if mean_value == 0.0:
        return float("nan")

    return (
        statistics.pstdev(values)
        / abs(mean_value)
    )


def summarize(
    rows: list[dict],
) -> list[dict]:

    grouped = defaultdict(list)

    for row in rows:
        grouped[
            transition_name(row)
        ].append(row)

    output = []

    for transition, transition_rows in grouped.items():

        for field in FIELDS:

            values = [
                float(
                    row[field]
                )
                for row in transition_rows
            ]

            output.append(
                {
                    "transition":
                        transition,

                    "metric":
                        field,

                    "population_count":
                        len(values),

                    "mean":
                        statistics.mean(values),

                    "median":
                        statistics.median(values),

                    "std":
                        statistics.pstdev(values),

                    "minimum":
                        min(values),

                    "maximum":
                        max(values),

                    "range":
                        max(values)
                        - min(values),

                    "coefficient_of_variation":
                        coefficient_of_variation(
                            values
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
            "transition",
            "metric",
            "population_count",
            "mean",
            "median",
            "std",
            "minimum",
            "maximum",
            "range",
            "coefficient_of_variation",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)


def print_metric(
    rows: list[dict],
    transition: str,
    metric: str,
) -> None:

    row = next(
        item
        for item in rows
        if item["transition"] == transition
        and item["metric"] == metric
    )

    print(
        f"  {metric:<28} "
        f"mean={row['mean']:+.6f} "
        f"median={row['median']:+.6f} "
        f"std={row['std']:.6f} "
        f"range=["
        f"{row['minimum']:+.6f}, "
        f"{row['maximum']:+.6f}] "
        f"CV={row['coefficient_of_variation']:.3f}"
    )


def print_results(
    rows: list[dict],
) -> None:

    print("=" * 145)
    print(
        "ADAPTIVE DIGITAL TWIN - "
        "PERSISTENCE BOUNDARY "
        "POPULATION STATISTICS"
    )
    print("=" * 145)
    print()

    for transition in (
        "0.30->0.35",
        "0.35->0.40",
    ):

        print(transition)

        for metric in (
            "analytic_transition_weight",
            "performance_term",
            "responsiveness_term",
            "regret_term",
            "under_term",
            "over_term",
            "entropy_term",
        ):

            print_metric(
                rows,
                transition,
                metric,
            )

        print()

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


def reversal_summary(
    rows: list[dict],
) -> list[dict]:

    output = []

    for transition in (
        "0.30->0.35",
        "0.35->0.40",
    ):

        transition_rows = [
            row
            for row in rows
            if transition_name(row)
            == transition
        ]

        for metric in (
            "regret_term",
            "under_term",
            "over_term",
            "entropy_term",
        ):

            values = [
                float(
                    row[metric]
                )
                for row in transition_rows
            ]

            expected_positive = (
                metric in {
                    "regret_term",
                    "under_term",
                }
            )

            if expected_positive:
                reversals = sum(
                    value < 0.0
                    for value in values
                )
            else:
                reversals = sum(
                    value > 0.0
                    for value in values
                )

            output.append(
                {
                    "transition":
                        transition,

                    "metric":
                        metric,

                    "reversal_count":
                        reversals,

                    "population_count":
                        len(values),

                    "reversal_rate":
                        (
                            reversals
                            / len(values)
                        ),
                }
            )

    return output


def print_reversals(
    rows: list[dict],
) -> None:

    print(
        "COMPONENT DIRECTION REVERSALS"
    )

    for row in rows:

        print(
            f"  {row['transition']:<10} "
            f"{row['metric']:<18} "
            f"{row['reversal_count']}/"
            f"{row['population_count']} "
            f"({row['reversal_rate']:.1%})"
        )

    print()

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

    reversals = reversal_summary(
        rows
    )

    print_reversals(
        reversals
    )


if __name__ == "__main__":
    main()
