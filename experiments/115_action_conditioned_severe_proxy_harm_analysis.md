\# Experiment 115 — Action-Conditioned Severe-Proxy Harm Analysis



\## Purpose



Experiment 114 rejected the hypothesis that a richer continuous pre-action support/action geometry could reliably identify the historical operating regime or improve the frozen severe-underestimation-proxy-to-harm mapping.



However, Experiment 114 also identified a strong secondary structural difference between the two historical blocks:



\- block `071–090` was dominated by support-baseline action 1;

\- block `091–110` was dominated by support-baseline action 2.



Experiment 115 therefore tests a separate structural hypothesis:



\*\*Is the relationship between the frozen pre-action severe-underestimation proxy and harmful support expansion conditioned on support-baseline action identity?\*\*



Experiment 115 treats action identity as a predefined structural variable.



It does not:



\- select an intervention threshold;

\- modify the controller;

\- introduce a new prospective seed block;

\- redefine the Experiment 110 severe-underestimation proxy;

\- or use realized outcome variables as predictors.



\---



\# Historical Population



Experiment 115 uses the same 88-event historical support-expansion population carried forward from Experiments 105–114.



Total support expansions:



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



Historical blocks:



\## Block 071–090



Seeds:



44071–44090



Total expansions:



\\\[

39

\\]



\## Block 091–110



Seeds:



44091–44110



Total expansions:



\\\[

49\.

\\]



No new outcomes are generated.



\---



\# Frozen Risk Representation



The risk variable is the previously frozen Experiment 110 out-of-fold:



`severe\_underestimation\_probability`



derived from:



`expanded\_historical\_state`.



Experiment 115 does not modify the severe-underestimation representation.



The proxy remains strictly pre-action.



\---



\# Structural Variable



The structural variable is:



`support\_baseline\_action`



with observed values:



\- action 1;

\- action 2.



Action identity is available before the support-expansion consequence is realized.



It is therefore temporally admissible as a structural diagnostic.



\---



\# Action-by-Block Population Structure



\## Block 071–090



\### Action 1



Rows:



\\\[

24

\\]



Harmful:



\\\[

2

\\]



Beneficial:



\\\[

22\.

\\]



\### Action 2



Rows:



\\\[

15

\\]



Harmful:



\\\[

0

\\]



Beneficial:



\\\[

15\.

\\]



\---



\# Block 091–110



\## Action 1



Rows:



\\\[

9

\\]



Harmful:



\\\[

6

\\]



Beneficial:



\\\[

3\.

\\]



\## Action 2



Rows:



\\\[

40

\\]



Harmful:



\\\[

0

\\]



Beneficial:



\\\[

40\.

\\]



\---



\# Primary Structural Finding



Across the full 88-event population:



\## Action 1



Total expansions:



\\\[

33

\\]



Harmful:



\\\[

8

\\]



Beneficial:



\\\[

25\.

\\]



Observed harmful fraction:



\\\[

\\frac{8}{33}

=

24.242\\%.

\\]



\## Action 2



Total expansions:



\\\[

55

\\]



Harmful:



\\\[

0

\\]



Beneficial:



\\\[

55\.

\\]



Observed harmful fraction:



\\\[

\\boxed{0\\%}.

\\]



Therefore:



\\\[

\\boxed{

\\text{all eight observed harmful support expansions occur under action 1.}

}

\\]



No harmful support expansion occurs under action 2 in the Experiment 115 historical sample.



This is the strongest structural result of the experiment.



\---



\# Action 1 Proxy Geometry — Block 071–090



For action 1:



Harmful severe-proxy mean:



\\\[

0.646221

\\]



Beneficial severe-proxy mean:



\\\[

0.460789

\\]



Difference:



\\\[

+0.185432.

\\]



Rank AUC:



\\\[

\\boxed{0.841}.

\\]



Thus within block `071–090`, higher severe-underestimation probability strongly ranks harmful action-1 expansions above beneficial action-1 expansions.



\---



\# Action 1 Proxy Geometry — Block 091–110



For action 1:



Harmful severe-proxy mean:



\\\[

0.625962

\\]



Beneficial severe-proxy mean:



\\\[

0.630104

\\]



Difference:



\\\[

\-0.004142.

\\]



Rank AUC:



\\\[

\\boxed{0.444}.

\\]



Thus within block `091–110`, severe-underestimation probability provides essentially no useful action-1 harmful-versus-beneficial ranking and is slightly reversed.



\---



\# Action 2 Geometry



Action 2 contains no harmful events in either block.



Therefore:



\\\[

\\boxed{

\\text{action-2 harmful-versus-beneficial AUC is not estimable.}

}

\\]



This is not missing data or a modeling failure.



The class distribution itself is uninformative because the observed action-2 population contains only beneficial support expansions.



\---



\# Pooled Action-Conditioned Geometry



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

25\.

\\]



Harmful severe-proxy mean:



\\\[

0.631027

\\]



Beneficial severe-proxy mean:



\\\[

0.481107

\\]



Rank AUC:



\\\[

\\boxed{0.760}.

\\]



Thus severe-underestimation probability retains useful pooled harmful-versus-beneficial ranking among action-1 expansions.



\---



\## Action 2



Rows:



\\\[

55

\\]



Harmful:



\\\[

0\.

\\]



Because no harmful event exists:



\\\[

\\text{rank AUC}

\\]



is undefined.



\---



\# Reciprocal Within-Action Transfer



The severe proxy was evaluated separately within each action under reciprocal block-held-out transfer.



\## Action 1 — Held Out Block 071–090



Training block:



`091–110`



Training rows:



\\\[

9

\\]



Training harmful:



\\\[

6\.

\\]



Test rows:



\\\[

24

\\]



Test harmful:



\\\[

2\.

\\]



Transferred AUC:



\\\[

\\boxed{0.159}.

\\]



This is substantially below chance under the trained orientation.



\---



\## Action 1 — Held Out Block 091–110



Training block:



`071–090`



Training rows:



\\\[

24

\\]



Training harmful:



\\\[

2\.

\\]



Test rows:



\\\[

9

\\]



Test harmful:



\\\[

6\.

\\]



Transferred AUC:



\\\[

\\boxed{0.444}.

\\]



Thus the within-action-1 severe-proxy relationship does not transfer reliably across blocks.



\---



\# Interpretation of the Action-1 Transfer Failure



The action-1 result is critical.



Experiment 115 does not show that action conditioning stabilizes the severe-proxy-to-harm mapping.



Instead:



\\\[

\\boxed{

\\text{action 1 concentrates all observed harmful expansions,}

}

\\]



while:



\\\[

\\boxed{

\\text{within action 1, the severe-proxy ranking remains block dependent.}

}

\\]



This distinction prevents the strong pooled action result from being misinterpreted as a validated action-conditioned risk function.



\---



\# Action 2 Transfer



Both block-specific action-2 populations contain:



\\\[

0

\\]



harmful events.



Therefore reciprocal action-2 harmful discrimination cannot be evaluated.



The experiment correctly marks both action-2 transfer folds as:



`uninformative\_class\_distribution`.



\---



\# Pooled Action-Conditioning Models



Experiment 115 compares four reciprocal block-held-out models:



1\. `severe\_proxy\_only`

2\. `action\_only`

3\. `proxy\_plus\_action`

4\. `proxy\_action\_interaction`



Action 2 is represented by an indicator variable.



The interaction model includes:



\\\[

\\text{severe proxy}

\\times

\\text{action-2 indicator}.

\\]



No operating threshold is selected.



\---



\# Severe Proxy Baseline



The frozen severe proxy alone reproduces Experiment 111:



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

\\text{maximum AUC}=0.878.

\\]



\---



\# Action Identity Alone



The action-only model achieves:



\\\[

\\boxed{

\\text{mean AUC}=0.834

}

\\]



\\\[

\\text{minimum AUC}=0.703

\\]



\\\[

\\text{maximum AUC}=0.965.

\\]



This strong discrimination is primarily driven by the observed structural fact that all harmful events occur under action 1 while action 2 contains no harmful events.



The action-2 coefficient is:



\\\[

\\boxed{-1.566}

\\]



with:



\\\[

\\boxed{100\\%\\text{ sign stability}}.

\\]



Thus action 2 is consistently associated with lower harmful-expansion probability in both reciprocal block fits.



\---



\# Severe Proxy Plus Action



The additive model achieves:



\\\[

\\boxed{

\\text{mean AUC}=0.926

}

\\]



\\\[

\\boxed{

\\text{minimum AUC}=0.905

}

\\]



\\\[

\\text{maximum AUC}=0.946.

\\]



This is a substantial improvement over the severe proxy alone.



Coefficient structure:



\### Severe Proxy



Mean coefficient:



\\\[

+0.790

\\]



Sign stability:



\\\[

100\\%.

\\]



\### Action-2 Indicator



Mean coefficient:



\\\[

\-1.380

\\]



Sign stability:



\\\[

100\\%.

\\]



Thus both higher severe-underestimation probability and action identity contribute stable directional information in the pooled reciprocal model.



\---



\# Proxy × Action Interaction



The full action-interaction model achieves the strongest pooled reciprocal performance:



\\\[

\\boxed{

\\text{mean AUC}=0.933

}

\\]



\\\[

\\boxed{

\\text{minimum AUC}=0.905

}

\\]



\\\[

\\boxed{

\\text{maximum AUC}=0.961.

}

\\]



Relative to severe proxy alone:



\\\[

\\boxed{

\\Delta\\text{mean AUC}=+0.112

}

\\]



and:



\\\[

\\boxed{

\\Delta\\text{minimum AUC}=+0.142.

}

\\]



These are large improvements relative to the previous frozen-proxy baseline.



\---



\# Interaction Coefficient Structure



\## Severe-Underestimation Probability



Mean coefficient:



\\\[

+0.901

\\]



Sign stability:



\\\[

100\\%.

\\]



\## Action-2 Indicator



Mean coefficient:



\\\[

\-0.807

\\]



Sign stability:



\\\[

100\\%.

\\]



\## Severe Proxy × Action 2



Mean coefficient:



\\\[

\-0.729

\\]



Sign stability:



\\\[

100\\%.

\\]



The coefficient structure is directionally stable across both reciprocal block fits.



\---



\# Why the 0.933 AUC Must Be Interpreted Conservatively



The interaction result is numerically strong.



However, the support-expansion class geometry is highly asymmetric:



\\\[

8/8

\\]



harmful events occur under action 1, while:



\\\[

0/55

\\]



action-2 expansions are harmful.



Therefore a substantial fraction of the pooled model's discrimination comes from structural action separation itself.



This means:



\\\[

\\boxed{

\\text{high pooled action-conditioned AUC}

\\neq

\\text{validated action-specific risk calibration}.

}

\\]



The within-action transfer results provide direct evidence for this distinction.



\---



\# Primary Scientific Result



Experiment 115 establishes a strong historical association between support action identity and harmful expansion.



Specifically:



\\\[

\\boxed{

H\_{A=1}=8/33

}

\\]



while:



\\\[

\\boxed{

H\_{A=2}=0/55.

}

\\]



Thus:



\\\[

\\boxed{

\\text{all observed harmful support expansions are concentrated in action 1.}

}

\\]



This is a stronger and more direct structural finding than the previous attempts to infer a generic continuous operating regime.



\---



\# Secondary Result



Adding action identity to the frozen severe-underestimation proxy substantially improves pooled reciprocal block-held-out discrimination.



The best pooled model achieves:



\\\[

\\boxed{

\\text{mean AUC}=0.933

}

\\]



and:



\\\[

\\boxed{

\\text{minimum AUC}=0.905.

}

\\]



However, this result is not sufficient to establish a stable action-conditioned safety rule because the within-action-1 severe-proxy relationship remains strongly block dependent.



\---



\# Important Negative Result



Among action-1 expansions:



\\\[

\\text{AUC}\_{071-090}=0.841

\\]



but:



\\\[

\\text{AUC}\_{091-110}=0.444.

\\]



Reciprocal within-action-1 model transfer yields:



\\\[

0.159

\\]



and:



\\\[

0.444.

\\]



Therefore:



\\\[

\\boxed{

\\text{conditioning on action identity does not stabilize}

\\atop

\\text{the severe-proxy-to-harm relationship itself.}

}

\\]



This prevents Experiment 115 from being interpreted as a solved action-conditioned operating-point problem.



\---



\# Relationship to Experiment 114



Experiment 114 found that continuous support/action geometry did not provide a useful transferable regime representation.



Its secondary diagnostic revealed a large action-composition shift between historical blocks.



Experiment 115 independently tests the action-conditioning hypothesis motivated by that diagnostic.



The result shows that the action-composition difference is associated with a much deeper class-structure difference:



\\\[

\\boxed{

\\text{harmful support expansion occurs only under action 1}

}

\\]



in the present historical population.



Thus the operating-point instability may partly reflect changing action composition.



However, action composition does not fully explain the problem because severe-proxy ranking within action 1 remains unstable.



\---



\# Alternative Interpretation to Avoid



Experiment 115 must not be summarized as:



> Action 2 is proven safe.



The historical evidence contains:



\\\[

55

\\]



action-2 support expansions and zero harmful events.



That is suggestive but not sufficient to establish universal safety.



The correct statement is:



\\\[

\\boxed{

\\text{no harmful action-2 support expansion was observed}

\\atop

\\text{in this historical population.}

}

\\]



Independent replication is required.



\---



\# Harmful-Event Scarcity



Only eight harmful support-expansion events exist in the Experiment 115 population.



All eight occur under action 1.



This creates strong structural separation but also makes the result sensitive to sample composition.



The next experiment should therefore test the action association on an independent historical block before any action-conditioned threshold is considered.



\---



\# What Experiment 115 Supports



Experiment 115 supports the claims that:



1\. all observed harmful support expansions in the 88-event population occur under action 1;



2\. no harmful action-2 support expansion is observed among 55 action-2 expansions;



3\. action identity alone carries substantial harmful-expansion information;



4\. adding action identity to the severe proxy substantially improves pooled reciprocal AUC;



5\. the action-interaction model reaches mean AUC 0.933 and minimum AUC 0.905;



6\. coefficient directions are stable across reciprocal block fits;



7\. the action-conditioned structural hypothesis warrants independent replication.



\---



\# What Experiment 115 Does Not Support



Experiment 115 does not establish:



1\. that action 2 is universally safe;



2\. an action-conditioned controller threshold;



3\. an action-conditioned veto rule;



4\. stable severe-proxy ranking within action 1;



5\. stable within-action operating-point transfer;



6\. prospective controller improvement;



7\. that action identity fully explains historical decision-boundary instability.



\---



\# Scientific Boundary



Experiment 115 introduces:



\- no intervention threshold;

\- no controller modification;

\- no new prospective seed;

\- no claim of action-2 safety;

\- no action-specific deployment rule.



The experiment remains a historical structural analysis.



\---



\# Experiment 115 Status



Experiment 115: COMPLETE



Primary structural result:



\\\[

\\boxed{

8/8

\\text{ harmful support expansions occur under action 1}

}

\\]



and:



\\\[

\\boxed{

0/55

\\text{ action-2 support expansions are harmful}.

}

\\]



Best pooled action-conditioned model:



\\\[

\\boxed{

\\texttt{proxy\\\_action\\\_interaction}

}

\\]



with:



\\\[

\\boxed{

\\text{mean AUC}=0.933

}

\\]



\\\[

\\boxed{

\\text{minimum AUC}=0.905.

}

\\]



Relative to severe proxy alone:



\\\[

\\boxed{

\\Delta\\text{mean AUC}=+0.112

}

\\]



\\\[

\\boxed{

\\Delta\\text{minimum AUC}=+0.142.

}

\\]



Within-action-1 risk transfer remains unstable.



No controller rule is authorized.



\---



\# Next Research Direction



The next experiment should replicate the action-association result on an independent already-consumed historical population.



The replication should be specified before observing its harmful-event distribution.



A suitable earlier historical block should:



\- exclude seeds `44071–44110`;

\- use the same support-expansion definition;

\- use the same action identity definition;

\- use the same harmful-versus-beneficial outcome definition;

\- avoid fitting a new threshold;

\- and report action-specific harmful rates directly.



The primary replication question should be:



\\\[

\\boxed{

\\text{Does harmful support expansion again concentrate under action 1?}

}

\\]



The primary replication outputs should include:



\\\[

N(A=1),

\\quad

N(H\\mid A=1),

\\quad

N(A=2),

\\quad

N(H\\mid A=2).

\\]



Only if the structural action association replicates independently should a later experiment evaluate whether action identity deserves a role in a prospective or action-conditioned controller design.

