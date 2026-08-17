# Review A — Existing-Artifact Remediation Feasibility

## Scope and freeze

This note answers only whether the frozen Experiment 166 evidence package contains enough information to perform the remedial analyses proposed by External Review A. It does **not** execute those analyses, change any scientific claim, modify Experiment 166, or authorize a new experiment. The claim-change/remediation freeze remains active pending reconciliation with the independent audit lane.

Reviewer snapshot: `d1e3285707ed788a39c7e883c157a8a359cde7db`.

## Frozen evidence structure verified

The Experiment 166 implementation writes three analysis tables in addition to the aggregate summary:

- `results/preregistered_cutoff_geometry_mechanism_rows.csv`
- `results/preregistered_cutoff_geometry_mechanism_by_seed.csv`
- `results/preregistered_cutoff_geometry_context_changes.csv`

The implementation also reads the committed target action table `results/prospective_action_conditioned_support_representation_actions_791_830.csv`. It explicitly requires `predicted_action_loss`, `unsafe_action`, `realized_action_regret`, `generation_seed`, `test_index`, and `action`, and asserts exactly three candidate actions per context.

The row-level output contains, by construction, `generation_seed`, `test_index`, `action`, `unsafe_action`, `realized_action_regret`, clean/poison scores, score delta, clean/poison exclusion masks, membership-switch status, clean cutoff score, absolute cutoff margin, and the frozen primary near-cutoff indicator.

The seed-level output contains the counts and endpoints needed to reproduce the published Criterion 1/2 summaries, including near/far switches, clean-only and poison-only exclusions, unsafe composition of those changes, `net_unsafe_crossing`, clean/poison unsafe selections, `delta_unsafe_selected`, regret, Jaccard overlap, transition counts, and metric deltas.

The changed-context table contains clean and poisoned selected actions, their unsafe labels, transition type, and regret for every context where the selected action changed.

## Feasibility of Review A remedies

### A. Criterion 1 dependence / cluster-respecting robustness

**Feasibility from frozen artifacts: YES.**

The committed row table contains seed and context identifiers plus `near_cutoff_primary` and `membership_switch`. Therefore a robustness analysis can resample or permute at seed/context-respecting units rather than treating action rows as freely independent. The original MH statistic can also be reconstructed from the existing rows/seed tables.

Important distinction: the analysis design must be specified before execution. A naive row shuffle would reproduce the same independence problem Review A identified. A valid robustness check must preserve the clustered structure and fixed-budget constraints it is intended to respect.

### B. Criterion 2 structural/bookkeeping null

**Feasibility from frozen artifacts: YES, with the committed upstream target action table.**

The row table alone contains the actual exclusion masks and unsafe labels but does not contain `predicted_action_loss`, which the downstream `select_actions` rule requires for counterfactual reselection. However, the frozen Experiment 166 implementation points to a committed target action table that contains `predicted_action_loss` and the same seed/context/action structure. Combining that committed target table with the row-level Experiment 166 output is sufficient in principle to construct counterfactual exclusion-mask permutations and rerun the unchanged downstream selection rule without generating a new target population or retraining the hazard model.

This would be a **new analysis of existing frozen evidence**, not a new scientific experiment, provided no new target/model outcomes are generated.

### C. Criterion 2 near-cutoff vs far-cutoff contrast

**Feasibility from frozen artifacts: YES, but the estimand must be defined carefully before execution.**

The row output explicitly identifies each switch as near/far relative to the frozen 10% cutoff band, and the target table supplies the downstream selection variables. The existing changed-context table documents actual selection changes, but by itself does not assign a downstream context-level consequence uniquely to one switched candidate when multiple candidate exclusions in the same context change. Therefore a valid near-vs-far comparison should define in advance how contexts with multiple switches are handled rather than attributing an outcome to individual rows post hoc.

### D. Criterion 1 matched non-poisoning perturbation control

**Feasibility from existing artifacts alone: NO.**

Review A's proposed clean-model re-seed comparator requires fitting a new clean model under a distinct random seed and generating a new clean-vs-clean score perturbation. The same frozen target population can be reused, but the model fit itself is new computed evidence. It should therefore be treated as a genuinely new control experiment/analysis and should not be run under the current freeze.

### E. Threshold-band sensitivity

**Feasibility from frozen artifacts: YES.**

The row table records continuous absolute distance to the clean cutoff, so descriptive or prospectively specified sensitivity analyses for alternative bands can be computed without regenerating outcomes. Because 5%/20% were secondary preregistered analyses, any inferential expansion beyond the preregistration must remain explicitly secondary/exploratory.

## Current logistics conclusion

Review A's three most important Experiment 166 objections divide cleanly:

1. **unit-of-analysis/dependence** — adjudicable with existing frozen artifacts;
2. **Criterion 2 bookkeeping/geometric specificity** — adjudicable with existing frozen artifacts plus the already-committed target action table;
3. **poisoning-specificity of Criterion 1** — requires a new matched non-poisoning model-fit control and remains locked until the independent audit is reconciled.

No remedial computation has been run as part of this feasibility audit.
