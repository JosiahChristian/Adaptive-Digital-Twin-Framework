# Decision-Aware Evidence Synthesis Through Experiment 166

## Purpose

This synthesis consolidates the poisoning/decision experiments into one bounded research story. It preserves positive, negative, mixed, and failed preregistered results and does not reinterpret failed tests as successes.

## Evidence progression

### 1. A fixed-budget decision effect appeared

Targeted source-label corruption sometimes worsened downstream intervention outcomes and sometimes improved them, despite the attack, model family, and fixed intervention-budget rule remaining frozen. This ruled out any universal claim that poisoning is either uniformly harmful or beneficial at the downstream decision layer.

### 2. Population shift changed the sign of downstream effects

Across independent untouched populations, the same targeted corruption produced harmful, favorable, and mixed changes in unsafe selections and realized regret. Global ranking metrics did not uniquely determine the sign of those downstream effects. The replicated phenomenon is therefore **heterogeneity of decision consequences under population shift**, not a poisoning benefit.

### 3. The simple repair story failed

A constrained context-tail audit did not reliably improve downstream performance even though it recovered some poisoned labels. On one untouched population, the poisoned intervention outperformed the clean intervention. This falsified the assumption that increasing source-label fidelity must monotonically improve fixed-budget downstream utility.

### 4. Global prediction and downstream decisions are not interchangeable

Prospective tests showed directional disagreement between changes in global prediction metrics and changes in unsafe selections or regret. However, the preregistered broad weak-coupling hypothesis failed because some predictive quantities retained meaningful associations with downstream endpoints. The defensible conclusion is therefore metric- and population-dependent rather than universal decoupling.

### 5. Intervention-aligned recall was strong once, but its hierarchy did not replicate

Experiment 163 found that excluded-unsafe recall tracked unsafe-selection change with Spearman rho -0.907622 and regret change with rho -0.804072 across 40 fresh generation seeds. It substantially outperformed ROC AUC for unsafe-selection association, while superiority over average precision narrowly missed the preregistered bootstrap criterion.

Experiment 165 prospectively tested the observed recall > AP > AUC hierarchy on another untouched 40-seed population. It failed to replicate. Excluded-unsafe recall retained the largest absolute association with unsafe-selection change (rho -0.534196), but AP and AUC changed ordering and neither paired-bootstrap superiority interval stayed above zero. For regret, AUC had the largest absolute observed association on that population.

The retained conclusion is therefore: **metric usefulness varies by population and endpoint; no stable universal hierarchy among excluded-unsafe recall, AP, and ROC AUC has been established.**

### 6. Experiment 166 prospectively supported a local cutoff-geometry mechanism inside the frozen pipeline

Experiment 166 directly tested the cutoff hypothesis generated diagnostically in Experiment 154 on an untouched 40-seed population. The primary near-cutoff band was frozen at the closest 10% of candidate rows before target adjudication.

Membership switches were strongly enriched near the cutoff: Mantel–Haenszel common odds ratio 10.567477 with 95% CI [8.345537, 13.380992]. The seed-level net unsafe-crossing quantity was strongly negatively associated with downstream unsafe-selection change: Spearman rho -0.873179 with a 10,000-bootstrap 95% CI [-0.946362, -0.735018]. Both preregistered co-primary criteria passed.

Across all seeds there were 308 exclusion-membership switches, 50.3247% of which occurred within the frozen near-cutoff band, while mean clean/poison exclusion-set Jaccard overlap remained high at 0.923823. This is consistent with consequential local reordering under high global set overlap.

The result promotes the local cutoff hypothesis from diagnostic plausibility to **prospective simulator-internal support**, but it does not establish causal sufficiency, independence from structural or mathematical coupling to the unsafe-selection endpoint, or invariance across budgets, populations, attacks, model classes, or cutoff definitions.

## Current mechanistic model

The accumulated evidence supports the following bounded account within the tested fixed-budget pipeline:

1. a model perturbation changes candidate hazard scores;
2. only some score changes alter intervention membership near the fixed cutoff;
3. local membership turnover changes which candidates are excluded;
4. the safe/unsafe composition of those boundary crossings is strongly associated with downstream unsafe-selection changes;
5. whole-distribution metrics can underweight these local operating-boundary changes.

This account is prospectively supported in Experiment 166 but remains subject to external adversarial review, especially regarding unit of analysis, inferential assumptions, mathematical coupling, and alternative explanations such as generic ranking instability.

## Strongest current bounded claim

Within the tested simulator, attack, hazard model, population generator, and frozen fixed-budget intervention procedure, **targeted label corruption has heterogeneous downstream consequences across shifted populations; global predictive metrics alone do not characterize those consequences consistently; and a preregistered prospective test found perturbation-induced membership changes concentrated near the intervention cutoff, with boundary-crossing safety composition strongly associated with downstream unsafe-selection changes.**

This is stronger than a purely descriptive metric-proxy account and weaker than a universal causal mechanism claim.

## Claims that did not survive falsification

The evidence does not support any of the following:

- targeted poisoning always worsens downstream utility;
- targeted poisoning is beneficial;
- restoring more corrupted labels necessarily improves downstream utility;
- prediction and decision metrics are universally weakly coupled;
- excluded-unsafe recall is universally superior to AP or ROC AUC;
- the recall > AP > AUC hierarchy is stable across populations.

Experiment 166 does not rescue any of these failed claims.

## Claims still not established

The evidence does not yet establish:

- that cutoff geometry is causally sufficient for the downstream effect;
- that the Experiment 166 association is free of structural or mathematical coupling to the unsafe-selection endpoint;
- that the inferential unit and dependence assumptions are fully resolved;
- that the mechanism survives materially different intervention budgets;
- that it survives a meaningful population-family shift rather than another seed sample from the same generator;
- that it transfers across attack mechanisms or model classes;
- that boundary composition can prospectively predict effect sign;
- deployment safety, universal adversarial robustness, clinical validity, or biomedical validity.

## Publication framing

The decision-aware poisoning line is best framed as a methodological result about **evaluation under adversarial perturbation, population shift, and fixed-budget decision rules**. The central contribution is not an attack-success story or a metric leaderboard. It is evidence that model-level discrimination can fail to characterize downstream decision effects consistently and that local operating-boundary behavior can carry information not captured by whole-distribution summaries.

A publication-grade manuscript should foreground preregistration, untouched-population tests, heterogeneous outcomes, failed hypotheses, and the distinction between prospective mechanism support and universal causal proof. Negative experiments remain part of the contribution because they eliminate simpler narratives.

## Current evidence gate while external review is pending

Do not launch a new mechanism-generalization experiment solely because Experiment 166 was favorable. The external pre-quadrangulation review should first challenge the current result for:

- unit-of-analysis validity;
- membership-switch dependence;
- mathematical/structural coupling between boundary composition and unsafe-selection change;
- Mantel–Haenszel appropriateness;
- preregistration fidelity;
- alternative ranking-instability explanations;
- causal-language inflation.

Until that review is reconciled, manuscript Abstract/Discussion/conclusion language should remain bounded to prospective association/mechanism support in the tested pipeline.

If the Experiment 166 line survives that review, the next scientific gates are materially different intervention budgets, meaningful population-family shift, attack shift, model-class shift, and finally prospectively frozen effect-sign prediction.

## Scope limits

These are simulator-internal findings. They do not establish deployment safety, universal adversarial robustness, clinical validity, biomedical validity, transfer across arbitrary cyber-physical systems, or invariance across intervention budgets, attacks, models, or population families.
