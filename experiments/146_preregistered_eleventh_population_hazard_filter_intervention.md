# Experiment 146 — preregistered eleventh-population hazard-filter intervention

## Question

Can the already validated source-trained action-plus-context hazard signal improve a simulated action-selection decision, rather than merely rank unsafe candidate actions?

## Frozen design

This protocol and analysis code are committed before eleventh-population seeds 44431–44470 are generated.

The source hazard model is unchanged from Experiments 140, 142, and 144 and is trained only on:

`results/action_conditioned_support_representation_analysis_actions_071_110.csv`

Hazard features remain `action_2`, `action_3`, and `context_support_distance`. The alert/exclusion budget remains the unlabeled fixed-coverage budget implied by the established 0.80 source unsafe-recall target.

For each target context (`generation_seed × test_index`), three candidate actions are available with predicted action losses generated independently of target unsafe labels.

### Baseline policy

Choose the candidate with minimum `predicted_action_loss` (stable action-order tie breaking).

### Hazard-filter policy

1. Rank all target candidate actions with the frozen source hazard model.
2. Mark the globally highest-risk candidates using the frozen source coverage and the unlabeled target score distribution.
3. Within each context, choose the minimum-predicted-loss candidate among unmarked actions.
4. If all three candidates are marked, fall back to the baseline action.

Target unsafe labels and realized regret are used only after selections are fixed for evaluation.

## Matched conditional-random control

The negative control preserves, separately for every context, the exact number of candidate actions excluded by the primary hazard filter. In each of 5,000 trials, that many excluded positions are randomly reassigned among the three candidate actions, after which the identical minimum-predicted-loss selection rule is applied.

This preserves the intervention/exclusion budget per context while destroying the correspondence between the learned hazard ranking and the action excluded.

## Primary endpoints and criteria

Two co-primary endpoints are frozen:

1. number of selected actions whose realized regret exceeds 0.005 (`unsafe selected actions`);
2. total realized regret of selected actions.

The intervention claim passes only if the hazard-filter policy is better than the **1st percentile** of the 5,000 matched random-control trials on both endpoints (fewer unsafe selected actions and lower total realized regret).

Secondary descriptive endpoints include baseline versus hazard-filter unsafe rate, mean regret, number of contexts whose selected action changes, and empirical probabilities that a random-control trial is as good as or better than the hazard-filter policy.

## Interpretation boundaries

A pass would establish only a **simulator-internal counterfactual intervention result**: under this candidate-action model and frozen source-trained hazard rule, hazard-aware filtering improves the selected simulated action relative to the specified baseline and matched random exclusions.

It would not establish real-world causal efficacy, autonomous deployment safety, biomedical/clinical applicability, or universal transfer to other dynamical systems. Those remain untested.
