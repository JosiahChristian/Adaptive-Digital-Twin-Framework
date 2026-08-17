# Experiment 157 preregistration: prediction-decision divergence under targeted label corruption

## Motivation
Experiments 154 and 156 showed that a fixed 20% targeted unsafe-to-safe label corruption can produce favorable downstream intervention outcomes on shifted target populations even when global discrimination changes little or inconsistently. The next question is whether prediction quality and decision utility can prospectively diverge under the same frozen corruption mechanism.

## Frozen source and attack
Use the same source population, feature set, logistic model family, class weighting, 20% targeted unsafe-to-safe corruption of the highest-context-distance unsafe source rows, and source-derived 80% unsafe-recall coverage rule used in Experiments 150-156.

## Fresh target population
Generate a new untouched 40-seed population using seeds **44631-44670** only after this preregistration is committed. Use the same reconstruction mechanism as the prior prospective action-conditioned populations.

## Prediction endpoints
For clean and poisoned models on the untouched target, report:
- ROC AUC;
- average precision;
- excluded-unsafe recall at the frozen exclusion budget.

Define prediction direction as:
- `prediction_improves` if poisoned model is better on at least two of the three prediction endpoints and worse on none;
- `prediction_degrades` if poisoned model is worse on at least two and better on none;
- `prediction_mixed` otherwise.

## Decision endpoints
Apply the exact same predicted-loss selector after the frozen top-N hazard exclusion for each model. Report:
- unsafe selections;
- total realized regret.

Define decision direction as:
- `decision_improves` only if poisoned model has both fewer unsafe selections and lower regret;
- `decision_degrades` only if poisoned model has both more unsafe selections and higher regret;
- `decision_mixed` otherwise.

## Primary divergence criterion
Prediction-decision divergence is present if prediction direction and decision direction are not aligned, specifically any of:
- prediction_degrades + decision_improves;
- prediction_improves + decision_degrades;
- prediction_mixed + decision_improves;
- prediction_mixed + decision_degrades.

The strongest preregistered divergence pattern is **prediction_degrades + decision_improves** or **prediction_improves + decision_degrades**.

## Interpretation boundary
A pass would show that, in this frozen simulation and corruption mechanism under population shift, conventional ranking metrics do not reliably determine downstream intervention utility. It would not imply that poisoning is beneficial, that lower-quality labels should be preferred, or that the phenomenon generalizes beyond the studied simulator and policy.
