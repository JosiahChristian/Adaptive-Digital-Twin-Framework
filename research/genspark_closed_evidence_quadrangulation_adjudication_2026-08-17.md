# Genspark closed-evidence quadrangulation adjudication — 2026-08-17

## Scope

Review/synthesis artifact only. This note preserves and adjudicates the externally generated Genspark GPT-5.6 Luna closed-evidence review. It does not modify experiment code, preregistrations, generated scientific results, active workflows, or manuscript conclusions.

## Protocol validity

A delivery-handshake was completed before the substantive review. The reviewer explicitly acknowledged closed-evidence mode, confirmed visibility of the inline evidence dossier and delivery marker, and did not begin scientific review during the handshake. The substantive response contained no external URLs, citations, literature references, or other obvious web-derived material. The review is therefore admissible as a closed-evidence external quadrangulation component.

## ADT claim adjudication

### Experiment 166 poisoning specificity

External verdict: **NOT SUPPORTED**.

Adjudicated interpretation: this is consistent with the repository's frozen `specificity_unresolved` result. The external categorical label should not be read as proof that poisoning can never have a specific effect; it means the current evidence does not support poisoning-specific cutoff localization.

### Experiment 166 cutoff-localization phenomenon

External verdict: **SUPPORTED ONLY WITH NARROWER WORDING**.

The reviewer independently distinguished phenomenon from mechanism and endorsed only pipeline-specific wording: the tested fixed-budget top-N ranking pipeline exhibits near-cutoff concentration of membership switches under both poisoning and the matched non-poison control.

### Criterion 2 / downstream causal-preferential mechanism

External verdict: **INVALIDATED BY DESIGN/ANALYSIS**.

The reviewer relied on the bookkeeping-preserving null, which reproduced the strong correlation, and on the later near-versus-far downstream-specificity analysis, whose observed direction contradicted the preferential near-switch interpretation. This independently converges with the internal audit that Criterion 2 cannot serve as independent mechanistic evidence.

### Harmful-expansion headline pre-decision predictor

External verdict: **INVALIDATED BY DESIGN/ANALYSIS**.

The reviewer independently identified that `loss_floor_error` and `expanded_action_loss_error` depend on post-outcome quantities and therefore cannot support a pre-decision prediction claim. It also explicitly rejected the idea that seed-held-out cross-validation cures this temporal leakage.

### Non-leaking loss-surface-only signal

External verdict: **SUPPORTED ONLY WITH NARROWER WORDING**.

The reviewer accepted only an exploratory, dataset- and evaluation-dependent discrimination claim and required prospective evaluation for any stronger predictive statement.

## Publication recommendation

External recommendation: **READY AFTER DOCUMENTATION CORRECTION**.

The reviewer concluded that no new scientific experiment is required before publication of appropriately narrowed claims, provided the manuscript accurately documents:

- unresolved poisoning specificity;
- the bookkeeping-preserving null failure of Criterion 2 as independent mechanism evidence;
- falsified downstream near-switch specificity;
- confirmed timing leakage in the headline harmful-expansion model;
- preserved negative and failed results;
- narrow simulator/pipeline scope.

## Claim boundary after quadrangulation

The external review does not justify strengthening any ADT claim beyond the current internal audits. It independently supports the following publication boundary:

1. Near-cutoff localization is an empirical phenomenon in the tested fixed-budget ranking pipeline.
2. Poisoning specificity is not established.
3. The original Criterion-2 mechanistic interpretation is not independent evidence of causality or preferential near-cutoff influence.
4. The `calibration_compact` harmful-expansion model is retrospective outcome-informed discrimination, not valid pre-decision prediction.
5. Temporally legitimate loss-surface-only variants remain exploratory.

## Experiment gate

No new ADT experiment is required solely to publish these narrowed claims. New experiments become scientifically necessary only if the manuscript seeks stronger causal, poisoning-specific, prospective-prediction, or generalization claims.
