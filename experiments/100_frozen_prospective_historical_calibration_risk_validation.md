# Experiment 100 — Frozen Prospective Historical Calibration-Risk Validation

## Purpose

Experiment 099 identified a historical local calibration-risk representation capable of discriminating severe consequence underestimation using only historical prediction-error information available before the current outcome.

Experiment 100 tests whether that representation generalizes prospectively to an entirely unseen seed block.

This experiment is a representation-validation experiment.

It does **not** modify the controller and does **not** use the prospective outcomes to construct, select, tune, or revise the representation.

---

## Primary Research Question

Can a calibration-risk representation constructed exclusively from historical information available before an action prospectively identify severe consequence underestimation on previously unseen generation seeds?

Formally, the experiment tests whether information of the form

P(severe underestimation | predicted action loss, historical local calibration state)

generalizes prospectively beyond the data used to discover the representation.

---

## Historical Development Data

The representation is frozen from Experiment 099.

Historical development seeds:

44001-44070

Experiment 099 used local neighborhoods of:

k = 7

Severe consequence-underestimation threshold:

prediction error <= -0.050

where prediction error is defined consistently with Experiment 099.

No outcome from the Experiment 100 prospective block may enter the historical representation used to predict that same outcome.

---

## Frozen Primary Representation

The primary representation is the Experiment 099:

loss_plus_local_calibration

feature set.

Its components are:

- predicted_action_loss
- local_mean_error
- local_underestimate_fraction
- local_severe_underestimate_fraction
- local_error_std

The representation and feature definitions are frozen before observing Experiment 100 outcomes.

No feature may be added, removed, transformed, or replaced after prospective outcomes are observed.

---

## Prospective Seed Block

The frozen prospective validation block is:

44071-44090

These seeds must not be used for:

- feature discovery
- feature selection
- model selection
- hyperparameter selection
- neighborhood-size selection
- threshold selection
- exploratory retrospective analysis before validation

---

## Prediction Protocol

For every eligible action-context pair in the prospective block:

1. Construct the pre-action representation.
2. Construct the local historical calibration state using historical observations available prior to the evaluated outcome.
3. Produce the frozen severe-underestimation risk score.
4. Record the prediction.
5. Only afterward evaluate the realized consequence and assign the severe-underestimation target.

The current evaluated outcome must never enter its own predictor representation.

---

## Primary Target

Severe consequence underestimation:

prediction error <= -0.050

Primary positive class:

severe_underestimation

Primary negative class:

nonsevere

---

## Primary Evaluation

The primary prospective evaluation will report:

- ROC AUC
- balanced accuracy
- severe-underestimation recall
- severe-underestimation precision
- nonsevere specificity
- confusion counts
- severe-event prevalence

Seed-level performance will also be reported to determine whether aggregate performance is concentrated in a small number of seeds.

---

## Primary Hypothesis

The frozen historical calibration-risk representation contains prospective information about severe consequence underestimation beyond the current predicted action loss alone.

The primary comparison is:

loss_plus_local_calibration

versus

predicted_loss_only

on the frozen prospective seed block.

Evidence favoring the historical calibration representation requires improvement that is not attributable solely to one isolated seed or a vanishingly small severe-event population.

---

## Secondary Diagnostic Models

For interpretability and decomposition, the following Experiment 099 representations may be evaluated without replacing the primary model:

- predicted_loss_only
- local_mean_error_only
- local_underestimate_fraction_only
- local_severe_fraction_only
- local_error_std_only
- local_calibration_compact

These are secondary diagnostics.

They may not be used post hoc to redefine the primary Experiment 100 hypothesis.

---

## Failure Conditions

The primary prospective hypothesis will not be considered supported if any of the following dominates the result:

1. The historical calibration representation fails to outperform predicted loss alone.
2. Prospective discrimination collapses toward chance.
3. Apparent performance is driven by only one seed or an extremely small number of severe events.
4. Feature behavior reverses materially relative to Experiment 099.
5. Information leakage is discovered.
6. The historical neighborhood construction uses information unavailable before the evaluated outcome.
7. Performance depends on post hoc alteration of the frozen representation.

A negative result is scientifically valid and must be retained.

---

## Interpretation Constraints

Experiment 100 tests predictive representation generalization.

It does not establish that a controller using this representation improves control performance.

It does not establish causal relationships between historical calibration state and harmful adaptation.

It does not authorize modification of the adaptive controller.

Any controller intervention based on this representation requires a separate prospective experiment.

---

## Frozen Experimental Boundary

Before observing seeds 44071-44090, the following are frozen:

- prospective seed block: 44071-44090
- historical development block: 44001-44070
- local neighborhood size: 7
- severe-underestimation threshold: -0.050
- primary representation: loss_plus_local_calibration
- baseline comparison: predicted_loss_only
- feature definitions inherited from Experiment 099
- primary target definition
- primary evaluation metrics

Any later deviation must be explicitly documented and may not silently replace this preregistered analysis.

---

## Scientific Transition

Experiments through 099 established that harmful adaptive expansions are strongly associated retrospectively with consequence-model calibration failure and that historical local prediction-error structure contains pre-action information about severe underestimation.

Experiment 100 asks the next necessary question:

**Can the digital twin use its own historical calibration experience to anticipate an impending consequence-model failure on genuinely unseen data before the outcome occurs?**

---

## Prospective Results

Experiment 100 was executed on the frozen prospective seed block:

44071-44090

The prospective block contained:

- 4,278 action-context observations
- 326 severe-underestimation events
- 3,952 nonsevere events
- severe-underestimation prevalence: 7.620%
- severe events present in all 20 prospective seeds

The prospective block was not used for feature discovery, feature selection, model selection, neighborhood-size selection, or classifier fitting.

### Primary Preregistered Comparison

The frozen primary representation was:

loss_plus_local_calibration

The preregistered baseline was:

predicted_loss_only

Prospective performance was:

| Metric | predicted_loss_only | loss_plus_local_calibration | Change |
|---|---:|---:|---:|
| ROC AUC | 0.639 | 0.743 | +0.103 |
| Balanced accuracy | 61.443% | 68.045% | +6.602 percentage points |
| Severe-underestimation recall | 88.650% | 65.644% | -23.006 percentage points |
| Severe-underestimation precision | 10.007% | 15.485% | +5.478 percentage points |
| Nonsevere specificity | 34.236% | 70.445% | +36.210 percentage points |

The baseline confusion counts were:

- TP = 289
- FP = 2,599
- FN = 37
- TN = 1,353

The primary historical calibration-risk representation produced:

- TP = 214
- FP = 1,168
- FN = 112
- TN = 2,784

Thus, at the frozen 0.50 classification threshold, the historical calibration-risk representation substantially increased specificity and reduced false-positive classifications while also reducing severe-underestimation recall.

The threshold-dependent recall/specificity tradeoff must therefore be distinguished from the threshold-independent discrimination result.

Most importantly, prospective ROC AUC increased from 0.639 to 0.743.

This supports the preregistered hypothesis that historical local calibration information contains predictive information about severe consequence underestimation beyond current predicted action loss alone.

---

## Seed-Level Stability

The primary representation was evaluated across all 20 prospective seeds.

Results were:

- seeds evaluated: 20
- seeds containing severe-underestimation events: 20
- seeds containing at least one true-positive prediction: 20
- mean seed balanced accuracy: 64.450%
- minimum seed balanced accuracy: 52.278%
- mean seed ROC AUC: 0.720
- minimum seed ROC AUC: 0.549

The aggregate prospective result therefore was not produced by a single isolated seed or by a prospective block containing only a negligible number of severe events.

Performance varied across seeds, but prospective discrimination remained distributed across the validation block.

---

## Feature-Direction Transfer

The frozen representation was also evaluated for directional consistency between the historical development population and the prospective population.

Observed severe-versus-nonsevere mean differences were:

| Feature | Development delta | Prospective delta | Direction preserved |
|---|---:|---:|---|
| predicted_action_loss | -0.069957 | -0.043705 | yes |
| local_mean_error | -0.104216 | -0.058984 | yes |
| local_error_std | -0.000355 | +0.006844 | no |
| local_underestimate_fraction | +0.222841 | +0.163395 | yes |
| local_severe_underestimate_fraction | +0.127204 | +0.072403 | yes |

Four of five feature directions were preserved prospectively.

The only reversal occurred for local_error_std, whose development separation was already approximately zero.

The principal historical calibration relationships therefore transferred to the unseen prospective block.

---

## Frozen Primary Model Coefficients

The standardized coefficients of the frozen primary model were:

- predicted_action_loss: +0.432
- local_mean_error: -2.285
- local_error_std: +0.054
- local_underestimate_fraction: +0.181
- local_severe_underestimate_fraction: -0.334

The dominant coefficient was associated with local_mean_error.

This is consistent with the Experiment 099 observation that local historical calibration bias contains substantial information about future severe underestimation risk.

---

## Secondary Diagnostic Results

The preregistered secondary representations produced the following prospective ROC AUC values:

- predicted_loss_only: 0.639
- local_mean_error_only: 0.740
- local_underestimate_fraction_only: 0.728
- local_severe_fraction_only: 0.655
- local_error_std_only: 0.414
- local_calibration_compact: 0.749
- loss_plus_local_calibration: 0.743

The secondary local_calibration_compact representation achieved a numerically higher prospective ROC AUC than the preregistered primary model.

This observation is secondary and does not replace or redefine the primary Experiment 100 hypothesis.

It nevertheless provides additional evidence that the useful prospective signal is concentrated strongly in historical calibration structure itself.

---

## Preregistered Interpretation Check

The preregistered checks produced:

- primary ROC AUC exceeds baseline: yes
- primary balanced accuracy exceeds baseline: yes
- severe events span multiple seeds: yes
- majority of feature directions preserved: yes

Accordingly, the preregistered Experiment 100 interpretation is:

**Prospective evidence favors the frozen historical calibration-risk representation over predicted loss alone.**

---

## Scientific Conclusion

Experiment 099 established retrospectively that local historical prediction-error structure contains pre-action information about severe consequence underestimation.

Experiment 100 extends that result prospectively.

On an untouched 20-seed validation block, a representation constructed from predicted action loss and historical local calibration state discriminated future severe consequence underestimation better than predicted action loss alone.

The primary ROC AUC improvement was:

0.639 -> 0.743

and the primary balanced-accuracy improvement was:

61.443% -> 68.045%.

The prospective population contained 326 severe events distributed across all 20 validation seeds, reducing the likelihood that the result reflects a single-seed anomaly or an extremely sparse positive class.

The experiment therefore provides prospective evidence for the following representation-level claim:

**A digital twin's historical local calibration experience contains information that can help anticipate future consequence-model underestimation before the evaluated consequence is observed.**

This result remains predictive rather than causal.

Experiment 100 does not establish that acting on the calibration-risk signal improves controller performance, and no controller behavior was modified during this experiment.

A controller intervention based on historical calibration-risk information requires a separately preregistered prospective experiment.

---

## Experimental Status

Experiment 100: COMPLETE

Primary preregistered hypothesis: SUPPORTED

Controller modification: NONE

Primary prospective result:

loss_plus_local_calibration outperformed predicted_loss_only on both ROC AUC and balanced accuracy on seeds 44071-44090.

Next experimental transition:

**Move from prospective representation validation to the design of a separately frozen calibration-aware controller intervention.**