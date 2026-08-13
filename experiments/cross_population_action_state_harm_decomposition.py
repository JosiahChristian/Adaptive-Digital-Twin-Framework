import csv
import math
import statistics
from pathlib import Path

import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


EARLY_EVENT_PATH = Path(
    "results/"
    "harmful_expansion_action_conditioned_epistemic_excess_analysis_events.csv"
)

LATE_EVENT_PATH = Path(
    "results/"
    "action_conditioned_severe_proxy_harm_analysis_events.csv"
)

LATE_GEOMETRY_PATH = Path(
    "results/"
    "action_conditioned_support_representation_analysis_actions_071_110.csv"
)


SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "cross_population_action_state_harm_decomposition.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "cross_population_action_state_harm_decomposition_events.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "cross_population_action_state_harm_decomposition_coefficients.csv"
)


POPULATION_EARLY = "population_001_010"
POPULATION_LATE = "population_071_110"


GEOMETRY_FEATURES = [
    "context_support_distance",
    "action_support_distance",
    "action_support_minus_context",
    "predicted_action_loss",
    "predicted_relative_loss",
]


RANDOM_STATE = 42


def read_csv(path):
    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        return list(
            csv.DictReader(
                file
            )
        )


def as_float(
    row,
    field,
    default=float("nan"),
):
    value = row.get(
        field,
        "",
    )

    if value in (
        "",
        None,
    ):
        return default

    try:
        return float(
            value
        )

    except (
        TypeError,
        ValueError,
    ):
        return default


def as_int(
    row,
    field,
    default=0,
):
    value = as_float(
        row,
        field,
    )

    if not math.isfinite(
        value
    ):
        return default

    return int(
        value
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


def early_population():
    rows = read_csv(
        EARLY_EVENT_PATH
    )

    output = []

    for row in rows:
        expanded_action = as_int(
            row,
            "expanded_action",
        )

        reconstructed_action = as_int(
            row,
            "expanded_action_reconstructed",
        )

        if (
            expanded_action
            != reconstructed_action
        ):
            raise RuntimeError(
                "Early-population action reconstruction mismatch: "
                f"seed={row.get('generation_seed')} "
                f"test_index={row.get('test_index')}"
            )

        if expanded_action not in {
            1,
            2,
        }:
            continue

        outcome = row.get(
            "outcome",
            "",
        )

        if outcome not in {
            "beneficial",
            "harmful",
        }:
            continue

        context_distance = as_float(
            row,
            "context_support_distance",
        )

        action_distance = as_float(
            row,
            "action_support_distance",
        )

        predicted_action_loss = as_float(
            row,
            "predicted_action_loss",
        )

        predicted_relative_loss = as_float(
            row,
            "predicted_relative_loss",
        )

        values = [
            context_distance,
            action_distance,
            predicted_action_loss,
            predicted_relative_loss,
        ]

        if not all(
            math.isfinite(
                value
            )
            for value in values
        ):
            raise RuntimeError(
                "Non-finite early-population pre-action geometry."
            )

        output.append(
            {
                "population":
                    POPULATION_EARLY,

                "generation_seed":
                    as_int(
                        row,
                        "generation_seed",
                    ),

                "test_index":
                    as_int(
                        row,
                        "test_index",
                    ),

                "action":
                    expanded_action,

                "action2_indicator":
                    int(
                        expanded_action
                        == 2
                    ),

                "harmful_target":
                    int(
                        outcome
                        == "harmful"
                    ),

                "context_support_distance":
                    context_distance,

                "action_support_distance":
                    action_distance,

                "action_support_minus_context":
                    (
                        action_distance
                        - context_distance
                    ),

                "predicted_action_loss":
                    predicted_action_loss,

                "predicted_relative_loss":
                    predicted_relative_loss,
            }
        )

    return output


def late_geometry_lookup():
    rows = read_csv(
        LATE_GEOMETRY_PATH
    )

    lookup = {}

    for row in rows:
        key = (
            as_int(
                row,
                "generation_seed",
            ),
            as_int(
                row,
                "test_index",
            ),
            as_int(
                row,
                "action",
            ),
        )

        lookup[
            key
        ] = row

    return lookup


def late_population():
    event_rows = read_csv(
        LATE_EVENT_PATH
    )

    geometry_lookup = (
        late_geometry_lookup()
    )

    output = []
    seen = set()

    for row in event_rows:
        # Experiment 115 event export should already contain one
        # row per support expansion, but deduplicate defensively.
        key = (
            as_int(
                row,
                "generation_seed",
            ),
            as_int(
                row,
                "test_index",
            ),
            as_int(
                row,
                "support_baseline_action",
            ),
        )

        if key in seen:
            continue

        seen.add(
            key
        )

        generation_seed, test_index, action = key

        if action not in {
            1,
            2,
        }:
            continue

        geometry_row = geometry_lookup.get(
            key
        )

        if geometry_row is None:
            raise RuntimeError(
                "Missing later-population action geometry for "
                f"key={key}"
            )

        context_distance = as_float(
            geometry_row,
            "context_support_distance",
        )

        action_distance = as_float(
            geometry_row,
            "action_support_distance",
        )

        predicted_action_loss = as_float(
            geometry_row,
            "predicted_action_loss",
        )

        predicted_relative_loss = as_float(
            geometry_row,
            "predicted_relative_loss",
        )

        values = [
            context_distance,
            action_distance,
            predicted_action_loss,
            predicted_relative_loss,
        ]

        if not all(
            math.isfinite(
                value
            )
            for value in values
        ):
            raise RuntimeError(
                "Non-finite later-population pre-action geometry."
            )

        output.append(
            {
                "population":
                    POPULATION_LATE,

                "generation_seed":
                    generation_seed,

                "test_index":
                    test_index,

                "action":
                    action,

                "action2_indicator":
                    int(
                        action
                        == 2
                    ),

                "harmful_target":
                    as_int(
                        row,
                        "harmful_target",
                    ),

                "context_support_distance":
                    context_distance,

                "action_support_distance":
                    action_distance,

                "action_support_minus_context":
                    (
                        action_distance
                        - context_distance
                    ),

                "predicted_action_loss":
                    predicted_action_loss,

                "predicted_relative_loss":
                    predicted_relative_loss,
            }
        )

    return output


def population_summary(
    rows,
):
    output = []

    for population in [
        POPULATION_EARLY,
        POPULATION_LATE,
    ]:
        matching = [
            row
            for row in rows
            if row[
                "population"
            ]
            == population
        ]

        for action in [
            1,
            2,
        ]:
            action_rows = [
                row
                for row in matching
                if row[
                    "action"
                ]
                == action
            ]

            harmful = sum(
                row[
                    "harmful_target"
                ]
                for row in action_rows
            )

            output.append(
                {
                    "record_type":
                        "population_action_summary",

                    "population":
                        population,

                    "action":
                        action,

                    "rows":
                        len(
                            action_rows
                        ),

                    "harmful":
                        harmful,

                    "beneficial":
                        (
                            len(
                                action_rows
                            )
                            - harmful
                        ),

                    "harmful_rate":
                        (
                            harmful
                            / len(
                                action_rows
                            )
                            if action_rows
                            else float(
                                "nan"
                            )
                        ),
                }
            )

    return output


def reciprocal_action_prediction(
    rows,
):
    output = []
    coefficients = []

    for held_out_population in [
        POPULATION_EARLY,
        POPULATION_LATE,
    ]:
        training_rows = [
            row
            for row in rows
            if row[
                "population"
            ]
            != held_out_population
        ]

        test_rows = [
            row
            for row in rows
            if row[
                "population"
            ]
            == held_out_population
        ]

        x_train = build_matrix(
            training_rows,
            GEOMETRY_FEATURES,
        )

        y_train = build_labels(
            training_rows,
            "action2_indicator",
        )

        x_test = build_matrix(
            test_rows,
            GEOMETRY_FEATURES,
        )

        y_test = build_labels(
            test_rows,
            "action2_indicator",
        )

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
                    "action_prediction_fold",

                "held_out_population":
                    held_out_population,

                "training_rows":
                    len(
                        training_rows
                    ),

                "test_rows":
                    len(
                        test_rows
                    ),

                "roc_auc":
                    auc,
            }
        )

        classifier = model.named_steps[
            "classifier"
        ]

        for feature, coefficient in zip(
            GEOMETRY_FEATURES,
            classifier.coef_[
                0
            ],
        ):
            coefficients.append(
                {
                    "record_type":
                        "action_prediction_coefficient",

                    "held_out_population":
                        held_out_population,

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


def reciprocal_harm_models(
    rows,
):
    model_specs = {
        "geometry_only":
            GEOMETRY_FEATURES,

        "action_only": [
            "action2_indicator",
        ],

        "geometry_plus_action":
            (
                GEOMETRY_FEATURES
                + [
                    "action2_indicator",
                ]
            ),
    }

    fold_rows = []
    coefficient_rows = []

    for model_name, features in model_specs.items():

        for held_out_population in [
            POPULATION_EARLY,
            POPULATION_LATE,
        ]:
            training_rows = [
                row
                for row in rows
                if row[
                    "population"
                ]
                != held_out_population
            ]

            test_rows = [
                row
                for row in rows
                if row[
                    "population"
                ]
                == held_out_population
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

            fold_rows.append(
                {
                    "record_type":
                        "harm_model_fold",

                    "model":
                        model_name,

                    "held_out_population":
                        held_out_population,

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
                        auc,
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
                            "harm_model_coefficient",

                        "model":
                            model_name,

                        "held_out_population":
                            held_out_population,

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
                    "harm_model_summary",

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
        "CROSS-POPULATION ACTION-STATE HARM DECOMPOSITION"
    )

    print(
        "=" * 210
    )

    print(
        f"frozen geometry features="
        f"{GEOMETRY_FEATURES}"
    )

    print()

    early_rows = early_population()

    late_rows = late_population()

    rows = (
        early_rows
        + late_rows
    )

    print(
        "JOINED CROSS-POPULATION DATA"
    )

    print(
        f"early rows="
        f"{len(early_rows)}"
    )

    print(
        f"later rows="
        f"{len(late_rows)}"
    )

    print(
        f"total rows="
        f"{len(rows)}"
    )

    print(
        f"total harmful="
        f"{sum(row['harmful_target'] for row in rows)}"
    )

    print()

    population_rows = population_summary(
        rows
    )

    print(
        "POPULATION ACTION-HARM SUMMARY"
    )

    for population in [
        POPULATION_EARLY,
        POPULATION_LATE,
    ]:
        print()

        print(
            population
        )

        matching = [
            row
            for row in population_rows
            if row[
                "population"
            ]
            == population
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
                f"harmful_rate="
                f"{row['harmful_rate']:.3%}"
            )

    (
        action_fold_rows,
        action_coefficient_rows,
    ) = reciprocal_action_prediction(
        rows
    )

    print()

    print(
        "CAN PRE-ACTION GEOMETRY PREDICT ACTION IDENTITY?"
    )

    for row in action_fold_rows:
        print(
            f"held_out="
            f"{row['held_out_population']:<20} "
            f"train_rows="
            f"{row['training_rows']} "
            f"test_rows="
            f"{row['test_rows']} "
            f"AUC="
            f"{row['roc_auc']:.3f}"
        )

    action_aucs = [
        float(
            row[
                "roc_auc"
            ]
        )
        for row in action_fold_rows
    ]

    print(
        f"mean action-prediction AUC="
        f"{statistics.mean(action_aucs):.3f}"
    )

    print(
        f"minimum action-prediction AUC="
        f"{min(action_aucs):.3f}"
    )

    (
        harm_fold_rows,
        harm_coefficient_rows,
    ) = reciprocal_harm_models(
        rows
    )

    harm_summary_rows = (
        summarize_harm_models(
            harm_fold_rows
        )
    )

    print()

    print(
        "RECIPROCAL POPULATION-HELD-OUT HARM MODELS"
    )

    for row in harm_summary_rows:
        print(
            f"{row['model']:<24} "
            f"mean_AUC="
            f"{row['mean_auc']:.3f} "
            f"min_AUC="
            f"{row['min_auc']:.3f} "
            f"max_AUC="
            f"{row['max_auc']:.3f}"
        )

    geometry_summary = next(
        row
        for row in harm_summary_rows
        if row[
            "model"
        ]
        == "geometry_only"
    )

    action_summary = next(
        row
        for row in harm_summary_rows
        if row[
            "model"
        ]
        == "action_only"
    )

    combined_summary = next(
        row
        for row in harm_summary_rows
        if row[
            "model"
        ]
        == "geometry_plus_action"
    )

    print()

    print(
        "ACTION VALUE-ADD AFTER GEOMETRY"
    )

    print(
        f"geometry_only mean AUC="
        f"{geometry_summary['mean_auc']:.3f}"
    )

    print(
        f"action_only mean AUC="
        f"{action_summary['mean_auc']:.3f}"
    )

    print(
        f"geometry_plus_action mean AUC="
        f"{combined_summary['mean_auc']:.3f}"
    )

    print(
        f"dMeanAUC vs geometry="
        f"{combined_summary['mean_auc'] - geometry_summary['mean_auc']:+.3f}"
    )

    print(
        f"dMinAUC vs geometry="
        f"{combined_summary['min_auc'] - geometry_summary['min_auc']:+.3f}"
    )

    coefficient_summary_rows = (
        coefficient_stability(
            harm_coefficient_rows
        )
    )

    print()

    print(
        "HARM-MODEL COEFFICIENT STABILITY"
    )

    for row in coefficient_summary_rows:
        print(
            f"{row['model']:<24} "
            f"{row['feature']:<38} "
            f"mean_coef="
            f"{row['mean_coefficient']:+.3f} "
            f"abs_coef="
            f"{row['mean_absolute_coefficient']:.3f} "
            f"sign_stability="
            f"{row['sign_stability']:.3%}"
        )

    action_adjusted = [
        row
        for row in coefficient_summary_rows
        if (
            row[
                "model"
            ]
            == "geometry_plus_action"
            and row[
                "feature"
            ]
            == "action2_indicator"
        )
    ]

    if action_adjusted:
        row = action_adjusted[
            0
        ]

        print()

        print(
            "ADJUSTED ACTION EFFECT"
        )

        print(
            f"action2 mean coefficient="
            f"{row['mean_coefficient']:+.3f}"
        )

        print(
            f"action2 sign stability="
            f"{row['sign_stability']:.3%}"
        )

    print()

    print(
        "INTERPRETATION NOTE"
    )

    print(
        "Experiment 117 uses the same frozen five-variable "
        "pre-action support/loss geometry in two non-overlapping "
        "historical populations."
    )

    print(
        "The early population uses its existing action-conditioned "
        "geometry fields. The later population is joined to the "
        "previously reconstructed 44071-44110 action-context geometry."
    )

    print(
        "No realized regret, realized loss, harmful label, or other "
        "post-outcome quantity enters the geometry representation."
    )

    print(
        "The central test is whether action identity retains "
        "population-held-out harm information after adjustment for "
        "the common observable pre-action geometry."
    )

    print(
        "No operating threshold, prospective seed, action-specific "
        "veto, or controller modification is introduced."
    )

    print(
        "=" * 210
    )

    summary_rows = []

    summary_rows.extend(
        population_rows
    )

    summary_rows.extend(
        action_fold_rows
    )

    summary_rows.extend(
        harm_summary_rows
    )

    summary_rows.extend(
        harm_fold_rows
    )

    summary_rows.extend(
        coefficient_summary_rows
    )

    save_csv(
        SUMMARY_OUTPUT_PATH,
        summary_rows,
    )

    save_csv(
        EVENT_OUTPUT_PATH,
        rows,
    )

    save_csv(
        COEFFICIENT_OUTPUT_PATH,
        (
            action_coefficient_rows
            + harm_coefficient_rows
            + coefficient_summary_rows
        ),
    )

    print(
        f"Summary saved to: "
        f"{SUMMARY_OUTPUT_PATH}"
    )

    print(
        f"Cross-population events saved to: "
        f"{EVENT_OUTPUT_PATH}"
    )

    print(
        f"Coefficient results saved to: "
        f"{COEFFICIENT_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()