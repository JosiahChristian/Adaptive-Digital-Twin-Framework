# Decision-Aware Experiment Chronology

## Scope
This chronology records the inferential sequence of the decision-aware adversarial-label-corruption line. It distinguishes prospective tests from diagnostics and retrospective synthesis so manuscript ordering cannot imply that hypotheses were specified earlier than they were.

## Experiment 153 — constrained audit mitigation
A preregistered limited audit attempted to repair targeted corrupted source labels. It failed the primary mitigation criteria: recovering some poisoned rows did not improve either downstream endpoint relative to the poisoned intervention. This falsified a simple label-fidelity-to-decision-utility story.

## Experiment 154 — boundary diagnostic
Because the poisoned model unexpectedly outperformed the clean model on the Experiment 153 population, a mechanism diagnostic examined ranking and intervention changes. Global AUC did not improve, while a relatively small change in exclusion-set membership yielded more unsafe-to-safe than safe-to-unsafe decision transitions. This generated, but did not prove, the local cutoff/boundary hypothesis.

## Experiments 155–156 — prospective replication of the unexpected decision sign
A fresh untouched population was generated before applying the frozen comparison. The poisoned intervention again produced fewer unsafe selections and lower regret than the clean intervention. This established that the favorable sign was not unique to one target population, while remaining incompatible with any general claim that poisoning is beneficial.

## Experiments 157–158 — preregistered prediction-decision divergence
A new untouched population tested a strict divergence definition. Prediction metrics degraded, unsafe selections improved slightly, and regret worsened. The preregistered binary divergence criterion failed. The result redirected the research toward endpoint-specific non-monotonicity rather than a universal prediction-versus-decision decoupling claim.

## Experiment 159 — retrospective cross-population synthesis
The same frozen corruption/intervention procedure was summarized across four independent untouched populations. Downstream signs were heterogeneous: harmful, favorable, favorable, and mixed. This synthesis motivated a seed-level prospective test rather than another population-level directional claim.

## Experiments 160–161 — preregistered seed-level coupling
A fresh 40-seed population tested whether conventional predictive changes were broadly weakly coupled to downstream changes. The broad weak-coupling criterion failed because an intervention-aligned quantity retained meaningful association with unsafe-selection changes. This narrowed the hypothesis to comparative metric usefulness.

## Experiments 162–163 — preregistered intervention-aligned metric superiority
On another fresh 40-seed population, excluded-unsafe recall had a very strong association with unsafe-selection change and substantially exceeded ROC AUC. However, superiority over average precision was not bootstrap-confirmed, so the full preregistered criterion failed. This was retained as partial, population-specific evidence.

## Experiments 164–165 — exact prospective hierarchy replication
The observed recall > AP > AUC ordering was frozen and tested on another untouched 40-seed population without changing thresholds or adding rescue endpoints. The hierarchy failed to replicate with bootstrap support, and regret showed a different ordering. This falsified promotion of the Experiment 163 ordering into a stable metric hierarchy.

## Experiment 166 — preregistered local cutoff-geometry mechanism test
The local cutoff hypothesis originally generated diagnostically in Experiment 154 was finally subjected to a direct prospective mechanism test on an untouched 40-seed population. The primary near-cutoff band was frozen at 10% before adjudication. Changed exclusion membership was strongly localized near the fixed intervention boundary: the Mantel–Haenszel common odds ratio was 10.567477 with 95% CI [8.345537, 13.380992], satisfying the first co-primary criterion. The seed-level net unsafe-crossing quantity was strongly negatively associated with downstream unsafe-selection change (Spearman rho = −0.873179; 10,000-bootstrap 95% CI [−0.946362, −0.735018]), satisfying the second co-primary criterion. Both criteria passed, so the preregistered cutoff-geometry mechanism-support indicator was true.

Across the population there were 308 exclusion-membership switches; 50.3247% occurred within the frozen closest-10% band around the cutoff, despite mean clean/poisoned exclusion-set Jaccard overlap of 0.923823. These descriptive quantities make clear how a relatively small local reordering can coexist with high global decision-set overlap.

The Experiment 166 result prospectively supports the proposed operating-boundary mechanism inside this frozen simulator pipeline. It does not establish mechanism invariance across arbitrary populations, attack mechanisms, model classes, intervention budgets, or deployed systems.

## Current inferential position
The experiment sequence supports heterogeneous downstream consequences of targeted source-label corruption under population shift and demonstrates that model-level discrimination metrics cannot be assumed to determine fixed-budget decision outcomes. Experiment 166 additionally provides prospective simulator-internal evidence for a local cutoff-geometry mechanism: perturbations matter when they change intervention membership near the action boundary, and the downstream sign depends strongly on the safety composition of those crossings. The evidence still does not establish a universally superior predictive metric or a universal causal law.

## Next admissible experimental gate
The original local-cutoff mechanism question has now passed its first direct prospective test. Further experiments should therefore target **generalization or falsification of that mechanism**, not re-test the same population until significance is obtained. Appropriate next gates include a preregistered intervention-budget perturbation test, a fresh population-family replication, or a model-class replication that freezes the Experiment 166 mechanism criteria before outcomes are observed. Repetition of failed metric-hierarchy tests solely to seek significance remains excluded.