import csv
import statistics
from pathlib import Path


INPUT_PATH = Path(
    "results/mismatch_classification.csv"
)

OUTPUT_PATH = Path(
    "results/confidence_aware_attribution.csv"
)


AMBIGUOUS_THRESHOLD = 0.10
LOW_CONFIDENCE_THRESHOLD = 0.30


def load_rows() -> list[dict]:

    with INPUT_PATH.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def confidence_band(
    margin: float,
) -> str:

    if margin < AMBIGUOUS_THRESHOLD:
        return "ambiguous"

    if margin < LOW_CONFIDENCE_THRESHOLD:
        return "low_confidence"

    return "confident"


def analyze_rows(
    rows: list[dict],
) -> list[dict]:

    output_rows = []

    for row in rows:

        margin = float(
            row["classification_margin"]
        )

        band = confidence_band(
            margin
        )

        output_rows.append(
            {
                **row,
                "confidence_band":
                    band,
                "abstain":
                    band == "ambiguous",
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


def summarize(
    rows: list[dict],
) -> None:

    bands = [
        "ambiguous",
        "low_confidence",
        "confident",
    ]

    total = len(
        rows
    )

    correct_total = sum(
        row["correct"] == "True"
        for row in rows
    )

    print("=" * 102)

    print(
        "ADAPTIVE DIGITAL TWIN — "
        "CONFIDENCE-AWARE MISMATCH ATTRIBUTION"
    )

    print("=" * 102)

    print(
        f"Original hard-classification accuracy: "
        f"{correct_total}/{total} "
        f"({correct_total / total:.3%})"
    )

    print()

    for band in bands:

        band_rows = [
            row
            for row in rows
            if row["confidence_band"]
            == band
        ]

        if not band_rows:
            continue

        correct = sum(
            row["correct"] == "True"
            for row in band_rows
        )

        margins = [
            float(
                row[
                    "classification_margin"
                ]
            )
            for row in band_rows
        ]

        print(
            f"{band:<20}"
            f"count={len(band_rows):<4} "
            f"accuracy="
            f"{correct / len(band_rows):.3%} "
            f"mean_margin="
            f"{statistics.mean(margins):.6f}"
        )

    print()

    accepted_rows = [
        row
        for row in rows
        if row["confidence_band"]
        != "ambiguous"
    ]

    accepted_correct = sum(
        row["correct"] == "True"
        for row in accepted_rows
    )

    abstained_rows = [
        row
        for row in rows
        if row["confidence_band"]
        == "ambiguous"
    ]

    errors = [
        row
        for row in rows
        if row["correct"] == "False"
    ]

    abstained_errors = [
        row
        for row in errors
        if row["confidence_band"]
        == "ambiguous"
    ]

    print(
        f"Coverage after abstention: "
        f"{len(accepted_rows)}/{total} "
        f"({len(accepted_rows) / total:.3%})"
    )

    print(
        f"Accuracy on accepted cases: "
        f"{accepted_correct}/"
        f"{len(accepted_rows)} "
        f"({accepted_correct / len(accepted_rows):.3%})"
    )

    print(
        f"Abstention count: "
        f"{len(abstained_rows)}"
    )

    print(
        f"Errors captured by abstention: "
        f"{len(abstained_errors)}/"
        f"{len(errors)} "
        f"("
        f"{len(abstained_errors) / len(errors):.3%}"
        f")"
    )

    print("=" * 102)


def main() -> None:

    rows = load_rows()

    analyzed_rows = analyze_rows(
        rows
    )

    save_results(
        analyzed_rows
    )

    summarize(
        analyzed_rows
    )

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()