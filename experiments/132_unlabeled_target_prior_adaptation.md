# Experiment 132 — unlabeled target-prior adaptation diagnostic

## Method

Starting from the source-prior-corrected probabilities, an EM label-shift update
estimated target prevalence from the unlabeled target score distribution. Unsafe
labels were not used during adaptation. Labels were opened only for evaluation.

## Results

| Metric | Fixed source prior | Unlabeled EM |
|---|---:|---:|
| Estimated/assumed prior | 0.208 | 0.099 |
| Observed prevalence | 0.132 | 0.132 |
| Mean-risk error | 0.048 | **0.033** |
| Brier score | 0.1224 | **0.1220** |
| Log loss | 0.4046 | **0.4009** |
| ECE | 0.0797 | **0.0711** |
| AUC | 0.760 | 0.760 |

## Conclusion

Unlabeled EM adaptation yields consistent but small calibration improvements and
preserves ranking. It underestimates target prevalence, so it does not solve the
problem. Because the method was selected after examining the fifth population,
Experiment 134 must confirm it on a sixth untouched population.
