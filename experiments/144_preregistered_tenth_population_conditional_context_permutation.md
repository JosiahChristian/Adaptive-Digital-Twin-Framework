# Experiment 144 — preregistered tenth-population conditional-context permutation control

## Question

Does the *correct row-level pairing* of `context_support_distance` with an action-context row provide prospective decision value, beyond action identity, seed-level environment, and the marginal distribution of context values?

## Frozen design

This protocol and its analysis code are committed before tenth-population seeds 44391–44430 are generated.

The source-trained action-plus-context model remains frozen to the same source population used in Experiments 140 and 142:

`results/action_conditioned_support_representation_analysis_actions_071_110.csv`

Features remain:

- `action_2`
- `action_3`
- `context_support_distance`

The alert budget remains the unlabeled fixed-coverage budget implied by the established 0.80 source unsafe-recall target.

On the untouched tenth population, the primary rule ranks rows with their correctly paired context values. The negative control performs 5,000 conditional permutations. Within every `generation_seed × action` stratum, `context_support_distance` values are randomly reassigned among rows while action identity, seed membership, unsafe labels, the stratum-level context distribution, and the total alert count remain fixed. Unsafe labels are never used to construct rankings.

## Primary endpoint and criterion

Primary endpoint: number of unsafe actions captured at the frozen alert budget.

The row-pairing claim passes only if the correctly paired context rule captures more unsafe actions than the 99th percentile of the 5,000 conditional-permutation controls. The empirical fraction of permutations equaling or exceeding the primary result is also reported.

Because alert count and class totals are fixed, recall, precision, specificity, and balanced accuracy are monotonic functions of the same true-positive count; they are reported descriptively rather than treated as independent primary criteria.

## Interpretation boundaries

A pass would support a simulation-specific claim that row-level context correspondence carries prospective ranking information beyond action identity, seed-level environment, and marginal context distributions.

A failure will be retained and will narrow the claim. No tuning on the tenth-population outcomes will be used to rescue the preregistered test.

This experiment does not establish causal intervention benefit, deployment safety, clinical applicability, or cross-domain transfer.
