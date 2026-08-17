# Experiment 166 — Existing-Artifact Audit Adjudication Result

## Status

This is an **audit/robustness result**, not a replacement for the historical preregistered Experiment 166 result. It executes only Analyses A–C frozen in `research/experiment_166_audit_adjudication_plan.md`. No model was retrained, no target population was regenerated, and the matched clean-to-clean perturbation control was not run.

Source reviewer snapshot: `d1e3285707ed788a39c7e883c157a8a359cde7db`.

Execution provenance:

- audit script commit: `91acfc2708df11a84ca257f684cdbfadd7f63fb6`;
- isolated workflow run: `32073115707`;
- workflow job: `95520451247`;
- audit artifact: `9302471386`;
- artifact SHA-256: `9ff108ac152fcf4a247e02ab1bc0823b97442e369feb9ba5a42756eec73764bb`.

The four scientific input artifacts used by the audit were verified byte-identical to the frozen reviewer snapshot before interpretation:

- `results/preregistered_cutoff_geometry_mechanism_rows.csv` → `220065b7525ac0563b83df3d98e4c367622dc18e`;
- `results/prospective_action_conditioned_support_representation_actions_791_830.csv` → `7037370f8ccaada4b0b19f56964262786b9fadf6`;
- `results/preregistered_cutoff_geometry_context_changes.csv` → `cd97e988b98784febf5ef2f86459ec22ac0f7925`;
- `results/preregistered_cutoff_geometry_mechanism.csv` → `cf71b022905649b9628ca03d0d030dcee82a504f`.

## Analysis A — context/seed-respecting Criterion 1 robustness

Using generation seed as the independent inferential unit:

- 40 seeds;
- mean seed-level near-cutoff switch rate: **0.15342**;
- mean seed-level far-cutoff switch rate: **0.01719**;
- mean near-minus-far rate difference: **0.13623**;
- 95% seed-bootstrap interval for the difference: **[0.11424, 0.15789]**;
- 95% of seeds had a positive near-minus-far difference.

A secondary context aggregation found 1,002 contexts containing both near- and far-cutoff candidates. In those contexts, the presence rate of a near-cutoff switch was 0.15469 and the presence rate of a far-cutoff switch was 0.

### Adjudication

The original localization/enrichment phenomenon is **robust to seed-level inference** and is not explained away merely by treating the three candidate rows per context as independent Bernoulli observations.

This result does **not** establish that the localization is poisoning-specific. A fixed-budget ranking rule may still generically localize perturbation-induced membership changes near its cutoff.

## Analysis B — Criterion 2 bookkeeping-preserving null

A 10,000-permutation null preserved each seed's candidate contexts, unsafe labels, predicted action losses, actual switched set, common exclusions, fixed clean/poison exclusion counts, and the unchanged downstream action-selection rule. It randomized only which switched rows were assigned to the clean-only versus poison-only side.

Results:

- observed Spearman rho: **-0.87318**;
- null mean rho: **-0.87142**;
- null median rho: **-0.87653**;
- central 95% null interval: **[-0.93697, -0.77690]**;
- observed percentile in the null: **0.5331**;
- one-sided probability of a rho as or more negative than observed: **0.53315**.

### Adjudication

The observed Criterion 2 correlation is **ordinary under the bookkeeping-preserving null**. It therefore does not provide independent evidence for the proposed composition-to-decision mechanism beyond the structural relationship induced by the constrained exclusion/selection pipeline.

This confirms the structural-coupling objection while rejecting the stronger claim that the two variables are algebraically identical.

## Analysis C — near-cutoff versus far-cutoff downstream specificity

The classification rule was frozen before execution: switched contexts were `near_only`, `far_only`, or `mixed`, with the primary comparison `near_only` versus `far_only` and mixed contexts reported separately.

Results:

- total switched contexts: **308**;
- `near_only`: **155**;
- `far_only`: **153**;
- `mixed`: **0**;
- selected-action-change rate in `near_only`: **0.63871**;
- selected-action-change rate in `far_only`: **0.95425**;
- near-minus-far rate difference: **-0.31554**;
- 95% seed-bootstrap interval: **[-0.40818, -0.23161]**;
- Haldane-corrected near-versus-far odds ratio: **0.09016**.

### Adjudication

The frozen evidence does **not** show that near-cutoff-only switches are more consequential for final selected-action changes. The observed direction is strongly opposite: far-cutoff-only switched contexts were substantially more likely to change the selected action.

## Combined interpretation

The audit separates one surviving phenomenon from the stronger mechanism claim:

1. **Survives:** clean-versus-poison membership switches are strongly enriched near the clean fixed-budget cutoff, and that enrichment survives seed-level inference.
2. **Does not survive as independent mechanistic evidence:** the Criterion 2 crossing-composition correlation is reproduced by a bookkeeping-preserving structural null.
3. **Falsified under the frozen specificity test:** downstream selected-action changes are not preferentially associated with near-cutoff-only switched contexts; the result is in the opposite direction.

Accordingly, the current frozen evidence does **not** support the stronger phrase **"local cutoff-geometry mechanism"** as a mechanism connecting cutoff proximity, switched-set composition, and downstream selected-action change.

The historical Experiment 166 preregistered pass remains part of the record; this audit demonstrates that passing those frozen criteria was not sufficient to diagnose the mechanism originally named.

The remaining high-information question is narrower: **is the surviving near-cutoff localization itself specific to poisoning, or is it a generic consequence of perturbing a correlated score ranking under a fixed top-N selector?** Answering that requires the separately locked matched clean-to-clean perturbation control, which would create new model evidence and was not executed here.

## Claim gate

Until that next evidence decision is explicitly authorized and separately designed:

- preserve the original Experiment 166 result unchanged;
- do not present Criterion 2 as independent mechanistic support;
- do not present the conjunction of Criteria 1 and 2 as validating a local cutoff-geometry mechanism;
- preserve the negative audit findings alongside the positive localization result;
- do not strengthen Abstract, Discussion, or Conclusion language from Experiment 166.
