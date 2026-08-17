# Experiment 148 — preregistered twelfth-population intervention replication

## Purpose

Experiment 146 produced a large prospective simulator-internal intervention effect on one untouched population. Experiment 148 is an **independent prospective replication**, not a redesigned intervention.

This protocol is committed before twelfth-population seeds 44471–44510 are generated.

## Frozen replication

The following are unchanged from Experiment 146:

- source training population;
- hazard features (`action_2`, `action_3`, `context_support_distance`);
- 0.80 source unsafe-recall target used to define the frozen candidate-exclusion coverage;
- predicted-loss baseline policy;
- hazard-filter candidate exclusion and fallback rule;
- matched per-context random-exclusion control;
- 5,000 random trials;
- unsafe-regret threshold of 0.005;
- co-primary endpoints;
- requirement that the hazard-filter result beat the 1st percentile of matched random controls on both unsafe selected actions and total realized regret.

Only the untouched target seeds and the random-control RNG seed differ.

## Replication criterion

The Experiment 146 intervention effect is considered independently replicated only if **both original preregistered co-primary criteria pass again** on the twelfth population without policy or threshold redesign.

Failure will be retained and will prevent describing the intervention result as prospectively replicated.

## Boundaries

Even a successful replication remains simulator-internal evidence. It does not establish real-world causal efficacy, deployment safety, biomedical/clinical applicability, or cross-domain transfer.
