# ADT Manuscript Submission-Readiness Audit — 2026-08-17

**Scope:** end-to-end audit of `research/manuscript/manuscript.md` on the review branch after claim reconciliation, sentence-level evidence checking, methods/reproducibility expansion, and literature positioning. No experimental machinery or historical artifacts are modified by this record.

## Verdict

**REVIEW-READY MANUSCRIPT CANDIDATE; NOT YET FINAL-SUBMISSION-READY.**

The narrowed scientific claims are internally consistent with the current committed evidence and closed-evidence adjudication. No new ADT experiment is required solely to support the claims currently made in the manuscript. Final submission packaging still requires venue formatting and resolution/documentation of the stronger-control result discoverability issue described below.

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

A balanced claim-adjudication table now places original favorable evidence beside later discriminating/falsifying evidence. This reduces the risk that the preregistered positive Experiment 166 statistics or approximately 0.979 retrospective AUC receive disproportionate visual emphasis.

Publication-quality figures are not yet required for scientific review readiness. If figures are added later, they must preserve the same balance and must not plot superseded headline metrics without timing/claim labels.

### 8. Reproducibility paths and artifact discoverability — PARTIAL

The following are directly discoverable on `main`:

- Experiment 166 preregistration;
- original Experiment 166 result summary;
- stronger matched-control prospective protocol;
- existing-artifact structural adjudication materials;
- earlier weaker matched-control failure;
- harmful-expansion primary artifacts and leakage audit;
- current claim matrix and reconciliations.

**Outstanding documentation issue:** the final stronger matched-control numerical adjudication is preserved in the committed pre-quadrangulation reconciliation and CI provenance, but there is no standalone stronger-control result file on `main` at the analogous audit result path. This should not be repaired by fabricating or rerunning the experiment. If the original CI artifact/result output is recoverable, it should be preserved as a directly discoverable evidence artifact before final submission. If it is not recoverable, the manuscript and repository must continue to disclose that provenance limitation explicitly.

### 9. Cross-repository non-conflation — PASS

The manuscript explicitly prevents the adversarial-RL repository from being treated as mechanistic corroboration, statistical replication, or cross-domain validation of ADT.

## Citation verification notes

The following manuscript entries were directly rechecked against primary publisher/proceedings records during this gate:

- Elmachtoub & Grigas, *Smart Predict, then Optimize*, Management Science 68(1):9-26.
- Elmachtoub, Liang & McNellis, ICML/PMLR 119:2858-2867.
- Mandi et al., ICML/PMLR 162:14935-14947.
- Heuton et al., ICML/PMLR 267:23136-23154.
- Chen & Suh, ICML/PMLR 37:371-380.
- Asudeh et al., *On Obtaining Stable Rankings*.
- Kapoor & Narayanan, Patterns 4(9):100804.
- Qiu et al., Scientific Reports 15:11078.
- Splettstößer, Ellwein & Wortmann, Procedia CIRP 119:867-872.
- Builes-Montaño et al., Scientific Reports 15:39738.

## Current publication boundary

The manuscript is ready to be treated as a **review-ready publication candidate** for the current narrow claims. It is not yet a final submission package because journal/conference formatting, final figures/tables, metadata, and the stronger-control result-artifact discoverability issue remain outside this gate.

## Next gate

Proceed to the adversarial-RL evidence-completion/manuscript gate in parallel. For ADT, do not launch a new experiment unless a stronger causal, poisoning-specific, prospective-prediction, or broader-generalization claim is intentionally reintroduced.