# Publication-candidate staleness audit — 2026-08-17

## Scope

Review/synthesis artifact only. This note does not edit the historical publication-candidate synthesis, experiment code, preregistrations, generated scientific results, active workflows, or manuscript conclusions.

## Finding

`research/publication_candidate.md` predates the completed harmful-expansion timing/leakage audit and is no longer a current statement of the evidence boundary.

The historical document frames the candidate contribution as compact **pre-decision** loss-surface features identifying harmful expansion and lists the `calibration_compact` model's approximately 0.950 balanced accuracy and 0.979 ROC AUC as evidence currently in favor. It also lists a timing/leakage audit as a future publication gate.

That gate has now been completed and failed for the headline model's pre-decision interpretation. The compact model contains `loss_floor_error` and `expanded_action_loss_error`, which depend on `true_best_loss` and `realized_expanded_action_loss`, respectively. These are post-outcome quantities. The strongest coefficient is the post-outcome expanded-action residual. Seed-held-out cross-validation does not cure feature-time leakage.

## Adjudication

**The historical publication candidate is superseded in its positive pre-decision framing.**

The approximately 0.979 AUC / 0.950 balanced-accuracy result may be retained only as retrospective outcome-informed discrimination. It cannot be the positive anchor for a paper claiming pre-decision harmful-expansion prediction.

The non-leaking loss-surface-only variants provide weaker exploratory discrimination (pooled AUC approximately 0.68–0.71 in the committed summary), but the current evidence does not yet establish prospective predictive performance.

## Current publication implication

A paper centered on validated pre-decision harmful-expansion prediction is **not currently supported** by the existing headline model. Two scientifically legitimate paths remain:

1. If harmful-expansion prediction is central, prospectively freeze a temporally valid feature set and test it on genuinely held-out evidence with seed-compatible uncertainty and simple baselines.
2. If it is peripheral, preserve the leakage result as a negative methodological finding and do not spend another experiment attempting to rescue the old headline model.

The Experiment 166 line should also remain bounded to a robust cutoff-localization phenomenon in the tested fixed-budget pipeline; matched label-preserving perturbations do not currently support poisoning specificity.

## Review rule

Future reviewers should read `research/publication_candidate.md` as historical hypothesis-generation context, not as a current publication recommendation. Current claim boundaries are governed by the later leakage audit, Experiment 166 reconciliation, and post-audit supersession note.
