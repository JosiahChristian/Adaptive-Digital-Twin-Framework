# Experiment 129 — source-only probability calibration diagnostic

## Purpose

Determine whether Experiment 127's overconfidence comes from class-balanced
logistic fitting rather than failure of the ranking representation. Every model
was fitted or corrected using population 071–110 only; population 151–190 was
evaluation-only. Because the alternatives were compared after exposure to the
fourth population, selection requires a fifth prospective population.

## Results

| Source-only specification | AUC | Brier | Log loss | ECE | Mean risk |
|---|---:|---:|---:|---:|---:|
| Balanced logistic | 0.829 | 0.161 | 0.496 | 0.184 | 0.378 |
| Unweighted logistic | 0.831 | 0.131 | 0.406 | 0.070 | 0.183 |
| Balanced + source-prior correction | 0.829 | **0.131** | **0.399** | **0.063** | 0.172 |

Observed target prevalence was 0.195. The source-prior correction applies an
intercept offset derived solely from the 071–110 unsafe prevalence (0.208);
it does not use target labels.

## Conclusion

Much of the probability error was induced by class weighting, which implicitly
centers the fitted prior near 0.5. Source-prior correction preserved ranking and
substantially improved all probability metrics. The frozen 0.5 threshold is no
longer an appropriate operating rule after calibration and is not treated as a
primary endpoint.

Experiments 130–131 prospectively test the source-prior-corrected probabilities
on a fifth untouched population. Primary endpoints are Brier score, log loss,
ECE, and mean-risk/prevalence error.

## Artifacts

- `results/source_only_probability_calibration_diagnostic.csv`
- `results/source_only_probability_calibration_bins.csv`
