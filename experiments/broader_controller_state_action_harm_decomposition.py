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
    "cross_population_action_state_harm_decomposition_events.csv"
)

SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "broader_controller_state_action_harm_decomposition.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "broader_controller_state_action_harm_decomposition_events.csv"
)

COEFFICIENT_OUTPUT_PATH = Path(
    "results/"
    "broader_controller_state_action_harm_decomposition_coefficients.csv"
)


POPULATION_EARLY = "population_001_010"
POPULATION_LATE = "population_071_110"

RANDOM_STATE = 42


BROADER_STATE_FEATURES = [
    "context_benefit_probability",
    "context_release_probability",
    "context_anchor_age",
    "context_trigger_score",
    "context_feature_distance",
    "context_current_mismatch_indicator",
    "context_current_parameter_estimate",
    "predicted_under_risk",
    "predicted_primary_regret",
    "predicted_expanded_regret",
    "predicted_regret_margin",
]


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
        action = as_int(
            row,
            "expanded_action",
        )

        reconstructed_action = as_int(
            row,
            "expanded_action_reconstructed",
        )

        if action != reconstructed_action:
            raise RuntimeError(
                "Early action reconstruction mismatch."
            )

        if action not in {
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

        record = {
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
                action,

            "action2_indicator":
                int(
                    action
                    == 2
                ),

            "harmful_target":
                int(
                    outcome
                    == "harmful"
                ),
        }

        for feature in BROADER_STATE_FEATURES:
            value = as_float(
                row,
                feature,
            )

            if not math.isfinite(
                value
            ):
                raise RuntimeError(
                    f"Missing or non-finite early feature: {feature}"
                )

            record[
                feature
            ] = value

        output.append(
            record
        )

    return output


def late_state_source_candidates():
    candidates = []

    for path in Path(
        "results"
    ).glob(
        "*.csv"
    ):
        header = []

        try:
            with path.open(
                "r",
                newline="",
                encoding="utf-8",
            ) as file:
                reader = csv.reader(
                    file
                )

                header = next(
                    reader
                )

        except (
            StopIteration,
            OSError,
        ):
            continue

        required = {
            "generation_seed",
            "test_index",
            *BROADER_STATE_FEATURES,
        }

        if required.issubset(
            set(
                header
            )
        ):
            candidates.append(
                path
            )

    return sorted(
        candidates
    )


def late_population():
    all_event_rows = read_csv(
        LATE_EVENT_PATH
    )

    late_event_rows = [
        row
        for row in all_event_rows
        if row.get(
            "population",
            "",
        )
        == POPULATION_LATE
    ]

    if len(
        late_event_rows
    ) != 88:
        raise RuntimeError(
            "Unexpected later-population event count: "
            f"{len(late_event_rows)}; expected 88."
        )


    candidates = (
        late_state_source_candidates()
    )

    print(
        "LATE BROADER-STATE SOURCE DISCOVERY"
    )

    if not candidates:
        raise RuntimeError(
            "No later-population CSV contains the complete "
            "frozen broader controller-state feature set. "
            "Experiment 118 will not proceed with a partial "
            "or weakened state representation."
        )

    for path in candidates:
        print(
            f"candidate={path}"
        )

    target_keys = {
        (
            as_int(
                row,
                "generation_seed",
            ),
            as_int(
                row,
                "test_index",
            ),
        )
        for row in late_event_rows
    }

    scored = []

    for path in candidates:
        rows = read_csv(
            path
        )

        available = {
            (
                as_int(
                    row,
                    "generation_seed",
                ),
                as_int(
                    row,
                    "test_index",
                ),
            )
            for row in rows
        }

        matched = len(
            target_keys
            & available
        )

        scored.append(
            (
                matched,
                path,
            )
        )

        print(
            f"  matched="
            f"{matched}/"
            f"{len(target_keys)}"
        )

    scored.sort(
        key=lambda item:
            item[
                0
            ],
        reverse=True,
    )

    best_match_count, best_path = scored[
        0
    ]

    print()

    print(
        f"selected later state source="
        f"{best_path}"
    )

    print(
        f"coverage="
        f"{best_match_count}/"
        f"{len(target_keys)}"
    )

    if best_match_count != len(
        target_keys
    ):
        raise RuntimeError(
            "Later broader controller-state source does not "
            "cover all target support-expansion events. "
            "Experiment 118 will not proceed with partial coverage."
        )

    state_rows = read_csv(
        best_path
    )

    lookup = {}

    for row in state_rows:
        key = (
            as_int(
                row,
                "generation_seed",
            ),
            as_int(
                row,
                "test_index",
            ),
        )

        if key not in lookup:
            lookup[
                key
            ] = row

    output = []

    for row in late_event_rows:
        key = (
            as_int(
                row,
                "generation_seed",
            ),
            as_int(
                row,
                "test_index",
            ),
        )

        source = lookup.get(
            key
        )

        if source is None:
            raise RuntimeError(
                f"Missing later broader state for key={key}"
            )

        action = as_int(
            row,
            "action",
        )

        record = {
            "population":
                POPULATION_LATE,

            "generation_seed":
                key[
                    0
                ],

            "test_index":
                key[
                    1
                ],

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

            "late_state_source":
                str(
                    best_path
                ),
        }

        for feature in BROADER_STATE_FEATURES:
            value = as_float(
                source,
                feature,
            )

            if not math.isfinite(
                value
            ):
                raise RuntimeError(
                    f"Missing or non-finite later feature "
                    f"{feature} for key={key}"
                )

            record[
                feature
            ] = value

        output.append(
            record
        )

    return output


def reciprocal_action_prediction(
    rows,
):
    fold_rows = []
    coefficient_rows = []

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
            BROADER_STATE_FEATURES,
        )

        y_train = build_labels(
            training_rows,
            "action2_indicator",
        )

        x_test = build_matrix(
            test_rows,
            BROADER_STATE_FEATURES,
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

        fold_rows.append(
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
            BROADER_STATE_FEATURES,
            classifier.coef_[
                0
            ],
        ):
            coefficient_rows.append(
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
        fold_rows,
        coefficient_rows,
    )


def reciprocal_harm_models(
    rows,
):
    model_specs = {
        "broader_state_only":
            BROADER_STATE_FEATURES,

        "action_only": [
            "action2_indicator",
        ],

        "broader_state_plus_action":
            (
                BROADER_STATE_FEATURES
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
        "BROADER CONTROLLER-STATE ACTION-HARM DECOMPOSITION"
    )

    print(
        "=" * 210
    )

    print(
        f"frozen broader state features="
        f"{BROADER_STATE_FEATURES}"
    )

    print()

    early_rows = early_population()

    late_rows = late_population()

    rows = (
        early_rows
        + late_rows
    )

    print()

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

    (
        action_fold_rows,
        action_coefficient_rows,
    ) = reciprocal_action_prediction(
        rows
    )

    print()

    print(
        "CAN BROADER PRE-ACTION STATE PREDICT ACTION IDENTITY?"
    )

    for row in action_fold_rows:
        print(
            f"held_out="
            f"{row['held_out_population']:<20} "
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
        summarize_models(
            harm_fold_rows
        )
    )

    print()

    print(
        "RECIPROCAL POPULATION-HELD-OUT HARM MODELS"
    )

    for row in harm_summary_rows:
        print(
            f"{row['model']:<28} "
            f"mean_AUC="
            f"{row['mean_auc']:.3f} "
            f"min_AUC="
            f"{row['min_auc']:.3f} "
            f"max_AUC="
            f"{row['max_auc']:.3f}"
        )

    state_summary = next(
        row
        for row in harm_summary_rows
        if row[
            "model"
        ]
        == "broader_state_only"
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
        == "broader_state_plus_action"
    )

    print()

    print(
        "ACTION VALUE-ADD AFTER BROADER STATE"
    )

    print(
        f"broader_state_only mean AUC="
        f"{state_summary['mean_auc']:.3f}"
    )

    print(
        f"action_only mean AUC="
        f"{action_summary['mean_auc']:.3f}"
    )

    print(
        f"broader_state_plus_action mean AUC="
        f"{combined_summary['mean_auc']:.3f}"
    )

    print(
        f"dMeanAUC vs broader state="
        f"{combined_summary['mean_auc'] - state_summary['mean_auc']:+.3f}"
    )

    print(
        f"dMinAUC vs broader state="
        f"{combined_summary['min_auc'] - state_summary['min_auc']:+.3f}"
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
            f"{row['model']:<28} "
            f"{row['feature']:<42} "
            f"mean_coef="
            f"{row['mean_coefficient']:+.3f} "
            f"abs_coef="
            f"{row['mean_absolute_coefficient']:.3f} "
            f"sign_stability="
            f"{row['sign_stability']:.3%}"
        )

    adjusted_action = [
        row
        for row in coefficient_summary_rows
        if (
            row[
                "model"
            ]
            == "broader_state_plus_action"
            and row[
                "feature"
            ]
            == "action2_indicator"
        )
    ]

    if adjusted_action:
        row = adjusted_action[
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
        "Experiment 118 freezes a broader pre-action controller-state "
        "representation before observing harm-model performance."
    )

    print(
        "The state representation includes controller probabilities, "
        "anchor/trigger context, mismatch/parameter state, predicted "
        "under-risk, and predicted regret quantities."
    )

    print(
        "Realized regret, realized loss, harmful label, and other "
        "post-outcome quantities are excluded from the state model."
    )

    print(
        "The central test is whether action identity retains "
        "population-held-out harmful-expansion information after "
        "adjustment for this broader controller state."
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