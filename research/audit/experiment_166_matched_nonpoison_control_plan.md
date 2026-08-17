# Experiment 166 matched non-poisoning control: prospective audit plan

Status: **FROZEN BEFORE CONTROL OUTCOME GENERATION**

Authorization date: 2026-08-17

Historical scientific anchor: reviewer snapshot `d1e3285707ed788a39c7e883c157a8a359cde7db`.

Purpose: test whether the surviving Experiment 166 near-cutoff membership-switch enrichment is specific to label poisoning or is also produced by a comparably sized, label-preserving perturbation of the fitted ranking model. This is a new audit/control analysis. It does not replace, edit, or retroactively alter Experiment 166 or its preregistration.

## Frozen inputs and machinery

The control must use the same source table, target table, features, preprocessing, model family, class weighting, exclusion-count calculation, stable top-N ranking, clean cutoff, 10% clean-cutoff proximity band, target seeds, and downstream action-selection rule used by `experiments/preregistered_cutoff_geometry_mechanism.py`.

Source table: `results/action_conditioned_support_representation_analysis_actions_071_110.csv`.

Target table: `results/prospective_action_conditioned_support_representation_actions_791_830.csv`.

Features: `action_2`, `action_3`, `context_support_distance`.

Model: `StandardScaler()` followed by `LogisticRegression(class_weight='balanced', max_iter=5000, random_state=16644830)`.

Target seeds: 44791 through 44830 inclusive.

The historical clean and poison fits are reconstructed exactly from the frozen Experiment 166 recipe solely to define the historical poison perturbation magnitude and the clean reference geometry. The poison result itself is not rerun as a new experiment.

## Non-poisoning perturbation

Generate exactly **128 candidate clean-label bootstrap models**. Candidate index `j` in 0..127 uses NumPy `default_rng(16655000 + j)`.

For each candidate, independently bootstrap the original source rows **within the original binary label strata**, sampling with replacement exactly the original number of safe rows and exactly the original number of unsafe rows. Labels are never flipped, altered, synthesized, or reassigned. The bootstrap sample is then fit with the identical scaler/logistic-regression pipeline and feature set.

This stratified bootstrap is chosen because changing only `random_state` in the frozen logistic-regression specification may not generate a meaningful perturbation. The bootstrap creates a genuine label-preserving model perturbation while retaining class counts and the original model family.

No candidate may be selected using unsafe target outcomes, realized regret, selected-action changes, near/far localization rates, or any endpoint below.

## Frozen matching rule

For each candidate and each of the 40 target seeds, compute the candidate top-N exclusion mask with the same seed-specific exclusion count `k` used by Experiment 166. Compare candidate-vs-clean exclusion geometry to historical poison-vs-clean exclusion geometry.

For each candidate compute:

1. absolute difference between its mean 40-seed exclusion Jaccard and the historical poison mean 40-seed exclusion Jaccard;
2. absolute difference between its total membership-switch count and the historical poison total membership-switch count.

Select one and only one control candidate by the following lexicographic rule, fixed in advance: minimize (1); ties at machine precision are broken by minimizing (2); any remaining tie is broken by the smallest candidate index.

Match adequacy is a gate, not a tuning loop. The selected candidate is considered adequately matched only if BOTH conditions hold:

- absolute mean-Jaccard difference <= 0.010; and
- absolute total-switch-count difference <= 10% of the historical poison total-switch count.

No additional candidates will be generated if the gate fails. A failed gate makes the specificity test **inconclusive because perturbation magnitude was not adequately matched**. The observed control endpoint must still be preserved and reported.

## Primary endpoint

Near/far status is frozen from the original clean model exactly as in Experiment 166: within each target seed, the 10% of candidate action rows nearest the clean exclusion cutoff are `near`; all others are `far`.

For perturbation P in {historical poison, matched non-poison control}, define for each generation seed:

`D_P(seed) = near membership-switch rate - far membership-switch rate`.

The primary specificity estimand is the paired seed-level difference:

`S(seed) = D_poison(seed) - D_control(seed)`.

The point estimate is the mean of `S(seed)` over the 40 frozen generation seeds.

Inference uses exactly **10,000 bootstrap resamples of whole generation seeds** with `default_rng(16656001)`. Each resample draws 40 seeds with replacement and recomputes the mean paired difference. The percentile 2.5% and 97.5% quantiles form the 95% interval. Candidate action rows are not treated as independent inferential units.

## Frozen decision rule

The match-adequacy gate is evaluated first.

If the gate passes:

- **Poisoning-specific localization supported** only if the entire 95% bootstrap interval for mean `S` is strictly greater than zero.
- **Evidence against poisoning specificity** if the entire interval is at or below zero.
- **Specificity unresolved** if the interval crosses zero.

If the match gate fails, the formal decision is **inconclusive due to inadequate perturbation matching**, regardless of the endpoint direction.

No Criterion 2 composition-direction correlation is used as primary evidence because the preceding existing-artifact audit showed that statistic is reproduced by the bookkeeping-preserving null.

## Secondary diagnostics (descriptive/audit only)

Preserve and report: selected candidate index and bootstrap seed; clean/control/poison mean Jaccards and total switches; per-seed Jaccards and switch counts; control mean near and far switch rates; control seed-level enrichment difference and its seed-bootstrap interval; poison and control fractions of all switches occurring near cutoff; downstream selected-action-change summaries; score-shift summaries; and all 128 matching diagnostics.

These secondary results cannot override the frozen primary decision rule.

## Integrity constraints

The implementation must not modify the historical experiment code, historical result artifacts, source/target artifacts, manuscript conclusions, or preregistration. New outputs must live under `results/audit/` (or a GitHub Actions audit artifact) and be explicitly labeled post-review audit/control evidence.

The control outcome must not be inspected before this plan is committed to Git history. Implementation details necessary to faithfully execute this frozen plan may be added afterward, but the candidate count, random seeds, perturbation mechanism, matching rule, adequacy gate, primary endpoint, bootstrap scheme, and decision rule above are frozen.