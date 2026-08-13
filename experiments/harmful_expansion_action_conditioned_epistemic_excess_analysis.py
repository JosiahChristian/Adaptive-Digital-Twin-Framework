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


EVENT_INPUT_PATH = Path(
    "results/"
    "cross_seed_harmful_expansion_feature_decomposition_events.csv"
)

OUTPUT_PATH = Path(
    "results/"
    "harmful_expansion_action_conditioned_epistemic_excess_analysis.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "harmful_expansion_action_conditioned_epistemic_excess_analysis_events.csv"
)

FOLD_OUTPUT_PATH = Path(
    "results/"
    "harmful_expansion_action_conditioned_epistemic_excess_analysis_folds.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "harmful_expansion_action_conditioned_epistemic_excess_analysis_coefficients.csv"
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

CLASS_THRESHOLD = 0.50

FLOAT_TOLERANCE = 1e-12
RANDOM_STATE = 42


MODEL_SPECS = {
    "context_support_only": [
        "context_support_distance",
    ],

    "action_support_only": [
        "action_support_distance",
    ],

    "epistemic_excess_only": [
        "epistemic_excess",
    ],

    "predicted_loss_only": [
        "predicted_action_loss",
    ],

    "context_plus_action": [
        "context_support_distance",
        "action_support_distance",
    ],

    "context_plus_excess": [
        "context_support_distance",
        "epistemic_excess",
    ],

    "loss_plus_excess": [
        "predicted_action_loss",
        "epistemic_excess",
    ],

    "context_loss_excess": [
        "context_support_distance",
        "predicted_action_loss",
        "epistemic_excess",
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


def read_expansion_events() -> list[dict]:

    with EVENT_INPUT_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        rows = list(
            csv.DictReader(
                file
            )
        )

    return [
        row
        for row in rows
        if row.get(
            "outcome",
            "",
        )
        in (
            "beneficial",
            "harmful",
        )
    ]


def expansion_action_from_event(
    row: dict,
) -> int:

    candidate_fields = [
        "expanded_action",
        "support_action",
        "baseline_action",
        "selected_action",
    ]

    for field in candidate_fields:

        if (
            field in row
            and row[
                field
            ]
            not in (
                "",
                None,
            )
        ):

            return int(
                float(
                    row[
                        field
                    ]
                )
            )

    raise KeyError(
        "Could not locate expanded action in event row. "
        "Expected one of: "
        "expanded_action, support_action, baseline_action, selected_action."
    )


def event_test_index(
    row: dict,
) -> int:

    candidate_fields = [
        "test_index",
        "context_index",
        "index",
    ]

    for field in candidate_fields:

        if (
            field in row
            and row[
                field
            ]
            not in (
                "",
                None,
            )
        ):

            return int(
                float(
                    row[
                        field
                    ]
                )
            )

    raise KeyError(
        "Could not locate test index in event row."
    )


def event_seed(
    row: dict,
) -> int:

    candidate_fields = [
        "generation_seed",
        "seed",
    ]

    for field in candidate_fields:

        if (
            field in row
            and row[
                field
            ]
            not in (
                "",
                None,
            )
        ):

            return int(
                float(
                    row[
                        field
                    ]
                )
            )

    raise KeyError(
        "Could not locate generation seed in event row."
    )


def reconstruct_seed_geometry(
    generation_seed: int,
) -> dict:

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

    return {
        "test_rows":
            test_rows,

        "test_losses":
            test_losses,

        "test_risks":
            test_risks,

        "context_support":
            context_support,

        "action_support":
            action_support,
    }


def standardized_difference(
    beneficial_values: list[float],
    harmful_values: list[float],
) -> float:

    if (
        len(
            beneficial_values
        )
        < 2
        or len(
            harmful_values
        )
        < 2
    ):

        return 0.0

    beneficial_variance = statistics.variance(
        beneficial_values
    )

    harmful_variance = statistics.variance(
        harmful_values
    )

    pooled_variance = (
        (
            (
                len(
                    beneficial_values
                )
                - 1
            )
            * beneficial_variance
        )
        +
        (
            (
                len(
                    harmful_values
                )
                - 1
            )
            * harmful_variance
        )
    ) / (
        len(
            beneficial_values
        )
        + len(
            harmful_values
        )
        - 2
    )

    if (
        pooled_variance
        <= FLOAT_TOLERANCE
    ):

        return 0.0

    return (
        statistics.mean(
            harmful_values
        )
        - statistics.mean(
            beneficial_values
        )
    ) / (
        pooled_variance
        ** 0.5
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
                    "outcome"
                ]
                == "harmful"
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

        if not test_rows:
            continue

        x_train = build_matrix(
            train_rows,
            feature_names,
        )

        y_train = build_labels(
            train_rows
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

        x_test = build_matrix(
            test_rows,
            feature_names,
        )

        y_test = build_labels(
            test_rows
        )

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

        fold_rows.append(
            {
                "model":
                    model_name,

                "held_out_seed":
                    held_out_seed,

                "test_events":
                    len(
                        test_rows
                    ),

                "test_harmful":
                    int(
                        np.sum(
                            y_test
                            == 1
                        )
                    ),

                "test_beneficial":
                    int(
                        np.sum(
                            y_test
                            == 0
                        )
                    ),

                "balanced_accuracy":
                    balanced_accuracy,

                "harmful_recall":
                    float(
                        recall_score(
                            y_test,
                            predictions,
                            pos_label=1,
                            zero_division=0,
                        )
                    ),

                "harmful_precision":
                    float(
                        precision_score(
                            y_test,
                            predictions,
                            pos_label=1,
                            zero_division=0,
                        )
                    ),

                "beneficial_specificity":
                    specificity_score(
                        y_test,
                        predictions,
                    ),

                "roc_auc":
                    safe_auc(
                        y_test,
                        probabilities,
                    ),
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

        "events":
            len(
                y_true
            ),

        "harmful_events":
            int(
                np.sum(
                    y_true
                    == 1
                )
            ),

        "beneficial_events":
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

        "harmful_recall":
            float(
                recall_score(
                    y_true,
                    y_pred,
                    pos_label=1,
                    zero_division=0,
                )
            ),

        "harmful_precision":
            float(
                precision_score(
                    y_true,
                    y_pred,
                    pos_label=1,
                    zero_division=0,
                )
            ),

        "beneficial_specificity":
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


def summarize_coefficients(
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
                    value
                    > 0
                )
                for value in values
            ]
        )

        negative_fraction = statistics.mean(
            [
                float(
                    value
                    < 0
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

    return output


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

    source_events = read_expansion_events()

    source_events = [
        row
        for row in source_events
        if event_seed(
            row
        )
        in ANALYSIS_SEEDS
    ]

    reconstructed = {}

    enriched_events = []

    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "HARMFUL-EXPANSION ACTION-CONDITIONED "
        "EPISTEMIC-EXCESS ANALYSIS"
    )

    print(
        "=" * 210
    )

    print(
        f"input="
        f"{EVENT_INPUT_PATH}"
    )

    print(
        f"analysis seeds="
        f"{ANALYSIS_SEEDS}"
    )

    print(
        f"source beneficial/harmful events="
        f"{len(source_events)}"
    )

    print()

    for generation_seed in ANALYSIS_SEEDS:

        print(
            f"reconstructing seed "
            f"{generation_seed}..."
        )

        reconstructed[
            generation_seed
        ] = reconstruct_seed_geometry(
            generation_seed
        )

    for event in source_events:

        generation_seed = event_seed(
            event
        )

        test_index = event_test_index(
            event
        )

        action = expansion_action_from_event(
            event
        )

        geometry = reconstructed[
            generation_seed
        ]

        test_rows = geometry[
            "test_rows"
        ]

        test_losses = geometry[
            "test_losses"
        ]

        test_risks = geometry[
            "test_risks"
        ]

        if (
            test_index < 0
            or test_index
            >= len(
                test_rows
            )
        ):

            raise IndexError(
                f"Event test_index {test_index} "
                f"is outside reconstructed seed "
                f"{generation_seed} test rows."
            )

        row = test_rows[
            test_index
        ]

        predicted_losses = test_losses[
            test_index
        ]

        predicted_risk = test_risks[
            test_index
        ]

        context_distance = (
            context_support_distance(
                geometry[
                    "context_support"
                ],
                row,
                predicted_risk,
            )
        )

        action_distance = (
            action_support_distance(
                geometry[
                    "action_support"
                ],
                row,
                predicted_risk,
                predicted_losses,
                action,
            )
        )

        predicted_action_loss = float(
            predicted_losses[
                action
            ]
        )

        minimum_predicted_loss = min(
            float(
                predicted_losses[
                    other
                ]
            )
            for other in ACTIONS
        )

        copy = dict(
            event
        )

        copy[
            "generation_seed"
        ] = generation_seed

        copy[
            "test_index"
        ] = test_index

        copy[
            "expanded_action_reconstructed"
        ] = action

        copy[
            "context_support_distance"
        ] = context_distance

        copy[
            "action_support_distance"
        ] = action_distance

        copy[
            "epistemic_excess"
        ] = (
            action_distance
            - context_distance
        )

        copy[
            "predicted_action_loss"
        ] = predicted_action_loss

        copy[
            "predicted_relative_loss"
        ] = (
            predicted_action_loss
            - minimum_predicted_loss
        )

        enriched_events.append(
            copy
        )

    beneficial_rows = [
        row
        for row in enriched_events
        if row[
            "outcome"
        ]
        == "beneficial"
    ]

    harmful_rows = [
        row
        for row in enriched_events
        if row[
            "outcome"
        ]
        == "harmful"
    ]

    diagnostic_fields = [
        "context_support_distance",
        "action_support_distance",
        "epistemic_excess",
        "predicted_action_loss",
        "predicted_relative_loss",
    ]

    diagnostic_rows = []

    for field in diagnostic_fields:

        beneficial_values = [
            float(
                row[
                    field
                ]
            )
            for row in beneficial_rows
        ]

        harmful_values = [
            float(
                row[
                    field
                ]
            )
            for row in harmful_rows
        ]

        diagnostic_rows.append(
            {
                "record_type":
                    "diagnostic",

                "metric":
                    field,

                "beneficial_count":
                    len(
                        beneficial_values
                    ),

                "harmful_count":
                    len(
                        harmful_values
                    ),

                "beneficial_mean":
                    statistics.mean(
                        beneficial_values
                    ),

                "harmful_mean":
                    statistics.mean(
                        harmful_values
                    ),

                "difference_harmful_minus_beneficial":
                    (
                        statistics.mean(
                            harmful_values
                        )
                        - statistics.mean(
                            beneficial_values
                        )
                    ),

                "standardized_difference":
                    standardized_difference(
                        beneficial_values,
                        harmful_values,
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
            enriched_events,
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

    coefficient_summary = (
        summarize_coefficients(
            coefficient_rows
        )
    )

    output_rows = []

    for row in model_summaries:

        copy = {
            "record_type":
                "model_summary"
        }

        copy.update(
            row
        )

        output_rows.append(
            copy
        )

    output_rows.extend(
        diagnostic_rows
    )

    save_csv(
        OUTPUT_PATH,
        output_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        enriched_events,
    )

    save_csv(
        FOLD_OUTPUT_PATH,
        fold_rows,
    )

    save_csv(
        COEFFICIENT_OUTPUT_PATH,
        coefficient_summary,
    )

    print()

    print(
        "EVENT POPULATION"
    )

    print(
        f"beneficial="
        f"{len(beneficial_rows)}"
    )

    print(
        f"harmful="
        f"{len(harmful_rows)}"
    )

    print()

    print(
        "UNIVARIATE HARMFUL-EXPANSION SEPARATION"
    )

    for row in diagnostic_rows:

        print(
            f"{row['metric']:<32} "
            f"beneficial="
            f"{row['beneficial_mean']:.6f} "
            f"harmful="
            f"{row['harmful_mean']:.6f} "
            f"delta="
            f"{row['difference_harmful_minus_beneficial']:+.6f} "
            f"effect="
            f"{row['standardized_difference']:+.3f}"
        )

    print()

    print(
        "LEAVE-ONE-SEED-OUT HARMFUL-EXPANSION CLASSIFICATION"
    )

    for row in model_summaries:

        print(
            f"{row['model']:<28} "
            f"balanced_acc="
            f"{row['balanced_accuracy']:.3%} "
            f"harmful_recall="
            f"{row['harmful_recall']:.3%} "
            f"harmful_precision="
            f"{row['harmful_precision']:.3%} "
            f"beneficial_specificity="
            f"{row['beneficial_specificity']:.3%} "
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
            for row in coefficient_summary
            if row[
                "model"
            ]
            == model_name
        ]

        matching.sort(
            key=lambda row: (
                float(
                    row[
                        "dominant_sign_fraction"
                    ]
                ),
                float(
                    row[
                        "mean_absolute_coefficient"
                    ]
                ),
            ),
            reverse=True,
        )

        for row in matching:

            print(
                f"  "
                f"{row['feature']:<32} "
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
        "BEST RETROSPECTIVE EVENT MODEL"
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
        f"harmful_recall="
        f"{best['harmful_recall']:.3%}"
    )

    print(
        f"beneficial_specificity="
        f"{best['beneficial_specificity']:.3%}"
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
        "Experiment 093 is retrospective. "
        "It tests whether action-conditioned epistemic excess "
        "is associated specifically with harmful responsive expansion. "
        "No controller threshold or prospective guard is defined."
    )

    print(
        "=" * 210
    )

    print(
        f"Summary saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Enriched event results saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )

    print(
        f"Fold results saved to: "
        f"{FOLD_OUTPUT_PATH}"
    )

    print(
        f"Coefficient stability saved to: "
        f"{COEFFICIENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()