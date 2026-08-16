# Experiment 122 — frozen third-population support reconstruction

## Purpose

Reconstruct a genuinely unseen seed population (44111–44150) after freezing the candidate-action support representation used before this run. No Experiment 118–121 harm model was fitted or tuned on these seeds before reconstruction.

## Design

- 40 unseen generation seeds: 44111–44150.
- Three candidate actions evaluated at every eligible context.
- Exported context support distance, action-conditioned support distance, predicted action loss, relative loss, realized regret, and unsafe-action label.
- Leave-one-seed-out diagnostics are descriptive reconstruction checks, not the frozen prospective transfer test.
- The controller-event feature set from Experiment 118 is not fully present in this export, so Experiment 122 cannot by itself validate that 11-state-feature model.

## Results

The reconstruction produced 8,211 candidate-action rows: 1,209 unsafe and 7,002 safe (14.72% unsafe).

| Descriptive model | Pooled ROC AUC | Mean held-seed ROC AUC |
|---|---:|---:|
| Context support + predicted loss + action support | 0.550 | 0.563 |
| Context support + predicted loss | 0.540 | 0.547 |
| Predicted loss only | 0.529 | 0.535 |
| Context + action support | 0.518 | 0.527 |
| Action support only | 0.442 | 0.432 |
| Context support only | 0.430 | 0.420 |

For the three-variable joint representation, coefficient directions were stable across all 40 leave-one-seed-out folds: context support negative, action support positive, and predicted loss positive. Stability of sign does not compensate for weak discrimination.

## Interpretation

This population is materially harder than the earlier populations for the support-geometry proxy. The best descriptive AUC is only 0.550 pooled and 0.563 averaged across held-out seeds. Raw context or action support distance alone is directionally inverted and below chance; their contrast becomes useful only jointly with predicted loss. This falsifies any claim that support distance alone is a portable harm discriminator.

The prospective boundary remains intact. Experiment 123 fits the predeclared representations only on the earlier 071–110 population and scores 44111–44150 once, without refitting or threshold selection on the third population.

## Artifacts

- `results/prospective_action_conditioned_support_representation_111_150.csv`
- `results/prospective_action_conditioned_support_representation_folds_111_150.csv`
- `results/prospective_action_conditioned_support_representation_actions_111_150.csv`
- `results/prospective_action_conditioned_support_representation_coefficients_111_150.csv`
