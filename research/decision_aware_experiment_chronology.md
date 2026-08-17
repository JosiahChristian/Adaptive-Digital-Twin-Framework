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

## Current inferential position
The experiment sequence supports heterogeneous downstream consequences of targeted source-label corruption under population shift and demonstrates that model-level discrimination metrics cannot be assumed to determine fixed-budget decision outcomes. It does not establish a universally superior metric or a proven causal boundary mechanism.

## Next admissible experimental gate
Further prospective experimentation should occur only for a materially new mechanistic or generalization question. The strongest mechanistic candidate is direct local cutoff geometry, specified before outcomes and compared against global metrics and simple baselines. Repetition of failed metric-hierarchy tests solely to seek significance is excluded.
