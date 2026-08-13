import csv
from collections import Counter
from pathlib import Path

from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)
from experiments.responsiveness_preserving_safe_persistence_control import (
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
    "action_effective_responsiveness_analysis.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "action_effective_responsiveness_analysis_contexts.csv"
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

PRIMARY_EPSILON = 0.0005

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


def true_minimum_set(
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


def predicted_safe_set(
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


def feature_vector(
    row: dict,
    predicted_risk: float,
    predicted_losses: dict,
) -> list[float]:

    from experiments.responsiveness_preserving_safe_persistence_control import (
        FEATURE_NAMES,
    )

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


def train_regret_models(
    rows: list[dict],
    predicted_losses: list[dict],
    predicted_risks: list[float],
) -> dict:

    from sklearn.ensemble import RandomForestRegressor

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
                42
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
    models: dict,
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


def action_set(
    levels: list[float],
    candidates: dict[
        float,
        list[int],
    ],
    index: int,
) -> list[int]:

    return sorted(
        {
            int(
                candidates[
                    risk_level
                ][index]
            )
            for risk_level
            in levels
        }
    )


def lambda_text(
    levels: list[float],
) -> str:

    return "|".join(
        f"{level:.2f}"
        for level in levels
    )


def action_text(
    actions: list[int],
) -> str:

    return "|".join(
        str(
            action
        )
        for action in actions
    )


def percentage(
    numerator: int,
    denominator: int,
) -> float:

    if denominator == 0:
        return 0.0

    return (
        numerator
        / denominator
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

    total = len(
        test_rows
    )

    context_rows = []

    predicted_multi_action_contexts = 0
    true_multi_action_contexts = 0

    predicted_action_singletons = 0
    true_action_singletons = 0

    responsive_headroom_contexts = 0
    exact_regret_free_action_reduction_contexts = 0

    lambda_change_same_action_contexts = 0
    lambda_change_different_action_contexts = 0

    baseline_action_oracle_matches = 0
    baseline_lambda_oracle_matches = 0

    baseline_action_gap_total = 0
    baseline_lambda_gap_total = 0.0

    true_action_set_size_counts = Counter()
    predicted_action_set_size_counts = Counter()

    for index, row in enumerate(
        test_rows
    ):

        predicted_levels = predicted_safe_set(
            predicted_regrets[
                index
            ]
        )

        true_levels = true_minimum_set(
            true_regrets[
                index
            ]
        )

        predicted_actions = action_set(
            predicted_levels,
            candidates,
            index,
        )

        true_actions = action_set(
            true_levels,
            candidates,
            index,
        )

        predicted_action_set_size_counts[
            len(
                predicted_actions
            )
        ] += 1

        true_action_set_size_counts[
            len(
                true_actions
            )
        ] += 1

        if len(
            predicted_actions
        ) > 1:

            predicted_multi_action_contexts += 1

        else:

            predicted_action_singletons += 1

        if len(
            true_actions
        ) > 1:

            true_multi_action_contexts += 1

        else:

            true_action_singletons += 1

        responsive_true_action = min(
            true_actions
        )

        conservative_true_action = max(
            true_actions
        )

        responsive_true_lambda = min(
            true_levels,
            key=lambda risk_level: (
                int(
                    candidates[
                        risk_level
                    ][index]
                ),
                risk_level,
            ),
        )

        baseline_lambda = min(
            predicted_levels
        )

        baseline_action = int(
            candidates[
                baseline_lambda
            ][index]
        )

        if (
            responsive_true_action
            < conservative_true_action
        ):

            responsive_headroom_contexts += 1

        if (
            responsive_true_action
            < conservative_true_action
            and abs(
                min(
                    true_regrets[
                        index
                    ].values()
                )
                - true_regrets[
                    index
                ][
                    responsive_true_lambda
                ]
            )
            <= FLOAT_TOLERANCE
        ):

            exact_regret_free_action_reduction_contexts += 1

        baseline_action_gap = (
            baseline_action
            - responsive_true_action
        )

        baseline_lambda_gap = (
            baseline_lambda
            - responsive_true_lambda
        )

        baseline_action_gap_total += max(
            0,
            baseline_action_gap,
        )

        baseline_lambda_gap_total += max(
            0.0,
            baseline_lambda_gap,
        )

        if (
            baseline_action
            == responsive_true_action
        ):

            baseline_action_oracle_matches += 1

        if (
            baseline_lambda
            == responsive_true_lambda
        ):

            baseline_lambda_oracle_matches += 1

        lambda_equivalent_candidates = [
            risk_level
            for risk_level
            in predicted_levels
            if (
                risk_level
                != baseline_lambda
            )
        ]

        different_lambda_same_action = any(
            int(
                candidates[
                    risk_level
                ][index]
            )
            == baseline_action
            for risk_level
            in lambda_equivalent_candidates
        )

        different_lambda_different_action = any(
            int(
                candidates[
                    risk_level
                ][index]
            )
            != baseline_action
            for risk_level
            in lambda_equivalent_candidates
        )

        if different_lambda_same_action:

            lambda_change_same_action_contexts += 1

        if different_lambda_different_action:

            lambda_change_different_action_contexts += 1

        context_rows.append(
            {
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

                "predicted_safe_levels":
                    lambda_text(
                        predicted_levels
                    ),

                "predicted_safe_actions":
                    action_text(
                        predicted_actions
                    ),

                "predicted_safe_action_count":
                    len(
                        predicted_actions
                    ),

                "true_minimum_levels":
                    lambda_text(
                        true_levels
                    ),

                "true_safe_actions":
                    action_text(
                        true_actions
                    ),

                "true_safe_action_count":
                    len(
                        true_actions
                    ),

                "responsive_true_lambda":
                    responsive_true_lambda,

                "responsive_true_action":
                    responsive_true_action,

                "conservative_true_action":
                    conservative_true_action,

                "action_headroom":
                    (
                        conservative_true_action
                        - responsive_true_action
                    ),

                "baseline_lambda":
                    baseline_lambda,

                "baseline_action":
                    baseline_action,

                "baseline_action_gap":
                    baseline_action_gap,

                "baseline_lambda_gap":
                    baseline_lambda_gap,

                "baseline_matches_responsive_action":
                    int(
                        baseline_action
                        == responsive_true_action
                    ),

                "baseline_matches_responsive_lambda":
                    int(
                        baseline_lambda
                        == responsive_true_lambda
                    ),

                "different_lambda_same_action_available":
                    int(
                        different_lambda_same_action
                    ),

                "different_lambda_different_action_available":
                    int(
                        different_lambda_different_action
                    ),
            }
        )

    summary_rows = [
        {
            "contexts":
                total,

            "predicted_multi_action_contexts":
                predicted_multi_action_contexts,

            "predicted_multi_action_fraction":
                percentage(
                    predicted_multi_action_contexts,
                    total,
                ),

            "true_multi_action_contexts":
                true_multi_action_contexts,

            "true_multi_action_fraction":
                percentage(
                    true_multi_action_contexts,
                    total,
                ),

            "responsive_headroom_contexts":
                responsive_headroom_contexts,

            "responsive_headroom_fraction":
                percentage(
                    responsive_headroom_contexts,
                    total,
                ),

            "exact_regret_free_action_reduction_contexts":
                exact_regret_free_action_reduction_contexts,

            "exact_regret_free_action_reduction_fraction":
                percentage(
                    exact_regret_free_action_reduction_contexts,
                    total,
                ),

            "baseline_action_oracle_matches":
                baseline_action_oracle_matches,

            "baseline_action_oracle_accuracy":
                percentage(
                    baseline_action_oracle_matches,
                    total,
                ),

            "baseline_lambda_oracle_matches":
                baseline_lambda_oracle_matches,

            "baseline_lambda_oracle_accuracy":
                percentage(
                    baseline_lambda_oracle_matches,
                    total,
                ),

            "mean_positive_action_gap":
                (
                    baseline_action_gap_total
                    / total
                ),

            "mean_positive_lambda_gap":
                (
                    baseline_lambda_gap_total
                    / total
                ),

            "lambda_change_same_action_contexts":
                lambda_change_same_action_contexts,

            "lambda_change_same_action_fraction":
                percentage(
                    lambda_change_same_action_contexts,
                    total,
                ),

            "lambda_change_different_action_contexts":
                lambda_change_different_action_contexts,

            "lambda_change_different_action_fraction":
                percentage(
                    lambda_change_different_action_contexts,
                    total,
                ),
        }
    ]

    save_csv(
        OUTPUT_PATH,
        summary_rows,
    )

    save_csv(
        CONTEXT_OUTPUT_PATH,
        context_rows,
    )

    print("=" * 185)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "ACTION-EFFECTIVE RESPONSIVENESS "
        "ANALYSIS"
    )

    print("=" * 185)

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
        f"{total}"
    )

    print(
        f"primary epsilon="
        f"{PRIMARY_EPSILON:.4f}"
    )

    print()

    print(
        "SAFE ACTION-SET STRUCTURE"
    )

    print(
        "predicted safe sets with "
        "multiple distinct actions="
        f"{predicted_multi_action_contexts}/"
        f"{total} "
        f"("
        f"{percentage(predicted_multi_action_contexts, total):.3%}"
        f")"
    )

    print(
        "true minimum sets with "
        "multiple distinct actions="
        f"{true_multi_action_contexts}/"
        f"{total} "
        f"("
        f"{percentage(true_multi_action_contexts, total):.3%}"
        f")"
    )

    print()

    print(
        "TRUE SAFE ACTION-SET SIZE"
    )

    for size in sorted(
        true_action_set_size_counts
    ):

        count = true_action_set_size_counts[
            size
        ]

        print(
            f"size={size}: "
            f"{count} "
            f"("
            f"{percentage(count, total):.3%}"
            f")"
        )

    print()

    print(
        "PREDICTED SAFE ACTION-SET SIZE"
    )

    for size in sorted(
        predicted_action_set_size_counts
    ):

        count = predicted_action_set_size_counts[
            size
        ]

        print(
            f"size={size}: "
            f"{count} "
            f"("
            f"{percentage(count, total):.3%}"
            f")"
        )

    print()

    print(
        "RESPONSIVENESS HEADROOM"
    )

    print(
        "contexts with a lower "
        "true safe persistence action="
        f"{responsive_headroom_contexts}/"
        f"{total} "
        f"("
        f"{percentage(responsive_headroom_contexts, total):.3%}"
        f")"
    )

    print(
        "exact regret-free action "
        "reduction contexts="
        f"{exact_regret_free_action_reduction_contexts}/"
        f"{total} "
        f"("
        f"{percentage(exact_regret_free_action_reduction_contexts, total):.3%}"
        f")"
    )

    print()

    print(
        "BASELINE RESPONSIVE RECOVERY"
    )

    print(
        "responsive lambda accuracy="
        f"{percentage(baseline_lambda_oracle_matches, total):.3%}"
    )

    print(
        "responsive action accuracy="
        f"{percentage(baseline_action_oracle_matches, total):.3%}"
    )

    print(
        "mean positive lambda gap="
        f"{baseline_lambda_gap_total / total:.4f}"
    )

    print(
        "mean positive action gap="
        f"{baseline_action_gap_total / total:.4f}"
    )

    print()

    print(
        "LAMBDA REDUNDANCY INSIDE "
        "PREDICTED SAFE SET"
    )

    print(
        "different lambda, same action available="
        f"{lambda_change_same_action_contexts}/"
        f"{total} "
        f"("
        f"{percentage(lambda_change_same_action_contexts, total):.3%}"
        f")"
    )

    print(
        "different lambda, different action available="
        f"{lambda_change_different_action_contexts}/"
        f"{total} "
        f"("
        f"{percentage(lambda_change_different_action_contexts, total):.3%}"
        f")"
    )

    print("=" * 185)

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