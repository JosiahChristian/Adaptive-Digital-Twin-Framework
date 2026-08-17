# Research Claim Ledger

This ledger separates what the current ADT evidence supports from what remains provisional or unsupported. It is intentionally conservative and should be revised whenever new experiments weaken, narrow, or overturn an entry.

## Evidence-supported observations

### C1 — Compact pre-decision loss-surface features contain predictive signal in the documented event population

**Status:** supported within the current generated population and evaluation procedure.

The tracked absolute-loss-floor harmful-expansion analysis evaluates 65 events (15 harmful, 50 beneficial). Its compact calibration model reports 0.950 balanced accuracy, 1.000 harmful-event recall, 0.750 harmful-event precision, and 0.979 ROC AUC, with mean fold balanced accuracy 0.939 and mean fold ROC AUC 0.913.

**Permitted wording:** pre-decision loss-surface information contains substantial predictive signal for harmful expansion events in the documented generated population.

**Do not claim:** causal identification, deployment robustness, universal harmful-adaptation prediction, or generalization to arbitrary dynamical systems.

Primary artifact: [`results/absolute_loss_floor_harmful_expansion_analysis.csv`](../results/absolute_loss_floor_harmful_expansion_analysis.csv)

### C2 — Simple support-distance representations are insufficient as a standalone unsafe-behavior detector

**Status:** supported negative result in the documented action-conditioned analysis.

The strongest listed support-distance model reaches only 0.593 balanced accuracy and 0.619 ROC AUC; the action-support-only representation is weaker.

**Permitted wording:** simple geometric distance from observed support does not adequately explain or detect unsafe action-level behavior in the evaluated population.

Primary artifact: [`results/action_conditioned_support_representation_analysis.csv`](../results/action_conditioned_support_representation_analysis.csv)

### C3 — Strong pooled discrimination can fail under conditioned transfer

**Status:** supported falsification result.

The severe-proxy/action analysis contains pooled models with AUC above 0.92, but within-action cross-block transfer for action 1 falls to ROC AUC 0.159 and 0.444. This prevents treating the pooled score as robust transferable harm prediction.

**Permitted wording:** pooled discrimination can be substantially confounded by action/block structure and must survive conditioned transfer before being promoted as a general predictor.

Primary artifact: [`results/action_conditioned_severe_proxy_harm_analysis.csv`](../results/action_conditioned_severe_proxy_harm_analysis.csv)

### C4 — The Experiment 153 apparent poisoning benefit is not evidence that poisoning globally improves the hazard model

**Status:** mechanism diagnosis supported; prospective replication is still active.

Experiment 154 found nearly unchanged global ranking performance between clean and poisoned models (ROC AUC 0.833773 versus 0.831417) and high overlap between exclusion sets (Jaccard 0.924229). The observed intervention difference was concentrated near a fixed top-N decision boundary. At the context level, 220 of 2,799 selected actions changed, including 41 unsafe-to-safe and 22 safe-to-unsafe transitions.

**Permitted wording:** the observed reversal is consistent with a local intervention-boundary reordering rather than a global improvement in hazard ranking.

**Do not claim yet:** that the effect is definitively population-specific or that its sign will fail to replicate. Experiment 156 is explicitly testing that prospective question.

Primary result note: [`research/experiment_154_result.md`](experiment_154_result.md)

## Active claims under prospective test

### P1 — The Experiment 153 intervention reversal is a target-population-specific boundary effect

**Status:** unresolved / prospectively testing.

Experiment 156 freezes the clean model, targeted attack, intervention budget, and diagnostic endpoints on a fresh reconstructed target population. No synthesis document should promote P1 to a supported claim until that prospective result is committed and interpreted.

## Claims currently prohibited by the evidence

- The adaptive-digital-twin problem has been solved.
- The framework has demonstrated deployment-ready safety or control performance.
- The current predictors generalize to real-world cyber-physical or biomedical systems.
- Poisoning is beneficial or acts as reliable regularization.
- High pooled discrimination alone establishes transferable hazard prediction.
- Support distance alone provides a reliable unsafe-action detector.
- Any biomedical interpretation constitutes clinical validation.

## Promotion rule

A provisional claim should move into the evidence-supported section only after the relevant preregistered or prospectively frozen evaluation has completed and its result survives checks for leakage, population dependence, conditioning effects, threshold sensitivity, and plausible competing explanations. Negative or null results remain part of the ledger rather than being removed when a later favorable result appears.
