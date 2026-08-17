# Experiment 134 — preregistered sixth-population unlabeled-EM confirmation

## Protocol

The action-plus-context model was trained only on population 071–110. Fixed
source-prior correction and the unlabeled EM update were frozen before seeds
44231–44270 existed. EM observed target feature scores but not target unsafe
labels.

## Results

| Metric | Unlabeled EM | Fixed source prior |
|---|---:|---:|
| Estimated/assumed prior | 0.094 | 0.208 |
| Observed prevalence | 0.215 | 0.215 |
| Mean-risk error | 0.121 | **0.035** |
| ROC AUC | 0.813 | 0.813 |
| Brier score | 0.176 | **0.150** |
| Log loss | 0.548 | **0.473** |
| ECE | 0.149 | **0.071** |

## Conclusion

The prospective test falsifies portable unlabeled EM prior adaptation. The
method substantially underestimated prevalence and worsened every calibration
metric while leaving ranking unchanged. The modest fifth-population diagnostic
gain did not generalize.

This indicates that simple label shift is violated: changes in the score
distribution cannot be interpreted reliably as changes in class prior while
holding class-conditional score distributions fixed.

The accepted evidence boundary is now:

- action identity plus context support has prospectively robust ranking across
  the fourth and sixth populations (AUC 0.829 and 0.813);
- fixed source-prior correction is markedly safer than balanced raw
  probabilities but remains imperfect under population drift;
- unlabeled EM adaptation is rejected;
- calibrated intervention thresholds still require either labeled online
  calibration, invariant conditional modeling, or a formally conservative
  decision rule.

## Artifact

- `results/preregistered_sixth_population_unlabeled_em.csv`
