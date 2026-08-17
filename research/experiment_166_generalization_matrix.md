# Experiment 166 Mechanism Generalization Matrix

## Purpose

Experiment 166 provides the first direct prospective support for the local cutoff-geometry mechanism in the frozen ADT simulator pipeline. This document defines the dimensions along which that result must be challenged before the mechanism can be described as robust rather than configuration-specific.

This is a synthesis/planning artifact, not a preregistration. Exact experimental criteria belong in separately frozen preregistration documents before any target outcomes are inspected.

## Current anchor result

Experiment 166 passed both preregistered co-primary criteria on an untouched 40-seed population:

- cutoff localization: Mantel–Haenszel common odds ratio 10.567477, 95% CI [8.345537, 13.380992];
- boundary-composition association: Spearman rho -0.873179, 10,000-bootstrap 95% CI [-0.946362, -0.735018].

There were 308 exclusion-membership switches, 50.3247% within the frozen closest-10% cutoff band, despite mean clean/poisoned exclusion-set Jaccard overlap 0.923823.

The result supports a local operating-boundary mechanism inside the tested configuration. It does not establish invariance.

## Generalization dimensions

| Dimension | What must change | What should remain frozen where possible | Scientific question | Failure meaning |
|---|---|---|---|---|
| Intervention budget | exclusion/selection budget | attack, model, population generator, boundary definitions | Does localization/composition survive a changed operating cutoff? | Mechanism may depend on one budget regime |
| Population family | target population-generating regime | model, attack, budget, mechanism criteria | Does the mechanism survive meaningful population shift? | Current support may be population-family-specific |
| Attack mechanism | corruption/perturbation process | model, budget, population family, mechanism endpoints | Is cutoff geometry a general perturbation-to-decision mechanism or attack-specific? | Mechanism may be peculiar to targeted source-label corruption |
| Model class | hazard-model specification | attack, budget, population family, mechanism criteria | Does the mechanism survive different score geometry? | Current result may depend on one model's ranking structure |
| Cutoff neighborhood | preregistered boundary width/definition | all upstream conditions | Is the localization result robust to reasonable boundary definitions? | Evidence may depend on a narrow operationalization |
| Effect sign | populations/conditions producing improvement, degradation, or near-zero effect | sign-prediction rule | Can boundary composition prospectively predict consequence direction? | Mechanism may explain outcomes retrospectively without predictive value |

## Recommended order

### Gate G1 — intervention-budget shift

This is the cleanest immediate falsification because it changes the decision boundary while leaving most of the upstream simulator/model/attack pipeline intact. The mechanism should not be considered budget-robust until prospectively tested at materially different budgets.

### Gate G2 — fresh population-family replication

A fresh seed sample from effectively the same generator is weaker than a meaningful population-family shift. The next population test should alter a scientifically interpretable generating condition while freezing the mechanism criteria in advance.

### Gate G3 — attack shift

Repeat the mechanism test under a perturbation that is meaningfully distinct from targeted source-label corruption. This is necessary before describing cutoff geometry as a perturbation-general mechanism.

### Gate G4 — model-class shift

A changed hazard model should alter score geometry enough to challenge whether the mechanism is tied to one estimator's ranking behavior.

### Gate G5 — prospective sign prediction

The strongest mechanistic promotion would occur if pre-outcome boundary quantities can prospectively predict whether a perturbation will increase, decrease, or negligibly change unsafe selections. The prediction rule and indifference region must be frozen before outcomes.

## Promotion ladder

**Current:** prospectively supported, simulator/configuration-specific mechanism.

**After G1 + G2 survive:** evidence for robustness across operating conditions and meaningful population variation.

**After attack/model shifts survive:** evidence for broader computational generality inside the research framework.

**After prospective sign prediction survives:** substantially stronger evidence that boundary composition is predictively mechanistic rather than merely explanatory.

None of these stages alone establishes deployment safety, real cyber-physical transfer, biomedical applicability, or a universal causal law.

## Stopping/falsification discipline

A failed gate remains part of the evidence record. The mechanism should be narrowed to the conditions that survive rather than repeatedly changing thresholds, boundary widths, populations, or endpoints until significance appears. Any rescue hypothesis generated after a failure must be labeled exploratory and receive a new prospective test on untouched data.
