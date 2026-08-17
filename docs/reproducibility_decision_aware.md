# Reproducibility Package — Decision-Aware Adversarial Label Corruption

## Scope
This package documents the exact evidence path for the decision-aware poisoning line through Experiment 165. The objective is independent rerunability of the frozen computational comparisons, not merely archival preservation of favorable outputs.

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

## Environment
The Experiment 165 workflow records the current reproducible runtime baseline:

- Ubuntu GitHub Actions runner
- Python 3.11
- NumPy
- pandas
- SciPy
- scikit-learn

For exact historical reruns, use the workflow corresponding to the experiment being reproduced rather than assuming all earlier experiments used identical dependency versions.

## Reproduction levels

### Level 1 — artifact verification
Confirm that the tracked result CSVs contain the reported scalar outcomes and that manuscript tables are generated directly from those files. No simulation rerun is required.

### Level 2 — experiment rerun
Use the experiment-specific GitHub Actions workflow or run the corresponding Python module locally from the repository root. Preserve the frozen target population, attack definition, intervention budget, endpoints, and seed ranges.

### Level 3 — prospective reconstruction
Where an experiment pair separates target reconstruction from evaluation, rerun the reconstruction stage first and then the frozen evaluation stage without inspecting outcome-dependent results between stages.

## Experiment 165 reference command

```bash
python -m pip install --upgrade pip numpy pandas scipy scikit-learn
python -m experiments.preregistered_intervention_aligned_metric_hierarchy_replication
```

The corresponding workflow additionally captures console output and uploads/commits the summary and by-seed CSV artifacts.

## Integrity rules

1. Do not alter seed ranges after observing results.
2. Do not replace failed preregistered endpoints with post-hoc rescue endpoints while retaining a prospective label.
3. Distinguish diagnostic analyses from prospective tests in all figures and manuscript prose.
4. Preserve negative, mixed, and null findings in the evidence package.
5. Treat `research/decision_aware_master_results.csv` as the compact index, not as a replacement for primary result files.
6. Any future Experiment 166+ must answer a materially new mechanism/generalization question and receive its own preregistration before outcome inspection.

## Verification checklist

- [ ] repository commit SHA recorded for the submitted manuscript
- [ ] experiment-specific workflows present
- [ ] all primary CSV artifacts tracked
- [ ] seed-level artifacts retained where statistical claims depend on them
- [ ] manuscript values traceable to a named file and column
- [ ] figure-generation source data retained
- [ ] failed hypotheses represented in tables and discussion
- [ ] scope limits stated explicitly

## Current reproducibility boundary
The package supports computational reproducibility within this simulator and repository. It does not establish external validity, deployment safety, transfer to real cyber-physical systems, transfer across arbitrary model classes, or transfer across attack/intervention settings not prospectively tested.
