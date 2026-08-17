# Decision-Aware Evidence Synthesis Through Experiment 165

## Purpose

This synthesis consolidates the poisoning/decision experiments into one bounded research story. It preserves positive, negative, and mixed preregistered results and does not reinterpret failed tests as successes.

## Evidence progression

### 1. A fixed-budget decision effect appeared

Targeted source-label corruption sometimes worsened downstream intervention outcomes and sometimes improved them, despite the attack, model family, and fixed intervention-budget rule remaining frozen. This immediately ruled out any universal claim that poisoning is either uniformly harmful or beneficial at the downstream decision layer.

### 2. Population shift changed the sign of downstream effects

Across independent untouched populations, the same targeted corruption produced harmful, beneficial, and mixed changes in unsafe selections and realized regret. Global ranking metrics did not uniquely determine the sign of those downstream effects. The replicated phenomenon is therefore **heterogeneity of decision consequences under population shift**, not a poisoning benefit.

### 3. The simple repair story failed

A constrained context-tail audit did not reliably improve downstream performance even though it recovered some poisoned labels. On one untouched population, the poisoned intervention outperformed the clean intervention. This falsified the assumption that increasing source-label fidelity must monotonically improve fixed-budget downstream utility.

### 4. Global prediction and downstream decisions are not interchangeable

Prospective tests showed frequent directional disagreement between changes in global prediction metrics and changes in unsafe selections or regret. However, the preregistered broad weak-coupling hypothesis failed because some predictive quantities retained meaningful associations with downstream endpoints. The defensible conclusion is therefore metric- and population-dependent rather than universal decoupling.

### 5. Intervention-aligned recall was strong once, but its hierarchy did not replicate

Experiment 163 found that excluded-unsafe recall tracked unsafe-selection change with Spearman rho -0.907622 and regret change with rho -0.804072 across 40 fresh generation seeds. It substantially outperformed ROC AUC for unsafe-selection association, while the superiority over average precision narrowly missed the preregistered bootstrap criterion.

Experiment 165 then prospectively tested the observed hierarchy on another untouched 40-seed population. It failed to replicate. Excluded-unsafe recall retained the largest absolute association with unsafe-selection change (rho -0.534196), but AP and AUC changed ordering and neither paired-bootstrap superiority interval stayed above zero. For regret, AUC had the largest absolute observed association on that population.

The retained conclusion is therefore: **metric usefulness itself varies by population and endpoint; no stable universal hierarchy among excluded-unsafe recall, AP, and ROC AUC has been established.**

## Current mechanistic model

The accumulated evidence is consistent with, but does not yet prove, a local cutoff mechanism:

1. a model perturbation changes candidate hazard scores;
2. only some score changes alter ordering near the fixed intervention cutoff;
3. local rank turnover changes which candidates are excluded;
4. the safe/unsafe composition and downstream cost of those switched candidates determine intervention outcomes;
5. whole-distribution metrics may underweight these local changes.

The key unresolved question is whether directly measured local boundary geometry prospectively explains outcome sensitivity better than global summary metrics across populations.

## Strongest current bounded claim

Within the tested simulator, attack, hazard model, and frozen fixed-budget intervention procedure, **targeted label corruption has heterogeneous downstream consequences across shifted populations, and model-level predictive metrics alone are insufficient to characterize those consequences consistently. Decision-layer evaluation is therefore necessary in addition to global discrimination metrics.**

This statement is stronger than any claim that one predictive metric is universally superior and weaker than a causal claim about boundary geometry.

## Claims that did not survive falsification

The evidence does not support any of the following:

- targeted poisoning always worsens downstream utility;
- targeted poisoning is beneficial;
- restoring more corrupted labels necessarily improves downstream utility;
- prediction and decision metrics are universally weakly coupled;
- excluded-unsafe recall is universally superior to AP or ROC AUC;
- the recall > AP > AUC hierarchy is stable across populations;
- the local cutoff mechanism has already been causally established.

## Publication framing

The decision-aware poisoning line is best framed as a methodological result about **evaluation under adversarial perturbation and population shift**. The central contribution is not an attack-success story or a metric leaderboard. It is evidence that conclusions drawn from model-level discrimination can fail to predict the sign and magnitude of downstream decision effects under a frozen intervention rule.

A publication-grade manuscript should foreground preregistration, untouched-population replication, heterogeneous outcomes, and explicit failed hypotheses. Negative experiments are part of the contribution because they eliminate simpler narratives.

## Next evidence gate

Do not launch another metric-hierarchy replication. A genuinely new experiment is justified only if it tests the candidate mechanism directly. Such a test should prospectively freeze local cutoff quantities, for example:

- score gap immediately across the intervention cutoff;
- candidate density within a fixed score neighborhood of the cutoff;
- clean-to-perturbed rank turnover near the cutoff;
- unsafe/safe composition of the switched set;
- perturbation magnitude among cutoff-crossing candidates.

The next mechanistic test should compare these direct local quantities against global AUC/AP and simple baselines on untouched populations, with the primary explanatory criterion frozen in advance.

## Scope limits

These are simulator-internal findings. They do not establish deployment safety, universal adversarial robustness, clinical validity, biomedical validity, transfer across model classes, transfer across attacks, or invariance across intervention budgets.
