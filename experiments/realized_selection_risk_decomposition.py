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
    "realized_selection_risk_decomposition.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "realized_selection_risk_decomposition_contexts.csv"
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

            if action in safe_actions:

                downside = 0.0

            else:

                downside = max(
                    0.0,
                    regret(
                        row,
                        action,
                    ),
                )

            y.append(
                downside
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


def positive_probability(
    model: RandomForestClassifier,
    x: list[list[float]],
) -> list[float]:

    probabilities = model.predict_proba(
        x
    )

    classes = list(
        model.classes_
    )

    if 1 not in classes:

        return [
            0.0
            for _ in x
        ]

    positive_index = classes.index(
        1
    )

    return [
        float(
            row[
                positive_index
            ]
        )
        for row in probabilities
    ]


def predict_action_safety(
    models: dict[
        int,
        RandomForestClassifier,
    ],
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> list[dict]:

    output = [
        {}
        for _ in rows
    ]

    for action in (
        ACTIONS
    ):

        x = [
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
        ]

        scores = positive_probability(
            models[
                action
            ],
            x,
        )

        for index, score in enumerate(
            scores
        ):

            output[
                index
            ][
                action
            ] = score

    return output


def predict_action_downside(
    models: dict[
        int,
        RandomForestRegressor,
    ],
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> list[dict]:

    output = [
        {}
        for _ in rows
    ]

    for action in (
        ACTIONS
    ):

        x = [
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
        ]

        predictions = models[
            action
        ].predict(
            x
        )

        for index, value in enumerate(
            predictions
        ):

            output[
                index
            ][
                action
            ] = max(
                0.0,
                float(
                    value
                ),
            )

    return output


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

    safety_scores = predict_action_safety(
        safety_models,
        test_rows,
        test_losses,
        test_risks,
    )

    downside_scores = predict_action_downside(
        downside_models,
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

        added_actions = []

        for action in (
            ACTIONS
        ):

            if action in expanded_actions:
                continue

            if (
                safety_scores[
                    index
                ][
                    action
                ]
                >= SAFETY_THRESHOLD
                and downside_scores[
                    index
                ][
                    action
                ]
                <= DOWNSIDE_THRESHOLD
            ):

                expanded_actions.add(
                    action
                )

                added_actions.append(
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

        incremental_regret = (
            expanded_regret
            - primary_regret
        )

        action_step = (
            primary_action
            - expanded_action
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

        selected_safety_score = safety_scores[
            index
        ][
            expanded_action
        ]

        selected_downside_score = downside_scores[
            index
        ][
            expanded_action
        ]

        realized_downside = max(
            0.0,
            expanded_regret,
        )

        downside_error = (
            realized_downside
            - selected_downside_score
        )

        safety_overconfidence = (
            selected_safety_score
            if expanded_action
            not in true_actions
            else 0.0
        )

        predicted_primary_regret = min(
            predicted_regrets[
                index
            ][
                risk_level
            ]
            for risk_level
            in primary_levels
        )

        predicted_regret_for_expanded_action = min(
            [
                predicted_regrets[
                    index
                ][
                    risk_level
                ]
                for risk_level
                in RISK_LEVELS
                if int(
                    candidates[
                        risk_level
                    ][index]
                )
                == expanded_action
            ],
            default=predicted_primary_regret,
        )

        predicted_regret_margin = (
            predicted_regret_for_expanded_action
            - predicted_primary_regret
        )

        record = {
            "test_index":
                index,

            "outcome":
                outcome,

            "best_persistence":
                int(
                    row[
                        "best_persistence"
                    ]
                ),

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

            "added_actions":
                action_text(
                    set(
                        added_actions
                    )
                ),

            "primary_action":
                primary_action,

            "expanded_action":
                expanded_action,

            "true_responsive_action":
                true_responsive_action,

            "action_step":
                action_step,

            "primary_regret":
                primary_regret,

            "expanded_regret":
                expanded_regret,

            "incremental_regret":
                incremental_regret,

            "selected_safety_score":
                selected_safety_score,

            "selected_downside_score":
                selected_downside_score,

            "realized_downside":
                realized_downside,

            "downside_error":
                downside_error,

            "safety_overconfidence":
                safety_overconfidence,

            "predicted_primary_regret":
                predicted_primary_regret,

            "predicted_expanded_action_regret":
                predicted_regret_for_expanded_action,

            "predicted_regret_margin":
                predicted_regret_margin,

            "score_action_1":
                safety_scores[
                    index
                ][1],

            "score_action_2":
                safety_scores[
                    index
                ][2],

            "score_action_3":
                safety_scores[
                    index
                ][3],

            "downside_action_1":
                downside_scores[
                    index
                ][1],

            "downside_action_2":
                downside_scores[
                    index
                ][2],

            "downside_action_3":
                downside_scores[
                    index
                ][3],
        }

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
            [
                float(
                    record[
                        field
                    ]
                )
                for record in records
            ]
        )


    def max_field(
        records: list[dict],
        field: str,
    ) -> float:

        if not records:
            return 0.0

        return max(
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

        summary_rows.append(
            {
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

                "mean_action_step":
                    mean_field(
                        records,
                        "action_step",
                    ),

                "mean_primary_regret":
                    mean_field(
                        records,
                        "primary_regret",
                    ),

                "mean_expanded_regret":
                    mean_field(
                        records,
                        "expanded_regret",
                    ),

                "mean_incremental_regret":
                    mean_field(
                        records,
                        "incremental_regret",
                    ),

                "max_incremental_regret":
                    max_field(
                        records,
                        "incremental_regret",
                    ),

                "mean_safety_score":
                    mean_field(
                        records,
                        "selected_safety_score",
                    ),

                "mean_downside_score":
                    mean_field(
                        records,
                        "selected_downside_score",
                    ),

                "mean_realized_downside":
                    mean_field(
                        records,
                        "realized_downside",
                    ),

                "mean_downside_error":
                    mean_field(
                        records,
                        "downside_error",
                    ),

                "max_downside_error":
                    max_field(
                        records,
                        "downside_error",
                    ),

                "mean_safety_overconfidence":
                    mean_field(
                        records,
                        "safety_overconfidence",
                    ),

                "mean_predicted_regret_margin":
                    mean_field(
                        records,
                        "predicted_regret_margin",
                    ),
            }
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
        "ADAPTIVE DIGITAL TWIN - "
        "REALIZED SELECTION-RISK "
        "DECOMPOSITION"
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
        f"risk-model contexts="
        f"{len(meta_train_rows)}"
    )

    print(
        f"test contexts="
        f"{len(test_rows)}"
    )

    print(
        f"primary epsilon="
        f"{PRIMARY_EPSILON:.4f}"
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
        "EXPANSION OUTCOME COUNTS"
    )

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

        print(
            f"{label:<12} "
            f"{len(records)}/"
            f"{len(test_rows)} "
            f"("
            f"{len(records) / len(test_rows):.3%}"
            f")"
        )

    print()

    print(
        "OUTCOME DIAGNOSTICS"
    )

    for summary in (
        summary_rows
    ):

        print(
            f"{summary['outcome']:<12} "
            f"mean_step="
            f"{summary['mean_action_step']:.3f} "
            f"mean_incremental_regret="
            f"{summary['mean_incremental_regret']:.6f} "
            f"max_incremental_regret="
            f"{summary['max_incremental_regret']:.6f} "
            f"mean_safety="
            f"{summary['mean_safety_score']:.3f} "
            f"mean_predicted_downside="
            f"{summary['mean_downside_score']:.6f} "
            f"mean_realized_downside="
            f"{summary['mean_realized_downside']:.6f} "
            f"mean_downside_error="
            f"{summary['mean_downside_error']:.6f} "
            f"max_downside_error="
            f"{summary['max_downside_error']:.6f} "
            f"mean_overconfidence="
            f"{summary['mean_safety_overconfidence']:.3f} "
            f"mean_predicted_regret_margin="
            f"{summary['mean_predicted_regret_margin']:.6f}"
        )

    print()

    print(
        "HARMFUL EXPANSION DETAILS"
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
                f"step="
                f"{record['action_step']} "
                f"safety="
                f"{record['selected_safety_score']:.3f} "
                f"pred_downside="
                f"{record['selected_downside_score']:.6f} "
                f"realized_regret="
                f"{record['expanded_regret']:.6f} "
                f"downside_error="
                f"{record['downside_error']:.6f} "
                f"pred_regret_margin="
                f"{record['predicted_regret_margin']:.6f}"
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