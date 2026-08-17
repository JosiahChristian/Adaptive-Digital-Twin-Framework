# Publication Claim and Falsification Ledger

## Purpose

This ledger separates supported claims, partial evidence, falsified hypotheses, and prohibited interpretations for the decision-aware adversarial-label-corruption line. It is intended to prevent retrospective overclaiming when manuscript text is drafted.

## Supported claims

### S1. Targeted label corruption can materially change downstream fixed-budget decisions
Supported by prospective poisoning experiments in which the same intervention policy produced measurable changes in unsafe selections and realized regret after targeted unsafe-to-safe source-label concealment.

### S2. The sign of the downstream effect is population-dependent
Across independent untouched target populations, the same frozen corruption and intervention procedure produced harmful, beneficial, and mixed changes in downstream endpoints.

### S3. Source-label fidelity and downstream utility are not monotonically linked under the tested procedure
The constrained label-audit experiment failed to improve the poisoned intervention on an untouched population, and the poisoned intervention outperformed the clean intervention on that population.

### S4. Global discrimination metrics alone do not consistently characterize downstream intervention consequences
ROC AUC and average precision sometimes moved in directions that did not match unsafe-selection or regret changes. Their relationships to downstream endpoints varied across populations.

### S5. Decision-layer evaluation is necessary for this fixed-budget adversarial decision pipeline
Because identical or similar model-level metric changes can coexist with different downstream outcomes, evaluation of the actual selection/exclusion policy is required in addition to model-level metrics.

## Partial or population-specific evidence

### P1. Excluded-unsafe recall can be highly informative
Experiment 163 showed very strong seed-level association between excluded-unsafe recall change and downstream unsafe-selection/regret change. This supports intervention-aligned measurement as a useful diagnostic on some populations.

### P2. A local cutoff mechanism is plausible
Boundary-turnover diagnostics and the fixed top-N design are consistent with the hypothesis that local score/rank changes near the intervention cutoff drive downstream sensitivity. This remains mechanistic inference, not established causality.

## Falsified or failed preregistered hypotheses

### F1. A constrained context-tail audit reliably mitigates the targeted attack
Failed. The constrained audit did not improve either primary downstream endpoint relative to the poisoned model on its untouched target population.

### F2. Targeted poisoning has a consistently harmful downstream sign
Falsified by untouched populations where the poisoned intervention had fewer unsafe selections and lower regret than the clean intervention.

### F3. Targeted poisoning has a consistently beneficial downstream sign
Falsified by populations where poisoning substantially worsened unsafe selections and regret, and by a population with mixed endpoint effects.

### F4. Prediction and decision effects are broadly weakly coupled
The preregistered seed-level weak-coupling criterion failed because at least one intervention-aligned predictive quantity showed a meaningful association with downstream effects.

### F5. Excluded-unsafe recall is prospectively superior to both ROC AUC and AP
Experiment 163 did not pass the full superiority criterion because the recall-versus-AP bootstrap interval crossed zero.

### F6. The hierarchy recall > AP > AUC replicates across untouched populations
Experiment 165 failed the preregistered hierarchy replication. The hierarchy was not stable and bootstrap superiority intervals crossed zero.

## Prohibited manuscript interpretations

Do not state or imply that:

- poisoning improves safety;
- degraded prediction improves control;
- ROC AUC or AP are useless;
- excluded-unsafe recall is universally optimal;
- label repair is harmful in general;
- the local cutoff mechanism has been proven causal;
- the findings generalize beyond the tested simulator, attack, hazard model, intervention budget, or population-generation process;
- the results establish operational, biomedical, clinical, aerospace, or deployment safety.

## Manuscript-safe central claim

Within the tested simulation and frozen fixed-budget intervention procedure, targeted source-label corruption produced heterogeneous downstream consequences across shifted target populations. Model-level discrimination metrics did not consistently determine the sign or magnitude of these decision effects, so adversarial evaluation at the actual decision layer was necessary to characterize system behavior.

## Evidence standard for future promotion

A stronger causal/mechanistic claim requires a prospectively specified experiment that directly measures local cutoff geometry on untouched populations and demonstrates reproducible explanatory or predictive advantage over global metrics and simple baselines. Repeating failed metric-hierarchy tests without a new mechanistic hypothesis is not sufficient.
