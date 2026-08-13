\# Experiment 117 — Cross-Population Action-State Harm Decomposition



\## Purpose



Experiments 115 and 116 established that support-expansion action identity is associated with harmful-expansion risk across two non-overlapping historical populations.



Experiment 115 observed:



\\\[

P(H\\mid A=1)=24.242\\%

\\]



and:



\\\[

P(H\\mid A=2)=0\\%.

\\]



Experiment 116 independently replicated the direction:



\\\[

P(H\\mid A=1)=36.842\\%

\\]



and:



\\\[

P(H\\mid A=2)=17.391\\%.

\\]



The exact zero-harm action-2 pattern did not replicate, but the directional action-harm association did.



Experiment 117 therefore asks a mechanism-oriented question:



\*\*Is action identity merely standing in for observable pre-action support/loss geometry, or does action identity retain harmful-expansion information after controlling for the same geometry across both historical populations?\*\*



Experiment 117 is a cross-population decomposition analysis.



It does not establish causality.



It does not define a controller rule.



\---



\# Competing Hypotheses



\## State-Proxy Hypothesis



Action identity may appear predictive because action selection is determined by pre-action state:



\\\[

A \\leftarrow Z \\rightarrow H

\\]



where:



\- \\(A\\) is support-expansion action identity;

\- \\(Z\\) is observable pre-action support/loss geometry;

\- \\(H\\) is harmful support expansion.



Under this hypothesis, action identity should add little transferable information once \\(Z\\) is included.



\---



\## Residual Action-Structure Hypothesis



Alternatively:



\\\[

Z \\rightarrow H

\\]



while:



\\\[

A

\\]



retains information associated with harmful expansion after adjustment for the observable geometry.



Under this hypothesis, action identity should improve cross-population harm discrimination beyond geometry alone and should retain a stable coefficient direction.



Experiment 117 tests these alternatives predictively rather than causally.



\---



\# Independent Historical Populations



Two non-overlapping historical populations are used.



\## Early Population



Label:



`population\_001\_010`



Source:



`results/harmful\_expansion\_action\_conditioned\_epistemic\_excess\_analysis\_events.csv`



Rows:



\\\[

65

\\]



Harmful:



\\\[

15

\\]



Beneficial:



\\\[

50\.

\\]



\---



\## Later Population



Label:



`population\_071\_110`



Source population:



Experiment 115 support-expansion events.



Rows:



\\\[

88

\\]



Harmful:



\\\[

8

\\]



Beneficial:



\\\[

80\.

\\]



The later population is joined to the previously reconstructed action-conditioned support representation:



`results/action\_conditioned\_support\_representation\_analysis\_actions\_071\_110.csv`



\---



\# Combined Population



Total rows:



\\\[

153

\\]



Total harmful expansions:



\\\[

23\.

\\]



The populations are non-overlapping in generation-seed range.



\---



\# Frozen Cross-Population Geometry



Before observing Experiment 117 results, a common five-variable pre-action geometry was frozen:



\\\[

Z=

\[

d\_c,

d\_a,

d\_a-d\_c,

L\_{\\mathrm{pred}},

L\_{\\mathrm{relative}}

].

\\]



The variables are:



\- `context\_support\_distance`

\- `action\_support\_distance`

\- `action\_support\_minus\_context`

\- `predicted\_action\_loss`

\- `predicted\_relative\_loss`



The fifth variable is deterministically derived from the first two:



\\\[

\\texttt{action\\\_support\\\_minus\\\_context}

=

\\texttt{action\\\_support\\\_distance}

\-

\\texttt{context\\\_support\\\_distance}.

\\]



No realized outcome variable enters the geometry.



\---



\# Temporal Validity



The geometry is restricted to values available before realization of support-expansion harm.



Excluded from the representation are:



\- realized regret;

\- realized action loss;

\- loss prediction error;

\- harmful/beneficial label;

\- true-best action;

\- true-responsive action;

\- other post-outcome quantities.



Action identity is also available before the realized support-expansion consequence.



\---



\# Cross-Population Action-Harm Summary



\## Early Population



\### Action 1



Rows:



\\\[

19

\\]



Harmful:



\\\[

7

\\]



Beneficial:



\\\[

12

\\]



Harmful rate:



\\\[

\\boxed{36.842\\%}.

\\]



\### Action 2



Rows:



\\\[

46

\\]



Harmful:



\\\[

8

\\]



Beneficial:



\\\[

38

\\]



Harmful rate:



\\\[

\\boxed{17.391\\%}.

\\]



\---



\# Later Population



\## Action 1



Rows:



\\\[

33

\\]



Harmful:



\\\[

8

\\]



Beneficial:



\\\[

25

\\]



Harmful rate:



\\\[

\\boxed{24.242\\%}.

\\]



\## Action 2



Rows:



\\\[

55

\\]



Harmful:



\\\[

0

\\]



Beneficial:



\\\[

55

\\]



Harmful rate:



\\\[

\\boxed{0.000\\%}.

\\]



\---



\# Cross-Population Direction



Both populations satisfy:



\\\[

\\boxed{

P(H\\mid A=1)

>

P(H\\mid A=2).

}

\\]



Thus the replicated structural association identified in Experiments 115–116 remains present in the combined Experiment 117 analysis.



However, absolute rates remain population dependent.



\---



\# Can Observable Geometry Predict Action Identity?



The first mechanistic question asks whether the frozen pre-action geometry reliably predicts whether the support expansion uses action 1 or action 2.



The model is trained on one population and evaluated unchanged on the other.



\## Hold Out Early Population



Train:



later population



Test:



early population



AUC:



\\\[

\\boxed{0.338}.

\\]



\---



\## Hold Out Later Population



Train:



early population



Test:



later population



AUC:



\\\[

\\boxed{0.549}.

\\]



\---



\# Action-Prediction Summary



Mean reciprocal AUC:



\\\[

\\boxed{0.443}

\\]



Minimum reciprocal AUC:



\\\[

\\boxed{0.338}.

\\]



Therefore:



\\\[

\\boxed{

\\text{the frozen five-variable geometry does not provide}

\\atop

\\text{a stable cross-population representation of action identity.}

}

\\]



This argues against the simplest version of the state-proxy hypothesis.



\---



\# Reciprocal Population-Held-Out Harm Models



Three models are compared:



1\. `geometry\_only`

2\. `action\_only`

3\. `geometry\_plus\_action`



The objective is not in-sample fit.



The central question is transfer between the two non-overlapping historical populations.



\---



\# Geometry-Only Harm Model



The five-variable pre-action geometry alone produces:



\\\[

\\text{mean AUC}=0.413

\\]



\\\[

\\text{minimum AUC}=0.409

\\]



\\\[

\\text{maximum AUC}=0.417.

\\]



Thus:



\\\[

\\boxed{

\\text{the common support/loss geometry does not transfer}

\\atop

\\text{as a useful harmful-expansion classifier.}

}

\\]



Performance is below chance under the predefined harmful-risk orientation.



The result should not be post-hoc inverted and presented as successful prediction.



\---



\# Action-Only Harm Model



Action identity alone produces:



\\\[

\\boxed{

\\text{mean AUC}=0.729

}

\\]



\\\[

\\boxed{

\\text{minimum AUC}=0.613

}

\\]



\\\[

\\text{maximum AUC}=0.844.

\\]



Thus action identity transfers substantially better across populations than the common five-variable geometry.



\---



\# Geometry Plus Action



The adjusted model produces:



\\\[

\\boxed{

\\text{mean AUC}=0.560

}

\\]



\\\[

\\boxed{

\\text{minimum AUC}=0.512

}

\\]



\\\[

\\text{maximum AUC}=0.608.

\\]



Relative to geometry alone:



\\\[

\\Delta\\text{mean AUC}

=

0.560-0.413

=

\\boxed{+0.147}

\\]



and:



\\\[

\\Delta\\text{minimum AUC}

=

0.512-0.409

=

\\boxed{+0.103}.

\\]



Therefore action identity provides transferable information beyond the frozen observable geometry.



\---



\# Important Comparative Result



Although adding action improves on geometry alone:



\\\[

0.560 > 0.413,

\\]



the combined model remains weaker than action alone:



\\\[

0.560 < 0.729.

\\]



Therefore:



\\\[

\\boxed{

\\text{the tested geometry does not sharpen the action-harm signal.}

}

\\]



Instead, the geometry introduces substantial population-transfer instability.



This argues against treating the five-variable geometry as the explanatory mechanism underlying the replicated action association.



\---



\# Adjusted Action Coefficient



In the `geometry\_plus\_action` model, the action-2 indicator has mean standardized coefficient:



\\\[

\\boxed{-1.176}.

\\]



Sign stability:



\\\[

\\boxed{100\\%}.

\\]



Therefore in both reciprocal population fits, action 2 remains associated with lower harmful-expansion risk after adjustment for the common geometry.



This is the most important mechanistic result of Experiment 117.



\---



\# Action-Only Coefficient



The action-only model gives:



\\\[

\\boxed{

\\beta\_{\\text{action2}}=-1.166

}

\\]



with:



\\\[

\\boxed{100\\%\\text{ sign stability}}.

\\]



The adjusted coefficient:



\\\[

\-1.176

\\]



is similar in magnitude to the action-only coefficient:



\\\[

\-1.166.

\\]



Thus the frozen geometry does not materially attenuate the observed action association.



\---



\# Geometry Coefficient Stability



\## Geometry Only



\### Action Support Distance



Mean coefficient:



\\\[

+0.143

\\]



Sign stability:



\\\[

100\\%.

\\]



\### Action Support Minus Context



Mean coefficient:



\\\[

\-0.214

\\]



Sign stability:



\\\[

100\\%.

\\]



\### Context Support Distance



Mean coefficient:



\\\[

+0.340

\\]



Sign stability:



\\\[

100\\%.

\\]



\### Predicted Action Loss



Mean coefficient:



\\\[

+0.276

\\]



Mean absolute coefficient:



\\\[

0.713

\\]



Sign stability:



\\\[

50\\%.

\\]



\### Predicted Relative Loss



Mean coefficient:



\\\[

\-0.160

\\]



Sign stability:



\\\[

100\\%.

\\]



Several directions are stable, but their joint cross-population harmful-ranking performance remains poor.



\---



\# Adjusted Geometry Coefficients



Within the `geometry\_plus\_action` model:



\### Action Support Distance



Mean coefficient:



\\\[

+0.218

\\]



Sign stability:



\\\[

100\\%.

\\]



\### Action Support Minus Context



Mean coefficient:



\\\[

\-0.113

\\]



Sign stability:



\\\[

50\\%.

\\]



\### Context Support Distance



Mean coefficient:



\\\[

+0.343

\\]



Sign stability:



\\\[

100\\%.

\\]



\### Predicted Action Loss



Mean coefficient:



\\\[

+0.350

\\]



Sign stability:



\\\[

50\\%.

\\]



\### Predicted Relative Loss



Mean coefficient:



\\\[

\-0.075

\\]



Sign stability:



\\\[

50\\%.

\\]



The mixed sign stability of several geometry terms is consistent with the weak reciprocal population transfer.



\---



\# Primary Result



Experiment 117 tests whether the replicated action-harm association from Experiments 115–116 can be explained by a common observable five-variable pre-action support/loss geometry.



The result does not support that explanation.



The geometry:



\- does not predict action identity reliably across populations;

\- does not predict harmful expansion reliably across populations;

\- does not attenuate the action coefficient materially.



Meanwhile, action identity:



\- transfers substantially better than geometry alone;

\- improves both mean and minimum AUC when added to geometry;

\- retains a negative action-2 coefficient with 100% sign stability.



Therefore:



\\\[

\\boxed{

\\text{action identity carries residual harmful-expansion}

\\atop

\\text{information not captured by the frozen five-variable geometry.}

}

\\]



\---



\# What This Does Not Mean



Experiment 117 does \*\*not\*\* establish that action identity is causal.



The result:



\\\[

A

\\]



retains predictive information after adjustment for:



\\\[

Z

\\]



only shows that the tested \\(Z\\) does not explain away the association.



Unobserved or omitted pre-action variables may still determine both:



\- action identity;

\- harmful-expansion risk.



Possible omitted state includes:



\- trigger state;

\- anchor age;

\- mismatch state;

\- release probability;

\- current parameter estimate;

\- predicted regret structure;

\- model uncertainty;

\- state-space location;

\- latent controller state;

\- other action-selection context.



Therefore:



\\\[

\\boxed{

\\text{residual predictive information}

\\neq

\\text{causal action effect}.

}

\\]



\---



\# State-Proxy Hypothesis Result



The simplest state-proxy explanation was:



\\\[

A \\leftarrow Z \\rightarrow H.

\\]



If the frozen common geometry \\(Z\\) fully explained the action association, action identity should contribute little after adjustment.



Instead:



\\\[

\\beta\_{\\text{action2}}=-1.176

\\]



with:



\\\[

100\\%\\text{ sign stability},

\\]



and:



\\\[

\\Delta\\text{minimum AUC}=+0.103

\\]



after adding action to geometry.



Therefore the tested five-variable state-proxy hypothesis is not supported.



\---



\# Residual Action-Structure Hypothesis Result



The evidence is consistent with:



\\\[

\\boxed{

\\text{action identity encoding structural information not represented}

\\atop

\\text{by the tested common support/loss geometry.}

}

\\]



However, the experiment does not determine whether that residual information is:



\- intrinsic to the action;

\- due to omitted controller state;

\- due to latent action-selection context;

\- or due to another pre-action variable correlated with action identity.



That distinction remains unresolved.



\---



\# Relationship to Experiments 115 and 116



\## Experiment 115



Discovered the action-harm association in seeds `44071–44110`.



\## Experiment 116



Independently replicated the direction in seeds `44001–44010`.



\## Experiment 117



Tests whether the association disappears after adjustment for a common observable pre-action geometry.



It does not.



Thus the progression is:



\\\[

\\text{discovery}

\\rightarrow

\\text{independent directional replication}

\\rightarrow

\\text{mechanistic decomposition}.

\\]



\---



\# Why Geometry Alone Performs Poorly



The common geometry model achieves:



\\\[

\\text{mean AUC}=0.413.

\\]



This indicates substantial cross-population instability in the relationship between:



\- support distance;

\- predicted loss geometry;

\- harmful expansion.



That finding is consistent with earlier experiments showing that continuous scalar or compact state representations often fail to transfer even when they show useful local or retrospective separation.



The action association appears more stable than these particular continuous quantities.



\---



\# Scientific Boundary



Experiment 117 introduces:



\- no new seed;

\- no controller threshold;

\- no action-specific veto;

\- no policy modification;

\- no causal claim.



The experiment remains a historical cross-population decomposition analysis.



\---



\# What Experiment 117 Supports



Experiment 117 supports the claims that:



1\. action identity is not reliably predictable from the frozen five-variable geometry across populations;



2\. geometry alone transfers poorly for harmful-expansion prediction;



3\. action identity alone transfers substantially better;



4\. adding action identity to geometry improves mean and minimum population-held-out AUC;



5\. the adjusted action-2 coefficient remains negative in both reciprocal population fits;



6\. the action association is not explained away by the tested common support/loss geometry;



7\. action identity therefore remains a credible residual structural risk marker.



\---



\# What Experiment 117 Does Not Support



Experiment 117 does not establish:



1\. that action identity causes harm;



2\. that action 1 should be vetoed;



3\. that action 2 is safe;



4\. a deployable action-conditioned controller;



5\. that the common five-variable geometry is the complete pre-action state;



6\. that omitted-state confounding has been eliminated;



7\. a stable harmful-risk threshold;



8\. prospective controller improvement.



\---



\# Experiment 117 Status



Experiment 117: COMPLETE



Action-prediction performance from common geometry:



\\\[

\\boxed{

\\text{mean AUC}=0.443

}

\\]



\\\[

\\boxed{

\\text{minimum AUC}=0.338.

}

\\]



Harm prediction:



\### Geometry Only



\\\[

\\boxed{

\\text{mean AUC}=0.413

}

\\]



\\\[

\\boxed{

\\text{minimum AUC}=0.409.

}

\\]



\### Action Only



\\\[

\\boxed{

\\text{mean AUC}=0.729

}

\\]



\\\[

\\boxed{

\\text{minimum AUC}=0.613.

}

\\]



\### Geometry Plus Action



\\\[

\\boxed{

\\text{mean AUC}=0.560

}

\\]



\\\[

\\boxed{

\\text{minimum AUC}=0.512.

}

\\]



Action value-add over geometry:



\\\[

\\boxed{

\\Delta\\text{mean AUC}=+0.147

}

\\]



\\\[

\\boxed{

\\Delta\\text{minimum AUC}=+0.103.

}

\\]



Adjusted action-2 coefficient:



\\\[

\\boxed{-1.176}

\\]



Sign stability:



\\\[

\\boxed{100\\%}.

\\]



Primary interpretation:



\\\[

\\boxed{

\\text{the replicated action-harm association survives adjustment}

\\atop

\\text{for the tested common pre-action support/loss geometry.}

}

\\]



No causal or controller claim is authorized.



\---



\# Next Research Direction



Experiment 117 narrows the mechanism question further.



The next analysis should examine pre-action variables that exist in the earlier historical representation but were excluded from the common five-variable geometry because they were not yet reconstructed for the later population.



Candidate state families include:



\- `context\_benefit\_probability`

\- `context\_release\_probability`

\- `context\_anchor\_age`

\- `context\_trigger\_score`

\- `context\_feature\_distance`

\- `context\_current\_mismatch\_indicator`

\- `context\_current\_parameter\_estimate`

\- predicted primary regret

\- predicted expanded regret

\- predicted regret margin

\- predicted under-risk

\- action-step structure



The next experiment should first determine whether these variables can be reconstructed consistently for the later population without using realized outcomes.



Only then should they be tested as candidate explanations of the residual action association.



The central next question is:



\*\*Does a broader pre-action controller-state representation explain the action-harm association that support/loss geometry failed to explain?\*\*



No prospective action-conditioned controller modification should occur until that question is resolved.

