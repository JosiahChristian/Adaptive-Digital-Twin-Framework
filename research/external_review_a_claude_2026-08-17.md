# External Review A — Claude Pre-Quadrangulation Review

## Status

Frozen external review record captured from the 2026-08-17 Claude hostile pre-quadrangulation review. This file records the reviewer's findings and scope only. It does **not** adjudicate the findings, alter scientific claims, modify Experiment 166, or authorize remediation experiments.

The reviewer explicitly reported having read the ADT research review index, Experiment 166 preregistration, Experiment 166 adjudication code, Experiment 166 primary result CSV, decision-aware chronology, claim ledger, and Experiment 166 interpretation. The reviewer also explicitly reported that it had **not** independently recomputed all seed/row/context-level CSV statistics and had not read every secondary artifact. Statements depending on unread artifacts therefore remain review findings rather than independently verified facts.

## Findings recorded for reconciliation

### C-ADT-01 — Criterion 1 establishes enrichment, not overwhelming concentration

Claude accepted the reported Mantel–Haenszel enrichment near the frozen cutoff band but emphasized that only 50.3% of membership switches occurred inside the nearest 10% band. It recommended wording such as "statistically enriched near the cutoff" rather than language implying that nearly all switches are concentrated there.

Proposed severity: minor/reporting for wording; the numerical enrichment itself was not disputed.

### C-ADT-02 — Missing matched non-poisoning perturbation control

Claude argued that a fixed top-k rule applied to two highly correlated continuous rankings will generically concentrate disagreements near the decision threshold. Because Experiment 166 does not include a matched clean-to-clean/re-seeded perturbation comparator, the current evidence does not distinguish a poisoning-specific boundary-localization signature from generic threshold sensitivity/ranking instability.

Proposed severity: major-correctable for the poisoning-specific mechanism interpretation.

Suggested discriminator: retrain a matched clean model with a changed random seed, hold the target population and intervention rule fixed, and run the same localization analysis. This suggestion is recorded only; no such analysis/experiment is authorized by this file.

### C-ADT-03 — Criterion 1 row/context dependence may overstate inferential confidence

Claude noted that the Mantel–Haenszel analysis stratifies by generation seed but treats row-level contributions inside a seed as if they were ordinary independent Bernoulli observations. Because each context contributes three related candidates and the fixed top-k budget constrains exclusion membership, within-context/within-seed dependence may narrow the reported interval and p-value.

Proposed severity: major-correctable.

Suggested existing-artifact check: a cluster/seed-respecting permutation or resampling analysis using the committed row-level table.

### C-ADT-04 — Criterion 2 is structurally coupled to the downstream endpoint

Claude derived that `net_unsafe_crossing` changes the unsafe composition of the non-excluded candidate pool, while `delta_unsafe_selected` counts the resulting change in unsafe downstream selections. With only three candidates per context and substantial exclusion coverage, a strong negative relationship is expected from pool-composition arithmetic even without any special cutoff-geometry effect.

Claude explicitly stated that this is not a strict identity: degrees of freedom remain because an excluded candidate may not have been selected, safe-candidate switches also affect the argmin, and loss/tie structure matters. Nevertheless, the magnitude/sign of the correlation may be substantially structural.

Proposed severity: major-correctable, borderline fatal **for the specific cutoff-geometry mechanism framing**, not for the weaker observation that exclusion composition predicts selection changes.

Suggested existing-artifact checks: a permutation/shuffle null preserving relevant marginals and a near-cutoff-versus-far-cutoff contrast of composition/outcome coupling.

### C-ADT-05 — Combined co-primary pass is not yet jointly diagnostic of "local cutoff geometry"

Claude's conceptual objection is that Criterion 1 tests localization while Criterion 2 tests composition/outcome coupling without conditioning on cutoff proximity. Therefore the conjunction of two individually passing criteria does not necessarily demonstrate that boundary proximity itself explains the composition/outcome relationship.

Proposed severity: major-correctable for mechanism naming/interpretation.

### C-ADT-06 — Preregistration/freeze discipline survived review

Claude found no evidence that the target seeds, 10% primary band, co-primary criteria, or bootstrap settings were changed after outcomes were inspected. It characterized the freeze as genuine and technically enforced in code.

Proposed disposition candidate after reconciliation: already addressed / strength, pending independent audit confirmation.

### C-ADT-07 — Failed/negative results appear preserved

Claude specifically noted that failed mitigation, failed divergence, failed broad weak-coupling, partial metric-superiority, and failed metric-hierarchy replication remained visible in the chronology/ledger rather than being rewritten as successes.

Proposed disposition candidate after reconciliation: already addressed / strength, pending independent audit confirmation.

### C-ADT-08 — Secondary harmful-expansion claim has small-event uncertainty risk

Claude flagged the harmful-expansion result because the ledger reports 15 harmful events among 65 total events and strong discrimination without a confidence interval on balanced accuracy. Claude did not independently recompute the underlying raw CSV in the review captured here.

Proposed severity: major-correctable if confirmed from the raw artifact; verification still required.

Suggested existing-artifact analysis: bootstrap/appropriate uncertainty interval on the already-tracked event-level data.

## Claude's strongest bounded ADT claim

Claude's final review permitted a narrow formulation: within the frozen simulator/model/attack/fixed-budget setup, clean-versus-poisoned exclusion-status changes are statistically enriched near the cutoff and the net safety composition of those changes is strongly associated with unsafe-selection changes, but current evidence does not by itself establish a poisoning-specific boundary-localized mechanism distinct from generic threshold sensitivity to correlated score perturbations.

## Publication/readiness assessment recorded

Claude judged the current "local cutoff-geometry mechanism" framing not ready for faculty-level endorsement, while considering the work suitable for workshop-level review as a bounded simulator study of decision-boundary sensitivity if caveats are explicit. This is a reviewer judgment, not an adopted project status.

## Freeze reminder

No manuscript claim, Abstract, Discussion, conclusion, claim ledger, preregistration, generated result artifact, or active experiment is changed by this record. All findings remain unadjudicated until reconciled with the independent audit lane and primary committed evidence.