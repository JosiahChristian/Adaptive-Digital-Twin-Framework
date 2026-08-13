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

from experiments.historical_local_calibration_risk_representation import (
    event_rows_for_seed,
)


OUTPUT_PATH = Path(
    "results/"
    "frozen_prospective_historical_calibration_risk_validation.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "frozen_prospective_historical_calibration_risk_validation_events.csv"
)

SEED_OUTPUT_PATH = Path(
    "results/"
    "frozen_prospective_historical_calibration_risk_validation_seeds.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "frozen_prospective_historical_calibration_risk_validation_coefficients.csv"
)


DEVELOPMENT_SEEDS = list(
    range(
        44001,
        44071,
    )
)

PROSPECTIVE_SEEDS = list(
    range(
        44071,
        44091,
    )
)


K_NEIGHBORS = 7

SEVERE_UNDERESTIMATION_THRESHOLD = -0.050

CLASS_THRESHOLD = 0.50

RANDOM_STATE = 42


PRIMARY_MODEL_NAME = (
    "loss_plus_local_calibration"
)

BASELINE_MODEL_NAME = (
    "predicted_loss_only"
)


MODEL_SPECS = {
    "predicted_loss_only": [
        "predicted_action_loss",
    ],

    "local_mean_error_only": [
        "local_mean_error",
    ],

    "local_underestimate_fraction_only": [
        "local_underestimate_fraction",
    ],

    "local_severe_fraction_only": [
        "local_severe_underestimate_fraction",
    ],

    "local_error_std_only": [
        "local_error_std",
    ],

    "local_calibration_compact": [
        "local_mean_error",
        "local_error_std",
        "local_underestimate_fraction",
        "local_severe_underestimate_fraction",
    ],

    "loss_plus_local_calibration": [
        "predicted_action_loss",
        "local_mean_error",
        "local_error_std",
        "local_underestimate_fraction",
        "local_severe_underestimate_fraction",
    ],
}


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
    feature_names,
):
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
    rows,
):
    return np.asarray(
        [
            int(
                float(
                    row[
                        "calibration_error"
                    ]
                )
                <= SEVERE_UNDERESTIMATION_THRESHOLD
            )
            for row in rows
        ],
        dtype=int,
    )


def safe_auc(
    y_true,
    probabilities,
):
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
    y_true,
    predictions,
):
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


def confusion_counts(
    y_true,
    predictions,
):
    tp = int(
        np.sum(
            (
                y_true
                == 1
            )
            & (
                predictions
                == 1
            )
        )
    )

    fp = int(
        np.sum(
            (
                y_true
                == 0
            )
            & (
                predictions
                == 1
            )
        )
    )

    fn = int(
        np.sum(
            (
                y_true
                == 1
            )
            & (
                predictions
                == 0
            )
        )
    )

    tn = int(
        np.sum(
            (
                y_true
                == 0
            )
            & (
                predictions
                == 0
            )
        )
    )

    return (
        tp,
        fp,
        fn,
        tn,
    )


def evaluate_predictions(
    y_true,
    probabilities,
):
    predictions = (
        probabilities
        >= CLASS_THRESHOLD
    ).astype(
        int
    )

    (
        tp,
        fp,
        fn,
        tn,
    ) = confusion_counts(
        y_true,
        predictions,
    )

    balanced_accuracy = (
        float(
            balanced_accuracy_score(
                y_true,
                predictions,
            )
        )
        if (
            len(
                np.unique(
                    y_true
                )
            )
            == 2
        )
        else float(
            "nan"
        )
    )

    severe_recall = float(
        recall_score(
            y_true,
            predictions,
            pos_label=1,
            zero_division=0,
        )
    )

    severe_precision = float(
        precision_score(
            y_true,
            predictions,
            pos_label=1,
            zero_division=0,
        )
    )

    specificity = specificity_score(
        y_true,
        predictions,
    )

    auc = safe_auc(
        y_true,
        probabilities,
    )

    return {
        "balanced_accuracy":
            balanced_accuracy,

        "severe_recall":
            severe_recall,

        "severe_precision":
            severe_precision,

        "nonsevere_specificity":
            specificity,

        "roc_auc":
            auc,

        "tp":
            tp,

        "fp":
            fp,

        "fn":
            fn,

        "tn":
            tn,
    }


def fit_frozen_models(
    development_rows,
):
    models = {}

    coefficient_rows = []

    for (
        model_name,
        feature_names,
    ) in MODEL_SPECS.items():

        x_train = build_matrix(
            development_rows,
            feature_names,
        )

        y_train = build_labels(
            development_rows
        )

        model = make_model()

        model.fit(
            x_train,
            y_train,
        )

        models[
            model_name
        ] = model

        classifier = model.named_steps[
            "classifier"
        ]

        for (
            feature,
            coefficient,
        ) in zip(
            feature_names,
            classifier.coef_[
                0
            ],
        ):

            coefficient_rows.append(
                {
                    "model":
                        model_name,

                    "feature":
                        feature,

                    "standardized_coefficient":
                        float(
                            coefficient
                        ),
                }
            )

    return (
        models,
        coefficient_rows,
    )


def predict_model(
    model,
    rows,
    feature_names,
):
    x = build_matrix(
        rows,
        feature_names,
    )

    return model.predict_proba(
        x
    )[
        :,
        1
    ]


def finite_mean(
    values,
):
    finite = [
        value
        for value in values
        if math.isfinite(
            value
        )
    ]

    if not finite:
        return float(
            "nan"
        )

    return statistics.mean(
        finite
    )


def evaluate_seed_level(
    models,
    prospective_rows,
):
    seed_rows = []

    grouped = defaultdict(
        list
    )

    for row in prospective_rows:
        grouped[
            int(
                row[
                    "generation_seed"
                ]
            )
        ].append(
            row
        )

    for seed in PROSPECTIVE_SEEDS:
        rows = grouped[
            seed
        ]

        y_true = build_labels(
            rows
        )

        for (
            model_name,
            feature_names,
        ) in MODEL_SPECS.items():

            probabilities = predict_model(
                models[
                    model_name
                ],
                rows,
                feature_names,
            )

            metrics = evaluate_predictions(
                y_true,
                probabilities,
            )

            severe_total = int(
                np.sum(
                    y_true
                    == 1
                )
            )

            nonsevere_total = int(
                np.sum(
                    y_true
                    == 0
                )
            )

            seed_rows.append(
                {
                    "generation_seed":
                        seed,

                    "model":
                        model_name,

                    "rows":
                        len(
                            rows
                        ),

                    "severe_rows":
                        severe_total,

                    "nonsevere_rows":
                        nonsevere_total,

                    "severe_fraction":
                        (
                            severe_total
                            / len(
                                rows
                            )
                        ),

                    **metrics,
                }
            )

    return seed_rows


def aggregate_seed_statistics(
    seed_rows,
    model_name,
):
    rows = [
        row
        for row in seed_rows
        if row[
            "model"
        ]
        == model_name
    ]

    informative_balanced = [
        float(
            row[
                "balanced_accuracy"
            ]
        )
        for row in rows
        if math.isfinite(
            float(
                row[
                    "balanced_accuracy"
                ]
            )
        )
    ]

    informative_auc = [
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

    seeds_with_severe = sum(
        int(
            int(
                row[
                    "severe_rows"
                ]
            )
            > 0
        )
        for row in rows
    )

    return {
        "seeds":
            len(
                rows
            ),

        "seeds_with_severe":
            seeds_with_severe,

        "mean_seed_balanced_accuracy":
            finite_mean(
                informative_balanced
            ),

        "min_seed_balanced_accuracy":
            (
                min(
                    informative_balanced
                )
                if informative_balanced
                else float(
                    "nan"
                )
            ),

        "mean_seed_auc":
            finite_mean(
                informative_auc
            ),

        "min_seed_auc":
            (
                min(
                    informative_auc
                )
                if informative_auc
                else float(
                    "nan"
                )
            ),

        "seeds_with_tp":
            sum(
                int(
                    int(
                        row[
                            "tp"
                        ]
                    )
                    > 0
                )
                for row in rows
            ),
    }


def feature_diagnostics(
    development_rows,
    prospective_rows,
):
    fields = [
        "predicted_action_loss",
        "local_mean_error",
        "local_error_std",
        "local_underestimate_fraction",
        "local_severe_underestimate_fraction",
    ]

    output = []

    development_labels = build_labels(
        development_rows
    )

    prospective_labels = build_labels(
        prospective_rows
    )

    for field in fields:

        dev_nonsevere = [
            float(
                row[
                    field
                ]
            )
            for (
                row,
                target,
            ) in zip(
                development_rows,
                development_labels,
            )
            if target == 0
        ]

        dev_severe = [
            float(
                row[
                    field
                ]
            )
            for (
                row,
                target,
            ) in zip(
                development_rows,
                development_labels,
            )
            if target == 1
        ]

        prospective_nonsevere = [
            float(
                row[
                    field
                ]
            )
            for (
                row,
                target,
            ) in zip(
                prospective_rows,
                prospective_labels,
            )
            if target == 0
        ]

        prospective_severe = [
            float(
                row[
                    field
                ]
            )
            for (
                row,
                target,
            ) in zip(
                prospective_rows,
                prospective_labels,
            )
            if target == 1
        ]

        dev_delta = (
            statistics.mean(
                dev_severe
            )
            - statistics.mean(
                dev_nonsevere
            )
        )

        prospective_delta = (
            statistics.mean(
                prospective_severe
            )
            - statistics.mean(
                prospective_nonsevere
            )
        )

        output.append(
            {
                "metric":
                    field,

                "development_nonsevere_mean":
                    statistics.mean(
                        dev_nonsevere
                    ),

                "development_severe_mean":
                    statistics.mean(
                        dev_severe
                    ),

                "development_delta":
                    dev_delta,

                "prospective_nonsevere_mean":
                    statistics.mean(
                        prospective_nonsevere
                    ),

                "prospective_severe_mean":
                    statistics.mean(
                        prospective_severe
                    ),

                "prospective_delta":
                    prospective_delta,

                "direction_preserved":
                    int(
                        (
                            dev_delta
                            == 0.0
                        )
                        or (
                            prospective_delta
                            == 0.0
                        )
                        or (
                            np.sign(
                                dev_delta
                            )
                            == np.sign(
                                prospective_delta
                            )
                        )
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
        "FROZEN PROSPECTIVE HISTORICAL "
        "CALIBRATION-RISK VALIDATION"
    )

    print(
        "=" * 210
    )

    print(
        f"development seeds="
        f"{DEVELOPMENT_SEEDS[0]}-"
        f"{DEVELOPMENT_SEEDS[-1]}"
    )

    print(
        f"prospective seeds="
        f"{PROSPECTIVE_SEEDS[0]}-"
        f"{PROSPECTIVE_SEEDS[-1]}"
    )

    print(
        f"local neighbors="
        f"{K_NEIGHBORS}"
    )

    print(
        f"severe underestimation threshold="
        f"{SEVERE_UNDERESTIMATION_THRESHOLD:.3f}"
    )

    print(
        f"primary model="
        f"{PRIMARY_MODEL_NAME}"
    )

    print(
        f"baseline model="
        f"{BASELINE_MODEL_NAME}"
    )

    print()

    print(
        "RECONSTRUCTING FROZEN DEVELOPMENT POPULATION"
    )

    development_rows = []

    for seed in DEVELOPMENT_SEEDS:

        print(
            f"development seed "
            f"{seed}..."
        )

        development_rows.extend(
            event_rows_for_seed(
                seed
            )
        )

    print()

    print(
        "FITTING FROZEN DEVELOPMENT MODELS"
    )

    (
        models,
        coefficient_rows,
    ) = fit_frozen_models(
        development_rows
    )

    print(
        f"development action-context rows="
        f"{len(development_rows)}"
    )

    development_labels = build_labels(
        development_rows
    )

    print(
        f"development severe="
        f"{int(np.sum(development_labels == 1))}"
    )

    print(
        f"development nonsevere="
        f"{int(np.sum(development_labels == 0))}"
    )

    print()

    print(
        "BEGINNING UNTOUCHED PROSPECTIVE BLOCK"
    )

    prospective_rows = []

    for seed in PROSPECTIVE_SEEDS:

        print(
            f"prospective seed "
            f"{seed}..."
        )

        seed_events = event_rows_for_seed(
            seed
        )

        prospective_rows.extend(
            seed_events
        )

    prospective_labels = build_labels(
        prospective_rows
    )

    severe_total = int(
        np.sum(
            prospective_labels
            == 1
        )
    )

    nonsevere_total = int(
        np.sum(
            prospective_labels
            == 0
        )
    )

    print()

    print(
        "PROSPECTIVE EVENT POPULATION"
    )

    print(
        f"action-context rows="
        f"{len(prospective_rows)}"
    )

    print(
        f"severe_underestimation="
        f"{severe_total}"
    )

    print(
        f"nonsevere="
        f"{nonsevere_total}"
    )

    print(
        f"severe fraction="
        f"{severe_total / len(prospective_rows):.3%}"
    )

    summary_rows = []

    event_output_rows = [
        dict(
            row
        )
        for row in prospective_rows
    ]

    print()

    print(
        "FROZEN PROSPECTIVE MODEL PERFORMANCE"
    )

    for (
        model_name,
        feature_names,
    ) in MODEL_SPECS.items():

        probabilities = predict_model(
            models[
                model_name
            ],
            prospective_rows,
            feature_names,
        )

        metrics = evaluate_predictions(
            prospective_labels,
            probabilities,
        )

        for (
            row,
            probability,
        ) in zip(
            event_output_rows,
            probabilities,
        ):

            row[
                f"{model_name}_probability"
            ] = float(
                probability
            )

        summary = {
            "record_type":
                "model_summary",

            "model":
                model_name,

            "feature_count":
                len(
                    feature_names
                ),

            "features":
                "|".join(
                    feature_names
                ),

            "prospective_rows":
                len(
                    prospective_rows
                ),

            "severe_rows":
                severe_total,

            "nonsevere_rows":
                nonsevere_total,

            "severe_fraction":
                (
                    severe_total
                    / len(
                        prospective_rows
                    )
                ),

            **metrics,
        }

        summary_rows.append(
            summary
        )

        print(
            f"{model_name:<34} "
            f"balanced_acc="
            f"{metrics['balanced_accuracy']:.3%} "
            f"severe_recall="
            f"{metrics['severe_recall']:.3%} "
            f"severe_precision="
            f"{metrics['severe_precision']:.3%} "
            f"specificity="
            f"{metrics['nonsevere_specificity']:.3%} "
            f"AUC="
            f"{metrics['roc_auc']:.3f} "
            f"TP="
            f"{metrics['tp']} "
            f"FP="
            f"{metrics['fp']} "
            f"FN="
            f"{metrics['fn']} "
            f"TN="
            f"{metrics['tn']}"
        )

    seed_rows = evaluate_seed_level(
        models,
        prospective_rows,
    )

    for row in summary_rows:

        stability = aggregate_seed_statistics(
            seed_rows,
            row[
                "model"
            ],
        )

        row.update(
            stability
        )

    summary_lookup = {
        row[
            "model"
        ]:
            row
        for row in summary_rows
    }

    primary = summary_lookup[
        PRIMARY_MODEL_NAME
    ]

    baseline = summary_lookup[
        BASELINE_MODEL_NAME
    ]

    print()

    print(
        "PRIMARY PREREGISTERED COMPARISON"
    )

    print(
        f"primary="
        f"{PRIMARY_MODEL_NAME}"
    )

    print(
        f"baseline="
        f"{BASELINE_MODEL_NAME}"
    )

    print(
        f"dBalancedAccuracy="
        f"{primary['balanced_accuracy'] - baseline['balanced_accuracy']:+.3%}"
    )

    print(
        f"dSevereRecall="
        f"{primary['severe_recall'] - baseline['severe_recall']:+.3%}"
    )

    print(
        f"dSpecificity="
        f"{primary['nonsevere_specificity'] - baseline['nonsevere_specificity']:+.3%}"
    )

    print(
        f"dAUC="
        f"{primary['roc_auc'] - baseline['roc_auc']:+.3f}"
    )

    print()

    print(
        "PRIMARY SEED-LEVEL STABILITY"
    )

    print(
        f"seeds="
        f"{primary['seeds']}"
    )

    print(
        f"seeds with severe events="
        f"{primary['seeds_with_severe']}"
    )

    print(
        f"seeds with >=1 true positive="
        f"{primary['seeds_with_tp']}"
    )

    print(
        f"mean seed balanced accuracy="
        f"{primary['mean_seed_balanced_accuracy']:.3%}"
    )

    print(
        f"min seed balanced accuracy="
        f"{primary['min_seed_balanced_accuracy']:.3%}"
    )

    print(
        f"mean seed AUC="
        f"{primary['mean_seed_auc']:.3f}"
    )

    print(
        f"min seed AUC="
        f"{primary['min_seed_auc']:.3f}"
    )

    diagnostic_rows = feature_diagnostics(
        development_rows,
        prospective_rows,
    )

    print()

    print(
        "FEATURE-DIRECTION TRANSFER"
    )

    for row in diagnostic_rows:

        print(
            f"{row['metric']:<38} "
            f"dev_delta="
            f"{row['development_delta']:+.6f} "
            f"prospective_delta="
            f"{row['prospective_delta']:+.6f} "
            f"direction_preserved="
            f"{bool(row['direction_preserved'])}"
        )

    preserved_count = sum(
        int(
            row[
                "direction_preserved"
            ]
        )
        for row in diagnostic_rows
    )

    print()

    print(
        "FROZEN PRIMARY MODEL COEFFICIENTS"
    )

    for row in coefficient_rows:

        if row[
            "model"
        ] != PRIMARY_MODEL_NAME:
            continue

        print(
            f"{row['feature']:<38} "
            f"coefficient="
            f"{row['standardized_coefficient']:+.3f}"
        )

    print()

    print(
        "PREREGISTERED INTERPRETATION CHECK"
    )

    auc_improved = (
        primary[
            "roc_auc"
        ]
        > baseline[
            "roc_auc"
        ]
    )

    balanced_improved = (
        primary[
            "balanced_accuracy"
        ]
        > baseline[
            "balanced_accuracy"
        ]
    )

    not_single_seed = (
        primary[
            "seeds_with_severe"
        ]
        > 1
    )

    feature_direction_majority = (
        preserved_count
        >= (
            len(
                diagnostic_rows
            )
            / 2
        )
    )

    print(
        f"primary AUC exceeds baseline="
        f"{auc_improved}"
    )

    print(
        f"primary balanced accuracy exceeds baseline="
        f"{balanced_improved}"
    )

    print(
        f"severe events span multiple seeds="
        f"{not_single_seed}"
    )

    print(
        f"majority feature directions preserved="
        f"{feature_direction_majority}"
    )

    print()

    if (
        auc_improved
        and balanced_improved
        and not_single_seed
        and feature_direction_majority
    ):

        print(
            "PRIMARY RESULT: "
            "prospective evidence favors the frozen "
            "historical calibration-risk representation "
            "over predicted loss alone."
        )

    else:

        print(
            "PRIMARY RESULT: "
            "the preregistered prospective evidence does "
            "not fully support superiority of the frozen "
            "historical calibration-risk representation."
        )

    print()

    print(
        "IMPORTANT INTERPRETATION LIMIT"
    )

    print(
        "Experiment 100 validates predictive representation only. "
        "No controller action is changed by these predictions."
    )

    print(
        "Prospective test outcomes are used only after prediction "
        "to score calibration error and severe-underestimation labels."
    )

    print(
        "=" * 210
    )

    output_rows = []

    output_rows.extend(
        summary_rows
    )

    for row in diagnostic_rows:

        copy = {
            "record_type":
                "feature_transfer"
        }

        copy.update(
            row
        )

        output_rows.append(
            copy
        )

    save_csv(
        OUTPUT_PATH,
        output_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        event_output_rows,
    )

    save_csv(
        SEED_OUTPUT_PATH,
        seed_rows,
    )

    save_csv(
        COEFFICIENT_OUTPUT_PATH,
        coefficient_rows,
    )

    print(
        f"Summary saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Prospective event predictions saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )

    print(
        f"Seed-level results saved to: "
        f"{SEED_OUTPUT_PATH}"
    )

    print(
        f"Frozen coefficients saved to: "
        f"{COEFFICIENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()