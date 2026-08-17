# Decision-Aware Evaluation of Targeted Label Corruption Under Population Shift

## Abstract
Predictive model degradation does not necessarily determine the sign or magnitude of downstream decision effects when a model is embedded inside a fixed-budget intervention policy. This study investigates targeted source-label corruption in a simulator-based adaptive digital-twin setting using a sequence of diagnostic, preregistered, and prospectively replicated experiments. Across shifted target populations, the same frozen corruption and intervention procedure produced harmful, favorable, and mixed downstream outcomes, ruling out simple universal narratives of either poisoning harm or benefit. A constrained label-repair intervention also failed to monotonically improve downstream utility. In one fresh 40-seed population, an intervention-aligned excluded-unsafe recall metric was more strongly associated with unsafe-selection changes than ROC AUC and numerically more strongly associated than average precision. However, a subsequent exact prospective replication failed to confirm a stable recall > AP > AUC hierarchy. The resulting evidence supports a narrower methodological conclusion: model-level discrimination metrics are insufficient by themselves to characterize fixed-budget decision consequences under adversarial perturbation and population shift, and decision-layer evaluation is necessary. A local cutoff-reordering mechanism is consistent with the accumulated evidence but remains unproven.

## 1. Introduction
Machine-learning components in adaptive or decision-support systems are often evaluated through global predictive metrics such as ROC AUC and average precision. These quantities are useful summaries of discrimination across a distribution, but they do not directly encode the consequences of a downstream policy that acts on only a limited subset of ranked candidates. Under fixed-budget intervention, small score perturbations near the action boundary may change which candidates are selected even when whole-distribution discrimination changes very little.

This distinction becomes especially important under adversarial training-data corruption and population shift. A targeted label-poisoning mechanism can perturb model scores, while a subsequent fixed-budget policy converts those scores into discrete intervention choices. The resulting decision effect can therefore depend not only on global predictive degradation but also on local ordering, population composition, and which candidates cross the intervention cutoff.

The present study examines this problem through a sequence of simulator-internal experiments. The research design intentionally preserves failed preregistrations and mixed outcomes. Rather than asking only whether poisoning reduces predictive accuracy, the study asks whether the same corruption procedure produces consistent downstream effects, whether restoring corrupted labels necessarily improves decisions, whether global metrics predict decision-layer consequences, and whether an intervention-aligned metric provides a more stable account of those consequences.

The contribution is methodological rather than a claim of attack benefit, universal robustness, or deployment safety. The central result is that downstream consequences are heterogeneous across shifted populations and that no tested global or intervention-aligned metric has yet established a universal hierarchy for predicting those consequences.

## 2. Research Questions
The decision-aware experimental sequence addresses four bounded questions.

**RQ1.** Does targeted source-label corruption produce a consistent direction of downstream fixed-budget decision harm across shifted populations?

**RQ2.** Does partial recovery of corrupted source labels necessarily improve downstream utility?

**RQ3.** Do global predictive metrics such as ROC AUC and average precision consistently characterize changes in downstream unsafe selections and realized regret?

**RQ4.** Does an intervention-aligned predictive quantity, excluded-unsafe recall, prospectively and reproducibly outperform global discrimination metrics in tracking downstream effects?

## 3. Methods

### 3.1 Experimental setting
The experiments are conducted within the Adaptive-Digital-Twin-Framework simulator. A context-informed hazard model assigns candidate hazard scores, and a frozen fixed-budget intervention rule excludes a fixed number of high-ranked candidates. The decision layer is evaluated through at least two endpoints: the number of unsafe actions that remain selected and total realized regret.

The adversarial condition uses targeted corruption of source training labels. Across the decision-aware sequence, the model family, attack construction, intervention rule, and preregistered endpoints are held fixed within each prospective comparison. New target populations or seed blocks are generated before evaluating the frozen comparison where prospective replication is required.

### 3.2 Predictive metrics
The principal global predictive metrics are ROC AUC and average precision. Later experiments additionally evaluate excluded-unsafe recall, an intervention-aligned quantity tied more directly to the fixed-budget exclusion decision.

### 3.3 Decision endpoints
Two primary downstream quantities are used throughout the sequence: unsafe selections remaining after intervention and realized regret. Because these endpoints can move in different directions, neither is treated as a substitute for the other.

### 3.4 Inferential discipline
The experiment chronology distinguishes diagnostics, retrospective synthesis, and prospective tests. Post-hoc observations are not relabeled as preregistered findings. Failed criteria remain failed even when secondary quantities appear favorable. Subsequent experiments test narrowed hypotheses on fresh populations rather than revising earlier thresholds after outcome inspection.

## 4. Results

### 4.1 Partial label repair did not monotonically improve downstream utility
Experiment 153 tested a constrained audit designed to recover a subset of corrupted labels. Although some poisoned labels were repaired, the audited model did not improve either downstream endpoint relative to the poisoned model. Unsafe selections were 218 under the audit and 217 under the poisoned condition, while regret was 10.642 and 10.620, respectively. The preregistered mitigation claim therefore failed.

This result falsified the simple assumption that increasing source-label fidelity necessarily produces monotonic improvement in fixed-budget decision utility.

### 4.2 A boundary-local diagnostic explained an unexpected intervention reversal without implying a globally better poisoned model
Experiment 154 examined why the poisoned model could outperform the clean model downstream on the Experiment 153 population. Global ROC AUC changed only slightly, from 0.833773 in the clean model to 0.831417 in the poisoned model. Yet 41 contexts changed from unsafe to safe decisions and 22 changed from safe to unsafe.

This pattern suggested that a relatively small score perturbation could alter candidate ordering near the fixed intervention cutoff. The analysis was diagnostic, not causal proof, and therefore generated the local boundary-reordering hypothesis rather than confirming it.

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

## 5. Discussion
The strongest surviving conclusion is not that one predictive metric is universally superior. Instead, the experiments show that metric usefulness varies by population and downstream endpoint. A quantity closely aligned with the intervention decision can be highly informative on one population and substantially less dominant on another.

The results also clarify the role of global discrimination metrics. ROC AUC and average precision remain valid measures of model discrimination, but they cannot be assumed to determine the sign or magnitude of fixed-budget downstream consequences. In the present experiments, substantial downstream changes sometimes occurred with very small global metric changes, while clear prediction degradation sometimes coexisted with mixed decision effects.

A local cutoff-reordering mechanism provides a plausible explanation. Under a fixed exclusion budget, only score perturbations that alter membership or ordering near the intervention boundary can change the selected set. The impact of those changes then depends on the safety composition and regret contribution of the switched candidates. Whole-distribution metrics may underweight this local geometry. However, the current evidence is consistent with this mechanism rather than causally establishing it.

The failed preregistrations are substantively important. The constrained repair test rejected a monotonic repair-to-utility story. The prediction-decision divergence test rejected an overly simple binary decoupling formulation. The metric-superiority and hierarchy-replication tests rejected promotion of one favorable population result into a universal leaderboard. Together, these failures narrow the claim to a more defensible methodological result.

## 6. Limitations
All findings are simulator-internal. The study does not establish deployment safety, external validity, clinical or biomedical validity, transfer to arbitrary cyber-physical systems, invariance across model classes, invariance across attack mechanisms, or invariance across intervention budgets. The current local cutoff mechanism is not yet causally established. The observed heterogeneity also implies that additional generalization claims require prospective testing rather than extrapolation from the current populations.

## 7. Conclusion
Targeted label corruption in a fixed-budget decision pipeline can produce heterogeneous downstream effects under population shift, including harmful, favorable, and mixed outcomes. Partial restoration of corrupted labels does not necessarily improve downstream utility, and global discrimination metrics do not consistently determine the resulting decision consequences. An intervention-aligned recall quantity showed strong population-specific value but failed to establish a stable prospective hierarchy over AP and ROC AUC.

The evidence therefore supports decision-layer evaluation as a necessary complement to global predictive evaluation in the tested adversarial setting. The next scientifically justified step is a preregistered mechanistic test of local cutoff geometry rather than another attempt to reproduce a universal metric hierarchy.

## Artifact map
- `research/decision_aware_experiment_chronology.md`
- `research/decision_aware_evidence_synthesis.md`
- `research/decision_aware_master_results.csv`
- `research/manuscript_tables.md`
- `docs/reproducibility_decision_aware.md`
- `results/prospective_poisoning_boundary_replication.csv`
- `results/preregistered_prediction_decision_divergence.csv`
- `results/preregistered_intervention_aligned_metric_superiority.csv`
- `results/preregistered_intervention_aligned_metric_hierarchy_replication.csv`
