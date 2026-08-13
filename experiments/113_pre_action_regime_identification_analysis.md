\# Experiment 113 — Pre-Action Regime Identification Analysis



\## Purpose



Experiments 107-112 repeatedly established that useful risk ranking does not automatically produce a stable intervention operating point.



The central unresolved issue became:



\*\*Can the digital twin identify, before action execution, which risk-to-action mapping regime it currently occupies?\*\*



Experiment 113 tests that question using a deliberately restricted pre-action representation.



The experiment asks three things:



1\. whether the two historical support-expansion blocks occupy distinguishable pre-action state distributions;

2\. whether a multivariate pre-action regime score can identify block membership out of seed;

3\. whether that inferred regime score improves or modulates the mapping from frozen severe-underestimation probability to harmful support expansion.



Experiment 113 is diagnostic only.



It does not:



\- define a controller threshold;

\- modify the controller;

\- introduce new prospective seeds;

\- use outcome-derived information as a regime feature;

\- or treat block identity itself as a deployable feature.



\---



\# Historical Population



The experiment uses the same historical support-expansion population carried forward from Experiments 105-112.



Total events:



\\\[

88

\\]



Historical blocks:



\## Block A



`block\_071\_090`



Seeds:



44071-44090



\## Block B



`block\_091\_110`



Seeds:



44091-44110



No new support-expansion outcomes are generated.



\---



\# Pre-Action Regime Features



The available regime-feature set was:



\- `local\_error\_std`

\- `severe\_underestimation\_probability`



No optional support-context fields were available in the Experiment 111 event file used by this analysis.



Thus the tested regime representation was intentionally compact.



Both variables are available before support-expansion outcome realization.



\---



\# Regime Label



Block identity is used only as an experimental target.



The regime target is defined as:



\\\[

\\text{Block A}=0

\\]



and:



\\\[

\\text{Block B}=1.

\\]



This label is not a controller input.



It exists only to test whether the two historical blocks correspond to recognizable pre-action state regimes.



\---



\# Univariate Regime Geometry



\## Local Error Standard Deviation



Block A mean:



\\\[

0.053559

\\]



Block B mean:



\\\[

0.056657

\\]



Difference:



\\\[

+0.003098

\\]



Best-orientation regime AUC:



\\\[

\\boxed{0.517}.

\\]



This is essentially chance-level separation.



Therefore `local\_error\_std` does not meaningfully distinguish the two historical blocks by itself.



\---



\## Severe-Underestimation Probability



Block A mean:



\\\[

0.460501

\\]



Block B mean:



\\\[

0.499651

\\]



Difference:



\\\[

+0.039150

\\]



Best-orientation regime AUC:



\\\[

\\boxed{0.572}.

\\]



This is weak separation.



Thus the frozen severe-underestimation probability contains only modest information about historical block identity.



\---



\# Leave-One-Seed-Out Regime Identification



A multivariate logistic model using:



\- `local\_error\_std`

\- `severe\_underestimation\_probability`



was evaluated using leave-one-generation-seed-out prediction.



The pooled out-of-fold regime AUC was:



\\\[

\\boxed{0.279}.

\\]



This is substantially below chance under the predefined target orientation.



The result indicates that the learned block-identification mapping does not transfer reliably to held-out seeds in the intended direction.



\---



\# Why the AUC Must Not Be Post-Hoc Flipped



Because:



\\\[

1-0.279=0.721,

\\]



it would be mathematically possible to reverse the score orientation after observing the result.



Experiment 113 does not permit that reinterpretation.



The target orientation was defined in advance:



\\\[

\\text{Block B}=1.

\\]



Therefore the correct result is:



\\\[

\\boxed{

\\text{the predefined regime-identification model failed}

}

\\]



rather than:



\\\[

\\boxed{

\\text{AUC}=0.721.

}

\\]



A post-hoc inversion would redefine the learned regime score after observing held-out performance.



That would not constitute valid evidence that the original regime detector transferred.



The below-chance result may indicate structured anti-alignment, but that possibility requires a separate analysis and may not be treated as success within Experiment 113.



\---



\# Regime-Model Coefficient Stability



\## Local Error Standard Deviation



Mean coefficient:



\\\[

+0.037

\\]



Mean absolute coefficient:



\\\[

0.058

\\]



Sign stability:



\\\[

79.167\\%.

\\]



This is weaker than the coefficient stability observed for several earlier calibration-state models.



\---



\## Severe-Underestimation Probability



Mean coefficient:



\\\[

+0.212

\\]



Mean absolute coefficient:



\\\[

0.228

\\]



Sign stability:



\\\[

95.833\\%.

\\]



Although its sign is relatively stable, the overall regime-identification model still fails out of seed.



Stable coefficient direction alone is therefore not sufficient evidence for useful regime recognition.



\---



\# Risk-to-Harm Modulation Test



The primary falsification question is not merely whether block identity can be predicted.



It is whether the inferred pre-action regime score improves the mapping from severe-underestimation probability to harmful support expansion.



Four models were evaluated under reciprocal block-held-out validation:



1\. `severe\_proxy\_only`

2\. `regime\_only`

3\. `proxy\_plus\_regime`

4\. `proxy\_regime\_interaction`



\---



\# Severe Proxy Baseline



The frozen severe-underestimation probability alone produces:



\\\[

\\boxed{

\\text{mean AUC}=0.821

}

\\]



with:



\\\[

\\boxed{

\\text{minimum AUC}=0.764

}

\\]



and maximum AUC:



\\\[

0.878.

\\]



This reproduces the Experiment 111 support-expansion ranking result.



\---



\# Regime Score Only



The inferred regime score alone produces:



\\\[

\\text{mean AUC}=0.739

\\]



with:



\\\[

\\text{minimum AUC}=0.649

\\]



and maximum AUC:



\\\[

0.829.

\\]



This indicates that the regime score contains some association with harmful support expansion.



However, this does not validate it as a useful regime detector because its direct leave-one-seed-out block-identification performance failed.



The result must therefore remain diagnostic.



\---



\# Severe Proxy Plus Regime Score



The additive model produces:



\\\[

\\text{mean AUC}=0.668

\\]



with:



\\\[

\\text{minimum AUC}=0.581

\\]



and maximum AUC:



\\\[

0.756.

\\]



This is substantially worse than the severe proxy alone.



Relative to the severe-proxy baseline:



\\\[

\\Delta\\text{mean AUC}

=

\\boxed{-0.153}

\\]



and:



\\\[

\\Delta\\text{minimum AUC}

=

\\boxed{-0.183}

\\]



approximately.



Thus the inferred regime score does not improve harmful-expansion discrimination.



It materially degrades it.



\---



\# Severe-Proxy Regime Interaction



The interaction model produces exactly the same transfer summary:



\\\[

\\text{mean AUC}=0.668

\\]



\\\[

\\text{minimum AUC}=0.581

\\]



\\\[

\\text{maximum AUC}=0.756.

\\]



Relative to the severe-proxy baseline:



\\\[

\\boxed{

\\Delta\\text{mean AUC}=-0.153

}

\\]



and:



\\\[

\\boxed{

\\Delta\\text{minimum AUC}=-0.182.

}

\\]



Therefore the interaction hypothesis is not supported.



\---



\# Primary Falsification Result



Experiment 113 tests the hypothesis:



\\\[

\\boxed{

\\text{a compact pre-action regime score derived from}

\\atop

\\texttt{local\\\_error\\\_std}

\+

\\texttt{severe\\\_underestimation\\\_probability}

\\atop

\\text{may explain the cross-block risk-to-action mapping shift.}

}

\\]



The result does not support that hypothesis.



Evidence against it includes:



1\. weak univariate block separation;

2\. pooled leave-one-seed-out regime AUC of only 0.279;

3\. degradation of harmful-expansion AUC when the regime score is added;

4\. no benefit from an explicit risk-by-regime interaction.



Thus:



\\\[

\\boxed{

\\text{the operating-point instability is not explained}

\\atop

\\text{by a regime state recoverable from these two variables.}

}

\\]



\---



\# Relationship to Experiment 112



Experiment 112 established that:



\\\[

\\boxed{

\\text{decision-boundary heterogeneity remains}

}

\\]



even when the controller uses a learned pre-action severe-underestimation probability instead of raw error dispersion.



Experiment 113 asks whether that heterogeneity corresponds to a recognizable regime in the same compact risk-state space.



It does not.



Therefore:



\\\[

\\boxed{

\\text{decision-boundary heterogeneity exists,}

}

\\]



but:



\\\[

\\boxed{

\\text{its source is not captured by the tested}

\\atop

\\text{two-variable calibration-risk representation.}

}

\\]



\---



\# Important Methodological Consequence



The prerequisite for a regime-conditioned controller experiment has failed.



Experiment 113 was intended to establish a valid pre-action regime representation before any regime-conditioned threshold design.



Because the regime representation did not survive its diagnostic tests, the next experiment should \*\*not\*\* proceed directly to a regime-conditioned controller threshold.



Doing so would introduce complexity without validated regime information.



\---



\# Why This Negative Result Matters



It would have been easy to respond to the threshold instability from Experiments 107 and 112 by constructing a conditional controller immediately.



Experiment 113 prevents that premature move.



The experiment shows that a regime-conditioned controller based only on:



\- local calibration-error dispersion;

\- frozen severe-underestimation probability



would not be scientifically justified.



This is a useful falsification.



It narrows the search toward richer pre-action system state rather than increasingly elaborate transformations of the same calibration-risk signals.



\---



\# Current Interpretation of the Threshold Instability



The evidence now supports the following layered conclusion.



\## Ranking Layer



The twin can estimate meaningful risk.



The severe-underestimation proxy achieves useful reciprocal support-expansion ranking.



\## Operating-Point Layer



A fixed scalar threshold does not transfer reliably.



\## Compact Regime Layer



The threshold instability is not explained by a regime detector constructed from the same two calibration-risk quantities.



Therefore the missing information likely lies elsewhere in the system state.



\---



\# Candidate Sources of Missing Regime Information



The next analysis should examine richer, physically or computationally meaningful pre-action state already available within the simulation architecture.



Potential candidate classes include:



\- support geometry;

\- state-space location;

\- controller mismatch state;

\- adaptive transient state;

\- anchor age;

\- trigger state;

\- uncertainty state;

\- action identity;

\- action-transition geometry;

\- local model-support density;

\- predicted loss-surface geometry;

\- release probability;

\- or other quantities already present in the controller before action execution.



These candidates should be defined from existing architecture rather than discovered through unrestricted feature fishing.



\---



\# Harmful-Event Scarcity



The support-expansion population still contains only eight harmful events.



This means complex harmful-event interaction models remain highly vulnerable to instability.



Accordingly, the next regime analysis should preferably first test whether richer pre-action state distinguishes the historical operating regimes independently of the harmful label.



Only after establishing such regime structure should harmful-risk modulation be tested.



\---



\# What Experiment 113 Supports



Experiment 113 supports the claims that:



1\. `local\_error\_std` provides essentially no univariate block separation;



2\. severe-underestimation probability provides only weak block separation;



3\. the compact multivariate regime model fails under leave-one-seed-out validation;



4\. the predefined regime score should not be post-hoc inverted and relabeled as successful;



5\. adding the regime score to the severe proxy substantially degrades support-expansion discrimination;



6\. an explicit proxy-by-regime interaction also degrades performance;



7\. the compact calibration-risk regime hypothesis is therefore falsified.



\---



\# What Experiment 113 Does Not Support



Experiment 113 does not establish:



1\. a deployable regime detector;



2\. a regime-conditioned controller rule;



3\. a regime-conditioned threshold;



4\. that the below-chance regime AUC should be inverted and used;



5\. that block identity itself is an acceptable controller feature;



6\. that the source of decision-boundary heterogeneity has been identified;



7\. that all possible pre-action regime representations have failed.



\---



\# Scientific Boundary



Experiment 113 establishes a useful boundary:



\\\[

\\boxed{

\\text{decision-boundary heterogeneity}

\\neq

\\text{recoverable compact calibration-risk regime}

}

\\]



under the representation tested.



The next research phase should broaden the regime representation using independent pre-action system state rather than continue manipulating the same scalar risk variables.



\---



\# Experiment 113 Status



Experiment 113: COMPLETE



Pre-action regime-identification result:



\\\[

\\boxed{

\\text{pooled leave-one-seed-out AUC}=0.279

}

\\]



under the predefined block orientation.



Risk-to-harm modulation result:



\### Severe proxy alone



\\\[

\\boxed{

\\text{mean AUC}=0.821,\\quad

\\text{minimum AUC}=0.764

}

\\]



\### Severe proxy plus regime score



\\\[

\\text{mean AUC}=0.668

\\]



\### Proxy-regime interaction



\\\[

\\text{mean AUC}=0.668

\\]



Interaction value-add:



\\\[

\\boxed{

\\Delta\\text{mean AUC}=-0.153

}

\\]



\\\[

\\boxed{

\\Delta\\text{minimum AUC}=-0.182.

}

\\]



The compact regime hypothesis is not supported.



No controller modification is defined.



\---



\# Next Research Direction



The next experiment should inspect the existing controller and support-expansion event representation to identify a \*\*predefined richer set of pre-action system-state variables\*\* that could plausibly encode operating regime.



The analysis should proceed in two stages:



1\. determine whether richer system state distinguishes the historical blocks or operating regimes under held-out validation;

2\. only if that succeeds, test whether the resulting frozen regime representation modulates the severe-proxy-to-harm relationship.



The central next question is:



\*\*Does the broader pre-action dynamical and controller state contain regime information that the calibration-risk representation alone does not?\*\*



No new prospective controller intervention should occur until such regime information is demonstrated.

