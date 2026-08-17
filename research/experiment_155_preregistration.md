# Experiment 155 preregistration: prospective replication of the poisoning boundary effect

## Purpose
Experiment 153 produced the unexpected result that the fixed-budget intervention driven by the 20% targeted label-concealment model selected fewer unsafe actions and lower regret than the clean model on one untouched target population. Experiment 154 showed that this was not caused by better global discrimination; it arose from local top-N exclusion-boundary reordering.

Experiment 155 prospectively tests whether that apparent poisoned-model advantage replicates on a fresh untouched target population.

## Frozen source models and intervention
Use the same source action table, feature set, logistic model family, source-clean labels, and 20% targeted unsafe-to-safe concealment attack as Experiments 150-154.

Use the same clean-model 80% source-unsafe-recall threshold to determine intervention coverage. Convert that clean source coverage to an exact exclusion count on the new target population. The clean and poisoned models receive the identical target exclusion count.

No audit or mitigation is used in this experiment.

## Fresh target population
Generate seeds **44591-44630** only after this preregistration is committed, using the unchanged action-conditioned prospective reconstruction pipeline.

## Frozen endpoints
Report:

1. clean and poisoned unsafe selections;
2. clean and poisoned total realized regret;
3. clean and poisoned ROC AUC and average precision;
4. top-N exclusion-set Jaccard overlap;
5. clean-only and poison-only exclusion-slice unsafe prevalence;
6. context-level transition counts, including safe-to-unsafe and unsafe-to-safe transitions.

## Primary replication classification
Classify the Experiment 153 apparent poisoning benefit as **replicated** only if, on the new target population, the poisoned model again has BOTH fewer unsafe selections and lower total regret than the clean model at identical exclusion count.

Classify it as **not replicated** if either endpoint is equal or worse for the poisoned model.

This classification is descriptive and directional; no new defense or tuning is permitted based on the outcome.

## Interpretation boundary
Replication would establish only that this specific attack can reproducibly alter a fixed intervention boundary in a direction that improves these simulator-internal endpoints under some target populations. Non-replication would support the interpretation that the Experiment 153 reversal was population-specific. Neither outcome implies that poisoning is beneficial, that corrupted labels should be retained, or that the intervention is deployment-safe.
