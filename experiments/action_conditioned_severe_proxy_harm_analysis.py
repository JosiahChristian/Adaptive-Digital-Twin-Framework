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
    "frozen_pre_action_calibration_proxy_support_expansion_transfer_events.csv"
)

SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "action_conditioned_severe_proxy_harm_analysis.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "action_conditioned_severe_proxy_harm_analysis_events.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "action_conditioned_severe_proxy_harm_analysis_coefficients.csv"
)


BLOCKS = [
    "block_071_090",
    "block_091_110",
]

ACTIONS = [
    1,
    2,
]

SOURCE_MODEL = "severe_proxy_only"

PROXY_FIELD = "severe_underestimation_probability"

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
    seen = set()

    for row in rows:
        if row.get(
            "model",
            "",
        ) != SOURCE_MODEL:
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
            PROXY_FIELD
        ] = float(
            copy[
                PROXY_FIELD
            ]
        )

        copy[
            "harmful_target"
        ] = int(
            copy[
                "harmful_target"
            ]
        )

        output.append(
            copy
        )

    return output


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


def action_block_geometry(
    rows,
):
    output = []

    for block in BLOCKS:
        for action in ACTIONS:

            matching = [
                row
                for row in rows
                if (
                    row[
                        "held_out_block"
                    ]
                    == block
                    and int(
                        row[
                            "support_baseline_action"
                        ]
                    )
                    == action
                )
            ]

            harmful = [
                row
                for row in matching
                if int(
                    row[
                        "harmful_target"
                    ]
                )
                == 1
            ]

            beneficial = [
                row
                for row in matching
                if int(
                    row[
                        "harmful_target"
                    ]
                )
                == 0
            ]

            y_true = np.asarray(
                [
                    int(
                        row[
                            "harmful_target"
                        ]
                    )
                    for row in matching
                ],
                dtype=int,
            )

            scores = np.asarray(
                [
                    float(
                        row[
                            PROXY_FIELD
                        ]
                    )
                    for row in matching
                ],
                dtype=float,
            )

            harmful_mean = (
                statistics.mean(
                    float(
                        row[
                            PROXY_FIELD
                        ]
                    )
                    for row in harmful
                )
                if harmful
                else float(
                    "nan"
                )
            )

            beneficial_mean = (
                statistics.mean(
                    float(
                        row[
                            PROXY_FIELD
                        ]
                    )
                    for row in beneficial
                )
                if beneficial
                else float(
                    "nan"
                )
            )

            output.append(
                {
                    "record_type":
                        "action_block_geometry",

                    "block":
                        block,

                    "action":
                        action,

                    "rows":
                        len(
                            matching
                        ),

                    "harmful":
                        len(
                            harmful
                        ),

                    "beneficial":
                        len(
                            beneficial
                        ),

                    "harmful_proxy_mean":
                        harmful_mean,

                    "beneficial_proxy_mean":
                        beneficial_mean,

                    "difference_harmful_minus_beneficial":
                        (
                            harmful_mean
                            - beneficial_mean
                            if (
                                math.isfinite(
                                    harmful_mean
                                )
                                and math.isfinite(
                                    beneficial_mean
                                )
                            )
                            else float(
                                "nan"
                            )
                        ),

                    "rank_auc":
                        safe_auc(
                            y_true,
                            scores,
                        ),
                }
            )

    return output


def pooled_action_geometry(
    rows,
):
    output = []

    for action in ACTIONS:
        matching = [
            row
            for row in rows
            if int(
                row[
                    "support_baseline_action"
                ]
            )
            == action
        ]

        y_true = np.asarray(
            [
                int(
                    row[
                        "harmful_target"
                    ]
                )
                for row in matching
            ],
            dtype=int,
        )

        scores = np.asarray(
            [
                float(
                    row[
                        PROXY_FIELD
                    ]
                )
                for row in matching
            ],
            dtype=float,
        )

        harmful = [
            float(
                row[
                    PROXY_FIELD
                ]
            )
            for row in matching
            if int(
                row[
                    "harmful_target"
                ]
            )
            == 1
        ]

        beneficial = [
            float(
                row[
                    PROXY_FIELD
                ]
            )
            for row in matching
            if int(
                row[
                    "harmful_target"
                ]
            )
            == 0
        ]

        output.append(
            {
                "record_type":
                    "pooled_action_geometry",

                "action":
                    action,

                "rows":
                    len(
                        matching
                    ),

                "harmful":
                    len(
                        harmful
                    ),

                "beneficial":
                    len(
                        beneficial
                    ),

                "harmful_proxy_mean":
                    (
                        statistics.mean(
                            harmful
                        )
                        if harmful
                        else float(
                            "nan"
                        )
                    ),

                "beneficial_proxy_mean":
                    (
                        statistics.mean(
                            beneficial
                        )
                        if beneficial
                        else float(
                            "nan"
                        )
                    ),

                "rank_auc":
                    safe_auc(
                        y_true,
                        scores,
                    ),
            }
        )

    return output


def build_matrix(
    rows,
    features,
):
    return np.asarray(
        [
            [
                float(
                    row[
                        field
                    ]
                )
                for field in features
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


def reciprocal_within_action(
    rows,
):
    output = []

    for action in ACTIONS:

        for held_out_block in BLOCKS:

            training_rows = [
                row
                for row in rows
                if (
                    row[
                        "held_out_block"
                    ]
                    != held_out_block
                    and int(
                        row[
                            "support_baseline_action"
                        ]
                    )
                    == action
                )
            ]

            test_rows = [
                row
                for row in rows
                if (
                    row[
                        "held_out_block"
                    ]
                    == held_out_block
                    and int(
                        row[
                            "support_baseline_action"
                        ]
                    )
                    == action
                )
            ]

            y_train = build_labels(
                training_rows
            )

            y_test = build_labels(
                test_rows
            )

            if (
                len(
                    training_rows
                )
                == 0
                or len(
                    test_rows
                )
                == 0
                or len(
                    np.unique(
                        y_train
                    )
                )
                < 2
                or len(
                    np.unique(
                        y_test
                    )
                )
                < 2
            ):
                output.append(
                    {
                        "record_type":
                            "within_action_transfer",

                        "action":
                            action,

                        "held_out_block":
                            held_out_block,

                        "training_rows":
                            len(
                                training_rows
                            ),

                        "training_harmful":
                            int(
                                np.sum(
                                    y_train
                                    == 1
                                )
                            )
                            if len(
                                y_train
                            )
                            else 0,

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
                            )
                            if len(
                                y_test
                            )
                            else 0,

                        "roc_auc":
                            float(
                                "nan"
                            ),

                        "status":
                            "uninformative_class_distribution",
                    }
                )

                continue

            x_train = build_matrix(
                training_rows,
                [
                    PROXY_FIELD,
                ],
            )

            x_test = build_matrix(
                test_rows,
                [
                    PROXY_FIELD,
                ],
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

            output.append(
                {
                    "record_type":
                        "within_action_transfer",

                    "action":
                        action,

                    "held_out_block":
                        held_out_block,

                    "training_rows":
                        len(
                            training_rows
                        ),

                    "training_harmful":
                        int(
                            np.sum(
                                y_train
                                == 1
                            )
                        ),

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

                    "roc_auc":
                        safe_auc(
                            y_test,
                            probabilities,
                        ),

                    "status":
                        "evaluated",
                }
            )

    return output


def pooled_model_comparison(
    rows,
):
    prepared = []

    for row in rows:
        copy = dict(
            row
        )

        action_indicator = int(
            int(
                row[
                    "support_baseline_action"
                ]
            )
            == 2
        )

        copy[
            "action2_indicator"
        ] = action_indicator

        copy[
            "proxy_x_action2"
        ] = (
            float(
                row[
                    PROXY_FIELD
                ]
            )
            * action_indicator
        )

        prepared.append(
            copy
        )

    model_specs = {
        "severe_proxy_only": [
            PROXY_FIELD,
        ],

        "action_only": [
            "action2_indicator",
        ],

        "proxy_plus_action": [
            PROXY_FIELD,
            "action2_indicator",
        ],

        "proxy_action_interaction": [
            PROXY_FIELD,
            "action2_indicator",
            "proxy_x_action2",
        ],
    }

    fold_rows = []
    coefficient_rows = []

    for model_name, features in model_specs.items():

        for held_out_block in BLOCKS:

            training_rows = [
                row
                for row in prepared
                if row[
                    "held_out_block"
                ]
                != held_out_block
            ]

            test_rows = [
                row
                for row in prepared
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
                training_rows
            )

            x_test = build_matrix(
                test_rows,
                features,
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

            auc = safe_auc(
                y_test,
                probabilities,
            )

            fold_rows.append(
                {
                    "record_type":
                        "pooled_model_fold",

                    "model":
                        model_name,

                    "held_out_block":
                        held_out_block,

                    "roc_auc":
                        auc,

                    "training_harmful":
                        int(
                            np.sum(
                                y_train
                                == 1
                            )
                        ),

                    "test_harmful":
                        int(
                            np.sum(
                                y_test
                                == 1
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
                coefficient_rows.append(
                    {
                        "record_type":
                            "pooled_model_coefficient",

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
        fold_rows,
        coefficient_rows,
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
        ]

        output.append(
            {
                "record_type":
                    "pooled_model_summary",

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
            float(
                row[
                    "mean_auc"
                ]
            ),
            float(
                row[
                    "min_auc"
                ]
            ),
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
                "record_type":
                    "coefficient_summary",

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
        "ACTION-CONDITIONED SEVERE-PROXY HARM ANALYSIS"
    )

    print(
        "=" * 210
    )

    print(
        f"input="
        f"{INPUT_PATH}"
    )

    print(
        f"source model="
        f"{SOURCE_MODEL}"
    )

    print(
        f"proxy="
        f"{PROXY_FIELD}"
    )

    print(
        f"actions="
        f"{ACTIONS}"
    )

    print()

    rows = read_events()

    print(
        "EVENT POPULATION"
    )

    print(
        f"rows="
        f"{len(rows)}"
    )

    print(
        f"harmful="
        f"{sum(row['harmful_target'] for row in rows)}"
    )

    print(
        f"beneficial="
        f"{sum(1 - row['harmful_target'] for row in rows)}"
    )

    geometry_rows = action_block_geometry(
        rows
    )

    pooled_geometry_rows = pooled_action_geometry(
        rows
    )

    print()

    print(
        "ACTION-BY-BLOCK PROXY GEOMETRY"
    )

    for block in BLOCKS:
        print()

        print(
            block
        )

        matching = [
            row
            for row in geometry_rows
            if row[
                "block"
            ]
            == block
        ]

        for row in matching:
            print(
                f"  action="
                f"{row['action']} "
                f"rows="
                f"{row['rows']} "
                f"harmful="
                f"{row['harmful']} "
                f"beneficial="
                f"{row['beneficial']} "
                f"harmful_mean="
                f"{row['harmful_proxy_mean']:.6f} "
                f"beneficial_mean="
                f"{row['beneficial_proxy_mean']:.6f} "
                f"delta="
                f"{row['difference_harmful_minus_beneficial']:+.6f} "
                f"rank_AUC="
                f"{row['rank_auc']:.3f}"
            )

    print()

    print(
        "POOLED ACTION-CONDITIONED GEOMETRY"
    )

    for row in pooled_geometry_rows:
        print(
            f"action="
            f"{row['action']} "
            f"rows="
            f"{row['rows']} "
            f"harmful="
            f"{row['harmful']} "
            f"beneficial="
            f"{row['beneficial']} "
            f"harmful_mean="
            f"{row['harmful_proxy_mean']:.6f} "
            f"beneficial_mean="
            f"{row['beneficial_proxy_mean']:.6f} "
            f"rank_AUC="
            f"{row['rank_auc']:.3f}"
        )

    within_action_rows = (
        reciprocal_within_action(
            rows
        )
    )

    print()

    print(
        "RECIPROCAL BLOCK-HELD-OUT WITHIN-ACTION TRANSFER"
    )

    for action in ACTIONS:
        print()

        print(
            f"action={action}"
        )

        matching = [
            row
            for row in within_action_rows
            if row[
                "action"
            ]
            == action
        ]

        for row in matching:
            print(
                f"  held_out="
                f"{row['held_out_block']:<16} "
                f"train_rows="
                f"{row['training_rows']} "
                f"train_harmful="
                f"{row['training_harmful']} "
                f"test_rows="
                f"{row['test_rows']} "
                f"test_harmful="
                f"{row['test_harmful']} "
                f"AUC="
                f"{row['roc_auc']:.3f} "
                f"status="
                f"{row['status']}"
            )

    (
        fold_rows,
        coefficient_rows,
    ) = pooled_model_comparison(
        rows
    )

    summary_rows = summarize_models(
        fold_rows
    )

    coefficient_summary_rows = (
        coefficient_stability(
            coefficient_rows
        )
    )

    print()

    print(
        "POOLED ACTION-CONDITIONING MODEL COMPARISON"
    )

    for row in summary_rows:
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
        for row in summary_rows
        if row[
            "model"
        ]
        == "severe_proxy_only"
    )

    interaction = next(
        row
        for row in summary_rows
        if row[
            "model"
        ]
        == "proxy_action_interaction"
    )

    print()

    print(
        "ACTION-INTERACTION VALUE-ADD"
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
        "COEFFICIENT STABILITY"
    )

    for row in coefficient_summary_rows:
        print(
            f"{row['model']:<30} "
            f"{row['feature']:<36} "
            f"mean_coef="
            f"{row['mean_coefficient']:+.3f} "
            f"abs_coef="
            f"{row['mean_absolute_coefficient']:.3f} "
            f"sign_stability="
            f"{row['sign_stability']:.3%}"
        )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 115 treats support-baseline action identity "
        "as a predefined structural variable motivated by the "
        "secondary action-composition diagnostic in Experiment 114."
    )

    print(
        "No intervention threshold is selected."
    )

    print(
        "Within-action transfer is reported only where both training "
        "and held-out action subsets contain harmful and beneficial "
        "events; otherwise the fold is marked uninformative."
    )

    print(
        "The pooled interaction test asks whether action identity "
        "modifies the frozen severe-underestimation-proxy-to-harm "
        "relationship under reciprocal block-held-out evaluation."
    )

    print(
        "No new prospective seed or controller modification "
        "is introduced."
    )

    print(
        "Only eight harmful support-expansion events exist, so "
        "all positive interaction evidence remains provisional."
    )

    print(
        "=" * 210
    )

    combined_summary = []

    combined_summary.extend(
        geometry_rows
    )

    combined_summary.extend(
        pooled_geometry_rows
    )

    combined_summary.extend(
        within_action_rows
    )

    combined_summary.extend(
        summary_rows
    )

    combined_summary.extend(
        fold_rows
    )

    combined_summary.extend(
        coefficient_summary_rows
    )

    save_csv(
        SUMMARY_OUTPUT_PATH,
        combined_summary,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        rows,
    )

    save_csv(
        COEFFICIENT_OUTPUT_PATH,
        (
            coefficient_rows
            + coefficient_summary_rows
        ),
    )

    print(
        f"Summary saved to: "
        f"{SUMMARY_OUTPUT_PATH}"
    )

    print(
        f"Joined event population saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )

    print(
        f"Coefficient results saved to: "
        f"{COEFFICIENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()