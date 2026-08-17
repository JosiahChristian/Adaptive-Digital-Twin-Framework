# Experiment 131 — preregistered fifth-population calibration confirmation

## Protocol

The primary model was the class-balanced action-identity-plus-context logistic
model trained only on population 071–110, followed by a fixed log-odds intercept
correction using the source unsafe prevalence (20.81%). The fifth-population
outcomes did not inform fitting or correction.

## Results

| Metric | Source-prior corrected | Balanced uncorrected |
|---|---:|---:|
| ROC AUC | 0.760 | 0.760 |
| Brier score | **0.122** | 0.187 |
| Log loss | **0.405** | 0.594 |
| 10-bin ECE | **0.080** | 0.261 |
| Mean predicted risk | 0.180 | 0.381 |
| Observed unsafe prevalence | 0.132 | 0.132 |
| Absolute prevalence error | **0.048** | 0.249 |

## Conclusion

The source-prior correction prospectively and materially improves probability
quality without changing ranking. This confirms that the balanced model's
overconfidence is largely a prior distortion.

Calibration is improved, not solved. Unsafe prevalence shifted from 20.81% in
the training population to 13.17% in the fifth population, leaving a 4.8-point
mean-risk error and ECE 0.080. A fixed source prior cannot fully absorb changing
target prevalence.

Experiment 132 evaluates an unlabeled score-distribution EM prior adjustment.
That is a post-confirmation diagnostic on this exposed population and requires a
new prospective population before any portability claim.

## Artifacts

- `results/preregistered_fifth_population_calibration.csv`
- `results/preregistered_fifth_population_calibration_bins.csv`
