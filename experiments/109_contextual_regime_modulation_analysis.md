\# Experiment 109 — Contextual Regime Modulation Analysis



\## Purpose



Experiments 105-108 established an increasingly specific result concerning historical calibration-error dispersion.



Experiment 105 showed that `local\_error\_std` is directionally stable across two historical support-expansion blocks.



Experiment 106 showed that it retains useful reciprocal block-held-out discrimination.



Experiment 107 showed that an absolute operating threshold transfers asymmetrically.



Experiment 108 then falsified the hypothesis that this instability is primarily a raw-scale problem: raw, z-score, robust-z, and percentile representations produced identical transferred decisions.



The remaining question is therefore contextual:



\*\*Does the meaning of `local\_error\_std` depend on another state variable that differs across regimes?\*\*



Experiment 109 tests a deliberately restricted set of contextual candidates rather than conducting unrestricted feature search.



The primary objective is explanatory.



No controller rule, threshold, or new prospective intervention is introduced.



\---



\# Historical Population



Experiment 109 uses the same already-consumed support-expansion event population used in Experiments 105-108.



Historical blocks:



\## Block 071-090



Seeds:



44071-44090



\## Block 091-110



Seeds:



44091-44110



Combined population:



\- total support-expansion events: 88

\- beneficial expansions: 80

\- harmful expansions: 8



No new seeds or outcomes are generated.



\---



\# Base Signal



The baseline representation is:



`local\_error\_std`



Experiment 106 previously established reciprocal block-held-out performance of approximately:



\\\[

\\text{mean AUC}=0.806

\\]



with:



\\\[

\\text{minimum AUC}=0.716.

\\]



Experiment 109 treats this as the contextual-model baseline.



\---



\# Predefined Context Candidates



Three contextual quantities are evaluated.



\## Context Support Distance



`context\_support\_distance`



This is available before the action consequence is observed and is therefore potentially deployable.



It represents contextual support geometry surrounding the candidate action.



\---



\## Predicted Baseline Action Loss



`predicted\_baseline\_action\_loss`



This is also available before the realized consequence is observed and is therefore potentially deployable.



It represents the model's predicted loss associated with the baseline action.



\---



\## Baseline Action Loss Error



`baseline\_action\_loss\_error`



This variable is fundamentally different.



It represents realized prediction error associated with the action outcome.



It is therefore available only after the consequence has been observed.



Accordingly:



\\\[

\\boxed{

\\texttt{baseline\\\_action\\\_loss\\\_error}

\\text{ is retrospective outcome information.}

}

\\]



It is included only as an explanatory diagnostic.



It is not an eligible controller feature.



\---



\# Models Evaluated



The following reciprocal block-held-out models were evaluated:



1\. `local\_error\_std` alone;



2\. `local\_error\_std + context\_support\_distance`;



3\. `local\_error\_std + predicted\_baseline\_action\_loss`;



4\. `local\_error\_std + baseline\_action\_loss\_error`;



5\. each corresponding interaction model including:



\\\[

\\texttt{local\\\_error\\\_std}

\\times

\\texttt{context}.

\\]



Each model is trained entirely on one historical block and evaluated on the opposite block.



The procedure is then reversed.



\---



\# Baseline Performance



For:



`error\_std\_only`



the reciprocal block-held-out result is:



\\\[

\\boxed{

\\text{mean AUC}=0.806

}

\\]



and:



\\\[

\\boxed{

\\text{minimum AUC}=0.716.

}

\\]



The coefficient on `local\_error\_std` is:



\\\[

+1.201

\\]



with:



\\\[

\\boxed{

100\\% \\text{ sign stability}.

}

\\]



This reproduces the earlier finding that larger local calibration-error dispersion is consistently associated with harmful support expansion.



\---



\# Context Support Distance



The additive model:



`error\_std\_plus\_context\_support\_distance`



produces:



\\\[

\\text{mean AUC}=0.602

\\]



and:



\\\[

\\text{minimum AUC}=0.570.

\\]



Relative to the error-dispersion baseline:



\\\[

\\Delta\\text{mean AUC}=-0.203

\\]



and:



\\\[

\\Delta\\text{minimum AUC}=-0.146.

\\]



The context-support-distance coefficient has only:



\\\[

50\\%

\\]



sign stability across the reciprocal block fits.



Thus context support distance does not provide stable incremental discrimination in this experiment.



The interaction model performs similarly poorly:



\\\[

\\text{mean AUC}=0.596

\\]



with:



\\\[

\\text{minimum AUC}=0.570.

\\]



Therefore:



\\\[

\\boxed{

\\text{context support distance does not explain the}

\\atop

\\text{cross-block modulation of error dispersion here.}

}

\\]



\---



\# Predicted Baseline Action Loss



The additive model:



`error\_std\_plus\_predicted\_baseline\_action\_loss`



produces:



\\\[

\\text{mean AUC}=0.765

\\]



and:



\\\[

\\text{minimum AUC}=0.635.

\\]



Relative to the baseline:



\\\[

\\Delta\\text{mean AUC}=-0.041

\\]



and:



\\\[

\\Delta\\text{minimum AUC}=-0.081.

\\]



The predicted-loss coefficient in the additive model has only:



\\\[

50\\%

\\]



sign stability.



Thus adding predicted baseline action loss does not improve reciprocal block generalization.



\---



\# Predicted-Loss Interaction



The interaction model:



`error\_std\_x\_predicted\_baseline\_action\_loss`



produces:



\\\[

\\text{mean AUC}=0.802

\\]



and:



\\\[

\\text{minimum AUC}=0.716.

\\]



Relative to the error-dispersion baseline:



\\\[

\\Delta\\text{mean AUC}=-0.004

\\]



and:



\\\[

\\Delta\\text{minimum AUC}=0.000.

\\]



This is effectively comparable to the baseline but does not demonstrate incremental value.



Its coefficients are directionally stable in this small historical sample:



\- `local\_error\_std`: positive

\- predicted baseline action loss: negative

\- interaction: positive



However, the held-out discrimination does not improve.



Therefore coefficient structure alone is insufficient evidence for a useful contextual modifier.



\---



\# Retrospective Outcome-Error Result



The strongest result occurs when `baseline\_action\_loss\_error` is added.



The additive model:



`error\_std\_plus\_baseline\_action\_loss\_error`



produces:



\\\[

\\boxed{

\\text{mean AUC}=0.994

}

\\]



with:



\\\[

\\boxed{

\\text{minimum AUC}=0.988

}

\\]



and maximum AUC:



\\\[

1.000.

\\]



Relative to `local\_error\_std` alone:



\\\[

\\boxed{

\\Delta\\text{mean AUC}=+0.188

}

\\]



and:



\\\[

\\boxed{

\\Delta\\text{minimum AUC}=+0.272.

}

\\]



This is by far the largest observed contextual value-add.



\---



\# Outcome-Error Coefficient Structure



For the additive outcome-error model:



`local\_error\_std` has mean coefficient:



\\\[

+0.732

\\]



with 100% sign stability.



`baseline\_action\_loss\_error` has mean coefficient:



\\\[

\\boxed{-1.627}

\\]



with:



\\\[

\\boxed{

100\\% \\text{ sign stability}.

}

\\]



Thus the reciprocal block fits consistently associate harmful expansion with:



1\. larger historical local calibration-error dispersion; and

2\. more negative realized baseline action loss error.



Under the experiment's error convention, this is consistent with realized action loss being worse than predicted.



Conceptually:



\\\[

\\boxed{

\\text{historical calibration instability}

\+

\\text{realized consequence underestimation}

\\rightarrow

\\text{harmful expansion risk}.

}

\\]



This is an explanatory relationship.



It is not yet a usable pre-action decision rule.



\---



\# Outcome-Error Interaction



The interaction model:



`error\_std\_x\_baseline\_action\_loss\_error`



also produces:



\\\[

\\text{mean AUC}=0.994

\\]



and:



\\\[

\\text{minimum AUC}=0.988.

\\]



Therefore adding the explicit interaction does not improve discrimination beyond the additive outcome-error model.



The interaction coefficient itself is negative and 100% sign-stable:



\\\[

\-1.141.

\\]



But because the simpler additive model already reaches the same reciprocal block-held-out AUC, the interaction provides no demonstrated discriminatory value-add.



\---



\# Critical Temporal Validity Constraint



The near-perfect outcome-error result must not be misinterpreted.



`baseline\_action\_loss\_error` cannot be known before the candidate action consequence occurs.



Therefore it would constitute temporal leakage if used as an input to a pre-action controller.



Consequently:



\\\[

\\boxed{

\\text{AUC}=0.994

\\neq

\\text{deployable pre-action prediction}.

}

\\]



The result instead identifies an explanatory target.



It says that realized prediction error contains almost all of the additional information required to separate harmful from beneficial support expansions in these historical blocks.



That is scientifically useful because it tells the next research phase what must be approximated \*before\* the action is taken.



\---



\# Deployable Context Results



The two directly pre-action contextual candidates evaluated here do not improve on `local\_error\_std`.



\### Context support distance



\\\[

\\Delta\\text{mean AUC}=-0.203.

\\]



\### Predicted baseline action loss



\\\[

\\Delta\\text{mean AUC}=-0.041.

\\]



\### Predicted-loss interaction



\\\[

\\Delta\\text{mean AUC}=-0.004.

\\]



None provides positive reciprocal block-held-out value-add.



Therefore Experiment 109 does not identify a deployable contextual modifier for the error-dispersion signal.



\---



\# Primary Result



Experiment 109 supports two distinct conclusions.



\## Deployable conclusion



Among the strictly pre-action contextual variables tested:



\\\[

\\boxed{

\\text{no candidate improves the cross-block discrimination}

\\atop

\\text{of local error dispersion.}

}

\\]



\## Explanatory conclusion



Realized baseline action loss error provides very large and highly stable retrospective separation:



\\\[

\\boxed{

\\text{mean AUC}=0.994,\\quad

\\text{minimum AUC}=0.988.

}

\\]



Therefore the unresolved regime dependence appears closely connected to whether the model is about to underestimate the consequence of the candidate action.



\---



\# Relationship to Experiment 108



Experiment 108 showed that the problem cannot be repaired by simply rescaling `local\_error\_std`.



Experiment 109 now shows that two obvious pre-action contextual modifiers also fail to repair the representation.



However, realized action-loss error nearly resolves the classification problem retrospectively.



The research question therefore becomes more specific.



It is no longer:



\*\*How should `local\_error\_std` be normalized?\*\*



Nor merely:



\*\*What generic contextual variable should be added?\*\*



The next question is:



\\\[

\\boxed{

\\text{Can impending calibration error be estimated}

\\atop

\\text{from information available before action execution?}

}

\\]



\---



\# Mechanistic Interpretation



The evidence accumulated through Experiments 100-109 increasingly separates two concepts:



\### Historical calibration-risk state



This describes whether the model has recently behaved unreliably in nearby action-context regions.



\### Impending realized calibration failure



This describes whether the model's current candidate-action consequence is actually about to be underestimated.



The first is observable pre-action through historical information.



The second is only directly known after the consequence occurs.



Harmful expansion appears to depend strongly on both.



This suggests that the central unresolved problem is not simply identifying globally unreliable regions.



It is estimating when historical unreliability is likely to become \*\*current consequential underestimation\*\*.



\---



\# Implication for Representation Learning



The retrospective outcome-error result provides a useful supervised target for subsequent historical analysis.



Instead of immediately predicting the sparse harmful-expansion label, a future experiment can ask whether pre-action state variables predict:



\- the sign of impending action-loss error;

\- severe negative action-loss error;

\- or the magnitude of impending underestimation.



Such a target exists across a much larger action-context population than the eight harmful support-expansion events alone.



This potentially allows representation learning with substantially more statistical information.



Any resulting representation would then have to be evaluated separately on support-expansion decisions.



\---



\# Harmful-Event Scarcity



The support-expansion population contains only eight harmful events:



\- 2 in block 071-090;

\- 6 in block 091-110.



This remains a severe limitation.



The near-perfect outcome-error AUC should therefore not be interpreted as a precise estimate of future performance.



Its importance is mechanistic:



the effect is large, reciprocal across blocks, and directionally stable enough to identify realized calibration error as a high-priority explanatory variable.



Independent validation remains necessary.



\---



\# What Experiment 109 Supports



Experiment 109 supports the claims that:



1\. `local\_error\_std` remains a stable historical ranking signal;



2\. context support distance does not improve its reciprocal block-held-out discrimination;



3\. predicted baseline action loss does not improve its reciprocal block-held-out discrimination;



4\. simple interactions with those pre-action variables do not solve the problem;



5\. realized baseline action loss error provides extremely strong retrospective explanatory discrimination;



6\. the outcome-error association is directionally stable across blocks;



7\. impending consequence underestimation is therefore a plausible mechanistic target for subsequent pre-action representation learning.



\---



\# What Experiment 109 Does Not Support



Experiment 109 does not establish:



1\. a new controller feature;



2\. a new intervention threshold;



3\. that `baseline\_action\_loss\_error` can be used pre-action;



4\. that the retrospective AUC of 0.994 will generalize prospectively;



5\. that the current contextual candidates exhaust the available pre-action state;



6\. that a reliable pre-action proxy for impending loss error already exists;



7\. that the harmful-expansion selectivity problem has been solved.



\---



\# Scientific Boundary



The distinction established here is essential:



\\\[

\\boxed{

\\text{explanation after outcome}

\\neq

\\text{prediction before action}.

}

\\]



Experiment 109 substantially improves mechanistic understanding without claiming a deployable solution.



That is the correct interpretation of the near-perfect retrospective result.



\---



\# Experiment 109 Status



Experiment 109: COMPLETE



Primary deployable-context result:



\\\[

\\boxed{

\\text{no tested pre-action contextual modifier improves}

\\atop

\\texttt{local\\\_error\\\_std}

\\text{ across both historical blocks}.

}

\\]



Primary explanatory result:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}

\+

\\texttt{baseline\\\_action\\\_loss\\\_error}

}

\\]



achieves:



\\\[

\\boxed{

\\text{mean reciprocal AUC}=0.994

}

\\]



and:



\\\[

\\boxed{

\\text{minimum reciprocal AUC}=0.988.

}

\\]



The outcome-error variable remains strictly retrospective and is not authorized for controller use.



\---



\# Next Research Direction



The next experiment should test whether strictly pre-action information can predict impending calibration error over a larger historical action-context population.



The target should be defined before fitting.



A natural progression is to evaluate pre-action prediction of:



1\. signed action-loss error;



2\. underestimation versus non-underestimation;



3\. severe underestimation using the previously established calibration-error threshold.



The analysis should use block- or seed-held-out validation so that any apparent proxy must transfer across generation seeds.



Only after a pre-action calibration-error proxy demonstrates robust held-out performance should it be evaluated as a second-stage representation for support-expansion selectivity.



No new prospective controller intervention should occur merely because the retrospective outcome-error model performs well.

