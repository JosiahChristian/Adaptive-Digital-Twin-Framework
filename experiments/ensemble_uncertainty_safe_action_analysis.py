import csv
import statistics
from pathlib import Path

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
)

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
    adaptive_risk_predictions,
    direct_predictions,
)


OUTPUT_PATH = Path(
    "results/"
    "ensemble_uncertainty_safe_action_analysis.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "ensemble_uncertainty_safe_action_analysis_contexts.csv"
)

BASE_GENERATION_SEED = 44000

TEST_FRACTION = 0.30
META_FRACTION = 0.30

RISK_LEVELS = [
    0.00,
    0.10,
    0.25,
    1.00,
]

ACTIONS = [
    1,
    2,
    3,
]

PRIMARY_EPSILON = 0.0005

SAFETY_THRESHOLD = 0.60
DOWNSIDE_THRESHOLD = 0.020

K_VALUES = [
    0.0,
    0.25,
    0.50,
    0.75,
    1.00,
    1.25,
    1.50,
    2.00,
]

FLOAT_TOLERANCE = 1e-12
RANDOM_STATE = 42


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


def selected_loss(
    row: dict,
    persistence: int,
) -> float:

    return float(
        row[
            f"loss_k{persistence}"
        ]
    )


def regret(
    row: dict,
    persistence: int,
) -> float:

    return (
        selected_loss(
            row,
            persistence,
        )
        - float(
            row[
                "best_loss"
            ]
        )
    )


def feature_vector(
    row: dict,
    predicted_risk: float,
    predicted_losses: dict,
) -> list[float]:

    base_features = [
        float(
            row[name]
        )
        for name in FEATURE_NAMES
    ]

    loss_k1 = float(
        predicted_losses[1]
    )

    loss_k2 = float(
        predicted_losses[2]
    )

    loss_k3 = float(
        predicted_losses[3]
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


def candidate_predictions(
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict[
    float,
    list[int],
]:

    output = {
        0.00:
            direct_predictions(
                predicted_losses
            )
    }

    for risk_level in [
        0.10,
        0.25,
        1.00,
    ]:

        output[
            risk_level
        ] = adaptive_risk_predictions(
            predicted_losses,
            predicted_risks,
            risk_level,
        )

    return output


def true_regret_table(
    rows: list[dict],
    candidates: dict[
        float,
        list[int],
    ],
) -> list[dict]:

    output = []

    for index, row in enumerate(
        rows
    ):

        output.append(
            {
                risk_level:
                    regret(
                        row,
                        candidates[
                            risk_level
                        ][index],
                    )
                for risk_level
                in RISK_LEVELS
            }
        )

    return output


def true_minimum_levels(
    regret_row: dict,
) -> list[float]:

    minimum = min(
        regret_row.values()
    )

    return [
        risk_level
        for risk_level
        in RISK_LEVELS
        if abs(
            regret_row[
                risk_level
            ]
            - minimum
        )
        <= FLOAT_TOLERANCE
    ]


def true_safe_actions(
    regret_row: dict,
    candidates: dict[
        float,
        list[int],
    ],
    index: int,
) -> set[int]:

    levels = true_minimum_levels(
        regret_row
    )

    return {
        int(
            candidates[
                risk_level
            ][index]
        )
        for risk_level
        in levels
    }


def train_regret_models(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict[
    float,
    RandomForestRegressor,
]:

    candidates = candidate_predictions(
        predicted_losses,
        predicted_risks,
    )

    x = [
        feature_vector(
            row,
            predicted_risk,
            loss_row,
        )
        for (
            row,
            predicted_risk,
            loss_row,
        ) in zip(
            rows,
            predicted_risks,
            predicted_losses,
        )
    ]

    models = {}

    for risk_level in (
        RISK_LEVELS
    ):

        y = [
            regret(
                row,
                candidates[
                    risk_level
                ][index],
            )
            for index, row in enumerate(
                rows
            )
        ]

        model = RandomForestRegressor(
            n_estimators=700,
            min_samples_leaf=2,
            random_state=(
                RANDOM_STATE
                + int(
                    risk_level
                    * 1000
                )
                + 1
            ),
        )

        model.fit(
            x,
            y,
        )

        models[
            risk_level
        ] = model

    return models


def predicted_regret_table(
    models: dict[
        float,
        RandomForestRegressor,
    ],
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> list[dict]:

    x = [
        feature_vector(
            row,
            predicted_risk,
            loss_row,
        )
        for (
            row,
            predicted_risk,
            loss_row,
        ) in zip(
            rows,
            predicted_risks,
            predicted_losses,
        )
    ]

    predictions = {
        risk_level:
            models[
                risk_level
            ].predict(
                x
            )
        for risk_level
        in RISK_LEVELS
    }

    output = []

    for index in range(
        len(rows)
    ):

        output.append(
            {
                risk_level:
                    max(
                        0.0,
                        float(
                            predictions[
                                risk_level
                            ][index]
                        ),
                    )
                for risk_level
                in RISK_LEVELS
            }
        )

    return output


def predicted_safe_levels(
    predicted_regret_row: dict,
) -> list[float]:

    minimum = min(
        predicted_regret_row.values()
    )

    return [
        risk_level
        for risk_level
        in RISK_LEVELS
        if (
            predicted_regret_row[
                risk_level
            ]
            <= (
                minimum
                + PRIMARY_EPSILON
                + FLOAT_TOLERANCE
            )
        )
    ]


def action_set_from_levels(
    levels: list[float],
    candidates: dict[
        float,
        list[int],
    ],
    index: int,
) -> set[int]:

    return {
        int(
            candidates[
                risk_level
            ][index]
        )
        for risk_level
        in levels
    }


def train_action_safety_models(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
    candidates: dict[
        float,
        list[int],
    ],
) -> dict[
    int,
    RandomForestClassifier,
]:

    true_regrets = true_regret_table(
        rows,
        candidates,
    )

    models = {}

    for action in (
        ACTIONS
    ):

        x = []
        y = []

        for index, row in enumerate(
            rows
        ):

            x.append(
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

            safe_actions = true_safe_actions(
                true_regrets[
                    index
                ],
                candidates,
                index,
            )

            y.append(
                int(
                    action
                    in safe_actions
                )
            )

        model = RandomForestClassifier(
            n_estimators=800,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=(
                RANDOM_STATE
                + 9000
                + action
            ),
        )

        model.fit(
            x,
            y,
        )

        models[
            action
        ] = model

    return models


def train_action_downside_models(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
    candidates: dict[
        float,
        list[int],
    ],
) -> dict[
    int,
    RandomForestRegressor,
]:

    true_regrets = true_regret_table(
        rows,
        candidates,
    )

    models = {}

    for action in (
        ACTIONS
    ):

        x = []
        y = []

        for index, row in enumerate(
            rows
        ):

            safe_actions = true_safe_actions(
                true_regrets[
                    index
                ],
                candidates,
                index,
            )

            x.append(
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

            target = (
                0.0
                if action in safe_actions
                else max(
                    0.0,
                    regret(
                        row,
                        action,
                    ),
                )
            )

            y.append(
                target
            )

        model = RandomForestRegressor(
            n_estimators=800,
            min_samples_leaf=2,
            random_state=(
                RANDOM_STATE
                + 12000
                + action
            ),
        )

        model.fit(
            x,
            y,
        )

        models[
            action
        ] = model

    return models


def tree_classifier_probability(
    tree,
    sample: list[float],
) -> float:

    probabilities = tree.predict_proba(
        [
            sample
        ]
    )[0]

    classes = list(
        tree.classes_
    )

    if 1 not in classes:
        return 0.0

    positive_index = classes.index(
        1
    )

    return float(
        probabilities[
            positive_index
        ]
    )


def classifier_ensemble_stats(
    model: RandomForestClassifier,
    sample: list[float],
) -> tuple[
    float,
    float,
]:

    values = [
        tree_classifier_probability(
            tree,
            sample,
        )
        for tree in model.estimators_
    ]

    mean_value = statistics.mean(
        values
    )

    std_value = (
        statistics.pstdev(
            values
        )
        if len(values) > 1
        else 0.0
    )

    return (
        mean_value,
        std_value,
    )


def regressor_ensemble_stats(
    model: RandomForestRegressor,
    sample: list[float],
) -> tuple[
    float,
    float,
]:

    values = [
        max(
            0.0,
            float(
                tree.predict(
                    [
                        sample
                    ]
                )[0]
            ),
        )
        for tree in model.estimators_
    ]

    mean_value = statistics.mean(
        values
    )

    std_value = (
        statistics.pstdev(
            values
        )
        if len(values) > 1
        else 0.0
    )

    return (
        mean_value,
        std_value,
    )


def responsive_action(
    actions: set[int],
) -> int:

    return min(
        actions
    )


def action_text(
    actions: set[int],
) -> str:

    return "|".join(
        str(
            action
        )
        for action in sorted(
            actions
        )
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

        for key in row.keys():

            if key not in fields:
                fields.append(
                    key
                )

    for row in rows:

        for field in fields:

            row.setdefault(
                field,
                ""
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
            rows
        )


def main() -> None:

    rows = generate_analysis_rows(
        base_seed=BASE_GENERATION_SEED
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

    meta_candidates = candidate_predictions(
        meta_losses,
        meta_risks,
    )

    regret_models = train_regret_models(
        meta_train_rows,
        meta_losses,
        meta_risks,
    )

    safety_models = train_action_safety_models(
        meta_train_rows,
        meta_losses,
        meta_risks,
        meta_candidates,
    )

    downside_models = train_action_downside_models(
        meta_train_rows,
        meta_losses,
        meta_risks,
        meta_candidates,
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

    candidates = candidate_predictions(
        test_losses,
        test_risks,
    )

    predicted_regrets = predicted_regret_table(
        regret_models,
        test_rows,
        test_losses,
        test_risks,
    )

    true_regrets = true_regret_table(
        test_rows,
        candidates,
    )

    context_rows = []

    beneficial_rows = []
    neutral_rows = []
    harmful_rows = []

    for index, row in enumerate(
        test_rows
    ):

        primary_levels = predicted_safe_levels(
            predicted_regrets[
                index
            ]
        )

        primary_actions = action_set_from_levels(
            primary_levels,
            candidates,
            index,
        )

        true_actions = true_safe_actions(
            true_regrets[
                index
            ],
            candidates,
            index,
        )

        expanded_actions = set(
            primary_actions
        )

        action_stats = {}

        for action in (
            ACTIONS
        ):

            sample = action_specific_features(
                row,
                test_risks[
                    index
                ],
                test_losses[
                    index
                ],
                action,
            )

            (
                safety_mean,
                safety_std,
            ) = classifier_ensemble_stats(
                safety_models[
                    action
                ],
                sample,
            )

            (
                downside_mean,
                downside_std,
            ) = regressor_ensemble_stats(
                downside_models[
                    action
                ],
                sample,
            )

            action_stats[
                action
            ] = {
                "safety_mean":
                    safety_mean,

                "safety_std":
                    safety_std,

                "downside_mean":
                    downside_mean,

                "downside_std":
                    downside_std,
            }

            if action in primary_actions:
                continue

            if (
                safety_mean
                >= SAFETY_THRESHOLD
                and downside_mean
                <= DOWNSIDE_THRESHOLD
            ):

                expanded_actions.add(
                    action
                )

        primary_action = responsive_action(
            primary_actions
        )

        expanded_action = responsive_action(
            expanded_actions
        )

        true_responsive_action = responsive_action(
            true_actions
        )

        primary_regret = regret(
            row,
            primary_action,
        )

        expanded_regret = regret(
            row,
            expanded_action,
        )

        changed_action = (
            expanded_action
            != primary_action
        )

        if not changed_action:

            outcome = "neutral"

        elif (
            expanded_action
            == true_responsive_action
            and expanded_regret
            <= primary_regret
            + FLOAT_TOLERANCE
        ):

            outcome = "beneficial"

        elif (
            expanded_regret
            > primary_regret
            + FLOAT_TOLERANCE
        ):

            outcome = "harmful"

        else:

            outcome = "neutral"

        selected_stats = action_stats[
            expanded_action
        ]

        record = {
            "test_index":
                index,

            "outcome":
                outcome,

            "primary_actions":
                action_text(
                    primary_actions
                ),

            "expanded_actions":
                action_text(
                    expanded_actions
                ),

            "true_safe_actions":
                action_text(
                    true_actions
                ),

            "primary_action":
                primary_action,

            "expanded_action":
                expanded_action,

            "true_responsive_action":
                true_responsive_action,

            "primary_regret":
                primary_regret,

            "expanded_regret":
                expanded_regret,

            "incremental_regret":
                (
                    expanded_regret
                    - primary_regret
                ),

            "selected_safety_mean":
                selected_stats[
                    "safety_mean"
                ],

            "selected_safety_std":
                selected_stats[
                    "safety_std"
                ],

            "selected_downside_mean":
                selected_stats[
                    "downside_mean"
                ],

            "selected_downside_std":
                selected_stats[
                    "downside_std"
                ],

            "selected_realized_regret":
                expanded_regret,
        }

        for k in (
            K_VALUES
        ):

            record[
                f"safety_lcb_k_{k:.2f}"
            ] = (
                selected_stats[
                    "safety_mean"
                ]
                - (
                    k
                    * selected_stats[
                        "safety_std"
                    ]
                )
            )

            record[
                f"downside_ucb_k_{k:.2f}"
            ] = (
                selected_stats[
                    "downside_mean"
                ]
                + (
                    k
                    * selected_stats[
                        "downside_std"
                    ]
                )
            )

        context_rows.append(
            record
        )

        if outcome == "beneficial":

            beneficial_rows.append(
                record
            )

        elif outcome == "harmful":

            harmful_rows.append(
                record
            )

        else:

            neutral_rows.append(
                record
            )

    def mean_field(
        records: list[dict],
        field: str,
    ) -> float:

        if not records:
            return 0.0

        return statistics.mean(
            float(
                record[
                    field
                ]
            )
            for record in records
        )


    summary_rows = []

    for label, records in [
        (
            "beneficial",
            beneficial_rows,
        ),
        (
            "neutral",
            neutral_rows,
        ),
        (
            "harmful",
            harmful_rows,
        ),
    ]:

        summary = {
            "outcome":
                label,

            "contexts":
                len(
                    records
                ),

            "fraction":
                (
                    len(
                        records
                    )
                    / len(
                        test_rows
                    )
                ),

            "mean_safety":
                mean_field(
                    records,
                    "selected_safety_mean",
                ),

            "mean_safety_std":
                mean_field(
                    records,
                    "selected_safety_std",
                ),

            "mean_downside":
                mean_field(
                    records,
                    "selected_downside_mean",
                ),

            "mean_downside_std":
                mean_field(
                    records,
                    "selected_downside_std",
                ),

            "mean_realized_regret":
                mean_field(
                    records,
                    "selected_realized_regret",
                ),
        }

        for k in (
            K_VALUES
        ):

            summary[
                f"mean_safety_lcb_k_{k:.2f}"
            ] = mean_field(
                records,
                f"safety_lcb_k_{k:.2f}",
            )

            summary[
                f"mean_downside_ucb_k_{k:.2f}"
            ] = mean_field(
                records,
                f"downside_ucb_k_{k:.2f}",
            )

        summary_rows.append(
            summary
        )

    print("=" * 195)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "ENSEMBLE UNCERTAINTY "
        "SAFE-ACTION ANALYSIS"
    )

    print("=" * 195)

    print(
        f"generation seed="
        f"{BASE_GENERATION_SEED}"
    )

    print(
        f"total contexts="
        f"{len(rows)}"
    )

    print(
        f"base-training contexts="
        f"{len(base_train_rows)}"
    )

    print(
        f"uncertainty-model contexts="
        f"{len(meta_train_rows)}"
    )

    print(
        f"test contexts="
        f"{len(test_rows)}"
    )

    print(
        f"safety threshold="
        f"{SAFETY_THRESHOLD:.2f}"
    )

    print(
        f"downside threshold="
        f"{DOWNSIDE_THRESHOLD:.3f}"
    )

    print()

    print(
        "OUTCOME UNCERTAINTY SUMMARY"
    )

    for summary in (
        summary_rows
    ):

        print(
            f"{summary['outcome']:<12} "
            f"n="
            f"{summary['contexts']:<2} "
            f"mean_safety="
            f"{summary['mean_safety']:.3f} "
            f"safety_std="
            f"{summary['mean_safety_std']:.3f} "
            f"mean_downside="
            f"{summary['mean_downside']:.6f} "
            f"downside_std="
            f"{summary['mean_downside_std']:.6f} "
            f"realized_regret="
            f"{summary['mean_realized_regret']:.6f}"
        )

    print()

    print(
        "CONFIDENCE-BOUND SWEEP"
    )

    for k in (
        K_VALUES
    ):

        beneficial_lcb = mean_field(
            beneficial_rows,
            f"safety_lcb_k_{k:.2f}",
        )

        harmful_lcb = mean_field(
            harmful_rows,
            f"safety_lcb_k_{k:.2f}",
        )

        beneficial_ucb = mean_field(
            beneficial_rows,
            f"downside_ucb_k_{k:.2f}",
        )

        harmful_ucb = mean_field(
            harmful_rows,
            f"downside_ucb_k_{k:.2f}",
        )

        print(
            f"k={k:.2f} "
            f"beneficial_LCB="
            f"{beneficial_lcb:.3f} "
            f"harmful_LCB="
            f"{harmful_lcb:.3f} "
            f"beneficial_UCB="
            f"{beneficial_ucb:.6f} "
            f"harmful_UCB="
            f"{harmful_ucb:.6f}"
        )

    print()

    print(
        "HARMFUL CONTEXT DETAILS"
    )

    if not harmful_rows:

        print(
            "No harmful expansion contexts."
        )

    else:

        for record in harmful_rows:

            print(
                f"test_index="
                f"{record['test_index']} "
                f"primary="
                f"{record['primary_action']} "
                f"expanded="
                f"{record['expanded_action']} "
                f"true_safe="
                f"{record['true_safe_actions']} "
                f"safety_mean="
                f"{record['selected_safety_mean']:.3f} "
                f"safety_std="
                f"{record['selected_safety_std']:.3f} "
                f"downside_mean="
                f"{record['selected_downside_mean']:.6f} "
                f"downside_std="
                f"{record['selected_downside_std']:.6f} "
                f"realized_regret="
                f"{record['selected_realized_regret']:.6f}"
            )

    save_csv(
        OUTPUT_PATH,
        summary_rows,
    )

    save_csv(
        CONTEXT_OUTPUT_PATH,
        context_rows,
    )

    print("=" * 195)

    print(
        f"Summary results saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Context results saved to: "
        f"{CONTEXT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()