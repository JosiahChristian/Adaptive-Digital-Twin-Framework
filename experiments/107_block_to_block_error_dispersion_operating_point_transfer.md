\# Experiment 107 — Block-to-Block Error-Dispersion Operating-Point Transfer



\## Purpose



Experiment 106 identified:



`local\_error\_std`



as the strongest compact historical second-stage selector candidate under reciprocal block-held-out validation.



Its block-held-out ROC AUC values were:



\- 0.716

\- 0.895



with:



\- mean ROC AUC: 0.806

\- minimum ROC AUC: 0.716

\- coefficient sign stability: 100%



However, useful ranking discrimination does not guarantee that a single absolute operating threshold transfers between regimes.



Experiment 107 therefore tests whether an intervention-style operating point derived from one historical block transfers unchanged to the other historical block.



The central question is:



\*\*Can an absolute threshold on local calibration-error dispersion retain harmful-event sensitivity and beneficial-expansion specificity when transferred across historical regimes?\*\*



Experiment 107 is a historical operating-point transfer analysis.



It does not:



\- introduce a new prospective seed block,

\- modify the controller,

\- define a deployable intervention threshold,

\- or alter the Experiment 101 calibration-aware controller.



\---



\## Historical Blocks



Experiment 107 uses the same two already-consumed support-expansion blocks analyzed in Experiments 105 and 106.



\### Block 071-090



Seeds:



44071-44090



Support-expansion population:



\- beneficial: 37

\- harmful: 2



\### Block 091-110



Seeds:



44091-44110



Support-expansion population:



\- beneficial: 43

\- harmful: 6



Total harmful events across both blocks:



8



The low harmful-event count remains a major limitation.



\---



\## Threshold-Selection Rule



The threshold-selection procedure is applied independently within each training block.



Candidate thresholds are the observed values of:



`local\_error\_std`



within that block.



The historical selection rule is:



1\. Retain only thresholds achieving harmful recall of at least 80%.

2\. Among qualifying thresholds, choose the threshold with highest beneficial specificity.

3\. Break ties using higher harmful precision.

4\. If still tied, choose the higher threshold.



The selected threshold is then transferred unchanged to the opposite block.



The test block is never used to select its own threshold.



\---



\# Transfer Direction 1



\## Train on Block 071-090



Selected threshold:



\\\[

\\boxed{

\\tau\_{\\sigma}=0.054195542076

}

\\]



Training population:



\- harmful: 2

\- beneficial: 37



Training performance:



\- harmful recall: 100.000%

\- beneficial specificity: 51.351%

\- harmful precision: 10.000%

\- balanced accuracy: 75.676%

\- flagged fraction: 51.282%



\---



\## Transfer to Block 091-110



The threshold:



\\\[

0.054195542076

\\]



was applied unchanged to block 091-110.



Test population:



\- harmful: 6

\- beneficial: 43



Transferred performance:



\- harmful recall: 100.000%

\- beneficial specificity: 60.465%

\- harmful precision: 26.087%

\- balanced accuracy: 80.233%

\- flagged fraction: 46.939%



Confusion counts:



\- TP = 6

\- FP = 17

\- FN = 0

\- TN = 26



This transfer direction is favorable.



The threshold selected from block 071-090 captured every harmful support expansion in block 091-110.



\---



\# Transfer Direction 2



\## Train on Block 091-110



Selected threshold:



\\\[

\\boxed{

\\tau\_{\\sigma}=0.074718712972

}

\\]



Training population:



\- harmful: 6

\- beneficial: 43



Training performance:



\- harmful recall: 83.333%

\- beneficial specificity: 88.372%

\- harmful precision: 50.000%

\- balanced accuracy: 85.853%

\- flagged fraction: 20.408%



\---



\## Transfer to Block 071-090



The threshold:



\\\[

0.074718712972

\\]



was applied unchanged to block 071-090.



Test population:



\- harmful: 2

\- beneficial: 37



Transferred performance:



\- harmful recall: 50.000%

\- beneficial specificity: 81.081%

\- harmful precision: 12.500%

\- balanced accuracy: 65.541%

\- flagged fraction: 20.513%



Confusion counts:



\- TP = 1

\- FP = 7

\- FN = 1

\- TN = 30



This transfer direction fails the original 80% harmful-recall objective.



One of the two harmful events falls below the threshold learned from the opposite block.



\---



\# Threshold Stability



The independently selected thresholds are:



\\\[

0.054195542076

\\]



and:



\\\[

0.074718712972.

\\]



Mean threshold:



\\\[

0.064457127524

\\]



Threshold range:



\\\[

\[0.054195542076,\\ 0.074718712972]

\\]



Absolute difference:



\\\[

\\boxed{

0.020523170896

}

\\]



This difference is substantial relative to the scale of the feature itself.



Therefore, the historical operating points are not numerically stable across the two blocks.



\---



\# Transferred Performance Summary



Mean transferred harmful recall:



\\\[

75.000\\%

\\]



Minimum transferred harmful recall:



\\\[

\\boxed{50.000\\%}

\\]



Mean transferred beneficial specificity:



\\\[

70.773\\%

\\]



Minimum transferred specificity:



\\\[

60.465\\%

\\]



Mean transferred balanced accuracy:



\\\[

72.887\\%

\\]



Minimum transferred balanced accuracy:



\\\[

65.541\\%

\\]



The average performance remains useful, but the minimum transferred harmful recall is incompatible with a claim of stable safety-oriented threshold transfer.



\---



\# Local Sensitivity — Transfer 071-090 to 091-110



Around the transferred operating region, block 091-110 retains 100% harmful recall across a substantial range.



Observed thresholds and performance include:



\### Threshold 0.048421835492



\- harmful recall: 100.000%

\- specificity: 53.488%

\- precision: 23.077%

\- balanced accuracy: 76.744%



\### Threshold 0.054631655583



\- harmful recall: 100.000%

\- specificity: 60.465%

\- precision: 26.087%

\- balanced accuracy: 80.233%



\### Threshold 0.060492190920



\- harmful recall: 100.000%

\- specificity: 67.442%

\- precision: 30.000%

\- balanced accuracy: 83.721%



Thus, in block 091-110, the lower error-dispersion threshold region provides a favorable safety-specificity tradeoff.



\---



\# Local Sensitivity — Transfer 091-110 to 071-090



The opposite test block behaves differently.



Across nearby thresholds:



\### Threshold 0.065289038692



\- harmful recall: 50.000%

\- specificity: 75.676%



\### Threshold 0.075557486913



\- harmful recall: 50.000%

\- specificity: 81.081%



\### Threshold 0.082648976798



\- harmful recall: 50.000%

\- specificity: 91.892%



The harmful recall remains fixed at:



\\\[

\\boxed{50\\%}

\\]



throughout this local threshold region.



Therefore the failure is not simply the result of tiny numerical imprecision around one selected threshold.



The block contains one harmful event positioned materially below the operating region learned from block 091-110.



\---



\# Primary Finding



Experiment 107 demonstrates a distinction between:



\\\[

\\boxed{

\\text{ranking transfer}

}

\\]



and:



\\\[

\\boxed{

\\text{operating-point transfer}.

}

\\]



Experiment 106 showed that `local\_error\_std` preserves useful block-held-out ranking discrimination.



Experiment 107 shows that the corresponding absolute threshold does \*\*not\*\* transfer symmetrically.



One transfer direction achieves:



\\\[

100\\%

\\]



harmful recall.



The reverse direction achieves only:



\\\[

50\\%.

\\]



Therefore:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}

\\text{ appears more stable as a ranking representation}

\\atop

\\text{than as an absolute cross-regime threshold.}

}

\\]



\---



\# Why Threshold Averaging Is Not Justified



The two selected thresholds are:



\\\[

0.054195542076

\\]



and:



\\\[

0.074718712972.

\\]



It would be possible to calculate their arithmetic mean and propose an intermediate threshold.



Experiment 107 does not justify doing so.



Such a threshold would be constructed after observing both test blocks and would therefore be post hoc.



Additionally, only eight harmful events exist across the entire analysis population.



Thus, no averaged or compromise threshold may be described as historically validated based on Experiment 107.



\---



\# Relationship to Experiment 106



Experiment 106 found:



\\\[

\\boxed{

\\text{mean ROC AUC}=0.806

}

\\]



for `local\_error\_std` under reciprocal block-held-out validation.



Experiment 107 reveals why ROC AUC alone is insufficient for controller design.



A representation may order harmful events above beneficial events reasonably well while still experiencing enough scale or distribution shift that one absolute threshold fails to retain required harmful-event sensitivity across regimes.



Therefore:



\\\[

\\boxed{

\\text{good discrimination}

\\not\\Rightarrow

\\text{stable absolute operating point}.

}

\\]



\---



\# Emerging Regime-Shift Hypothesis



The asymmetric threshold transfer suggests that the distributional scale of:



`local\_error\_std`



may differ across regimes.



This raises a new representation-level hypothesis:



\*\*Relative error-dispersion position may be more transferable than raw absolute error dispersion.\*\*



For example, candidate representations might include:



\- historical percentile rank,

\- standardized deviation from a historical reference distribution,

\- block-independent empirical quantile,

\- or another scale-normalized measure.



Experiment 107 does not select among these possibilities.



It only motivates testing whether scale normalization improves cross-regime operating-point stability.



\---



\# What Experiment 107 Supports



Experiment 107 supports the claims that:



1\. `local\_error\_std` remains scientifically relevant as a second-stage ranking signal.



2\. One block-derived threshold transfers successfully in one direction.



3\. Threshold transfer is asymmetric.



4\. A single absolute raw threshold is not yet historically stable enough for prospective freezing.



5\. Operating-point validation must be separated from ranking validation.



\---



\# What Experiment 107 Does Not Support



Experiment 107 does not establish:



1\. a deployable threshold on `local\_error\_std`;



2\. that the mean of the two block thresholds should be used;



3\. that the higher or lower threshold should be selected prospectively;



4\. that the Experiment 101 controller should yet be modified;



5\. that raw error dispersion is scale-invariant across regimes;



6\. prospective generalization of an error-dispersion guard.



\---



\# Harmful-Event Scarcity



Only eight harmful events are available across both historical blocks.



One block contains only two.



Consequently, threshold estimates are highly sensitive to individual harmful events.



The transfer failure from block 091-110 to block 071-090 is caused by missing one of only two harmful events, which changes recall from 100% to 50%.



This does not make the failure unimportant.



Rather, it demonstrates how fragile an absolute threshold would currently be.



\---



\# Scientific Interpretation



Experiment 107 does not invalidate `local\_error\_std`.



Instead, it narrows what can currently be claimed about it.



The evidence now supports:



\\\[

\\boxed{

\\text{historical local calibration-error dispersion}

\\atop

\\text{contains block-generalizable ranking information}

}

\\]



but not yet:



\\\[

\\boxed{

\\text{one raw absolute error-dispersion threshold}

\\atop

\\text{generalizes reliably across regimes}.

}

\\]



This distinction should govern the next experiment.



\---



\# Next Research Question



The next analysis should test whether normalization of local calibration-error dispersion reduces the cross-block operating-point shift.



A suitable experiment should evaluate historical representations such as:



\- raw `local\_error\_std`,

\- within-reference percentile rank,

\- z-normalized error dispersion,

\- and potentially robust normalization using median and MAD.



The analysis should preserve block-held-out transfer.



The central question is:



\*\*Can a scale-normalized error-dispersion representation maintain the ranking value of local\_error\_std while producing a more stable operating point across historical regimes?\*\*



No prospective controller test should begin unless a normalized representation demonstrates improved historical transfer stability.



\---



\## Experiment 107 Status



Experiment 107: COMPLETE



Primary result:



\\\[

\\boxed{

\\text{absolute raw error-dispersion threshold transfer is asymmetric}

}

\\]



Transferred harmful recall:



\- direction 1: 100%

\- direction 2: 50%



Minimum transferred harmful recall:



\\\[

\\boxed{50\\%}

\\]



Conclusion:



\\\[

\\boxed{

\\text{raw } \\texttt{local\\\_error\\\_std}

\\text{ is not yet suitable for a frozen absolute controller threshold}.

}

\\]



No new controller threshold is defined.

