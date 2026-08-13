import csv
import statistics
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor

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
    fixed_predictions,
    oracle_predictions,
    evaluate_policy,
)


OUTPUT_PATH = Path(
    "results/"
    "responsiveness_regularized_risk_operating_point_selection.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "responsiveness_regularized_risk_operating_point_selection_contexts.csv"
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

BETA_VALUES = [
    0.000,
    0.001,
    0.0025,
    0.005,
    0.010,
    0.020,
    0.050,
]

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


def candidate_predictions(
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict[
    float,
    list[int],
]:

    output = {}

    for risk_level in (
        RISK_LEVELS
    ):

        if risk_level == 0.0:

            output[
                risk_level
            ] = direct_predictions(
                predicted_losses
            )

        else:

            output[
                risk_level
            ] = adaptive_risk_predictions(
                predicted_losses,
                predicted_risks,
                risk_level,
            )

    return output


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

    arrays = {
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
                            arrays[
                                risk_level
                            ][index]
                        ),
                    )
                for risk_level
                in RISK_LEVELS
            }
        )

    return output


def conservatism_cost(
    risk_level: float,
) -> float:

    maximum = max(
        RISK_LEVELS
    )

    if maximum <= 0.0:
        return 0.0

    return (
        risk_level
        / maximum
    )


def select_regularized_risk_levels(
    predicted_regrets: list[dict],
    beta: float,
) -> list[float]:

    output = []

    for row in predicted_regrets:

        selected = min(
            RISK_LEVELS,
            key=lambda risk_level: (
                row[
                    risk_level
                ]
                + beta
                * conservatism_cost(
                    risk_level
                ),
                risk_level,
            ),
        )

        output.append(
            selected
        )

    return output


def actions_from_selected_risk(
    selected_risk_levels: list[float],
    candidates: dict[
        float,
        list[int],
    ],
) -> list[int]:

    return [
        int(
            candidates[
                risk_level
            ][index]
        )
        for index, risk_level in enumerate(
            selected_risk_levels
        )
    ]


def oracle_risk_levels(
    rows: list[dict],
    candidates: dict[
        float,
        list[int],
    ],
) -> list[float]:

    output = []

    for index, row in enumerate(
        rows
    ):

        selected = min(
            RISK_LEVELS,
            key=lambda risk_level: (
                regret(
                    row,
                    candidates[
                        risk_level
                    ][index],
                ),
                risk_level,
            ),
        )

        output.append(
            selected
        )

    return output


def save_csv(
    path: Path,
    rows: list[dict],
) -> None:

    path.parent.mkdir(
        exist_ok=True
    )

    with path.open(
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


def print_policy_result(
    result: dict,
) -> None:

    print(
        f"{result['policy']:<30} "
        f"mean_regret="
        f"{result['mean_regret']:.6f} "
        f"zero_regret="
        f"{result['zero_regret_fraction']:.3%} "
        f"regret>0.005="
        f"{result['regret_gt_0_005_fraction']:.3%} "
        f"under="
        f"{result['under_count']:<2} "
        f"over="
        f"{result['over_count']:<2} "
        f"entropy="
        f"{result['action_entropy']:.3f} "
        f"dominant="
        f"{result['dominant_action_fraction']:.3%}"
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

    occurrence_model = (
        train_occurrence_model(
            base_train_rows
        )
    )

    magnitude_model = (
        train_magnitude_model(
            base_train_rows
        )
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

    regret_models = train_regret_models(
        meta_train_rows,
        meta_losses,
        meta_risks,
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

    predicted_regrets = (
        predicted_regret_table(
            regret_models,
            test_rows,
            test_losses,
            test_risks,
        )
    )

    candidates = candidate_predictions(
        test_losses,
        test_risks,
    )

    direct = candidates[
        0.00
    ]

    evaluations = []

    evaluations.append(
        evaluate_policy(
            name="direct_loss",
            predictions=direct,
            rows=test_rows,
            direct=direct,
        )
    )

    for risk_level in [
        0.10,
        0.25,
        1.00,
    ]:

        evaluations.append(
            evaluate_policy(
                name=(
                    "fixed_lambda_"
                    f"{risk_level:.2f}"
                ),
                predictions=candidates[
                    risk_level
                ],
                rows=test_rows,
                direct=direct,
            )
        )

    regularized_context_rows = []

    for beta in (
        BETA_VALUES
    ):

        selected_levels = (
            select_regularized_risk_levels(
                predicted_regrets,
                beta,
            )
        )

        selected_actions = (
            actions_from_selected_risk(
                selected_levels,
                candidates,
            )
        )

        result = evaluate_policy(
            name=(
                "regularized_beta_"
                f"{beta:.4f}"
            ),
            predictions=selected_actions,
            rows=test_rows,
            direct=direct,
        )

        result[
            "beta"
        ] = beta

        result[
            "mean_selected_lambda"
        ] = statistics.mean(
            selected_levels
        )

        evaluations.append(
            result
        )

        for index, (
            row,
            selected_level,
            selected_action,
        ) in enumerate(
            zip(
                test_rows,
                selected_levels,
                selected_actions,
            )
        ):

            regularized_context_rows.append(
                {
                    "beta":
                        beta,

                    "test_index":
                        index,

                    "best_persistence":
                        int(
                            row[
                                "best_persistence"
                            ]
                        ),

                    "predicted_under_risk":
                        float(
                            test_risks[
                                index
                            ]
                        ),

                    "selected_lambda":
                        selected_level,

                    "selected_action":
                        selected_action,

                    "selected_regret":
                        regret(
                            row,
                            selected_action,
                        ),

                    "predicted_regret":
                        predicted_regrets[
                            index
                        ][
                            selected_level
                        ],

                    "regularization_cost":
                        beta
                        * conservatism_cost(
                            selected_level
                        ),
                }
            )

    true_oracle_levels = (
        oracle_risk_levels(
            test_rows,
            candidates,
        )
    )

    oracle_actions = (
        actions_from_selected_risk(
            true_oracle_levels,
            candidates,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="oracle_lambda",
            predictions=oracle_actions,
            rows=test_rows,
            direct=direct,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="fixed_k3",
            predictions=fixed_predictions(
                3,
                test_rows,
            ),
            rows=test_rows,
            direct=direct,
        )
    )

    evaluations.append(
        evaluate_policy(
            name="action_oracle",
            predictions=oracle_predictions(
                test_rows
            ),
            rows=test_rows,
            direct=direct,
        )
    )

    all_fields = []

    for row in evaluations:

        for key in row.keys():

            if key not in all_fields:
                all_fields.append(
                    key
                )

    for row in evaluations:

        for field in all_fields:

            row.setdefault(
                field,
                ""
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
            fieldnames=all_fields,
        )

        writer.writeheader()
        writer.writerows(
            evaluations
        )

    save_csv(
        CONTEXT_OUTPUT_PATH,
        regularized_context_rows,
    )

    print("=" * 180)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "RESPONSIVENESS-REGULARIZED "
        "RISK OPERATING-POINT SELECTION"
    )

    print("=" * 180)

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
        f"regret-model contexts="
        f"{len(meta_train_rows)}"
    )

    print(
        f"test contexts="
        f"{len(test_rows)}"
    )

    print()

    print(
        "POLICY PERFORMANCE"
    )

    for result in evaluations:

        print_policy_result(
            result
        )

    print()

    print(
        "REGULARIZATION SWEEP"
    )

    for result in evaluations:

        if not result[
            "policy"
        ].startswith(
            "regularized_beta_"
        ):
            continue

        print(
            f"beta="
            f"{float(result['beta']):.4f} "
            f"mean_lambda="
            f"{float(result['mean_selected_lambda']):.4f} "
            f"regret="
            f"{result['mean_regret']:.6f} "
            f"under="
            f"{result['under_count']} "
            f"over="
            f"{result['over_count']} "
            f"entropy="
            f"{result['action_entropy']:.3f} "
            f"dominant="
            f"{result['dominant_action_fraction']:.3%}"
        )

    print("=" * 180)

    print(
        f"Policy results saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Context results saved to: "
        f"{CONTEXT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()