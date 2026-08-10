import csv
from pathlib import Path


GLOBAL_PATH = Path(
    "results/residual_attribution_baseline.csv"
)

TEMPORAL_PATH = Path(
    "results/temporal_residual_attribution.csv"
)

ADAPTATION_PATH = Path(
    "results/adaptation_response_attribution.csv"
)

OUTPUT_PATH = Path(
    "results/mismatch_classification.csv"
)


CLASS_NAMES = [
    "measurement_noise",
    "process_disturbance",
    "parameter_mismatch",
    "structural_change",
]


def load_csv(
    path: Path,
) -> list[dict]:

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def index_by_regime_seed(
    rows: list[dict],
) -> dict:

    return {
        (
            row["regime"],
            int(row["seed"]),
        ): row
        for row in rows
    }


def value(
    row: dict,
    field: str,
) -> float:

    return float(
        row[field]
    )


def normalize_score(
    score: float,
) -> float:

    return max(
        0.0,
        score,
    )


def classify_row(
    *,
    regime: str,
    global_row: dict,
    temporal_row: dict,
    adaptation_row: dict | None,
) -> dict:

    mean_abs_innovation = value(
        global_row,
        "mean_absolute_innovation",
    )

    mean_nis = value(
        global_row,
        "mean_nis",
    )

    longest_run = value(
        global_row,
        "longest_nis_run_above_1",
    )

    autocorrelation = value(
        global_row,
        "innovation_lag1_autocorrelation",
    )

    event_nis_rise = value(
        temporal_row,
        "delta_event_vs_pre_nis",
    )

    recovery_ratio = value(
        temporal_row,
        "recovery_ratio_nis",
    )

    event_max_nis = value(
        temporal_row,
        "event_max_nis",
    )

    event_autocorrelation_rise = value(
        temporal_row,
        "delta_event_vs_pre_autocorrelation",
    )

    persistent_parameter_shift = 0.0
    post_parameter_activity = 0.0

    if adaptation_row is not None:

        persistent_parameter_shift = abs(
            value(
                adaptation_row,
                "parameter_shift_post_vs_pre",
            )
        )

        post_parameter_activity = value(
            adaptation_row,
            "post_cumulative_abs_parameter_update",
        )

    measurement_noise_score = (
        2.0
        * max(
            0.0,
            mean_abs_innovation
            - 0.75,
        )
        +
        1.5
        * max(
            0.0,
            0.30
            - autocorrelation,
        )
        +
        max(
            0.0,
            8.0
            - longest_run,
        )
        / 8.0
        +
        max(
            0.0,
            0.50
            - abs(
                event_nis_rise
            ),
        )
    )

    process_disturbance_score = (
        1.5
        * max(
            0.0,
            event_nis_rise
            - 1.0,
        )
        +
        0.08
        * max(
            0.0,
            event_max_nis
            - 8.0,
        )
        +
        1.5
        * max(
            0.0,
            0.60
            - recovery_ratio,
        )
        +
        max(
            0.0,
            event_autocorrelation_rise
        )
        -
        8.0
        * persistent_parameter_shift
    )

    parameter_mismatch_score = (
        0.10
        * max(
            0.0,
            longest_run
            - 7.0,
        )
        +
        3.0
        * max(
            0.0,
            autocorrelation
            - 0.35,
        )
        +
        max(
            0.0,
            mean_nis
            - 1.4,
        )
        +
        max(
            0.0,
            0.75
            - abs(
                event_nis_rise
            ),
        )
    )

    structural_change_score = (
        12.0
        * persistent_parameter_shift
        +
        2.0
        * post_parameter_activity
        +
        max(
            0.0,
            event_nis_rise
            - 0.75,
        )
        +
        max(
            0.0,
            event_autocorrelation_rise
        )
    )

    scores = {
        "measurement_noise":
            normalize_score(
                measurement_noise_score
            ),

        "process_disturbance":
            normalize_score(
                process_disturbance_score
            ),

        "parameter_mismatch":
            normalize_score(
                parameter_mismatch_score
            ),

        "structural_change":
            normalize_score(
                structural_change_score
            ),
    }

    predicted_class = max(
        scores,
        key=scores.get,
    )

    ordered_scores = sorted(
        scores.values(),
        reverse=True,
    )

    margin = (
        ordered_scores[0]
        - ordered_scores[1]
    )

    return {
        "true_class":
            regime,
        "predicted_class":
            predicted_class,

        "measurement_noise_score":
            scores[
                "measurement_noise"
            ],

        "process_disturbance_score":
            scores[
                "process_disturbance"
            ],

        "parameter_mismatch_score":
            scores[
                "parameter_mismatch"
            ],

        "structural_change_score":
            scores[
                "structural_change"
            ],

        "classification_margin":
            margin,

        "correct":
            predicted_class
            == regime,
    }


def build_dataset() -> list[dict]:

    global_rows = load_csv(
        GLOBAL_PATH
    )

    temporal_rows = load_csv(
        TEMPORAL_PATH
    )

    adaptation_rows = load_csv(
        ADAPTATION_PATH
    )

    global_index = (
        index_by_regime_seed(
            global_rows
        )
    )

    temporal_index = (
        index_by_regime_seed(
            temporal_rows
        )
    )

    adaptation_index = (
        index_by_regime_seed(
            adaptation_rows
        )
    )

    output_rows = []

    for regime in CLASS_NAMES:

        for seed in range(100):

            key = (
                regime,
                seed,
            )

            global_row = (
                global_index[key]
            )

            temporal_row = (
                temporal_index[key]
            )

            adaptation_row = (
                adaptation_index.get(
                    key
                )
            )

            result = classify_row(
                regime=regime,
                global_row=global_row,
                temporal_row=temporal_row,
                adaptation_row=(
                    adaptation_row
                ),
            )

            output_rows.append(
                {
                    "regime":
                        regime,
                    "seed":
                        seed,
                    **result,
                }
            )

    return output_rows


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


def print_summary(
    rows: list[dict],
) -> None:

    total = len(
        rows
    )

    correct = sum(
        1
        for row in rows
        if row["correct"]
    )

    print("=" * 92)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "EXPLICIT MISMATCH CLASSIFICATION"
    )

    print("=" * 92)

    print(
        f"Overall accuracy: "
        f"{correct}/{total} "
        f"({correct / total:.3%})"
    )

    print()

    for class_name in CLASS_NAMES:

        class_rows = [
            row
            for row in rows
            if row["regime"]
            == class_name
        ]

        class_correct = sum(
            1
            for row in class_rows
            if row["correct"]
        )

        print(
            f"{class_name:<24}"
            f"{class_correct:>3}"
            f"/"
            f"{len(class_rows):<3}"
            f" "
            f"{class_correct / len(class_rows):.3%}"
        )

    print("=" * 92)


def main() -> None:

    rows = build_dataset()

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