# Experiment 146 — preregistered eleventh-population hazard-filter intervention

## Question

Can the already validated source-trained action-plus-context hazard signal improve a simulated action-selection decision, rather than merely rank unsafe candidate actions?

## Frozen design

This protocol and analysis code were committed before eleventh-population seeds 44431–44470 were generated.

The source hazard model was unchanged from Experiments 140, 142, and 144 and was trained only on `results/action_conditioned_support_representation_analysis_actions_071_110.csv`. Hazard features remained `action_2`, `action_3`, and `context_support_distance`. The exclusion budget remained the unlabeled fixed-coverage budget implied by the established 0.80 source unsafe-recall target.

For each target context (`generation_seed × test_index`), the baseline selected the candidate with minimum `predicted_action_loss`. The hazard-filter policy excluded globally high-risk candidates at the frozen coverage, then selected the minimum-predicted-loss candidate among those remaining; if all candidates were excluded, it fell back to baseline.

Target unsafe labels and realized regret were used only after selections were fixed for evaluation.

## Matched conditional-random control

For each context, 5,000 random-control trials preserved the exact number of candidate actions excluded by the primary hazard filter while randomly reassigning which candidate positions were excluded. The identical minimum-predicted-loss selector was then applied. This preserved the intervention budget per context while destroying targeted exclusion.

## Frozen primary criteria

The hazard-filter intervention passed only if it produced both:

1. fewer unsafe selected actions than the 1st percentile of matched random controls; and
2. lower total realized regret than the 1st percentile of matched random controls.

## Results

The untouched eleventh population contained 3,182 decision contexts and 9,546 candidate-action rows. At the frozen 39.018% candidate exclusion coverage, 3,725 candidate actions were excluded.

| Endpoint | Predicted-loss baseline | Hazard-filter policy | Matched random exclusions |
|---|---:|---:|---:|
| Unsafe selected actions | 811 | **454** | mean 742.91; 1st pct 712 |
| Unsafe selected-action rate | 25.49% | **14.27%** | — |
| Total realized regret | 48.8763 | **18.2045** | mean 41.5078; 1st pct 39.4960 |
| Mean realized regret/context | 0.01536 | **0.00572** | — |
| Selected actions changed vs baseline | — | 1,784 / 3,182 (56.07%) | — |

The hazard filter reduced unsafe selections by **357** relative to baseline and total realized regret by **30.6718**. None of 5,000 matched random-control trials achieved an unsafe-selection count or total regret as low as the hazard-filter policy. Both preregistered co-primary criteria passed.

## Conclusion

Experiment 146 provides prospective **simulator-internal counterfactual intervention evidence**: the previously validated source-trained hazard signal was useful not only for ranking unsafe candidate actions but also for improving a frozen simulated action-selection procedure on an untouched population. The advantage greatly exceeded matched random exclusions at the same per-context intervention budget.

This remains a simulator-specific result. It does not establish real-world causal efficacy, autonomous deployment safety, biomedical/clinical applicability, or universal cross-domain transfer. Independent prospective replication is required before treating the intervention effect as stable.

## Artifacts

- `results/preregistered_eleventh_population_hazard_filter_intervention.csv`
- `results/preregistered_eleventh_population_hazard_filter_random_trials.csv`
- `results/preregistered_eleventh_population_hazard_filter_by_seed.csv`
- `results/experiment_146_console_output.txt`
