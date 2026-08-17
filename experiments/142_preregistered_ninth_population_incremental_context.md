# Experiment 142 — preregistered ninth-population incremental-context ablation

## Question

Does context support add decision-relevant information beyond learned action identity alone?

Experiment 140 prospectively showed that the frozen action-plus-context ranking outperformed an action-identity-matched random allocation at identical alert coverage. Experiment 142 raises the control: the comparator is now a learned source-trained action-only logistic model rather than random allocation.

## Frozen design

This protocol and its analysis code were committed before ninth-population seeds 44351–44390 were generated.

Training data remained frozen at `results/action_conditioned_support_representation_analysis_actions_071_110.csv`.

Two logistic models were fit only on the frozen source population:

- action-only: `action_2`, `action_3`
- action+context: `action_2`, `action_3`, `context_support_distance`

The source action+context model defined the alert budget using the already established 0.80 source unsafe-recall target. On the ninth population, both models received the identical alert count using only each model's unlabeled target score distribution. Ninth-population unsafe labels were used only after alerts were fixed for evaluation.

## Primary criteria

The incremental-context claim passed only if all three conditions held on the untouched ninth population:

1. action+context captured more unsafe actions than action-only at identical alert coverage;
2. action+context had higher ROC AUC than action-only;
3. a 10,000-resample seed-level bootstrap of the mean difference in unsafe actions captured had a 95% interval whose lower bound was greater than zero.

These criteria were frozen before target outcomes existed.

## Schema-only repair

The first execution attempt failed before producing Experiment 142 results because the analysis referenced a non-existent `seed` column while the frozen action tables use `generation_seed`. The repair changed only this identifier reference. Features, models, thresholds, source coverage, bootstrap count, RNG seed, endpoints, and success criteria remained unchanged. The workflow was also hardened with `set -o pipefail` so a Python failure cannot be masked by `tee`.

## Results

| Endpoint | Action only | Action + context | Difference |
|---|---:|---:|---:|
| Unsafe recall | 0.6013 | **0.7058** | **+0.1045** |
| Unsafe precision | 0.4041 | **0.4744** | +0.0702 |
| Balanced accuracy | 0.6431 | **0.7139** | **+0.0708** |
| ROC AUC | 0.6944 | **0.7565** | **+0.0621** |
| Unsafe actions captured | 1,617 | **1,898** | **+281** |
| Alert coverage | 0.3902 | 0.3902 | matched |

The seed-level bootstrap mean additional unsafe actions captured was approximately 7.027 per seed, with a 95% interval of **[5.025, 9.175]**. All three preregistered primary criteria passed.

## Conclusion

On an untouched ninth population with materially higher unsafe-outcome prevalence than the preceding population, context information provided prospective incremental value beyond a learned action-only model at identical alert coverage.

The validated claim remains simulation-specific. This result establishes incremental predictive/triage value of the context-support variable in this framework; it does not establish causal intervention benefit, deployment safety, clinical applicability, or universal cross-domain transfer.

## Artifacts

- `results/preregistered_ninth_population_incremental_context.csv`
- `results/preregistered_ninth_population_incremental_context_by_seed.csv`
- `results/preregistered_ninth_population_incremental_context_bootstrap.csv`
- `results/experiment_142_console_output.txt`
