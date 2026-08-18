# Adaptive-Digital-Twin-Framework

Computational research framework for adaptive digital twins in complex evolving systems.

## Repository purpose

This repository is maintained as an experimental evidence record. It contains research questions, preregistrations, experiment implementations, generated result artifacts, falsification studies, audit code, negative results, and reproducibility material.

No manuscript or publication is represented as complete on `main`. Interpretive papers will be authored separately from this evidence base.

## Current evidence status

### Experiment 166: fixed-budget cutoff localization

The historical poisoning condition produced:

- mean exclusion-set Jaccard: **0.923823**
- membership switches: **308**
- near-cutoff Mantel-Haenszel odds ratio: **10.567477**
- 95% CI: **[8.345537, 13.380992]**
- Criterion-2 Spearman rho: **-0.873179**

Later falsification and control work changed the interpretation of those original positive criteria:

- a bookkeeping-preserving null reproduced the Criterion-2 correlation;
- near-only switched contexts did not show preferential downstream selected-action change relative to far-only contexts;
- a prospectively frozen label-preserving non-poison control adequately matched perturbation magnitude and reproduced essentially the same cutoff localization.

For the stronger matched control:

- poison mean near-minus-far enrichment: **0.13623**
- control mean near-minus-far enrichment: **0.13438**
- poison-minus-control difference: **0.001845**
- 95% seed-bootstrap CI: **[0.0000, 0.00554]**
- current specificity status: **not established / specificity unresolved**

The evidence supports a near-cutoff localization phenomenon within the tested fixed-budget ranking pipeline. The current evidence does not establish poisoning specificity or an independent causal boundary-composition mechanism.

Relevant internal records include the Experiment 166 preregistration/result chain, `research/audit/`, the experiment chronology, and the current evidence-status records.

### Harmful-expansion discrimination

The tracked compact model result contains **65 events**: 15 harmful and 50 beneficial. Retrospective performance includes:

- balanced accuracy: **0.950**
- harmful-event recall: **1.000**
- harmful-event precision: **0.750**
- ROC AUC: **approximately 0.979**

The later timing audit established that two residual features require post-outcome information. The headline compact model is therefore evidence of retrospective outcome-informed discrimination, not valid pre-decision prediction.

Models restricted to temporally legitimate loss-surface information showed weaker exploratory discrimination, with pooled ROC AUC approximately **0.683–0.711** in the documented analyses.

[Tracked compact-model result](results/absolute_loss_floor_harmful_expansion_analysis.csv)

### Preserved negative and failed results

The evidence record retains findings that constrain favorable results, including:

- Experiment 165 did not prospectively replicate the earlier recall > AP > AUC hierarchy;
- Experiment 158 did not satisfy its preregistered prediction-decision divergence criteria;
- simple support-distance representations were weak as standalone unsafe-behavior detectors;
- pooled discrimination did not consistently survive conditioned transfer;
- Experiment 166 Criterion 2 did not survive the structural-null challenge;
- preferential downstream near-switch specificity failed;
- poisoning specificity was unresolved under the stronger matched non-poison control;
- the strongest harmful-expansion model contains confirmed prediction-time leakage.

## Evidence organization

```text
research/       preregistrations, chronology, audits, evidence-status records
experiments/    executable experimental programs
results/        tracked generated outputs
simulation/     simulated system and trajectory generation
models/         adaptive and predictive model code
tests/          implementation checks
.github/        reproducibility and CI workflows
```

## Evidence standard

Experimental claims remain conditional on the exact population, seed structure, model, feature construction, intervention rule, and outcome definition recorded for each experiment. Candidate/action rows are not automatically treated as independent experimental replications. Later falsification results do not delete earlier positive results; they constrain their interpretation.

## Reproducibility

Experiment code, workflow definitions, generated summaries, and audit scripts are retained so reported findings can be checked against the producing source revision. Where a result is preserved as a CI artifact rather than a tracked result file, provenance information is retained separately.

## Current status

**Active research evidence base.**

The repository does not claim that the general adaptive-digital-twin problem has been solved, that Experiment 166 identifies a poisoning-specific mechanism, or that the retrospective harmful-expansion classifier is a validated pre-decision predictor.
