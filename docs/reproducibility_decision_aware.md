# Reproducibility Package — Decision-Aware Adversarial Label Corruption

## Scope
This package documents the exact evidence path for the decision-aware poisoning line through Experiment 166. The objective is independent rerunability of the frozen computational comparisons, not merely archival preservation of favorable outputs.

## Canonical evidence map

| Stage | Experiment(s) | Primary artifact(s) | Inferential role |
|---|---:|---|---|
| constrained repair | 153 | experiment result note + downstream result artifacts | falsified simple repair-improves-utility claim |
| boundary diagnostic | 154 | `research/experiment_154_result.md` | generated local cutoff-reordering hypothesis |
| prospective boundary replication | 155–156 | `results/prospective_poisoning_boundary_replication.csv` | replicated favorable downstream sign on fresh population |
| prediction/decision divergence test | 157–158 | `results/preregistered_prediction_decision_divergence.csv` | failed strong divergence criterion; retained mixed endpoint result |
| cross-population synthesis | 159 | synthesis artifacts / chronology | established heterogeneous downstream signs descriptively |
| seed-level coupling | 160–161 | seed-level evaluation artifacts | rejected broad weak-coupling claim |
| metric-superiority test | 162–163 | `results/preregistered_intervention_aligned_metric_superiority.csv` | partial support for decision-aligned recall over ROC AUC |
| hierarchy replication | 164–165 | `results/preregistered_intervention_aligned_metric_hierarchy_replication.csv` and `_by_seed.csv` | falsified stable recall > AP > AUC hierarchy |
| cutoff-geometry mechanism | 166 | `research/experiment_166_preregistration.md`, `results/preregistered_cutoff_geometry_mechanism.csv`, `_by_seed.csv`, `_rows.csv`, and context-change artifact | prospectively supported local cutoff localization and unsafe-crossing composition mechanism in the frozen pipeline |

## Environment
The Experiment 166 adjudication workflow records the current reproducible runtime baseline:

- Ubuntu GitHub Actions runner
- Python 3.11
- NumPy
- pandas
- SciPy
- scikit-learn
- statsmodels

For exact historical reruns, use the workflow corresponding to the experiment being reproduced rather than assuming all earlier experiments used identical dependency versions.

## Reproduction levels

### Level 1 — artifact verification
Confirm that tracked result CSVs contain the reported scalar outcomes and that manuscript tables and figures are generated directly from those files. No simulation rerun is required.

### Level 2 — experiment rerun
Use the experiment-specific GitHub Actions workflow or run the corresponding Python module locally from the repository root. Preserve the frozen target population, attack definition, intervention budget, endpoints, cutoff-band definition, and seed ranges.

### Level 3 — prospective reconstruction
Where an experiment separates target reconstruction from evaluation, rerun the reconstruction stage first and then the frozen evaluation stage without outcome-dependent changes between stages.

## Experiment 166 reference commands

Target reconstruction:

```bash
python -m pip install --upgrade pip numpy pandas scipy scikit-learn statsmodels
python -m experiments.prospective_support_reconstruction_791_830
```

Frozen mechanism adjudication:

```bash
python -m experiments.preregistered_cutoff_geometry_mechanism
```

The adjudication must consume the already reconstructed seeds 44791–44830 and retain the preregistered 10% near-cutoff band, Mantel–Haenszel/CMH criterion, and 10,000 paired seed bootstrap for the net-unsafe-crossing association.

## Experiment 166 primary verification values
The canonical summary artifact must reproduce:

- 40 target seeds;
- Mantel–Haenszel common odds ratio 10.567476648997085;
- 95% CI [8.345536708045579, 13.380992335632634];
- cutoff-localization criterion pass = 1;
- Spearman rho(net unsafe crossing, delta unsafe selected) = -0.8731789408092587;
- 95% bootstrap interval [-0.9463615603179073, -0.7350180597401996];
- composition-direction criterion pass = 1;
- overall cutoff-geometry mechanism support = 1;
- 308 membership switches, with 0.5032467532467533 in the frozen closest-10% band;
- mean exclusion-set Jaccard = 0.9238228511679869.

## Integrity rules

1. Do not alter seed ranges after observing results.
2. Do not replace failed preregistered endpoints with post-hoc rescue endpoints while retaining a prospective label.
3. Distinguish diagnostic analyses from prospective tests in all figures and manuscript prose.
4. Preserve negative, mixed, and null findings in the evidence package.
5. Treat `research/decision_aware_master_results.csv` as the compact index, not as a replacement for primary result files.
6. For Experiment 166, do not redefine the primary 10% cutoff band post hoc; 5% and 20% sensitivity bands remain secondary only.
7. For future experiments, require a materially new mechanism/generalization question and a committed preregistration before outcome inspection.

## Verification checklist

- [ ] repository commit SHA recorded for the submitted manuscript
- [ ] experiment-specific workflows present
- [ ] all primary CSV artifacts tracked
- [ ] seed-level artifacts retained where statistical claims depend on them
- [ ] row-level cutoff-geometry artifact retained for Experiment 166
- [ ] context-transition artifact retained for Experiment 166
- [ ] manuscript values traceable to a named file and column
- [ ] figure-generation source data retained
- [ ] failed hypotheses represented in tables and discussion
- [ ] Experiment 166 co-primary pass/fail flags reproduced from raw artifacts
- [ ] scope limits stated explicitly

## Current reproducibility boundary
The package supports computational reproducibility within this simulator and repository. Experiment 166 provides prospective mechanism support for the frozen model/attack/intervention pipeline, but the package does not establish external validity, deployment safety, transfer to real cyber-physical systems, or invariance across arbitrary model classes, attack mechanisms, population generators, or intervention budgets.
