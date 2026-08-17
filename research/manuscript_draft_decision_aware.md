# Decision-Aware Evaluation of Targeted Label Corruption Under Population Shift

## Abstract
Predictive model degradation does not necessarily determine the sign or magnitude of downstream decision effects when a model is embedded inside a fixed-budget intervention policy. This study investigates targeted source-label corruption in a simulator-based adaptive digital-twin setting using a sequence of diagnostic, preregistered, and prospectively replicated experiments. Across shifted target populations, the same frozen corruption and intervention procedure produced harmful, favorable, and mixed downstream outcomes, ruling out simple universal narratives of either poisoning harm or benefit. A constrained label-repair intervention also failed to monotonically improve downstream utility. In one fresh 40-seed population, an intervention-aligned excluded-unsafe recall metric was more strongly associated with unsafe-selection changes than ROC AUC and numerically more strongly associated than average precision, but a subsequent exact prospective replication failed to confirm a stable recall > AP > AUC hierarchy. A final preregistered 40-seed mechanism test then showed that intervention-set membership switches were strongly concentrated near the frozen score cutoff (Mantel–Haenszel common odds ratio 10.57, 95% CI 8.35–13.38) and that the safety composition of boundary crossings strongly tracked downstream unsafe-selection changes (Spearman rho −0.873, 95% bootstrap interval −0.946 to −0.735). The resulting evidence supports a bounded methodological conclusion: model-level discrimination metrics are insufficient by themselves to characterize fixed-budget decision consequences under adversarial perturbation and population shift, while local cutoff geometry and the composition of candidates crossing that cutoff provide prospective explanatory value in the tested pipeline.

## 1. Introduction
Machine-learning components in adaptive or decision-support systems are often evaluated through global predictive metrics such as ROC AUC and average precision. These quantities are useful summaries of discrimination across a distribution, but they do not directly encode the consequences of a downstream policy that acts on only a limited subset of ranked candidates. Under fixed-budget intervention, small score perturbations near the action boundary may change which candidates are selected even when whole-distribution discrimination changes very little.

This distinction becomes especially important under adversarial training-data corruption and population shift. A targeted label-poisoning mechanism can perturb model scores, while a subsequent fixed-budget policy converts those scores into discrete intervention choices. The resulting decision effect can therefore depend not only on global predictive degradation but also on local ordering, population composition, and which candidates cross the intervention cutoff.

The present study examines this problem through a sequence of simulator-internal experiments. The research design intentionally preserves failed preregistrations and mixed outcomes. Rather than asking only whether poisoning reduces predictive accuracy, the study asks whether the same corruption procedure produces consistent downstream effects, whether restoring corrupted labels necessarily improves decisions, whether global metrics predict decision-layer consequences, whether an intervention-aligned metric provides a more stable account of those consequences, and whether the final decision effects are prospectively explained by local cutoff geometry.

The contribution is methodological rather than a claim of attack benefit, universal robustness, or deployment safety. The central result is that downstream consequences are heterogeneous across shifted populations and that no tested predictive metric establishes a universal hierarchy, while a preregistered mechanism test supports the role of local cutoff crossings in the tested fixed-budget pipeline.

## 2. Research Questions
The decision-aware experimental sequence addresses five bounded questions.

**RQ1.** Does targeted source-label corruption produce a consistent direction of downstream fixed-budget decision harm across shifted populations?

**RQ2.** Does partial recovery of corrupted source labels necessarily improve downstream utility?

**RQ3.** Do global predictive metrics such as ROC AUC and average precision consistently characterize changes in downstream unsafe selections and realized regret?

**RQ4.** Does an intervention-aligned predictive quantity, excluded-unsafe recall, prospectively and reproducibly outperform global discrimination metrics in tracking downstream effects?

**RQ5.** Are membership changes caused by targeted corruption concentrated near the fixed intervention cutoff, and does the safety composition of those crossings prospectively account for downstream unsafe-selection changes?

## 3. Methods

### 3.1 Experimental setting
The experiments are conducted within the Adaptive-Digital-Twin-Framework simulator. A context-informed hazard model assigns candidate hazard scores, and a frozen fixed-budget intervention rule excludes a fixed number of high-ranked candidates. The decision layer is evaluated through at least two endpoints: the number of unsafe actions that remain selected and total realized regret.

The adversarial condition uses targeted corruption of source training labels. Across the decision-aware sequence, the model family, attack construction, intervention rule, and preregistered endpoints are held fixed within each prospective comparison. New target populations or seed blocks are generated before evaluating the frozen comparison where prospective replication is required.

### 3.2 Predictive metrics
The principal global predictive metrics are ROC AUC and average precision. Later experiments additionally evaluate excluded-unsafe recall, an intervention-aligned quantity tied more directly to the fixed-budget exclusion decision.

### 3.3 Decision endpoints
Two primary downstream quantities are used throughout the sequence: unsafe selections remaining after intervention and realized regret. Because these endpoints can move in different directions, neither is treated as a substitute for the other.

### 3.4 Cutoff-geometry mechanism test
Experiment 166 preregistered a direct mechanism test on a fresh 40-seed population. For each target seed, clean and poisoned models used the identical exclusion count. Candidate rows were ranked by absolute distance from the clean-model intervention cutoff, and the primary near-cutoff band was frozen as the closest 10% of rows. A stratified Mantel–Haenszel analysis tested whether exclusion-membership switches were enriched in that near-cutoff band. Separately, for each seed, the net number of unsafe candidates newly excluded by the poisoned model relative to the clean model was compared with the corresponding change in downstream unsafe selections using Spearman correlation and 10,000 paired seed-level bootstrap resamples. Both co-primary criteria were required to pass.

### 3.5 Inferential discipline
The experiment chronology distinguishes diagnostics, retrospective synthesis, and prospective tests. Post-hoc observations are not relabeled as preregistered findings. Failed criteria remain failed even when secondary quantities appear favorable. Subsequent experiments test narrowed hypotheses on fresh populations rather than revising earlier thresholds after outcome inspection.

## 4. Results

### 4.1 Partial label repair did not monotonically improve downstream utility
Experiment 153 tested a constrained audit designed to recover a subset of corrupted labels. Although some poisoned labels were repaired, the audited model did not improve either downstream endpoint relative to the poisoned model. Unsafe selections were 218 under the audit and 217 under the poisoned condition, while regret was 10.642 and 10.620, respectively. The preregistered mitigation claim therefore failed.

This result falsified the simple assumption that increasing source-label fidelity necessarily produces monotonic improvement in fixed-budget decision utility.

### 4.2 A boundary-local diagnostic generated the cutoff-reordering hypothesis
Experiment 154 examined why the poisoned model could outperform the clean model downstream on the Experiment 153 population. Global ROC AUC changed only slightly, from 0.833773 in the clean model to 0.831417 in the poisoned model. Yet 41 contexts changed from unsafe to safe decisions and 22 changed from safe to unsafe.

This pattern suggested that a relatively small score perturbation could alter candidate ordering near the fixed intervention cutoff. At that point the analysis was diagnostic rather than causal proof and therefore generated the local boundary-reordering hypothesis.

### 4.3 The favorable downstream sign replicated prospectively on a fresh population
Experiment 156 prospectively tested the frozen comparison on a new untouched population. Unsafe selections decreased from 371 under the clean model to 346 under the poisoned model, and regret decreased from 16.160316 to 15.206882. At the same time, ROC AUC changed only from 0.763685 to 0.765520 and average precision from 0.441181 to 0.443655. The exclusion-set Jaccard overlap was 0.912342.

Among changed contexts, 37 transitions were unsafe-to-safe and 12 were safe-to-unsafe. The favorable downstream sign therefore replicated, but the result does not imply that poisoning is beneficial in general or that the poisoned hazard model is globally superior.

### 4.4 Prediction degradation and decision outcomes were endpoint-dependent
Experiment 158 preregistered a strong prediction-decision divergence criterion. Poisoning degraded ROC AUC from 0.794692 to 0.769117, average precision from 0.409900 to 0.395638, and excluded-unsafe recall from 0.780680 to 0.757594. Unsafe selections nevertheless improved slightly from 358 to 354, while regret worsened from 12.865555 to 13.399262.

Because the downstream endpoints themselves moved in different directions, the preregistered divergence and strong-divergence indicators were both false. The result therefore supports separate prediction-layer and decision-layer evaluation, but not a universal binary decoupling law.

### 4.5 Cross-population synthesis established heterogeneous downstream effects
Experiment 159 summarized four untouched target populations evaluated with the same frozen corruption and intervention procedure. Downstream effects included harmful, favorable, favorable, and mixed responses. This heterogeneity is the central replicated population-level phenomenon.

The synthesis rules out two simple interpretations. The evidence does not support the claim that targeted corruption always worsens downstream utility, and it also does not support the claim that corruption is beneficial. Instead, downstream effects depend on population and endpoint under the tested procedure.

### 4.6 Intervention-aligned recall showed strong population-specific association but no stable hierarchy
Experiment 163 evaluated 40 fresh generation seeds. The Spearman association between excluded-unsafe recall change and unsafe-selection change was −0.907622, compared with −0.771977 for average precision and −0.498384 for ROC AUC. For regret change, the corresponding associations were −0.804072, −0.457497, and −0.355226.

The absolute-correlation advantage of recall over ROC AUC for unsafe-selection change was 0.409238, with a 95% bootstrap interval of [0.134358, 0.706060], supporting superiority over AUC on this population. The recall-over-AP advantage was 0.135645, with interval [−0.012068, 0.309136], so the preregistered full superiority criterion failed.

Experiment 165 then prospectively replicated the observed recall > AP > AUC ordering on another untouched 40-seed population. The unsafe-selection associations were −0.534196 for recall, +0.134710 for AP, and +0.244525 for AUC. Bootstrap superiority intervals for recall over both AUC and AP crossed zero. For regret, the observed associations were −0.290680 for recall, +0.369530 for AP, and +0.481448 for AUC. The prospective hierarchy replication therefore failed.

### 4.7 Local cutoff geometry received prospective mechanism support
Experiment 166 directly tested the mechanism generated by Experiment 154 on a new untouched 40-seed population. Membership switches were strongly enriched in the preregistered closest-10% cutoff band. The Mantel–Haenszel common odds ratio was 10.567, with a 95% confidence interval of [8.346, 13.381], and the two-sided stratified test was significant, satisfying the first co-primary criterion.

The second co-primary criterion also passed. Across seeds, the net number of unsafe candidates newly excluded by the poisoned model was strongly negatively associated with the change in downstream unsafe selections: Spearman rho = −0.873179, with a 95% paired-bootstrap interval of [−0.946362, −0.735018]. Thus, seeds in which poisoning moved more unsafe candidates into the exclusion set tended to show larger reductions in unsafe downstream selections.

Both preregistered co-primary criteria therefore passed. Of 308 total exclusion-membership switches, 50.3% occurred within the closest 10% of rows to the clean cutoff, and mean clean/poison exclusion-set Jaccard overlap remained 0.9238. Mean changes in global prediction metrics were negative (AUC −0.0402, AP −0.0631, excluded-unsafe recall −0.0442), showing that the mechanism result is not equivalent to a claim of globally improved prediction.

## 5. Discussion
The strongest surviving conclusion is not that one predictive metric is universally superior and not that targeted corruption is beneficial. Instead, the experiments show that metric usefulness and downstream effects vary by population and endpoint, while the final preregistered mechanism test provides prospective evidence for how a fixed-budget decision rule converts score perturbations into action changes.

The Experiment 166 result sharpens the earlier diagnostic interpretation. Membership changes were not distributed uniformly across the score range; they were concentrated near the frozen intervention cutoff. Moreover, the safety composition of those switched candidates strongly tracked the direction of downstream unsafe-selection changes. This supports a mechanistic account in which local rank perturbations around an operating boundary, rather than whole-distribution discrimination alone, determine which candidates are removed from consideration and thereby alter downstream action selection.

The results also clarify the role of global discrimination metrics. ROC AUC and average precision remain valid measures of model discrimination, but they cannot be assumed to determine the sign or magnitude of fixed-budget downstream consequences. Experiment 166 itself showed negative average changes in global prediction metrics while establishing a strong relationship between boundary-crossing composition and unsafe-selection changes. Operational evaluation therefore requires explicit analysis at the intervention layer.

The failed preregistrations remain substantively important. The constrained repair test rejected a monotonic repair-to-utility story. The prediction-decision divergence test rejected an overly simple binary decoupling formulation. The metric-superiority and hierarchy-replication tests rejected promotion of one favorable population result into a universal leaderboard. Experiment 166 does not erase these failures; it explains why a simpler global-metric story was inadequate for the tested pipeline.

## 6. Limitations
All findings are simulator-internal. The study does not establish deployment safety, external validity, clinical or biomedical validity, transfer to arbitrary cyber-physical systems, invariance across model classes, invariance across attack mechanisms, or invariance across intervention budgets. Experiment 166 provides prospective support for the local cutoff-geometry mechanism under the frozen model, attack, population generator, and fixed-budget policy; it does not establish a universal causal law outside those conditions. Additional mechanistic generalization would require preregistered tests across materially different model classes, attacks, or intervention budgets.

## 7. Conclusion
Targeted label corruption in a fixed-budget decision pipeline can produce heterogeneous downstream effects under population shift, including harmful, favorable, and mixed outcomes. Partial restoration of corrupted labels does not necessarily improve downstream utility, and global discrimination metrics do not consistently determine the resulting decision consequences. An intervention-aligned recall quantity showed strong population-specific value but failed to establish a stable prospective hierarchy over AP and ROC AUC.

A final preregistered mechanism test provides the strongest explanatory result in the sequence: exclusion-membership changes were concentrated near the intervention cutoff, and the safety composition of those boundary crossings strongly predicted downstream unsafe-selection changes. The evidence therefore supports decision-layer and local-boundary evaluation as necessary complements to global predictive evaluation in the tested adversarial setting.

## Artifact map
- `research/decision_aware_experiment_chronology.md`
- `research/decision_aware_evidence_synthesis.md`
- `research/decision_aware_master_results.csv`
- `research/manuscript_tables.md`
- `docs/reproducibility_decision_aware.md`
- `research/experiment_166_preregistration.md`
- `research/experiment_166_analysis_plan.md`
- `results/prospective_poisoning_boundary_replication.csv`
- `results/preregistered_prediction_decision_divergence.csv`
- `results/preregistered_intervention_aligned_metric_superiority.csv`
- `results/preregistered_intervention_aligned_metric_hierarchy_replication.csv`
- `results/preregistered_cutoff_geometry_mechanism.csv`
- `results/preregistered_cutoff_geometry_mechanism_by_seed.csv`
- `results/preregistered_cutoff_geometry_mechanism_rows.csv`
- `results/preregistered_cutoff_geometry_context_changes.csv`
