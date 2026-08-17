# Publication Readiness Checklist — Decision-Aware Adversarial Evaluation

## Current status

The experimental sequence is sufficient for a serious manuscript draft centered on heterogeneous downstream effects and the necessity of decision-layer evaluation. It is **not** yet sufficient for a causal boundary-geometry claim.

## Ready now

- [x] Frozen source model family and feature set documented.
- [x] Targeted corruption construction documented.
- [x] Downstream intervention rule frozen within comparisons.
- [x] Multiple untouched target populations generated prospectively.
- [x] Harmful, beneficial, and mixed downstream outcomes preserved.
- [x] Negative preregistered experiments preserved.
- [x] Cross-population synthesis completed.
- [x] Seed-level metric/outcome analyses completed.
- [x] Independent metric-hierarchy replication attempted and failed.
- [x] Claim/falsification ledger created.
- [x] Manuscript scaffold created.
- [x] Scope and prohibited interpretations documented.

## Required before external submission

- [ ] Build one canonical experiment chronology table with commit/preregistration identifiers and target seed blocks.
- [ ] Build one canonical cross-population results table from machine-readable result files.
- [ ] Generate publication-quality figures for cross-population sign heterogeneity and metric/outcome relationships.
- [ ] Verify all manuscript numbers against source CSVs, not prose summaries.
- [ ] Add exact software/environment versions and reproducibility instructions.
- [ ] Add a data provenance section describing how each source and target dataset was generated.
- [ ] Add a statistical-analysis section explaining bootstrap design, independence assumptions, and why seed is used as the resampling unit.
- [ ] Add a threats-to-validity section covering simulator dependence, fixed-budget design, attack specificity, model-class specificity, and repeated hypothesis progression.
- [ ] Decide whether the decision-aware line is the primary paper or a secondary methodological study relative to the pre-decision harmful-expansion line.
- [ ] Perform a final claim audit: every abstract/conclusion sentence must map to the claim ledger.

## Optional strengthening work

### Direct boundary-geometry experiment
Only pursue if the goal is to promote the candidate mechanism from interpretation to evidence. Freeze local cutoff quantities before observing a new target population. Do not use another metric-hierarchy replication as a substitute.

### Additional model class
A prospectively frozen second model family could test whether heterogeneous decision effects are specific to logistic ranking geometry. This would be a generalization study, not a rescue experiment.

### Intervention-budget sensitivity
A prospectively frozen set of intervention budgets could test whether sign heterogeneity and local-boundary sensitivity persist outside the current operating point. This is important before making any budget-general claim.

## Stop rules

Do not launch new experiments merely because:

- a bootstrap interval narrowly crossed zero;
- a preferred metric lost its ordering on one population;
- a negative result makes the narrative less simple;
- another population might make a failed criterion significant.

Launch new work only when it tests a new preregistered mechanism, generalization dimension, or robustness boundary.

## Manuscript-safe headline

**The same targeted label corruption can have different downstream consequences across shifted populations under a frozen decision policy, and model-level metrics alone do not consistently characterize those system-level effects.**
