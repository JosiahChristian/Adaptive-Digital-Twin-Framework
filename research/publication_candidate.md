# Publication-Oriented Candidate Synthesis

This document identifies the narrowest current ADT result that may be worth developing toward faculty-supervised publication. It is not a manuscript and does not declare the result publishable yet.

## Candidate contribution

A defensible candidate contribution is narrower than "adaptive digital twins can predict harmful adaptation." The current evidence instead supports investigating the following proposition:

> **Compact pre-decision loss-surface features may identify harmful action-space expansion events before the downstream harm is observed, while several seemingly plausible alternative representations fail under stronger conditioning or transfer.**

The value of this candidate is not only the strongest positive metric. The research program already contains negative evidence that constrains the mechanism and helps distinguish the signal from simpler explanations.

## Evidence currently in favor

The compact three-feature loss-surface model in `absolute_loss_floor_harmful_expansion_analysis.csv` was evaluated on 65 events (15 harmful, 50 beneficial) and reports:

- balanced accuracy: **0.950**
- harmful-event recall: **1.000**
- harmful-event precision: **0.750**
- ROC AUC: **0.979**
- mean fold balanced accuracy: **0.939**
- mean fold ROC AUC: **0.913**

These numbers are strong enough to justify further falsification, not strong enough by themselves to justify a general claim.

## Evidence that narrows the mechanism

### Support-distance alternatives are weak

The strongest listed support-distance model in the action-conditioned support analysis reaches only about **0.593 balanced accuracy** and **0.619 ROC AUC**. This argues against a simple story in which distance from observed support is sufficient to explain unsafe behavior.

### Pooled action/proxy models can be misleading

Some pooled action/proxy models exceed **0.92 AUC**, but within-action cross-block transfer falls sharply. This is evidence that high pooled discrimination can be driven by structural confounding and should not be accepted without conditioned transfer.

### Intervention outcomes can diverge from global ranking metrics

Experiments 153-156 show that small score-order changes around a fixed intervention boundary can alter selected actions and downstream regret without materially improving global ranking metrics. This is a separate phenomenon from the compact loss-surface event predictor, but it is methodologically important: evaluation of an adaptive system should distinguish prediction quality from decision consequences.

## Candidate paper framing

A faculty-supervised paper could eventually be framed around **pre-decision risk prediction for adaptive action-space expansion under nonstationarity**, with the digital-twin framework serving as the experimental infrastructure rather than as the claim itself.

The paper should emphasize:

1. a narrowly defined harmful-expansion event;
2. pre-decision feature construction that cannot use downstream information;
3. calibration/held-out separation;
4. comparison with simple and plausible alternative feature families;
5. conditioned transfer and population-shift tests;
6. explicit negative results and failure cases;
7. decision-level consequences evaluated separately from ranking metrics.

## Publication gates still required

Before this becomes a serious submission candidate, the following gates should be satisfied or explicitly reported as failures:

- **true held-out population replication** of the compact predictor, not merely within-population cross-validation;
- **label-definition sensitivity** to show the result is not an artifact of one harm threshold;
- **timing/leakage audit** proving every predictive feature is available before the expansion decision;
- **simpler baseline comparison**, including one-feature and low-capacity alternatives;
- **calibration stability** across populations and thresholds;
- **action- and block-conditioned generalization**;
- **distribution-shift stress tests** that can make the predictor fail;
- **confidence intervals or resampling uncertainty** appropriate to the event count;
- **failure-case taxonomy** describing where the predictor is wrong and why;
- **independent faculty review of the experimental design and statistical claims** before manuscript-level language is adopted.

## What should not be the paper claim

The current evidence does not justify claiming that:

- a general adaptive-digital-twin problem has been solved;
- the method is deployment-ready;
- the predictor transfers to arbitrary cyber-physical systems;
- the result is causal;
- biomedical or aerospace applicability has been established;
- poisoning-related boundary effects are beneficial.

## Stopping rule

The candidate should be abandoned or substantially narrowed if stronger held-out evaluation shows that the compact loss-surface signal is population-specific, label-definition-specific, leakage-sensitive, or no better than simpler baselines. A negative outcome would still be scientifically useful because the repository already preserves the failed alternatives and transfer limitations needed to explain why the original apparent signal did not generalize.
