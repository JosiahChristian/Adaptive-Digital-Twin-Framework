# Decision-Aware Evidence Synthesis Through Experiment 163

## Purpose

This synthesis consolidates the poisoning/decision experiments into one bounded research story. It does not modify or prescribe the active experimental pipeline.

## Evidence progression

### 1. A surprising fixed-budget effect appeared

Earlier experiments showed that a poisoned hazard model could sometimes produce fewer unsafe selections under a frozen intervention budget even though the poisoned model was not globally better. This ruled out the simple interpretation that a favorable downstream outcome necessarily reflected improved global hazard prediction.

### 2. The effect prospectively replicated, but not as a universal benefit

A fresh reconstructed population reproduced the directional boundary-sensitive intervention effect while global ranking metrics remained nearly unchanged. Subsequent multi-population evaluation showed heterogeneous outcomes: some populations improved on downstream endpoints, others worsened, and prediction metrics did not determine the sign of those effects.

The evidence therefore rejects both "poisoning is beneficial" and "poisoning always worsens every downstream endpoint."

### 3. Global prediction and downstream decisions are not interchangeable

Seed-level evaluation showed frequent directional disagreement between changes in ROC AUC and changes in fixed-budget outcomes. However, the preregistered broad weak-coupling hypothesis failed because some predictive quantities retained meaningful association with downstream endpoints.

The correct conclusion is metric-specific rather than a universal prediction-versus-decision decoupling claim.

### 4. Decision-aligned evaluation became substantially more informative

Experiment 163 found that change in excluded-unsafe recall tracked unsafe-selection change with Spearman rho -0.907622 and regret change with rho -0.804072 across 40 fresh generation seeds. ROC AUC was substantially weaker for both endpoints. Average precision was more competitive, and the preregistered superiority of excluded-unsafe recall over both AUC and AP was not confirmed because the recall-versus-AP bootstrap interval crossed zero.

This is a partial positive result with an important negative boundary: intervention alignment matters, but no single metric has yet been established as universally superior.

## Current mechanistic model

The accumulated evidence is consistent with the following candidate mechanism:

1. a model perturbation changes candidate scores;
2. only some score changes alter ordering near the fixed-budget cutoff;
3. local rank changes alter which candidates are excluded or selected;
4. the safety composition of those changed candidates determines downstream unsafe selections and regret;
5. global ranking metrics can underweight these local changes because they summarize the entire score distribution.

This mechanism is **not yet established**. The current experiments infer it from metric/outcome behavior rather than directly measuring and prospectively validating the local boundary geometry.

## Strongest current bounded claim

Within the tested simulator and frozen fixed-budget decision procedure, **global predictive discrimination alone is insufficient to characterize the downstream consequence of model perturbations, and an intervention-aligned metric can track downstream effects substantially more strongly than ROC AUC.**

The evidence does not establish universal superiority over average precision, causal sufficiency of excluded-unsafe recall, or transfer across budgets, attacks, model classes, or domains.

## Next evidence gate

A mechanistic promotion would require a prospectively specified test of local boundary quantities on fresh populations. Candidate quantities include:

- score gap immediately across the intervention cutoff;
- density of candidates in a fixed neighborhood of the cutoff;
- clean-to-perturbed rank turnover near the cutoff;
- unsafe/safe composition of the boundary neighborhood;
- perturbation magnitude among candidates capable of crossing the cutoff.

The quantities and primary endpoint should be frozen before inspecting outcomes. The test should compare boundary-aware predictors against global metrics and simple baselines, and should retain populations where the direction reverses or no effect appears.

## Publication relevance

This line should remain secondary to the existing pre-decision harmful-expansion publication candidate unless stronger prospective evidence shows that boundary geometry is a reproducible mechanism rather than an evaluation artifact. Its present value is methodological: it demonstrates why adaptive-system research should evaluate the actual decision rule in addition to reporting model-level discrimination metrics.

## Prohibited interpretations

The current evidence does not support claims that poisoning is beneficial, that degraded prediction improves control, that ROC AUC is generally useless, that excluded-unsafe recall is universally optimal, that a causal boundary mechanism has already been proven, or that these simulator-internal findings establish deployment safety or biomedical/clinical relevance.
