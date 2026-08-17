# Experiment 166 — Cutoff-Geometry Mechanism Interpretation

## Preregistered result

Experiment 166 prospectively adjudicated the local cutoff-geometry hypothesis on 40 frozen generation seeds after the target population and inferential criteria had been fixed.

The preregistered primary mechanism-support flag **passed**.

Key results:

- poison count: 328
- source exclusion coverage: 0.390179
- primary near-cutoff fraction: 0.100000
- Mantel–Haenszel common odds ratio for cutoff localization: **10.567477**
- 95% interval: **[8.345537, 13.380992]**
- CMH two-sided p-value: effectively 0 in the committed summary
- criterion 1 (cutoff localization): **pass**
- Spearman rho between net unsafe crossing and unsafe-selection change: **-0.873179**
- bootstrap interval: **[-0.946362, -0.735018]**
- criterion 2 (composition direction): **pass**
- primary cutoff-geometry mechanism support: **pass**

Across all seeds there were 308 membership switches, 50.3247% of which occurred near the preregistered cutoff region. Mean exclusion-set Jaccard overlap remained high at 0.923823, showing that the intervention sets were globally similar even while consequential local membership changes occurred.

## Mechanistic interpretation

This experiment materially strengthens the previously inferred boundary mechanism.

The evidence now directly supports two prospectively specified components:

1. **Localization:** membership changes caused by the perturbation are strongly concentrated near the fixed-budget intervention cutoff rather than being uniformly distributed across the ranking.
2. **Composition:** the net safety composition of those crossings strongly tracks the change in downstream unsafe selections.

Together, these findings explain how relatively small score perturbations can produce meaningful decision changes without requiring large changes in global discrimination metrics. A fixed-budget decision is sensitive to which candidates cross its boundary, not merely to aggregate ranking quality over the entire population.

## Important asymmetry in the result

The committed transition counts show 12 unsafe-to-safe versus 121 safe-to-unsafe switches, and the mean global predictive deltas are negative (AUC -0.040164, AP -0.063054, excluded-unsafe recall -0.044180). Experiment 166 therefore must not be framed as evidence of a beneficial perturbation. In this target population, the directly observed boundary mechanism accompanies predominantly harmful safety-composition changes.

That is scientifically useful: it separates the **mechanism** from the **sign of its consequence**. Boundary reordering can explain either beneficial or harmful downstream changes depending on which candidates cross the cutoff.

## Strongest defensible claim after Experiment 166

Within the tested simulator, attack, and frozen fixed-budget intervention procedure, model perturbations can alter downstream safety outcomes through **localized rank/membership changes near the intervention cutoff**, and the safety composition of those boundary crossings is strongly associated with the resulting change in unsafe selections.

This is stronger than the earlier metric-proxy interpretation because Experiment 166 directly tests the proposed local mechanism prospectively.

## What remains unproven

Experiment 166 does not establish:

- that cutoff geometry is the only mechanism linking model perturbation to decision consequences;
- that the same localization strength holds at other intervention budgets;
- transfer to another attack mechanism, model class, simulator, or domain;
- causal sufficiency of any single boundary statistic;
- deployment relevance or real cyber-physical safety;
- beneficial poisoning or useful adversarial regularization.

## Next falsification gates

Before promoting the mechanism beyond a simulator-specific result, the strongest tests would be:

1. **budget shift:** freeze substantially different intervention budgets and test whether localization/composition predictions survive;
2. **attack shift:** repeat under a meaningfully different perturbation mechanism;
3. **population replication:** reproduce the preregistered mechanism criteria on another untouched population;
4. **model shift:** test whether the mechanism survives a changed hazard-model specification;
5. **sign prediction:** prospectively predict whether boundary composition implies improvement, degradation, or negligible decision change before observing the downstream endpoint.

These are strengthening/falsification stages. Experiment 166 itself should remain immutable as the first direct prospective mechanism test.
