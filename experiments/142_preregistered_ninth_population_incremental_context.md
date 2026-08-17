# Experiment 142 — preregistered ninth-population incremental-context ablation

## Question

Does context support add decision-relevant information beyond learned action identity alone?

Experiment 140 prospectively showed that the frozen action-plus-context ranking outperformed an action-identity-matched random allocation at identical alert coverage. Experiment 142 raises the control: the comparator is now a learned source-trained action-only logistic model rather than random allocation.

## Frozen design

This protocol and its analysis code are committed before ninth-population seeds 44351–44390 are generated.

Training data remain frozen at `results/action_conditioned_support_representation_analysis_actions_071_110.csv`.

Two logistic models are fit only on the frozen source population:

- action-only: `action_2`, `action_3`
- action+context: `action_2`, `action_3`, `context_support_distance`

The source action+context model defines the alert budget using the already established 0.80 source unsafe-recall target. On the ninth population, both models receive the identical alert count using only each model's unlabeled target score distribution. Ninth-population unsafe labels are used only after alerts are fixed for evaluation.

## Primary criteria

The incremental-context claim passes only if all three conditions hold on the untouched ninth population:

1. action+context captures more unsafe actions than action-only at identical alert coverage;
2. action+context has higher ROC AUC than action-only;
3. a 10,000-resample seed-level bootstrap of the mean difference in unsafe actions captured has a 95% interval whose lower bound is greater than zero.

These criteria are intentionally stricter than the Experiment 140 matched-random control and are frozen before target outcomes exist.

## Interpretation boundaries

A pass would support a simulation-specific incremental-information claim: context support contains prospectively useful information beyond action identity under the current source-trained representation and fixed-coverage alert/defer setting.

A pass would not establish causal intervention benefit, clinical applicability, deployment safety, or universal transfer across dynamical systems. A failure will be retained as evidence against the stronger incremental-context claim and will not be tuned away on this population.
