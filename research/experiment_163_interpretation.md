# Experiment 163 — Intervention-Aligned Metric Interpretation

## What the preregistered test found

Experiment 163 evaluated 40 fresh generation seeds under the frozen clean-versus-poisoned decision pipeline.

Change in excluded-unsafe recall was strongly associated with both downstream endpoints:

- unsafe-selection change: Spearman rho = **-0.907622**
- regret change: Spearman rho = **-0.804072**

The corresponding global-metric associations were weaker:

- AUC vs. unsafe-selection change: **-0.498384**
- AUC vs. regret change: **-0.355226**
- AP vs. unsafe-selection change: **-0.771977**
- AP vs. regret change: **-0.457497**

The recall metric's absolute-correlation advantage over AUC for unsafe selections was 0.409238, with bootstrap interval approximately [0.134358, 0.706060]. Its advantage over AP was only 0.135645, with interval approximately [-0.012068, 0.309136]. The preregistered full-superiority criterion therefore failed.

## Interpretation

The result supports a **metric-alignment** interpretation rather than a universal metric-superiority claim.

A metric defined close to the intervention itself can track downstream consequences substantially better than a global discrimination metric. That is unsurprising mechanistically: a fixed-budget intervention depends primarily on candidate ordering around the exclusion/selection boundary, whereas ROC AUC averages ranking behavior across the full score distribution.

Average precision is more competitive in this experiment. Because the preregistered recall-versus-AP superiority interval crosses zero, the evidence does not establish that excluded-unsafe recall is uniquely or universally optimal.

## Emerging mechanistic hypothesis

The accumulated Experiments 154–163 suggest a narrower hypothesis worth future prospective testing:

**The downstream sensitivity of a fixed-budget adaptive decision is governed more directly by local score/rank structure near the intervention boundary than by global discrimination quality.**

This hypothesis is not established by Experiment 163. The current experiment compares metrics; it does not directly measure or manipulate boundary geometry.

A genuine mechanistic test would need prospectively defined local quantities such as score gaps around the cutoff, rank turnover, density near the boundary, unsafe/safe composition in the boundary neighborhood, and perturbation magnitude. Those quantities should predict downstream instability on fresh populations without being selected after inspecting the outcome.

## Why this matters for ADT

If the hypothesis survives falsification, it could connect several otherwise heterogeneous findings:

1. small perturbations can change fixed-budget outcomes despite little change in global ranking metrics;
2. the direction of the effect varies across populations;
3. global AUC changes frequently disagree in sign with downstream changes;
4. a decision-aligned metric tracks downstream behavior more strongly than AUC in fresh seeded evaluation.

The scientific contribution would then concern **decision-aware evaluation of adaptive models**, not poisoning as beneficial or harmful in itself.

## Boundaries

This experiment does not establish causal sufficiency of excluded-unsafe recall, universal superiority over AP, deployment safety, a universal prediction-decision law, or transfer beyond the tested simulator and fixed-budget decision procedure.
