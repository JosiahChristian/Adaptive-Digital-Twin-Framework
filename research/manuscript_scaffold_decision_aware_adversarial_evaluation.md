# Manuscript Scaffold: Decision-Aware Adversarial Evaluation Under Population Shift

## Working title

**When Model Metrics Are Not Enough: Decision-Layer Effects of Targeted Label Corruption Under Population Shift**

Alternative conservative title:

**Heterogeneous Downstream Effects of Targeted Label Corruption in a Fixed-Budget Adaptive Decision Pipeline**

## One-sentence contribution

We show in a controlled simulation study that the same targeted source-label corruption can produce harmful, beneficial, or mixed downstream effects across untouched shifted populations under a frozen fixed-budget intervention rule, while conventional model-level discrimination metrics do not consistently determine those decision outcomes.

## Abstract skeleton

### Background
Adaptive and safety-oriented ML systems are often evaluated primarily with model-level discrimination metrics even when deployment behavior is governed by a downstream intervention or selection rule.

### Objective
Test whether targeted source-label corruption produces decision effects that can be inferred reliably from global predictive metrics under population shift.

### Methods
Use a frozen hazard model family, targeted unsafe-to-safe label-concealment attack, fixed intervention-budget rule, preregistered hypotheses, independent untouched target populations, and seed-level paired/bootstrap analyses. Report unsafe selections and realized regret alongside ROC AUC, average precision, and intervention-aligned recall.

### Results
The same corruption caused materially different downstream effects across populations, including harm, benefit, and mixed endpoint changes. Several simpler hypotheses failed prospectively: constrained label repair did not reliably improve utility; broad weak coupling was not supported; an observed intervention-aligned metric hierarchy did not replicate. Global model metrics therefore did not provide a stable surrogate for downstream behavior.

### Conclusion
Adversarial evaluation of adaptive decision systems should include the actual decision layer and preserve population-specific outcome heterogeneity rather than inferring system-level consequences from model metrics alone.

## Introduction

1. Distinguish prediction quality from decision quality in pipelines where model scores feed a fixed budget or action rule.
2. Explain why adversarial label corruption is especially relevant: perturbations may alter ranking locally without uniformly changing global discrimination.
3. Identify the gap: standard robustness reporting often emphasizes AUC/AP or classifier loss while downstream policy consequences receive less direct testing.
4. State the narrow research question: under a frozen attack and intervention rule, are downstream effects stable across shifted populations and reliably reflected by model-level metrics?
5. State contribution without causal overreach.

## Methods

### Simulation and source population
Describe the adaptive digital-twin simulation environment, source action-level dataset, unsafe-action label, realized action regret, and context-support-distance feature.

### Hazard model
Standardized logistic regression with balanced class weighting and frozen feature set. Explicitly state that the model class was not tuned after prospective outcomes.

### Intervention rule
Explain the fixed top-N exclusion procedure and how coverage is derived from the clean source model using the frozen source-unsafe-recall rule. Emphasize identical exclusion counts within each target comparison.

### Targeted corruption
Unsafe-to-safe source-label concealment concentrated in the highest context-support-distance unsafe rows at the frozen dose.

### Prospective target populations
Describe independent untouched seed blocks and the commit-before-generation workflow used to maintain temporal separation between preregistration and target outcomes.

### Primary decision endpoints
- unsafe selected actions;
- total realized regret.

### Model-level metrics
- ROC AUC;
- average precision;
- excluded-unsafe recall at the intervention budget.

### Experimental sequence
Summarize the progression rather than presenting 150–165 as disconnected experiments:

1. establish targeted corruption vulnerability;
2. test a frozen label-audit mitigation and then a constrained audit;
3. diagnose unexpected downstream improvement on one shifted population;
4. replicate and test prediction–decision divergence prospectively;
5. synthesize cross-population heterogeneity;
6. test seed-level coupling and intervention-aligned metric hypotheses;
7. independently test the observed metric hierarchy.

### Statistical discipline
State preregistration criteria, untouched populations, 500/1,000 matched controls where applicable, 10,000 paired bootstrap resamples for metric-comparison experiments, and preservation of failed hypotheses.

## Results

### R1. Targeted corruption can materially degrade downstream intervention performance
Present the population where unsafe selections increased from 323 to 392 and regret increased from approximately 15.16 to 16.21 under the targeted attack.

### R2. Full-tail oracle auditing demonstrates recoverability but is structurally favorable
Present Experiment 151 as an upper-bound result, not an operational defense.

### R3. Constrained repair does not imply improved utility
Show the failed constrained-audit result and the clean-versus-poisoned reversal on its untouched population.

### R4. The downstream sign varies across populations
Present the cross-population table with harmful, beneficial, beneficial, and mixed outcomes under the same frozen perturbation.

### R5. Global predictive changes do not determine decision-effect direction
Present the prospective divergence and seed-level coupling results, including the failed broad weak-coupling criterion.

### R6. Intervention-aligned recall can be highly associated with unsafe-selection change, but the metric hierarchy is unstable
Present Experiment 163 followed immediately by the Experiment 165 non-replication. This paired presentation is essential to avoid cherry-picking.

## Proposed main figures

### Figure 1 — Study design and evidence progression
Diagram source model → targeted corruption → fixed-budget exclusion → target decisions, plus the preregistration/untouched-population sequence.

### Figure 2 — Cross-population downstream heterogeneity
For each untouched population, plot poison-minus-clean change in unsafe selections and regret. The visual should make sign reversals obvious.

### Figure 3 — Prediction metrics versus downstream effects
Seed-level scatterplots or rank plots comparing delta AUC, delta AP, and delta excluded-unsafe recall against delta unsafe selections and delta regret for the key prospective populations.

### Figure 4 — Replication failure of metric hierarchy
Side-by-side observed correlations and bootstrap intervals from Experiments 163 and 165.

## Proposed main tables

### Table 1 — Experimental chronology and preregistration status
Columns: experiment, target population, hypothesis, primary endpoints, prospective/retrospective status, pass/fail, interpretation.

### Table 2 — Cross-population clean vs poisoned decision outcomes
Unsafe selections, regret, AUC, AP, excluded-unsafe recall, and poison-minus-clean deltas.

### Table 3 — Claim/falsification matrix
Map each manuscript claim to supporting and contradicting experiments.

## Discussion

### Main finding
The tested adversarial perturbation does not have a single system-level effect under population shift. Downstream harm is mediated by the interaction between score perturbations, a fixed intervention rule, and target-population composition.

### Why global metrics can be insufficient
Whole-distribution ranking summaries can remain similar while local ordering near the intervention cutoff changes. This is a candidate explanation rather than a proven mechanism.

### Why negative results matter
The failed audit, weak-coupling, superiority, and hierarchy-replication tests eliminate attractive but overly simple narratives and strengthen the bounded conclusion.

### Practical implication
For ML components embedded in decision systems, robustness assessment should report the downstream policy/intervention endpoints directly, alongside standard predictive metrics.

### Limitations
- one simulator family;
- one primary hazard model class;
- one targeted label-concealment construction;
- fixed-budget intervention design;
- simulated regret/unsafe labels;
- no operational poison detector;
- no claim of deployment, clinical, biomedical, or aerospace validity;
- local boundary geometry remains a candidate mechanism requiring direct prospective testing.

## Conclusion

The strongest conclusion is methodological: adversarial robustness at the model layer cannot be assumed to translate monotonically to robustness at the decision layer under population shift. The actual intervention policy and downstream endpoints must be evaluated directly.

## Manuscript drafting rule

Every positive claim should be paired with the prospective experiment that could have falsified it. Failed preregistered hypotheses should remain visible in the main narrative rather than being moved entirely to supplementary material.
