import csv
import statistics
from collections import Counter
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
)


OUTPUT_PATH = Path(
    "results/"
    "safe_action_set_recall_error_decomposition.csv"
)

CONTEXT_OUTPUT_PATH = Path(
    "results/"
    "safe_action_set_recall_error_decomposition_contexts.csv"
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


def responsive_action(
    actions: set[int],
) -> int:

    return min(
        actions
    )


def conservative_action(
    actions: set[int],
) -> int:

    return max(
        actions
    )


def safe_action_recall(
    true_actions: set[int],
    predicted_actions: set[int],
) -> float:

    if not true_actions:
        return 1.0

    return (
        len(
            true_actions
            & predicted_actions
        )
        / len(
            true_actions
        )
    )


def safe_action_precision(
    true_actions: set[int],
    predicted_actions: set[int],
) -> float:

    if not predicted_actions:
        return 1.0

    return (
        len(
            true_actions
            & predicted_actions
        )
        / len(
            predicted_actions
        )
    )


def action_text(
    actions: set[int],
) -> str:

    return "|".join(
        str(action)
        for action in sorted(
            actions
        )
    )


def lambda_text(
    levels: list[float],
) -> str:

    return "|".join(
        f"{level:.2f}"
        for level in levels
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

    recall_values = []
    precision_values = []

    responsive_retained_count = 0
    responsive_excluded_count = 0

    gate_failure_count = 0
    selection_failure_count = 0
    correct_responsive_selection_count = 0

    false_safe_action_inclusion_contexts = 0
    missed_safe_action_exclusion_contexts = 0

    false_safe_action_count = 0
    missed_safe_action_count = 0

    false_safe_regret_values = []

    responsive_absent_but_lower_action_exists = 0

    predicted_singleton_true_multi_count = 0
    predicted_multi_true_multi_count = 0

    error_type_counts = Counter()

    for index, row in enumerate(
        test_rows
    ):

        true_levels = true_minimum_levels(
            true_regrets[
                index
            ]
        )

        predicted_levels = (
            predicted_safe_levels(
                predicted_regrets[
                    index
                ]
            )
        )

        true_actions = action_set_from_levels(
            true_levels,
            candidates,
            index,
        )

        predicted_actions = action_set_from_levels(
            predicted_levels,
            candidates,
            index,
        )

        true_responsive_action = (
            responsive_action(
                true_actions
            )
        )

        true_conservative_action = (
            conservative_action(
                true_actions
            )
        )

        baseline_lambda = min(
            predicted_levels
        )

        baseline_action = int(
            candidates[
                baseline_lambda
            ][index]
        )

        intersection = (
            true_actions
            & predicted_actions
        )

        missed_actions = (
            true_actions
            - predicted_actions
        )

        false_safe_actions = (
            predicted_actions
            - true_actions
        )

        recall = safe_action_recall(
            true_actions,
            predicted_actions,
        )

        precision = safe_action_precision(
            true_actions,
            predicted_actions,
        )

        recall_values.append(
            recall
        )

        precision_values.append(
            precision
        )

        responsive_retained = (
            true_responsive_action
            in predicted_actions
        )

        if responsive_retained:
            responsive_retained_count += 1
        else:
            responsive_excluded_count += 1

        if missed_actions:
            missed_safe_action_exclusion_contexts += 1
            missed_safe_action_count += len(
                missed_actions
            )

        if false_safe_actions:
            false_safe_action_inclusion_contexts += 1
            false_safe_action_count += len(
                false_safe_actions
            )

        for false_action in (
            false_safe_actions
        ):

            false_safe_regret_values.append(
                regret(
                    row,
                    false_action,
                )
            )

        if (
            len(
                predicted_actions
            )
            == 1
            and len(
                true_actions
            )
            > 1
        ):

            predicted_singleton_true_multi_count += 1

        if (
            len(
                predicted_actions
            )
            > 1
            and len(
                true_actions
            )
            > 1
        ):

            predicted_multi_true_multi_count += 1

        if not responsive_retained:

            gate_failure_count += 1

            error_type = (
                "gate_failure"
            )

            if (
                min(
                    true_actions
                )
                < min(
                    predicted_actions
                )
            ):

                responsive_absent_but_lower_action_exists += 1

        elif (
            baseline_action
            != true_responsive_action
        ):

            selection_failure_count += 1

            error_type = (
                "selection_failure"
            )

        else:

            correct_responsive_selection_count += 1

            error_type = (
                "correct"
            )

        error_type_counts[
            error_type
        ] += 1

        false_safe_max_regret = (
            max(
                [
                    regret(
                        row,
                        action,
                    )
                    for action in false_safe_actions
                ],
                default=0.0,
            )
        )

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

                "true_minimum_levels":
                    lambda_text(
                        true_levels
                    ),

                "predicted_safe_levels":
                    lambda_text(
                        predicted_levels
                    ),

                "true_safe_actions":
                    action_text(
                        true_actions
                    ),

                "predicted_safe_actions":
                    action_text(
                        predicted_actions
                    ),

                "intersection_actions":
                    action_text(
                        intersection
                    ),

                "missed_safe_actions":
                    action_text(
                        missed_actions
                    ),

                "false_safe_actions":
                    action_text(
                        false_safe_actions
                    ),

                "safe_action_recall":
                    recall,

                "safe_action_precision":
                    precision,

                "true_responsive_action":
                    true_responsive_action,

                "true_conservative_action":
                    true_conservative_action,

                "responsive_action_retained":
                    int(
                        responsive_retained
                    ),

                "baseline_lambda":
                    baseline_lambda,

                "baseline_action":
                    baseline_action,

                "baseline_selects_responsive_action":
                    int(
                        baseline_action
                        == true_responsive_action
                    ),

                "error_type":
                    error_type,

                "false_safe_max_regret":
                    false_safe_max_regret,

                "true_safe_action_count":
                    len(
                        true_actions
                    ),

                "predicted_safe_action_count":
                    len(
                        predicted_actions
                    ),
            }
        )

    mean_recall = statistics.mean(
        recall_values
    )

    mean_precision = statistics.mean(
        precision_values
    )

    mean_false_safe_regret = (
        statistics.mean(
            false_safe_regret_values
        )
        if false_safe_regret_values
        else 0.0
    )

    max_false_safe_regret = (
        max(
            false_safe_regret_values
        )
        if false_safe_regret_values
        else 0.0
    )

    summary_rows = [
        {
            "contexts":
                total,

            "mean_safe_action_recall":
                mean_recall,

            "mean_safe_action_precision":
                mean_precision,

            "responsive_action_retained_count":
                responsive_retained_count,

            "responsive_action_retention_fraction":
                percentage(
                    responsive_retained_count,
                    total,
                ),

            "responsive_action_excluded_count":
                responsive_excluded_count,

            "responsive_action_exclusion_fraction":
                percentage(
                    responsive_excluded_count,
                    total,
                ),

            "gate_failure_count":
                gate_failure_count,

            "gate_failure_fraction":
                percentage(
                    gate_failure_count,
                    total,
                ),

            "selection_failure_count":
                selection_failure_count,

            "selection_failure_fraction":
                percentage(
                    selection_failure_count,
                    total,
                ),

            "correct_responsive_selection_count":
                correct_responsive_selection_count,

            "correct_responsive_selection_fraction":
                percentage(
                    correct_responsive_selection_count,
                    total,
                ),

            "missed_safe_action_exclusion_contexts":
                missed_safe_action_exclusion_contexts,

            "missed_safe_action_exclusion_fraction":
                percentage(
                    missed_safe_action_exclusion_contexts,
                    total,
                ),

            "missed_safe_action_count":
                missed_safe_action_count,

            "false_safe_action_inclusion_contexts":
                false_safe_action_inclusion_contexts,

            "false_safe_action_inclusion_fraction":
                percentage(
                    false_safe_action_inclusion_contexts,
                    total,
                ),

            "false_safe_action_count":
                false_safe_action_count,

            "mean_false_safe_action_regret":
                mean_false_safe_regret,

            "max_false_safe_action_regret":
                max_false_safe_regret,

            "predicted_singleton_true_multi_count":
                predicted_singleton_true_multi_count,

            "predicted_singleton_true_multi_fraction":
                percentage(
                    predicted_singleton_true_multi_count,
                    total,
                ),

            "predicted_multi_true_multi_count":
                predicted_multi_true_multi_count,

            "predicted_multi_true_multi_fraction":
                percentage(
                    predicted_multi_true_multi_count,
                    total,
                ),

            "responsive_absent_but_lower_action_exists":
                responsive_absent_but_lower_action_exists,

            "responsive_absent_but_lower_action_exists_fraction":
                percentage(
                    responsive_absent_but_lower_action_exists,
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

    print("=" * 190)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "SAFE-ACTION-SET RECALL AND "
        "ERROR DECOMPOSITION"
    )

    print("=" * 190)

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
        "SAFE-ACTION SET QUALITY"
    )

    print(
        "mean action recall="
        f"{mean_recall:.3%}"
    )

    print(
        "mean action precision="
        f"{mean_precision:.3%}"
    )

    print()

    print(
        "RESPONSIVE ACTION RETENTION"
    )

    print(
        "responsive action retained="
        f"{responsive_retained_count}/"
        f"{total} "
        f"("
        f"{percentage(responsive_retained_count, total):.3%}"
        f")"
    )

    print(
        "responsive action excluded="
        f"{responsive_excluded_count}/"
        f"{total} "
        f"("
        f"{percentage(responsive_excluded_count, total):.3%}"
        f")"
    )

    print()

    print(
        "ERROR DECOMPOSITION"
    )

    print(
        "gate failures="
        f"{gate_failure_count}/"
        f"{total} "
        f"("
        f"{percentage(gate_failure_count, total):.3%}"
        f")"
    )

    print(
        "selection failures="
        f"{selection_failure_count}/"
        f"{total} "
        f"("
        f"{percentage(selection_failure_count, total):.3%}"
        f")"
    )

    print(
        "correct responsive selections="
        f"{correct_responsive_selection_count}/"
        f"{total} "
        f"("
        f"{percentage(correct_responsive_selection_count, total):.3%}"
        f")"
    )

    print()

    print(
        "SAFE-SET FALSE NEGATIVES"
    )

    print(
        "contexts with missed true-safe actions="
        f"{missed_safe_action_exclusion_contexts}/"
        f"{total} "
        f"("
        f"{percentage(missed_safe_action_exclusion_contexts, total):.3%}"
        f")"
    )

    print(
        "total missed safe actions="
        f"{missed_safe_action_count}"
    )

    print(
        "predicted singleton while truth multi-action="
        f"{predicted_singleton_true_multi_count}/"
        f"{total} "
        f"("
        f"{percentage(predicted_singleton_true_multi_count, total):.3%}"
        f")"
    )

    print()

    print(
        "SAFE-SET FALSE POSITIVES"
    )

    print(
        "contexts with false-safe actions="
        f"{false_safe_action_inclusion_contexts}/"
        f"{total} "
        f"("
        f"{percentage(false_safe_action_inclusion_contexts, total):.3%}"
        f")"
    )

    print(
        "total false-safe actions="
        f"{false_safe_action_count}"
    )

    print(
        "mean false-safe regret="
        f"{mean_false_safe_regret:.6f}"
    )

    print(
        "max false-safe regret="
        f"{max_false_safe_regret:.6f}"
    )

    print()

    print(
        "STRUCTURAL DIAGNOSTIC"
    )

    print(
        "predicted multi-action and true multi-action="
        f"{predicted_multi_true_multi_count}/"
        f"{total} "
        f"("
        f"{percentage(predicted_multi_true_multi_count, total):.3%}"
        f")"
    )

    print(
        "responsive action absent while "
        "a lower safe action truly exists="
        f"{responsive_absent_but_lower_action_exists}/"
        f"{total} "
        f"("
        f"{percentage(responsive_absent_but_lower_action_exists, total):.3%}"
        f")"
    )

    print("=" * 190)

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