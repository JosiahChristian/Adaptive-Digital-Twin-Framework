import csv
import math
import statistics
from pathlib import Path


INPUT_PATH = Path(
    "results/"
    "multiseed_support_aware_robustness_validation_seeds.csv"
)

OUTPUT_PATH = Path(
    "results/"
    "seed_level_support_aware_failure_decomposition.csv"
)

SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "seed_level_support_aware_failure_decomposition_summary.csv"
)

PRIMARY_POLICY = "primary_baseline"
SUPPORT_POLICY = "support_2.50"

FLOAT_TOLERANCE = 1e-12


def read_csv(
    path: Path,
) -> list[dict]:

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
    row: dict,
    field: str,
) -> float:

    return float(
        row[
            field
        ]
    )


def as_int(
    row: dict,
    field: str,
) -> int:

    return int(
        float(
            row[
                field
            ]
        )
    )


def safe_float(
    row: dict,
    field: str,
    default: float = 0.0,
) -> float:

    value = row.get(
        field,
        "",
    )

    if value in (
        "",
        None,
    ):

        return default

    return float(
        value
    )


def safe_int(
    row: dict,
    field: str,
    default: int = 0,
) -> int:

    value = row.get(
        field,
        "",
    )

    if value in (
        "",
        None,
    ):

        return default

    return int(
        float(
            value
        )
    )


def paired_rows_by_seed(
    rows: list[dict],
) -> list[
    tuple[
        int,
        dict,
        dict,
    ]
]:

    by_seed = {}

    for row in rows:

        policy = row[
            "policy"
        ]

        if policy not in (
            PRIMARY_POLICY,
            SUPPORT_POLICY,
        ):

            continue

        seed = as_int(
            row,
            "generation_seed",
        )

        by_seed.setdefault(
            seed,
            {},
        )

        by_seed[
            seed
        ][
            policy
        ] = row

    pairs = []

    for seed in sorted(
        by_seed
    ):

        policies = by_seed[
            seed
        ]

        if (
            PRIMARY_POLICY
            not in policies
            or SUPPORT_POLICY
            not in policies
        ):

            continue

        pairs.append(
            (
                seed,
                policies[
                    PRIMARY_POLICY
                ],
                policies[
                    SUPPORT_POLICY
                ],
            )
        )

    return pairs


def pearson_correlation(
    x: list[float],
    y: list[float],
) -> float:

    if (
        len(x) < 2
        or len(y) < 2
        or len(x) != len(y)
    ):

        return 0.0

    mean_x = statistics.mean(
        x
    )

    mean_y = statistics.mean(
        y
    )

    numerator = sum(
        (
            a
            - mean_x
        )
        * (
            b
            - mean_y
        )
        for a, b in zip(
            x,
            y,
        )
    )

    denominator_x = math.sqrt(
        sum(
            (
                a
                - mean_x
            )
            ** 2
            for a in x
        )
    )

    denominator_y = math.sqrt(
        sum(
            (
                b
                - mean_y
            )
            ** 2
            for b in y
        )
    )

    denominator = (
        denominator_x
        * denominator_y
    )

    if (
        denominator
        <= FLOAT_TOLERANCE
    ):

        return 0.0

    return (
        numerator
        / denominator
    )


def classify_seed(
    delta_retention: float,
    delta_regret: float,
) -> str:

    responsive_gain = (
        delta_retention
        > FLOAT_TOLERANCE
    )

    consequence_cost = (
        delta_regret
        > FLOAT_TOLERANCE
    )

    if (
        responsive_gain
        and not consequence_cost
    ):

        return (
            "responsive_gain_no_regret_cost"
        )

    if (
        responsive_gain
        and consequence_cost
    ):

        return (
            "responsive_gain_with_regret_cost"
        )

    if (
        not responsive_gain
        and not consequence_cost
    ):

        return (
            "no_gain_no_regret_cost"
        )

    return (
        "no_gain_with_regret_cost"
    )


def save_csv(
    path: Path,
    rows: list[dict],
) -> None:

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

    for row in rows:

        for field in fields:

            row.setdefault(
                field,
                "",
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
            rows
        )


def main() -> None:

    rows = read_csv(
        INPUT_PATH
    )

    pairs = paired_rows_by_seed(
        rows
    )

    seed_rows = []

    category_counts = {
        "responsive_gain_no_regret_cost":
            0,

        "responsive_gain_with_regret_cost":
            0,

        "no_gain_no_regret_cost":
            0,

        "no_gain_with_regret_cost":
            0,
    }

    delta_regrets = []
    delta_under = []
    delta_over = []
    delta_entropy = []
    delta_retention = []
    delta_recall = []
    delta_precision = []

    harmful_counts = []
    beneficial_counts = []
    recovered_counts = []

    zero_harmful_seeds = 0
    regret_nonincrease_seeds = 0
    regret_increase_seeds = 0
    under_nonincrease_seeds = 0
    under_increase_seeds = 0

    worst_regret_seed = None
    worst_regret_delta = -math.inf

    worst_under_seed = None
    worst_under_delta = -math.inf

    best_retention_seed = None
    best_retention_gain = -math.inf

    for (
        seed,
        primary,
        support,
    ) in pairs:

        primary_regret = as_float(
            primary,
            "mean_regret",
        )

        support_regret = as_float(
            support,
            "mean_regret",
        )

        primary_under = as_int(
            primary,
            "under_count",
        )

        support_under = as_int(
            support,
            "under_count",
        )

        primary_over = as_int(
            primary,
            "over_count",
        )

        support_over = as_int(
            support,
            "over_count",
        )

        primary_entropy = as_float(
            primary,
            "action_entropy",
        )

        support_entropy = as_float(
            support,
            "action_entropy",
        )

        primary_retention = safe_float(
            primary,
            "responsive_action_retention",
        )

        support_retention = safe_float(
            support,
            "responsive_action_retention",
        )

        primary_recall = safe_float(
            primary,
            "safe_action_recall",
        )

        support_recall = safe_float(
            support,
            "safe_action_recall",
        )

        primary_precision = safe_float(
            primary,
            "safe_action_precision",
        )

        support_precision = safe_float(
            support,
            "safe_action_precision",
        )

        harmful = safe_int(
            support,
            "harmful_expansion_contexts",
        )

        beneficial = safe_int(
            support,
            "beneficial_expansion_contexts",
        )

        recovered = safe_int(
            support,
            "recovered_responsive_contexts",
        )

        expanded = safe_int(
            support,
            "expansion_contexts",
        )

        delta_r = (
            support_regret
            - primary_regret
        )

        delta_u = (
            support_under
            - primary_under
        )

        delta_o = (
            support_over
            - primary_over
        )

        delta_h = (
            support_entropy
            - primary_entropy
        )

        delta_ret = (
            support_retention
            - primary_retention
        )

        delta_rec = (
            support_recall
            - primary_recall
        )

        delta_prec = (
            support_precision
            - primary_precision
        )

        category = classify_seed(
            delta_ret,
            delta_r,
        )

        category_counts[
            category
        ] += 1

        if (
            harmful
            == 0
        ):

            zero_harmful_seeds += 1

        if (
            delta_r
            <= FLOAT_TOLERANCE
        ):

            regret_nonincrease_seeds += 1

        else:

            regret_increase_seeds += 1

        if (
            delta_u
            <= 0
        ):

            under_nonincrease_seeds += 1

        else:

            under_increase_seeds += 1

        if (
            delta_r
            > worst_regret_delta
        ):

            worst_regret_delta = delta_r
            worst_regret_seed = seed

        if (
            delta_u
            > worst_under_delta
        ):

            worst_under_delta = delta_u
            worst_under_seed = seed

        if (
            delta_ret
            > best_retention_gain
        ):

            best_retention_gain = delta_ret
            best_retention_seed = seed

        delta_regrets.append(
            delta_r
        )

        delta_under.append(
            float(
                delta_u
            )
        )

        delta_over.append(
            float(
                delta_o
            )
        )

        delta_entropy.append(
            delta_h
        )

        delta_retention.append(
            delta_ret
        )

        delta_recall.append(
            delta_rec
        )

        delta_precision.append(
            delta_prec
        )

        harmful_counts.append(
            float(
                harmful
            )
        )

        beneficial_counts.append(
            float(
                beneficial
            )
        )

        recovered_counts.append(
            float(
                recovered
            )
        )

        benefit_harm_ratio = (
            beneficial
            / harmful
            if harmful > 0
            else float(
                beneficial
            )
        )

        seed_rows.append(
            {
                "generation_seed":
                    seed,

                "primary_regret":
                    primary_regret,

                "support_regret":
                    support_regret,

                "delta_regret":
                    delta_r,

                "primary_under":
                    primary_under,

                "support_under":
                    support_under,

                "delta_under":
                    delta_u,

                "primary_over":
                    primary_over,

                "support_over":
                    support_over,

                "delta_over":
                    delta_o,

                "primary_entropy":
                    primary_entropy,

                "support_entropy":
                    support_entropy,

                "delta_entropy":
                    delta_h,

                "primary_retention":
                    primary_retention,

                "support_retention":
                    support_retention,

                "delta_retention":
                    delta_ret,

                "primary_recall":
                    primary_recall,

                "support_recall":
                    support_recall,

                "delta_recall":
                    delta_rec,

                "primary_precision":
                    primary_precision,

                "support_precision":
                    support_precision,

                "delta_precision":
                    delta_prec,

                "expansion_contexts":
                    expanded,

                "recovered_responsive_contexts":
                    recovered,

                "beneficial_expansions":
                    beneficial,

                "harmful_expansions":
                    harmful,

                "benefit_harm_ratio":
                    benefit_harm_ratio,

                "category":
                    category,
            }
        )

    total_seeds = len(
        pairs
    )

    corr_retention_regret = (
        pearson_correlation(
            delta_retention,
            delta_regrets,
        )
    )

    corr_harmful_regret = (
        pearson_correlation(
            harmful_counts,
            delta_regrets,
        )
    )

    corr_harmful_under = (
        pearson_correlation(
            harmful_counts,
            delta_under,
        )
    )

    corr_recovered_regret = (
        pearson_correlation(
            recovered_counts,
            delta_regrets,
        )
    )

    corr_beneficial_regret = (
        pearson_correlation(
            beneficial_counts,
            delta_regrets,
        )
    )

    summary_rows = [
        {
            "metric":
                "seeds",

            "value":
                total_seeds,
        },
        {
            "metric":
                "responsive_gain_no_regret_cost",

            "value":
                category_counts[
                    "responsive_gain_no_regret_cost"
                ],
        },
        {
            "metric":
                "responsive_gain_with_regret_cost",

            "value":
                category_counts[
                    "responsive_gain_with_regret_cost"
                ],
        },
        {
            "metric":
                "no_gain_no_regret_cost",

            "value":
                category_counts[
                    "no_gain_no_regret_cost"
                ],
        },
        {
            "metric":
                "no_gain_with_regret_cost",

            "value":
                category_counts[
                    "no_gain_with_regret_cost"
                ],
        },
        {
            "metric":
                "zero_harmful_expansion_seeds",

            "value":
                zero_harmful_seeds,
        },
        {
            "metric":
                "regret_nonincrease_seeds",

            "value":
                regret_nonincrease_seeds,
        },
        {
            "metric":
                "regret_increase_seeds",

            "value":
                regret_increase_seeds,
        },
        {
            "metric":
                "under_nonincrease_seeds",

            "value":
                under_nonincrease_seeds,
        },
        {
            "metric":
                "under_increase_seeds",

            "value":
                under_increase_seeds,
        },
        {
            "metric":
                "mean_delta_regret",

            "value":
                statistics.mean(
                    delta_regrets
                ),
        },
        {
            "metric":
                "median_delta_regret",

            "value":
                statistics.median(
                    delta_regrets
                ),
        },
        {
            "metric":
                "mean_delta_under",

            "value":
                statistics.mean(
                    delta_under
                ),
        },
        {
            "metric":
                "mean_delta_over",

            "value":
                statistics.mean(
                    delta_over
                ),
        },
        {
            "metric":
                "mean_delta_entropy",

            "value":
                statistics.mean(
                    delta_entropy
                ),
        },
        {
            "metric":
                "mean_delta_retention",

            "value":
                statistics.mean(
                    delta_retention
                ),
        },
        {
            "metric":
                "mean_delta_recall",

            "value":
                statistics.mean(
                    delta_recall
                ),
        },
        {
            "metric":
                "mean_delta_precision",

            "value":
                statistics.mean(
                    delta_precision
                ),
        },
        {
            "metric":
                "mean_harmful_expansions",

            "value":
                statistics.mean(
                    harmful_counts
                ),
        },
        {
            "metric":
                "mean_beneficial_expansions",

            "value":
                statistics.mean(
                    beneficial_counts
                ),
        },
        {
            "metric":
                "mean_recovered_responsive",

            "value":
                statistics.mean(
                    recovered_counts
                ),
        },
        {
            "metric":
                "corr_delta_retention_delta_regret",

            "value":
                corr_retention_regret,
        },
        {
            "metric":
                "corr_harmful_delta_regret",

            "value":
                corr_harmful_regret,
        },
        {
            "metric":
                "corr_harmful_delta_under",

            "value":
                corr_harmful_under,
        },
        {
            "metric":
                "corr_recovered_delta_regret",

            "value":
                corr_recovered_regret,
        },
        {
            "metric":
                "corr_beneficial_delta_regret",

            "value":
                corr_beneficial_regret,
        },
        {
            "metric":
                "worst_regret_seed",

            "value":
                worst_regret_seed,
        },
        {
            "metric":
                "worst_regret_delta",

            "value":
                worst_regret_delta,
        },
        {
            "metric":
                "worst_under_seed",

            "value":
                worst_under_seed,
        },
        {
            "metric":
                "worst_under_delta",

            "value":
                worst_under_delta,
        },
        {
            "metric":
                "best_retention_gain_seed",

            "value":
                best_retention_seed,
        },
        {
            "metric":
                "best_retention_gain",

            "value":
                best_retention_gain,
        },
    ]

    save_csv(
        OUTPUT_PATH,
        seed_rows,
    )

    save_csv(
        SUMMARY_OUTPUT_PATH,
        summary_rows,
    )

    print("=" * 200)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "SEED-LEVEL SUPPORT-AWARE "
        "FAILURE DECOMPOSITION"
    )

    print("=" * 200)

    print(
        f"input="
        f"{INPUT_PATH}"
    )

    print(
        f"paired seeds="
        f"{total_seeds}"
    )

    print()

    print(
        "SEED-LEVEL DELTAS "
        "(support_2.50 - primary)"
    )

    for row in (
        seed_rows
    ):

        print(
            f"seed="
            f"{row['generation_seed']} "
            f"dR="
            f"{row['delta_regret']:+.6f} "
            f"dUnder="
            f"{row['delta_under']:+d} "
            f"dOver="
            f"{row['delta_over']:+d} "
            f"dRetention="
            f"{row['delta_retention']:+.3%} "
            f"dRecall="
            f"{row['delta_recall']:+.3%} "
            f"dPrecision="
            f"{row['delta_precision']:+.3%} "
            f"beneficial="
            f"{row['beneficial_expansions']} "
            f"harmful="
            f"{row['harmful_expansions']} "
            f"recovered="
            f"{row['recovered_responsive_contexts']} "
            f"class="
            f"{row['category']}"
        )

    print()

    print(
        "SEED CATEGORY COUNTS"
    )

    print(
        "responsive gain, "
        "no regret cost="
        f"{category_counts['responsive_gain_no_regret_cost']}/"
        f"{total_seeds}"
    )

    print(
        "responsive gain, "
        "with regret cost="
        f"{category_counts['responsive_gain_with_regret_cost']}/"
        f"{total_seeds}"
    )

    print(
        "no responsive gain, "
        "no regret cost="
        f"{category_counts['no_gain_no_regret_cost']}/"
        f"{total_seeds}"
    )

    print(
        "no responsive gain, "
        "with regret cost="
        f"{category_counts['no_gain_with_regret_cost']}/"
        f"{total_seeds}"
    )

    print()

    print(
        "SAFETY CONCENTRATION"
    )

    print(
        "zero-harmful seeds="
        f"{zero_harmful_seeds}/"
        f"{total_seeds}"
    )

    print(
        "regret nonincrease seeds="
        f"{regret_nonincrease_seeds}/"
        f"{total_seeds}"
    )

    print(
        "regret increase seeds="
        f"{regret_increase_seeds}/"
        f"{total_seeds}"
    )

    print(
        "under nonincrease seeds="
        f"{under_nonincrease_seeds}/"
        f"{total_seeds}"
    )

    print(
        "under increase seeds="
        f"{under_increase_seeds}/"
        f"{total_seeds}"
    )

    print()

    print(
        "MEAN DELTAS"
    )

    print(
        f"mean dR="
        f"{statistics.mean(delta_regrets):+.6f}"
    )

    print(
        f"median dR="
        f"{statistics.median(delta_regrets):+.6f}"
    )

    print(
        f"mean dUnder="
        f"{statistics.mean(delta_under):+.3f}"
    )

    print(
        f"mean dOver="
        f"{statistics.mean(delta_over):+.3f}"
    )

    print(
        f"mean dEntropy="
        f"{statistics.mean(delta_entropy):+.3f}"
    )

    print(
        f"mean dRetention="
        f"{statistics.mean(delta_retention):+.3%}"
    )

    print(
        f"mean dRecall="
        f"{statistics.mean(delta_recall):+.3%}"
    )

    print(
        f"mean dPrecision="
        f"{statistics.mean(delta_precision):+.3%}"
    )

    print()

    print(
        "DESCRIPTIVE CORRELATIONS"
    )

    print(
        "corr(dRetention,dR)="
        f"{corr_retention_regret:+.3f}"
    )

    print(
        "corr(harmful,dR)="
        f"{corr_harmful_regret:+.3f}"
    )

    print(
        "corr(harmful,dUnder)="
        f"{corr_harmful_under:+.3f}"
    )

    print(
        "corr(recovered,dR)="
        f"{corr_recovered_regret:+.3f}"
    )

    print(
        "corr(beneficial,dR)="
        f"{corr_beneficial_regret:+.3f}"
    )

    print()

    print(
        "EXTREMES"
    )

    print(
        f"worst regret seed="
        f"{worst_regret_seed} "
        f"dR="
        f"{worst_regret_delta:+.6f}"
    )

    print(
        f"worst under seed="
        f"{worst_under_seed} "
        f"dUnder="
        f"{worst_under_delta:+d}"
    )

    print(
        f"best retention-gain seed="
        f"{best_retention_seed} "
        f"dRetention="
        f"{best_retention_gain:+.3%}"
    )

    print("=" * 200)

    print(
        f"Seed decomposition saved to: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Summary saved to: "
        f"{SUMMARY_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()