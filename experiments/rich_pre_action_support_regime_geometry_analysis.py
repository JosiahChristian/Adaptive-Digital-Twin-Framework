import csv
import math
import statistics
from collections import Counter
from pathlib import Path

import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RESULTS_DIR = Path(
    "results"
)

SUPPORT_EVENT_PATH = (
    RESULTS_DIR
    / "cross_block_constituent_stability_analysis_events.csv"
)

SEVERE_PROXY_EVENT_PATH = (
    RESULTS_DIR
    / "frozen_pre_action_calibration_proxy_support_expansion_transfer_events.csv"
)

SUMMARY_OUTPUT_PATH = (
    RESULTS_DIR
    / "rich_pre_action_support_regime_geometry_analysis.csv"
)

EVENT_OUTPUT_PATH = (
    RESULTS_DIR
    / "rich_pre_action_support_regime_geometry_analysis_events.csv"
)

COEFFICIENT_OUTPUT_PATH = (
    RESULTS_DIR
    / "rich_pre_action_support_regime_geometry_analysis_coefficients.csv"
)


BLOCK_A = "block_071_090"
BLOCK_B = "block_091_110"

SEVERE_PROXY_MODEL = "severe_proxy_only"

RANDOM_STATE = 42

FLOAT_TOLERANCE = 1e-12


PRIMARY_REGIME_FEATURES = [
    "context_support_distance",
    "action_support_distance",
    "action_support_minus_context",
    "predicted_action_loss",
    "predicted_relative_loss",
]


RICH_SOURCE_REQUIRED_COLUMNS = {
    "generation_seed",
    "test_index",
    "action",
    *PRIMARY_REGIME_FEATURES,
}


def read_csv(
    path,
):
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


def read_header(
    path,
):
    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.reader(
            file
        )

        try:
            return next(
                reader
            )

        except StopIteration:
            return []


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


def support_key(
    row,
):
    return (
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


def rich_key(
    row,
):
    return (
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


def proxy_key(
    row,
):
    return (
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


def candidate_rich_source_files():
    candidates = []

    for path in sorted(
        RESULTS_DIR.glob(
            "*.csv"
        )
    ):
        if path in {
            SUMMARY_OUTPUT_PATH,
            EVENT_OUTPUT_PATH,
            COEFFICIENT_OUTPUT_PATH,
        }:
            continue

        header = set(
            read_header(
                path
            )
        )

        if RICH_SOURCE_REQUIRED_COLUMNS.issubset(
            header
        ):
            candidates.append(
                path
            )

    return candidates


def score_candidate_source(
    path,
    support_keys,
):
    rows = read_csv(
        path
    )

    available_keys = {
        rich_key(
            row
        )
        for row in rows
    }

    matched = sum(
        int(
            key
            in available_keys
        )
        for key in support_keys
    )

    preferred_name_bonus = int(
        "action_conditioned_support"
        in path.name
    )

    return (
        matched,
        preferred_name_bonus,
        -len(
            path.name
        ),
    )


def discover_rich_source(
    support_rows,
):
    candidates = candidate_rich_source_files()

    if not candidates:
        raise FileNotFoundError(
            "No results CSV contains the required rich "
            "pre-action action/support geometry columns: "
            f"{sorted(RICH_SOURCE_REQUIRED_COLUMNS)}"
        )

    support_keys = {
        support_key(
            row
        )
        for row in support_rows
    }

    scored = []

    for path in candidates:
        score = score_candidate_source(
            path,
            support_keys,
        )

        scored.append(
            (
                score,
                path,
            )
        )

    scored.sort(
        key=lambda item:
            item[
                0
            ],
        reverse=True,
    )

    best_score, best_path = scored[
        0
    ]

    matched = best_score[
        0
    ]

    print(
        "RICH SOURCE DISCOVERY"
    )

    for score, path in scored:
        print(
            f"candidate={path} "
            f"matched_support_events="
            f"{score[0]}/"
            f"{len(support_keys)}"
        )

    print()

    print(
        f"selected rich source="
        f"{best_path}"
    )

    print(
        f"coverage="
        f"{matched}/"
        f"{len(support_keys)}"
    )

    if matched != len(
        support_keys
    ):
        raise RuntimeError(
            "Best rich pre-action source does not cover "
            "all support-expansion events. "
            f"Coverage={matched}/{len(support_keys)}. "
            "Experiment 114 will not proceed with a partial join."
        )

    return best_path


def build_severe_proxy_lookup():
    rows = read_csv(
        SEVERE_PROXY_EVENT_PATH
    )

    lookup = {}

    for row in rows:
        if row.get(
            "model",
            "",
        ) != SEVERE_PROXY_MODEL:
            continue

        key = proxy_key(
            row
        )

        probability = as_float(
            row,
            "severe_underestimation_probability",
        )

        if math.isfinite(
            probability
        ):
            lookup[
                key
            ] = probability

    return lookup


def join_population():
    support_rows = read_csv(
        SUPPORT_EVENT_PATH
    )

    rich_source = discover_rich_source(
        support_rows
    )

    rich_rows = read_csv(
        rich_source
    )

    rich_lookup = {}

    for row in rich_rows:
        key = rich_key(
            row
        )

        if key not in rich_lookup:
            rich_lookup[
                key
            ] = row

    severe_proxy_lookup = (
        build_severe_proxy_lookup()
    )

    output = []

    missing_rich = []
    missing_proxy = []

    for support_row in support_rows:
        key = support_key(
            support_row
        )

        rich_row = rich_lookup.get(
            key
        )

        if rich_row is None:
            missing_rich.append(
                key
            )
            continue

        if key not in severe_proxy_lookup:
            missing_proxy.append(
                key
            )
            continue

        copy = dict(
            support_row
        )

        for feature in PRIMARY_REGIME_FEATURES:
            value = as_float(
                rich_row,
                feature,
            )

            if not math.isfinite(
                value
            ):
                raise ValueError(
                    f"Non-finite {feature} "
                    f"for support event {key}"
                )

            copy[
                feature
            ] = value

        copy[
            "severe_underestimation_probability"
        ] = float(
            severe_proxy_lookup[
                key
            ]
        )

        copy[
            "harmful_target"
        ] = int(
            copy.get(
                "class",
                "",
            )
            == "harmful"
        )

        copy[
            "regime_target"
        ] = int(
            copy[
                "block"
            ]
            == BLOCK_B
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
            "rich_source_file"
        ] = str(
            rich_source
        )

        output.append(
            copy
        )

    if missing_rich:
        raise RuntimeError(
            "Rich geometry join failed. "
            f"Missing {len(missing_rich)} events. "
            f"First missing key={missing_rich[0]}"
        )

    if missing_proxy:
        raise RuntimeError(
            "Frozen severe-proxy join failed. "
            f"Missing {len(missing_proxy)} events. "
            f"First missing key={missing_proxy[0]}"
        )

    if len(
        output
    ) != len(
        support_rows
    ):
        raise RuntimeError(
            "Joined population is incomplete."
        )

    return (
        output,
        rich_source,
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


def univariate_regime_geometry(
    rows,
):
    output = []

    for feature in PRIMARY_REGIME_FEATURES:
        block_a = [
            float(
                row[
                    feature
                ]
            )
            for row in rows
            if row[
                "block"
            ]
            == BLOCK_A
        ]

        block_b = [
            float(
                row[
                    feature
                ]
            )
            for row in rows
            if row[
                "block"
            ]
            == BLOCK_B
        ]

        labels = np.asarray(
            [
                0
            ]
            * len(
                block_a
            )
            + [
                1
            ]
            * len(
                block_b
            ),
            dtype=int,
        )

        values = np.asarray(
            block_a
            + block_b,
            dtype=float,
        )

        auc = safe_auc(
            labels,
            values,
        )

        output.append(
            {
                "record_type":
                    "univariate_regime_geometry",

                "feature":
                    feature,

                "block_a_mean":
                    statistics.mean(
                        block_a
                    ),

                "block_b_mean":
                    statistics.mean(
                        block_b
                    ),

                "difference_b_minus_a":
                    (
                        statistics.mean(
                            block_b
                        )
                        - statistics.mean(
                            block_a
                        )
                    ),

                "regime_auc_b_high":
                    auc,

                "best_orientation_auc":
                    max(
                        auc,
                        1.0
                        - auc
                    ),
            }
        )

    return output


def action_distribution_diagnostics(
    rows,
):
    output = []

    actions = sorted(
        {
            int(
                row[
                    "support_baseline_action"
                ]
            )
            for row in rows
        }
    )

    for block in [
        BLOCK_A,
        BLOCK_B,
    ]:
        block_rows = [
            row
            for row in rows
            if row[
                "block"
            ]
            == block
        ]

        counts = Counter(
            int(
                row[
                    "support_baseline_action"
                ]
            )
            for row in block_rows
        )

        for action in actions:
            count = counts.get(
                action,
                0,
            )

            output.append(
                {
                    "record_type":
                        "action_distribution",

                    "block":
                        block,

                    "action":
                        action,

                    "count":
                        count,

                    "fraction":
                        (
                            count
                            / len(
                                block_rows
                            )
                            if block_rows
                            else float(
                                "nan"
                            )
                        ),
                }
            )

    return output


def leave_one_seed_out_regime_model(
    rows,
):
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
    event_rows = []
    coefficient_rows = []

    for held_out_seed in seeds:
        training_rows = [
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
            training_rows,
            PRIMARY_REGIME_FEATURES,
        )

        y_train = build_labels(
            training_rows,
            "regime_target",
        )

        x_test = build_matrix(
            test_rows,
            PRIMARY_REGIME_FEATURES,
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

        predictions = (
            probabilities
            >= 0.50
        ).astype(
            int
        )

        seed_accuracy = float(
            np.mean(
                predictions
                == y_test
            )
        )

        fold_rows.append(
            {
                "record_type":
                    "regime_seed_fold",

                "held_out_seed":
                    held_out_seed,

                "true_regime":
                    int(
                        y_test[
                            0
                        ]
                    ),

                "test_rows":
                    len(
                        test_rows
                    ),

                "mean_regime_probability":
                    float(
                        np.mean(
                            probabilities
                        )
                    ),

                "classification_accuracy":
                    seed_accuracy,
            }
        )

        classifier = model.named_steps[
            "classifier"
        ]

        for feature, coefficient in zip(
            PRIMARY_REGIME_FEATURES,
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
            event = {
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

                "block":
                    row[
                        "block"
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

                "severe_underestimation_probability":
                    float(
                        row[
                            "severe_underestimation_probability"
                        ]
                    ),
            }

            for feature in PRIMARY_REGIME_FEATURES:
                event[
                    feature
                ] = float(
                    row[
                        feature
                    ]
                )

            event_rows.append(
                event
            )

    return (
        fold_rows,
        event_rows,
        coefficient_rows,
    )


def aggregate_regime_metrics(
    event_rows,
    fold_rows,
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

    probabilities = np.asarray(
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

    predictions = (
        probabilities
        >= 0.50
    ).astype(
        int
    )

    return {
        "record_type":
            "regime_identification_summary",

        "pooled_loso_auc":
            safe_auc(
                y_true,
                probabilities,
            ),

        "pooled_accuracy":
            float(
                np.mean(
                    predictions
                    == y_true
                )
            ),

        "mean_seed_accuracy":
            statistics.mean(
                float(
                    row[
                        "classification_accuracy"
                    ]
                )
                for row in fold_rows
        ),
    }


def coefficient_stability(
    coefficient_rows,
):
    output = []

    for feature in PRIMARY_REGIME_FEATURES:
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

        if not values:
            continue

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


def harm_modulation_models(
    regime_event_rows,
):
    rows = [
        dict(
            row
        )
        for row in regime_event_rows
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

        "rich_regime_only": [
            "regime_probability",
        ],

        "proxy_plus_rich_regime": [
            "severe_underestimation_probability",
            "regime_probability",
        ],

        "proxy_rich_regime_interaction": [
            "severe_underestimation_probability",
            "regime_probability",
            "proxy_x_regime",
        ],
    }

    fold_rows = []
    coefficient_rows = []

    for model_name, features in model_specs.items():

        for held_out_block in [
            BLOCK_A,
            BLOCK_B,
        ]:
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

            fold_rows.append(
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
                coefficient_rows.append(
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
        "RICH PRE-ACTION SUPPORT REGIME GEOMETRY ANALYSIS"
    )

    print(
        "=" * 210
    )

    print(
        f"primary regime features="
        f"{PRIMARY_REGIME_FEATURES}"
    )

    print()

    (
        rows,
        rich_source,
    ) = join_population()

    print()

    print(
        "JOINED POPULATION"
    )

    print(
        f"rows="
        f"{len(rows)}"
    )

    print(
        f"rich source="
        f"{rich_source}"
    )

    print(
        f"block A rows="
        f"{sum(row['block'] == BLOCK_A for row in rows)}"
    )

    print(
        f"block B rows="
        f"{sum(row['block'] == BLOCK_B for row in rows)}"
    )

    print(
        f"harmful="
        f"{sum(row['harmful_target'] for row in rows)}"
    )

    print(
        f"beneficial="
        f"{sum(1 - row['harmful_target'] for row in rows)}"
    )

    geometry_rows = univariate_regime_geometry(
        rows
    )

    print()

    print(
        "UNIVARIATE RICH PRE-ACTION REGIME GEOMETRY"
    )

    for row in geometry_rows:
        print(
            f"{row['feature']:<38} "
            f"A_mean="
            f"{row['block_a_mean']:.6f} "
            f"B_mean="
            f"{row['block_b_mean']:.6f} "
            f"delta="
            f"{row['difference_b_minus_a']:+.6f} "
            f"best_orientation_AUC="
            f"{row['best_orientation_auc']:.3f}"
        )

    action_rows = (
        action_distribution_diagnostics(
            rows
        )
    )

    print()

    print(
        "SECONDARY ACTION-IDENTITY DIAGNOSTIC"
    )

    for block in [
        BLOCK_A,
        BLOCK_B,
    ]:
        print()

        print(
            block
        )

        matching = [
            row
            for row in action_rows
            if row[
                "block"
            ]
            == block
        ]

        for row in matching:
            print(
                f"  action="
                f"{row['action']} "
                f"count="
                f"{row['count']} "
                f"fraction="
                f"{row['fraction']:.3%}"
            )

    (
        regime_fold_rows,
        regime_event_rows,
        regime_coefficient_rows,
    ) = leave_one_seed_out_regime_model(
        rows
    )

    regime_summary = (
        aggregate_regime_metrics(
            regime_event_rows,
            regime_fold_rows,
        )
    )

    coefficient_summary_rows = (
        coefficient_stability(
            regime_coefficient_rows
        )
    )

    print()

    print(
        "RICH PRE-ACTION REGIME IDENTIFICATION"
    )

    print(
        f"pooled LOSO regime AUC="
        f"{regime_summary['pooled_loso_auc']:.3f}"
    )

    print(
        f"pooled classification accuracy="
        f"{regime_summary['pooled_accuracy']:.3%}"
    )

    print(
        f"mean seed accuracy="
        f"{regime_summary['mean_seed_accuracy']:.3%}"
    )

    print()

    print(
        "REGIME COEFFICIENT STABILITY"
    )

    for row in coefficient_summary_rows:
        print(
            f"{row['feature']:<38} "
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
    ) = harm_modulation_models(
        regime_event_rows
    )

    harm_summary_rows = (
        summarize_harm_models(
            harm_fold_rows
        )
    )

    print()

    print(
        "RISK-TO-HARM MODULATION"
    )

    for row in harm_summary_rows:
        print(
            f"{row['model']:<34} "
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
        == "proxy_rich_regime_interaction"
    )

    print()

    print(
        "RICH REGIME INTERACTION VALUE-ADD"
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
        "Experiment 114 freezes a five-variable rich pre-action "
        "support/action geometry before observing regime-performance "
        "results."
    )

    print(
        "The primary representation contains context support distance, "
        "action support distance, support-minus-context distance, "
        "predicted action loss, and predicted relative loss."
    )

    print(
        "Realized regret, realized loss, loss error, harmful class, "
        "true-best action, and other outcome-derived variables are "
        "excluded from regime construction."
    )

    print(
        "Action identity is reported only as a secondary structural "
        "diagnostic and is not included in the primary continuous "
        "regime classifier."
    )

    print(
        "The regime score is evaluated first as a block-identification "
        "representation and only afterward as a diagnostic modifier "
        "of the frozen severe-proxy-to-harm mapping."
    )

    print(
        "No operating threshold, new prospective seed, or controller "
        "modification is introduced."
    )

    print(
        "=" * 210
    )

    summary_rows = []

    summary_rows.extend(
        geometry_rows
    )

    summary_rows.extend(
        action_rows
    )

    summary_rows.append(
        regime_summary
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