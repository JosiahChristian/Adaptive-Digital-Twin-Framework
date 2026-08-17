# Experiment 128 — seed-cluster robustness and calibration audit

## Purpose

Stress-test Experiment 127 against within-seed dependence, seed heterogeneity,
and probability miscalibration. The frozen 071–110 models were reconstructed
and applied unchanged to the fourth population.

## Seed-cluster inference

Resampling all rows independently can overstate precision because candidate
actions from one generated seed share trajectory structure. Therefore 5,000
bootstrap replicates sampled the 40 generation seeds as whole clusters.

| Quantity | Estimate | Seed-cluster 95% CI |
|---|---:|---:|
| Primary action + context AUC | 0.829 | [0.818, 0.840] |
| AUC gain over action identity | +0.0480 | [+0.0409, +0.0554] |

The context-support gain was positive in every cluster-bootstrap replicate.

## Seed heterogeneity

The primary model's individual-seed AUC ranged from 0.774 to 0.887 across all
40 seeds. No seed fell to chance or below. This rules out the explanation that
the pooled result is driven by a small subset of favorable seeds.

## Calibration

| Model | Brier score | Log loss | 10-bin ECE |
|---|---:|---:|---:|
| Action + context support | 0.161 | 0.496 | 0.184 |
| Action identity only | 0.201 | 0.593 | 0.270 |

The primary model improves all calibration scores relative to action identity,
but remains substantially overconfident. For example, its highest predicted-risk
decile averaged probability 0.740 while the observed unsafe fraction was 0.457.

## Conclusion

Prospective ranking robustness survives seed-cluster inference and every
individual seed. Absolute probabilities do not transfer cleanly. Current
evidence supports a ranking model, not a calibrated risk estimator or deployment
threshold.

Experiment 129 evaluates source-only calibration specifications without fitting
to fourth-population labels. Because model choice will be informed by exposed
fourth-population results, any selected calibration must be confirmed on a new
fifth population.

## Artifacts

- `results/fourth_population_seed_cluster_robustness.csv`
- `results/fourth_population_seed_level_performance.csv`
- `results/fourth_population_calibration.csv`
- `results/fourth_population_seed_cluster_bootstrap_summary.csv`
