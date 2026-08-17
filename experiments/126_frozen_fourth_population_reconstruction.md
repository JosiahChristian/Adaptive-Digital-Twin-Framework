# Experiment 126 — frozen fourth-population reconstruction

## Purpose

Generate a new, untouched population for prospective confirmation of the
action-aware hypothesis developed after Experiments 123–125.

## Integrity controls

Before seeds 44151–44190 were generated:

- the primary Experiment 127 representation was frozen as action identity plus
  context support;
- training was frozen to population 071–110;
- the 0.5 threshold, ROC-AUC primary endpoint, comparators, and 5,000-bootstrap
  analysis were committed;
- no fourth-population outcome informed model selection or fitting.

The reconstruction produced 9,435 candidate-action rows, including 1,841 unsafe
and 7,594 safe outcomes.

## Artifacts

- `results/prospective_action_conditioned_support_representation_151_190.csv`
- `results/prospective_action_conditioned_support_representation_folds_151_190.csv`
- `results/prospective_action_conditioned_support_representation_actions_151_190.csv`
- `results/prospective_action_conditioned_support_representation_coefficients_151_190.csv`
