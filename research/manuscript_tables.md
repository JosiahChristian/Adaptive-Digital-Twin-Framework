# Manuscript Tables — Decision-Aware Poisoning Study

## Table 1. Prospective and diagnostic experiment sequence

| Experiment | Design | Status | Main result | Interpretation |
|---:|---|---|---|---|
| 153 | preregistered constrained audit | failed | partial recovery of corrupted labels did not improve downstream utility | falsifies monotonic repair-to-utility assumption |
| 154 | boundary diagnostic | diagnostic | AUC remained nearly unchanged while 41 unsafe-to-safe vs 22 safe-to-unsafe transitions occurred | generated local cutoff-reordering mechanism hypothesis |
| 156 | prospective boundary replication | passed | unsafe selections 371→346; regret 16.1603→15.2069 | favorable downstream sign replicated on fresh population |
| 158 | preregistered prediction/decision divergence | failed | AUC 0.7947→0.7691; AP 0.4099→0.3956; unsafe 358→354; regret 12.8656→13.3993 | prediction degraded while decision endpoints moved in mixed directions |
| 159 | cross-population synthesis | descriptive | harmful, favorable, favorable, and mixed downstream responses across four untouched populations | establishes heterogeneity, not benefit |
| 161 | preregistered weak-coupling test | failed | decision-aligned recall retained meaningful association with unsafe-selection change | rejects broad weak-coupling claim |
| 163 | preregistered metric superiority | partial | unsafe-change rho: recall −0.9076, AP −0.7720, AUC −0.4984 | recall exceeded AUC; recall-over-AP bootstrap interval crossed zero |
| 165 | preregistered hierarchy replication | failed | unsafe-change rho: recall −0.5342, AP +0.1347, AUC +0.2445 | recall > AP > AUC hierarchy did not prospectively replicate |
| 166 | preregistered cutoff-geometry mechanism test | passed | MH OR 10.5675 [8.3455, 13.3810]; unsafe-crossing rho −0.8732 [−0.9464, −0.7350] | prospectively supports local cutoff reordering plus crossing composition as a simulator-internal mechanism |

## Table 2. Experiment 156 prospective boundary replication

| Quantity | Clean | Poisoned | Difference / interpretation |
|---|---:|---:|---|
| unsafe selected | 371 | 346 | −25 |
| total regret | 16.160316 | 15.206882 | −0.953434 |
| ROC AUC | 0.763685 | 0.765520 | +0.001835 |
| average precision | 0.441181 | 0.443655 | +0.002475 |
| exclusion-set Jaccard | — | — | 0.912342 |
| unsafe→safe transitions | — | — | 37 |
| safe→unsafe transitions | — | — | 12 |

Interpretation: the downstream sign replicated despite only small changes in global ranking metrics. This is not evidence that poisoning is generally beneficial.

## Table 3. Experiment 158 preregistered prediction/decision test

| Quantity | Clean | Poisoned | Change |
|---|---:|---:|---:|
| ROC AUC | 0.794692 | 0.769117 | −0.025575 |
| average precision | 0.409900 | 0.395638 | −0.014263 |
| excluded-unsafe recall | 0.780680 | 0.757594 | −0.023086 |
| unsafe selected | 358 | 354 | −4 |
| total regret | 12.865555 | 13.399262 | +0.533707 |

Preregistered divergence flag: **false**. Strong-divergence flag: **false**.

## Table 4. Seed-level metric associations with downstream outcomes

| Experiment | Endpoint | Excluded-unsafe recall rho | AP rho | ROC AUC rho | Prospective conclusion |
|---:|---|---:|---:|---:|---|
| 163 | unsafe-selection change | −0.907622 | −0.771977 | −0.498384 | strong population-specific recall association; superiority over AP not confirmed |
| 163 | regret change | −0.804072 | −0.457497 | −0.355226 | recall strongest in this population |
| 165 | unsafe-selection change | −0.534196 | +0.134710 | +0.244525 | hierarchy replication failed |
| 165 | regret change | −0.290680 | +0.369530 | +0.481448 | endpoint ordering changed; AUC largest absolute observed association |

## Table 5. Bootstrap tests of recall advantage for unsafe-selection association

| Experiment | Comparison | Observed absolute-correlation advantage | 95% bootstrap interval | Supported? |
|---:|---|---:|---|---|
| 163 | recall − AUC | 0.409238 | [0.134358, 0.706060] | yes |
| 163 | recall − AP | 0.135645 | [−0.012068, 0.309136] | no |
| 165 | recall − AUC | 0.289671 | [−0.180322, 0.666006] | no |
| 165 | recall − AP | 0.399486 | [−0.092801, 0.689561] | no |

## Table 6. Experiment 166 preregistered cutoff-geometry mechanism test

| Quantity | Result | Frozen criterion | Outcome |
|---|---:|---|---|
| seeds | 40 | untouched preregistered population | satisfied |
| source exclusion coverage | 0.390179 | descriptive | — |
| primary near-cutoff fraction | 0.10 | frozen before adjudication | satisfied |
| Mantel–Haenszel common odds ratio | 10.567477 | OR > 1 with lower 95% CI > 1 | pass |
| MH 95% CI | [8.345537, 13.380992] | lower bound > 1 | pass |
| CMH two-sided p | < machine-reported precision | significance consistent with localization | pass |
| net unsafe-crossing vs unsafe-selection rho | −0.873179 | negative with upper bootstrap CI < 0 | pass |
| bootstrap 95% CI for rho | [−0.946362, −0.735018] | upper bound < 0 | pass |
| total membership switches | 308 | descriptive | — |
| fraction of switches near cutoff | 0.503247 | descriptive | — |
| mean exclusion-set Jaccard | 0.923823 | descriptive | — |
| unsafe→safe crossings | 12 | descriptive | — |
| safe→unsafe crossings | 121 | descriptive | — |
| primary cutoff-geometry mechanism support | true | both co-primary criteria pass | **pass** |

Interpretation: on the frozen Experiment 166 simulator population, changed exclusion membership was strongly localized around the fixed action boundary and the safety composition of boundary crossings strongly tracked the downstream unsafe-selection response. This prospectively supports the local cutoff-geometry mechanism under the tested pipeline. It does not establish a universal causal law across arbitrary populations, models, attacks, or intervention budgets.

## Caption language constraint
All tables should be described as simulator-internal evidence under the frozen attack, model, population-generation, and fixed-budget intervention procedures. No table supports universal metric superiority, beneficial poisoning, deployment safety, or mechanism invariance outside the prospectively tested Experiment 166 setting.