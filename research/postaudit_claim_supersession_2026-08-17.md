# Post-audit claim supersession — 2026-08-17

## Scope

Review/synthesis artifact only. This note does not alter experiment code, preregistrations, generated scientific results, active workflows, or manuscript conclusions. Historical claim records remain preserved for chronology.

## Purpose

The completed harmful-expansion timing/leakage audit post-dates parts of `research/claim_ledger.md` and the earlier pre-quadrangulation reconciliation. This note records which older claim language is no longer current so that reviewers do not mistake preserved historical wording for the present evidentiary boundary.

## Superseded ADT harmful-expansion wording

The historical Claim C1 in `research/claim_ledger.md` states that compact pre-decision loss-surface features contain substantial predictive signal and cites the `calibration_compact` model's approximately 0.95 balanced accuracy and 0.979 ROC AUC.

That performance cannot support a pre-decision prediction claim because the model includes:

- `loss_floor_error = predicted_loss_floor - true_best_loss`
- `expanded_action_loss_error = predicted_action_loss - realized_expanded_action_loss`

Both residual features require realized outcome information unavailable at the claimed prediction time. Seed-held-out cross-validation does not correct feature-time leakage. The dominant mean absolute coefficient in the compact model is the post-outcome `expanded_action_loss_error` term (approximately 2.593 versus approximately 0.503 and 0.507 for the other two terms).

### Current status

**The historical C1 wording is superseded for prospective/pre-decision interpretation.**

Current defensible wording from committed artifacts is:

> Pre-decision loss-surface-only quantities show exploratory discriminatory signal in the documented generated event population, but prospective predictive performance has not been established. The near-perfect `calibration_compact` performance is retrospective outcome-informed discrimination and must not be cited as pre-decision prediction performance.

No new experiment is required merely to repair the claim boundary. A new prospectively frozen pre-decision-only study is warranted only if harmful-expansion prediction is retained as a central scientific contribution.

## Experiment 166 status after matched-control audit

The earlier preregistered Experiment 166 criteria remain preserved as historical results, but the combined audited evidence supersedes any poisoning-specific mechanistic interpretation.

Current defensible wording is:

> In the tested fixed top-N ranking/intervention pipeline, perturbation-induced membership changes robustly localize near the intervention cutoff. A prospectively frozen label-preserving perturbation matched to the poisoning condition in ranking magnitude reproduced essentially the same localization, so poisoning specificity is not established. The preregistered composition-to-decision correlation is not independent mechanistic evidence under a bookkeeping-preserving null, and near-only switches did not preferentially produce downstream selected-action changes.

Accordingly, no further Experiment 166 control should be launched simply to recover poisoning specificity.

## Current pre-quadrangulation state

For any future external or quadrangulation review, the following documents should be interpreted together:

1. historical primary experiment artifacts and preregistrations;
2. `research/prequadrangulation_claim_reconciliation_2026-08-17.md`;
3. `research/harmful_expansion_timing_leakage_audit_2026-08-17.md`;
4. this supersession note.

Where older review/ledger wording conflicts with the completed later audit, the later adjudication governs the current claim boundary while the older text remains preserved as provenance.
