import csv
import math
import statistics
from pathlib import Path

import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


SUPPORT_EVENT_PATH = Path(
    "results/"
    "frozen_pre_action_calibration_proxy_support_expansion_transfer_events.csv"
)

SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "pre_action_regime_identification_analysis.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "pre_action_regime_identification_analysis_events.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "pre_action_regime_identification_analysis_coefficients.csv"
)


BLOCK_A = "block_071_090"
BLOCK_B = "block_091_110"

SEVERE_PROXY_MODEL = "severe_proxy_only"

RANDOM_STATE = 42

FLOAT_TOLERANCE = 1e-12


# Strictly pre-action candidate variables.
# No realized loss, regret, harmful label, or outcome-derived variable
# is allowed here.
REGIME_FEATURES = [
    "local_error_std",
    "severe_underestimation_probability",
]


# The regime model will also use support-event fields if available.
OPTIONAL_REGIME_FEATURES = [
    "context_support_distance",
    "predicted_baseline_action_loss",
]


def read_events():
    with SUPPORT_EVENT_PATH.open(
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

    seen = set()

    for row in rows:
        if row.get(
            "model",
            "",
        ) != SEVERE_PROXY_MODEL:
            continue

        key = (
            int(
                float(
                    row[
                        "generation_seed"
                    ]
                )
            ),
            int(
                float(
                    row[
                        "test_index"
                    ]
                )
            ),
            int(
                float(
                    row[
                        "support_baseline_action"
                    ]
                )
            ),
        )

        if key in seen:
            continue

        seen.add(
            key
        )

        copy = dict(
            row
        )

        copy[
            "generation_seed"
        ] = key[
            0
        ]

        copy[
            "test_index"
        ] = key[
            1
        ]

        copy[
            "support_baseline_action"
        ] = key[
            2
        ]

        copy[
            "harmful_target"
        ] = int(
            copy[
                "harmful_target"
            ]
        )

        copy[
            "regime_target"
        ] = int(
            copy[
                "held_out_block"
            ]
            == BLOCK_B
        )

        for field in [
            "local_error_std",
            "severe_underestimation_probability",
            *OPTIONAL_REGIME_FEATURES,
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
    features,
):
    return [
        row
        for row in rows
        if all(
            math.isfinite(
                float(
                    row[
                        feature
                    ]
                )
            )
            for feature in features
        )
    ]


def build_matrix(
    rows,
    features,
):
    return np.asarray(
        [
            [
                float(
                    row[
                        feature
                    ]
                )
                for feature in features
            ]
            for row in rows
        ],
        dtype=float,
    )


def build_labels(
    rows,
    field,
):
    return np.asarray(
        [
            int(
                row[
                    field
                ]
            )
            for row in rows
        ],
        dtype=int,
    )


def safe_auc(
    y_true,
    scores,
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
            scores,
        )
    )


def make_classifier():
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


def available_regime_features(
    rows,
):
    features = list(
        REGIME_FEATURES
    )

    for field in OPTIONAL_REGIME_FEATURES:
        if all(
            math.isfinite(
                float(
                    row[
                        field
                    ]
                )
            )
            for row in rows
        ):
            features.append(
                field
            )

    return features


def univariate_regime_geometry(
    rows,
    features,
):
    output = []

    for feature in features:
        a_values = [
            float(
                row[
                    feature
                ]
            )
            for row in rows
            if row[
                "held_out_block"
            ]
            == BLOCK_A
        ]

        b_values = [
            float(
                row[
                    feature
                ]
            )
            for row in rows
            if row[
                "held_out_block"
            ]
            == BLOCK_B
        ]

        pooled = (
            a_values
            + b_values
        )

        labels = np.asarray(
            [
                0
            ]
            * len(
                a_values
            )
            + [
                1
            ]
            * len(
                b_values
            ),
            dtype=int,
        )

        scores = np.asarray(
            pooled,
            dtype=float,
        )

        auc = safe_auc(
            labels,
            scores,
        )

        output.append(
            {
                "record_type":
                    "univariate_regime_geometry",

                "feature":
                    feature,

                "block_a_mean":
                    statistics.mean(
                        a_values
                    ),

                "block_b_mean":
                    statistics.mean(
                        b_values
                    ),

                "difference_b_minus_a":
                    (
                        statistics.mean(
                            b_values
                        )
                        - statistics.mean(
                            a_values
                        )
                    ),

                "regime_auc_b_high":
                    auc,

                "regime_auc_best_orientation":
                    max(
                        auc,
                        1.0 - auc,
                    ),
            }
        )

    return output


def leave_one_seed_out_regime_model(
    rows,
    features,
):
    fold_rows = []
    event_rows = []
    coefficient_rows = []

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

    usable_rows = finite_rows(
        rows,
        features,
    )

    for held_out_seed in seeds:
        training_rows = [
            row
            for row in usable_rows
            if int(
                row[
                    "generation_seed"
                ]
            )
            != held_out_seed
        ]

        test_rows = [
            row
            for row in usable_rows
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
            training_rows,
            features,
        )

        y_train = build_labels(
            training_rows,
            "regime_target",
        )

        x_test = build_matrix(
            test_rows,
            features,
        )

        y_test = build_labels(
            test_rows,
            "regime_target",
        )

        if len(
            np.unique(
                y_train
            )
        ) < 2:
            continue

        model = make_classifier()

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

        fold_auc = safe_auc(
            y_test,
            probabilities,
        )

        fold_rows.append(
            {
                "record_type":
                    "regime_seed_fold",

                "held_out_seed":
                    held_out_seed,

                "test_rows":
                    len(
                        test_rows
                    ),

                "test_regime":
                    int(
                        y_test[
                            0
                        ]
                    ),

                "auc":
                    fold_auc,
            }
        )

        classifier = model.named_steps[
            "classifier"
        ]

        for feature, coefficient in zip(
            features,
            classifier.coef_[
                0
            ],
        ):
            coefficient_rows.append(
                {
                    "record_type":
                        "regime_coefficient",

                    "held_out_seed":
                        held_out_seed,

                    "feature":
                        feature,

                    "coefficient":
                        float(
                            coefficient
                        ),
                }
            )

        for row, probability in zip(
            test_rows,
            probabilities,
        ):
            event_rows.append(
                {
                    "generation_seed":
                        int(
                            row[
                                "generation_seed"
                            ]
                        ),

                    "test_index":
                        int(
                            row[
                                "test_index"
                            ]
                        ),

                    "support_baseline_action":
                        int(
                            row[
                                "support_baseline_action"
                            ]
                        ),

                    "held_out_block":
                        row[
                            "held_out_block"
                        ],

                    "regime_target":
                        int(
                            row[
                                "regime_target"
                            ]
                        ),

                    "regime_probability":
                        float(
                            probability
                        ),

                    "harmful_target":
                        int(
                            row[
                                "harmful_target"
                            ]
                        ),

                    "local_error_std":
                        float(
                            row[
                                "local_error_std"
                            ]
                        ),

                    "severe_underestimation_probability":
                        float(
                            row[
                                "severe_underestimation_probability"
                            ]
                        ),
                }
            )

    return (
        fold_rows,
        event_rows,
        coefficient_rows,
    )


def aggregate_regime_performance(
    event_rows,
):
    y_true = np.asarray(
        [
            int(
                row[
                    "regime_target"
                ]
            )
            for row in event_rows
        ],
        dtype=int,
    )

    scores = np.asarray(
        [
            float(
                row[
                    "regime_probability"
                ]
            )
            for row in event_rows
        ],
        dtype=float,
    )

    return safe_auc(
        y_true,
        scores,
    )


def coefficient_stability(
    coefficient_rows,
):
    output = []

    features = sorted(
        {
            row[
                "feature"
            ]
            for row in coefficient_rows
        }
    )

    for feature in features:
        values = [
            float(
                row[
                    "coefficient"
                ]
            )
            for row in coefficient_rows
            if row[
                "feature"
            ]
            == feature
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
                "record_type":
                    "regime_coefficient_summary",

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


def fit_harm_models_with_regime(
    event_rows,
):
    rows = [
        dict(
            row
        )
        for row in event_rows
    ]

    for row in rows:
        row[
            "proxy_x_regime"
        ] = (
            float(
                row[
                    "severe_underestimation_probability"
                ]
            )
            * float(
                row[
                    "regime_probability"
                ]
            )
        )

    model_specs = {
        "severe_proxy_only": [
            "severe_underestimation_probability",
        ],

        "regime_only": [
            "regime_probability",
        ],

        "proxy_plus_regime": [
            "severe_underestimation_probability",
            "regime_probability",
        ],

        "proxy_regime_interaction": [
            "severe_underestimation_probability",
            "regime_probability",
            "proxy_x_regime",
        ],
    }

    output = []
    coefficients = []

    for model_name, features in model_specs.items():

        for held_out_block in [
            BLOCK_A,
            BLOCK_B,
        ]:
            training_rows = [
                row
                for row in rows
                if row[
                    "held_out_block"
                ]
                != held_out_block
            ]

            test_rows = [
                row
                for row in rows
                if row[
                    "held_out_block"
                ]
                == held_out_block
            ]

            x_train = build_matrix(
                training_rows,
                features,
            )

            y_train = build_labels(
                training_rows,
                "harmful_target",
            )

            x_test = build_matrix(
                test_rows,
                features,
            )

            y_test = build_labels(
                test_rows,
                "harmful_target",
            )

            if len(
                np.unique(
                    y_train
                )
            ) < 2:
                continue

            model = make_classifier()

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

            output.append(
                {
                    "record_type":
                        "harm_modulation_fold",

                    "model":
                        model_name,

                    "held_out_block":
                        held_out_block,

                    "roc_auc":
                        auc,

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
                }
            )

            classifier = model.named_steps[
                "classifier"
            ]

            for feature, coefficient in zip(
                features,
                classifier.coef_[
                    0
                ],
            ):
                coefficients.append(
                    {
                        "record_type":
                            "harm_modulation_coefficient",

                        "model":
                            model_name,

                        "held_out_block":
                            held_out_block,

                        "feature":
                            feature,

                        "coefficient":
                            float(
                                coefficient
                            ),
                    }
                )

    return (
        output,
        coefficients,
    )


def summarize_harm_models(
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
        matching = [
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
            for row in matching
        ]

        output.append(
            {
                "record_type":
                    "harm_modulation_summary",

                "model":
                    model_name,

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
        key=lambda row: (
            row[
                "mean_auc"
            ],
            row[
                "min_auc"
            ],
        ),
        reverse=True,
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
        "PRE-ACTION REGIME IDENTIFICATION ANALYSIS"
    )

    print(
        "=" * 210
    )

    rows = read_events()

    features = available_regime_features(
        rows
    )

    print(
        f"event rows="
        f"{len(rows)}"
    )

    print(
        f"regime features="
        f"{features}"
    )

    print(
        f"block A="
        f"{BLOCK_A}"
    )

    print(
        f"block B="
        f"{BLOCK_B}"
    )

    print()

    geometry_rows = univariate_regime_geometry(
        rows,
        features,
    )

    print(
        "UNIVARIATE PRE-ACTION REGIME GEOMETRY"
    )

    for row in geometry_rows:
        print(
            f"{row['feature']:<42} "
            f"A_mean="
            f"{row['block_a_mean']:.6f} "
            f"B_mean="
            f"{row['block_b_mean']:.6f} "
            f"delta="
            f"{row['difference_b_minus_a']:+.6f} "
            f"best_orientation_AUC="
            f"{row['regime_auc_best_orientation']:.3f}"
        )

    (
        regime_fold_rows,
        regime_event_rows,
        regime_coefficient_rows,
    ) = leave_one_seed_out_regime_model(
        rows,
        features,
    )

    pooled_regime_auc = aggregate_regime_performance(
        regime_event_rows
    )

    coefficient_summary_rows = (
        coefficient_stability(
            regime_coefficient_rows
        )
    )

    print()

    print(
        "PRE-ACTION REGIME IDENTIFICATION"
    )

    print(
        f"pooled leave-one-seed-out regime AUC="
        f"{pooled_regime_auc:.3f}"
    )

    print()

    print(
        "REGIME COEFFICIENT STABILITY"
    )

    for row in coefficient_summary_rows:
        print(
            f"{row['feature']:<42} "
            f"mean_coef="
            f"{row['mean_coefficient']:+.3f} "
            f"abs_coef="
            f"{row['mean_absolute_coefficient']:.3f} "
            f"sign_stability="
            f"{row['sign_stability']:.3%}"
        )

    (
        harm_fold_rows,
        harm_coefficient_rows,
    ) = fit_harm_models_with_regime(
        regime_event_rows
    )

    harm_summary_rows = summarize_harm_models(
        harm_fold_rows
    )

    print()

    print(
        "RISK-TO-HARM REGIME MODULATION"
    )

    for row in harm_summary_rows:
        print(
            f"{row['model']:<30} "
            f"mean_AUC="
            f"{row['mean_auc']:.3f} "
            f"min_AUC="
            f"{row['min_auc']:.3f} "
            f"max_AUC="
            f"{row['max_auc']:.3f}"
        )

    baseline = next(
        row
        for row in harm_summary_rows
        if row[
            "model"
        ]
        == "severe_proxy_only"
    )

    interaction = next(
        row
        for row in harm_summary_rows
        if row[
            "model"
        ]
        == "proxy_regime_interaction"
    )

    print()

    print(
        "INTERACTION VALUE-ADD"
    )

    print(
        f"dMeanAUC="
        f"{interaction['mean_auc'] - baseline['mean_auc']:+.3f}"
    )

    print(
        f"dMinAUC="
        f"{interaction['min_auc'] - baseline['min_auc']:+.3f}"
    )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 113 uses block identity only as an analysis "
        "target for learning a pre-action regime score."
    )

    print(
        "Block identity itself is never used as a deployable "
        "harm-prediction feature."
    )

    print(
        "All regime features are restricted to information available "
        "before support-expansion outcome realization."
    )

    print(
        "The key falsification test is whether the pre-action regime "
        "score improves or modulates the frozen severe-proxy-to-harm "
        "relationship under reciprocal block-held-out evaluation."
    )

    print(
        "No operating threshold, prospective seed, or controller "
        "modification is introduced."
    )

    print(
        "=" * 210
    )

    summary_rows = []

    summary_rows.extend(
        geometry_rows
    )

    summary_rows.append(
        {
            "record_type":
                "regime_identification_summary",

            "pooled_loso_regime_auc":
                pooled_regime_auc,
        }
    )

    summary_rows.extend(
        coefficient_summary_rows
    )

    summary_rows.extend(
        harm_summary_rows
    )

    summary_rows.extend(
        harm_fold_rows
    )

    save_csv(
        SUMMARY_OUTPUT_PATH,
        summary_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        regime_event_rows,
    )

    save_csv(
        COEFFICIENT_OUTPUT_PATH,
        (
            regime_coefficient_rows
            + harm_coefficient_rows
        ),
    )

    print(
        f"Summary saved to: "
        f"{SUMMARY_OUTPUT_PATH}"
    )

    print(
        f"Regime event scores saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )

    print(
        f"Coefficient results saved to: "
        f"{COEFFICIENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()