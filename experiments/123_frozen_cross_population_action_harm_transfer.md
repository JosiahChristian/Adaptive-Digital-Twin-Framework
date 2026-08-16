# Experiment 123 — frozen cross-population action-harm transfer

## Prospective protocol

The six representations were fixed before scoring the third population. Models
were fitted only on candidate-action rows from seeds 071–110 (7,881 rows; 1,640
unsafe) and then applied once, without refitting, sign correction, feature
selection, or threshold optimization, to seeds 44111–44150 (8,211 rows; 1,209
unsafe). Uncertainty used 5,000 outcome-stratified bootstrap resamples of the
untouched target population.

## Results

| Frozen representation | Target ROC AUC | 95% bootstrap CI |
|---|---:|---:|
| Context support only | 0.572 | [0.556, 0.587] |
| Context + action support | 0.569 | [0.553, 0.585] |
| Action support only | 0.558 | [0.543, 0.574] |
| Predicted loss only | 0.468 | [0.451, 0.486] |
| Context + predicted loss | 0.455 | [0.438, 0.471] |
| Context + predicted loss + action support | 0.452 | [0.435, 0.468] |

The frozen joint model underperformed context support alone by 0.120 AUC
(95% paired bootstrap CI [-0.138, -0.102]; probability of a positive
difference = 0/5,000). It also underperformed action support alone by 0.107
[-0.127, -0.086].

At the frozen 0.5 threshold, all models had balanced accuracy below 0.477. Thus
even the above-chance rankings from the support-only models were not calibrated
for direct target-population classification.

## Conclusion

The joint support/loss harm representation does **not** transfer prospectively
to the third population. Its target AUC is significantly below chance. The
failure is not a marginal loss of accuracy: predicted action loss reverses the
useful ordering supplied by support geometry, and the frozen decision threshold
is badly miscalibrated.

The proper scientific conclusion is falsification of portability, not
validation. Support geometry retains weak ranking information, but neither the
joint coefficients nor the 0.5 operating threshold can be treated as invariant
across populations.

## Next test

Experiment 124 audits covariate drift, label-conditional drift, prevalence
shift, and feature/outcome direction reversal. This is explanatory diagnosis;
it will not retroactively alter the frozen Experiment 123 result.

## Artifacts

- `results/frozen_cross_population_action_harm_transfer.csv`
- `results/frozen_cross_population_action_harm_transfer_bootstrap.csv`
- `results/frozen_cross_population_action_harm_transfer_coefficients.csv`
