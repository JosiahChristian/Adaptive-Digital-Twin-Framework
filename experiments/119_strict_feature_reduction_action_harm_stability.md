# Experiment 119 — Strict Feature Reduction and Action-Harm Stability

## Objective

Test whether the joint controller-state/action signal from Experiment 118 survives strict, training-only feature reduction.

The experiment prevents held-out-population leakage by selecting state features independently inside each reciprocal population-transfer fold. Selection uses 250 stratified bootstraps across five L1-regularization values (1,250 fits per training population).

A feature qualifies only when:

- selection frequency is at least 60%, and
- coefficient-sign consistency is at least 80%.

Action identity is not used to choose state features. No intervention threshold or controller modification is introduced.

## Populations

The same non-overlapping populations used in Experiment 118 are retained:

- early population: 65 expansion events, 15 harmful;
- later population: 88 expansion events, 8 harmful;
- combined: 153 expansion events, 23 harmful.

Evaluation remains reciprocal and population-held-out.

## Selected Features

Training on the later population and holding out the early population selected:

- `context_benefit_probability`
- `context_current_parameter_estimate`
- `predicted_primary_regret`

Training on the early population and holding out the later population selected:

- `context_anchor_age`
- `context_current_mismatch_indicator`

The two reduced feature sets do not overlap. This is direct evidence that a compact state representation is not stable across the two populations under the prespecified selection criterion.

## Results

| Model | Mean AUC | Minimum AUC | Maximum AUC |
|---|---:|---:|---:|
| Full state + action | **0.845** | **0.789** | **0.900** |
| Full state only | 0.736 | 0.605 | 0.867 |
| Action only | 0.729 | 0.613 | 0.844 |
| Reduced state + action | 0.632 | 0.616 | 0.648 |
| Reduced state only | 0.539 | 0.500 | 0.577 |

The reduced state-plus-action model improves over reduced state alone by:

- mean AUC: **+0.093**
- minimum AUC: **+0.116**

However, it underperforms the full state-plus-action model by:

- mean AUC: **−0.213**

## Action-Coefficient Stability

The action-2 coefficient remains negative in both transfer directions.

| Held-out population | Reduced-model action-2 coefficient |
|---|---:|
| early population | −1.522 |
| later population | −0.168 |

Sign stability is therefore:

**100%**

The direction of the action association survives strict feature reduction, but its magnitude varies substantially across populations.

## Falsification Outcome

The strong claim tested was:

> A small, stable subset of pre-action state variables plus action identity preserves the transferred discrimination achieved by the full Experiment 118 representation.

That claim is falsified.

Strict training-only feature reduction produces different state subsets in the two populations and reduces mean AUC from 0.845 to 0.632.

A narrower claim survives:

> Action identity retains incremental harmful-expansion information after independently reduced state adjustment.

This is supported by the +0.093 mean-AUC and +0.116 minimum-AUC improvements over reduced state alone, together with 100% action-coefficient sign stability.

## Interpretation

The Experiment 118 result is not reducible to a small population-invariant state signature under the present sample size and stability threshold. Predictive information appears distributed across a broader controller-state representation, while the action association is directionally more stable than the selected state constituents.

This result argues against premature construction of a compact prospective veto. A controller intervention based on the unstable reduced state would risk population-specific behavior.

## Limitations

- Only 23 harmful events are available.
- The later population contains eight harmful events.
- Stability selection is sensitive to finite-sample perturbation.
- The two-population design cannot establish general population invariance.
- Action identity remains associational, not causal.
- The full model may retain redundant but collectively useful state information.

## Conclusion

Experiment 119 falsifies the hypothesis that strict feature reduction preserves the full joint signal.

The full state-plus-action model remains substantially stronger:

- mean AUC: **0.845**
- minimum AUC: **0.789**

The reduced model achieves:

- mean AUC: **0.632**
- minimum AUC: **0.616**

Action identity remains directionally stable and adds information beyond reduced state, but the state representation is not yet compact or population invariant.

The next experiment should distinguish whether the lost performance is caused by correlated-feature substitution, distributed multivariate information, or sample-size instability. Grouped/clustered feature reduction and leave-group-out ablation should be evaluated before any prospective controller modification.
