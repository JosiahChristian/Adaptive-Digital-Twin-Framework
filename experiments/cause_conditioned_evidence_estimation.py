import csv
import itertools
from pathlib import Path


INPUT_PATH = Path(
    "results/balanced_evidence_boundary_sampling.csv"
)

OUTPUT_PATH = Path(
    "results/cause_conditioned_evidence_estimation.csv"
)


FEATURES_BY_CLASS = {
    "measurement_noise": [
        "classification_margin",
        "score_spread",
        "post_cumulative_abs_parameter_update",
    ],

    "process_disturbance": [
        "classification_margin",
        "score_spread",
        "event_max_nis",
        "delta_event_vs_pre_nis",
        "recovery_ratio_nis",
    ],

    "parameter_mismatch": [
        "classification_margin",
        "score_spread",
    ],

    "structural_change": [
        "parameter_shift_post_vs_pre",
        "score_spread",
        "classification_margin",
        "post_cumulative_abs_parameter_update",
        "delta_event_vs_pre_nis",
    ],
}


def load_rows() -> list[dict]:

    with INPUT_PATH.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def truth(
    row: dict,
) -> bool:

    return (
        row["evidence_sufficient"]
        == "True"
    )


def quantile_thresholds(
    values: list[float],
) -> list[float]:

    ordered = sorted(
        values
    )

    fractions = [
        0.10,
        0.20,
        0.30,
        0.40,
        0.50,
        0.60,
        0.70,
        0.80,
        0.90,
    ]

    thresholds = []

    for fraction in fractions:

        index = round(
            fraction
            * (
                len(ordered) - 1
            )
        )

        thresholds.append(
            ordered[index]
        )

    return sorted(
        set(
            thresholds
        )
    )


def predicate(
    value: float,
    *,
    direction: str,
    threshold: float,
) -> bool:

    if direction == ">=":
        return (
            value
            >= threshold
        )

    if direction == "<=":
        return (
            value
            <= threshold
        )

    raise ValueError(
        f"Unknown direction: "
        f"{direction}"
    )


def evaluate_predictions(
    rows: list[dict],
    predictions: list[bool],
) -> dict:

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for row, prediction in zip(
        rows,
        predictions,
    ):

        actual = truth(
            row
        )

        if prediction and actual:
            tp += 1

        elif (
            not prediction
            and not actual
        ):
            tn += 1

        elif prediction:
            fp += 1

        else:
            fn += 1

    accuracy = (
        (tp + tn)
        / len(rows)
    )

    precision = (
        tp
        / (tp + fp)
        if tp + fp
        else 0.0
    )

    recall = (
        tp
        / (tp + fn)
        if tp + fn
        else 0.0
    )

    specificity = (
        tn
        / (tn + fp)
        if tn + fp
        else 0.0
    )

    balanced_accuracy = (
        (
            recall
            + specificity
        )
        / 2.0
    )

    return {
        "accuracy":
            accuracy,

        "balanced_accuracy":
            balanced_accuracy,

        "precision":
            precision,

        "recall":
            recall,

        "specificity":
            specificity,

        "tp":
            tp,

        "tn":
            tn,

        "fp":
            fp,

        "fn":
            fn,
    }


def candidate_sort_key(
    candidate: dict,
):

    return (
        candidate[
            "balanced_accuracy"
        ],
        candidate[
            "accuracy"
        ],
        min(
            candidate[
                "precision"
            ],
            candidate[
                "recall"
            ],
        ),
        candidate[
            "precision"
        ],
        candidate[
            "recall"
        ],
    )


def search_single_feature(
    rows: list[dict],
    *,
    feature: str,
) -> list[dict]:

    values = [
        float(
            row[feature]
        )
        for row in rows
    ]

    thresholds = (
        quantile_thresholds(
            values
        )
    )

    candidates = []

    for direction in [
        ">=",
        "<=",
    ]:

        for threshold in thresholds:

            predictions = [
                predicate(
                    float(
                        row[feature]
                    ),
                    direction=direction,
                    threshold=threshold,
                )
                for row in rows
            ]

            metrics = (
                evaluate_predictions(
                    rows,
                    predictions,
                )
            )

            candidates.append(
                {
                    "rule_type":
                        "single",

                    "feature_1":
                        feature,

                    "direction_1":
                        direction,

                    "threshold_1":
                        threshold,

                    "feature_2":
                        "",

                    "direction_2":
                        "",

                    "threshold_2":
                        "",

                    **metrics,
                }
            )

    return candidates


def search_feature_pair(
    rows: list[dict],
    *,
    feature_1: str,
    feature_2: str,
) -> list[dict]:

    values_1 = [
        float(
            row[feature_1]
        )
        for row in rows
    ]

    values_2 = [
        float(
            row[feature_2]
        )
        for row in rows
    ]

    thresholds_1 = (
        quantile_thresholds(
            values_1
        )
    )

    thresholds_2 = (
        quantile_thresholds(
            values_2
        )
    )

    candidates = []

    for direction_1 in [
        ">=",
        "<=",
    ]:

        for direction_2 in [
            ">=",
            "<=",
        ]:

            for threshold_1 in (
                thresholds_1
            ):

                for threshold_2 in (
                    thresholds_2
                ):

                    predictions = []

                    for row in rows:

                        first = (
                            predicate(
                                float(
                                    row[
                                        feature_1
                                    ]
                                ),
                                direction=(
                                    direction_1
                                ),
                                threshold=(
                                    threshold_1
                                ),
                            )
                        )

                        second = (
                            predicate(
                                float(
                                    row[
                                        feature_2
                                    ]
                                ),
                                direction=(
                                    direction_2
                                ),
                                threshold=(
                                    threshold_2
                                ),
                            )
                        )

                        predictions.append(
                            first
                            and second
                        )

                    metrics = (
                        evaluate_predictions(
                            rows,
                            predictions,
                        )
                    )

                    candidates.append(
                        {
                            "rule_type":
                                "pair",

                            "feature_1":
                                feature_1,

                            "direction_1":
                                direction_1,

                            "threshold_1":
                                threshold_1,

                            "feature_2":
                                feature_2,

                            "direction_2":
                                direction_2,

                            "threshold_2":
                                threshold_2,

                            **metrics,
                        }
                    )

    return candidates


def search_class(
    rows: list[dict],
    *,
    class_name: str,
) -> list[dict]:

    class_rows = [
        row
        for row in rows
        if row["true_class"]
        == class_name
    ]

    features = (
        FEATURES_BY_CLASS[
            class_name
        ]
    )

    single_candidates = []

    for feature in features:

        single_candidates.extend(
            search_single_feature(
                class_rows,
                feature=feature,
            )
        )

    pair_candidates = []

    for (
        feature_1,
        feature_2,
    ) in itertools.combinations(
        features,
        2,
    ):

        pair_candidates.extend(
            search_feature_pair(
                class_rows,
                feature_1=feature_1,
                feature_2=feature_2,
            )
        )

    best_single = max(
        single_candidates,
        key=candidate_sort_key,
    )

    best_pair = max(
        pair_candidates,
        key=candidate_sort_key,
    )

    return [
        {
            "cause":
                class_name,
            **best_single,
        },
        {
            "cause":
                class_name,
            **best_pair,
        },
    ]


def run_experiment() -> list[dict]:

    rows = load_rows()

    results = []

    for class_name in (
        FEATURES_BY_CLASS
    ):

        results.extend(
            search_class(
                rows,
                class_name=(
                    class_name
                ),
            )
        )

    return results


def save_results(
    rows: list[dict],
) -> None:

    OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(
            rows
        )


def rule_text(
    row: dict,
) -> str:

    first = (
        f"{row['feature_1']} "
        f"{row['direction_1']} "
        f"{float(row['threshold_1']):.6f}"
    )

    if (
        row["rule_type"]
        == "single"
    ):
        return first

    second = (
        f"{row['feature_2']} "
        f"{row['direction_2']} "
        f"{float(row['threshold_2']):.6f}"
    )

    return (
        f"{first} AND "
        f"{second}"
    )


def print_summary(
    rows: list[dict],
) -> None:

    print("=" * 120)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "CAUSE-CONDITIONED EVIDENCE ESTIMATION"
    )

    print("=" * 120)

    for cause in (
        FEATURES_BY_CLASS
    ):

        print(
            f"\n{cause}"
        )

        cause_rows = [
            row
            for row in rows
            if row["cause"]
            == cause
        ]

        for row in cause_rows:

            print(
                f"  "
                f"{row['rule_type']:<7}"
                f"acc="
                f"{row['accuracy']:.3%} "
                f"bal_acc="
                f"{row['balanced_accuracy']:.3%} "
                f"precision="
                f"{row['precision']:.3%} "
                f"recall="
                f"{row['recall']:.3%} "
                f"FP="
                f"{row['fp']:<3} "
                f"FN="
                f"{row['fn']:<3}"
            )

            print(
                f"           "
                f"{rule_text(row)}"
            )

    print("=" * 120)


def main() -> None:

    rows = run_experiment()

    save_results(
        rows
    )

    print_summary(
        rows
    )

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()