\# Experiment 095 — Pre-Action Consequence-Underestimation Risk Analysis



\## Objective



Experiment 094 established that harmful responsive expansions are strongly associated with post-outcome absolute consequence underestimation.



For harmful events:



\\\[

\\hat L\_a-L(x,a)

\\]



was strongly negative, indicating that the learned loss model substantially underestimated realized consequence.



However, this calibration error is only observable after the action outcome is known.



Experiment 095 therefore asks whether severe future underestimation can be predicted using only information available before action execution.



The central question is:



\\\[

\\boxed{

\\text{Can severe future consequence underestimation be recognized}

\\atop

\\text{from pre-action information alone?}

}

\\]



No controller threshold is defined.



No new prospective seed block is consumed.



The experiment is retrospective and diagnostic.



\---



\# Analysis Population



The analysis uses the existing beneficial and harmful expansion events from generation seeds:



\\\[

44001,\\ldots,44010.

\\]



The total event population is:



\\\[

\\boxed{

65

}

\\]



responsive expansion events.



\---



\# Severe Underestimation Target



For expanded action \\(a\\), define action-level prediction error:



\\\[

e\_a

=

\\hat L\_a-L(x,a).

\\]



Experiment 095 defines severe consequence underestimation as:



\\\[

\\boxed{

e\_a<-0.05.

}

\\]



This threshold defines the retrospective target only.



It is not a controller parameter.



The population contains:



\\\[

\\boxed{

15

}

\\]



severe-underestimation events and:



\\\[

\\boxed{

50

}

\\]



non-severe events.



Thus the severe-event fraction is:



\\\[

\\boxed{

23.077\\%.

}

\\]



\---



\# Candidate Pre-Action Information



All classifier inputs are available before the expanded action is executed.



The tested feature families include:



\- predicted loss floor,

\- predicted loss ceiling,

\- predicted loss spread,

\- predicted expanded-action loss,

\- the existing predicted-risk stack,

\- transient-state variables,

\- and compact combinations of these quantities.



No model receives:



\\\[

L(x,a),

\\]



\\\[

e\_a,

\\]



or any other realized post-action quantity as an input.



\---



\# Predicted Loss Floor



Mean predicted loss floor is:



\\\[

0.117655

\\]



for non-severe events and:



\\\[

\\boxed{

0.138805

}

\\]



for severe-underestimation events.



Difference:



\\\[

+0.021150.

\\]



Standardized effect:



\\\[

\\boxed{

+0.493.

}

\\]



Thus severe future underestimation is associated with an elevated predicted loss floor.



\---



\# Predicted Loss Mean



Predicted mean loss changes from:



\\\[

0.126456

\\]



to:



\\\[

\\boxed{

0.151239.

}

\\]



Difference:



\\\[

+0.024782.

\\]



Standardized effect:



\\\[

\\boxed{

+0.547.

}

\\]



\---



\# Predicted Loss Ceiling



Predicted loss ceiling provides the strongest univariate pre-action separation.



Non-severe mean:



\\\[

0.135506.

\\]



Severe-underestimation mean:



\\\[

\\boxed{

0.162244.

}

\\]



Difference:



\\\[

\\boxed{

+0.026738.

}

\\]



Standardized effect:



\\\[

\\boxed{

+0.579.

}

\\]



Therefore:



\\\[

\\boxed{

C(x)\\uparrow

\\Rightarrow

P(\\text{future severe consequence underestimation})\\uparrow

}

\\]



retrospectively.



\---



\# Predicted Loss Spread



Predicted loss spread increases from:



\\\[

0.017851

\\]



to:



\\\[

\\boxed{

0.023438.

}

\\]



Difference:



\\\[

+0.005588.

\\]



Standardized effect:



\\\[

\\boxed{

+0.408.

}

\\]



Thus more action-sensitive predicted loss surfaces are also associated with greater calibration-failure risk.



\---



\# Predicted Expanded-Action Loss



Predicted action loss changes from:



\\\[

0.117665

\\]



to:



\\\[

\\boxed{

0.138805.

}

\\]



Standardized effect:



\\\[

\\boxed{

+0.493.

}

\\]



As in Experiment 094, the expanded action is usually approximately the predicted loss-floor action.



\---



\# Existing Predicted Risk



Predicted risk changes only from:



\\\[

0.032973

\\]



to:



\\\[

0.033474.

\\]



The standardized effect is:



\\\[

\\boxed{

+0.040.

}

\\]



Thus the existing risk model carries almost no univariate information about future severe absolute loss underestimation in this event population.



\---



\# Safety Score



Mean safety score changes from:



\\\[

0.843679

\\]



to:



\\\[

0.816334.

\\]



Difference:



\\\[

\-0.027346.

\\]



Standardized effect:



\\\[

\\boxed{

\-0.207.

}

\\]



There is some directional information, but the separation is modest.



\---



\# Predicted Downside



Predicted downside changes from:



\\\[

0.003303

\\]



to:



\\\[

0.004093.

\\]



Standardized effect:



\\\[

\\boxed{

+0.102.

}

\\]



This is weak separation.



\---



\# Transient-State Variables



The transient-state variables show moderate but secondary association.



\## Current Mismatch



\\\[

0.220733

\\rightarrow

0.260055

\\]



with effect:



\\\[

+0.210.

\\]



\## Anchor Age



\\\[

27.720

\\rightarrow

\\boxed{

20.933.

}

\\]



Standardized effect:



\\\[

\\boxed{

\-0.471.

}

\\]



\## Trigger Score



\\\[

6.619867

\\rightarrow

6.463268

\\]



with effect:



\\\[

\-0.125.

\\]



Among the transient variables, anchor age provides the strongest separation.



\---



\# Best Pre-Action Model



The best pooled leave-one-generation-seed-out classifier is:



\\\[

\\boxed{

\\text{predicted loss ceiling only}.

}

\\]



Its performance is:



\\\[

\\boxed{

67.667\\%

\\text{ balanced accuracy}

}

\\]



with:



\\\[

\\boxed{

73.333\\%

\\text{ severe-underestimation recall}

}

\\]



\\\[

36.667\\%

\\text{ severe precision}

\\]



\\\[

62.000\\%

\\text{ non-severe specificity}

\\]



and:



\\\[

\\boxed{

\\text{ROC-AUC}=0.652.

}

\\]



Mean fold balanced accuracy is:



\\\[

74.774\\%.

\\]



Mean fold ROC-AUC is:



\\\[

0.805.

\\]



Because the event population is small, the pooled metrics should remain the primary conservative reference.



\---



\# Loss-Ceiling Coefficient Stability



The standardized coefficient for predicted loss ceiling is:



\\\[

\\boxed{

+0.667.

}

\\]



Its sign is stable across:



\\\[

\\boxed{

100\\%

}

\\]



of evaluated folds.



Thus the direction of the relationship is extremely stable:



\\\[

\\boxed{

\\text{higher predicted ceiling}

\\rightarrow

\\text{greater severe-underestimation risk}.

}

\\]



\---



\# Loss Surface Compact Model



The compact loss-surface model contains:



\\\[

F(x),

\\]



\\\[

C(x),

\\]



and:



\\\[

S(x).

\\]



It achieves:



\\\[

66.333\\%

\\]



balanced accuracy,



\\\[

66.667\\%

\\]



severe recall,



\\\[

66.000\\%

\\]



non-severe specificity,



and:



\\\[

0.651

\\]



ROC-AUC.



Thus the full compact surface does not outperform the ceiling alone.



\---



\# Compact Loss-Surface Coefficients



All three coefficients are positive and fully sign-stable:



\\\[

\\beta\_C

=

+0.327,

\\]



\\\[

\\beta\_F

=

+0.275,

\\]



and:



\\\[

\\beta\_S

=

+0.256.

\\]



Each has:



\\\[

\\boxed{

100\\%

}

\\]



sign stability.



This confirms that elevated loss-surface level and spread are coherently associated with future calibration failure.



\---



\# Existing Risk Stack



The existing risk stack combines:



\\\[

\\text{predicted risk},

\\]



\\\[

\\text{safety score},

\\]



and:



\\\[

\\text{predicted downside}.

\\]



Its pooled performance is:



\\\[

\\boxed{

28.000\\%

\\text{ balanced accuracy}

}

\\]



with:



\\\[

\\boxed{

0.000\\%

\\text{ severe recall}

}

\\]



and:



\\\[

\\boxed{

\\text{ROC-AUC}=0.227.

}

\\]



This is a major negative result.



The existing safety-risk machinery does not successfully identify the future absolute-consequence underestimation events that dominate Experiment 094.



\---



\# Risk-Stack Coefficient Instability



Within the risk stack:



\\\[

\\beta\_{\\text{safety}}

\\approx

\-0.255,

\\]



\\\[

\\beta\_{\\text{downside}}

\\approx

\-0.138,

\\]



and:



\\\[

\\beta\_{\\text{risk}}

\\approx

+0.017.

\\]



The first two signs are only:



\\\[

88.889\\%

\\]



stable, while predicted risk has only:



\\\[

55.556\\%

\\]



dominant sign stability.



Thus the existing risk representation is not only weak but comparatively unstable for this target.



\---



\# Connection to Experiment 090



Experiment 090 showed that the harder prospective regime exhibited:



\- greater realized under-persistence,

\- larger predicted loss separation,

\- lower predicted risk,

\- lower predicted downside,

\- and higher safety confidence.



Experiment 095 provides event-level confirmation of the same architectural inconsistency.



Future severe loss underestimation is associated with elevated predicted loss-surface severity, while:



\\\[

\\boxed{

\\text{the existing risk stack provides little warning}.

}

\\]



This suggests that the learned consequence model and the safety-risk models are capturing different aspects of the operating regime.



\---



\# Transient-State Model



The transient-state representation achieves:



\\\[

\\boxed{

61.333\\%

\\text{ balanced accuracy}

}

\\]



with:



\\\[

66.667\\%

\\]



severe recall,



\\\[

56.000\\%

\\]



non-severe specificity,



and:



\\\[

0.585

\\]



ROC-AUC.



This is weaker than loss ceiling but materially stronger than the risk stack.



\---



\# Transient-State Coefficients



Anchor age has the strongest coefficient:



\\\[

\\boxed{

\-0.567

}

\\]



with:



\\\[

100\\%

\\]



sign stability.



Mismatch contributes:



\\\[

+0.206

\\]



with:



\\\[

100\\%

\\]



sign stability.



Trigger score contributes little:



\\\[

\-0.020.

\\]



Thus future calibration failures tend to occur in younger-anchor and somewhat higher-mismatch transient contexts.



\---



\# Adding State to Loss Geometry



The `loss\_plus\_state` representation performs worse than loss ceiling alone.



Balanced accuracy:



\\\[

55.333\\%.

\\]



ROC-AUC:



\\\[

0.605.

\\]



Although predicted loss ceiling remains positively stable within the model:



\\\[

\\beta\_C

=

+0.502,

\\]



the additional state variables do not improve overall held-out discrimination.



\---



\# Adding Existing Risk to Loss Geometry



The `loss\_plus\_risk` model performs:



\\\[

54.333\\%

\\]



balanced accuracy with:



\\\[

0.516

\\]



ROC-AUC.



This is substantially worse than loss ceiling alone.



Therefore the existing risk variables dilute rather than strengthen the most useful calibration-risk signal in this small retrospective population.



\---



\# Full Compact Pre-Action Model



The broadest compact model combines:



\- loss ceiling,

\- loss spread,

\- predicted risk,

\- safety score,

\- downside,

\- mismatch,

\- anchor age,

\- trigger score.



Its balanced accuracy is only:



\\\[

\\boxed{

48.667\\%.

}

\\]



ROC-AUC is:



\\\[

0.493.

\\]



Thus increasing feature count does not improve the mechanism.



This reinforces the value of simple interpretable representations.



\---



\# Simplicity Result



Experiment 095 therefore provides another strong example where:



\\\[

\\boxed{

\\text{more features}

\\neq

\\text{better held-out behavior}.

}

\\]



The simplest useful pre-action model:



\\\[

\\boxed{

C(x)

=

\\max\_a\\hat L\_a(x)

}

\\]



outperforms all tested multivariate alternatives.



\---



\# Severe-Underestimation Prediction Is Only Partial



Experiment 095 answers its central question affirmatively, but only partially.



A pre-action signal does exist.



The best candidate achieves:



\\\[

67.667\\%

\\]



balanced accuracy and:



\\\[

73.333\\%

\\]



severe-event recall.



However:



\\\[

\\text{ROC-AUC}=0.652

\\]



remains moderate.



Thus:



\\\[

\\boxed{

\\text{future severe consequence underestimation is partly predictable}

}

\\]



but:



\\\[

\\boxed{

\\text{the current signal is not yet strong enough to be treated}

\\atop

\\text{as a validated calibration-risk guard}.

}

\\]



\---



\# Small-Sample Limitation



Only:



\\\[

15

\\]



severe-underestimation events are available.



Therefore:



\\\[

1

\\]



event corresponds to:



\\\[

6.667

\\]



percentage points of severe recall.



Fold-level metrics can consequently be volatile.



The stronger fold-average values:



\\\[

74.774\\%

\\]



balanced accuracy and:



\\\[

0.805

\\]



AUC should therefore not override the more conservative pooled estimates.



\---



\# What Experiment 095 Establishes



Experiment 095 supports three main conclusions.



\## 1. Loss-Surface Severity Contains Pre-Action Calibration-Risk Information



Higher:



\\\[

F(x),

\\]



\\\[

M(x),

\\]



\\\[

C(x),

\\]



and:



\\\[

S(x)

\\]



are all associated with future severe consequence underestimation.



\---



\## 2. Predicted Loss Ceiling Is the Best Compact Signal



The strongest simple representation is:



\\\[

\\boxed{

C(x)=\\max\_a\\hat L\_a(x).

}

\\]



It is interpretable, deployable before action, and directionally stable across all folds.



\---



\## 3. Existing Risk Signals Do Not Capture This Failure Mode



The current predicted-risk, safety, and downside stack performs poorly for calibration-failure prediction.



Therefore:



\\\[

\\boxed{

\\text{calibration risk is not equivalent to the controller's}

\\atop

\\text{existing safety-risk representation}.

}

\\]



This is an important architectural distinction.



\---



\# What Experiment 095 Does Not Establish



Experiment 095 does not establish:



\- a deployable loss-ceiling threshold,

\- a prospectively validated calibration-risk guard,

\- that the ceiling is universally optimal,

\- that severe calibration failure is fully predictable,

\- or that the existing risk stack should be removed.



The experiment identifies a distinct failure mode and a moderate pre-action signal for that failure.



\---



\# Principal Conclusion



The strongest pre-action indicator of future severe consequence underestimation is:



\\\[

\\boxed{

C(x)

=

\\max\_a\\hat L\_a(x).

}

\\]



Severe events have mean ceiling:



\\\[

\\boxed{

0.162244

}

\\]



versus:



\\\[

0.135506

\\]



for non-severe events.



The standardized effect is:



\\\[

\\boxed{

+0.579.

}

\\]



The leave-one-seed-out ceiling-only model achieves:



\\\[

\\boxed{

67.667\\%

\\text{ balanced accuracy}

}

\\]



and:



\\\[

\\boxed{

73.333\\%

\\text{ severe recall}.

}

\\]



Its coefficient is:



\\\[

\\boxed{

+0.667

}

\\]



with:



\\\[

\\boxed{

100\\%

}

\\]



sign stability.



Therefore:



\\\[

\\boxed{

\\text{elevated predicted loss-surface severity carries}

\\atop

\\text{real but incomplete pre-action information about}

\\atop

\\text{future absolute consequence underestimation}.

}

\\]



\---



\# Final Architectural Interpretation



The accumulated experiments now distinguish at least three different concepts:



\\\[

\\boxed{

\\text{context epistemic support}

}

\\]



\\\[

\\boxed{

\\text{transient-state risk}

}

\\]



and:



\\\[

\\boxed{

\\text{absolute consequence calibration risk}.

}

\\]



These are not interchangeable.



The existing risk stack is useful for some controller decisions but does not identify the severe underestimation mechanism revealed in Experiment 094.



Loss-surface severity appears to carry a separate warning signal.



\---



\# Next Research Direction



Experiment 096 should remain retrospective.



Rather than searching another classifier family, it should analyze the threshold geometry of:



\\\[

\\boxed{

C(x)

}

\\]



directly.



The central question should be whether severe-underestimation events are concentrated in a coherent high-ceiling region.



The analysis should sweep interpretable ceiling thresholds and report, for each threshold:



\- severe-event recall,

\- non-severe specificity,

\- precision,

\- fraction of events flagged,

\- harmful-expansion recall,

\- beneficial-expansion preservation,

\- and seed-level stability.



The purpose should not be to optimize a controller threshold yet.



Instead, Experiment 096 should determine whether:



\\\[

\\boxed{

\\text{the ceiling signal has a stable operational boundary}

}

\\]



or whether the logistic relationship is diffuse across the full range.



If a narrow range of thresholds consistently provides useful severe-event concentration across seeds, a later experiment may preregister one threshold before evaluating an untouched prospective seed block.

