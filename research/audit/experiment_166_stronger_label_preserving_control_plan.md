# Experiment 166 stronger label-preserving control: prospective audit plan

Status: **FROZEN BEFORE STRONGER-CONTROL OUTCOME GENERATION**

Authorization date: 2026-08-17

Historical scientific anchor: reviewer snapshot `d1e3285707ed788a39c7e883c157a8a359cde7db`.

Predecessor control: `research/audit/experiment_166_matched_nonpoison_control_plan.md`. Its prospectively frozen 128-model stratified-bootstrap family failed the perturbation-magnitude gate (best control mean exclusion Jaccard 0.9888190680 and 42 switches versus poison 0.9238228512 and 308 switches). That failure is preserved and is the stated reason for prospectively defining a stronger family. No predecessor endpoint is reinterpreted.

Purpose: determine whether Experiment 166 near-cutoff switch localization exceeds that produced by a **magnitude-matched, label-preserving training-covariate perturbation**. This is a new post-review audit/control analysis and does not alter Experiment 166, its preregistration, historical artifacts, or manuscript claims.

## Frozen historical machinery

Use the same source/target tables, feature construction, scaler/logistic-regression model, class weighting, target seeds 44791--44830, source-derived exclusion coverage, stable top-N exclusion rule, clean cutoff, 10% clean-cutoff proximity band, and downstream action-selection rule as Experiment 166 and the predecessor audit.

Historical poison geometry is reconstructed exactly from the frozen Experiment 166 recipe only as a comparator. Required historical checks before control analysis: total poison-vs-clean membership switches = 308 and mean 40-seed exclusion Jaccard = 0.9238228511679869.

## Stronger label-preserving perturbation family

The new family perturbs **training covariates only**. No label is flipped, reassigned, synthesized, removed, or selected using target outcomes. Every candidate retains all source rows and their original labels.

For each candidate, independently perturb the continuous training feature `context_support_distance` by additive zero-mean Gaussian noise. Let `s` be the population standard deviation (`ddof=0`) of the clean source `context_support_distance`. Candidate noise is `Normal(0, (sigma*s)^2)` and is applied to every source row before fitting the otherwise identical model. Binary action-indicator features are unchanged. Target features are never perturbed.

Freeze the following 16 dimensionless sigma levels exactly:

`[0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.55, 0.70, 0.90, 1.10, 1.40, 1.80, 2.30, 3.00, 4.00, 5.50]`

For each sigma, generate exactly 16 independent candidates, for **256 total candidates**. Candidate index `j` in 0..255 maps to `sigma = SIGMAS[j // 16]`, replicate `j % 16`, and NumPy `default_rng(16657000 + j)`.

This grid is intentionally broad because the predecessor bootstrap family was prospectively demonstrated to be too weak. The entire strength grid and candidate count are frozen now; there is no adaptive expansion after outcomes are observed.

No candidate may be selected using unsafe target outcomes, realized regret, selected-action changes, near/far localization, or the primary endpoint.

## Frozen magnitude-matching rule

For each candidate compute, across the same 40 target seeds:

1. absolute difference from historical poison in mean exclusion Jaccard;
2. absolute difference from historical poison in total membership-switch count.

Select exactly one candidate lexicographically: minimize (1), then (2), then candidate index.

The selected control passes the magnitude gate only if BOTH:

- absolute mean-Jaccard difference <= 0.010; and
- absolute switch-count difference <= 10% of 308 (30.8 switches).

No additional sigma levels, replicates, seeds, or perturbation families may be added after observing this run. Failure again yields `inconclusive_inadequate_perturbation_match` and must be preserved.

## Primary endpoint and inference

Near/far membership is frozen from the original clean model exactly as in Experiment 166. For perturbation P in {historical poison, selected stronger control}, define per seed:

`D_P(seed) = near membership-switch rate - far membership-switch rate`.

Primary paired estimand:

`S(seed) = D_poison(seed) - D_control(seed)`.

Report the 40-seed mean. Inference uses exactly 10,000 bootstrap resamples of whole generation seeds with `default_rng(16658001)`. The 2.5th and 97.5th percentiles are the 95% interval. Action rows are not independent inferential units.

## Frozen decision rule

Evaluate magnitude adequacy first.

If the gate passes:

- `poisoning_specific_localization_supported` only if the entire 95% interval for mean S is strictly > 0;
- `evidence_against_poisoning_specificity` if the entire interval is <= 0;
- otherwise `specificity_unresolved`.

If the gate fails, decision = `inconclusive_inadequate_perturbation_match` regardless of endpoint direction.

The prior Criterion 2 composition-direction correlation remains excluded from primary evidence because the existing-artifact audit reproduced it under a bookkeeping-preserving null.

## Secondary diagnostics

Preserve all 256 matching diagnostics, selected sigma/replicate/seed, per-seed Jaccards and switch counts, near/far rates, score-shift summaries, selected-action changes, unsafe-selection changes, regret changes, and a seed-bootstrap interval for the selected control's D using 10,000 resamples with `default_rng(16658002)`. These cannot override the primary rule.

## Integrity constraints

Do not modify historical experiment code, preregistrations, source/target artifacts, historical results, active experimental workflows, Abstract, Discussion, or conclusions. New outputs live only under `results/audit/experiment_166_stronger_label_preserving_control/` or an isolated GitHub Actions artifact.

This protocol must be committed before the implementation is executed. Implementation may faithfully encode this plan afterward, but sigma levels, candidate count, seeds, matching rule, adequacy gate, endpoint, bootstrap, and decision rule are frozen.