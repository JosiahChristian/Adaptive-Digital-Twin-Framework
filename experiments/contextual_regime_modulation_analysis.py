import csv
import math
import statistics
from pathlib import Path

import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


INPUT_PATH = Path(
    "results/"
    "cross_block_constituent_stability_analysis_events.csv"
)

SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "contextual_regime_modulation_analysis.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "contextual_regime_modulation_analysis_events.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "contextual_regime_modulation_analysis_coefficients.csv"
)


BLOCKS = [
    "block_071_090",
    "block_091_110",
]

BASE_FEATURE = "local_error_std"

CONTEXT_CANDIDATES = [
    "context_support_distance",
    "predicted_baseline_action_loss",
    "baseline_action_loss_error",
]

FLOAT_TOLERANCE = 1e-12
RANDOM_STATE = 42


def read_events():
    with INPUT_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        rows = list(
            csv.DictReader(
                file
            )
        )

    output = []

    for row in rows:
        copy = dict(
            row
        )

        copy[
            "harmful_target"
        ] = int(
            copy[
                "class"
            ]
            == "harmful"
        )

        for field in [
            BASE_FEATURE,
            *CONTEXT_CANDIDATES,
        ]:
            value = copy.get(
                field,
                "",
            )

            try:
                copy[
                    field
                ] = float(
                    value
                )

            except (
                TypeError,
                ValueError,
            ):
                copy[
                    field
                ] = float(
                    "nan"
                )

        output.append(
            copy
        )

    return output


def finite_rows(
    rows,
    fields,
):
    return [
        row
        for row in rows
        if all(
            math.isfinite(
                float(
                    row[
                        field
                    ]
                )
            )
            for field in fields
        )
    ]


def safe_auc(
    y_true,
    probabilities,
):
    if len(
        np.unique(
            y_true
        )
    ) < 2:
        return float(
            "nan"
        )

    return float(
        roc_auc_score(
            y_true,
            probabilities,
        )
    )


def make_model():
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
                    C=1.0,
                    solver="liblinear",
                    random_state=RANDOM_STATE,
                    max_iter=5000,
                ),
            ),
        ]
    )


def build_matrix(
    rows,
    fields,
):
    return np.asarray(
        [
            [
                float(
                    row[
                        field
                    ]
                )
                for field in fields
            ]
            for row in rows
        ],
        dtype=float,
    )


def build_labels(
    rows,
):
    return np.asarray(
        [
            int(
                row[
                    "harmful_target"
                ]
            )
            for row in rows
        ],
        dtype=int,
    )


def add_interaction(
    rows,
    context_field,
):
    output = []

    interaction_field = (
        f"{BASE_FEATURE}_x_{context_field}"
    )

    for row in rows:
        copy = dict(
            row
        )

        copy[
            interaction_field
        ] = (
            float(
                row[
                    BASE_FEATURE
                ]
            )
            * float(
                row[
                    context_field
                ]
            )
        )

        output.append(
            copy
        )

    return (
        output,
        interaction_field,
    )


def evaluate_model(
    training_rows,
    test_rows,
    fields,
):
    training_rows = finite_rows(
        training_rows,
        fields,
    )

    test_rows = finite_rows(
        test_rows,
        fields,
    )

    x_train = build_matrix(
        training_rows,
        fields,
    )

    y_train = build_labels(
        training_rows
    )

    x_test = build_matrix(
        test_rows,
        fields,
    )

    y_test = build_labels(
        test_rows
    )

    if len(
        np.unique(
            y_train
        )
    ) < 2:
        return None

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

    auc = safe_auc(
        y_test,
        probabilities,
    )

    classifier = model.named_steps[
        "classifier"
    ]

    coefficients = {
        field:
            float(
                coefficient
            )
        for field, coefficient in zip(
            fields,
            classifier.coef_[
                0
            ],
        )
    }

    return {
        "auc":
            auc,

        "test_rows":
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

        "coefficients":
            coefficients,

        "probabilities":
            probabilities,

        "test_data":
            test_rows,
    }


def reciprocal_block_evaluation(
    rows,
    model_name,
    fields,
):
    fold_rows = []
    coefficient_rows = []
    prediction_rows = []

    for held_out_block in BLOCKS:
        training_rows = [
            row
            for row in rows
            if row[
                "block"
            ]
            != held_out_block
        ]

        test_rows = [
            row
            for row in rows
            if row[
                "block"
            ]
            == held_out_block
        ]

        result = evaluate_model(
            training_rows,
            test_rows,
            fields,
        )

        if result is None:
            continue

        fold_rows.append(
            {
                "model":
                    model_name,

                "features":
                    "|".join(
                        fields
                    ),

                "held_out_block":
                    held_out_block,

                "roc_auc":
                    result[
                        "auc"
                    ],

                "test_rows":
                    result[
                        "test_rows"
                    ],

                "test_harmful":
                    result[
                        "test_harmful"
                    ],

                "test_beneficial":
                    result[
                        "test_beneficial"
                    ],
            }
        )

        for field, coefficient in result[
            "coefficients"
        ].items():
            coefficient_rows.append(
                {
                    "model":
                        model_name,

                    "held_out_block":
                        held_out_block,

                    "feature":
                        field,

                    "coefficient":
                        coefficient,
                }
            )

        for row, probability in zip(
            result[
                "test_data"
            ],
            result[
                "probabilities"
            ],
        ):
            prediction_rows.append(
                {
                    "model":
                        model_name,

                    "held_out_block":
                        held_out_block,

                    "generation_seed":
                        int(
                            float(
                                row[
                                    "generation_seed"
                                ]
                            )
                        ),

                    "test_index":
                        int(
                            float(
                                row[
                                    "test_index"
                                ]
                            )
                        ),

                    "true_class":
                        row[
                            "class"
                        ],

                    "harmful_target":
                        int(
                            row[
                                "harmful_target"
                            ]
                        ),

                    "predicted_probability":
                        float(
                            probability
                        ),
                }
            )

    return (
        fold_rows,
        coefficient_rows,
        prediction_rows,
    )


def summarize_models(
    fold_rows,
):
    output = []

    model_names = sorted(
        {
            row[
                "model"
            ]
            for row in fold_rows
        }
    )

    for model_name in model_names:
        rows = [
            row
            for row in fold_rows
            if row[
                "model"
            ]
            == model_name
        ]

        aucs = [
            float(
                row[
                    "roc_auc"
                ]
            )
            for row in rows
            if math.isfinite(
                float(
                    row[
                        "roc_auc"
                    ]
                )
            )
        ]

        output.append(
            {
                "model":
                    model_name,

                "folds":
                    len(
                        rows
                    ),

                "mean_auc":
                    statistics.mean(
                        aucs
                    ),

                "min_auc":
                    min(
                        aucs
                    ),

                "max_auc":
                    max(
                        aucs
                    ),
            }
        )

    output.sort(
        key=lambda row:
            float(
                row[
                    "mean_auc"
                ]
            ),
        reverse=True,
    )

    return output


def coefficient_stability(
    coefficient_rows,
):
    output = []

    keys = sorted(
        {
            (
                row[
                    "model"
                ],
                row[
                    "feature"
                ],
            )
            for row in coefficient_rows
        }
    )

    for model_name, feature in keys:
        values = [
            float(
                row[
                    "coefficient"
                ]
            )
            for row in coefficient_rows
            if (
                row[
                    "model"
                ]
                == model_name
                and row[
                    "feature"
                ]
                == feature
            )
        ]

        positive_fraction = statistics.mean(
            int(
                value
                > 0
            )
            for value in values
        )

        negative_fraction = statistics.mean(
            int(
                value
                < 0
            )
            for value in values
        )

        output.append(
            {
                "model":
                    model_name,

                "feature":
                    feature,

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

                "sign_stability":
                    max(
                        positive_fraction,
                        negative_fraction,
                    ),
            }
        )

    return output


def save_csv(
    path,
    rows,
):
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


def main():
    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "CONTEXTUAL REGIME MODULATION ANALYSIS"
    )

    print(
        "=" * 210
    )

    print(
        f"input="
        f"{INPUT_PATH}"
    )

    print(
        f"base signal="
        f"{BASE_FEATURE}"
    )

    print(
        f"context candidates="
        f"{CONTEXT_CANDIDATES}"
    )

    print()

    rows = read_events()

    all_fold_rows = []
    all_coefficient_rows = []
    all_prediction_rows = []

    baseline_name = (
        "error_std_only"
    )

    (
        fold_rows,
        coefficient_rows,
        prediction_rows,
    ) = reciprocal_block_evaluation(
        rows,
        baseline_name,
        [
            BASE_FEATURE,
        ],
    )

    all_fold_rows.extend(
        fold_rows
    )

    all_coefficient_rows.extend(
        coefficient_rows
    )

    all_prediction_rows.extend(
        prediction_rows
    )

    for context_field in CONTEXT_CANDIDATES:
        (
            enriched_rows,
            interaction_field,
        ) = add_interaction(
            rows,
            context_field,
        )

        model_name = (
            f"error_std_plus_"
            f"{context_field}"
        )

        (
            fold_rows,
            coefficient_rows,
            prediction_rows,
        ) = reciprocal_block_evaluation(
            enriched_rows,
            model_name,
            [
                BASE_FEATURE,
                context_field,
            ],
        )

        all_fold_rows.extend(
            fold_rows
        )

        all_coefficient_rows.extend(
            coefficient_rows
        )

        all_prediction_rows.extend(
            prediction_rows
        )

        interaction_model_name = (
            f"error_std_x_"
            f"{context_field}"
        )

        (
            fold_rows,
            coefficient_rows,
            prediction_rows,
        ) = reciprocal_block_evaluation(
            enriched_rows,
            interaction_model_name,
            [
                BASE_FEATURE,
                context_field,
                interaction_field,
            ],
        )

        all_fold_rows.extend(
            fold_rows
        )

        all_coefficient_rows.extend(
            coefficient_rows
        )

        all_prediction_rows.extend(
            prediction_rows
        )

    summary_rows = summarize_models(
        all_fold_rows
    )

    coefficient_summary_rows = (
        coefficient_stability(
            all_coefficient_rows
        )
    )

    print(
        "RECIPROCAL BLOCK-HELD-OUT PERFORMANCE"
    )

    for row in summary_rows:
        print(
            f"{row['model']:<58} "
            f"mean_AUC="
            f"{row['mean_auc']:.3f} "
            f"min_AUC="
            f"{row['min_auc']:.3f} "
            f"max_AUC="
            f"{row['max_auc']:.3f}"
        )

    baseline = next(
        row
        for row in summary_rows
        if row[
            "model"
        ]
        == baseline_name
    )

    print()

    print(
        "VALUE-ADD VS ERROR-STD BASELINE"
    )

    for row in summary_rows:
        if row[
            "model"
        ] == baseline_name:
            continue

        print(
            f"{row['model']:<58} "
            f"dMeanAUC="
            f"{row['mean_auc'] - baseline['mean_auc']:+.3f} "
            f"dMinAUC="
            f"{row['min_auc'] - baseline['min_auc']:+.3f}"
        )

    print()

    print(
        "COEFFICIENT STABILITY"
    )

    for row in coefficient_summary_rows:
        print(
            f"{row['model']:<46} "
            f"{row['feature']:<42} "
            f"mean_coef="
            f"{row['mean_coefficient']:+.3f} "
            f"abs_coef="
            f"{row['mean_absolute_coefficient']:.3f} "
            f"sign_stability="
            f"{row['sign_stability']:.3%}"
        )

    best = summary_rows[
        0
    ]

    print()

    print(
        "BEST CONTEXTUAL MODEL"
    )

    print(
        f"name="
        f"{best['model']}"
    )

    print(
        f"mean_AUC="
        f"{best['mean_auc']:.3f}"
    )

    print(
        f"min_AUC="
        f"{best['min_auc']:.3f}"
    )

    print(
        f"dMeanAUC_vs_error_std="
        f"{best['mean_auc'] - baseline['mean_auc']:+.3f}"
    )

    print(
        f"dMinAUC_vs_error_std="
        f"{best['min_auc'] - baseline['min_auc']:+.3f}"
    )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 109 tests whether a small predefined "
        "context set improves the block-generalizable meaning "
        "of local_error_std."
    )

    print(
        "No new seed, threshold, or controller intervention "
        "is introduced."
    )

    print(
        "baseline_action_loss_error is a realized outcome field "
        "and therefore serves only as a retrospective explanatory "
        "diagnostic; it cannot become a pre-action controller feature."
    )

    print(
        "Any apparent value from that outcome field must remain "
        "separate from deployable pre-action context."
    )

    print(
        "=" * 210
    )

    save_csv(
        SUMMARY_OUTPUT_PATH,
        summary_rows
        + all_fold_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        all_prediction_rows,
    )

    save_csv(
        COEFFICIENT_OUTPUT_PATH,
        coefficient_summary_rows,
    )

    print(
        f"Summary saved to: "
        f"{SUMMARY_OUTPUT_PATH}"
    )

    print(
        f"Predictions saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )

    print(
        f"Coefficient stability saved to: "
        f"{COEFFICIENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()