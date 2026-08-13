\# Experiment 108 — Scale-Normalized Error-Dispersion Transfer



\## Purpose



Experiment 107 showed that `local\_error\_std` retains useful cross-block ranking information but does not support a stable raw absolute operating threshold.



The asymmetric threshold-transfer result raised a specific representation-level hypothesis:



\*\*Perhaps the transfer failure is primarily caused by scale drift in raw local calibration-error dispersion, and a normalized representation could produce a more stable operating point across regimes.\*\*



Experiment 108 tests that hypothesis directly.



The central question is:



\*\*Can monotonic scale normalization of local calibration-error dispersion improve block-to-block operating-point transfer without changing the underlying ordering of support-expansion events?\*\*



Experiment 108 is a historical representation-transfer analysis.



It does not:



\- introduce new prospective seeds,

\- modify the controller,

\- define a deployable threshold,

\- or alter the Experiment 101 calibration-aware intervention.



\---



\## Historical Event Population



Experiment 108 uses the same already-consumed support-expansion population analyzed in Experiments 105-107.



Blocks:



\### Block 071-090



Seeds:



44071-44090



\### Block 091-110



Seeds:



44091-44110



Total event population:



\- beneficial support expansions: 80

\- harmful support expansions: 8



No new outcomes are generated.



\---



\# Representations Evaluated



Experiment 108 compares four representations of:



`local\_error\_std`



\## Raw



The original untransformed historical local calibration-error standard deviation.



\## Z-Score



The value is standardized using the training block mean and standard deviation:



\\\[

z

=

\\frac{x-\\mu\_{\\mathrm{train}}}

{\\sigma\_{\\mathrm{train}}}.

\\]



The normalization parameters are fitted using the training block only.



\---



\## Robust Z-Score



The value is standardized using the training block median and median absolute deviation:



\\\[

z\_{\\mathrm{robust}}

=

\\frac{x-\\mathrm{median}\_{\\mathrm{train}}}

{1.4826\\cdot\\mathrm{MAD}\_{\\mathrm{train}}}.

\\]



Again, the reference distribution is derived exclusively from the training block.



\---



\## Empirical Percentile



Each event is represented by its empirical percentile relative to the training-block distribution of `local\_error\_std`.



This transformation expresses the event's dispersion relative to the training reference distribution rather than in raw units.



\---



\# Validation Design



The Experiment 107 transfer design is preserved.



For each representation:



\### Transfer Direction 1



Train/select threshold on:



44071-44090



Apply unchanged to:



44091-44110



\### Transfer Direction 2



Train/select threshold on:



44091-44110



Apply unchanged to:



44071-44090



No evaluation block contributes to the normalization reference or threshold selection used to evaluate that block.



\---



\# Threshold-Selection Rule



For every representation, the training-block threshold is selected using the same historical rule:



1\. Retain thresholds with harmful recall of at least 80%.

2\. Maximize beneficial specificity.

3\. Break ties using higher harmful precision.

4\. If still tied, choose the higher threshold.



Thus, any difference in transfer performance must arise from the representation rather than from a changed operating-point selection procedure.



\---



\# Raw Representation



\## Transfer 071-090 to 091-110



Selected threshold:



\\\[

0.054195542076

\\]



Training:



\- harmful recall: 100.000%

\- specificity: 51.351%

\- balanced accuracy: 75.676%



Transferred test performance:



\- harmful recall: 100.000%

\- specificity: 60.465%

\- harmful precision: 26.087%

\- balanced accuracy: 80.233%



Confusion counts:



\- TP = 6

\- FP = 17

\- FN = 0

\- TN = 26



\---



\## Transfer 091-110 to 071-090



Selected threshold:



\\\[

0.074718712972

\\]



Training:



\- harmful recall: 83.333%

\- specificity: 88.372%

\- balanced accuracy: 85.853%



Transferred test performance:



\- harmful recall: 50.000%

\- specificity: 81.081%

\- harmful precision: 12.500%

\- balanced accuracy: 65.541%



Confusion counts:



\- TP = 1

\- FP = 7

\- FN = 1

\- TN = 30



This reproduces Experiment 107.



\---



\# Z-Score Representation



\## Transfer 071-090 to 091-110



Selected threshold:



\\\[

0.031795929788

\\]



Transferred test performance:



\- harmful recall: 100.000%

\- specificity: 60.465%

\- harmful precision: 26.087%

\- balanced accuracy: 80.233%



Confusion counts:



\- TP = 6

\- FP = 17

\- FN = 0

\- TN = 26



\---



\## Transfer 091-110 to 071-090



Selected threshold:



\\\[

0.875604669954

\\]



Transferred test performance:



\- harmful recall: 50.000%

\- specificity: 81.081%

\- harmful precision: 12.500%

\- balanced accuracy: 65.541%



Confusion counts:



\- TP = 1

\- FP = 7

\- FN = 1

\- TN = 30



The z-score transformation changes the numerical threshold scale but not the transferred decisions.



\---



\# Robust Z-Score Representation



\## Transfer 071-090 to 091-110



Selected threshold:



\\\[

0.000000000000

\\]



Transferred test performance:



\- harmful recall: 100.000%

\- specificity: 60.465%

\- harmful precision: 26.087%

\- balanced accuracy: 80.233%



Confusion counts:



\- TP = 6

\- FP = 17

\- FN = 0

\- TN = 26



\---



\## Transfer 091-110 to 071-090



Selected threshold:



\\\[

1.153535944025

\\]



Transferred test performance:



\- harmful recall: 50.000%

\- specificity: 81.081%

\- harmful precision: 12.500%

\- balanced accuracy: 65.541%



Confusion counts:



\- TP = 1

\- FP = 7

\- FN = 1

\- TN = 30



Again, the transferred classification behavior is identical to the raw representation.



\---



\# Percentile Representation



\## Transfer 071-090 to 091-110



Selected percentile threshold:



\\\[

\\boxed{0.500000}

\\]



Transferred test performance:



\- harmful recall: 100.000%

\- specificity: 60.465%

\- harmful precision: 26.087%

\- balanced accuracy: 80.233%



Confusion counts:



\- TP = 6

\- FP = 17

\- FN = 0

\- TN = 26



\---



\## Transfer 091-110 to 071-090



Selected percentile threshold:



\\\[

\\boxed{0.806122}

\\]



Transferred test performance:



\- harmful recall: 50.000%

\- specificity: 81.081%

\- harmful precision: 12.500%

\- balanced accuracy: 65.541%



Confusion counts:



\- TP = 1

\- FP = 7

\- FN = 1

\- TN = 30



The percentile representation is particularly informative because it removes raw numerical scale as an explanation.



The selected relative operating positions differ substantially:



\\\[

0.500000

\\]



versus:



\\\[

0.806122.

\\]



Thus, the cross-regime instability exists in event rank position itself.



\---



\# Representation Transfer Summary



All four representations produce identical transferred outcome metrics.



For every representation:



Mean transferred harmful recall:



\\\[

\\boxed{75.000\\%}

\\]



Minimum transferred harmful recall:



\\\[

\\boxed{50.000\\%}

\\]



Mean transferred specificity:



\\\[

\\boxed{70.773\\%}

\\]



Minimum transferred specificity:



\\\[

60.465\\%

\\]



Mean transferred balanced accuracy:



\\\[

\\boxed{72.887\\%}

\\]



Minimum transferred balanced accuracy:



\\\[

65.541\\%.

\\]



Therefore no evaluated normalization improves the transfer decision geometry.



\---



\# Why the Results Are Identical



Raw, z-score, robust z-score, and percentile transformations are monotonic with respect to the underlying `local\_error\_std` ordering under the reference construction used here.



Because the threshold-selection procedure also operates on observed transformed values, each representation selects an operating boundary corresponding to the same ordering structure in its training block.



Therefore the transformed threshold may have a different numerical value while inducing the same classification partition.



Experiment 108 confirms this empirically.



\---



\# Primary Falsification Result



The hypothesis tested by Experiment 108 was:



\\\[

\\boxed{

\\text{cross-block threshold failure may primarily reflect}

\\atop

\\text{raw-scale drift in local error dispersion}.

}

\\]



The result does not support that hypothesis.



All evaluated normalization methods preserve the same asymmetric transfer behavior.



Therefore:



\\\[

\\boxed{

\\text{simple monotonic scale normalization does not solve}

\\atop

\\text{the error-dispersion operating-point instability}.

}

\\]



\---



\# Percentile Evidence



The percentile result provides the strongest falsification of a simple scale-drift explanation.



If the regimes differed only because one produced numerically larger or smaller `local\_error\_std` values, expressing each event relative to a reference distribution might have aligned the operating point.



Instead, the selected training percentiles are:



\\\[

0.500000

\\]



and:



\\\[

0.806122.

\\]



This means the harmful-event decision boundary occupies materially different relative positions across the two historical regimes.



Thus:



\\\[

\\boxed{

\\text{the instability is not merely a units problem.}

}

\\]



\---



\# Relationship to Experiment 107



Experiment 107 established that:



\- raw ranking discrimination remains useful,

\- but the raw absolute threshold transfers asymmetrically.



Experiment 108 asks whether normalization repairs that asymmetry.



It does not.



The two experiments together support:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}

\\text{ is useful as a ranking signal}

}

\\]



but:



\\\[

\\boxed{

\\text{its intervention boundary is regime-dependent}

}

\\]



under the historical populations studied.



\---



\# Representation Versus Conditional Geometry



The remaining explanation is more fundamental than simple scale drift.



The harmful events appear to occupy different portions of the `local\_error\_std` distribution across regimes.



That suggests that the relationship between dispersion and harmful support expansion may depend on additional contextual conditions.



Possible explanations include interactions with:



\- support geometry,

\- predicted loss geometry,

\- transient state,

\- regime-specific model calibration,

\- action structure,

\- mismatch state,

\- anchor age,

\- or other contextual variables already identified in earlier experiments.



Experiment 108 does not select among these explanations.



\---



\# What Experiment 108 Supports



Experiment 108 supports the claims that:



1\. simple normalization does not improve historical error-dispersion threshold transfer;



2\. raw, z-score, robust-z, and percentile representations produce the same transferred decisions under the tested procedure;



3\. the operating-point instability survives removal of raw numerical scale;



4\. percentile operating points differ substantially across blocks;



5\. the remaining selectivity problem likely involves contextual regime dependence rather than simple scale normalization.



\---



\# What Experiment 108 Does Not Support



Experiment 108 does not establish:



1\. a normalized controller threshold;



2\. superiority of z-score, robust-z, or percentile representations;



3\. that any average transformed threshold should be used;



4\. that error dispersion should be abandoned as a ranking signal;



5\. a specific contextual interaction explaining the regime dependence;



6\. prospective generalization of any second-stage selector.



\---



\# Why Further Scalar Reparameterization Is Not the Priority



The experiment has now tested several natural monotonic reparameterizations of the same scalar signal.



Because all produce the same decisions, continued search over additional monotonic transformations would not address the underlying issue.



The research should therefore move from:



\\\[

\\text{How should error dispersion be rescaled?}

\\]



to:



\\\[

\\boxed{

\\text{Under what contextual conditions does error dispersion}

\\atop

\\text{become predictive of harmful adaptive expansion?}

}

\\]



This represents a shift from scalar operating-point optimization to conditional regime analysis.



\---



\# Harmful-Event Scarcity



Only eight harmful events remain available across the two historical blocks.



This limitation continues to constrain inference.



The Experiment 108 negative result is nevertheless informative because all four representations produce exactly the same event-level transfer decisions.



The falsification does not depend on subtle differences in estimated performance.



\---



\# Scientific Interpretation



Experiments 105-108 now support a layered conclusion:



\### Experiment 105



`local\_error\_std` is directionally stable across blocks.



\### Experiment 106



It retains useful reciprocal block-held-out ranking discrimination.



\### Experiment 107



Its raw absolute operating threshold is unstable across transfer directions.



\### Experiment 108



Simple scale normalization does not repair that operating-point instability.



Thus:



\\\[

\\boxed{

\\text{the signal is real enough to rank risk,}

\\atop

\\text{but incomplete as a context-free decision rule.}

}

\\]



That distinction should govern the next research phase.



\---



\## Experiment 108 Status



Experiment 108: COMPLETE



Primary result:



\\\[

\\boxed{

\\text{scale-normalized error-dispersion representations}

\\atop

\\text{do not improve block-to-block operating-point transfer}.

}

\\]



All representations produce:



\- mean transferred harmful recall: 75.000%

\- minimum transferred harmful recall: 50.000%

\- mean transferred specificity: 70.773%

\- mean transferred balanced accuracy: 72.887%



No normalized controller threshold is defined.



\---



\# Next Research Direction



The next experiment should investigate contextual conditions associated with the cross-block operating-point shift.



A useful next analysis should compare harmful and beneficial support expansions across blocks using contextual variables that may modify the meaning of `local\_error\_std`.



Candidate variables should come from already established controller and state representations rather than unrestricted feature fishing.



Potential candidates include:



\- `context\_support\_distance`

\- predicted loss

\- predicted risk

\- safety score

\- downside score

\- current mismatch indicator

\- anchor age

\- trigger score

\- release probability

\- and action identity or action transition geometry



The experiment should ask:



\*\*Which contextual variables explain why similar levels of historical calibration-error dispersion correspond to different harmful-expansion risk across regimes?\*\*



No new controller intervention should be introduced until that conditional regime structure is understood.

