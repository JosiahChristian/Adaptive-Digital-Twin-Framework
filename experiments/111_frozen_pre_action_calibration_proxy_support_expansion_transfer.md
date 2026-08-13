\# Experiment 111 — Frozen Pre-Action Calibration-Proxy Support-Expansion Transfer



\## Purpose



Experiment 110 established that impending calibration failure can be predicted from strictly pre-action historical state.



The strongest severe-underestimation representation was:



`expanded\_historical\_state`



with:



\\\[

\\text{pooled AUC}=0.769

\\]



and:



\\\[

\\text{mean leave-one-seed-out AUC}=0.748.

\\]



Experiment 110 also produced an out-of-fold predicted severe-underestimation probability for every historical action-context event.



Experiment 111 asks whether that frozen pre-action proxy transfers into the sparse support-expansion selectivity problem.



The central question is:



\*\*Does a frozen pre-action estimate of impending severe calibration failure distinguish harmful from beneficial support expansions more reliably than historical local error dispersion alone?\*\*



Experiment 111 is a transfer and falsification analysis.



It does not:



\- redefine the Experiment 110 proxy;

\- use support-expansion labels to select Experiment 110 features;

\- introduce new prospective seeds;

\- define a controller threshold;

\- or modify the adaptive controller.



\---



\# Frozen Proxy Source



Experiment 111 imports the previously generated out-of-fold predictions from Experiment 110.



The severe-underestimation proxy is:



`expanded\_historical\_state`



targeting:



`severe\_underestimate\_target`.



For every support-expansion event, Experiment 111 retrieves the Experiment 110 leave-one-seed-out prediction associated with the exact:



\- generation seed;

\- test index;

\- action.



Thus, the severe-underestimation representation is not retrained against harmful-versus-beneficial support-expansion outcomes.



\---



\# Signed Calibration-Error Proxy



Experiment 111 also imports the Experiment 110 signed-error regression output from:



`expanded\_historical\_regression`.



Because more negative predicted calibration error corresponds to greater predicted underestimation, Experiment 111 defines:



\\\[

\\text{predicted underestimation magnitude}

=

\-\\widehat{\\text{calibration error}}.

\\]



This sign reversal is determined from the calibration-error convention.



It is not learned from support-expansion labels.



\---



\# Support-Expansion Population



Experiment 111 uses the same historical support-expansion population established in Experiment 105.



Total labeled support expansions:



\\\[

88

\\]



Beneficial:



\\\[

80

\\]



Harmful:



\\\[

8\.

\\]



The two historical blocks are:



\## Block 071-090



Seeds:



44071-44090



\## Block 091-110



Seeds:



44091-44110



No new outcomes are generated.



\---



\# Frozen Raw Signal Geometry



\## Block 071-090



\### Local Error Standard Deviation



Beneficial mean:



\\\[

0.052755

\\]



Harmful mean:



\\\[

0.068422

\\]



Difference:



\\\[

+0.015667

\\]



Harmful-high rank AUC:



\\\[

0.716.

\\]



\---



\## Severe-Underestimation Probability



Beneficial mean:



\\\[

0.450462

\\]



Harmful mean:



\\\[

0.646221

\\]



Difference:



\\\[

\\boxed{+0.195759}

\\]



Harmful-high rank AUC:



\\\[

\\boxed{0.878}.

\\]



This is substantially stronger than local error dispersion within this block.



\---



\## Predicted Underestimation Magnitude



Beneficial mean:



\\\[

\-0.060344

\\]



Harmful mean:



\\\[

\-0.042519

\\]



Difference:



\\\[

+0.017825

\\]



Rank AUC:



\\\[

0.608.

\\]



The signed-error proxy therefore provides only modest ranking separation in this block.



\---



\# Block 091-110 Raw Geometry



\## Local Error Standard Deviation



Beneficial mean:



\\\[

0.052894

\\]



Harmful mean:



\\\[

0.083627

\\]



Difference:



\\\[

+0.030733

\\]



Rank AUC:



\\\[

0.895.

\\]



\---



\## Severe-Underestimation Probability



Beneficial mean:



\\\[

0.482027

\\]



Harmful mean:



\\\[

0.625962

\\]



Difference:



\\\[

\\boxed{+0.143936}

\\]



Rank AUC:



\\\[

\\boxed{0.764}.

\\]



The severe-underestimation proxy remains directionally useful, though it is weaker than `local\_error\_std` in this block.



\---



\## Predicted Underestimation Magnitude



Beneficial mean:



\\\[

\-0.050237

\\]



Harmful mean:



\\\[

\-0.025171

\\]



Difference:



\\\[

+0.025065

\\]



Rank AUC:



\\\[

0.717.

\\]



\---



\# Reciprocal Block-Held-Out Validation



Experiment 111 evaluates each support-expansion representation by training on one historical block and testing on the other, then reversing the direction.



The frozen proxy outputs themselves are not learned from support-expansion labels.



Only the small support-expansion comparison models are trained reciprocally by block.



\---



\# Error Dispersion Baseline



\## Held Out: Block 071-090



Balanced accuracy:



\\\[

64.189\\%

\\]



Harmful recall:



\\\[

50.000\\%

\\]



Specificity:



\\\[

78.378\\%

\\]



AUC:



\\\[

0.716.

\\]



Confusion counts:



\- TP = 1

\- FP = 8

\- FN = 1

\- TN = 29



\---



\## Held Out: Block 091-110



Balanced accuracy:



\\\[

83.721\\%

\\]



Harmful recall:



\\\[

100.000\\%

\\]



Specificity:



\\\[

67.442\\%

\\]



AUC:



\\\[

0.895.

\\]



Confusion counts:



\- TP = 6

\- FP = 14

\- FN = 0

\- TN = 29



\---



\## Error-Dispersion Summary



Mean AUC:



\\\[

\\boxed{0.806}

\\]



Minimum AUC:



\\\[

0.716

\\]



Mean balanced accuracy:



\\\[

73.955\\%

\\]



Mean harmful recall:



\\\[

75.000\\%.

\\]



This reproduces Experiment 106.



\---



\# Frozen Severe-Underestimation Proxy



\## Held Out: Block 071-090



Balanced accuracy:



\\\[

\\boxed{81.081\\%}

\\]



Harmful recall:



\\\[

\\boxed{100.000\\%}

\\]



Specificity:



\\\[

62.162\\%

\\]



AUC:



\\\[

\\boxed{0.878}

\\]



Confusion counts:



\- TP = 2

\- FP = 14

\- FN = 0

\- TN = 23



\---



\## Held Out: Block 091-110



Balanced accuracy:



\\\[

65.891\\%

\\]



Harmful recall:



\\\[

66.667\\%

\\]



Specificity:



\\\[

65.116\\%

\\]



AUC:



\\\[

\\boxed{0.764}

\\]



Confusion counts:



\- TP = 4

\- FP = 15

\- FN = 2

\- TN = 28



\---



\## Severe-Proxy Summary



Mean AUC:



\\\[

\\boxed{0.821}

\\]



Minimum AUC:



\\\[

\\boxed{0.764}

\\]



Mean balanced accuracy:



\\\[

73.486\\%

\\]



Minimum balanced accuracy:



\\\[

65.891\\%

\\]



Mean harmful recall:



\\\[

\\boxed{83.333\\%}

\\]



Minimum harmful recall:



\\\[

66.667\\%

\\]



Mean specificity:



\\\[

63.639\\%.

\\]



The severe-underestimation proxy therefore produces the best mean reciprocal AUC among the tested representations.



\---



\# Value-Add Versus Error Dispersion



The primary comparison is:



\### Error Dispersion



\\\[

\\text{mean AUC}=0.806

\\]



\### Frozen Severe Proxy



\\\[

\\text{mean AUC}=0.821.

\\]



Therefore:



\\\[

\\boxed{

\\Delta\\text{mean AUC}=+0.015.

}

\\]



The improvement in minimum AUC is larger:



\\\[

0.716

\\rightarrow

0.764,

\\]



or:



\\\[

\\boxed{

\\Delta\\text{minimum AUC}=+0.048.

}

\\]



This improvement in the weaker block is scientifically important because prior experiments identified cross-regime instability as the central problem.



\---



\# Frozen Severe-Proxy Coefficient Stability



The reciprocal support-expansion classifier coefficient on:



`severe\_underestimation\_probability`



has mean standardized value:



\\\[

\\boxed{+1.316}

\\]



with:



\\\[

\\boxed{100\\%\\text{ sign stability}}.

\\]



Thus higher frozen pre-action probability of severe consequence underestimation is associated with harmful support expansion in both reciprocal fits.



\---



\# Signed-Error Proxy Alone



The signed-error proxy does not transfer as effectively.



Mean AUC:



\\\[

0.663

\\]



Minimum AUC:



\\\[

0.608.

\\]



Relative to error dispersion:



\\\[

\\boxed{

\\Delta\\text{mean AUC}=-0.143.

}

\\]



Therefore the continuous Experiment 110 signed-error regression does not provide the strongest support-expansion bridge.



The severe-underestimation classification proxy is clearly more effective for this purpose.



\---



\# Error Dispersion Plus Severe Proxy



The combined model achieves:



\\\[

\\text{mean AUC}=0.771

\\]



with minimum AUC:



\\\[

0.716.

\\]



This is worse than either:



\- the severe proxy alone;

\- or error dispersion alone on mean AUC.



Therefore adding raw local error dispersion to the severe proxy does not provide demonstrated incremental value.



\---



\# Error Dispersion Plus Signed-Error Proxy



This combination produces:



\\\[

\\text{mean AUC}=0.818

\\]



with:



\\\[

\\text{minimum AUC}=0.757.

\\]



This slightly exceeds error dispersion alone on mean AUC and improves its weaker held-out AUC.



However, it remains below the severe proxy alone on mean AUC:



\\\[

0.818 < 0.821.

\\]



Its mean harmful recall is:



\\\[

75.000\\%.

\\]



Thus it does not replace the frozen severe proxy as the strongest current transfer representation.



\---



\# Two Frozen Proxies



Combining:



\- severe-underestimation probability;

\- predicted underestimation magnitude



produces:



\\\[

\\text{mean AUC}=0.771

\\]



and:



\\\[

\\text{minimum AUC}=0.770.

\\]



Although the minimum AUC is highly balanced across the two blocks, classification performance is weaker:



\\\[

\\text{mean harmful recall}=58.333\\%.

\\]



This representation is therefore not favored.



\---



\# Error Dispersion Plus Both Proxies



The three-variable model produces:



\\\[

\\text{mean AUC}=0.767

\\]



with:



\\\[

\\text{minimum AUC}=0.743.

\\]



No evidence supports the additional complexity.



\---



\# Primary Finding



The strongest support-expansion transfer model is:



\\\[

\\boxed{

\\texttt{severe\\\_proxy\\\_only}.

}

\\]



Its reciprocal performance is:



\\\[

\\boxed{

\\text{mean AUC}=0.821

}

\\]



\\\[

\\boxed{

\\text{minimum AUC}=0.764

}

\\]



\\\[

\\boxed{

\\text{mean harmful recall}=83.333\\%.

}

\\]



Compared with error dispersion alone:



\\\[

\\boxed{

\\Delta\\text{mean AUC}=+0.015.

}

\\]



Thus the frozen Experiment 110 pre-action severe-underestimation representation carries transferable information about harmful support expansion.



\---



\# Why This Result Matters



Experiment 111 provides the first direct transfer from the broad calibration-error representation problem back into the sparse controller-selectivity problem.



The experimental chain is now:



\\\[

\\text{Experiment 109}

\\]



identified realized consequence underestimation as a powerful retrospective explanatory variable.



\\\[

\\Downarrow

\\]



\\\[

\\text{Experiment 110}

\\]



showed that impending severe underestimation is partly predictable from pre-action historical state.



\\\[

\\Downarrow

\\]



\\\[

\\text{Experiment 111}

\\]



shows that this frozen pre-action proxy retains harmful-versus-beneficial support-expansion information.



Therefore:



\\\[

\\boxed{

\\text{pre-action calibration-failure estimation}

\\atop

\\text{is relevant to controller selectivity.}

}

\\]



\---



\# Representation Independence



The Experiment 110 severe proxy was not selected using the eight harmful support-expansion outcomes.



It was developed on the much larger historical action-context calibration-error population.



Experiment 111 then evaluates its transfer onto support expansions.



This separation reduces the risk that the representation is merely overfit to the sparse harmful-expansion sample.



\---



\# Important Negative Result



The best result is not a more complicated joint classifier.



Instead:



\\\[

\\boxed{

\\text{the frozen severe-underestimation proxy alone}

}

\\]



performs best on mean AUC.



This suggests that the proxy is already compressing much of the historical calibration-state information relevant to harmful support expansion.



Adding raw error dispersion does not improve transfer.



\---



\# Remaining Regime Dependence



The result is improved but not regime-invariant.



Held-out AUC values are:



\\\[

0.878

\\]



and:



\\\[

0.764.

\\]



Harmful recall is:



\\\[

100\\%

\\]



and:



\\\[

66.667\\%.

\\]



Thus:



\\\[

\\boxed{

\\text{the proxy improves balance across blocks}

\\atop

\\text{but does not eliminate regime dependence.}

}

\\]



This remains an important limitation.



\---



\# Harmful-Event Scarcity



Only eight harmful support expansions are available:



\- two in one block;

\- six in the other.



Therefore the positive result remains provisional.



A single missed harmful event in the two-event block changes recall by 50 percentage points.



Accordingly, Experiment 111 should not be treated as sufficient evidence for controller deployment.



\---



\# What Experiment 111 Supports



Experiment 111 supports the claims that:



1\. the frozen Experiment 110 severe-underestimation proxy transfers into support-expansion selectivity;



2\. higher predicted severe-underestimation probability is associated with harmful expansion in both historical blocks;



3\. the severe proxy slightly outperforms `local\_error\_std` on mean reciprocal AUC;



4\. it materially improves the minimum held-out AUC relative to error dispersion;



5\. the signed-error proxy is weaker for support-expansion discrimination;



6\. combining the severe proxy with error dispersion does not improve mean AUC;



7\. pre-action calibration-failure estimation is therefore a plausible second-stage controller representation.



\---



\# What Experiment 111 Does Not Support



Experiment 111 does not establish:



1\. a controller threshold on severe-underestimation probability;



2\. stable operating-point transfer;



3\. prospective controller improvement;



4\. sufficient harmful-event sample size;



5\. that the severe proxy is fully regime invariant;



6\. that the Experiment 101 selectivity problem is solved;



7\. authorization to modify the controller.



\---



\# Experiment 111 Status



Experiment 111: COMPLETE



Best support-expansion transfer representation:



\\\[

\\boxed{

\\texttt{severe\\\_proxy\\\_only}

}

\\]



Performance:



\\\[

\\boxed{

\\text{mean AUC}=0.821

}

\\]



\\\[

\\boxed{

\\text{minimum AUC}=0.764

}

\\]



\\\[

\\boxed{

\\text{mean harmful recall}=83.333\\%

}

\\]



Relative mean-AUC improvement over `local\_error\_std`:



\\\[

\\boxed{

+0.015.

}

\\]



No controller threshold is defined.



\---



\# Next Research Direction



The next experiment should test whether a historical operating point on the frozen severe-underestimation probability transfers more stably than the raw `local\_error\_std` threshold tested in Experiment 107.



The threshold-selection procedure should preserve the same safety-oriented rule used previously:



\- require a minimum harmful-recall level on the training block;

\- maximize beneficial preservation among qualifying thresholds;

\- freeze the selected threshold;

\- evaluate it unchanged on the opposite block;

\- then reverse the transfer direction.



The primary comparison should be against Experiment 107.



The central question is:



\*\*Does the frozen pre-action severe-underestimation probability support a more stable cross-block intervention operating point than historical error dispersion alone?\*\*



Only if the proxy demonstrates materially better operating-point transfer should another prospective controller experiment be considered.

