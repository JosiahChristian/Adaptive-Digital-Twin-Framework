# Experiment 162 preregistration: intervention-aligned metric superiority

## Motivation
Experiment 161 rejected the broad weak-coupling hypothesis. However, the strongest seed-level association was between change in excluded-unsafe recall and change in unsafe selections (Spearman rho about -0.55), whereas global ROC AUC and average precision were only moderately associated with downstream endpoints and showed frequent sign discordance.

## Prospective question
Under the same frozen 20% targeted unsafe-to-safe label-concealment attack and fixed intervention rule, does an intervention-aligned prediction metric (excluded-unsafe recall at the intervention budget) track downstream unsafe selections more strongly than global ranking metrics (ROC AUC and average precision)?

## Fresh target
Generate a new untouched 40-seed population using seeds 44711-44750. The population-generation mechanism is unchanged.

## Frozen analysis
For each seed separately, compare clean vs poisoned models and compute poison-minus-clean deltas for ROC AUC, average precision, excluded-unsafe recall, unsafe selections, and total regret. Use Spearman correlations across seeds.

Primary correlation magnitudes:
- |rho(delta excluded-unsafe recall, delta unsafe selections)|
- |rho(delta ROC AUC, delta unsafe selections)|
- |rho(delta AP, delta unsafe selections)|

Run 10,000 paired seed-level bootstrap resamples. For each resample compute the difference in absolute correlation between excluded-unsafe recall and each global metric.

## Primary criteria
The intervention-aligned metric superiority claim passes only if both are true:
1. observed |rho(recall, unsafe)| exceeds both |rho(AUC, unsafe)| and |rho(AP, unsafe)|;
2. the 95% bootstrap interval for each paired absolute-correlation difference (recall minus AUC; recall minus AP) lies entirely above zero.

Secondary descriptive analysis reports analogous correlations with regret and directional discordance.

## Interpretation boundary
A pass supports only that, in this frozen simulation and attack/intervention construction, a metric evaluated at the operational exclusion budget tracks unsafe-selection changes better than two global ranking metrics. It does not establish a universal metric hierarchy, deployment safety, or general robustness.
