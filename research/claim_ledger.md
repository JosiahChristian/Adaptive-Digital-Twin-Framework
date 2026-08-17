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

**Status:** mechanism diagnosis supported and prospectively replicated as a fixed-budget intervention effect.

Experiment 154 found nearly unchanged global ranking performance between clean and poisoned models (ROC AUC 0.833773 versus 0.831417) and high overlap between exclusion sets (Jaccard 0.924229). The observed intervention difference was concentrated near a fixed top-N decision boundary. At the context level, 220 of 2,799 selected actions changed, including 41 unsafe-to-safe and 22 safe-to-unsafe transitions.

Experiment 156 then repeated the frozen clean model, targeted attack, intervention budget, and diagnostic endpoints on a fresh reconstructed target population. The same directional intervention effect replicated: poison-selected unsafe actions fell from 371 to 346, total regret fell from 16.160316 to 15.206882, and 37 unsafe-to-safe versus 12 safe-to-unsafe transitions occurred among changed contexts. Global ranking metrics again remained nearly unchanged, with clean versus poisoned ROC AUC 0.763685 versus 0.765520 and average precision 0.441181 versus 0.443655. The exclusion-set Jaccard overlap was 0.912342.

**Permitted wording:** a small poisoning-induced score perturbation can reproducibly change fixed-budget intervention outcomes by reordering candidates near the decision boundary, even when global ranking metrics remain essentially unchanged.

**Do not claim:** that poisoning improves the underlying hazard model, that poisoning is beneficial in general, that the effect constitutes useful regularization, or that it will persist under different attack mechanisms, budgets, model classes, or domains.

Primary result note: [`research/experiment_154_result.md`](experiment_154_result.md)  
Prospective replication artifact: [`results/prospective_poisoning_boundary_replication.csv`](../results/prospective_poisoning_boundary_replication.csv)

### C5 — Prediction degradation does not imply a consistent fixed-budget decision direction

**Status:** supported negative/falsification result from Experiment 158.

On the prospectively reconstructed target population, poisoning degraded global predictive metrics: ROC AUC fell from 0.794692 to 0.769117, average precision from 0.409900 to 0.395638, and excluded-unsafe recall from 0.780680 to 0.757594. Yet the downstream decision outcome was mixed rather than a clean directional reversal: selected unsafe actions changed only from 358 to 354 while total regret worsened from 12.865555 to 13.399262. The preregistered divergence indicators were both false (`prediction_decision_divergence = 0`, `strong_divergence = 0`).

**Permitted wording:** measurable prediction degradation can coexist with small or mixed changes in a fixed-budget downstream intervention, so predictive and decision metrics must be evaluated separately.

**Do not claim:** a general prediction-decision divergence phenomenon from this experiment; the preregistered divergence criterion did not fire.

Primary artifact: [`results/preregistered_prediction_decision_divergence.csv`](../results/preregistered_prediction_decision_divergence.csv)

### C6 — An intervention-aligned metric can track downstream effects more strongly than global discrimination metrics, but superiority over all global metrics is not yet established

**Status:** partially supported by the preregistered Experiment 163 evaluation.

Across 40 fresh generation seeds, the change in excluded-unsafe recall had a strong association with downstream unsafe-selection change (Spearman rho = -0.907622) and regret change (rho = -0.804072). The corresponding AUC associations were weaker (rho = -0.498384 with unsafe selections; -0.355226 with regret), and AP was intermediate (rho = -0.771977 with unsafe selections; -0.457497 with regret).

The absolute correlation advantage of excluded-unsafe recall over AUC for unsafe selections was 0.409238, with a bootstrap interval of approximately [0.134358, 0.706060], which stayed above zero. Its advantage over AP was smaller at 0.135645, with bootstrap interval approximately [-0.012068, 0.309136], which crossed zero. Therefore the preregistered `primary_metric_superiority_pass` remained false.

**Permitted wording:** in this fresh seeded evaluation, a decision-aligned recall metric tracked downstream intervention effects substantially more strongly than ROC AUC and numerically more strongly than AP, but the preregistered claim of superiority over both global metrics was not confirmed.

**Do not claim:** universal superiority of intervention-aligned metrics, causal sufficiency, or that excluded-unsafe recall is the optimal decision metric across budgets, populations, attacks, or model classes.

Primary artifact: [`results/preregistered_intervention_aligned_metric_superiority.csv`](../results/preregistered_intervention_aligned_metric_superiority.csv)

## Resolved prospective claims

### P1 — The Experiment 153 intervention reversal is purely target-population-specific

**Status:** falsified in its strong form.

Experiment 156 reproduced the same directional fixed-budget intervention effect on a fresh reconstructed target population. The evidence therefore no longer supports describing the Experiment 153 reversal as merely a one-population accident. What replicated, however, was the **boundary-sensitive intervention effect**, not a meaningful improvement in global hazard ranking.

The remaining scientific question is narrower: under which budgets, attack strengths, model classes, and target-population shifts does this boundary-reordering effect persist, reverse, or disappear?

### P2 — Prediction degradation will produce a preregistered prediction-decision divergence on the Experiment 158 population

**Status:** not supported.

Experiment 158 produced clear degradation in global prediction metrics, but the preregistered divergence and strong-divergence flags remained false. This is retained as a negative result. It narrows the useful claim to the need for separate predictive and downstream decision evaluation rather than establishing a general divergence law.

### P3 — The intervention-aligned metric is prospectively superior to both AUC and AP for tracking unsafe-selection changes

**Status:** not supported in the preregistered strong form.

Experiment 163 showed a clear and bootstrap-supported advantage over AUC, but not a bootstrap-supported advantage over AP. The observed ordering was recall > AP > AUC in absolute correlation with unsafe-selection change, yet the recall-versus-AP superiority interval crossed zero. The strong preregistered superiority criterion therefore failed and must remain a negative/partial result.

## Claims currently prohibited by the evidence

- The adaptive-digital-twin problem has been solved.
- The framework has demonstrated deployment-ready safety or control performance.
- The current predictors generalize to real-world cyber-physical or biomedical systems.
- Poisoning is beneficial or acts as reliable regularization.
- The replicated intervention effect means the poisoned hazard model is globally better.
- A general prediction-decision divergence phenomenon has been established.
- Intervention-aligned metrics have been shown to universally outperform global prediction metrics.
- High pooled discrimination alone establishes transferable hazard prediction.
- Support distance alone provides a reliable unsafe-action detector.
- Any biomedical interpretation constitutes clinical validation.

## Promotion rule

A provisional claim should move into the evidence-supported section only after the relevant preregistered or prospectively frozen evaluation has completed and its result survives checks for leakage, population dependence, conditioning effects, threshold sensitivity, and plausible competing explanations. Negative or null results remain part of the ledger rather than being removed when a later favorable result appears.
