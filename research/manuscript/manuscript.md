# Decision-Time Validity and Cutoff Geometry in a Fixed-Budget Adaptive Digital-Twin Pipeline

**Draft status:** canonical manuscript source on the review branch only. Claims remain constrained by the committed experimental record, hostile audits, and closed-evidence quadrangulation. This draft does not alter preregistrations, experiments, generated results, or historical evidence records.

## Abstract

Adaptive decision pipelines can exhibit strong statistical patterns that do not necessarily identify the mechanism that produced them or provide information available at decision time. We examine two such problems in a simulated adaptive digital-twin pipeline: localization of ranking changes near a fixed top-N cutoff and discrimination of harmful action-space expansion outcomes. In Experiment 166, exclusion-membership changes were strongly concentrated near the cutoff in the poisoning condition, but a prospectively frozen label-preserving non-poison perturbation matched the ranking perturbation magnitude and reproduced essentially the same localization pattern. The poison-minus-control localization difference was 0.001845 with a 95% seed-bootstrap interval of [0.0000, 0.00554], so the frozen poisoning-specificity criterion was not met. A separate compact harmful-expansion model achieved approximately 0.979 ROC AUC retrospectively, but two of its three features incorporate post-outcome quantities and therefore cannot support a pre-decision prediction claim. Models restricted to temporally legitimate loss-surface information showed weaker exploratory discrimination. Together, the results support a pipeline-specific cutoff-localization phenomenon and motivate strict separation of observed association, perturbation specificity, causal mechanism, and prediction-time validity.

## 1. Introduction

Adaptive digital twins combine state estimation, prediction, ranking, and intervention under changing system conditions. Such pipelines create a methodological challenge: a result can be numerically strong while its scientific interpretation remains limited by the construction of the decision rule or by the time at which predictor information becomes available. Fixed-budget ranking can concentrate membership changes near a selection boundary, while retrospective residual features can make an outcome appear highly predictable even when the required information would not exist at the intended decision time.

This study therefore focuses on claim validity rather than maximizing favorable metrics. The experimental record includes preregistered positive findings, failed prospective replications, null or negative mechanism tests, matched non-poison controls, and a later timing-leakage audit. Those findings are preserved together rather than allowing later positive results to erase earlier failures.

The present manuscript addresses two questions. First, does the near-cutoff localization observed in Experiment 166 identify a poisoning-specific mechanism, or is it also produced by a non-poison perturbation of comparable ranking magnitude? Second, does the strongest harmful-expansion classifier constitute a genuine pre-decision predictor, or does its performance depend on outcome-informed features? The evidence supports narrower answers than the strongest initial interpretations.

## 2. Methods

### 2.1 Evidence and claim-governance approach

The analyses reported here are interpreted according to the committed experimental chronology. Preregistered criteria are reported as originally evaluated, and later structural or falsification analyses are presented as subsequent adjudications rather than retroactively changing the historical result. Negative and failed findings are retained as constraints on interpretation. Where the historical chronology contains stronger pre-audit mechanism wording, the later committed reconciliation and leakage audits govern the present manuscript interpretation.

### 2.2 Experiment 166: fixed-budget ranking and cutoff localization

Experiment 166 used the frozen source population, feature set (`action_2`, `action_3`, and `context_support_distance`), class-balanced logistic-regression hazard model, and 20% targeted unsafe-to-safe source-label concealment procedure documented in its preregistration. Intervention coverage was derived from the clean source model using the frozen 80% source-unsafe-recall rule, and clean and perturbed models received the same exclusion count within each target seed. The untouched prospective target population comprised 40 generation seeds, 44791 through 44830.

For every target candidate, the preregistered record included clean and poisoned hazard scores, clean and poisoned exclusion membership, the clean cutoff score, absolute clean-cutoff margin, unsafe-action label, realized action regret, generation seed, context/test index, and action identifier. A membership switch was defined as a candidate excluded by exactly one of the clean and poisoned models. The primary near-cutoff band was frozen before target generation as the 10% of candidate rows within each seed having the smallest absolute clean-cutoff margins.

The original Criterion-1 analysis formed seed-stratified 2x2 counts for membership switching in the near 10% band versus the remaining 90% and estimated a Mantel-Haenszel common odds ratio with a two-sided Cochran-Mantel-Haenszel test. Criterion 1 required an odds ratio above 1, a 95% interval entirely above 1, and p < 0.05. Criterion 2 computed, for each of the 40 seeds, `net_unsafe_crossing = unsafe_poison_only_exclusions - unsafe_clean_only_exclusions` and `delta_unsafe_selected = poisoned_unsafe_selected - clean_unsafe_selected`; the frozen directional prediction was a negative Spearman association. Its interval used 10,000 paired seed-level bootstrap resamples.

The poisoning condition had mean exclusion-set Jaccard overlap 0.923823 and 308 membership switches. The original cutoff-band analysis yielded a Mantel-Haenszel common odds ratio of 10.567477 with 95% CI [8.345537, 13.380992]. The seed-level association had Spearman rho -0.873179 with bootstrap 95% CI [-0.946362, -0.735018]. Both original preregistered co-primary criteria passed.

Subsequent audits tested whether those results uniquely supported the proposed mechanism. A bookkeeping-preserving permutation null tested whether the Criterion-2 association could arise from the structure of the recorded quantities. A downstream-specificity analysis compared selected-action-change rates for near-only and far-only switched contexts.

A later, separately frozen label-preserving control perturbed only the continuous source-training covariate `context_support_distance` with zero-mean Gaussian noise while retaining all source rows and original labels; target features were never perturbed. Before outcome generation, the audit froze 16 noise levels with 16 independently seeded candidates at each level (256 candidates total), together with a lexicographic matching rule based first on absolute mean-Jaccard difference from the historical poisoning condition and then on total switch-count difference. Candidate selection was prohibited from using target unsafe outcomes, realized regret, selected-action changes, near/far localization, or the primary endpoint. The selected control had mean exclusion-set Jaccard overlap 0.924853 and 304 membership switches, satisfying the frozen adequacy requirements of Jaccard mismatch <= 0.010 and switch-count mismatch <= 30.8.

For poisoning specificity, near/far membership remained frozen from the original clean model. Within each seed, `D` was defined as near membership-switch rate minus far membership-switch rate, and the paired estimand was `S = D_poison - D_control`. Inference used 10,000 bootstrap resamples of whole generation seeds; action rows were not treated as independent inferential units. Poison enrichment was 0.13623 and matched-control enrichment was 0.13438, producing a mean paired difference of 0.001845 and a 95% seed-bootstrap CI [0.0000, 0.00554]. The frozen rule required the entire interval to be strictly above zero for poisoning-specific support; otherwise an interval overlapping zero yielded `specificity_unresolved` after a successful magnitude match.

### 2.3 Harmful-expansion discrimination and prediction-time audit

The headline compact harmful-expansion model used `predicted_loss_floor`, `loss_floor_error`, and `expanded_action_loss_error`. The latter two were defined as:

`loss_floor_error = predicted_loss_floor - true_best_loss`

`expanded_action_loss_error = predicted_action_loss - realized_expanded_action_loss`

The documented event population contained 65 events, including 15 harmful and 50 beneficial outcomes. The compact model reported approximately 0.95 balanced accuracy, 1.00 harmful-event recall, 0.75 harmful-event precision, and approximately 0.97867 ROC AUC under seed-held-out cross-validation.

A later prediction-time audit established that `true_best_loss` and `realized_expanded_action_loss` are known only after the relevant outcome/evaluation. Seed holdout therefore separates observations but does not make these residual variables available before the decision. Models restricted to temporally legitimate loss-surface information were evaluated separately and showed weaker pooled discrimination, with ROC AUC approximately 0.683-0.711 and balanced accuracy approximately 0.663-0.763 in the documented analyses. Some seed folds contained no harmful events, making fold-level AUC or balanced accuracy undefined.

### 2.4 Inferential units and reproducibility boundaries

Generation seed is the inferential unit for the Experiment 166 paired specificity analysis and for its seed-level correlation/bootstrap procedures. Candidate/action rows contribute to within-seed counts and rates but are not treated as independent units for the paired seed bootstrap. The stronger non-poison control reuses the same 40 target seeds and frozen clean cutoff geometry so the poison-control comparison is paired by seed.

For the harmful-expansion analysis, seed-held-out evaluation controls observation reuse across generation seeds but does not repair feature-timing leakage. The current event population is small and imbalanced, and folds without harmful events make some fold-level discrimination metrics undefined. Accordingly, the manuscript reports pooled non-leaking performance only as exploratory and does not convert the number of event rows into a claim of independent prospective replications.

Reproduction of the historical Experiment 166 analysis is governed by its committed preregistration and result artifact. Reproduction of the stronger matched control is governed by the separately committed prospective audit plan, including its fixed noise grid, deterministic candidate seeds, matching rule, adequacy gate, endpoint, and bootstrap seeds. The manuscript does not substitute prose for those machine- and protocol-level records; the evidence map below identifies the controlling files.

## 3. Results

### 3.1 Near-cutoff localization exists in the tested pipeline

The original Experiment 166 poisoning analysis showed strong enrichment of exclusion-membership switches near the frozen cutoff band. This supports the presence of a localization phenomenon under the tested poisoning condition.

The later matched-control comparison materially changes the specificity interpretation. The non-poison perturbation closely matched the poisoning condition in exclusion-set overlap and total membership switching, and it reproduced nearly the same near-minus-far enrichment. Under the prospectively frozen specificity rule, the lower bootstrap confidence bound did not exceed zero. Accordingly, poisoning specificity was **not established**. This result should not be interpreted as proof that poisoning-specific effects are universally absent; it means the present experiment does not distinguish the observed localization from a sufficiently matched non-poison ranking perturbation.

### 3.2 The original Criterion-2 association is not independent mechanistic evidence

The observed Criterion-2 correlation was reproduced by a bookkeeping-preserving permutation null. The observed rho of approximately -0.87318 had a one-sided null probability of 0.53315. Thus, although the historical preregistered association remains part of the experimental record, it cannot be used as independent evidence that boundary composition mechanistically drives downstream unsafe-selection change.

The downstream-specificity analysis further opposed the proposed preferential-near-switch interpretation. Selected-action-change rate was 0.63871 for near-only switched contexts and 0.95425 for far-only switched contexts, a near-minus-far difference of -0.31554 with seed-bootstrap 95% CI [-0.40818, -0.23161]. These results do not support the claim that near-cutoff switches preferentially drive downstream selected-action changes.

### 3.3 The strongest harmful-expansion model is retrospective, not pre-decision

The compact model's approximately 0.979 ROC AUC shows high outcome-informed retrospective discrimination in the documented event set. It does not demonstrate genuine pre-decision prediction because two residual features require post-outcome information. Cross-validation across seeds does not resolve this temporal mismatch.

Temporally legitimate loss-surface-only models showed weaker exploratory discrimination. These results are consistent with possible pre-decision signal in the documented event population, but the current analyses do not establish prospective or population-generalizable predictive performance.

## 4. Negative and Failed Results

The evidence record includes findings that constrain the favorable results above. Experiment 165 failed to prospectively replicate an earlier apparent recall > AP > AUC hierarchy. Experiment 158 showed degradation in global prediction metrics but did not satisfy its preregistered prediction-decision divergence criteria. Simple support-distance representations performed poorly as standalone unsafe-behavior detectors, and strong pooled discrimination failed conditioned transfer in at least one action/block setting. Experiment 166's Criterion-2 mechanistic interpretation did not survive the bookkeeping-preserving null, preferential downstream near-switch specificity was falsified in the documented analysis, poisoning specificity was unresolved under the matched non-poison control, and the headline harmful-expansion pre-decision interpretation contains confirmed timing leakage.

These results are not treated as ancillary failures to be removed from the narrative. They define the boundary between what the present evidence demonstrates and what remains unresolved.

## 5. Discussion

### 5.1 Phenomenon versus poisoning specificity

Experiment 166 provides evidence for a near-cutoff concentration of membership changes in the tested fixed-budget top-N ranking pipeline. The matched non-poison control indicates that this phenomenon can be reproduced without poisoning when ranking perturbation magnitude is closely matched. The strongest defensible interpretation is therefore pipeline-specific cutoff localization, not a poisoning-specific signature.

### 5.2 Association versus mechanism

The original strong Criterion-2 correlation cannot be treated as independent mechanistic evidence because a bookkeeping-preserving null reproduces it. Moreover, the downstream-specificity result runs opposite the prediction that near-only switches preferentially produce selected-action changes. A causal boundary-composition mechanism remains a possible future hypothesis, but it is not established by the present evidence.

### 5.3 Retrospective discrimination versus prospective prediction

The harmful-expansion analysis illustrates a separate validity problem. High retrospective discrimination can coexist with invalid pre-decision interpretation when predictor construction incorporates quantities realized only after the outcome. The temporally legitimate models are therefore the relevant evidence for prospective usefulness, and their current performance should remain exploratory until evaluated under a design that preserves decision-time availability and adequate seed-level outcome variation.

### 5.4 Scope and generalization

The present conclusions are limited to the studied simulation, ranking rule, intervention budget structure, models, perturbations, and seeds represented in the committed evidence. The results do not establish deployment validity, cross-domain transfer, aerospace or biomedical effectiveness, or a general law of adaptive systems. Separate adversarial-RL work may provide methodological context but is not corroborating evidence, statistical replication, or mechanistic triangulation for the ADT findings unless a future study explicitly validates such a relationship.

## 6. Limitations

Several limitations remain. The matched-control result constrains poisoning specificity but does not prove the universal absence of poisoning-specific effects. The cutoff-localization finding may be partly or substantially induced by fixed-budget ranking geometry and requires variation of ranking rules or intervention budgets before broader generalization. The harmful-expansion event population is small and imbalanced, and some seed folds lack harmful events. The non-leaking models therefore require stronger prospective evaluation before predictive claims are warranted. Finally, the present work is simulation-based and does not establish real-world operational validity.

## 7. Conclusion

The current evidence supports two deliberately narrow conclusions. First, the tested fixed-budget adaptive digital-twin ranking pipeline exhibits robust near-cutoff localization of membership changes, but available structural and matched-control tests do not establish poisoning specificity or an independent causal boundary-composition mechanism. Second, the documented event population shows exploratory discrimination from temporally legitimate loss-surface information, while the strongest compact harmful-expansion result is retrospective because it incorporates post-outcome residuals. These findings demonstrate the importance of separating ranking geometry from perturbation specificity and retrospective discrimination from information genuinely available at decision time.

No new experiment is required solely to report these narrowed findings. Stronger claims of poisoning specificity, causal mechanism, validated prospective prediction, or broad generalization would require new discriminating evidence.

## 8. Primary evidence map

The principal manuscript claims are anchored to the following committed records:

- Original Experiment 166 preregistration and numerical results: `research/experiment_166_preregistration.md` and `results/preregistered_cutoff_geometry_mechanism.csv`.
- Experiment 166 chronology: `research/decision_aware_experiment_chronology.md`; historical mechanism wording there is superseded for current interpretation by the later adjudications below.
- Existing-artifact structural and unit-of-analysis audit: `research/audit/experiment_166_existing_artifact_adjudication_result.md`.
- Stronger label-preserving control protocol: `research/audit/experiment_166_stronger_label_preserving_control_plan.md`; its prospective status, fixed candidate family, matching rule, inferential unit, and decision rule govern interpretation of the later matched-control result.
- Experiment 166 structural-null, downstream-specificity, and matched-control reconciliation: `research/prequadrangulation_claim_reconciliation_2026-08-17.md` and the committed audit/result evidence referenced there.
- Harmful-expansion event count, performance, feature timing, and leakage adjudication: `research/harmful_expansion_timing_leakage_audit_2026-08-17.md` and the primary result/event/coefficient/fold artifacts listed there.
- Current publication claim boundaries: `research/publication_claim_matrix_2026-08-17.md`.
- Closed-evidence external adjudication: the preserved 2026-08-17 Genspark/Luna review record in `research/`.

## Evidence-governance note

This manuscript draft is subordinate to the committed experimental artifacts, preregistrations, result records, later hostile audits, publication claim matrix, and closed-evidence external adjudication. Where a historical document contains stronger wording, the later adjudication governs current manuscript interpretation without deleting the historical record.
