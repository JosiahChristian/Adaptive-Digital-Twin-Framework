# Experiment 164 preregistration: intervention-aligned metric hierarchy replication

## Motivation
Experiment 163 found that seed-level changes in excluded-unsafe recall tracked downstream unsafe-selection changes much more strongly than ROC AUC and more strongly than average precision, but the bootstrap interval for recall-over-AP superiority narrowly crossed zero. Experiment 164 prospectively replicates the metric hierarchy without changing the attack, model, intervention rule, or superiority definition.

## Frozen target population
Generate a new untouched 40-seed target population using seeds **44751-44790** only after this preregistration is committed. Reconstruction must be identical to the preceding prospective action-conditioned populations.

## Frozen model and attack
Use the same source population, feature set (`action_2`, `action_3`, `context_support_distance`), class-balanced logistic-regression hazard model, 20% targeted unsafe-to-safe concealment attack concentrated in the largest context-support distances, and the same clean-source 80%-unsafe-recall rule to determine intervention coverage.

## Frozen seed-level quantities
For each target seed, compute poison-minus-clean changes in:

- ROC AUC;
- average precision;
- excluded-unsafe recall at the frozen intervention budget;
- selected unsafe actions;
- realized regret.

The primary downstream endpoint remains selected unsafe actions.

## Primary hierarchy criterion
Let `rho_recall`, `rho_ap`, and `rho_auc` be Spearman correlations between each metric change and unsafe-selection change across the 40 target seeds.

The hierarchy replication passes only if:

1. `abs(rho_recall) > abs(rho_ap) > abs(rho_auc)` in the observed population;
2. in 10,000 paired seed-level bootstrap resamples, the 95% interval for `abs(rho_recall) - abs(rho_auc)` lies entirely above zero;
3. in the same resamples, the 95% interval for `abs(rho_recall) - abs(rho_ap)` lies entirely above zero.

The regret correlations are secondary descriptive endpoints and cannot rescue the primary criterion.

## Interpretation boundary
A pass would support only that, under this frozen simulated attack/intervention setting, the intervention-aligned excluded-unsafe-recall metric is more strongly associated with downstream unsafe-selection changes than the two global ranking metrics on a second untouched population. It would not establish general metric superiority, deployment safety, or a universal evaluation rule.
