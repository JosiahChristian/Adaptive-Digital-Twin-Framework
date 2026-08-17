# Manuscript Update Required After Experiment 166

The existing decision-aware manuscript draft predates Experiment 166 and should not be treated as current until the following evidence is incorporated.

## Result that must be added

Experiment 166 is the first direct preregistered prospective test of the local cutoff-geometry mechanism suggested by the earlier decision-aware sequence.

On 40 frozen generation seeds, both primary criteria passed:

- cutoff localization: Mantel–Haenszel common odds ratio **10.567477**, 95% interval **[8.345537, 13.380992]**;
- boundary-composition direction: Spearman rho **-0.873179** between net unsafe crossing and unsafe-selection change, bootstrap interval **[-0.946362, -0.735018]**.

The primary cutoff-geometry mechanism-support flag passed.

## Narrative change required

The manuscript should no longer present boundary geometry only as an inferred explanation for metric/outcome discordance. It can now state, in simulator-bounded language, that a prospectively specified experiment directly supported:

1. strong localization of perturbation-induced membership switches near the fixed-budget cutoff; and
2. a strong association between the safety composition of those crossings and the resulting change in unsafe selections.

## Negative/limiting evidence that must remain visible

The same target population produced predominantly harmful composition changes:

- unsafe-to-safe transitions: **12**;
- safe-to-unsafe transitions: **121**;
- mean ΔAUC: **-0.040164**;
- mean ΔAP: **-0.063054**;
- mean Δexcluded-unsafe recall: **-0.044180**.

This is evidence for a mechanism, not beneficial poisoning.

The manuscript must preserve the failed metric-hierarchy replication preceding Experiment 166. Experiment 163's favorable metric ordering should not be rewritten as a stable universal hierarchy simply because the later mechanism test succeeded.

## Claim wording allowed

A defensible manuscript formulation is:

> Within the tested simulator and fixed-budget intervention procedure, model perturbations can change downstream safety outcomes through localized membership changes near the intervention cutoff; the safety composition of those boundary crossings strongly tracks the resulting unsafe-selection change.

## Claim wording still prohibited

The manuscript should not state or imply:

- cutoff geometry is the only causal mechanism;
- the mechanism is invariant to intervention budget;
- the mechanism transfers across attacks, models, simulators, or domains;
- poisoning is beneficial or useful regularization;
- the result establishes real-world safety or biomedical relevance.

## Required next manuscript gate

Before the decision-aware line is promoted to a broader/general mechanism claim, the manuscript should await at least one meaningful falsification/replication step such as budget shift, attack shift, model shift, or a second untouched-population mechanism replication.

Until then, Experiment 166 should be presented as a strong simulator-specific prospective mechanism result.
