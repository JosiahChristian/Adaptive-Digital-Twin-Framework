# Prospective context-hazard evidence checkpoint

## Current defensible claim

Within the current simulated adaptive-digital-twin candidate-action environment, a source-trained action-plus-context hazard score using action identity and `context_support_distance` contains prospective decision-relevant information about unsafe candidate actions. Under a fixed unlabeled alert/exclusion budget, the signal generalizes to untouched seed populations, adds value beyond action identity, depends on correct row-level context correspondence, and can improve a frozen simulated action-selection policy. The intervention effect has independently replicated once without policy redesign.

This is a **simulation-specific** claim. It is not a claim of real-world safety, clinical efficacy, biomedical applicability, universal digital-twin behavior, or deployment readiness.

## Evidence ladder

### Experiment 140 — matched-random action-identity control

On an untouched eighth population, the frozen action-plus-context rule outperformed 5,000 action-identity-matched random allocations at identical alert coverage. All preregistered criteria passed.

### Experiment 142 — learned action-only ablation

On an untouched ninth population with materially shifted unsafe prevalence, action+context captured 1,898 unsafe actions versus 1,617 for a learned action-only model at identical 39.02% alert coverage (+281), improved unsafe recall by 10.45 percentage points and ROC AUC by 0.0621, and produced a seed-bootstrap 95% interval of [5.025, 9.175] additional unsafe actions per seed. All preregistered criteria passed.

### Experiment 144 — conditional context permutation

On an untouched tenth population, correct row-level context pairing captured 2,004 unsafe actions versus a 5,000-trial within-seed×action conditional-permutation mean of 1,880.34 and 99th percentile of 1,898. No permutation matched the primary result. The preregistered criterion passed.

### Experiment 146 — first prospective simulated intervention

On an untouched eleventh population, the frozen hazard filter reduced unsafe selected actions from 811 to 454 and total realized regret from 48.8763 to 18.2045. The best 1% matched random-exclusion thresholds were still 712 unsafe selections and 39.4960 regret. Neither endpoint was matched by any of 5,000 controls. Both preregistered criteria passed.

### Experiment 148 — independent intervention replication

Without policy redesign, the same intervention on an untouched twelfth population reduced unsafe selected actions from 801 to 403 and total realized regret from 51.8658 to 10.5579. The best 1% matched-random thresholds were 690 unsafe selections and 38.8799 regret. No control matched the policy. Both original criteria passed again.

## What has been ruled out so far

The observed result is not adequately explained by:

- merely allocating the same number of alerts at random;
- action identity alone;
- a learned action-only predictor;
- seed-level environment alone;
- the marginal distribution of context-support distances alone;
- arbitrary candidate exclusions at the same per-context intervention budget;
- a single favorable intervention population.

## What remains unproven

Important unresolved questions include:

- robustness to corrupted or adversarially manipulated context/support information;
- robustness to source-model training contamination;
- calibration stability and coverage tradeoffs outside the frozen operating point;
- mechanism beyond the currently observed support-distance association;
- transfer to structurally different simulated dynamical systems;
- real-time closed-loop consequences rather than candidate-action counterfactual evaluation;
- any real-world or biomedical/clinical relevance.

## Research discipline from this checkpoint

Further work should attack one of the unresolved assumptions above rather than accumulating near-duplicate positive populations. Failed falsification tests must be retained. Stronger claims should be introduced only after prospective evidence supports them.
