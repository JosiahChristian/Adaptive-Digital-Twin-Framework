# Experiment 140 — preregistered eighth-population context-value confirmation

## Protocol

The source model, 39.02% alert budget, unlabeled target-quantile rule, and 5,000
matched-random action-identity controls were frozen before seeds 44311–44350
existed. The negative control alerted every action-1 row and randomly allocated
the remaining budget among action-2/3 rows.

Primary success required the context-ranked rule to exceed the 97.5th percentile
of random controls for unsafe recall, balanced accuracy, and harmful rows
captured.

## Results

| Endpoint | Context-ranked rule | Matched-random mean | Random 95% interval |
|---|---:|---:|---:|
| Unsafe recall | **0.868** | 0.632 | [0.624, 0.641] |
| Unsafe precision | **0.330** | 0.240 | [0.237, 0.244] |
| Balanced accuracy | **0.781** | 0.642 | [0.637, 0.647] |
| Harmful rows captured | **1,186** | 863.7 | [852, 876] |

At the identical 39.02% alert coverage, context ranking captured 322.3 more
harmful actions than random allocation on average. None of 5,000 random trials
equaled or exceeded the primary rule on any reported comparison. All three
preregistered criteria passed.

## Conclusion

This prospectively confirms that context support contributes substantial
decision value beyond action identity under a constrained alert budget. The
effect is not a pooled artifact, a calibration claim, or a consequence of
allocating more alerts.

The validated claim remains simulation-specific: a source-trained
action-plus-context ranking, combined with an unlabeled fixed-coverage
alert/defer rule, generalizes across new seed populations and outperforms
action-identity-matched random allocation. It does not yet establish causal
intervention benefit or deployment safety.

## Artifacts

- `results/preregistered_eighth_population_context_negative_control.csv`
- `results/preregistered_eighth_population_matched_random_trials.csv`
