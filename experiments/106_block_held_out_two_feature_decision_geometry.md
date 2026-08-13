\# Experiment 106 — Block-Held-Out Two-Feature Decision Geometry



\## Purpose



Experiment 105 identified two historical calibration-state variables with harmful-higher direction stability across both analyzed support-expansion blocks:



\- `local\_error\_std`

\- `local\_underestimate\_fraction`



Both variables showed 100% harmful-higher direction stability across:



\- block `44071-44090`

\- block `44091-44110`



However, cross-block univariate stability does not establish that the two signals provide complementary information.



Experiment 106 therefore tests whether the two variables jointly improve harmful-versus-beneficial support-expansion discrimination under strict block-held-out validation.



The central question is:



\*\*Does combining local calibration-error dispersion with ordinary historical underestimation frequency improve block-generalizable harmful-expansion discrimination beyond either feature alone?\*\*



Experiment 106 is a historical decision-geometry analysis.



It does not:



\- introduce new prospective seeds,

\- modify the controller,

\- define an intervention threshold,

\- or propose a new safety rule.



\---



\## Historical Event Population



Experiment 106 reuses the support-expansion event population reconstructed in Experiment 105.



Total labeled support-expansion events:



88



Beneficial:



80



Harmful:



8



The two historical blocks are:



\### Block 071-090



Seeds:



44071-44090



\### Block 091-110



Seeds:



44091-44110



\---



\## Validation Design



Experiment 106 uses reciprocal block-held-out validation.



\### Fold 1



Train on:



44091-44110



Test on:



44071-44090



\### Fold 2



Train on:



44071-44090



Test on:



44091-44110



Therefore, neither block is evaluated by a model trained on its own events.



This is stricter than pooled fitting and is intended to expose regime-specific decision boundaries.



\---



\## Candidate Models



Four compact models were evaluated.



\### Error Dispersion Only



Feature:



`local\_error\_std`



\### Underestimation Fraction Only



Feature:



`local\_underestimate\_fraction`



\### Two-Feature Compact



Features:



\- `local\_error\_std`

\- `local\_underestimate\_fraction`



\### Two-Feature Interaction



Features:



\- `local\_error\_std`

\- `local\_underestimate\_fraction`

\- `local\_error\_std \* local\_underestimate\_fraction`



All models use standardized logistic regression with balanced class weighting.



The classification threshold of 0.50 is used only for descriptive metrics.



It is not a proposed controller threshold.



\---



\# Block-Held-Out Performance



\## Error Dispersion Only



\### Held Out: Block 071-090



Training harmful events:



6



Test harmful events:



2



Balanced accuracy:



64.189%



Harmful recall:



50.000%



Harmful precision:



11.111%



Beneficial specificity:



78.378%



ROC AUC:



\\\[

\\boxed{0.716}

\\]



Confusion counts:



\- TP = 1

\- FP = 8

\- FN = 1

\- TN = 29



\### Held Out: Block 091-110



Training harmful events:



2



Test harmful events:



6



Balanced accuracy:



83.721%



Harmful recall:



100.000%



Harmful precision:



30.000%



Beneficial specificity:



67.442%



ROC AUC:



\\\[

\\boxed{0.895}

\\]



Confusion counts:



\- TP = 6

\- FP = 14

\- FN = 0

\- TN = 29



\### Summary



Mean balanced accuracy:



\\\[

\\boxed{73.955\\%}

\\]



Minimum balanced accuracy:



\\\[

64.189\\%

\\]



Mean harmful recall:



\\\[

\\boxed{75.000\\%}

\\]



Mean beneficial specificity:



\\\[

72.910\\%

\\]



Mean ROC AUC:



\\\[

\\boxed{0.806}

\\]



Minimum ROC AUC:



\\\[

\\boxed{0.716}

\\]



This is the strongest overall block-held-out result.



\---



\## Underestimation Fraction Only



\### Held Out: Block 071-090



Balanced accuracy:



64.189%



Harmful recall:



50.000%



Beneficial specificity:



78.378%



ROC AUC:



0.791



\### Held Out: Block 091-110



Balanced accuracy:



73.062%



Harmful recall:



83.333%



Beneficial specificity:



62.791%



ROC AUC:



0.752



\### Summary



Mean balanced accuracy:



68.626%



Minimum balanced accuracy:



64.189%



Mean harmful recall:



66.667%



Mean specificity:



70.585%



Mean ROC AUC:



\\\[

0.771

\\]



Minimum ROC AUC:



\\\[

0.752

\\]



This feature remains individually useful, but it underperforms `local\_error\_std` on mean AUC and mean balanced accuracy.



\---



\## Two-Feature Compact Model



\### Held Out: Block 071-090



Balanced accuracy:



64.189%



Harmful recall:



50.000%



Beneficial specificity:



78.378%



ROC AUC:



0.716



\### Held Out: Block 091-110



Balanced accuracy:



74.225%



Harmful recall:



83.333%



Beneficial specificity:



65.116%



ROC AUC:



0.826



\### Summary



Mean balanced accuracy:



69.207%



Minimum balanced accuracy:



64.189%



Mean harmful recall:



66.667%



Mean beneficial specificity:



71.747%



Mean ROC AUC:



\\\[

0.771

\\]



Minimum ROC AUC:



\\\[

0.716

\\]



The two-feature compact model therefore does not outperform `local\_error\_std` alone.



\---



\## Two-Feature Interaction Model



\### Held Out: Block 071-090



Balanced accuracy:



64.189%



Harmful recall:



50.000%



Beneficial specificity:



78.378%



ROC AUC:



0.716



\### Held Out: Block 091-110



Balanced accuracy:



74.225%



Harmful recall:



83.333%



Beneficial specificity:



65.116%



ROC AUC:



0.826



\### Summary



Mean balanced accuracy:



69.207%



Minimum balanced accuracy:



64.189%



Mean harmful recall:



66.667%



Mean specificity:



71.747%



Mean ROC AUC:



\\\[

0.771

\\]



The interaction model produces no improvement over the simpler two-feature compact model.



\---



\# Coefficient Stability



\## Error Dispersion Only



`local\_error\_std`



Mean standardized coefficient:



\\\[

\\boxed{+1.201}

\\]



Mean absolute coefficient:



1.201



Sign stability:



\\\[

\\boxed{100\\%}

\\]



The harmful-higher orientation remains stable in both block-held-out fits.



\---



\## Underestimation Fraction Only



`local\_underestimate\_fraction`



Mean coefficient:



\\\[

+0.948

\\]



Sign stability:



\\\[

100\\%

\\]



This confirms the univariate cross-block directional stability observed in Experiment 105.



\---



\## Two-Feature Compact Model



\### local\_error\_std



Mean coefficient:



\\\[

\\boxed{+1.258}

\\]



Sign stability:



\\\[

\\boxed{100\\%}

\\]



\### local\_underestimate\_fraction



Mean coefficient:



\\\[

+0.444

\\]



Sign stability:



\\\[

\\boxed{50\\%}

\\]



This is an important result.



Once `local\_error\_std` is included in the model, the coefficient direction of `local\_underestimate\_fraction` is no longer stable across blocks.



Therefore, the latter variable does not provide robust incremental information in the joint representation.



\---



\## Interaction Model



\### local\_error\_std



Mean coefficient:



+1.219



Sign stability:



100%



\### local\_underestimate\_fraction



Mean coefficient:



+0.367



Sign stability:



50%



\### Interaction Term



Mean coefficient:



+0.116



Sign stability:



100%



Although the interaction term remains positive across both fits, adding it does not improve block-held-out predictive performance.



Thus, interaction complexity is not supported by the present evidence.



\---



\# Two-Feature Value-Add Test



The primary comparison is whether adding `local\_underestimate\_fraction` to `local\_error\_std` improves generalization.



Mean ROC AUC:



\### Error Dispersion Only



\\\[

\\boxed{0.806}

\\]



\### Underestimation Fraction Only



\\\[

0.771

\\]



\### Two-Feature Compact



\\\[

0.771

\\]



Therefore:



\\\[

\\Delta\\mathrm{AUC}\_{\\text{compact-error std}}

=

\\boxed{-0.035}

\\]



and:



\\\[

\\Delta\\mathrm{AUC}\_{\\text{compact-underestimate}}

=

0.000.

\\]



The two-feature representation does \*\*not\*\* provide positive incremental value relative to error dispersion alone.



\---



\# Primary Finding



Experiment 106 identifies:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}

}

\\]



as the strongest compact block-generalizable constituent representation among the models tested.



Its block-held-out performance is:



\\\[

\\boxed{

\\text{mean ROC AUC}=0.806

}

\\]



with:



\\\[

\\boxed{

\\text{minimum ROC AUC}=0.716

}

\\]



and:



\\\[

\\boxed{

100\\%\\text{ coefficient sign stability}.

}

\\]



The two-feature combination does not improve performance.



Thus, the current evidence favors a simpler representation:



\\\[

\\boxed{

\\text{historical local calibration-error dispersion}

}

\\]



rather than a two-variable decision boundary.



\---



\# Relationship to Experiment 105



Experiment 105 showed that both:



\- `local\_error\_std`

\- `local\_underestimate\_fraction`



were harmful-higher in both analyzed blocks.



Experiment 106 adds an important distinction.



Directional stability alone does not imply complementary predictive value.



When both variables are modeled jointly:



\- `local\_error\_std` remains coefficient-stable,

\- `local\_underestimate\_fraction` becomes coefficient-unstable,

\- and overall discrimination decreases relative to `local\_error\_std` alone.



Therefore the more defensible interpretation is:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}

\\text{ carries the dominant block-generalizable signal.}

}

\\]



\---



\# Simplification Result



Experiment 106 performs an important model-selection simplification.



The research trajectory does not need to move toward a larger and more complicated second-stage selector simply because several constituent variables have individually shown useful effects.



The evidence instead supports reducing the candidate representation to one variable.



This is methodologically useful because a one-dimensional selector is:



\- easier to interpret,

\- easier to falsify,

\- easier to calibrate,

\- less vulnerable to overfitting,

\- and easier to validate prospectively.



\---



\# Block Asymmetry



Performance differs substantially between the two holdout directions.



AUC values for `local\_error\_std` are:



\\\[

0.716

\\]



and:



\\\[

0.895.

\\]



This indicates meaningful regime dependence in effect strength even though direction remains stable.



Therefore:



\\\[

\\boxed{

\\text{directional stability}

\\neq

\\text{constant effect magnitude}.

}

\\]



Any future operating-point analysis must preserve block structure rather than optimize only pooled performance.



\---



\# Harmful-Event Scarcity



Only:



\\\[

8

\\]



harmful events exist across the complete Experiment 106 population.



The reciprocal training folds therefore contain only:



\- 6 harmful events in one training direction,

\- 2 harmful events in the other.



This is extremely small for classifier estimation.



Accordingly, the positive block-held-out results remain provisional.



Experiment 106 does not establish a deployable selector.



\---



\# What Experiment 106 Supports



Experiment 106 supports the claim that:



1\. `local\_error\_std` retains useful harmful-versus-beneficial discrimination under reciprocal block-held-out validation.



2\. Its coefficient direction is stable across both training directions.



3\. The two-feature representation does not improve generalization.



4\. `local\_underestimate\_fraction` does not provide stable incremental value once error dispersion is modeled.



5\. A simpler one-dimensional decision geometry is currently better supported than a more complex constituent model.



\---



\# What Experiment 106 Does Not Support



Experiment 106 does not establish:



1\. a controller threshold on `local\_error\_std`;



2\. prospective generalization to an untouched future block;



3\. causal interpretation of error dispersion;



4\. sufficient statistical power for final validation;



5\. that the Experiment 101 selectivity cost has been solved;



6\. that the calibration-aware controller should yet be modified.



\---



\# Current Best Second-Stage Candidate



The strongest current historical second-stage candidate is:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}.

}

\\]



Conceptually, this represents the dispersion of historical consequence-model calibration error in the local action-context neighborhood.



The emerging hypothesis is:



\\\[

\\boxed{

\\text{greater historical calibration instability}

\\Rightarrow

\\text{greater risk that a support-admitted expansion is harmful}.

}

\\]



This hypothesis has now survived:



\- Experiment 103 discovery,

\- Experiment 104 directional replication,

\- Experiment 105 cross-block stability,

\- and Experiment 106 reciprocal block-held-out discrimination.



It has not yet been prospectively validated as a controller selector.



\---



\# Next Research Question



The next experiment should determine whether a historical operating point can be defined for `local\_error\_std` without exploiting pooled information across the same block used for evaluation.



A suitable next analysis should examine:



\- block-specific threshold geometry,

\- threshold transfer from one block to the other,

\- harmful recall,

\- beneficial preservation,

\- operating-point sensitivity,

\- and whether any threshold region is stable enough to freeze prospectively.



No new controller intervention should be run until such threshold-transfer evidence exists.



The next question is therefore:



\*\*Can a threshold on historical local calibration-error dispersion transfer between historical blocks while retaining harmful-event sensitivity and materially improving beneficial-expansion preservation?\*\*



\---



\## Experiment 106 Status



Experiment 106: COMPLETE



Best block-held-out model:



\\\[

\\boxed{

\\texttt{error\\\_std\\\_only}

}

\\]



Mean ROC AUC:



\\\[

\\boxed{0.806}

\\]



Minimum ROC AUC:



\\\[

\\boxed{0.716}

\\]



Mean balanced accuracy:



\\\[

\\boxed{73.955\\%}

\\]



Mean harmful recall:



\\\[

\\boxed{75.000\\%}

\\]



Two-feature value-add:



\\\[

\\boxed{\\text{not supported}}

\\]



No controller threshold or intervention is defined.

