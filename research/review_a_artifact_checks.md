# Review A Artifact Checks — Synthesis Lane

## Purpose

These are narrow primary-artifact checks prompted by External Review A (Claude). They are **not final dispositions** and do not alter ADT claims, Experiment 166, generated results, preregistrations, manuscript language, or active workflows. Final reconciliation remains locked until the independent audit lane is available.

## Check ADT-A1 — chronology and preregistration ordering

The frozen chronology records Experiment 154 as the diagnostic that generated the local cutoff/boundary hypothesis, Experiments 155–165 as subsequent prospective/negative/metric tests, and Experiment 166 as the first direct preregistered cutoff-geometry test. This supports the historical distinction between diagnostic hypothesis generation and later prospective adjudication.

**Synthesis-lane status:** no evidence found in the frozen chronology that the Experiment 166 cutoff hypothesis was retroactively presented as preregistered before Experiment 154.

## Check ADT-A2 — Criterion 1 wording versus descriptive switch fraction

The Experiment 166 record reports 308 membership switches with 50.3247% inside the frozen closest-10% band, alongside a Mantel–Haenszel common odds ratio of 10.567477. Those quantities support strong **enrichment relative to the much larger far region** but do not mean that an overwhelming majority of all switches lie near the cutoff.

**Synthesis-lane status:** Claude's distinction between "statistically enriched near" and stronger ordinary-language "concentrated near" wording is materially supported by the reported descriptive fraction. Final wording remains locked pending reconciliation.

## Check ADT-A3 — Criterion 2 structural relationship remains a live issue

The Experiment 166 definitions use the safety composition of clean-only versus poison-only exclusions to construct `net_unsafe_crossing`, while `delta_unsafe_selected` is computed from downstream selected unsafe counts after the corresponding exclusion masks are applied. These are not identical quantities, but both depend on the same clean-versus-poisoned membership changes and unsafe labels. Therefore structural coupling is plausible and cannot be ruled out merely because the observed Spearman correlation is less than 1 in magnitude.

**Synthesis-lane status:** Claude's structural-coupling objection remains unresolved by the frozen primary result alone. A null/contrast analysis may be able to adjudicate it using existing row/context artifacts, but no such analysis is authorized here.

## Check ADT-A4 — Criterion 1 unit of analysis remains a live issue

The frozen pipeline operates on three candidate rows per context and applies a fixed exclusion budget within each generation seed. A row-level contingency analysis stratified by seed therefore contains dependence induced by shared contexts and constrained membership counts. The current review materials do not establish that the nominal Mantel–Haenszel variance fully accounts for those dependencies.

**Synthesis-lane status:** Claude's concern about inferential confidence is not resolved by seed stratification alone. This is distinct from the descriptive observation that switches are enriched near the cutoff.

## Check ADT-A5 — harmful-expansion small-event concern

The tracked `absolute_loss_floor_harmful_expansion_analysis.csv` explicitly reports 65 events, including 15 harmful and 50 beneficial, with the compact calibration model reporting balanced accuracy 0.95, harmful recall 1.0, harmful precision 0.75, ROC AUC 0.9787, mean-fold balanced accuracy 0.9389, and mean-fold ROC AUC 0.9131. The tracked summary does not include an interval estimate for the reported balanced accuracy.

**Synthesis-lane status:** Claude's small-event/uncertainty concern is grounded in the committed summary. This does not invalidate the result; it identifies an uncertainty-reporting question that should be adjudicated from event-level evidence before stronger promotion.

## Lock

No claim change, reanalysis, remediation experiment, or manuscript revision is authorized by this note.