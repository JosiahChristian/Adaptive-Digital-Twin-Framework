import csv
import math
from pathlib import Path

from experiments.pareto_safe_responsive_persistence_analysis import (
    adaptive_policy,
    pareto_front,
)
from experiments.responsiveness_preserving_safe_persistence_control import (
    RISK_MULTIPLIERS,
    deterministic_split,
    train_loss_models,
    train_occurrence_model,
    train_magnitude_model,
    predicted_loss_table,
    predict_two_stage_risk,
    direct_predictions,
    fixed_risk_predictions,
    adaptive_risk_predictions,
    fixed_predictions,
    oracle_predictions,
    evaluate_policy,
)
from experiments.persistence_policy_learnability_margin_analysis import (
    generate_analysis_rows,
)


OUTPUT_PATH = Path(
    "results/"
    "collapse_aware_pareto_knee_selection.csv"
)

FIXED_RISK_PENALTY = 0.010

ENTROPY_MINIMUMS = [
    0.10,
    0.20,
    0.30,
    0.40,
    0.60,
]

DOMINANT_ACTION_LIMITS = [
    0.99,
    0.95,
    0.90,
    0.80,
    0.70,
]


def normalize(
    value: float,
    minimum: float,
    maximum: float,
) -> float:

    if maximum <= minimum:
        return 0.0

    return (
        value
        - minimum
    ) / (
        maximum
        - minimum
    )


def frontier_bounds(
    frontier: list[dict],
) -> dict:

    return {
        "regret_min":
            min(
                row["mean_regret"]
                for row in frontier
            ),

        "regret_max":
            max(
                row["mean_regret"]
                for row in frontier
            ),

        "under_min":
            min(
                row["under_count"]
                for row in frontier
            ),

        "under_max":
            max(
                row["under_count"]
                for row in frontier
            ),

        "over_min":
            min(
                row["over_count"]
                for row in frontier
            ),

        "over_max":
            max(
                row["over_count"]
                for row in frontier
            ),

        "entropy_min":
            min(
                row["action_entropy"]
                for row in frontier
            ),

        "entropy_max":
            max(
                row["action_entropy"]
                for row in frontier
            ),
    }


def normalized_objectives(
    row: dict,
    bounds: dict,
) -> dict:

    regret = normalize(
        row["mean_regret"],
        bounds["regret_min"],
        bounds["regret_max"],
    )

    under = normalize(
        row["under_count"],
        bounds["under_min"],
        bounds["under_max"],
    )

    over = normalize(
        row["over_count"],
        bounds["over_min"],
        bounds["over_max"],
    )

    responsiveness_loss = (
        1.0
        - normalize(
            row["action_entropy"],
            bounds["entropy_min"],
            bounds["entropy_max"],
        )
    )

    return {
        "regret":
            regret,

        "under":
            under,

        "over":
            over,

        "responsiveness_loss":
            responsiveness_loss,
    }


def geometric_ideal_distance(
    row: dict,
    bounds: dict,
) -> float:

    values = normalized_objectives(
        row,
        bounds,
    )

    return math.sqrt(
        values["regret"] ** 2
        + values["under"] ** 2
        + values["over"] ** 2
        + values["responsiveness_loss"] ** 2
    )


def collapse_penalty_score(
    row: dict,
    bounds: dict,
    collapse_weight: float = 1.0,
) -> float:

    values = normalized_objectives(
        row,
        bounds,
    )

    dominant_penalty = (
        row[
            "dominant_action_fraction"
        ] ** 2
    )

    return (
        values["regret"]
        + values["under"]
        + values["over"]
        + values["responsiveness_loss"]
        + collapse_weight
        * dominant_penalty
    )


def select_entropy_constrained(
    frontier: list[dict],
    entropy_minimum: float,
) -> dict | None:

    feasible = [
        row
        for row in frontier
        if row[
            "action_entropy"
        ]
        >= entropy_minimum
    ]

    if not feasible:
        return None

    return min(
        feasible,
        key=lambda row: (
            row["mean_regret"],
            row["under_count"],
            row["over_count"],
            -row["action_entropy"],
        ),
    )


def select_dominance_constrained(
    frontier: list[dict],
    dominant_limit: float,
) -> dict | None:

    feasible = [
        row
        for row in frontier
        if row[
            "dominant_action_fraction"
        ]
        <= dominant_limit
    ]

    if not feasible:
        return None

    return min(
        feasible,
        key=lambda row: (
            row["mean_regret"],
            row["under_count"],
            row["over_count"],
            -row["action_entropy"],
        ),
    )


def select_geometric_knee(
    frontier: list[dict],
    exclude_collapsed: bool,
) -> dict:

    candidates = frontier

    if exclude_collapsed:

        noncollapsed = [
            row
            for row in frontier
            if row[
                "action_entropy"
            ]
            > 1e-12
        ]

        if noncollapsed:
            candidates = noncollapsed

    bounds = frontier_bounds(
        frontier
    )

    return min(
        candidates,
        key=lambda row:
            geometric_ideal_distance(
                row,
                bounds,
            ),
    )


def select_collapse_penalized(
    frontier: list[dict],
) -> dict:

    bounds = frontier_bounds(
        frontier
    )

    return min(
        frontier,
        key=lambda row:
            collapse_penalty_score(
                row,
                bounds,
            ),
    )


def regret_equivalent_best_entropy(
    frontier: list[dict],
    tolerance: float = 1e-12,
) -> list[dict]:

    output = []

    for row in frontier:

        equivalents = [
            candidate
            for candidate in frontier
            if abs(
                candidate[
                    "mean_regret"
                ]
                - row[
                    "mean_regret"
                ]
            )
            <= tolerance
        ]

        best = max(
            equivalents,
            key=lambda candidate:
                candidate[
                    "action_entropy"
                ],
        )

        if (
            best["policy"]
            == row["policy"]
            and best
            not in output
        ):

            output.append(
                best
            )

    return output


def save_results(
    frontier: list[dict],
    selections: list[dict],
) -> None:

    OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )

    selected_by = {}

    for selection in selections:

        policy = selection[
            "policy"
        ]

        selected_by.setdefault(
            policy,
            []
        ).append(
            selection[
                "criterion"
            ]
        )

    rows = []

    for row in frontier:

        output = dict(
            row
        )

        output[
            "selected_by"
        ] = ";".join(
            selected_by.get(
                row["policy"],
                [],
            )
        )

        rows.append(
            output
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


def print_policy(
    label: str,
    row: dict,
) -> None:

    print(
        f"{label:<34} "
        f"policy="
        f"{row['policy']:<20} "
        f"regret="
        f"{row['mean_regret']:.6f} "
        f"under="
        f"{row['under_count']:<2} "
        f"over="
        f"{row['over_count']:<2} "
        f"entropy="
        f"{row['action_entropy']:.3f} "
        f"dominant="
        f"{row['dominant_action_fraction']:.3%}"
    )


def main() -> None:

    rows = generate_analysis_rows()

    (
        train_rows,
        test_rows,
    ) = deterministic_split(
        rows
    )

    loss_models = train_loss_models(
        train_rows
    )

    occurrence_model = train_occurrence_model(
        train_rows
    )

    magnitude_model = train_magnitude_model(
        train_rows
    )

    predicted_losses = predicted_loss_table(
        loss_models,
        test_rows,
    )

    predicted_risks = predict_two_stage_risk(
        occurrence_model,
        magnitude_model,
        test_rows,
    )

    direct = direct_predictions(
        predicted_losses
    )

    evaluations = []

    for persistence in (
        1,
        2,
        3,
    ):

        evaluations.append(
            evaluate_policy(
                name=f"fixed_k{persistence}",
                predictions=fixed_predictions(
                    persistence,
                    test_rows,
                ),
                rows=test_rows,
                direct=direct,
            )
        )

    evaluations.append(
        evaluate_policy(
            name="direct_loss",
            predictions=direct,
            rows=test_rows,
            direct=direct,
        )
    )

    fixed_risk = fixed_risk_predictions(
        predicted_losses,
        FIXED_RISK_PENALTY,
    )

    evaluations.append(
        evaluate_policy(
            name="fixed_risk_0.010",
            predictions=fixed_risk,
            rows=test_rows,
            direct=direct,
        )
    )

    for multiplier in (
        RISK_MULTIPLIERS
    ):

        predictions = adaptive_risk_predictions(
            predicted_losses,
            predicted_risks,
            multiplier,
        )

        evaluations.append(
            evaluate_policy(
                name=(
                    "two_stage_"
                    f"{multiplier:.2f}"
                ),
                predictions=predictions,
                rows=test_rows,
                direct=direct,
            )
        )

    evaluations.append(
        evaluate_policy(
            name="oracle",
            predictions=oracle_predictions(
                test_rows
            ),
            rows=test_rows,
            direct=direct,
        )
    )

    frontier = pareto_front(
        evaluations
    )

    selections = []

    geometric_all = select_geometric_knee(
        frontier,
        exclude_collapsed=False,
    )

    selections.append(
        {
            "criterion":
                "geometric_all",

            "policy":
                geometric_all[
                    "policy"
                ],
        }
    )

    geometric_noncollapsed = (
        select_geometric_knee(
            frontier,
            exclude_collapsed=True,
        )
    )

    selections.append(
        {
            "criterion":
                "geometric_noncollapsed",

            "policy":
                geometric_noncollapsed[
                    "policy"
                ],
        }
    )

    collapse_penalized = (
        select_collapse_penalized(
            frontier
        )
    )

    selections.append(
        {
            "criterion":
                "collapse_penalized",

            "policy":
                collapse_penalized[
                    "policy"
                ],
        }
    )

    entropy_selections = []

    for entropy_minimum in (
        ENTROPY_MINIMUMS
    ):

        selected = (
            select_entropy_constrained(
                frontier,
                entropy_minimum,
            )
        )

        if selected is None:
            continue

        entropy_selections.append(
            (
                entropy_minimum,
                selected,
            )
        )

        selections.append(
            {
                "criterion":
                    (
                        "entropy>="
                        f"{entropy_minimum:.2f}"
                    ),

                "policy":
                    selected[
                        "policy"
                    ],
            }
        )

    dominance_selections = []

    for dominant_limit in (
        DOMINANT_ACTION_LIMITS
    ):

        selected = (
            select_dominance_constrained(
                frontier,
                dominant_limit,
            )
        )

        if selected is None:
            continue

        dominance_selections.append(
            (
                dominant_limit,
                selected,
            )
        )

        selections.append(
            {
                "criterion":
                    (
                        "dominant<="
                        f"{dominant_limit:.2f}"
                    ),

                "policy":
                    selected[
                        "policy"
                    ],
            }
        )

    regret_equivalent = (
        regret_equivalent_best_entropy(
            frontier
        )
    )

    save_results(
        frontier,
        selections,
    )

    print("=" * 175)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "COLLAPSE-AWARE PARETO "
        "KNEE SELECTION"
    )

    print("=" * 175)

    print(
        f"total contexts="
        f"{len(rows)}"
    )

    print(
        f"training contexts="
        f"{len(train_rows)}"
    )

    print(
        f"test contexts="
        f"{len(test_rows)}"
    )

    print()

    print(
        "PARETO FRONT"
    )

    for row in frontier:

        print_policy(
            "frontier",
            row,
        )

    print()

    print(
        "GEOMETRIC SELECTIONS"
    )

    print_policy(
        "geometric all",
        geometric_all,
    )

    print_policy(
        "geometric noncollapsed",
        geometric_noncollapsed,
    )

    print_policy(
        "collapse penalized",
        collapse_penalized,
    )

    print()

    print(
        "ENTROPY-CONSTRAINED SELECTIONS"
    )

    for threshold, row in (
        entropy_selections
    ):

        print_policy(
            (
                "entropy >= "
                f"{threshold:.2f}"
            ),
            row,
        )

    print()

    print(
        "DOMINANT-ACTION-CONSTRAINED "
        "SELECTIONS"
    )

    for threshold, row in (
        dominance_selections
    ):

        print_policy(
            (
                "dominant <= "
                f"{threshold:.2f}"
            ),
            row,
        )

    print()

    print(
        "REGRET-EQUIVALENT "
        "MAX-ENTROPY POLICIES"
    )

    for row in regret_equivalent:

        print_policy(
            "equal-regret representative",
            row,
        )

    print("=" * 175)

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()