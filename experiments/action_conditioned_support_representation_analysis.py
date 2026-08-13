import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    balanced_accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
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
    "action_conditioned_support_representation_analysis.csv"
)

FOLD_OUTPUT_PATH = Path(
    "results/"
    "action_conditioned_support_representation_analysis_folds.csv"
)

ACTION_OUTPUT_PATH = Path(
    "results/"
    "action_conditioned_support_representation_analysis_actions.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "action_conditioned_support_representation_analysis_coefficients.csv"
)


ANALYSIS_SEEDS = [
    44001,
    44002,
    44003,
    44004,
    44005,
    44006,
    44007,
    44008,
    44009,
    44010,
]

TEST_FRACTION = 0.30
META_FRACTION = 0.30

ACTIONS = [
    1,
    2,
    3,
]

K_NEIGHBORS = 5

REGRET_THRESHOLD = 0.005

CLASS_THRESHOLD = 0.50

FLOAT_TOLERANCE = 1e-12
RANDOM_STATE = 42


MODEL_SPECS = {
    "context_support_only": [
        "context_support_distance",
    ],

    "predicted_loss_only": [
        "predicted_action_loss",
    ],

    "context_plus_loss": [
        "context_support_distance",
        "predicted_action_loss",
    ],

    "action_support_only": [
        "action_support_distance",
    ],

    "context_plus_action_support": [
        "context_support_distance",
        "action_support_distance",
    ],

    "context_loss_action_support": [
        "context_support_distance",
        "predicted_action_loss",
        "action_support_distance",
    ],
}


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
    action: int,
) -> float:

    return float(
        row[
            f"loss_k{action}"
        ]
    )


def action_regret(
    row: dict,
    action: int,
) -> float:

    return (
        selected_loss(
            row,
            action,
        )
        - float(
            row[
                "best_loss"
            ]
        )
    )


def context_representation(
    row: dict,
    predicted_risk: float,
) -> list[float]:

    return (
        [
            float(
                row[
                    name
                ]
            )
            for name in FEATURE_NAMES
        ]
        + [
            float(
                predicted_risk
            )
        ]
    )


def normalized_loss_rank(
    predicted_losses: dict,
    action: int,
) -> float:

    current = float(
        predicted_losses[
            action
        ]
    )

    lower_count = sum(
        int(
            float(
                predicted_losses[
                    other
                ]
            )
            <
            (
                current
                - FLOAT_TOLERANCE
            )
        )
        for other in ACTIONS
        if other != action
    )

    return (
        lower_count
        / (
            len(
                ACTIONS
            )
            - 1
        )
    )


def action_conditioned_representation(
    row: dict,
    predicted_risk: float,
    predicted_losses: dict,
    action: int,
) -> list[float]:

    action_loss = float(
        predicted_losses[
            action
        ]
    )

    all_losses = [
        float(
            predicted_losses[
                other
            ]
        )
        for other in ACTIONS
    ]

    minimum_loss = min(
        all_losses
    )

    maximum_loss = max(
        all_losses
    )

    mean_loss = statistics.mean(
        all_losses
    )

    loss_range = (
        maximum_loss
        - minimum_loss
    )

    relative_to_minimum = (
        action_loss
        - minimum_loss
    )

    relative_to_mean = (
        action_loss
        - mean_loss
    )

    normalized_relative_loss = (
        relative_to_minimum
        / loss_range
        if loss_range
        > FLOAT_TOLERANCE
        else 0.0
    )

    rank = normalized_loss_rank(
        predicted_losses,
        action,
    )

    return (
        context_representation(
            row,
            predicted_risk,
        )
        + [
            action_loss,
            relative_to_minimum,
            relative_to_mean,
            normalized_relative_loss,
            rank,
        ]
    )


def build_context_support(
    rows: list[dict],
    predicted_risks: list[float],
) -> dict:

    matrix = np.asarray(
        [
            context_representation(
                row,
                predicted_risks[
                    index
                ],
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

    return {
        "scaler":
            scaler,

        "training_matrix":
            scaled,
    }


def build_action_support(
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
                action_conditioned_representation(
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
        "scaler":
            scaler,

        "training_matrix":
            scaled,

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


def context_support_distance(
    support_object: dict,
    row: dict,
    predicted_risk: float,
) -> float:

    raw = np.asarray(
        [
            context_representation(
                row,
                predicted_risk,
            )
        ],
        dtype=float,
    )

    scaled = support_object[
        "scaler"
    ].transform(
        raw
    )[0]

    return mean_knn_distance(
        support_object[
            "training_matrix"
        ],
        scaled,
    )


def action_support_distance(
    support_object: dict,
    row: dict,
    predicted_risk: float,
    predicted_losses: dict,
    action: int,
) -> float:

    raw = np.asarray(
        [
            action_conditioned_representation(
                row,
                predicted_risk,
                predicted_losses,
                action,
            )
        ],
        dtype=float,
    )

    scaled = support_object[
        "scaler"
    ].transform(
        raw
    )[0]

    mask = (
        support_object[
            "actions"
        ]
        == action
    )

    action_training_matrix = support_object[
        "training_matrix"
    ][
        mask
    ]

    return mean_knn_distance(
        action_training_matrix,
        scaled,
    )


def max_action_distance_difference(
    distances: dict[int, float],
) -> float:

    return max(
        abs(
            distances[
                first
            ]
            - distances[
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


def make_model() -> Pipeline:

    return Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "classifier",
                LogisticRegression(
                    class_weight="balanced",
                    l1_ratio=0,
                    C=1.0,
                    solver="liblinear",
                    random_state=RANDOM_STATE,
                    max_iter=5000,
                ),
            ),
        ]
    )


def build_matrix(
    rows: list[dict],
    feature_names: list[str],
) -> np.ndarray:

    return np.asarray(
        [
            [
                float(
                    row[
                        feature
                    ]
                )
                for feature in feature_names
            ]
            for row in rows
        ],
        dtype=float,
    )


def build_labels(
    rows: list[dict],
) -> np.ndarray:

    return np.asarray(
        [
            int(
                row[
                    "unsafe_action"
                ]
            )
            for row in rows
        ],
        dtype=int,
    )


def safe_auc(
    y_true: np.ndarray,
    probabilities: np.ndarray,
) -> float:

    if (
        len(
            np.unique(
                y_true
            )
        )
        < 2
    ):

        return float(
            "nan"
        )

    return float(
        roc_auc_score(
            y_true,
            probabilities,
        )
    )


def specificity_score(
    y_true: np.ndarray,
    predictions: np.ndarray,
) -> float:

    mask = (
        y_true
        == 0
    )

    if not np.any(
        mask
    ):

        return float(
            "nan"
        )

    return float(
        np.mean(
            predictions[
                mask
            ]
            == 0
        )
    )


def finite_mean(
    values: list[float],
) -> float:

    valid = [
        value
        for value in values
        if math.isfinite(
            value
        )
    ]

    if not valid:

        return float(
            "nan"
        )

    return statistics.mean(
        valid
    )


def evaluate_model(
    rows: list[dict],
    model_name: str,
    feature_names: list[str],
) -> tuple[
    dict,
    list[dict],
    list[dict],
]:

    seeds = sorted(
        {
            int(
                row[
                    "generation_seed"
                ]
            )
            for row in rows
        }
    )

    fold_rows = []
    coefficient_rows = []

    pooled_true = []
    pooled_predictions = []
    pooled_probabilities = []

    for held_out_seed in seeds:

        train_rows = [
            row
            for row in rows
            if int(
                row[
                    "generation_seed"
                ]
            )
            != held_out_seed
        ]

        test_rows = [
            row
            for row in rows
            if int(
                row[
                    "generation_seed"
                ]
            )
            == held_out_seed
        ]

        x_train = build_matrix(
            train_rows,
            feature_names,
        )

        y_train = build_labels(
            train_rows
        )

        x_test = build_matrix(
            test_rows,
            feature_names,
        )

        y_test = build_labels(
            test_rows
        )

        if (
            len(
                np.unique(
                    y_train
                )
            )
            < 2
        ):

            continue

        model = make_model()

        model.fit(
            x_train,
            y_train,
        )

        probabilities = model.predict_proba(
            x_test
        )[
            :,
            1
        ]

        predictions = (
            probabilities
            >= CLASS_THRESHOLD
        ).astype(
            int
        )

        balanced_accuracy = (
            float(
                balanced_accuracy_score(
                    y_test,
                    predictions,
                )
            )
            if len(
                np.unique(
                    y_test
                )
            )
            == 2
            else float(
                "nan"
            )
        )

        harmful_recall = float(
            recall_score(
                y_test,
                predictions,
                pos_label=1,
                zero_division=0,
            )
        )

        harmful_precision = float(
            precision_score(
                y_test,
                predictions,
                pos_label=1,
                zero_division=0,
            )
        )

        specificity = specificity_score(
            y_test,
            predictions,
        )

        auc = safe_auc(
            y_test,
            probabilities,
        )

        fold_rows.append(
            {
                "model":
                    model_name,

                "held_out_seed":
                    held_out_seed,

                "test_rows":
                    len(
                        test_rows
                    ),

                "test_unsafe":
                    int(
                        np.sum(
                            y_test
                            == 1
                        )
                    ),

                "test_safe":
                    int(
                        np.sum(
                            y_test
                            == 0
                        )
                    ),

                "balanced_accuracy":
                    balanced_accuracy,

                "unsafe_recall":
                    harmful_recall,

                "unsafe_precision":
                    harmful_precision,

                "safe_specificity":
                    specificity,

                "roc_auc":
                    auc,
            }
        )

        classifier = model.named_steps[
            "classifier"
        ]

        for feature, coefficient in zip(
            feature_names,
            classifier.coef_[
                0
            ],
        ):

            coefficient_rows.append(
                {
                    "model":
                        model_name,

                    "held_out_seed":
                        held_out_seed,

                    "feature":
                        feature,

                    "standardized_coefficient":
                        float(
                            coefficient
                        ),
                }
            )

        pooled_true.extend(
            y_test.tolist()
        )

        pooled_predictions.extend(
            predictions.tolist()
        )

        pooled_probabilities.extend(
            probabilities.tolist()
        )

    y_true = np.asarray(
        pooled_true,
        dtype=int,
    )

    y_pred = np.asarray(
        pooled_predictions,
        dtype=int,
    )

    probabilities = np.asarray(
        pooled_probabilities,
        dtype=float,
    )

    fold_balanced = [
        float(
            row[
                "balanced_accuracy"
            ]
        )
        for row in fold_rows
    ]

    fold_auc = [
        float(
            row[
                "roc_auc"
            ]
        )
        for row in fold_rows
    ]

    summary = {
        "model":
            model_name,

        "features":
            "|".join(
                feature_names
            ),

        "feature_count":
            len(
                feature_names
            ),

        "rows":
            len(
                y_true
            ),

        "unsafe_rows":
            int(
                np.sum(
                    y_true
                    == 1
                )
            ),

        "safe_rows":
            int(
                np.sum(
                    y_true
                    == 0
                )
            ),

        "balanced_accuracy":
            float(
                balanced_accuracy_score(
                    y_true,
                    y_pred,
                )
            ),

        "unsafe_recall":
            float(
                recall_score(
                    y_true,
                    y_pred,
                    pos_label=1,
                    zero_division=0,
                )
            ),

        "unsafe_precision":
            float(
                precision_score(
                    y_true,
                    y_pred,
                    pos_label=1,
                    zero_division=0,
                )
            ),

        "safe_specificity":
            specificity_score(
                y_true,
                y_pred,
            ),

        "roc_auc":
            safe_auc(
                y_true,
                probabilities,
            ),

        "mean_fold_balanced_accuracy":
            finite_mean(
                fold_balanced
            ),

        "mean_fold_roc_auc":
            finite_mean(
                fold_auc
            ),
    }

    return (
        summary,
        fold_rows,
        coefficient_rows,
    )


def coefficient_summary(
    rows: list[dict],
) -> list[dict]:

    grouped = defaultdict(
        list
    )

    for row in rows:

        grouped[
            (
                row[
                    "model"
                ],
                row[
                    "feature"
                ],
            )
        ].append(
            float(
                row[
                    "standardized_coefficient"
                ]
            )
        )

    output = []

    for (
        model_name,
        feature,
    ), values in grouped.items():

        positive_fraction = statistics.mean(
            [
                float(
                    value > 0
                )
                for value in values
            ]
        )

        negative_fraction = statistics.mean(
            [
                float(
                    value < 0
                )
                for value in values
            ]
        )

        output.append(
            {
                "model":
                    model_name,

                "feature":
                    feature,

                "folds":
                    len(
                        values
                    ),

                "mean_coefficient":
                    statistics.mean(
                        values
                    ),

                "mean_absolute_coefficient":
                    statistics.mean(
                        abs(
                            value
                        )
                        for value in values
                    ),

                "positive_fraction":
                    positive_fraction,

                "negative_fraction":
                    negative_fraction,

                "dominant_sign_fraction":
                    max(
                        positive_fraction,
                        negative_fraction,
                    ),
            }
        )

    output.sort(
        key=lambda row: (
            row[
                "model"
            ],
            -float(
                row[
                    "mean_absolute_coefficient"
                ]
            ),
        )
    )

    return output


def standardized_difference(
    safe_values: list[float],
    unsafe_values: list[float],
) -> float:

    if (
        len(
            safe_values
        )
        < 2
        or len(
            unsafe_values
        )
        < 2
    ):

        return 0.0

    safe_variance = statistics.variance(
        safe_values
    )

    unsafe_variance = statistics.variance(
        unsafe_values
    )

    numerator = (
        (
            len(
                safe_values
            )
            - 1
        )
        * safe_variance
        +
        (
            len(
                unsafe_values
            )
            - 1
        )
        * unsafe_variance
    )

    denominator = (
        len(
            safe_values
        )
        + len(
            unsafe_values
        )
        - 2
    )

    if denominator <= 0:

        return 0.0

    pooled_variance = (
        numerator
        / denominator
    )

    if (
        pooled_variance
        <= FLOAT_TOLERANCE
    ):

        return 0.0

    return (
        statistics.mean(
            unsafe_values
        )
        - statistics.mean(
            safe_values
        )
    ) / (
        pooled_variance
        ** 0.5
    )


def main() -> None:

    action_rows = []

    context_action_separations = []

    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "ACTION-CONDITIONED SUPPORT "
        "REPRESENTATION ANALYSIS"
    )

    print(
        "=" * 210
    )

    print(
        f"analysis seeds="
        f"{ANALYSIS_SEEDS}"
    )

    print(
        f"unsafe action regret threshold="
        f"{REGRET_THRESHOLD:.3f}"
    )

    print()

    for generation_seed in ANALYSIS_SEEDS:

        print(
            f"running seed "
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

        context_support = build_context_support(
            meta_train_rows,
            meta_risks,
        )

        action_support = build_action_support(
            meta_train_rows,
            meta_losses,
            meta_risks,
        )

        for index, row in enumerate(
            test_rows
        ):

            context_distance = (
                context_support_distance(
                    context_support,
                    row,
                    test_risks[
                        index
                    ],
                )
            )

            distances = {}

            for action in ACTIONS:

                distance = (
                    action_support_distance(
                        action_support,
                        row,
                        test_risks[
                            index
                        ],
                        test_losses[
                            index
                        ],
                        action,
                    )
                )

                distances[
                    action
                ] = distance

                regret_value = action_regret(
                    row,
                    action,
                )

                predicted_action_loss = float(
                    test_losses[
                        index
                    ][
                        action
                    ]
                )

                minimum_predicted_loss = min(
                    float(
                        test_losses[
                            index
                        ][
                            other
                        ]
                    )
                    for other in ACTIONS
                )

                action_rows.append(
                    {
                        "generation_seed":
                            generation_seed,

                        "test_index":
                            index,

                        "action":
                            action,

                        "context_support_distance":
                            context_distance,

                        "action_support_distance":
                            distance,

                        "action_support_minus_context":
                            (
                                distance
                                - context_distance
                            ),

                        "predicted_action_loss":
                            predicted_action_loss,

                        "predicted_relative_loss":
                            (
                                predicted_action_loss
                                - minimum_predicted_loss
                            ),

                        "realized_action_regret":
                            regret_value,

                        "unsafe_action":
                            int(
                                regret_value
                                > REGRET_THRESHOLD
                            ),
                    }
                )

            context_action_separations.append(
                max_action_distance_difference(
                    distances
                )
            )

    nonzero_action_separation = sum(
        int(
            value
            > FLOAT_TOLERANCE
        )
        for value in context_action_separations
    )

    total_contexts = len(
        context_action_separations
    )

    mean_action_separation = statistics.mean(
        context_action_separations
    )

    max_action_separation = max(
        context_action_separations
    )

    safe_rows = [
        row
        for row in action_rows
        if int(
            row[
                "unsafe_action"
            ]
        )
        == 0
    ]

    unsafe_rows = [
        row
        for row in action_rows
        if int(
            row[
                "unsafe_action"
            ]
        )
        == 1
    ]

    diagnostic_fields = [
        "context_support_distance",
        "action_support_distance",
        "action_support_minus_context",
        "predicted_action_loss",
        "predicted_relative_loss",
    ]

    diagnostic_summary = []

    for field in diagnostic_fields:

        safe_values = [
            float(
                row[
                    field
                ]
            )
            for row in safe_rows
        ]

        unsafe_values = [
            float(
                row[
                    field
                ]
            )
            for row in unsafe_rows
        ]

        diagnostic_summary.append(
            {
                "model":
                    f"diagnostic_{field}",

                "features":
                    field,

                "feature_count":
                    1,

                "rows":
                    len(
                        action_rows
                    ),

                "unsafe_rows":
                    len(
                        unsafe_rows
                    ),

                "safe_rows":
                    len(
                        safe_rows
                    ),

                "balanced_accuracy":
                    "",

                "unsafe_recall":
                    "",

                "unsafe_precision":
                    "",

                "safe_specificity":
                    "",

                "roc_auc":
                    "",

                "mean_fold_balanced_accuracy":
                    "",

                "mean_fold_roc_auc":
                    "",

                "safe_mean":
                    statistics.mean(
                        safe_values
                    ),

                "unsafe_mean":
                    statistics.mean(
                        unsafe_values
                    ),

                "standardized_difference_unsafe_minus_safe":
                    standardized_difference(
                        safe_values,
                        unsafe_values,
                    ),
            }
        )

    model_summaries = []
    fold_rows = []
    coefficient_rows = []

    for (
        model_name,
        feature_names,
    ) in MODEL_SPECS.items():

        (
            summary,
            folds,
            coefficients,
        ) = evaluate_model(
            action_rows,
            model_name,
            feature_names,
        )

        model_summaries.append(
            summary
        )

        fold_rows.extend(
            folds
        )

        coefficient_rows.extend(
            coefficients
        )

    model_summaries.sort(
        key=lambda row: (
            float(
                row[
                    "balanced_accuracy"
                ]
            ),
            float(
                row[
                    "roc_auc"
                ]
            ),
        ),
        reverse=True,
    )

    coefficient_rows_summary = (
        coefficient_summary(
            coefficient_rows
        )
    )

    output_rows = (
        model_summaries
        + diagnostic_summary
    )

    save_csv(
        OUTPUT_PATH,
        output_rows,
    )

    save_csv(
        FOLD_OUTPUT_PATH,
        fold_rows,
    )

    save_csv(
        ACTION_OUTPUT_PATH,
        action_rows,
    )

    save_csv(
        COEFFICIENT_OUTPUT_PATH,
        coefficient_rows_summary,
    )

    print()

    print(
        "ACTION-CONDITIONAL GEOMETRY"
    )

    print(
        f"contexts="
        f"{total_contexts}"
    )

    print(
        f"contexts with nonzero action-distance separation="
        f"{nonzero_action_separation}/"
        f"{total_contexts} "
        f"("
        f"{nonzero_action_separation / total_contexts:.3%}"
        f")"
    )

    print(
        f"mean max pairwise action-distance difference="
        f"{mean_action_separation:.6f}"
    )

    print(
        f"maximum pairwise action-distance difference="
        f"{max_action_separation:.6f}"
    )

    print()

    print(
        "ACTION CONSEQUENCE POPULATION"
    )

    print(
        f"action-context pairs="
        f"{len(action_rows)}"
    )

    print(
        f"safe pairs="
        f"{len(safe_rows)} "
        f"("
        f"{len(safe_rows) / len(action_rows):.3%}"
        f")"
    )

    print(
        f"unsafe pairs="
        f"{len(unsafe_rows)} "
        f"("
        f"{len(unsafe_rows) / len(action_rows):.3%}"
        f")"
    )

    print()

    print(
        "UNIVARIATE CONSEQUENCE SEPARATION"
    )

    for row in diagnostic_summary:

        print(
            f"{row['features']:<34} "
            f"safe="
            f"{row['safe_mean']:.6f} "
            f"unsafe="
            f"{row['unsafe_mean']:.6f} "
            f"effect="
            f"{row['standardized_difference_unsafe_minus_safe']:+.3f}"
        )

    print()

    print(
        "LEAVE-ONE-SEED-OUT UNSAFE-ACTION CLASSIFICATION"
    )

    for row in model_summaries:

        print(
            f"{row['model']:<30} "
            f"balanced_acc="
            f"{row['balanced_accuracy']:.3%} "
            f"unsafe_recall="
            f"{row['unsafe_recall']:.3%} "
            f"unsafe_precision="
            f"{row['unsafe_precision']:.3%} "
            f"safe_specificity="
            f"{row['safe_specificity']:.3%} "
            f"AUC="
            f"{row['roc_auc']:.3f} "
            f"mean_fold_bal_acc="
            f"{row['mean_fold_balanced_accuracy']:.3%} "
            f"mean_fold_AUC="
            f"{row['mean_fold_roc_auc']:.3f}"
        )

    print()

    print(
        "COEFFICIENT STABILITY"
    )

    for model_name in MODEL_SPECS:

        print()

        print(
            model_name
        )

        matching = [
            row
            for row in coefficient_rows_summary
            if row[
                "model"
            ]
            == model_name
        ]

        for row in matching:

            print(
                f"  "
                f"{row['feature']:<34} "
                f"mean_coef="
                f"{row['mean_coefficient']:+.3f} "
                f"abs_coef="
                f"{row['mean_absolute_coefficient']:.3f} "
                f"sign_stability="
                f"{row['dominant_sign_fraction']:.3%}"
            )

    print()

    best = model_summaries[
        0
    ]

    print(
        "BEST RETROSPECTIVE MODEL"
    )

    print(
        f"name="
        f"{best['model']}"
    )

    print(
        f"balanced_accuracy="
        f"{best['balanced_accuracy']:.3%}"
    )

    print(
        f"roc_auc="
        f"{best['roc_auc']:.3f}"
    )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 092 evaluates representation geometry and "
        "retrospective consequence association only. "
        "No new controller threshold or prospective policy is defined."
    )

    print(
        "=" * 210
    )

    print(
        f"Summary saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Fold results saved to: "
        f"{FOLD_OUTPUT_PATH}"
    )

    print(
        f"Action-context results saved to: "
        f"{ACTION_OUTPUT_PATH}"
    )

    print(
        f"Coefficient stability saved to: "
        f"{COEFFICIENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()