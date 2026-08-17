# Experiment 148 — preregistered twelfth-population intervention replication

## Purpose

Experiment 146 produced a large prospective simulator-internal intervention effect on one untouched population. Experiment 148 is an **independent prospective replication**, not a redesigned intervention.

The protocol was committed before twelfth-population seeds 44471–44510 were generated.

## Frozen replication

The following were unchanged from Experiment 146:

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

Only the untouched target seeds and random-control RNG seed differed.

## Results

The untouched twelfth population contained 3,100 decision contexts and 9,300 candidate-action rows. At the unchanged 39.018% candidate exclusion coverage, 3,629 candidate actions were excluded.

| Endpoint | Predicted-loss baseline | Hazard-filter replication | Matched random exclusions |
|---|---:|---:|---:|
| Unsafe selected actions | 801 | **403** | mean 727.42; 1st pct 690 |
| Unsafe selected-action rate | 25.84% | **13.00%** | — |
| Total realized regret | 51.8658 | **10.5579** | mean 41.3738; 1st pct 38.8799 |
| Mean realized regret/context | 0.01673 | **0.00341** | — |
| Selected actions changed vs baseline | — | 1,800 / 3,100 (58.06%) | — |

The unchanged hazard filter reduced unsafe selections by **398** relative to baseline and total realized regret by **41.3079**. None of 5,000 matched random-control trials achieved an unsafe-selection count or total regret as low as the frozen hazard-filter policy.

Both original preregistered co-primary criteria passed again. Experiment 146's simulator-internal intervention effect is therefore **prospectively replicated on an independent untouched population without policy redesign**.

## Boundaries

The replication materially strengthens the simulator-specific intervention claim, but it still does not establish real-world causal efficacy, deployment safety, biomedical/clinical applicability, or cross-domain transfer.

## Artifacts

- `results/preregistered_twelfth_population_intervention_replication.csv`
- `results/preregistered_twelfth_population_intervention_replication_random_trials.csv`
- `results/preregistered_twelfth_population_intervention_replication_by_seed.csv`
- `results/experiment_148_console_output.txt`
