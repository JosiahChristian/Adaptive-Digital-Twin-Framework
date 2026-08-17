# Experiment 154 preregistration: diagnose apparent poisoning benefit under population shift

## Motivation
Experiment 153 produced a prospective falsification result: on the untouched 44551-44590 population, the clean model selected more unsafe actions and incurred more regret than the 20% targeted-poisoning model, while the constrained audit did not improve either endpoint. This experiment diagnoses that reversal without changing the model family or intervention policy.

## Frozen models and target
Use the same source population, clean labels, 20% targeted unsafe-to-safe concealment attack, features, logistic model, source-derived 80% unsafe-recall threshold rule, and untouched target population from Experiment 153.

## Diagnostic questions
At the identical frozen target exclusion count, compare clean and poisoned models on:

1. target candidate-level ROC AUC for `unsafe_action`;
2. target candidate-level average precision;
3. unsafe recall inside the excluded top-N hazard set;
4. mean and median predicted hazard score for truly unsafe target rows;
5. mean and median predicted hazard score for truly safe target rows;
6. overlap/Jaccard similarity of the clean and poisoned top-N exclusion sets;
7. counts of rows excluded by clean only, poisoned only, and both;
8. unsafe prevalence in the clean-only and poisoned-only exclusion sets;
9. intervention-selected action changes between clean and poisoned models, including transitions safe->unsafe and unsafe->safe;
10. regret differences on contexts where the selected action differs.

## Hypothesis classification
No directional pass/fail claim is preregistered. This is a mechanism-discrimination experiment. Results should be interpreted using the following predeclared patterns:

- **Ranking-improvement pattern:** poisoned model has higher AUC/AP and/or higher unsafe recall at fixed top-N coverage, suggesting the label concealment acted like an accidental regularizer under this population shift.
- **Decision-boundary interaction pattern:** global ranking metrics are unchanged or worse, but the poisoned-only exclusion set is enriched for candidates that alter final action selection beneficially, suggesting the intervention policy is sensitive to local top-N ordering rather than global hazard discrimination.
- **Mixed pattern:** evidence supports both mechanisms.
- **Unresolved:** neither pattern is supported clearly.

## Interpretation boundary
This experiment cannot establish that poisoning is beneficial in general. It diagnoses one prospective population where a specific targeted contamination unexpectedly improved downstream intervention endpoints. Any mitigation redesign must wait until this diagnostic is complete.
