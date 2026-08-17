# Decision-Time Validity and Cutoff Geometry in a Fixed-Budget Adaptive Digital-Twin Pipeline

**Draft status:** canonical manuscript source on the review branch only. Claims remain constrained by the committed experimental record, hostile audits, and closed-evidence quadrangulation. This draft does not alter preregistrations, experiments, generated results, or historical evidence records.

## Abstract

Adaptive decision pipelines can exhibit strong statistical patterns that do not necessarily identify the mechanism that produced them or provide information available at decision time. We examine two such problems in a simulated adaptive digital-twin pipeline: localization of ranking changes near a fixed top-N cutoff and discrimination of harmful action-space expansion outcomes. In Experiment 166, exclusion-membership changes were strongly concentrated near the cutoff in the poisoning condition, but a prospectively frozen label-preserving non-poison perturbation matched the ranking perturbation magnitude and reproduced essentially the same localization pattern. The poison-minus-control localization difference was 0.001845 with a 95% seed-bootstrap interval of [0.0000, 0.00554], so the frozen poisoning-specificity criterion was not met. A separate compact harmful-expansion model achieved approximately 0.979 ROC AUC retrospectively, but two of its three features incorporate post-outcome quantities and therefore cannot support a pre-decision prediction claim. Models restricted to temporally legitimate loss-surface information showed weaker exploratory discrimination. Together, the results support a pipeline-specific cutoff-localization phenomenon and motivate strict separation of observed association, perturbation specificity, causal mechanism, and prediction-time validity.

## 1. Introduction

Adaptive digital-twin research increasingly couples continuously updated digital representations with prediction, decision support, and adaptive control. Recent implementations span self-adaptive manufacturing architectures, adaptive control systems, and digital-twin-supported clinical decision systems [1-3]. These examples motivate treating the digital twin not only as a state representation, but also as part of a decision pipeline whose validity depends on how predictions are converted into interventions.

That distinction is important because predictive accuracy and downstream decision quality are not interchangeable objectives. Predict-then-optimize and decision-focused learning research explicitly studies settings in which predicted quantities are subsequently used inside an optimization or discrete decision problem; this literature shows that minimizing conventional prediction error need not minimize downstream decision loss [4-6]. Recent top-K intervention work makes the same distinction in fixed-budget settings, where the decision is the selected size-K subset rather than the forecast alone [7].

Fixed-budget ranking also creates a specific sensitivity question near the selection boundary. Top-K ranking theory identifies the separation between the K-th and (K+1)-th items as a central quantity governing reliable set identification [8], while ranking-stability work studies how small changes in scoring rules can alter ranked outputs, including top-k membership [9]. These results make near-boundary sensitivity a plausible generic explanation for cutoff-localized membership changes, but they do **not** establish that this explanation caused the pattern observed in Experiment 166.

A separate validity problem arises when a predictor contains information unavailable at the intended prediction time. Methodological work on leakage in machine-learning-based science documents how outcome-linked or otherwise unavailable information can yield overoptimistic performance estimates and invalid scientific conclusions [10]. The presence of leakage in the harmful-expansion model reported here, however, is established by the model's own feature definitions and timing audit, not by the external literature.

This study therefore focuses on claim validity rather than maximizing favorable metrics. The experimental record includes preregistered positive findings, failed prospective replications, null or negative mechanism tests, matched non-poison controls, and a later timing-leakage audit. Those findings are preserved together rather than allowing later positive results to erase earlier failures.

The present manuscript addresses two questions. First, does the near-cutoff localization observed in Experiment 166 identify a poisoning-specific mechanism, or is it also produced by a non-poison perturbation of comparable ranking magnitude? Second, does the strongest harmful-expansion classifier constitute a genuine pre-decision predictor, or does its performance depend on outcome-informed features? The evidence supports narrower answers than the strongest initial interpretations.

### 1.1 Literature-to-evidence boundary

External literature in this manuscript provides methodological and disciplinary context only. It is not used to adjudicate Experiment 166 poisoning specificity, the Criterion-2 mechanism claim, downstream near-switch specificity, or harmful-expansion feature timing. Those conclusions are determined exclusively by the committed internal experimental and audit record. Accordingly, literature showing that ranking systems *can* be boundary-sensitive does not prove that ranking geometry caused Experiment 166, and literature documenting leakage elsewhere does not itself prove leakage in this study.

## 2. Methods

### 2.1 Evidence and claim-governance approach

The analyses reported here are interpreted according to the committed experimental chronology. Preregistered criteria are reported as originally evaluated, and later structural or falsification analyses are presented as subsequent adjudications rather than retroactively changing the historical result. Negative and failed findings are retained as constraints on interpretation. Where the historical chronology contains stronger pre-audit mechanism wording, the later committed reconciliation and leakage audits govern the present manuscript interpretation.

### 2.2 Experiment 166: fixed-budget ranking and cutoff localization

Experiment 166 evaluated changes in exclusion membership within a fixed top-N ranking/intervention pipeline. The original preregistered analysis tested whether membership switches were enriched in a frozen closest-10% cutoff band and whether a seed-level switch-related quantity was associated with downstream unsafe-selection change.

The experiment used the same frozen source population, feature set (`action_2`, `action_3`, `context_support_distance`), class-balanced logistic-regression hazard model, and 20% targeted unsafe-to-safe source-label concealment used in the preceding decision-aware experiments. Intervention coverage was determined from the clean source model using the frozen 80% source-unsafe-recall rule, and clean and poisoned models received the same exclusion count within each target seed. A fresh untouched target population of 40 generation seeds, 44791-44830, was generated only after preregistration.

A membership switch was defined as a candidate excluded by exactly one of the clean or poisoned models. Within each seed, candidates were ranked by absolute clean cutoff margin, and the primary near-cutoff band was the closest 10% of candidate rows to the clean cutoff. Criterion 1 pooled seed-stratified 2x2 counts and used a Mantel-Haenszel common odds ratio with a two-sided Cochran-Mantel-Haenszel test. Criterion 2 computed, per seed, `net_unsafe_crossing = unsafe_poison_only_exclusions - unsafe_clean_only_exclusions` and `delta_unsafe_selected = poisoned_unsafe_selected - clean_unsafe_selected`, then estimated their Spearman association with 10,000 paired bootstrap resamples of whole generation seeds.

The poisoning condition had mean exclusion-set Jaccard overlap 0.923823 and 308 membership switches. The original cutoff-band analysis yielded a Mantel-Haenszel common odds ratio of 10.567477 with 95% CI [8.345537, 13.380992]. The seed-level association had Spearman rho -0.873179 with bootstrap 95% CI [-0.946362, -0.735018]. Both original preregistered co-primary criteria passed.

Subsequent audits tested whether those results uniquely supported the proposed mechanism. A bookkeeping-preserving permutation null was used to test whether the Criterion-2 association could arise from the structure of the recorded quantities. A downstream-specificity analysis compared selected-action-change rates for near-only and far-only switched contexts.

A separately frozen stronger label-preserving control was then defined prospectively after an earlier weaker control failed its perturbation-magnitude gate. The stronger family preserved every source row and original label, perturbed only the continuous source-training feature `context_support_distance` with zero-mean Gaussian noise, left binary action indicators unchanged, and never perturbed target features. Sixteen predeclared dimensionless noise levels were crossed with 16 independent replicates for 256 total candidates. Candidate selection could use only mean exclusion-Jaccard mismatch and total membership-switch mismatch relative to the historical poison condition; target outcomes, regret, selected-action changes, and near/far localization were prohibited from selection.

The selected stronger control passed the prospectively frozen magnitude gate only if absolute mean-Jaccard mismatch was at most 0.010 and absolute switch-count mismatch was at most 30.8 switches. The selected control had mean exclusion-set Jaccard overlap 0.924853 and 304 membership switches, satisfying those criteria.

The poisoning-specificity comparison used the frozen per-seed estimand `D = near membership-switch rate - far membership-switch rate` and the paired contrast `S = D_poison - D_control`. Inference used exactly 10,000 bootstrap resamples of whole generation seeds; action rows were not treated as independent inferential units. Poison enrichment was 0.13623 and matched-control enrichment was 0.13438, producing a paired poison-minus-control difference of 0.001845 and a 95% seed-bootstrap CI [0.0000, 0.00554]. The frozen rule required the entire interval to be strictly above zero for poisoning-specific support.

### 2.3 Harmful-expansion discrimination and prediction-time audit

The headline compact harmful-expansion model used `predicted_loss_floor`, `loss_floor_error`, and `expanded_action_loss_error`. The latter two were defined as:

`loss_floor_error = predicted_loss_floor - true_best_loss`

`expanded_action_loss_error = predicted_action_loss - realized_expanded_action_loss`

The documented event population contained 65 events, including 15 harmful and 50 beneficial outcomes. The compact model reported approximately 0.95 balanced accuracy, 1.00 harmful-event recall, 0.75 harmful-event precision, and approximately 0.97867 ROC AUC under seed-held-out cross-validation.

A later prediction-time audit established that `true_best_loss` and `realized_expanded_action_loss` are known only after the relevant outcome/evaluation. Seed holdout therefore separates observations but does not make these residual variables available before the decision. Models restricted to temporally legitimate loss-surface information were evaluated separately and showed weaker pooled discrimination, with ROC AUC approximately 0.683-0.711 and balanced accuracy approximately 0.663-0.763 in the documented analyses. Some seed folds contained no harmful events, making fold-level AUC or balanced accuracy undefined.

### 2.4 Inferential units and reproducibility boundaries

For Experiment 166 and its later audits, the generation seed is the inferential resampling unit when bootstrap uncertainty is reported. Candidate/action rows are nested observations used to construct seed-level or seed-stratified statistics; they are not treated as independent experimental replications. The original Criterion-1 Mantel-Haenszel analysis explicitly stratifies by seed, while later bootstrap analyses resample whole seeds.

For harmful expansion, seed-held-out cross-validation controls reuse across generated populations but does not repair feature-timing violations. Prospective validity therefore requires both held-out evaluation and a feature set computable at the intended decision time.

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

This interpretation is methodologically compatible with prior top-K literature without being established by it. Chen and Suh showed that reliable top-K identification under a latent-score ranking model depends on the separation between the K-th and (K+1)-th scores [8], and Asudeh et al. developed explicit stability analyses for rankings and top-k outputs under changes to scoring weights [9]. These studies support treating boundary separation and ranking stability as relevant competing explanations. They do not establish that the Experiment 166 localization is a mathematical necessity, nor do they imply that poisoning could never add a distinct effect.

### 5.2 Association versus mechanism

The original strong Criterion-2 correlation cannot be treated as independent mechanistic evidence because a bookkeeping-preserving null reproduces it. Moreover, the downstream-specificity result runs opposite the prediction that near-only switches preferentially produce selected-action changes. A causal boundary-composition mechanism remains a possible future hypothesis, but it is not established by the present evidence.

This distinction parallels a broader decision-focused-learning principle: downstream decisions depend on the structure of the decision problem, not solely on generic predictive error [4-7]. The present study contributes a concrete caution within one fixed-budget simulator pipeline, but it does not claim a general theorem connecting ranking perturbations to downstream actions.

### 5.3 Retrospective discrimination versus prospective prediction

The harmful-expansion analysis illustrates a separate validity problem. High retrospective discrimination can coexist with invalid pre-decision interpretation when predictor construction incorporates quantities realized only after the outcome. The temporally legitimate models are therefore the relevant evidence for prospective usefulness, and their current performance should remain exploratory until evaluated under a design that preserves decision-time availability and adequate seed-level outcome variation.

Kapoor and Narayanan document multiple forms of leakage in ML-based science and show that leakage can yield substantially overoptimistic scientific claims [10]. That literature supports the methodological requirement that scientific prediction claims be evaluated using information legitimately available to the model. In this manuscript, the specific leakage finding follows directly from the identities of `loss_floor_error` and `expanded_action_loss_error`; the citation provides methodological context rather than evidence about those variables.

### 5.4 Scope and generalization

The present conclusions are limited to the studied simulation, ranking rule, intervention budget structure, models, perturbations, and seeds represented in the committed evidence. The results do not establish deployment validity, cross-domain transfer, aerospace or biomedical effectiveness, or a general law of adaptive systems. Separate adversarial-RL work may provide methodological context but is not corroborating evidence, statistical replication, or mechanistic triangulation for the ADT findings unless a future study explicitly validates such a relationship.

The adaptive-digital-twin literature demonstrates that digital twins are being used in increasingly consequential adaptive-control and decision-support settings [1-3]. That broader relevance motivates rigorous claim validation here, but evidence of successful digital-twin applications elsewhere does not establish operational validity for this framework.

## 6. Limitations

Several limitations remain. The matched-control result constrains poisoning specificity but does not prove the universal absence of poisoning-specific effects. The cutoff-localization finding may be partly or substantially induced by fixed-budget ranking geometry and requires variation of ranking rules or intervention budgets before broader generalization. The harmful-expansion event population is small and imbalanced, and some seed folds lack harmful events. The non-leaking models therefore require stronger prospective evaluation before predictive claims are warranted. Finally, the present work is simulation-based and does not establish real-world operational validity.

## 7. Conclusion

The current evidence supports two deliberately narrow conclusions. First, the tested fixed-budget adaptive digital-twin ranking pipeline exhibits robust near-cutoff localization of membership changes, but available structural and matched-control tests do not establish poisoning specificity or an independent causal boundary-composition mechanism. Second, the documented event population shows exploratory discrimination from temporally legitimate loss-surface information, while the strongest compact harmful-expansion result is retrospective because it incorporates post-outcome residuals. These findings demonstrate the importance of separating ranking geometry from perturbation specificity and retrospective discrimination from information genuinely available at decision time.

No new experiment is required solely to report these narrowed findings. Stronger claims of poisoning specificity, causal mechanism, validated prospective prediction, or broad generalization would require new discriminating evidence.

## 8. Primary evidence map

The principal manuscript claims are anchored to the following committed records:

- Original Experiment 166 preregistered numerical results: `results/preregistered_cutoff_geometry_mechanism.csv`.
- Experiment 166 chronology and preregistration ordering: `research/decision_aware_experiment_chronology.md` and `research/experiment_166_preregistration.md`; historical mechanism wording in the chronology is superseded for current interpretation by the later adjudication below.
- Experiment 166 stronger matched-control prospective protocol: `research/audit/experiment_166_stronger_label_preserving_control_plan.md`.
- Experiment 166 structural-null, downstream-specificity, and matched-control reconciliation: `research/prequadrangulation_claim_reconciliation_2026-08-17.md` and its referenced committed result artifacts.
- Harmful-expansion event count, performance, feature timing, and leakage adjudication: `research/harmful_expansion_timing_leakage_audit_2026-08-17.md` and the primary result/event/coefficient/fold artifacts listed there.
- Current publication claim boundaries: `research/publication_claim_matrix_2026-08-17.md`.
- Closed-evidence external adjudication: the preserved 2026-08-17 Genspark/Luna review record in `research/`.

## 9. References

1. Qiu H, Al-Nussairi AKJ, Chevinli ZS, et al. Integrating digital twins with neural networks for adaptive control of automotive suspension systems. *Scientific Reports*. 2025;15:11078. doi:10.1038/s41598-025-91243-1.
2. Niemeyer C, et al. Self-adaptive digital twin reference architecture to improve process quality. *Procedia CIRP*. 2023;119:867-872. doi:10.1016/j.procir.2023.03.131.
3. Builes-Montaño CE, Lema-Perez L, Ramírez-Rincón A, et al. A digital twin-enhanced decision support system improves time-in-range in type 1 diabetes: a randomized clinical trial. *Scientific Reports*. 2025;15:39738. doi:10.1038/s41598-025-23165-x.
4. Elmachtoub AN, Grigas P. Smart "Predict, then Optimize". *Management Science*. 2022;68(1):9-26. doi:10.1287/mnsc.2020.3922.
5. Elmachtoub AN, Liang JCN, McNellis R. Decision Trees for Decision-Making under the Predict-then-Optimize Framework. *Proceedings of the 37th International Conference on Machine Learning*. PMLR 119:2858-2867, 2020.
6. Mandi J, Bucarey V, Tchomba MMK, Guns T. Decision-Focused Learning: Through the Lens of Learning to Rank. *Proceedings of the 39th International Conference on Machine Learning*. PMLR 162:14935-14947, 2022.
7. Heuton K, Muench F, Shrestha S, Stopka TJ, Hughes MC. Decision-aware Training of Spatiotemporal Forecasting Models to Select a Top-K Subset of Sites for Intervention. *Proceedings of the 42nd International Conference on Machine Learning*. PMLR 267:23136-23154, 2025.
8. Chen Y, Suh C. Spectral MLE: Top-K Rank Aggregation from Pairwise Comparisons. *Proceedings of the 32nd International Conference on Machine Learning*. PMLR 37:371-380, 2015.
9. Asudeh A, Jagadish HV, Miklau G, Stoyanovich J. On Obtaining Stable Rankings. *Proceedings of the VLDB Endowment*. 2018;12(3):237-250.
10. Kapoor S, Narayanan A. Leakage and the reproducibility crisis in machine-learning-based science. *Patterns*. 2023;4(9):100804. doi:10.1016/j.patter.2023.100804.

## Evidence-governance note

This manuscript draft is subordinate to the committed experimental artifacts, preregistrations, result records, later hostile audits, publication claim matrix, and closed-evidence external adjudication. Where a historical document contains stronger wording, the later adjudication governs current manuscript interpretation without deleting the historical record. External literature supplies context only and cannot supersede the internal experimental adjudications.
