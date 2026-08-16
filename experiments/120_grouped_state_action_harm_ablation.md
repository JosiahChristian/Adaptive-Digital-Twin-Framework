# Experiment 120 — Grouped Controller-State/Action Harm Ablation

## Objective

Determine whether the performance lost under strict individual-feature reduction in Experiment 119 reflects distributed information across mechanistic feature groups.

The eleven pre-action state variables were frozen into four groups before evaluation:

1. controller probabilities;
2. temporal/support context;
3. estimated plant state;
4. predicted risk and regret.

Each group was tested alone, with action identity, and by removing the complete group from the full state-plus-action model. Evaluation remained reciprocal and population-held-out.

## Principal Results

| Model | Mean AUC | Minimum AUC |
|---|---:|---:|
| Full state + action | **0.845** | **0.789** |
| Predicted risk/regret + action | 0.813 | 0.691 |
| Leave controller probabilities out | 0.807 | 0.752 |
| Leave temporal/support context out | 0.812 | 0.713 |
| Leave estimated plant state out | 0.830 | 0.783 |
| Leave predicted risk/regret out | 0.786 | 0.768 |
| Controller probabilities + action | 0.781 | 0.681 |
| Estimated plant state + action | 0.769 | 0.747 |
| Action only | 0.729 | 0.613 |

Action-2 coefficient sign stability was 100% in every action-containing model.

## Group-Ablation Outcome

Removing the predicted-risk/regret group caused the largest mean-AUC loss:

**−0.059**

Removing temporal/support context caused the largest minimum-AUC loss:

**−0.076**

Removing estimated plant state caused little degradation:

- mean-AUC change: −0.015;
- minimum-AUC change: −0.007.

No single group matched the full joint representation in both transfer directions.

## Cross-Population Asymmetry

The predicted-risk/regret group alone transferred very differently by direction:

- held-out early population: AUC 0.603;
- held-out later population: AUC 0.902.

Adding action improved these to:

- held-out early population: AUC 0.691;
- held-out later population: AUC 0.936.

Temporal/support context showed the reverse type of instability, contributing more to the weaker early-population transfer boundary than its group-only average suggests.

## Falsification Outcome

Experiment 120 rejects a single-dominant-group explanation.

Predictive performance is distributed across groups, and different groups protect different population-transfer directions. The failure of Experiment 119 is therefore not explained solely by correlated substitution among a few interchangeable individual variables.

The evidence supports:

> Harmful support expansion is represented by distributed controller-state information whose useful composition shifts across populations, while action identity retains a stable directional association.

It does not support a compact universal veto representation or a causal action effect.

## Limitations

- Only 23 harmful events are available across 153 expansions.
- Reciprocal evaluation uses only two populations.
- Logical groups were prespecified but remain modeling abstractions.
- AUC uncertainty is not yet quantified by population-stratified resampling.
- Group interactions and nonlinearities remain untested.

## Conclusion

The full state-plus-action representation remains the strongest and most balanced transferred model:

- mean AUC: **0.845**;
- minimum AUC: **0.789**.

Predicted risk/regret provides the largest average contribution, while temporal/support context is most important to worst-direction robustness. Estimated plant state is comparatively dispensable within the current full model.

Before prospective intervention, the next experiment should quantify uncertainty around all model and ablation differences using population-stratified bootstrap confidence intervals and paired AUC-difference distributions. This will test whether the apparent group contributions exceed finite-sample variability.
