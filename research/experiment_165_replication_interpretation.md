# Experiment 165 — Metric-Hierarchy Replication Interpretation

## Result

Experiment 165 prospectively tested the metric hierarchy on a new untouched 40-seed population.

The preregistered hierarchy replication **failed**.

Observed associations with unsafe-selection change were:

- excluded-unsafe recall: Spearman rho = **-0.534196**
- average precision: rho = **0.134710**
- ROC AUC: rho = **0.244525**

The absolute-correlation advantage of recall over AUC was 0.289671, but its bootstrap interval was approximately **[-0.180322, 0.666006]**, crossing zero. The advantage over AP was 0.399486 with interval approximately **[-0.092801, 0.689561]**, also crossing zero.

For regret, the observed associations were weaker and differently ordered:

- recall: rho = **-0.290680**
- AP: rho = **0.369530**
- AUC: rho = **0.481448**

The preregistered `primary_metric_hierarchy_replication_pass` remained false.

## Interpretation

This result materially weakens any claim that the Experiment 163 metric ordering is stable across untouched populations.

Experiment 163 showed a strong recall > AP > AUC ordering for unsafe-selection association. Experiment 165 does not reproduce that hierarchy with bootstrap support and shows a different ordering for regret.

The stronger conclusion is therefore negative but scientifically useful:

**metric alignment can matter, but no fixed global hierarchy among excluded-unsafe recall, AP, and ROC AUC has yet demonstrated stable replication across populations.**

The current evidence is consistent with population-dependent metric usefulness rather than a universally superior intervention-aligned metric.

## Implication for the boundary-geometry hypothesis

Experiment 165 does not falsify the broader hypothesis that local decision-boundary structure may govern downstream sensitivity. It does, however, show that a single summary metric such as excluded-unsafe recall is not a stable surrogate for that structure across populations.

If the boundary-geometry hypothesis is pursued, the next mechanistic test should directly measure local cutoff properties rather than relying on one intervention-aligned metric as a proxy.

Candidate local quantities include score gaps, rank turnover, candidate density near the cutoff, safe/unsafe composition of the boundary neighborhood, and perturbation magnitude for cutoff-crossing candidates.

## Claim boundary

Do not claim that excluded-unsafe recall generally outperforms AP or ROC AUC, that Experiment 163 established a stable metric hierarchy, or that intervention-aligned metrics are universally superior.

The defensible retained claim is narrower: model-level metrics and downstream decision consequences should be evaluated separately, and metric usefulness appears to depend on the population and endpoint under the tested fixed-budget decision procedure.
