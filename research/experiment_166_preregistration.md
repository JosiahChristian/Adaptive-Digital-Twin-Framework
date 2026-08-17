# Experiment 166 preregistration: causal cutoff-geometry mechanism test

## Motivation
Experiments 154 and 156 identified a plausible local cutoff-reordering mechanism: targeted source-label corruption changed downstream fixed-budget decisions even when whole-distribution discrimination changed little. Experiment 158 then showed that prediction degradation can coexist with mixed decision effects, while Experiments 163 and 165 showed that no tested predictive metric has a stable universal hierarchy across shifted populations.

The next question is therefore mechanistic rather than another metric leaderboard: **are downstream decision changes concentrated in contexts whose candidate scores lie close to the frozen intervention cutoff, and does the safety/regret composition of those cutoff crossings account for the observed decision effect?**

## Frozen source model, attack, and intervention
Use the same source population, feature set (`action_2`, `action_3`, `context_support_distance`), class-balanced logistic-regression hazard model, and 20% targeted unsafe-to-safe concealment attack concentrated in the largest context-support distances used in Experiments 150–165.

Determine intervention coverage from the clean source model using the same 80% source-unsafe-recall rule. Clean and poisoned models receive the identical exclusion count within every target seed.

No mitigation, audit, model tuning, threshold tuning, or alternative attack is permitted in this experiment.

## Fresh target population
Generate a new untouched 40-seed target population using seeds **44791–44830** only after this preregistration is committed. Use the unchanged prospective action-conditioned reconstruction mechanism.

## Frozen row-level quantities
For each target seed and candidate row, record before outcome aggregation:

- clean hazard score;
- poisoned hazard score;
- poison-minus-clean score change;
- clean exclusion membership;
- poisoned exclusion membership;
- clean cutoff score (lowest clean score included in the fixed top-N exclusion set);
- absolute clean cutoff margin `abs(clean_score - clean_cutoff_score)`;
- unsafe-action label;
- realized action regret;
- generation seed, context/test index, and action identifier.

Define a **membership switch** as a candidate excluded by exactly one of the clean or poisoned models.

## Frozen context-level quantities
For each context, record whether the final selected action changes between clean and poisoned intervention pipelines. For changed contexts classify the transition as:

- unsafe-to-safe;
- safe-to-unsafe;
- safe-to-safe;
- unsafe-to-unsafe.

Also record poison-minus-clean realized regret.

## Primary mechanistic tests
The experiment has two co-primary criteria. Both must pass for the local cutoff-geometry mechanism to receive prospective support.

### Criterion 1 — cutoff localization of membership switches
Within each seed, rank all candidate rows by absolute clean cutoff margin from smallest to largest. Define the **near-cutoff band** as the closest 10% of candidate rows to the clean cutoff, with the fraction frozen here before target generation.

Pool seed-level 2×2 counts and estimate the odds ratio for membership switching in the near-cutoff band versus the remaining 90% of rows. Use a stratified Mantel–Haenszel common odds ratio across seeds and a two-sided Cochran–Mantel–Haenszel test.

Criterion 1 passes only if:

1. the common odds ratio is greater than 1;
2. its 95% confidence interval lies entirely above 1; and
3. the two-sided stratified test has `p < 0.05`.

### Criterion 2 — switched-set composition accounts for unsafe-selection direction
For each seed compute:

`net_unsafe_crossing = unsafe_poison_only_exclusions - unsafe_clean_only_exclusions`

and

`delta_unsafe_selected = poisoned_unsafe_selected - clean_unsafe_selected`.

Because excluding more unsafe candidates under poisoning should reduce downstream unsafe selections, the preregistered directional prediction is a **negative** association.

Across the 40 untouched seeds, compute Spearman correlation between `net_unsafe_crossing` and `delta_unsafe_selected`. Use 10,000 paired seed-level bootstrap resamples for the correlation.

Criterion 2 passes only if:

1. observed Spearman rho is < 0; and
2. the 95% bootstrap interval lies entirely below 0.

## Secondary analyses
Report descriptively, without rescuing either primary criterion:

- analogous switched-set regret composition versus poison-minus-clean total regret;
- fraction of all membership switches falling in the near-cutoff 10% band;
- clean/poison exclusion-set Jaccard overlap by seed;
- global ROC AUC, average precision, and excluded-unsafe recall changes;
- counts of unsafe-to-safe and safe-to-unsafe context transitions;
- sensitivity summaries for 5% and 20% cutoff bands, explicitly labeled secondary and not used for the primary conclusion.

## Primary conclusion rule
The experiment supports the local cutoff-geometry mechanism only if **both** preregistered primary criteria pass.

If cutoff localization passes but switched-set composition does not predict downstream unsafe-selection direction, conclude that score perturbations are boundary-local but that the proposed composition-to-decision mechanism is insufficient.

If composition predicts downstream direction but cutoff localization fails, conclude that switched-set composition is informative but the claimed local-cutoff mechanism is not established.

If either criterion fails, do not alter the cutoff-band definition, correlation endpoint, or inferential threshold post hoc.

## Interpretation boundary
A pass would provide prospective simulator-internal evidence that the downstream effect of this frozen targeted label-corruption procedure is mediated by candidate reordering near a fixed intervention cutoff and by the safety composition of candidates crossing that boundary. It would not establish a universal causal law, beneficial poisoning, deployment safety, robustness across model classes or attacks, or external validity to arbitrary cyber-physical, biomedical, or operational systems.
