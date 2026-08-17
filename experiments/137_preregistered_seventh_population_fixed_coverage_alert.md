# Experiment 137 — preregistered seventh-population fixed-coverage alert

## Protocol

The source model and 80%-recall threshold were fitted only on population
071–110. Its resulting 39.02% alert coverage was frozen. On the unlabeled
seventh population, the score threshold was set only by the corresponding target
quantile. Target unsafe labels were not used to choose alerts.

Preregistered success required recall >= 0.75, NPV >= 0.90, and alert coverage
within 0.01 of the frozen budget.

## Results

| Endpoint | Result | Seed-cluster 95% CI |
|---|---:|---:|
| Unsafe recall | **0.815** | [0.791, 0.840] |
| Negative predictive value | **0.954** | [0.945, 0.963] |
| Alert coverage | **0.3902** | — |
| Balanced accuracy | 0.750 | [0.740, 0.762] |
| ROC AUC | 0.808 | — |
| Unsafe precision | 0.316 | — |

All three primary criteria passed.

## Action decomposition

- Action 1: all rows alerted; 100% unsafe recall.
- Action 2: 15.2% alerted; 17.3% unsafe recall.
- Action 3: 1.85% alerted; 45.8% unsafe recall.

## Conclusion

The prospective result confirms that unlabeled fixed coverage stabilizes safety
recall under score drift better than a fixed numeric threshold. This is an
alert/defer rule, not proof of calibrated risk or autonomous intervention
safety.

Because all action-1 rows are alerted and action 1 contains most unsafe outcomes,
Experiment 138 compares the rule against action-1-only and matched-coverage
random negative controls. That analysis determines whether context ranking adds
value beyond action identity.
