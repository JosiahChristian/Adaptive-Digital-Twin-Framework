import csv
import statistics
from pathlib import Path

import numpy as np

from sklearn.preprocessing import StandardScaler

from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)

from experiments.responsiveness_preserving_safe_persistence_control import (
    FEATURE_NAMES,
    train_loss_models,
    train_occurrence_model,
    train_magnitude_model,
    predicted_loss_table,
    predict_two_stage_risk,
)


OUTPUT_PATH = Path(
    "results/"
    "support_metric_action_conditionality_audit.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "support_metric_action_conditionality_audit_contexts.csv"
)

AUDIT_SEEDS = [
    44000,
    44011,
    44031,
]

TEST_FRACTION = 0.30
META_FRACTION = 0.30

ACTIONS = [
    1,
    2,
    3,
]

K_NEIGHBORS = 5

FLOAT_TOLERANCE = 1e-12


def three_way_split(
    rows: list[dict],
) -> tuple[
    list[dict],
    list[dict],
    list[dict],
]:

    test_start = int(
        len(rows)
        * (
            1.0
            - TEST_FRACTION
        )
    )

    development_rows = rows[
        :test_start
    ]

    test_rows = rows[
        test_start:
    ]

    meta_start = int(
        len(development_rows)
        * (
            1.0
            - META_FRACTION
        )
    )

    base_train_rows = development_rows[
        :meta_start
    ]

    meta_train_rows = development_rows[
        meta_start:
    ]

    return (
        base_train_rows,
        meta_train_rows,
        test_rows,
    )


def feature_vector(
    row: dict,
    predicted_risk: float,
    predicted_losses: dict,
) -> list[float]:

    base_features = [
        float(
            row[
                name
            ]
        )
        for name in FEATURE_NAMES
    ]

    loss_k1 = float(
        predicted_losses[
            1
        ]
    )

    loss_k2 = float(
        predicted_losses[
            2
        ]
    )

    loss_k3 = float(
        predicted_losses[
            3
        ]
    )

    return (
        base_features
        + [
            float(
                predicted_risk
            ),
            loss_k1,
            loss_k2,
            loss_k3,
            loss_k1 - loss_k2,
            loss_k1 - loss_k3,
            loss_k2 - loss_k3,
        ]
    )


def action_specific_features(
    row: dict,
    predicted_risk: float,
    predicted_losses: dict,
    action: int,
) -> list[float]:

    return (
        feature_vector(
            row,
            predicted_risk,
            predicted_losses,
        )
        + [
            float(
                action
            ),
            float(
                action - 1
            ),
            float(
                3 - action
            ),
        ]
    )


def current_support_objects(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict:

    output = {}

    for action in ACTIONS:

        matrix = np.asarray(
            [
                action_specific_features(
                    row,
                    predicted_risks[
                        index
                    ],
                    predicted_losses[
                        index
                    ],
                    action,
                )
                for index, row in enumerate(
                    rows
                )
            ],
            dtype=float,
        )

        scaler = StandardScaler()

        scaled = scaler.fit_transform(
            matrix
        )

        output[
            action
        ] = {
            "raw":
                matrix,

            "scaled":
                scaled,

            "scaler":
                scaler,
        }

    return output


def shared_support_object(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict:

    raw_rows = []
    action_labels = []

    for index, row in enumerate(
        rows
    ):

        for action in ACTIONS:

            raw_rows.append(
                action_specific_features(
                    row,
                    predicted_risks[
                        index
                    ],
                    predicted_losses[
                        index
                    ],
                    action,
                )
            )

            action_labels.append(
                action
            )

    matrix = np.asarray(
        raw_rows,
        dtype=float,
    )

    scaler = StandardScaler()

    scaled = scaler.fit_transform(
        matrix
    )

    return {
        "raw":
            matrix,

        "scaled":
            scaled,

        "scaler":
            scaler,

        "actions":
            np.asarray(
                action_labels,
                dtype=int,
            ),
    }


def mean_knn_distance(
    training_matrix: np.ndarray,
    sample: np.ndarray,
) -> float:

    distances = np.sqrt(
        np.sum(
            (
                training_matrix
                - sample
            )
            ** 2,
            axis=1,
        )
    )

    order = np.argsort(
        distances
    )

    k = min(
        K_NEIGHBORS,
        len(
            order
        ),
    )

    return float(
        np.mean(
            distances[
                order[
                    :k
                ]
            ]
        )
    )


def current_action_distance(
    support_objects: dict,
    row: dict,
    predicted_risk: float,
    predicted_losses: dict,
    action: int,
) -> float:

    raw_sample = np.asarray(
        [
            action_specific_features(
                row,
                predicted_risk,
                predicted_losses,
                action,
            )
        ],
        dtype=float,
    )

    scaled_sample = support_objects[
        action
    ][
        "scaler"
    ].transform(
        raw_sample
    )[0]

    return mean_knn_distance(
        support_objects[
            action
        ][
            "scaled"
        ],
        scaled_sample,
    )


def shared_action_distance(
    shared_object: dict,
    row: dict,
    predicted_risk: float,
    predicted_losses: dict,
    action: int,
) -> float:

    raw_sample = np.asarray(
        [
            action_specific_features(
                row,
                predicted_risk,
                predicted_losses,
                action,
            )
        ],
        dtype=float,
    )

    scaled_sample = shared_object[
        "scaler"
    ].transform(
        raw_sample
    )[0]

    matching_rows = (
        shared_object[
            "actions"
        ]
        == action
    )

    action_training_matrix = shared_object[
        "scaled"
    ][
        matching_rows
    ]

    return mean_knn_distance(
        action_training_matrix,
        scaled_sample,
    )


def max_pairwise_difference(
    values: dict[int, float],
) -> float:

    return max(
        abs(
            values[
                first
            ]
            - values[
                second
            ]
        )
        for first in ACTIONS
        for second in ACTIONS
        if first < second
    )


def save_csv(
    path: Path,
    rows: list[dict],
) -> None:

    path.parent.mkdir(
        exist_ok=True
    )

    if not rows:
        return

    fields = []

    for row in rows:

        for key in row:

            if key not in fields:
                fields.append(
                    key
                )

    normalized = []

    for row in rows:

        copy = dict(
            row
        )

        for field in fields:

            copy.setdefault(
                field,
                "",
            )

        normalized.append(
            copy
        )

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )

        writer.writeheader()
        writer.writerows(
            normalized
        )


def main() -> None:

    context_rows = []
    audit_rows = []

    current_nonzero_contexts = 0
    shared_nonzero_contexts = 0

    current_max_difference = 0.0
    shared_max_difference = 0.0

    current_pairwise_differences = []
    shared_pairwise_differences = []

    print(
        "=" * 205
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "SUPPORT METRIC ACTION-CONDITIONALITY AUDIT"
    )

    print(
        "=" * 205
    )

    print(
        f"audit seeds="
        f"{AUDIT_SEEDS}"
    )

    print()

    for generation_seed in AUDIT_SEEDS:

        print(
            f"auditing seed "
            f"{generation_seed}..."
        )

        rows = generate_analysis_rows(
            base_seed=generation_seed
        )

        (
            base_train_rows,
            meta_train_rows,
            test_rows,
        ) = three_way_split(
            rows
        )

        loss_models = train_loss_models(
            base_train_rows
        )

        occurrence_model = train_occurrence_model(
            base_train_rows
        )

        magnitude_model = train_magnitude_model(
            base_train_rows
        )

        meta_losses = predicted_loss_table(
            loss_models,
            meta_train_rows,
        )

        meta_risks = predict_two_stage_risk(
            occurrence_model,
            magnitude_model,
            meta_train_rows,
        )

        test_losses = predicted_loss_table(
            loss_models,
            test_rows,
        )

        test_risks = predict_two_stage_risk(
            occurrence_model,
            magnitude_model,
            test_rows,
        )

        current_objects = current_support_objects(
            meta_train_rows,
            meta_losses,
            meta_risks,
        )

        shared_object = shared_support_object(
            meta_train_rows,
            meta_losses,
            meta_risks,
        )

        print()

        print(
            f"seed {generation_seed} "
            f"ACTION-COORDINATE VARIANCE"
        )

        for action in ACTIONS:

            raw = current_objects[
                action
            ][
                "raw"
            ]

            scaled = current_objects[
                action
            ][
                "scaled"
            ]

            raw_action_columns = raw[
                :,
                -3:
            ]

            scaled_action_columns = scaled[
                :,
                -3:
            ]

            raw_variances = np.var(
                raw_action_columns,
                axis=0,
            )

            scaled_variances = np.var(
                scaled_action_columns,
                axis=0,
            )

            print(
                f"current metric action={action} "
                f"raw_var="
                f"{raw_variances.tolist()} "
                f"scaled_var="
                f"{scaled_variances.tolist()}"
            )

            audit_rows.append(
                {
                    "record_type":
                        "current_action_coordinate_variance",

                    "generation_seed":
                        generation_seed,

                    "action":
                        action,

                    "raw_var_action":
                        float(
                            raw_variances[
                                0
                            ]
                        ),

                    "raw_var_action_minus_1":
                        float(
                            raw_variances[
                                1
                            ]
                        ),

                    "raw_var_3_minus_action":
                        float(
                            raw_variances[
                                2
                            ]
                        ),

                    "scaled_var_action":
                        float(
                            scaled_variances[
                                0
                            ]
                        ),

                    "scaled_var_action_minus_1":
                        float(
                            scaled_variances[
                                1
                            ]
                        ),

                    "scaled_var_3_minus_action":
                        float(
                            scaled_variances[
                                2
                            ]
                        ),
                }
            )

        shared_raw_action_columns = shared_object[
            "raw"
        ][
            :,
            -3:
        ]

        shared_scaled_action_columns = shared_object[
            "scaled"
        ][
            :,
            -3:
        ]

        shared_raw_variances = np.var(
            shared_raw_action_columns,
            axis=0,
        )

        shared_scaled_variances = np.var(
            shared_scaled_action_columns,
            axis=0,
        )

        print(
            "shared metric "
            f"raw_var="
            f"{shared_raw_variances.tolist()} "
            f"scaled_var="
            f"{shared_scaled_variances.tolist()}"
        )

        audit_rows.append(
            {
                "record_type":
                    "shared_action_coordinate_variance",

                "generation_seed":
                    generation_seed,

                "action":
                    "all",

                "raw_var_action":
                    float(
                        shared_raw_variances[
                            0
                        ]
                    ),

                "raw_var_action_minus_1":
                    float(
                        shared_raw_variances[
                            1
                        ]
                    ),

                "raw_var_3_minus_action":
                    float(
                        shared_raw_variances[
                            2
                        ]
                    ),

                "scaled_var_action":
                    float(
                        shared_scaled_variances[
                            0
                        ]
                    ),

                "scaled_var_action_minus_1":
                    float(
                        shared_scaled_variances[
                            1
                        ]
                    ),

                "scaled_var_3_minus_action":
                    float(
                        shared_scaled_variances[
                            2
                        ]
                    ),
            }
        )

        for index, row in enumerate(
            test_rows
        ):

            current_distances = {
                action:
                    current_action_distance(
                        current_objects,
                        row,
                        test_risks[
                            index
                        ],
                        test_losses[
                            index
                        ],
                        action,
                    )
                for action in ACTIONS
            }

            shared_distances = {
                action:
                    shared_action_distance(
                        shared_object,
                        row,
                        test_risks[
                            index
                        ],
                        test_losses[
                            index
                        ],
                        action,
                    )
                for action in ACTIONS
            }

            current_difference = (
                max_pairwise_difference(
                    current_distances
                )
            )

            shared_difference = (
                max_pairwise_difference(
                    shared_distances
                )
            )

            current_pairwise_differences.append(
                current_difference
            )

            shared_pairwise_differences.append(
                shared_difference
            )

            current_max_difference = max(
                current_max_difference,
                current_difference,
            )

            shared_max_difference = max(
                shared_max_difference,
                shared_difference,
            )

            if (
                current_difference
                > FLOAT_TOLERANCE
            ):

                current_nonzero_contexts += 1

            if (
                shared_difference
                > FLOAT_TOLERANCE
            ):

                shared_nonzero_contexts += 1

            context_rows.append(
                {
                    "generation_seed":
                        generation_seed,

                    "test_index":
                        index,

                    "current_distance_k1":
                        current_distances[
                            1
                        ],

                    "current_distance_k2":
                        current_distances[
                            2
                        ],

                    "current_distance_k3":
                        current_distances[
                            3
                        ],

                    "current_max_pairwise_difference":
                        current_difference,

                    "shared_distance_k1":
                        shared_distances[
                            1
                        ],

                    "shared_distance_k2":
                        shared_distances[
                            2
                        ],

                    "shared_distance_k3":
                        shared_distances[
                            3
                        ],

                    "shared_max_pairwise_difference":
                        shared_difference,
                }
            )

    total_contexts = len(
        context_rows
    )

    mean_current_difference = statistics.mean(
        current_pairwise_differences
    )

    mean_shared_difference = statistics.mean(
        shared_pairwise_differences
    )

    audit_rows.extend(
        [
            {
                "record_type":
                    "distance_summary",

                "metric":
                    "current",

                "contexts":
                    total_contexts,

                "nonzero_action_separation_contexts":
                    current_nonzero_contexts,

                "nonzero_action_separation_fraction":
                    (
                        current_nonzero_contexts
                        / total_contexts
                    ),

                "mean_max_pairwise_difference":
                    mean_current_difference,

                "maximum_pairwise_difference":
                    current_max_difference,
            },
            {
                "record_type":
                    "distance_summary",

                "metric":
                    "shared",

                "contexts":
                    total_contexts,

                "nonzero_action_separation_contexts":
                    shared_nonzero_contexts,

                "nonzero_action_separation_fraction":
                    (
                        shared_nonzero_contexts
                        / total_contexts
                    ),

                "mean_max_pairwise_difference":
                    mean_shared_difference,

                "maximum_pairwise_difference":
                    shared_max_difference,
            },
        ]
    )

    save_csv(
        OUTPUT_PATH,
        audit_rows,
    )

    save_csv(
        CONTEXT_OUTPUT_PATH,
        context_rows,
    )

    print()

    print(
        "CURRENT METRIC ACTION SEPARATION"
    )

    print(
        f"contexts="
        f"{total_contexts}"
    )

    print(
        f"nonzero separation="
        f"{current_nonzero_contexts}/"
        f"{total_contexts} "
        f"("
        f"{current_nonzero_contexts / total_contexts:.3%}"
        f")"
    )

    print(
        f"mean max pairwise difference="
        f"{mean_current_difference:.12f}"
    )

    print(
        f"maximum pairwise difference="
        f"{current_max_difference:.12f}"
    )

    print()

    print(
        "SHARED-SCALER ACTION SEPARATION"
    )

    print(
        f"nonzero separation="
        f"{shared_nonzero_contexts}/"
        f"{total_contexts} "
        f"("
        f"{shared_nonzero_contexts / total_contexts:.3%}"
        f")"
    )

    print(
        f"mean max pairwise difference="
        f"{mean_shared_difference:.12f}"
    )

    print(
        f"maximum pairwise difference="
        f"{shared_max_difference:.12f}"
    )

    print()

    print(
        "FIRST 10 CONTEXT EXAMPLES"
    )

    for row in context_rows[
        :10
    ]:

        print(
            f"seed="
            f"{row['generation_seed']} "
            f"index="
            f"{row['test_index']} "
            f"current=["
            f"{row['current_distance_k1']:.6f},"
            f"{row['current_distance_k2']:.6f},"
            f"{row['current_distance_k3']:.6f}"
            f"] "
            f"current_delta="
            f"{row['current_max_pairwise_difference']:.12f} "
            f"shared=["
            f"{row['shared_distance_k1']:.6f},"
            f"{row['shared_distance_k2']:.6f},"
            f"{row['shared_distance_k3']:.6f}"
            f"] "
            f"shared_delta="
            f"{row['shared_max_pairwise_difference']:.12f}"
        )

    print()

    print(
        "AUDIT INTERPRETATION"
    )

    if (
        current_max_difference
        <= FLOAT_TOLERANCE
    ):

        print(
            "Current per-action-scaled support is exactly "
            "action-invariant within numerical tolerance."
        )

    else:

        print(
            "Current support retains measurable action separation."
        )

    if (
        shared_max_difference
        > FLOAT_TOLERANCE
    ):

        print(
            "Shared scaling preserves action-coordinate variation "
            "and produces action-dependent distances."
        )

    else:

        print(
            "Shared scaling still does not produce action separation."
        )

    print(
        "=" * 205
    )

    print(
        f"Audit summary saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Context-level audit saved to: "
        f"{CONTEXT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()