# Experiment 166 — Frozen Audit Adjudication Plan

## Status

This document specifies the order, estimands, and interpretation rules for adjudicating the independent-audit objections to Experiment 166. It is a coordination/audit artifact only. It does **not** execute a remedial analysis, regenerate outcomes, retrain a model, modify the preregistration, or change any manuscript claim.

The manuscript/claim freeze remains active. The original Experiment 166 result is preserved exactly as committed. The purpose of this plan is to prevent the audit response itself from becoming post-hoc researcher degrees of freedom.

Original reviewer snapshot: `d1e3285707ed788a39c7e883c157a8a359cde7db`.

## Audit questions to adjudicate

### Q1. Is Criterion 1's precision materially dependent on treating nested candidate rows as independent?

Original Criterion 1 is a seed-stratified row-level near-cutoff-versus-far comparison. The audit objection is that the three action candidates are nested within contexts and the fixed top-N exclusion rule induces dependence among candidate membership changes.

### Q2. Is Criterion 2 substantially a bookkeeping identity induced by the definitions and fixed-budget action-selection pipeline?

Criterion 2 correlates `net_unsafe_crossing` with `delta_unsafe_selected`. Both are downstream of changes to exclusion membership, so an observed negative association may partly or wholly arise from the selection bookkeeping even without poisoning-specific causal structure.

### Q3. Are downstream consequences specifically associated with near-cutoff switches rather than membership changes generally?

Criterion 1 establishes localization of switches relative to the clean cutoff, but does not by itself show that near-cutoff switches are more consequential for final selected actions than far-cutoff switches.

### Q4. Is Criterion 1 localization specific to poisoning rather than generic score perturbation under fixed top-N selection?

This requires a matched clean-to-clean perturbation/model-fit control. It cannot be answered from the existing artifacts alone and remains locked under the current freeze.

## Frozen existing-artifact adjudication sequence

No computation in this sequence is authorized merely by this document. Execution remains gated by reconciliation of the independent audit.

### Analysis A — context/seed-respecting Criterion 1 robustness

**Unit structure:** seed -> context -> three candidate actions.

**Frozen exposure:** candidate membership in the preregistered 10% near-cutoff band, computed exactly as Experiment 166 recorded it.

**Frozen outcome:** `membership_switch`.

**Primary audit estimand:** whether near-cutoff membership remains positively associated with switching when uncertainty respects context clustering and the seed structure.

**Required invariants:**

- do not redefine the 10% band;
- do not alter clean/poison exclusion masks;
- do not regenerate candidate rows;
- do not treat action rows as freely exchangeable across contexts;
- preserve all seeds, including zero-switch or sparse-switch seeds;
- report an effect estimate and uncertainty, not only a p-value.

**Interpretation:**

- If the cluster-respecting result remains clearly positive, the pseudoreplication objection is weakened but the poisoning-specificity objection remains unresolved.
- If uncertainty expands to include no enrichment or the direction becomes unstable, the original Criterion 1 inferential claim is not robust enough for mechanism language.

### Analysis B — Criterion 2 bookkeeping null

Construct a null using only the committed target rows, unsafe labels, predicted action losses, and frozen exclusion budget. The null must preserve the aspects of the selection problem that mechanically constrain `net_unsafe_crossing` and `delta_unsafe_selected` while breaking the poisoning-specific mapping between actual clean-only/poison-only membership changes and downstream action consequences.

**Required invariants:**

- preserve each seed's target contexts and three-action candidate sets;
- preserve the fixed exclusion count used in that seed;
- preserve candidate unsafe labels and predicted action losses;
- use the unchanged Experiment 166 downstream action-selection rule;
- do not retrain either hazard model;
- do not generate a new target population;
- define the permutation/exchangeability unit before execution;
- compare the observed Criterion 2 association with the resulting null distribution.

**Interpretation:**

- If associations as negative as the observed rho are common under the bookkeeping-preserving null, Criterion 2 cannot independently establish the proposed composition-to-decision mechanism.
- If the observed association is extreme relative to a valid null, the structural-coupling objection is weakened, subject to the null's adequacy.

### Analysis C — near-cutoff versus far-cutoff downstream specificity

This audit analysis asks whether switched candidates close to the frozen clean cutoff are more associated with final selected-action changes than switched candidates farther away.

Because a context may contain more than one switched candidate, candidate-level attribution is not permitted post hoc.

**Pre-execution context classification rule:**

For each context containing at least one membership switch, classify the context into one of three mutually exclusive groups:

1. `near_only`: one or more switched candidates are near-cutoff and no switched candidate is far-cutoff;
2. `far_only`: one or more switched candidates are far-cutoff and no switched candidate is near-cutoff;
3. `mixed`: both near- and far-cutoff switched candidates occur.

The primary specificity contrast is `near_only` versus `far_only`. `mixed` contexts are reported separately and are not reassigned to either group.

**Frozen downstream outcome:** whether the final selected action changes between clean and poisoned pipelines. Transition type and regret change remain descriptive secondary outcomes.

**Interpretation:**

- A stronger selected-action-change rate in `near_only` than `far_only` contexts would support downstream specificity of boundary-local switches.
- No difference, reversal, or severe sparsity would limit the mechanistic interpretation even if original Criterion 1 remains statistically enriched.

## Locked new-evidence control

### Analysis D — matched clean-to-clean perturbation control

Fit a distinct clean model under a prespecified alternative random seed and compare clean-to-clean score/exclusion perturbations with the observed clean-to-poison perturbation under the same target population and fixed-budget intervention.

This is **new computed model evidence** and is not authorized under the current freeze. Before execution it requires an explicit design specification including the alternative seed(s), whether one or multiple re-fits are used, the matching statistic(s), and the decision rule.

Its purpose is to distinguish poisoning-specific cutoff localization from generic order-statistic sensitivity of a fixed top-N selector.

## Reporting corrections independent of scientific adjudication

The audit identified a numeric `p = 0.0` representation caused by floating-point underflow. Any future manuscript/report rendering should describe such a result as below numerical precision or with an appropriate computable inequality rather than as a literal probability of zero. This is a reporting correction, not evidence strengthening.

Negative, failed, null, mixed, and weak-coupling results remain part of the evidentiary record and must not be removed during reconciliation.

## Claim gate

Until the independent audit, External Review A, and the remaining external review lanes are reconciled artifact-by-artifact:

- Experiment 166's committed pass remains a historical result of its preregistered criteria;
- the stronger causal/mechanistic interpretation remains provisional;
- Abstract, Discussion, and Conclusion language must not be strengthened from Experiment 166;
- no remediation result may silently replace the original result;
- any later adjudication must be reported as an audit/robustness analysis distinct from the preregistered experiment.
