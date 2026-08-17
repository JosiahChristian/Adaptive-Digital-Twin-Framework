# Experiment 144 — preregistered tenth-population conditional-context permutation control

## Question

Does the *correct row-level pairing* of `context_support_distance` with an action-context row provide prospective decision value, beyond action identity, seed-level environment, and the marginal distribution of context values?

## Frozen design

This protocol and its analysis code were committed before tenth-population seeds 44391–44430 were generated.

The source-trained action-plus-context model remained frozen to the same source population used in Experiments 140 and 142:

`results/action_conditioned_support_representation_analysis_actions_071_110.csv`

Features remained `action_2`, `action_3`, and `context_support_distance`. The alert budget remained the unlabeled fixed-coverage budget implied by the established 0.80 source unsafe-recall target.

On the untouched tenth population, the primary rule ranked rows with their correctly paired context values. The negative control performed 5,000 conditional permutations. Within every `generation_seed × action` stratum, `context_support_distance` values were randomly reassigned among rows while action identity, seed membership, unsafe labels, the stratum-level context distribution, and the total alert count remained fixed. Unsafe labels were never used to construct rankings.

## Primary criterion

The row-pairing claim passed only if the correctly paired context rule captured more unsafe actions than the 99th percentile of the 5,000 conditional-permutation controls.

## Results

The untouched tenth population contained 10,704 rows and 2,495 unsafe actions (23.309% prevalence). The frozen alert coverage was 39.018%, corresponding to 4,176 alerts.

| Endpoint | Correct context pairing | Conditional permutations |
|---|---:|---:|
| Unsafe actions captured | **2,004** | mean 1,880.34 |
| Unsafe recall | **0.8032** | — |
| Unsafe precision | **0.4799** | — |
| Balanced accuracy | **0.7693** | — |
| Permutation 95% TP interval | — | [1,866, 1,895] |
| Permutation 99th percentile TP | — | 1,898 |

The correctly paired rule captured approximately **123.66 more unsafe actions** than the conditional-permutation mean. None of 5,000 permutations equaled or exceeded the primary result (`P_perm >= primary = 0.0`). The preregistered criterion passed.

## Conclusion

This result prospectively supports a simulation-specific row-correspondence claim: the performance gain is not explained merely by action identity, seed-level environment, alert budget, or the marginal distribution of context-support distances. Correct row-level pairing of context support with the candidate action carries decision-relevant ranking information.

The result does not establish causal intervention benefit, deployment safety, clinical applicability, or universal cross-domain transfer. Those remain separate questions.

## Artifacts

- `results/preregistered_tenth_population_conditional_context_permutation.csv`
- `results/preregistered_tenth_population_conditional_context_permutation_trials.csv`
- `results/experiment_144_console_output.txt`
