# Experiment 160 preregistration: seed-level prediction-decision coupling under targeted label corruption

## Motivation
Experiments 150-159 show that the same fixed 20% targeted unsafe-to-safe source-label corruption can harm, improve, or split downstream intervention endpoints across independent shifted populations, while global ranking metrics move inconsistently. Experiment 160 tests a narrower prospective question: within one new untouched population, do seed-level changes in conventional prediction quality track seed-level changes in downstream decision utility?

## Frozen source model and attack
Use the same source action table, feature set (`action_2`, `action_3`, `context_support_distance`), balanced logistic regression, source-unsafe-recall coverage rule, and 20% targeted high-context-distance unsafe-to-safe label-concealment attack used in Experiments 150-159. No model tuning is permitted.

## Prospective target
Generate one new untouched 40-seed population using seeds **44671-44710**, with the identical population-generation mechanism used in prior prospective blocks. The target population is generated only after this preregistration is committed.

## Per-seed quantities
For every generation seed, evaluate clean and poisoned models using one global target exclusion count derived from the clean source-model coverage rule. Record:

- ROC AUC change: poisoned minus clean;
- average-precision change: poisoned minus clean;
- excluded-unsafe-recall change: poisoned minus clean;
- unsafe-selection change: poisoned minus clean (lower is better);
- total-regret change: poisoned minus clean (lower is better).

## Primary coupling tests
For seeds with defined prediction metrics, compute Spearman rank correlations by ranking each variable and taking Pearson correlation of ranks:

1. delta AUC versus delta regret;
2. delta AUC versus delta unsafe selections;
3. delta average precision versus delta regret;
4. delta excluded-unsafe recall versus delta unsafe selections.

If prediction improvements reliably imply decision improvements, these correlations should be negative because decision deltas are coded as poisoned-minus-clean costs.

## Frozen weak-coupling criterion
The prospective result supports *weak prediction-decision coupling* only if all are true:

1. no absolute primary correlation exceeds 0.50;
2. at least two of the four correlations have absolute value below 0.30;
3. at least 25% of evaluable seeds show AUC/regret directional discordance, defined as `sign(delta_auc) == sign(delta_regret)` when neither delta is zero;
4. at least 25% of evaluable seeds show AUC/unsafe-selection directional discordance by the same sign rule.

The sign rule reflects that prediction improvement is positive while decision improvement is negative, so equal signs are discordant.

## Secondary uncertainty analysis
Bootstrap the 40 seeds 10,000 times and report 95% percentile intervals for each Spearman correlation and for both discordance fractions. These intervals are descriptive and do not replace the frozen primary criteria.

## Interpretation boundary
A pass supports only the claim that, in this simulated shifted population under this fixed targeted label-corruption attack and intervention rule, conventional seed-level ranking changes are weak proxies for seed-level downstream intervention changes. It does not establish universal metric failure, deployment safety, clinical validity, or beneficial poisoning.
