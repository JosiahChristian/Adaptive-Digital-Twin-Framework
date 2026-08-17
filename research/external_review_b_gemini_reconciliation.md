# External Review B (Gemini) — frozen-snapshot reconciliation record

## Status

This file preserves the major findings supplied by the blind Gemini pre-quadrangulation reviewer and performs an initial artifact-level adjudication against the **frozen reviewer snapshot** `d1e3285707ed788a39c7e883c157a8a359cde7db`.

It is a review/reconciliation artifact only. It does **not** alter Experiment 166, regenerate results, modify preregistrations, authorize remediation analyses, or change manuscript claims. The manuscript/claim gate remains frozen pending completion of the remaining independent audit lane and final cross-review reconciliation.

## Review-B headline findings received

Gemini characterized:

1. Experiment 166 as a purported mathematical tautology/order-statistic artifact and assigned a fatal severity to the mechanistic claim.
2. The harmful-expansion line as fatally unstable because of an alleged effective event count of 1 positive case among 41 observations and alleged leakage/post-hoc feature construction.
3. The adversarial-RL detector as failing in subtle regimes and succeeding only under obvious policy degradation.
4. The two research lines as conceptually overfit to a shared diagnostic narrative.

The following sections separate portions that survive direct artifact checking from portions that do not.

## ADT-B1 — Experiment 166: claimed same-vector mathematical identity

### Gemini allegation

Gemini's displayed derivation described a cutoff feature and selected action as non-independent functions of the **same loss vector**, and concluded that the observed Experiment 166 association is a mathematical identity rather than an empirical/computational relationship.

### Frozen code check

That specific derivation does **not match the implemented variables**.

Experiment 166 constructs the clean and poisoned exclusion masks from **hazard-model probabilities**:

- `cs = clean_model.predict_proba(g[FEATURES])[:,1]`
- `ps = poison_model.predict_proba(g[FEATURES])[:,1]`
- `cm = topn(cs,k)`
- `pm = topn(ps,k)`

where `FEATURES = ['action_2','action_3','context_support_distance']`.

The downstream selected action is then chosen among the non-excluded candidates using a **different stored quantity**, `predicted_action_loss`:

- `losses = c.predicted_action_loss.to_numpy(float)`
- `j = min(avail, key = predicted_action_loss, action tie-break)`

Therefore the exclusion cutoff and downstream argmin are **not two deterministic functions of one common loss vector**, as Review B states.

### Initial disposition

**Review-B's exact “same loss vector / mathematical identity” proof: UNSUPPORTED by the frozen implementation.**

This does **not** resolve the legitimate structural objections identified independently elsewhere:

- a fixed top-k rule over highly correlated clean/poison hazard scores can generically localize membership changes near a boundary;
- Criterion 2 (`net_unsafe_crossing` versus `delta_unsafe_selected`) may still contain substantial pool-composition coupling;
- Criterion 1 still requires context/seed-aware robustness analysis;
- no matched non-poisoning score-perturbation control currently establishes poisoning-specific localization.

Accordingly, Gemini's *fatal proof* is rejected, while the broader mechanism claim remains provisional for independent reasons.

## ADT-B2 — Experiment 166: order-statistics concern

The frozen code does support the premise that Criterion 1 compares changes in two fixed-budget top-k masks derived from clean and poison hazard scores. Generic order-statistic boundary sensitivity therefore remains a valid alternative explanation requiring adjudication.

**Initial disposition: CONFIRMED AS A MAJOR UNRESOLVED ALTERNATIVE EXPLANATION, but not proven to be a tautology.**

No new control is executed in this file.

## ADT-B3 — harmful-expansion sample-size allegation

### Gemini allegation

Review B states that the harmful-expansion analysis has an effective event count of **1 positive case out of 41 observations (2.44%)**.

### Frozen primary-result check

The committed `results/absolute_loss_floor_harmful_expansion_analysis.csv` reports:

- `events = 65`
- `harmful_events = 15`
- `beneficial_events = 50`

for the principal compact calibration model, with the same 15/50 class counts reflected in the diagnostic rows.

### Initial disposition

**The specific 1/41 (2.44%) premise is FALSE for the frozen primary artifact.**

The true 15/65 harmful-event count is still small enough to justify uncertainty/small-sample concern, so interval estimation and stability remain legitimate audit questions. But Review B's fatal classification based on 1/41 cannot be retained.

## ADT-B4 — harmful-expansion leakage allegation

Review B also asserted feature leakage/post-decision construction. The aggregate CSV alone cannot establish that allegation. It requires direct inspection of the generation/timing code and source variables.

**Initial disposition: UNRESOLVED / REQUIRES CODE-LEVEL TIMING AUDIT.**

It must not be upgraded to a confirmed defect merely because Review B stated it.

## ADT-B5 — cross-repository conceptual overfitting

Review B inferred conceptual overfitting partly from the two review indexes. Review indexes are process/navigation artifacts, not primary scientific evidence of hypothesis contamination.

No direct evidence was supplied showing that ADT outcomes were used to choose adversarial-RL hypotheses or vice versa.

**Initial disposition: NOT ESTABLISHED.** Keep open only as a provenance/chronology question for final reconciliation.

## Review-B severity corrections at this stage

| Review-B finding | Review-B severity | Artifact-grounded status now |
|---|---|---|
| Exp166 same-loss-vector tautology | FATAL | **Rejected as formulated**; implementation uses hazard scores for exclusion and a separate `predicted_action_loss` for downstream selection |
| Generic top-k/order-statistic localization | embedded in fatal finding | **Major unresolved alternative explanation** |
| Harmful expansion has 1/41 positives | FATAL | **Factually contradicted** by frozen result: 15 harmful / 65 events |
| Harmful-expansion leakage | FATAL/part of headline | **Unresolved; code audit required** |
| Cross-repository conceptual overfitting | MAJOR | **Not established from evidence supplied** |

## Claim gate

No manuscript conclusion is changed by this reconciliation record. In particular:

- Experiment 166's historical preregistered pass remains preserved;
- the stronger local cutoff-geometry mechanism interpretation remains provisional;
- Gemini's claim that the result is already proven to be a mathematical identity is not accepted;
- harmful-expansion claims remain provisional pending uncertainty and timing/leakage audit, but are not struck on the false 1/41 premise;
- all negative/null/failed results remain visible.

## Next adjudication gates

Without executing them yet, the remaining high-information questions are:

1. context/seed-respecting robustness for Criterion 1;
2. a valid bookkeeping-preserving null for Criterion 2;
3. near-cutoff versus far-cutoff downstream specificity;
4. code-level timing/leakage audit of harmful-expansion features;
5. only after independent-review reconciliation, decide whether a matched clean-to-clean perturbation control is needed.
