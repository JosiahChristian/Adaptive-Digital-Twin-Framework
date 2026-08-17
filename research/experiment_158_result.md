# Experiment 158 result: prediction-decision divergence

Experiment 158 did not satisfy the preregistered divergence criterion.

On the untouched 44631-44670 population, targeted 20% unsafe-to-safe label concealment degraded all three frozen prediction metrics: ROC AUC 0.79469 -> 0.76912, average precision 0.40990 -> 0.39564, and excluded-unsafe recall 0.78068 -> 0.75759. Decision endpoints split: unsafe selections decreased slightly from 358 to 354, while total realized regret increased from 12.8656 to 13.3993.

The correct interpretation is therefore not a clean prediction/decision sign reversal. Instead, the result adds evidence that downstream decision utility is endpoint-specific and not monotonic in the conventional prediction metrics under the fixed top-N intervention policy and population shift.

The next step is a cross-population synthesis of all prospectively generated target blocks using the exact same clean and targeted-poisoned models, followed by a new prospective test only after the recurring pattern is stated precisely.
