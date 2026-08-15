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
    "results/persistence_040_preentry_validation.csv"
)

PREDICTORS = [
    "mean_regret",
    "under_count",
    "over_count",
    "action_entropy",
]


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


def load_preentry_features(path):

    values = {
        predictor: []
        for predictor in PREDICTORS
    }

    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["policy"] != "two_stage_0.35":
                continue

            for predictor in PREDICTORS:
                values[predictor].append(
                    float(row[predictor])
                )

    return {
        predictor: statistics.mean(samples)
        for predictor, samples in values.items()
    }


def pearson(x, y):

    mx = statistics.mean(x)
    my = statistics.mean(y)

    numerator = sum(
        (xi - mx) * (yi - my)
        for xi, yi in zip(x, y)
    )

    dx = math.sqrt(
        sum(
            (xi - mx) ** 2
            for xi in x
        )
    )

    dy = math.sqrt(
        sum(
            (yi - my) ** 2
            for yi in y
        )
    )

    denominator = dx * dy

    if math.isclose(
        denominator,
        0.0,
    ):
        return float("nan")

    return numerator / denominator


def leave_one_out_prediction(
    x,
    y,
):

    predictions = []

    for held_out in range(len(x)):

        train_indices = [
            index
            for index in range(len(x))
            if index != held_out
        ]

        train_x = [
            x[index]
            for index in train_indices
        ]

        train_y = [
            y[index]
            for index in train_indices
        ]

        mean_x = statistics.mean(train_x)
        mean_y = statistics.mean(train_y)

        denominator = sum(
            (value - mean_x) ** 2
            for value in train_x
        )

        if math.isclose(
            denominator,
            0.0,
        ):
            prediction = mean_y

        else:
            slope = (
                sum(
                    (
                        train_x[index]
                        - mean_x
                    )
                    * (
                        train_y[index]
                        - mean_y
                    )
                    for index
                    in range(len(train_x))
                )
                / denominator
            )

            intercept = (
                mean_y
                - slope * mean_x
            )

            prediction = (
                intercept
                + slope * x[held_out]
            )

        predictions.append(
            prediction
        )

    return predictions


def main():

    targets = load_targets()

    populations = list(
        POPULATION_PATHS.keys()
    )

    feature_rows = {
        population:
            load_preentry_features(path)
        for population, path
        in POPULATION_PATHS.items()
    }

    y = [
        targets[population]
        for population in populations
    ]

    results = []

    print("=" * 125)
    print(
        "ADAPTIVE DIGITAL TWIN - "
        "0.40 PRE-ENTRY PREDICTOR VALIDATION"
    )
    print("=" * 125)
    print()

    for predictor in PREDICTORS:

        x = [
            feature_rows[population][predictor]
            for population in populations
        ]

        correlation = pearson(
            x,
            y,
        )

        predictions = leave_one_out_prediction(
            x,
            y,
        )

        errors = [
            prediction - actual
            for prediction, actual
            in zip(predictions, y)
        ]

        mae = statistics.mean(
            abs(error)
            for error in errors
        )

        rmse = math.sqrt(
            statistics.mean(
                error ** 2
                for error in errors
            )
        )

        baseline_predictions = []

        for held_out in range(len(y)):

            train_y = [
                y[index]
                for index in range(len(y))
                if index != held_out
            ]

            baseline_predictions.append(
                statistics.mean(train_y)
            )

        baseline_mae = statistics.mean(
            abs(prediction - actual)
            for prediction, actual
            in zip(
                baseline_predictions,
                y,
            )
        )

        improvement = (
            1.0 - mae / baseline_mae
            if not math.isclose(
                baseline_mae,
                0.0,
            )
            else float("nan")
        )

        results.append(
            {
                "predictor":
                    predictor,

                "correlation":
                    correlation,

                "loo_mae":
                    mae,

                "loo_rmse":
                    rmse,

                "baseline_mae":
                    baseline_mae,

                "mae_improvement":
                    improvement,
            }
        )

    results.sort(
        key=lambda row:
            row["loo_mae"]
    )

    print(
        "LEAKAGE-FREE SINGLE-PREDICTOR "
        "LEAVE-ONE-POPULATION-OUT RESULTS"
    )

    for row in results:

        print(
            f"{row['predictor']:<20} "
            f"r={row['correlation']:+.6f} "
            f"LOO_MAE={row['loo_mae']:.6f} "
            f"LOO_RMSE={row['loo_rmse']:.6f} "
            f"baseline_MAE={row['baseline_mae']:.6f} "
            f"improvement={row['mae_improvement']:+.1%}"
        )

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
            fieldnames=[
                "predictor",
                "correlation",
                "loo_mae",
                "loo_rmse",
                "baseline_mae",
                "mae_improvement",
            ],
        )

        writer.writeheader()
        writer.writerows(results)

    print()
    print(
        "Validation design: "
        "m=0.35 observables only; "
        "no m=0.40 or transition-delta predictors."
    )

    print(
        "Cross-validation: "
        "leave one entire population out."
    )

    print()
    print(
        f"Results saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
