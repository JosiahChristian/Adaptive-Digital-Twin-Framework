# ADT Publication Packaging Plan — 2026-08-17

**Status:** review-branch publication-engineering record. This plan does not modify experiment code, preregistrations, generated scientific results, active workflows, or historical records.

## Governing rule

Every figure and table must be reproducible from a committed primary artifact or an explicitly identified derived manuscript source whose provenance is traceable to committed evidence. A visually convenient artifact must not be substituted for the scientifically controlling artifact.

## Critical provenance safeguard

`results/audit/experiment_166_matched_nonpoison_control_result.json` is the **earlier inadequate matched-control run**, not the later stronger adequately matched control. It reports mean exclusion Jaccard 0.988819, 42 membership switches, and `match_adequacy_pass: false`. It must not be used to render the later poisoning-specificity comparison.

The later stronger-control GitHub Actions artifact has now been directly recovered and digest-verified without rerunning the experiment. See `research/manuscript/experiment_166_stronger_control_artifact_verification_2026-08-17.md`.

Verified stronger-control provenance:

- run ID `32074736542`;
- artifact ID `9303122672`;
- producing head SHA `2a099bcfe339da876a7c5f0fb018c56f3776ecd9`;
- artifact SHA-256 `ced924c850aa5f6b5dd2923bcd6e761f00a3a15bbae620c639c4084fa876c904`;
- preserved aggregate `summary.json` and seed-level `paired_seed_results.csv`;
- primary decision `specificity_unresolved`.

The downloaded ZIP hash exactly matched GitHub's recorded digest. Direct provenance for the stronger matched-control numerical comparison is therefore **verified**. The earlier inadequate-control JSON remains scientifically distinct and must never be substituted.

## Recommended manuscript displays

### Table 1 — Experiment 166 adjudication ledger

Purpose: prevent the original positive result from visually dominating later falsification/adjudication evidence.

Rows:

- original cutoff-band localization criterion — MH OR 10.567477, 95% CI [8.345537, 13.380992], original criterion passed;
- original Criterion 2 — rho -0.873179, 95% bootstrap CI [-0.946362, -0.735018], original criterion passed;
- bookkeeping-preserving null — observed rho approximately -0.87318, one-sided null probability 0.53315, not independent mechanistic evidence;
- downstream near-only vs far-only selected-action change — difference -0.31554, 95% CI [-0.40818, -0.23161], preferential near-switch interpretation not supported;
- stronger matched-control poison-minus-control localization — difference 0.001845, 95% CI [0.0000, 0.00554], frozen specificity criterion not met.

Source rule: each row must cite its controlling committed artifact/adjudication record. The stronger-control row must be sourced from the digest-verified stronger-control artifact/provenance note, never from the earlier inadequate-control JSON.

### Figure 1 — Cutoff-localization comparison

Preferred display: poison and stronger matched-control mean near-minus-far enrichment with the paired poison-minus-control contrast and seed-bootstrap uncertainty. The verified stronger-control artifact supplies both aggregate and paired seed-level source data.

Required caption language:

> Similar cutoff localization was observed under poisoning and an adequately perturbation-matched label-preserving non-poison control; the frozen poisoning-specificity criterion was not met.

Prohibited visual framing:

- labeling the effect a poisoning signature;
- omitting the matched control while displaying only the original poison enrichment;
- using the inadequate earlier matched-control run as the comparison;
- implying that a CI touching zero proves absence of all poisoning-specific effects.

### Figure 2 — Harmful-expansion timing-validity comparison

Preferred display: headline outcome-informed compact model versus temporally legitimate loss-surface-only model family.

Required separation:

- approximately 0.979 ROC AUC labeled **retrospective/outcome-informed**;
- non-leaking ROC AUC range approximately 0.683-0.711 labeled **exploratory pre-decision-compatible**;
- no bar/legend may label the 0.979 result as prospective or deployable prediction.

Because the non-leaking results may exist across multiple folds/model variants, final rendering should use the committed event/fold/result artifacts identified in `harmful_expansion_timing_leakage_audit_2026-08-17.md`, not manually transcribed numbers alone.

## Table/figure balance rule

Any display of a historically favorable statistic must place the later validity constraint in the same table, figure caption, or immediately adjacent manuscript text. Negative or falsifying results cannot be moved solely to supplementary material while the superseded favorable interpretation remains in the main text.

## Submission packaging checklist

Before final submission:

- [x] Resolve direct provenance for the stronger matched-control numerical row/figure source.
- [ ] Generate all manuscript figures from version-controlled manuscript-generation code or documented source tables.
- [ ] Include figure captions that preserve `specificity_unresolved` as “not established,” not “proved absent.”
- [ ] Ensure the retrospective 0.979 model is never visually grouped with valid pre-decision models without an explicit timing label.
- [ ] Export a clean reference list in the target venue style.
- [ ] Produce a machine-readable source map from every figure/table value to repository path, workflow artifact, and/or commit.
- [ ] Re-run the whole-manuscript hostile review after final figure insertion.

## Current packaging verdict

The manuscript is review-ready and the stronger-control provenance gate is resolved. Final-submission readiness now requires provenance-safe figure rendering, source mapping, and venue packaging rather than any new scientific experiment or stronger claim.