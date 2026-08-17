# Experiment 161 — Seed-Level Prediction–Decision Coupling Interpretation

## Result

Experiment 161 prospectively evaluated 40 generation seeds on a newly reconstructed target population (8,598 rows) using the frozen clean-versus-poisoned comparison and decision procedure.

The preregistered **weak-coupling pass failed**.

Observed rank correlations between prediction changes and decision changes were mixed:

- ΔAUC vs. Δregret: Spearman rho **0.354**
- ΔAUC vs. Δunsafe-selected: rho **0.330**
- ΔAP vs. Δregret: rho **0.380**
- Δexcluded-unsafe-recall vs. Δunsafe-selected: rho **-0.546**

The AUC-based sign-discordance rates were high:

- ΔAUC vs. Δregret discordance: **0.656**
- ΔAUC vs. Δunsafe-selected discordance: **0.846**

However, the preregistered correlation criteria were not satisfied, so the experiment does not support the stronger claim that prediction and downstream decision changes are simply weakly coupled across seeds.

Bootstrap intervals also show substantial uncertainty for several correlations. The excluded-unsafe-recall/unsafe-selection relationship is the clearest nonzero association in the frozen summary, with a bootstrap interval approximately **[-0.742, -0.278]**.

## Interpretation

Experiment 161 strengthens the case against using **global AUC change alone** as a surrogate for downstream fixed-budget intervention effects: its sign disagrees with regret change in roughly two thirds of evaluated seeds and with unsafe-selection change in more than four fifths.

But it simultaneously falsifies an overly broad "weak coupling" story. Some decision-aware predictive quantities can remain meaningfully associated with downstream outcomes; in particular, change in excluded-unsafe recall shows a moderate inverse relationship with change in unsafe selections.

The more defensible direction is therefore metric-specific:

**global discrimination metrics and downstream intervention effects can be directionally discordant, while decision-aligned predictive metrics may retain stronger coupling to the corresponding downstream endpoint.**

This distinction is more informative than claiming either universal coupling or universal decoupling.

## Mechanistic implication

The current evidence suggests separating metrics by where they operate in the decision pipeline:

1. **Global ranking metrics** such as ROC AUC summarize discrimination over the full candidate distribution.
2. **Decision-aligned metrics** such as recall among excluded unsafe candidates operate closer to the fixed-budget intervention boundary.
3. **Decision outcomes** such as unsafe selections and regret depend on the identities and ordering of candidates near that boundary.

A future mechanistic analysis should therefore ask whether local/boundary-aware metrics predict decision consequences more reliably than global discrimination metrics. That is a candidate research direction, not a result established by Experiment 161.

## Claim boundary

Experiment 161 does not establish a universal prediction–decision decoupling law, universal metric failure, beneficial poisoning, or deployment-relevant adversarial vulnerability. It is simulator-internal evidence that metric choice matters when evaluating the downstream consequences of model perturbations under a frozen fixed-budget decision rule.
