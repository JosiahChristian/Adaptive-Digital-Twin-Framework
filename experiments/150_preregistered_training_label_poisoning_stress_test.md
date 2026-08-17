# Experiment 150 — preregistered training-label poisoning stress test

## Question

Is the prospectively replicated hazard-filter intervention vulnerable to **targeted source-training label concealment**, and is any degradation greater than that caused by the same amount of random label contamination?

This is a defensive robustness experiment. The attack is confined to the repository's simulated source-training table and is not a claim about real-world systems.

## Frozen design

This protocol and analysis code are committed before thirteenth-population seeds 44511–44550 are generated.

The clean source training data remain:

`results/action_conditioned_support_representation_analysis_actions_071_110.csv`

The intervention policy remains the Experiment 146/148 policy: source-trained action-plus-context hazard model, fixed candidate-exclusion coverage, then minimum-predicted-loss selection among unexcluded candidates with baseline fallback if all are excluded.

To isolate model corruption from budget changes, the candidate-exclusion coverage is frozen from the **clean** source model and held identical for clean, targeted-poisoned, and random-poisoned models.

## Targeted concealment attack

Among source rows truly labeled unsafe, the attacker selects those with the largest `context_support_distance` and flips their training label from unsafe (1) to safe (0). The feature values themselves are not changed.

Three contamination doses are frozen as fractions of source unsafe rows:

- 5%
- 10%
- 20%

The target population's true labels are never used to construct the poisoning attack or fit the poisoned models.

## Matched random-poison controls

At each dose, 200 control trials flip the same number of source unsafe labels to safe, but choose the flipped unsafe rows uniformly at random. Every control model receives the same clean frozen target exclusion budget.

## Primary vulnerability test

The 20% dose is the preregistered primary attack dose. A **specific targeted-poisoning vulnerability** is supported only if all of the following occur on the untouched thirteenth population:

1. targeted poisoning produces more unsafe selected actions than the clean hazard-filter policy;
2. targeted poisoning produces greater total realized regret than the clean hazard-filter policy;
3. targeted poisoning's unsafe selected-action count is worse than the 95th percentile of 200 matched random-poison controls; and
4. targeted poisoning's total realized regret is worse than the 95th percentile of matched random-poison controls.

The 5% and 10% doses are prespecified dose-response measurements, not independent primary hypotheses.

## Interpretation

A pass would identify a simulation-specific training-data integrity vulnerability in the otherwise replicated intervention. A failure would be evidence that this particular concealment strategy, at doses through 20%, does not cause degradation exceeding matched random contamination under the frozen intervention budget.

Neither outcome establishes security or insecurity of real deployed systems. No biomedical, clinical, or real-world safety claim is implied.
