# Experiment 152 preregistration: constrained context-tail audit

## Purpose
Experiment 151 showed exact recovery when a 20% audit budget covered all 328 source rows attacked by the 20% targeted unsafe-label concealment construction. Because that result is structurally favorable, Experiment 152 deliberately prevents complete attack coverage.

## Frozen attack and defense
Use the same source population and model family as Experiments 150-151. Construct the same 20% targeted unsafe-to-safe source-label concealment attack: conceal the 328 unsafe source rows with the largest context-support distances.

The defense may audit only **164 source rows**, exactly 50% of the poison-row count and about 2.08% of all source rows. The context-tail defense audits the 164 source rows with the largest context-support distances overall and restores their original labels.

Matched controls: 1,000 random audits, each verifying exactly 164 source rows sampled uniformly without replacement from the source population and restoring poisoned labels only where sampled.

## Prospective target
Evaluate on a new untouched 40-seed target population, seeds **44551-44590**, generated only after this preregistration is committed. The population-generation mechanism must be identical to the preceding prospective action-conditioned populations.

Freeze target intervention coverage using the clean source model and the same 80% source-unsafe-recall threshold rule used in Experiments 146-151. All clean, poisoned, defended, and random-audit models receive the identical target exclusion count.

## Co-primary criteria
The constrained context-tail audit passes only if:

1. unsafe selections are lower than the undefended poisoned model;
2. total realized regret is lower than the undefended poisoned model;
3. unsafe selections are <= the 5th percentile of 1,000 matched random audits;
4. total regret is <= the 5th percentile of matched random audits.

Recovery to clean performance is reported descriptively, not required. Exact recovery is not expected because the audit budget is intentionally smaller than the attack.

## Interpretation boundary
A pass would show only that, for this frozen simulation and attack, a severely constrained context-informed verification budget mitigates the attack more effectively than equal-budget random verification on an untouched target population. It would not establish automatic poison detection, general adversarial robustness, deployment safety, or clinical validity.
