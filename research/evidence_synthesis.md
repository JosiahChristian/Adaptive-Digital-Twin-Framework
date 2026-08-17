# Current Evidence Synthesis

This document separates the strongest current findings from negative results, transfer failures, and unresolved questions. It is intentionally narrower than the full experiment history.

## 1. Strongest current signal: compact pre-decision loss-surface features

The tracked `absolute_loss_floor_harmful_expansion_analysis.csv` evaluates 65 action-space expansion events: 15 harmful and 50 beneficial. A three-feature calibration model using `predicted_loss_floor`, `loss_floor_error`, and `expanded_action_loss_error` reports:

- balanced accuracy: **0.950**
- harmful-event recall: **1.000**
- harmful-event precision: **0.750**
- ROC AUC: **0.979**
- mean fold balanced accuracy: **0.939**
- mean fold ROC AUC: **0.913**

This is the strongest compact predictive result currently surfaced by the repository. It supports a narrow claim: within the documented generated population and evaluation procedure, pre-decision loss-surface information contains substantial signal about whether an expansion event will later be harmful.

It does **not** establish causal identification, deployment robustness, or generalization outside the generated populations already tested.

Primary artifact: [`results/absolute_loss_floor_harmful_expansion_analysis.csv`](../results/absolute_loss_floor_harmful_expansion_analysis.csv)

## 2. Negative/weak result: support-distance representation alone is insufficient

The action-conditioned support-representation analysis contains 2,316 rows, including 628 unsafe and 1,688 safe rows. Its strongest listed support-distance model (`context_support_distance|action_support_distance`) reaches only:

- balanced accuracy: **0.593**
- unsafe recall: **0.514**
- ROC AUC: **0.619**
- mean fold ROC AUC: **0.623**

The action-support-only model is weaker still (balanced accuracy **0.534**, ROC AUC **0.554**).

This result is important because it constrains the story: simple geometric distance from observed support should not currently be treated as a sufficient explanation or detector for unsafe action-level behavior.

Primary artifact: [`results/action_conditioned_support_representation_analysis.csv`](../results/action_conditioned_support_representation_analysis.csv)

## 3. Apparent pooled signal that fails transfer: severe-proxy/action models

The severe-proxy harm analysis shows strong pooled discrimination for models that include action identity. For example, the pooled `proxy_action_interaction` model reports mean AUC **0.933**, while `proxy_plus_action` reports mean AUC **0.926**.

However, the within-action transfer results are poor: for action 1, cross-block ROC AUC values are **0.159** and **0.444**. Action 2 has no harmful examples in the evaluated blocks and is therefore uninformative for transfer.

This is a useful falsification result. High pooled discrimination is not enough: the signal appears entangled with action/block structure and does not currently support a robust transferable harm-prediction claim.

Primary artifact: [`results/action_conditioned_severe_proxy_harm_analysis.csv`](../results/action_conditioned_severe_proxy_harm_analysis.csv)

## Current defensible synthesis

Taken together, the current evidence favors a narrower interpretation than a generic claim that "the twin can predict harmful adaptation":

1. **Some compact pre-decision loss-surface features show strong predictive signal in the current generated event population.**
2. **Simple support-distance features are weak and should not be promoted as a sufficient mechanism.**
3. **Some high pooled action/proxy scores collapse under cross-block transfer, demonstrating confounding/structure sensitivity that must remain visible.**

The research priority is therefore not to maximize the number of favorable models. It is to determine whether the compact loss-surface signal survives stronger population shifts, alternative event definitions, calibration choices, and competing explanations while preserving the negative transfer results as constraints on any eventual claim.

## Next falsification gates

Before elevating the compact loss-surface result toward a publication-level claim, the program should require evidence on:

- genuinely held-out generated populations rather than only within-population folds
- sensitivity to event-label and harm-threshold definitions
- calibration stability and threshold sensitivity
- alternative feature sets and simpler baselines
- action-conditioned and block-conditioned generalization
- leakage checks around feature construction and event timing
- persistence of predictive usefulness under distribution shift
- explicit failure cases and regions where the signal disappears

A favorable result at one gate should not erase failures at another. The synthesis should be revised whenever new experiments weaken, narrow, or overturn these conclusions.
