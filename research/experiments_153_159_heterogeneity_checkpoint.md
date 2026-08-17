# Experiments 153-159 checkpoint: heterogeneous poisoning effects under population shift

## Why this checkpoint matters
The sequence after Experiment 150 did not support a simple monotonic narrative in which higher source-label fidelity always yields better downstream intervention utility. That simplification was explicitly falsified.

Experiment 153 showed that a constrained context-tail audit failed all preregistered mitigation criteria on the 44551-44590 target block. The clean model selected 236 unsafe actions with total regret 11.520736, whereas the 20% targeted-poisoned model selected 217 unsafe actions with regret 10.620495. The constrained defended model selected 218 unsafe actions with regret 10.642472. Thus, partial label repair did not improve either endpoint relative to the poisoned model.

Experiment 154 diagnosed this counterintuitive result. Global discrimination did not improve materially under poisoning: clean ROC AUC was 0.833773 versus 0.831417 poisoned. However, the fixed-budget top-N exclusion sets differed on a small boundary: 129 clean-only and 129 poison-only exclusions, while Jaccard overlap remained 0.924229. At the context level, the poisoned boundary produced 41 unsafe-to-safe selected-action transitions versus 22 safe-to-unsafe transitions, lowering regret on that population.

Experiment 156 prospectively replicated an apparent decision-level poisoning benefit on the untouched 44591-44630 population. Unsafe selections fell from 371 to 346 and total regret from 16.160316 to 15.206882 under the unchanged targeted poisoning construction. The effect again arose with a highly overlapping exclusion set and relatively few boundary changes.

Experiment 158 then prospectively falsified a stronger binary prediction-decision-divergence claim on 44631-44670. Prediction metrics clearly degraded (AUC 0.794692 to 0.769117; AP 0.409900 to 0.395638; excluded-unsafe recall 0.780680 to 0.757594), but decision endpoints split: unsafe selections improved slightly (358 to 354) while regret worsened (12.865555 to 13.399262). The preregistered divergence criterion therefore failed.

Experiment 159 synthesized four independent untouched populations under the exact same source model, targeted 20% poisoning construction, clean-derived intervention budget, and candidate-selection rule. The decision response pattern was heterogeneous:

- 44511-44550: poisoning harmed both unsafe selections (+69) and regret (+1.045851).
- 44551-44590: poisoning improved both unsafe selections (-19) and regret (-0.900242).
- 44591-44630: poisoning improved both unsafe selections (-24) and regret (-0.922157).
- 44631-44670: poisoning slightly improved unsafe selections (-3) but worsened regret (+0.539997).

Prediction metrics were also heterogeneous and did not provide a simple monotonic explanation for the downstream decision effects.

## Defensible interpretation
The current evidence does **not** support any claim that targeted label corruption is beneficial. Instead, it supports the narrower observation that under the frozen simulated intervention and population shifts tested here, targeted source-label corruption can change downstream decision utility in a population- and endpoint-dependent manner, and conventional global ranking metrics do not obviously provide a monotonic proxy for those changes.

This motivates Experiment 160/161, which prospectively tests prediction-decision coupling at the seed level on a new untouched population rather than inferring the relationship from four population-level points.

## Claim boundary
Nothing in this checkpoint establishes universal metric failure, useful poisoning, automatic poisoning detection, deployment robustness, biomedical validity, or clinical relevance. The evidence is simulator-internal and specific to the frozen model, corruption mechanism, intervention budget, and population-generation process.
