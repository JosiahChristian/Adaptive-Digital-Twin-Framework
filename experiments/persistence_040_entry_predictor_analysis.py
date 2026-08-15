import csv
import math
import statistics
from pathlib import Path


BOUNDARY_PATH = Path(
    "results/persistence_boundary_eight_population_analysis.csv"
)

POPULATION_PATHS = {
    "seed_100_139":
        Path(
            "results/persistence_multiplier_local_refinement.csv"
        ),

    "seed_200_239":
        Path(
            "results/persistence_multiplier_independent_validation.csv"
        ),

    "seed_300_339":
        Path(
            "results/persistence_multiplier_population_300_339.csv"
        ),

    "seed_400_439":
        Path(
            "results/persistence_multiplier_population_400_439.csv"
        ),

    "seed_500_539":
        Path(
            "results/persistence_multiplier_population_500_539.csv"
        ),

    "seed_600_639":
        Path(
            "results/persistence_multiplier_population_600_639.csv"
        ),

    "seed_700_739":
        Path(
            "results/persistence_multiplier_population_700_739.csv"
        ),

    "seed_800_839":
        Path(
            "results/persistence_multiplier_population_800_839.csv"
        ),
}

OUTPUT_PATH = Path(
    "results/persistence_040_entry_predictor_analysis.csv"
)


METRICS = [
    "mean_regret",
    "under_count",
    "over_count",
    "action_entropy",
]


def load_boundary_targets() -> dict[str, float]:

    targets = {}

    with BOUNDARY_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            lower = float(
                row[
                    "lower_multiplier"
                ]
            )

            upper = float(
                row[
                    "upper_multiplier"
                ]
            )

            if not (
                math.isclose(
                    lower,
                    0.35,
                )
                and math.isclose(
                    upper,
                    0.40,
                )
            ):
                continue

            targets[
                row[
                    "population"
                ]
            ] = float(
                row[
                    "analytic_transition_weight"
                ]
            )

    return targets


def load_population(
    path: Path,
) -> list[dict]:

    rows = []

    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row[
                "policy"
            ] not in {
                "two_stage_0.35",
                "two_stage_0.40",
            }:
                continue

            record = dict(
                row
            )

            for metric in METRICS:

                record[
                    metric
                ] = float(
                    record[
                        metric
                    ]
                )

            rows.append(
                record
            )

    return rows


def mean_metric(
    rows: list[dict],
    policy: str,
    metric: str,
) -> float:

    values = [
        row[
            metric
        ]
        for row in rows
        if row[
            "policy"
        ] == policy
    ]

    return statistics.mean(
        values
    )


def population_features(
    population: str,
    path: Path,
    target: float,
) -> dict:

    rows = load_population(
        path
    )

    features = {
        "population":
            population,

        "transition_weight":
            target,
    }

    for metric in METRICS:

        value_035 = mean_metric(
            rows,
            "two_stage_0.35",
            metric,
        )

        value_040 = mean_metric(
            rows,
            "two_stage_0.40",
            metric,
        )

        features[
            f"{metric}_035"
        ] = value_035

        features[
            f"{metric}_040"
        ] = value_040

        features[
            f"delta_{metric}"
        ] = (
            value_040
            - value_035
        )

    return features


def pearson(
    x: list[float],
    y: list[float],
) -> float:

    mean_x = statistics.mean(
        x
    )

    mean_y = statistics.mean(
        y
    )

    numerator = sum(
        (
            xi - mean_x
        )
        * (
            yi - mean_y
        )
        for xi, yi
        in zip(
            x,
            y,
        )
    )

    denominator_x = math.sqrt(
        sum(
            (
                xi - mean_x
            )
            ** 2
            for xi in x
        )
    )

    denominator_y = math.sqrt(
        sum(
            (
                yi - mean_y
            )
            ** 2
            for yi in y
        )
    )

    denominator = (
        denominator_x
        * denominator_y
    )

    if math.isclose(
        denominator,
        0.0,
    ):
        return float(
            "nan"
        )

    return (
        numerator
        / denominator
    )


def predictor_rows(
    features: list[dict],
) -> list[dict]:

    predictor_names = [
        key
        for key in features[0].keys()
        if key not in {
            "population",
            "transition_weight",
        }
    ]

    targets = [
        row[
            "transition_weight"
        ]
        for row in features
    ]

    output = []

    for predictor in predictor_names:

        values = [
            row[
                predictor
            ]
            for row in features
        ]

        correlation = pearson(
            values,
            targets,
        )

        output.append(
            {
                "predictor":
                    predictor,

                "population_count":
                    len(
                        values
                    ),

                "correlation_with_transition_weight":
                    correlation,

                "absolute_correlation":
                    abs(
                        correlation
                    )
                    if not math.isnan(
                        correlation
                    )
                    else float(
                        "nan"
                    ),
            }
        )

    output.sort(
        key=lambda row: (
            -row[
                "absolute_correlation"
            ]
            if not math.isnan(
                row[
                    "absolute_correlation"
                ]
            )
            else float(
                "inf"
            )
        )
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
            "predictor",
            "population_count",
            "correlation_with_transition_weight",
            "absolute_correlation",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(
            rows
        )


def print_results(
    rows: list[dict],
) -> None:

    print(
        "=" * 125
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "0.40 ENTRY PREDICTOR ANALYSIS"
    )

    print(
        "=" * 125
    )

    print()

    print(
        "RANKED POPULATION-LEVEL PREDICTORS"
    )

    for row in rows:

        print(
            f"{row['predictor']:<30} "
            f"r="
            f"{row['correlation_with_transition_weight']:+.6f} "
            f"|r|="
            f"{row['absolute_correlation']:.6f}"
        )

    print()
    print(
        "NOTE: n=8 populations; correlations are exploratory, "
        "not confirmatory."
    )

    print()

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


def main() -> None:

    targets = load_boundary_targets()

    features = []

    for population, path in POPULATION_PATHS.items():

        features.append(
            population_features(
                population,
                path,
                targets[
                    population
                ],
            )
        )

    rows = predictor_rows(
        features
    )

    save_results(
        rows
    )

    print_results(
        rows
    )


if __name__ == "__main__":
    main()
