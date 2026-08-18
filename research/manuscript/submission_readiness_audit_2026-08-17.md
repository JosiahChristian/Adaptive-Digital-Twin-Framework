# ADT Manuscript Submission-Readiness Audit — 2026-08-17

**Scope:** end-to-end audit of `research/manuscript/manuscript.md` on the review branch after claim reconciliation, sentence-level evidence checking, methods/reproducibility expansion, literature positioning, and publication-provenance verification. No experimental machinery or historical artifacts are modified by this record.

## Verdict

**REVIEW-READY MANUSCRIPT CANDIDATE; NOT YET FINAL-SUBMISSION-READY.**

The narrowed scientific claims are internally consistent with the current committed evidence and closed-evidence adjudication. No new ADT experiment is required solely to support the claims currently made in the manuscript. The stronger-control CI artifact has now been recovered and digest-verified without rerunning the experiment, so the earlier discoverability blocker is resolved. Final submission packaging still requires final figure/table rendering, source-map completion checks, and venue-specific formatting.

## Gate checks

### 1. Claim-to-evidence traceability — PASS

- Original Experiment 166 numerical claims match `results/preregistered_cutoff_geometry_mechanism.csv`.
- Historical preregistered mechanism wording is preserved as chronology but is explicitly superseded for present interpretation by later adjudication.
- Criterion-2 structural-null, downstream-specificity, and poisoning-specificity boundaries match the committed reconciliation.
- Harmful-expansion timing/leakage language matches the committed leakage audit and does not use the leaked headline metrics as pre-decision evidence.
- The publication claim matrix and manuscript are aligned.

### 2. Preregistration chronology — PASS

The manuscript reports the original Experiment 166 co-primary pass before the later structural and matched-control falsification/adjudication analyses. It does not rewrite the historical preregistration as though the later objections were known in advance.

### 3. Unit of analysis and uncertainty language — PASS WITH SCOPE LIMITATION

- Generation seed is identified as the inferential resampling unit for later seed-bootstrap analyses.
- Candidate/action rows are explicitly treated as nested observations, not independent experimental replications.
- The original Mantel-Haenszel analysis is described as seed-stratified.
- Harmful-expansion seed holdout is not represented as curing temporal leakage.
- The manuscript does not claim uncertainty that is absent from the committed exploratory non-leaking harmful-expansion models.

### 4. Abstract / Results / Discussion / Conclusion consistency — PASS

All four sections preserve the same hierarchy:

1. near-cutoff localization exists within the tested fixed-budget pipeline;
2. poisoning specificity is not established;
3. the original Criterion-2 association is not independent mechanistic evidence;
4. preferential downstream near-switch influence failed in the tested analysis;
5. the approximately 0.979 harmful-expansion result is retrospective, not pre-decision;
6. temporally legitimate harmful-expansion discrimination remains exploratory.

No section silently restores a stronger claim rejected elsewhere.

### 5. Negative-result visibility — PASS

The manuscript contains a dedicated negative/failed-results section and also integrates the principal falsification results into the main Results and Discussion rather than relegating them solely to limitations.

### 6. Literature positioning — PASS

External literature is used only for disciplinary or methodological context. The manuscript contains an explicit literature-to-evidence boundary and a separate literature-positioning audit. Primary-source checks support the cited background propositions concerning predict-then-optimize decision loss, top-K boundary separation, ranking stability, adaptive digital-twin use, and leakage.

No external citation is permitted to establish Experiment 166 poisoning specificity, causal mechanism, or harmful-expansion leakage; those are determined by internal artifacts.

### 7. Visual/reporting balance — PASS FOR REVIEW DRAFT

A balanced claim-adjudication table places original favorable evidence beside later discriminating/falsifying evidence. This reduces the risk that the preregistered positive Experiment 166 statistics or approximately 0.979 retrospective AUC receive disproportionate visual emphasis.

Publication-quality figures are not yet required for scientific review readiness. The review branch now contains a digest-gated plotting source for the stronger-control comparison and a publication packaging plan that requires captions to preserve the narrowed interpretation.

### 8. Reproducibility paths and artifact discoverability — PASS WITH FINAL-PACKAGING REQUIREMENT

The following are directly discoverable on `main`:

- Experiment 166 preregistration;
- original Experiment 166 result summary;
- stronger matched-control prospective protocol;
- existing-artifact structural adjudication materials;
- earlier weaker matched-control failure;
- harmful-expansion primary artifacts and leakage audit;
- current claim matrix and reconciliations.

The final stronger-control output is not committed as a standalone result file on `main`, but the original CI artifact has now been directly recovered and verified:

- run ID `32074736542`;
- artifact ID `9303122672`;
- artifact name `experiment166-stronger-label-preserving-control`;
- producing head SHA `2a099bcfe339da876a7c5f0fb018c56f3776ecd9`;
- artifact SHA-256 `ced924c850aa5f6b5dd2923bcd6e761f00a3a15bbae620c639c4084fa876c904`;
- downloaded ZIP digest exactly matched GitHub's recorded digest;
- archive contains aggregate `summary.json`, `summary.csv`, candidate diagnostics, and paired seed-level results.

See `research/manuscript/experiment_166_stronger_control_artifact_verification_2026-08-17.md` and `research/manuscript/source_map.json`.

This resolves the scientific provenance/discoverability ambiguity for manuscript preparation. Final packaging should preserve a durable source pointer or archival copy consistent with repository policy before the temporary Actions artifact expires; doing so is documentation/reproducibility work, not a new experiment.

### 9. Cross-repository non-conflation — PASS

The manuscript explicitly prevents the adversarial-RL repository from being treated as mechanistic corroboration, statistical replication, or cross-domain validation of ADT.

## Citation verification notes

The manuscript literature entries were checked against their primary publisher/proceedings records during the literature-positioning gate. The external literature remains contextual and cannot supersede the internal experimental adjudications.

## Current publication boundary

The manuscript is ready to be treated as a **review-ready publication candidate** for the current narrow claims. It is not yet a final submission package because target-venue formatting, final rendered figures/tables, metadata, and durable packaging of the verified stronger-control artifact/source pointer remain outside this gate.

## Next gate

Finalize provenance-safe figures/tables and choose a target venue/format. Do not launch a new experiment unless a stronger causal, poisoning-specific, prospective-prediction, or broader-generalization claim is intentionally reintroduced.