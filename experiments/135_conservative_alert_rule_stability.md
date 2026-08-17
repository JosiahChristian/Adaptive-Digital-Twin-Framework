# Experiment 135 — conservative alert-rule stability

## Design

A class-balanced action-plus-context model was trained on population 071–110.
The highest source score threshold attaining at least 80% source unsafe recall
was selected (0.61286). That threshold flagged 39.02% of source rows.

Four exposed target populations compared:

1. the fixed numeric source threshold; and
2. an unlabeled fixed-coverage rule that chooses the target score quantile
   needed to preserve the frozen 39.02% alert budget.

No target labels enter either decision rule.

## Results

| Population | Rule | Recall | NPV | Alert coverage | Balanced accuracy |
|---|---|---:|---:|---:|---:|
| Third | Fixed threshold | 0.798 | 0.954 | 0.357 | 0.759 |
| Third | Fixed coverage | **0.811** | **0.954** | 0.390 | 0.747 |
| Fourth | Fixed threshold | 0.742 | 0.924 | 0.338 | 0.751 |
| Fourth | Fixed coverage | **0.835** | **0.947** | 0.390 | **0.777** |
| Fifth | Fixed threshold | 0.657 | 0.930 | 0.350 | 0.677 |
| Fifth | Fixed coverage | **0.823** | **0.962** | 0.390 | **0.749** |
| Sixth | Fixed threshold | 0.748 | 0.917 | 0.346 | 0.756 |
| Sixth | Fixed coverage | **0.811** | **0.933** | 0.390 | **0.768** |

## Interpretation

The numeric threshold is not portable. Preserving a source-derived alert budget
using only the unlabeled target score distribution stabilizes unsafe recall.
The rule is essentially a selective alert/defer policy, not a calibrated
probability threshold.

Action subgroup results show that action 1 is always alerted and accounts for
most unsafe rows. Fixed coverage also captures portions of unsafe action-2 and
action-3 rows, unlike the fixed threshold. This dependence must remain explicit:
the evidence concerns the current simulator's candidate-action structure.

## Prospective requirement

Experiment 137 freezes the fixed-coverage rule before a seventh population.
Primary success requires:

- unsafe recall at least 0.75;
- negative predictive value at least 0.90;
- alert coverage within 0.01 of the frozen 39.02% budget.

Balanced accuracy and action-subgroup recall are secondary endpoints.
