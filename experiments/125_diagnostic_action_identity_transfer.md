# Experiment 125 — diagnostic action-identity transfer

## Status

This hypothesis was formulated after inspecting the failed Experiment 123 target
population. Results on seeds 44111–44150 are therefore diagnostic, not a new
prospective confirmation.

## Results

| Frozen model | Target ROC AUC | 95% bootstrap CI |
|---|---:|---:|
| Action identity only | 0.785 | [0.772, 0.796] |
| Action + context support | 0.793 | [0.781, 0.805] |
| Action + support geometry | 0.792 | [0.780, 0.803] |
| Action + predicted loss | 0.756 | [0.741, 0.771] |
| Action + full geometry | 0.793 | [0.782, 0.805] |

At the frozen 0.5 threshold, action identity alone achieved balanced accuracy
0.768, unsafe recall 0.790, and unsafe precision 0.349. Adding context support
increased AUC by 0.00885, with paired bootstrap CI [0.00204, 0.01552].
Predicted loss reduced AUC by 0.0282 [-0.0340, -0.0223].

## Interpretation

Explicit action identity recovers most transferable discrimination. Context
support adds a small ranking improvement, while predicted loss is again harmful.
Because this representation was selected after target inspection, the result
cannot establish prospective portability.

Experiment 126 reconstructs a fourth unseen population (seeds 44151–44190).
Before that run, the confirmatory representation is frozen as action identity
plus context support, trained only on population 071–110. Experiment 127 will
score that model on the fourth population without modification.

## Artifacts

- `results/diagnostic_action_identity_transfer.csv`
- `results/diagnostic_action_identity_transfer_bootstrap.csv`
