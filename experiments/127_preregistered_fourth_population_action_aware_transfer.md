# Experiment 127 — preregistered fourth-population action-aware transfer

## Protocol

The model and analysis were committed before Experiment 126 generated seeds
44151–44190. The primary model was trained only on population 071–110 and used
action identity plus context support distance. There was no target refitting,
threshold selection, coefficient correction, or feature selection.

## Results

| Frozen model | ROC AUC | 95% bootstrap CI | Balanced accuracy at 0.5 |
|---|---:|---:|---:|
| **Primary: action + context support** | **0.829** | **[0.821, 0.838]** | **0.762** |
| Action identity only | 0.781 | [0.771, 0.791] | 0.750 |
| Context support only | 0.614 | [0.600, 0.628] | 0.527 |

The primary model achieved unsafe recall 0.772 and unsafe precision 0.430 at
the frozen threshold.

Its AUC advantage over action identity alone was +0.0480, with paired
95% bootstrap CI [+0.0416, +0.0545] and positive difference in all 5,000
bootstrap samples. Its advantage over context support alone was +0.2150
[+0.2004, +0.2297], also positive in all samples.

## Conclusion

The preregistered fourth-population result confirms that explicit action
identity plus context support is a portable candidate-action harm-ranking
representation in this simulation regime. This directly survives the failure
of the action-agnostic joint proxy in Experiment 123.

The result does not validate the earlier 11-feature controller-event model,
does not establish causality, and does not imply deployment readiness.
It establishes prospective cross-population discrimination for candidate-action
harm under the current simulator and frozen training protocol.

## Reproducibility note

The reconstruction result was pushed by GitHub Actions. GitHub suppresses
workflow chaining from token-authored pushes, so Experiment 127 was triggered
by a workflow-only commit after reconstruction. The preregistered Python model
file was unchanged; only the workflow path trigger was added.

## Artifacts

- `results/preregistered_fourth_population_action_aware_transfer.csv`
- `results/preregistered_fourth_population_action_aware_transfer_bootstrap.csv`
