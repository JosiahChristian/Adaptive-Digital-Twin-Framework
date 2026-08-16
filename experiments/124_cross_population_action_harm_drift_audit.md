# Experiment 124 — cross-population action-harm drift audit

## Purpose

Diagnose why the frozen Experiment 123 joint representation failed. This audit is explanatory and does not modify or rescue the prospective result.

## Findings

Every principal continuous feature shifted significantly between populations (all two-sample KS p-values below 5e-48). More importantly, four of five features changed their point-biserial association with unsafe action:

| Feature | Train association | Test association | Train AUC | Test AUC |
|---|---:|---:|---:|---:|
| Context support distance | +0.239 | -0.065 | 0.689 | 0.572 |
| Action support distance | +0.238 | -0.062 | 0.678 | 0.558 |
| Action minus context support | -0.086 | +0.055 | 0.419 | 0.557 |
| Predicted action loss | -0.104 | +0.037 | 0.448 | 0.532 |
| Predicted relative loss | -0.107 | -0.063 | 0.428 | 0.394 |

The apparent discrepancy between negative target correlations and support-only AUC above 0.5 is caused by applying coefficients learned with the positive training direction: the frozen model reverses the raw target ordering.

Action identity remained highly informative:

| Population | Action 1 unsafe | Action 2 unsafe | Action 3 unsafe |
|---|---:|---:|---:|
| Train 071–110 | 37.6% | 14.2% | 10.6% |
| Test 111–150 | 34.9% | 6.5% | 2.7% |

## Conclusion

Experiment 123 failed because continuous proxy semantics were not invariant. Covariate drift alone is insufficient to explain the failure; the feature/outcome relationships themselves reversed, which is concept drift. Predicted loss is especially hazardous because its learned direction damages otherwise weakly useful support ranking.

The stable ordering by action identity motivates Experiment 125: a frozen action-aware transfer comparison. It is a new hypothesis tested on the already exposed third population and therefore is confirmatory only with respect to a future fourth population; results on 111–150 are explicitly post-failure diagnostic.

## Artifacts

- `results/cross_population_action_harm_drift_audit.csv`
- `results/cross_population_action_harm_drift_by_action.csv`
