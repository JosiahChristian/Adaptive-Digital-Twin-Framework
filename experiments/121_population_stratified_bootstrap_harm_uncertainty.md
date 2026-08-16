# Experiment 121 — Population-Stratified Bootstrap Harm Uncertainty

## Objective

Quantify finite-sample uncertainty around the reciprocal population-held-out harm models and the group-ablation differences identified in Experiments 118–120.

The experiment uses 5,000 paired, outcome-stratified bootstrap resamples within each held-out population. Models and predictions are frozen before resampling. Paired AUC differences preserve the event-level dependence between competing models.

No intervention, threshold selection, or controller modification is introduced.

## Full Joint Model

The full state-plus-action model achieved:

- observed reciprocal mean AUC: **0.845**;
- bootstrap mean AUC: **0.845**;
- 95% bootstrap interval: **[0.768, 0.911]**.

By held-out population:

| Held-out population | AUC | 95% interval |
|---|---:|---:|
| early population | 0.789 | [0.667, 0.892] |
| later population | 0.900 | [0.806, 0.970] |

## Paired Reciprocal-Mean Comparisons

| Comparison | Observed ΔAUC | 95% paired interval | P(full better) |
|---|---:|---:|---:|
| Full vs state only | **+0.108** | **[+0.029, +0.191]** | 0.996 |
| Full vs action only | **+0.116** | **[+0.027, +0.198]** | 0.995 |
| Full vs no predicted-risk/regret group | +0.059 | [−0.016, +0.149] | 0.927 |
| Full vs no temporal/support group | +0.033 | [−0.002, +0.068] | 0.969 |

The full joint model's improvement over both state-only and action-only models remains positive across the 95% paired bootstrap intervals.

The individual group-ablation differences do not exclude zero at the reciprocal-mean level.

## Direction-Specific Findings

### Early population held out

Full versus state only:

- ΔAUC: +0.184;
- 95% interval: [+0.029, +0.345];
- probability full is better: 0.988.

Full versus action only:

- ΔAUC: +0.176;
- 95% interval: [+0.042, +0.309];
- probability full is better: 0.994.

Removing temporal/support context produced a reliable loss:

- ΔAUC: +0.076 in favor of the full model;
- 95% interval: [+0.024, +0.133];
- probability full is better: 0.996.

### Later population held out

Full versus state only:

- ΔAUC: +0.033;
- 95% interval: [+0.009, +0.067];
- probability full is better: 0.999.

The full-versus-action-only and group-ablation intervals include zero in this direction.

## Falsification Outcome

The hypothesis that Experiment 118's joint-model advantage is entirely attributable to finite-sample AUC fluctuation is not supported.

The full controller-state-plus-action model improves over:

- state alone, and
- action alone

with positive reciprocal-mean paired 95% intervals.

However, Experiment 121 does not support strong claims that either the predicted-risk/regret group or temporal/support group has a universally nonzero marginal contribution. Their reciprocal-mean ablation intervals include zero, and their importance varies by transfer direction.

## Interpretation

The robust finding is joint complementarity:

> Broader pre-action controller state and action identity contain complementary transferred information about harmful support expansion.

The less certain finding is the precise allocation of that information among state groups.

Temporal/support context materially protects the early-population transfer direction, while predicted risk/regret appears more important on average but remains uncertain under paired resampling.

## Limitations

- Bootstrap intervals quantify event-sampling uncertainty conditional on the two observed populations and fitted models.
- They do not quantify uncertainty from selecting populations, generating trajectories, or changing controller implementations.
- Only 23 harmful events are available.
- Two populations cannot establish population-invariant generalization.
- The analysis remains associational.

## Conclusion

Experiment 121 strengthens the joint controller-state/action result.

The full model's reciprocal mean AUC is **0.845** with a 95% interval of **[0.768, 0.911]**.

Its paired improvement is:

- **+0.108 [0.029, 0.191]** over state only;
- **+0.116 [0.027, 0.198]** over action only.

The next decisive falsification test is a frozen transfer to a third, non-overlapping population generated after model and feature specification. This prospective population should evaluate discrimination, calibration, action-coefficient direction, and group-ablation behavior without retuning.
