import csv
import math
import statistics
from pathlib import Path


BOUNDARY_PATH = Path(
    "results/persistence_boundary_eight_population_analysis.csv"
)

POPULATION_PATHS = {
    "seed_100_139": Path(
        "results/persistence_multiplier_local_refinement.csv"
    ),
    "seed_200_239": Path(
        "results/persistence_multiplier_independent_validation.csv"
    ),
    "seed_300_339": Path(
        "results/persistence_multiplier_population_300_339.csv"
    ),
    "seed_400_439": Path(
        "results/persistence_multiplier_population_400_439.csv"
    ),
    "seed_500_539": Path(
        "results/persistence_multiplier_population_500_539.csv"
    ),
    "seed_600_639": Path(
        "results/persistence_multiplier_population_600_639.csv"
    ),
    "seed_700_739": Path(
        "results/persistence_multiplier_population_700_739.csv"
    ),
    "seed_800_839": Path(
        "results/persistence_multiplier_population_800_839.csv"
    ),
}

OUTPUT_PATH = Path(
    "results/persistence_040_preentry_influence_analysis.csv"
)


def load_targets():

    targets = {}

    with BOUNDARY_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if (
                math.isclose(
                    float(row["lower_multiplier"]),
                    0.35,
                )
                and
                math.isclose(
                    float(row["upper_multiplier"]),
                    0.40,
                )
            ):
                targets[row["population"]] = float(
                    row["analytic_transition_weight"]
                )

    return targets


def load_mean_regret_035(path):

    values = []

    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["policy"] == "two_stage_0.35":
                values.append(
                    float(row["mean_regret"])
                )

    return statistics.mean(values)


def fit_linear(x, y):

    mean_x = statistics.mean(x)
    mean_y = statistics.mean(y)

    denominator = sum(
        (value - mean_x) ** 2
        for value in x
    )

    if math.isclose(
        denominator,
        0.0,
    ):
        return 0.0, mean_y

    slope = (
        sum(
            (xi - mean_x)
            * (yi - mean_y)
            for xi, yi
            in zip(x, y)
        )
        / denominator
    )

    intercept = (
        mean_y
        - slope * mean_x
    )

    return slope, intercept


def main():

    populations = list(
        POPULATION_PATHS.keys()
    )

    targets = load_targets()

    features = {
        population:
            load_mean_regret_035(path)
        for population, path
        in POPULATION_PATHS.items()
    }

    rows = []

    for held_out, population in enumerate(
        populations
    ):

        train_populations = [
            candidate
            for index, candidate
            in enumerate(populations)
            if index != held_out
        ]

        train_x = [
            features[candidate]
            for candidate
            in train_populations
        ]

        train_y = [
            targets[candidate]
            for candidate
            in train_populations
        ]

        slope, intercept = fit_linear(
            train_x,
            train_y,
        )

        actual = targets[
            population
        ]

        predictor_prediction = (
            intercept
            + slope
            * features[population]
        )

        baseline_prediction = (
            statistics.mean(train_y)
        )

        predictor_error = abs(
            predictor_prediction
            - actual
        )

        baseline_error = abs(
            baseline_prediction
            - actual
        )

        error_reduction = (
            baseline_error
            - predictor_error
        )

        rows.append(
            {
                "population":
                    population,

                "mean_regret_035":
                    features[population],

                "actual_threshold":
                    actual,

                "predictor_prediction":
                    predictor_prediction,

                "baseline_prediction":
                    baseline_prediction,

                "predictor_abs_error":
                    predictor_error,

                "baseline_abs_error":
                    baseline_error,

                "absolute_error_reduction":
                    error_reduction,

                "predictor_wins":
                    predictor_error
                    < baseline_error,

                "training_slope":
                    slope,

                "training_intercept":
                    intercept,
            }
        )

    predictor_mae = statistics.mean(
        row["predictor_abs_error"]
        for row in rows
    )

    baseline_mae = statistics.mean(
        row["baseline_abs_error"]
        for row in rows
    )

    wins = sum(
        row["predictor_wins"]
        for row in rows
    )

    slopes = [
        row["training_slope"]
        for row in rows
    ]

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
            fieldnames=list(
                rows[0].keys()
            ),
        )

        writer.writeheader()
        writer.writerows(rows)

    print("=" * 145)
    print(
        "ADAPTIVE DIGITAL TWIN - "
        "0.40 PRE-ENTRY INFLUENCE ANALYSIS"
    )
    print("=" * 145)
    print()

    print(
        "HELD-OUT POPULATION RESULTS"
    )

    for row in rows:

        outcome = (
            "WIN"
            if row["predictor_wins"]
            else "LOSS"
        )

        print(
            f"{row['population']:<14} "
            f"actual={row['actual_threshold']:.6f} "
            f"pred={row['predictor_prediction']:.6f} "
            f"base={row['baseline_prediction']:.6f} "
            f"pred_err={row['predictor_abs_error']:.6f} "
            f"base_err={row['baseline_abs_error']:.6f} "
            f"gain={row['absolute_error_reduction']:+.6f} "
            f"slope={row['training_slope']:+.6f} "
            f"{outcome}"
        )

    print()
    print(
        "AGGREGATE INFLUENCE SUMMARY"
    )

    print(
        f"predictor wins={wins}/{len(rows)} "
        f"({wins / len(rows):.1%})"
    )

    print(
        f"predictor MAE={predictor_mae:.6f}"
    )

    print(
        f"baseline MAE={baseline_mae:.6f}"
    )

    print(
        "MAE improvement="
        f"{1.0 - predictor_mae / baseline_mae:+.1%}"
    )

    print(
        f"training slope range="
        f"[{min(slopes):+.6f}, "
        f"{max(slopes):+.6f}]"
    )

    print(
        "slope sign consistency="
        f"{sum(slope < 0.0 for slope in slopes)}"
        f"/{len(slopes)} negative"
    )

    print()
    print(
        f"Results saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
