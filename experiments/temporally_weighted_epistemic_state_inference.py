import csv
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path

from experiments.single_trajectory_epistemic_state_inference import (
    BASE_PROCESS_NOISE_STD,
    BASE_TRUE_A,
    CONDITIONS,
    EVENT_STEP,
    PROCESS_INPUT,
    REFERENCE_TARGETS,
    RUNS_PER_CONDITION,
    STEPS,
    create_estimator,
)


OUTPUT_PATH = Path(
    "results/temporally_weighted_epistemic_state_inference.csv"
)

EVIDENCE_TIMES = [
    60,
    70,
    80,
    100,
]

BASE_SEED = 42000


MEMORY_SCHEMES = [
    "uniform",
    "event_anchored",
    "recency_weighted",
    "criterion_specific",
]


def mean_or_zero(
    values: list[float],
) -> float:

    if not values:
        return 0.0

    return statistics.mean(values)


def weighted_mean(
    values: list[float],
    weights: list[float],
) -> float:

    if not values:
        return 0.0

    total_weight = sum(weights)

    if total_weight <= 0.0:
        return mean_or_zero(values)

    return sum(
        value * weight
        for value, weight
        in zip(values, weights)
    ) / total_weight


def run_trajectory(
    *,
    condition: dict,
    seed: int,
) -> dict:

    random.seed(seed)

    estimator = create_estimator(
        initial_parameter_estimate=(
            condition[
                "initial_parameter_estimate"
            ]
        ),
        measurement_noise_std=(
            condition[
                "measurement_noise_std"
            ]
        ),
    )

    true_state = 0.0
    true_a = BASE_TRUE_A

    innovations = []
    nis_values = []
    mismatch_indicators = []
    parameter_estimates = []
    parameter_updates = []

    for step in range(STEPS):

        if (
            condition[
                "changed_true_a"
            ]
            is not None
            and step == EVENT_STEP
        ):
            true_a = condition[
                "changed_true_a"
            ]

        true_state = (
            true_a
            * true_state
            + PROCESS_INPUT
            + random.gauss(
                0.0,
                BASE_PROCESS_NOISE_STD,
            )
        )

        if (
            condition[
                "process_disturbance"
            ]
            != 0.0
            and step == EVENT_STEP
        ):
            true_state += condition[
                "process_disturbance"
            ]

        measurement = (
            true_state
            + random.gauss(
                0.0,
                condition[
                    "measurement_noise_std"
                ],
            )
        )

        result = estimator.step(
            control_input=PROCESS_INPUT,
            measurement=measurement,
        )

        innovations.append(
            result.innovation
        )

        nis_values.append(
            result.normalized_innovation_squared
        )

        mismatch_indicators.append(
            result.mismatch_indicator
        )

        parameter_estimates.append(
            result.parameter_estimate
        )

        parameter_updates.append(
            result.parameter_update
        )

    return {
        "innovations":
            innovations,
        "nis_values":
            nis_values,
        "mismatch_indicators":
            mismatch_indicators,
        "parameter_estimates":
            parameter_estimates,
        "parameter_updates":
            parameter_updates,
    }


def temporal_weights(
    *,
    evidence_time: int,
    scheme: str,
    criterion: str | None = None,
) -> list[float]:

    weights = []

    for step in range(
        evidence_time
    ):

        if scheme == "uniform":

            weight = 1.0

        elif scheme == "event_anchored":

            distance = abs(
                step - EVENT_STEP
            )

            weight = math.exp(
                -distance / 8.0
            )

        elif scheme == "recency_weighted":

            age = (
                evidence_time
                - 1
                - step
            )

            weight = math.exp(
                -age / 12.0
            )

        elif scheme == "criterion_specific":

            if criterion == "A":

                tau = 8.0

                distance = abs(
                    step - EVENT_STEP
                )

                weight = math.exp(
                    -distance / tau
                )

            elif criterion == "C":

                tau = 10.0

                distance = abs(
                    step - EVENT_STEP
                )

                weight = math.exp(
                    -distance / tau
                )

            elif criterion == "S":

                age = (
                    evidence_time
                    - 1
                    - step
                )

                weight = math.exp(
                    -age / 18.0
                )

            else:

                raise ValueError(
                    criterion
                )

        else:

            raise ValueError(
                scheme
            )

        weights.append(
            weight
        )

    return weights


def extract_weighted_features(
    trajectory: dict,
    *,
    evidence_time: int,
    scheme: str,
    criterion: str | None,
) -> dict:

    innovations = trajectory[
        "innovations"
    ][
        :evidence_time
    ]

    nis_values = trajectory[
        "nis_values"
    ][
        :evidence_time
    ]

    mismatch_indicators = trajectory[
        "mismatch_indicators"
    ][
        :evidence_time
    ]

    parameter_estimates = trajectory[
        "parameter_estimates"
    ][
        :evidence_time
    ]

    parameter_updates = trajectory[
        "parameter_updates"
    ][
        :evidence_time
    ]

    weights = temporal_weights(
        evidence_time=evidence_time,
        scheme=scheme,
        criterion=criterion,
    )

    absolute_innovations = [
        abs(value)
        for value in innovations
    ]

    absolute_updates = [
        abs(value)
        for value in parameter_updates
    ]

    nis_above_one = [
        1.0
        if value > 1.0
        else 0.0
        for value in nis_values
    ]

    weighted_parameter = (
        weighted_mean(
            parameter_estimates,
            weights,
        )
    )

    weighted_update = (
        weighted_mean(
            absolute_updates,
            weights,
        )
    )

    return {
        "weighted_abs_innovation":
            weighted_mean(
                absolute_innovations,
                weights,
            ),

        "weighted_nis":
            weighted_mean(
                nis_values,
                weights,
            ),

        "weighted_nis_above_1":
            weighted_mean(
                nis_above_one,
                weights,
            ),

        "weighted_mismatch_indicator":
            weighted_mean(
                mismatch_indicators,
                weights,
            ),

        "weighted_parameter_estimate":
            weighted_parameter,

        "weighted_abs_parameter_update":
            weighted_update,

        "current_parameter_estimate":
            parameter_estimates[-1],

        "current_mismatch_indicator":
            mismatch_indicators[-1],
    }


FEATURE_NAMES = [
    "weighted_abs_innovation",
    "weighted_nis",
    "weighted_nis_above_1",
    "weighted_mismatch_indicator",
    "weighted_parameter_estimate",
    "weighted_abs_parameter_update",
    "current_parameter_estimate",
    "current_mismatch_indicator",
]


def standardize(
    values: list[float],
) -> tuple[
    float,
    float,
]:

    mean_value = statistics.mean(
        values
    )

    if len(values) > 1:
        std_value = statistics.stdev(
            values
        )
    else:
        std_value = 0.0

    if std_value < 1e-12:
        std_value = 1.0

    return (
        mean_value,
        std_value,
    )


def fit_centroids(
    training_rows: list[dict],
) -> dict:

    scaling = {}

    for feature in FEATURE_NAMES:

        scaling[feature] = standardize(
            [
                row[feature]
                for row in training_rows
            ]
        )

    groups = defaultdict(list)

    for row in training_rows:
        groups[
            row["condition"]
        ].append(
            row
        )

    centroids = {}

    for condition, group in groups.items():

        centroid = {}

        for feature in FEATURE_NAMES:

            feature_mean = statistics.mean(
                row[feature]
                for row in group
            )

            scale_mean, scale_std = (
                scaling[feature]
            )

            centroid[feature] = (
                (
                    feature_mean
                    - scale_mean
                )
                / scale_std
            )

        centroids[
            condition
        ] = centroid

    return {
        "scaling":
            scaling,
        "centroids":
            centroids,
    }


def condition_weights(
    *,
    features: dict,
    model: dict,
) -> dict:

    distances = {}

    for condition, centroid in (
        model[
            "centroids"
        ].items()
    ):

        squared_distance = 0.0

        for feature in FEATURE_NAMES:

            mean_value, std_value = (
                model[
                    "scaling"
                ][
                    feature
                ]
            )

            standardized_value = (
                (
                    features[
                        feature
                    ]
                    - mean_value
                )
                / std_value
            )

            difference = (
                standardized_value
                - centroid[
                    feature
                ]
            )

            squared_distance += (
                difference ** 2
            )

        distances[
            condition
        ] = math.sqrt(
            squared_distance
        )

    similarities = {
        condition:
            math.exp(
                -distance
            )
        for condition, distance
        in distances.items()
    }

    total_similarity = sum(
        similarities.values()
    )

    return {
        condition:
            similarity
            / total_similarity
        for condition, similarity
        in similarities.items()
    }


def estimate_target(
    *,
    weights: dict,
    target_name: str,
) -> float:

    return sum(
        weight
        * REFERENCE_TARGETS[
            condition
        ][
            target_name
        ]
        for condition, weight
        in weights.items()
    )


def build_feature_rows() -> list[dict]:

    rows = []

    for condition_index, condition in enumerate(
        CONDITIONS
    ):

        reference_condition = (
            condition[
                "reference_condition"
            ]
        )

        target = REFERENCE_TARGETS[
            reference_condition
        ]

        for run_index in range(
            RUNS_PER_CONDITION
        ):

            seed = (
                BASE_SEED
                + condition_index
                * RUNS_PER_CONDITION
                + run_index
            )

            trajectory = run_trajectory(
                condition=condition,
                seed=seed,
            )

            split = (
                "train"
                if run_index
                < RUNS_PER_CONDITION // 2
                else "test"
            )

            for evidence_time in (
                EVIDENCE_TIMES
            ):

                for scheme in [
                    "uniform",
                    "event_anchored",
                    "recency_weighted",
                ]:

                    features = (
                        extract_weighted_features(
                            trajectory,
                            evidence_time=(
                                evidence_time
                            ),
                            scheme=scheme,
                            criterion=None,
                        )
                    )

                    rows.append(
                        {
                            "condition":
                                reference_condition,
                            "true_class":
                                condition[
                                    "class"
                                ],
                            "run_index":
                                run_index,
                            "split":
                                split,
                            "evidence_time":
                                evidence_time,
                            "scheme":
                                scheme,
                            "criterion":
                                "shared",
                            "target_p_fail_A":
                                target[
                                    "p_fail_A"
                                ],
                            "target_p_fail_C":
                                target[
                                    "p_fail_C"
                                ],
                            "target_p_fail_S":
                                target[
                                    "p_fail_S"
                                ],
                            **features,
                        }
                    )

                for criterion in [
                    "A",
                    "C",
                    "S",
                ]:

                    features = (
                        extract_weighted_features(
                            trajectory,
                            evidence_time=(
                                evidence_time
                            ),
                            scheme=(
                                "criterion_specific"
                            ),
                            criterion=criterion,
                        )
                    )

                    rows.append(
                        {
                            "condition":
                                reference_condition,
                            "true_class":
                                condition[
                                    "class"
                                ],
                            "run_index":
                                run_index,
                            "split":
                                split,
                            "evidence_time":
                                evidence_time,
                            "scheme":
                                "criterion_specific",
                            "criterion":
                                criterion,
                            "target_p_fail_A":
                                target[
                                    "p_fail_A"
                                ],
                            "target_p_fail_C":
                                target[
                                    "p_fail_C"
                                ],
                            "target_p_fail_S":
                                target[
                                    "p_fail_S"
                                ],
                            **features,
                        }
                    )

    return rows


def evaluate_shared_scheme(
    *,
    rows: list[dict],
    scheme: str,
    evidence_time: int,
) -> list[dict]:

    training_rows = [
        row
        for row in rows
        if (
            row["split"]
            == "train"
            and
            row["scheme"]
            == scheme
            and
            row[
                "evidence_time"
            ]
            == evidence_time
        )
    ]

    test_rows = [
        row
        for row in rows
        if (
            row["split"]
            == "test"
            and
            row["scheme"]
            == scheme
            and
            row[
                "evidence_time"
            ]
            == evidence_time
        )
    ]

    model = fit_centroids(
        training_rows
    )

    output = []

    for row in test_rows:

        weights = condition_weights(
            features=row,
            model=model,
        )

        estimate_a = estimate_target(
            weights=weights,
            target_name="p_fail_A",
        )

        estimate_c = estimate_target(
            weights=weights,
            target_name="p_fail_C",
        )

        estimate_s = estimate_target(
            weights=weights,
            target_name="p_fail_S",
        )

        output.append(
            {
                "condition":
                    row[
                        "condition"
                    ],
                "true_class":
                    row[
                        "true_class"
                    ],
                "run_index":
                    row[
                        "run_index"
                    ],
                "evidence_time":
                    evidence_time,
                "scheme":
                    scheme,
                "estimated_p_fail_A":
                    estimate_a,
                "estimated_p_fail_C":
                    estimate_c,
                "estimated_p_fail_S":
                    estimate_s,
                "target_p_fail_A":
                    row[
                        "target_p_fail_A"
                    ],
                "target_p_fail_C":
                    row[
                        "target_p_fail_C"
                    ],
                "target_p_fail_S":
                    row[
                        "target_p_fail_S"
                    ],
            }
        )

    return output


def evaluate_criterion_specific(
    *,
    rows: list[dict],
    evidence_time: int,
) -> list[dict]:

    models = {}

    for criterion in [
        "A",
        "C",
        "S",
    ]:

        training_rows = [
            row
            for row in rows
            if (
                row["split"]
                == "train"
                and
                row["scheme"]
                == "criterion_specific"
                and
                row[
                    "criterion"
                ]
                == criterion
                and
                row[
                    "evidence_time"
                ]
                == evidence_time
            )
        ]

        models[
            criterion
        ] = fit_centroids(
            training_rows
        )

    test_groups = defaultdict(dict)

    for row in rows:

        if (
            row["split"]
            != "test"
            or
            row["scheme"]
            != "criterion_specific"
            or
            row[
                "evidence_time"
            ]
            != evidence_time
        ):
            continue

        key = (
            row["condition"],
            row["run_index"],
        )

        test_groups[key][
            row["criterion"]
        ] = row

    output = []

    for (
        condition,
        run_index,
    ), group in (
        test_groups.items()
    ):

        row_a = group["A"]
        row_c = group["C"]
        row_s = group["S"]

        weights_a = condition_weights(
            features=row_a,
            model=models["A"],
        )

        weights_c = condition_weights(
            features=row_c,
            model=models["C"],
        )

        weights_s = condition_weights(
            features=row_s,
            model=models["S"],
        )

        estimate_a = estimate_target(
            weights=weights_a,
            target_name="p_fail_A",
        )

        estimate_c = estimate_target(
            weights=weights_c,
            target_name="p_fail_C",
        )

        estimate_s = estimate_target(
            weights=weights_s,
            target_name="p_fail_S",
        )

        output.append(
            {
                "condition":
                    condition,
                "true_class":
                    row_a[
                        "true_class"
                    ],
                "run_index":
                    run_index,
                "evidence_time":
                    evidence_time,
                "scheme":
                    "criterion_specific",
                "estimated_p_fail_A":
                    estimate_a,
                "estimated_p_fail_C":
                    estimate_c,
                "estimated_p_fail_S":
                    estimate_s,
                "target_p_fail_A":
                    row_a[
                        "target_p_fail_A"
                    ],
                "target_p_fail_C":
                    row_a[
                        "target_p_fail_C"
                    ],
                "target_p_fail_S":
                    row_a[
                        "target_p_fail_S"
                    ],
            }
        )

    return output


def add_errors(
    row: dict,
) -> dict:

    a_error = abs(
        row[
            "estimated_p_fail_A"
        ]
        - row[
            "target_p_fail_A"
        ]
    )

    c_error = abs(
        row[
            "estimated_p_fail_C"
        ]
        - row[
            "target_p_fail_C"
        ]
    )

    s_error = abs(
        row[
            "estimated_p_fail_S"
        ]
        - row[
            "target_p_fail_S"
        ]
    )

    return {
        **row,
        "A_mae":
            a_error,
        "C_mae":
            c_error,
        "S_mae":
            s_error,
        "marginal_mae":
            statistics.mean(
                [
                    a_error,
                    c_error,
                    s_error,
                ]
            ),
    }


def run_experiment() -> list[dict]:

    feature_rows = (
        build_feature_rows()
    )

    output_rows = []

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        for scheme in [
            "uniform",
            "event_anchored",
            "recency_weighted",
        ]:

            rows = evaluate_shared_scheme(
                rows=feature_rows,
                scheme=scheme,
                evidence_time=evidence_time,
            )

            output_rows.extend(
                add_errors(row)
                for row in rows
            )

        criterion_rows = (
            evaluate_criterion_specific(
                rows=feature_rows,
                evidence_time=evidence_time,
            )
        )

        output_rows.extend(
            add_errors(row)
            for row in criterion_rows
        )

    return output_rows


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

    print("=" * 126)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "TEMPORALLY WEIGHTED EPISTEMIC-STATE INFERENCE"
    )

    print("=" * 126)

    for evidence_time in (
        EVIDENCE_TIMES
    ):

        print()
        print(
            f"t={evidence_time}"
        )

        for scheme in (
            MEMORY_SCHEMES
        ):

            group = [
                row
                for row in rows
                if (
                    int(
                        row[
                            "evidence_time"
                        ]
                    )
                    == evidence_time
                    and
                    row[
                        "scheme"
                    ]
                    == scheme
                )
            ]

            a_mae = statistics.mean(
                float(
                    row["A_mae"]
                )
                for row in group
            )

            c_mae = statistics.mean(
                float(
                    row["C_mae"]
                )
                for row in group
            )

            s_mae = statistics.mean(
                float(
                    row["S_mae"]
                )
                for row in group
            )

            marginal_mae = (
                statistics.mean(
                    float(
                        row[
                            "marginal_mae"
                        ]
                    )
                    for row in group
                )
            )

            print(
                f"  {scheme:<20}"
                f"A={a_mae:.4f} "
                f"C={c_mae:.4f} "
                f"S={s_mae:.4f} "
                f"MAE="
                f"{marginal_mae:.4f}"
            )

    print("=" * 126)


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