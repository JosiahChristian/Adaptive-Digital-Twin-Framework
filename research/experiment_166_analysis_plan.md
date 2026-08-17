# Experiment 166 analysis plan — local cutoff geometry

This document translates the committed Experiment 166 preregistration into an implementation checklist. The preregistration is authoritative if any wording differs.

## Required inputs
- frozen source action table used by Experiments 162–165;
- fresh prospective target action table for seeds 44791–44830;
- unchanged feature construction and class-balanced logistic-regression model;
- frozen 20% targeted unsafe-to-safe source-label concealment attack;
- clean-source 80%-unsafe-recall coverage rule.

## Required outputs

### Row-level artifact
`results/preregistered_cutoff_geometry_mechanism_rows.csv`

Required columns:
`generation_seed,test_index,action,unsafe_action,realized_action_regret,clean_score,poison_score,delta_score,clean_excluded,poison_excluded,membership_switch,clean_cutoff_score,abs_clean_cutoff_margin,near_cutoff_primary`

### Seed-level artifact
`results/preregistered_cutoff_geometry_mechanism_by_seed.csv`

Required columns include:
`generation_seed,target_rows,target_contexts,exclusion_count,clean_cutoff_score,membership_switches,near_cutoff_rows,near_cutoff_switches,far_cutoff_switches,clean_only_exclusions,poison_only_exclusions,unsafe_clean_only_exclusions,unsafe_poison_only_exclusions,net_unsafe_crossing,clean_unsafe_selected,poison_unsafe_selected,delta_unsafe_selected,clean_total_regret,poison_total_regret,delta_regret,exclusion_jaccard,unsafe_to_safe,safe_to_unsafe,safe_to_safe,unsafe_to_unsafe`

### Summary artifact
`results/preregistered_cutoff_geometry_mechanism.csv`

Required fields include:
- seed count;
- Mantel–Haenszel common odds ratio;
- lower/upper 95% confidence limits;
- two-sided CMH p-value;
- Spearman rho for net unsafe crossing vs delta unsafe selected;
- 2.5th/97.5th percentile bootstrap limits from 10,000 paired seed resamples;
- individual criterion flags;
- overall primary mechanism-support flag.

### Context-transition artifact
`results/preregistered_cutoff_geometry_context_changes.csv`

Retain one row per context whose selected action changes, including old/new action safety and realized-regret difference.

## Deterministic implementation requirements
1. Stable sorting must be used for all top-N membership decisions.
2. The exact same exclusion count must be used for clean and poisoned models within each seed.
3. Near-cutoff membership is determined only from the clean score and clean cutoff.
4. The primary near-cutoff fraction is fixed at 10%; 5% and 20% are secondary only.
5. Bootstrap RNG seed must be fixed in source before evaluation.
6. No result-dependent seed filtering is permitted.
7. Seeds with degenerate 2×2 tables remain in the stratified analysis; implementation must use a method that handles zero cells without silently dropping strata.
8. Raw row-level and seed-level artifacts must be retained so every summary statistic can be independently reconstructed.

## Statistical implementation note
Prefer a standard stratified-table implementation for the Mantel–Haenszel odds ratio and Cochran–Mantel–Haenszel test. If the chosen library cannot handle a frozen stratum without modification, document the exact numerical convention in console output before interpreting the result; do not change the preregistered estimand.

## Integrity checks before evaluation
- assert target seeds are exactly 44791–44830;
- assert each context contains the expected candidate-action count;
- assert source poison count matches the frozen construction;
- assert clean and poisoned exclusion counts are identical per seed;
- assert row-level membership-switch counts equal clean-only plus poison-only counts;
- assert context transition counts reconcile with changed selections;
- assert no target-outcome-derived quantity is used to define the cutoff band.

## Reporting discipline
The final result note must state pass/fail for each co-primary criterion before discussing secondary metrics. A failure cannot be rescued by the 5% or 20% sensitivity bands, regret correlations, global predictive metrics, or a favorable single-seed example.
