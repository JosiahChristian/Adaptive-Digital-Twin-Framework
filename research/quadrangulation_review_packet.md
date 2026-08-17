# ADT External Adversarial Review Packet

## Status

Prepared in advance for the final quadrangulation gate. Do not submit this packet as a substitute for a frozen manuscript/repository snapshot; the external review should occur only when the active experimental cycle is declared complete enough for adversarial review.

## Reviewer role

Act as a skeptical independent peer reviewer with no obligation to preserve the authors' preferred narrative. Attempt to falsify the strongest claims using the repository evidence.

## Primary questions

1. Which manuscript/research claims are directly supported by prospective evidence?
2. Which claims rely primarily on retrospective or diagnostic analysis?
3. Is there any temporal leakage, target leakage, population reuse, threshold reuse, or post-outcome endpoint selection?
4. Are negative/null results represented with the same visibility as favorable results?
5. Do the statistical procedures match the sample structure and repeated-seed design?
6. Are confidence intervals, bootstrap procedures, and multiplicity choices defensible?
7. Are any apparent replications merely new random seeds from effectively the same generating distribution?
8. Could simpler confounds explain the pre-decision harmful-expansion result?
9. Does Experiment 166 genuinely test a local cutoff mechanism prospectively, or can its two co-primary criteria be satisfied by an alternative explanation?
10. Which claimed mechanisms survive meaningful population, budget, attack, and model changes?
11. Does the manuscript ever convert association into causal language without intervention-level evidence?
12. What is the strongest claim you would accept today, and what is the strongest claim you would reject?

## Required attacks on the Experiment 166 line

The reviewer should specifically challenge:

- whether the 10% near-cutoff band was fixed before target adjudication;
- whether the Mantel–Haenszel stratification is appropriate;
- whether membership switches are independent enough for the reported inferential treatment;
- whether the strong seed-level crossing/outcome correlation is partly definitional or mathematically coupled to the unsafe-selection endpoint;
- whether high exclusion-set Jaccard overlap plus localized switching supports the proposed mechanism or admits a simpler ranking-instability explanation;
- whether the mechanism survives intervention-budget changes;
- whether the mechanism survives a meaningful population-family shift rather than another seed sample;
- whether the mechanism survives a distinct attack and model class;
- whether boundary composition can prospectively predict effect sign.

## Required attacks on the harmful-expansion line

The reviewer should specifically challenge:

- event-definition sensitivity;
- feature timing and leakage;
- small harmful-event count;
- class imbalance;
- one-feature and low-capacity baselines;
- calibration stability;
- population independence;
- action/block confounding;
- whether the result remains useful after reasonable label-definition changes.

## Output format requested from external reviewer

For every criticism, classify it as:

- **fatal under current evidence**;
- **major but correctable**;
- **minor/reporting**;
- **not actually supported by repository evidence**.

For every major/fatal criticism, specify the minimum analysis or experiment that would resolve it.

Then provide:

1. strongest defensible claim;
2. strongest unsupported claim found;
3. top five threats to validity;
4. minimum experiments required before manuscript submission;
5. whether the work is currently suitable for faculty review, workshop submission, conference/journal submission, or none of these;
6. a recommendation: reject, major revision, minor revision, or provisionally accept, with reasoning.

## Reconciliation rule

The external review is one evidence source, not an authority vote. During quadrangulation, each criticism must be reconciled against the actual experiment artifacts and classified as already addressed, valid/unresolved, mistaken, requiring a new experiment, or requiring a wording/documentation change. Disagreements are resolved by evidence, not by majority opinion.
