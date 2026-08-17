# Harmful-expansion timing and leakage audit — 2026-08-17

## Scope

Review-only adjudication of committed artifacts. This audit does not modify experiment code, preregistrations, generated scientific results, active workflows, or manuscript conclusions.

## Question

Can the reported `calibration_compact` harmful-expansion classifier be interpreted as a pre-decision predictor using information available before the expansion decision?

## Primary evidence inspected

- `results/absolute_loss_floor_harmful_expansion_analysis.csv`
- `results/absolute_loss_floor_harmful_expansion_analysis_events.csv`
- `results/absolute_loss_floor_harmful_expansion_analysis_calibration.csv`
- `results/absolute_loss_floor_harmful_expansion_analysis_coefficients.csv`
- `results/absolute_loss_floor_harmful_expansion_analysis_folds.csv`
- `research/claim_ledger.md`

## Findings

### 1. The event count is 65, with 15 harmful and 50 beneficial events

The primary summary artifact reports 65 total events, 15 harmful events, and 50 beneficial events. This confirms that the earlier external-review premise of 1 harmful event among 41 events was not a description of this committed primary analysis.

### 2. The highest-performing `calibration_compact` model contains post-outcome information

The model is explicitly defined as:

`predicted_loss_floor | loss_floor_error | expanded_action_loss_error`

The event artifact makes the relevant identities recoverable from the stored columns:

- `loss_floor_error = predicted_loss_floor - true_best_loss`
- `expanded_action_loss_error = predicted_action_loss - realized_expanded_action_loss`

`true_best_loss` and `realized_expanded_action_loss` are realized/ground-truth quantities, not pre-decision model outputs. Therefore both residual features require information unavailable at the time a prospective expansion decision would have to be made.

### 3. The leakage is material, not merely nominal

The coefficient artifact reports mean absolute coefficient magnitudes for `calibration_compact` of approximately:

- `predicted_loss_floor`: 0.5034
- `loss_floor_error`: 0.5070
- `expanded_action_loss_error`: 2.5928

The post-outcome expanded-action residual is therefore the dominant term by a large margin in the fitted model.

### 4. Seed-held-out cross-validation does not remove this form of leakage

The fold artifact holds out generation seeds, which is useful for dependence control across generated populations. However, each held-out event row still contains `loss_floor_error` and `expanded_action_loss_error`, and those features themselves encode held-out realized outcomes. Cross-validation can prevent training-row reuse; it cannot make a post-outcome feature prospectively available.

Accordingly, the reported `calibration_compact` performance — balanced accuracy 0.95, harmful recall 1.00, harmful precision 0.75, ROC AUC about 0.979, mean fold balanced accuracy about 0.939, and mean fold ROC AUC about 0.913 — is valid only as retrospective discrimination using outcome-informed residuals. It is not valid evidence for a deployable or genuinely pre-decision classifier.

### 5. Non-leaking pre-decision-only variants remain informative but weaker

The same summary reports models using only quantities labeled as predictions available from the loss surface, including `predicted_loss_floor`, `predicted_loss_mean`, `predicted_loss_ceiling`, `predicted_loss_spread`, `predicted_action_loss`, and combinations of these. Their pooled ROC AUC values are approximately 0.683–0.711 and balanced accuracies approximately 0.663–0.763, materially below the leaked calibration model.

Some seed folds contain no harmful events, producing undefined fold-level balanced accuracy/AUC. The event population is also small and imbalanced (15 harmful versus 50 beneficial). These models therefore provide exploratory evidence that pre-decision loss-surface quantities may contain signal, but the current artifacts do not justify importing the leaked model's near-perfect discrimination into that claim.

## Adjudication

**CONFIRMED LEAKAGE FOR THE HEADLINE `calibration_compact` PRE-DECISION INTERPRETATION.**

The model itself may remain a valid retrospective diagnostic/classification analysis. The problem arises only if its performance is described as prediction from information available before the expansion outcome.

## Claim impact

The current claim-ledger statement that compact pre-decision loss-surface features contain substantial predictive signal is too strong insofar as it relies on the `calibration_compact` headline metrics. The strongest model includes post-outcome residuals and cannot support pre-decision predictive wording.

A narrower statement is defensible from the existing non-leaking variants: **pre-decision loss-surface-only features show exploratory discriminatory signal in the documented event population, but prospective predictive performance has not yet been established.**

This audit does not directly alter `research/claim_ledger.md`; the inconsistency is intentionally preserved for explicit reconciliation rather than silently rewriting the historical claim record.

## Next evidence gate

Do not rerun the leaked model merely with different cross-validation. If this claim is central enough to retain, prospectively freeze a pre-decision-only feature set before any new outcome labels are inspected, keep all features computable at decision time, use generation seed as the primary grouping unit, and report uncertainty compatible with the small harmful-event count. A simple baseline should be included.

If the harmful-expansion predictor is not central to the final ADT contribution, no new experiment is required: retain the retrospective diagnostic result, downgrade the prospective prediction claim, and carry the negative leakage adjudication into quadrangulation.
