\# Experiment 084 — Cross-Seed Harmful-Expansion Feature Decomposition



\## Objective



Experiment 083 showed that the remaining safety cost of support-aware expansion is systematic across the validation population rather than concentrated in only one or two pathological generation seeds.



Across seeds



\\\[

44001\\text{--}44010,

\\]



support-aware expansion at



\\\[

\\tau\_p=0.60,

\\qquad

\\tau\_d=0.020,

\\qquad

\\tau\_s=2.50

\\]



produced recurring harmful action-changing events.



At the seed level, harmful expansion count was strongly associated with consequence degradation:



\\\[

\\rho(

N\_{\\text{harmful}},

\\Delta R

)

=

0.977,

\\]



and:



\\\[

\\rho(

N\_{\\text{harmful}},

\\Delta U

)

=

1.000.

\\]



Experiment 084 therefore moves from seed-level analysis to pooled event-level decomposition.



The controller remains frozen.



No threshold is tuned.



The objective is to determine whether harmful expansions exhibit a stable pre-decision feature signature that distinguishes them from beneficial responsive recoveries.



The central question is:



\\\[

\\boxed{

\\text{Do residual harmful expansions share a cross-seed}

\\atop

\\text{pre-decision signature that beneficial expansions do not?}

}

\\]



\---



\## Validation Boundary



The same ten validation seeds are reused:



\\\[

44001,\\,

44002,\\,

44003,\\,

44004,\\,

44005,\\,

44006,\\,

44007,\\,

44008,\\,

44009,\\,

44010\.

\\]



These seeds have already been used for validation in Experiment 082 and diagnostic decomposition in Experiment 083.



Therefore Experiment 084 is explicitly retrospective.



Any feature separation discovered here must be treated as:



\\\[

\\boxed{

\\text{hypothesis-generating evidence}

}

\\]



rather than prospective controller validation.



Any eventual controller modification based on these findings must be evaluated on fresh untouched generation seeds.



\---



\## Frozen Controller



The support-aware controller remains fixed at:



\\\[

\\boxed{

\\tau\_p=0.60

}

\\]



for safe-membership probability,



\\\[

\\boxed{

\\tau\_d=0.020

}

\\]



for predicted downside,



and:



\\\[

\\boxed{

\\tau\_s=2.50

}

\\]



for mean five-nearest-neighbor support distance.



The admission rule therefore remains:



\\\[

\\hat p\_{\\text{safe}}(a)

\\geq

0.60,

\\]



\\\[

\\hat d(a)

\\leq

0.020,

\\]



and:



\\\[

d\_5(x,a)

\\leq

2.50.

\\]



\---



\# Event Definition



Experiment 084 records only contexts in which support-aware expansion changes the executed persistence action.



For each such event, define the primary action:



\\\[

a\_t^{\\text{primary}}

\\]



and expanded action:



\\\[

a\_t^{\\text{expanded}}.

\\]



The event is considered beneficial when:



\\\[

a\_t^{\\text{expanded}}

=

a\_t^{\\text{responsive}}

\\]



and:



\\\[

R\_t(

a\_t^{\\text{expanded}}

)

\-

R\_t(

a\_t^{\\text{primary}}

)

\\leq

0\.

\\]



It is harmful when:



\\\[

R\_t(

a\_t^{\\text{expanded}}

)

\-

R\_t(

a\_t^{\\text{primary}}

)

>

0\.

\\]



Remaining action-changing events are labeled neutral.



\---



\# Pooled Event Counts



Across all ten validation seeds, the frozen support-aware controller produced:



\\\[

\\boxed{

70

}

\\]



action-changing events.



These decomposed into:



\\\[

\\boxed{

50

\\text{ beneficial events}

}

\\]



\\\[

\\boxed{

15

\\text{ harmful events}

}

\\]



and:



\\\[

\\boxed{

5

\\text{ neutral events}.

}

\\]



Therefore beneficial events outnumber harmful events by:



\\\[

\\frac{50}{15}

\\approx

3.33.

\\]



This confirms that the expansion architecture is useful overall.



The research problem is not to eliminate expansion.



It is to selectively suppress the harmful minority.



\---



\# Standardized Feature Separation



For each diagnostic feature, Experiment 084 computes the standardized difference:



\\\[

d

=

\\frac{

\\mu\_{\\text{harmful}}

\-

\\mu\_{\\text{beneficial}}

}{

s\_{\\text{pooled}}

}.

\\]



Positive values indicate larger values in harmful events.



Negative values indicate smaller values in harmful events.



This provides a scale-independent measure of retrospective separation.



\---



\# Outcome Variables



The strongest standardized separation appears in:



\\\[

\\text{expanded regret}

\\]



and:



\\\[

\\text{incremental regret}.

\\]



Both have:



\\\[

\\boxed{

d=+6.437.

}

\\]



Beneficial events have mean incremental regret:



\\\[

0\.

\\]



Harmful events have mean incremental regret:



\\\[

0.055580.

\\]



The harmful-event range is:



\\\[

\[0.020148,\\ 0.085887].

\\]



These variables confirm that the outcome labels are strongly separated.



However, they are realized post-decision quantities.



Therefore they are:



\\\[

\\boxed{

\\text{not valid prospective controller inputs}.

}

\\]



All actionable interpretation must focus on pre-decision diagnostics.



\---



\# Predicted Loss Level



The strongest actionable separation appears in predicted loss under maximal persistence:



\\\[

\\hat L\_{k3}.

\\]



Beneficial events have mean:



\\\[

0.124578.

\\]



Harmful events have mean:



\\\[

\\boxed{

0.165255.

}

\\]



The standardized effect is:



\\\[

\\boxed{

+0.862.

}

\\]



The harmful range is:



\\\[

\[0.100564,\\ 0.219646].

\\]



Thus harmful expansions tend to occur in contexts that the learned loss models already regard as globally more difficult.



\---



\# Current Mismatch Indicator



A major context-level signal is:



\\\[

\\texttt{current\\\_mismatch\\\_indicator}.

\\]



Beneficial mean:



\\\[

0.195766.

\\]



Harmful mean:



\\\[

\\boxed{

0.343277.

}

\\]



Standardized effect:



\\\[

\\boxed{

+0.832.

}

\\]



The harmful range is:



\\\[

\[0.032006,\\ 0.610080].

\\]



Thus harmful expansions tend to occur under greater current mismatch.



This suggests the controller may be reducing persistence too aggressively when the current system state remains poorly aligned with its model or anchor.



\---



\# Anchor Age



Anchor age shows strong separation in the opposite direction.



Beneficial mean:



\\\[

28.700.

\\]



Harmful mean:



\\\[

\\boxed{

17.667.

}

\\]



Standardized effect:



\\\[

\\boxed{

\-0.792.

}

\\]



The harmful range is:



\\\[

\[2,\\ 36].

\\]



Thus harmful events tend to occur with younger anchors.



This result is especially interesting when combined with the mismatch signal.



The recurring pattern appears to be:



\\\[

\\boxed{

\\text{higher mismatch}

\+

\\text{younger anchor}.

}

\\]



A younger anchor may appear to provide fresh evidence, while the elevated mismatch indicates that the system remains dynamically unsettled.



\---



\# Predicted Loss \\(k=2\\)



Predicted loss at persistence \\(k=2\\) also separates the groups.



Beneficial mean:



\\\[

0.121483.

\\]



Harmful mean:



\\\[

\\boxed{

0.159144.

}

\\]



Standardized effect:



\\\[

\\boxed{

+0.789.

}

\\]



This reinforces the interpretation that harmful expansions arise in generally harder contexts rather than only in ambiguous local decisions.



\---



\# Support Distance



Support distance remains informative even after enforcing:



\\\[

d\_5\\le2.50.

\\]



Beneficial mean:



\\\[

2.054615.

\\]



Harmful mean:



\\\[

\\boxed{

2.245383.

}

\\]



Standardized effect:



\\\[

\\boxed{

+0.689.

}

\\]



The harmful range is:



\\\[

\[1.854452,\\ 2.493644].

\\]



Thus harmful events tend to cluster closer to the upper boundary of the existing support gate.



This shows that the support metric still contains useful information inside the admitted region.



However, the substantial range overlap implies that support distance alone is not sufficient for clean separation.



\---



\# Predicted Loss \\(k=1\\)



Predicted loss for the most responsive persistence action also differs.



Beneficial mean:



\\\[

0.126116.

\\]



Harmful mean:



\\\[

\\boxed{

0.153292.

}

\\]



Standardized effect:



\\\[

+0.675.

\\]



Again, harmful events occur in contexts with generally larger predicted losses.



\---



\# Predicted Loss Surface Shape



Several predicted-loss differences reveal a change in local loss geometry.



\## \\(k=2-k=3\\)



Beneficial mean:



\\\[

\-0.003095.

\\]



Harmful mean:



\\\[

\-0.006110.

\\]



Standardized effect:



\\\[

\-0.694.

\\]



\## \\(k=1-k=3\\)



Beneficial mean:



\\\[

+0.001538.

\\]



Harmful mean:



\\\[

\\boxed{

\-0.011963.

}

\\]



Standardized effect:



\\\[

\-0.632.

\\]



\## \\(k=1-k=2\\)



Beneficial mean:



\\\[

+0.004633.

\\]



Harmful mean:



\\\[

\-0.005853.

\\]



Standardized effect:



\\\[

\-0.479.

\\]



These results indicate that harmful contexts more often contain predicted loss surfaces that favor lower-persistence actions nominally.



In other words, the learned loss model itself frequently supports the responsive move.



The problem is that realized consequence disagrees with that learned local geometry.



\---



\# Trigger Score



The context trigger score also exhibits moderate separation.



Beneficial mean:



\\\[

6.745051.

\\]



Harmful mean:



\\\[

6.045988.

\\]



Standardized effect:



\\\[

\-0.571.

\\]



Thus harmful expansions tend to occur at somewhat lower trigger scores.



This may be relevant to the temporal or change-detection structure of the controller.



However, overlap remains substantial.



\---



\# Predicted Regret Margin



Predicted regret margin is:



\\\[

\\hat R(

a\_{\\text{expanded}}

)

\-

\\hat R(

a\_{\\text{primary}}

).

\\]



Beneficial mean:



\\\[

0.005207.

\\]



Harmful mean:



\\\[

\\boxed{

0.009685.

}

\\]



Standardized effect:



\\\[

\\boxed{

+0.566.

}

\\]



The harmful range is:



\\\[

\[0.000605,\\ 0.037723].

\\]



Thus harmful expansions tend to have a larger predicted-regret penalty than beneficial ones.



This is useful because it is available before execution.



However, the range overlaps strongly with beneficial events.



Therefore predicted regret margin is better viewed as one component of a multivariate risk signature rather than a standalone threshold candidate.



\---



\# Action Step



The average persistence reduction is larger for harmful expansions.



Beneficial mean:



\\\[

1.240.

\\]



Harmful mean:



\\\[

\\boxed{

1.467.

}

\\]



Standardized effect:



\\\[

\\boxed{

+0.502.

}

\\]



The harmful range includes both:



\\\[

1

\\]



and:



\\\[

2

\\]



step reductions.



Thus larger jumps toward responsiveness are somewhat more dangerous, but action-step size alone does not explain the failures.



\---



\# Predicted Downside



Predicted downside is higher in harmful events, though separation is moderate.



Beneficial mean:



\\\[

0.002542.

\\]



Harmful mean:



\\\[

\\boxed{

0.004480.

}

\\]



Standardized effect:



\\\[

\\boxed{

+0.400.

}

\\]



The harmful range is:



\\\[

\[0,\\ 0.016664].

\\]



This means the downside model is not completely blind to the harmful events.



On average it assigns them higher risk.



However, all remain below the frozen admission threshold:



\\\[

0.020.

\\]



Therefore the existing downside threshold is not sufficiently discriminative by itself.



\---



\# Safety Probability



Safety probability provides almost no separation.



Beneficial mean:



\\\[

0.812241.

\\]



Harmful mean:



\\\[

0.814908.

\\]



Standardized effect:



\\\[

\\boxed{

+0.024.

}

\\]



Thus:



\\\[

\\boxed{

\\hat p\_{\\text{safe}}

\\text{ is essentially non-discriminative within the admitted event set}.

}

\\]



This confirms the earlier single-seed findings from Experiments 078 and 079.



The harmful events are not low-confidence classifier decisions.



\---



\# Predicted Under-Persistence Risk



Predicted under-persistence risk also separates weakly.



Beneficial mean:



\\\[

0.032608.

\\]



Harmful mean:



\\\[

0.034693.

\\]



Standardized effect:



\\\[

+0.168.

\\]



Thus the existing under-risk estimator alone does not identify the residual harmful events.



\---



\# Core Gate Diagnostic Ranking



Among the variables already used directly or indirectly by the expansion gate, retrospective standardized separation is approximately:



\\\[

\\boxed{

\\text{support distance}

=

+0.689

}

\\]



\\\[

\\boxed{

\\text{predicted regret margin}

=

+0.566

}

\\]



\\\[

\\boxed{

\\text{action step}

=

+0.502

}

\\]



\\\[

\\boxed{

\\text{downside score}

=

+0.400

}

\\]



\\\[

\\boxed{

\\text{predicted under risk}

=

+0.168

}

\\]



\\\[

\\boxed{

\\text{safety score}

=

+0.024.

}

\\]



This ordering strongly suggests that the residual problem is not safe-membership confidence.



It is better characterized by a combination of support proximity, operating difficulty, predicted regret geometry, and transition size.



\---



\# Global Difficulty Signature



Three predicted losses are systematically higher in harmful events:



\\\[

\\hat L\_{k1},

\\quad

\\hat L\_{k2},

\\quad

\\hat L\_{k3}.

\\]



This indicates that harmful expansions tend to occur in globally difficult contexts.



A useful conceptual variable may therefore be a local difficulty statistic such as:



\\\[

D\_t

=

\\frac{

\\hat L\_{k1}

\+

\\hat L\_{k2}

\+

\\hat L\_{k3}

}{

3

}.

\\]



This was not explicitly tested as a controller feature in Experiment 084, but the observed component-wise separation motivates it as a future hypothesis.



\---



\# Mismatch–Anchor Interaction Hypothesis



The two strongest context-specific signals are:



\\\[

\\text{current mismatch}

\\]



and:



\\\[

\\text{anchor age}.

\\]



Harmful events tend to combine:



\\\[

\\boxed{

\\text{larger mismatch}

}

\\]



with:



\\\[

\\boxed{

\\text{younger anchor}.

}

\\]



This may indicate a transition regime where the controller has recently refreshed its anchor but the evolving system has not yet settled into a state where lower persistence is actually safe.



Conceptually, this suggests a possible interaction:



\\\[

I\_t

=

\\frac{

\\text{mismatch}

}{

1+\\text{anchor age}

}.

\\]



Experiment 084 does not test this derived feature.



It only motivates it as a prospective hypothesis.



\---



\# Support-Boundary Hypothesis



Harmful events also occur closer to the current support boundary:



\\\[

2.245

\\]



versus:



\\\[

2.055.

\\]



Because all admitted events satisfy:



\\\[

d\_5\\le2.50,

\\]



the remaining failures may arise from contexts that are technically supported but only weakly so.



However, simply tightening the support threshold retrospectively would risk discarding beneficial events.



The cross-seed evidence therefore favors multivariate analysis rather than another univariate threshold sweep.



\---



\# Predicted-Regret Geometry Hypothesis



Harmful events exhibit larger predicted regret margins:



\\\[

0.009685

\\]



versus:



\\\[

0.005207.

\\]



At the same time, the nominal predicted loss differences often favor lower persistence.



This suggests disagreement between two internal views of the candidate action:



1\. nominal predicted action loss,

2\. predicted consequence-regret structure.



The residual harmful cases may therefore be characterized by inconsistent internal model signals.



A future hypothesis could quantify this disagreement explicitly.



\---



\# Why No New Controller Is Selected Here



Experiment 084 is retrospective.



The ten analyzed seeds have already been used in prior validation and diagnostics.



Selecting a new threshold or feature rule directly from these events and reporting its performance on the same events would introduce adaptive overfitting.



Therefore:



\\\[

\\boxed{

\\text{Experiment 084 does not define a new controller.}

}

\\]



It only identifies candidate signatures for prospective testing.



\---



\# Candidate Multivariate Signature



The strongest actionable pattern suggested by the pooled data is approximately:



\\\[

\\boxed{

\\text{higher global predicted loss}

}

\\]



\\\[

\+

\\]



\\\[

\\boxed{

\\text{higher current mismatch}

}

\\]



\\\[

\+

\\]



\\\[

\\boxed{

\\text{younger anchor}

}

\\]



\\\[

\+

\\]



\\\[

\\boxed{

\\text{larger support distance}

}

\\]



\\\[

\+

\\]



\\\[

\\boxed{

\\text{larger predicted regret margin}

}

\\]



\\\[

\+

\\]



\\\[

\\boxed{

\\text{larger responsive action step}.

}

\\]



No single one of these variables is likely sufficient.



The remaining error appears multivariate.



\---



\# Principal Conclusion



Experiment 084 provides the first pooled cross-seed feature-level view of residual harmful support-aware expansions.



Across ten validation seeds, the frozen controller produced:



\\\[

\\boxed{

50

\\text{ beneficial}

}

\\]



\\\[

\\boxed{

15

\\text{ harmful}

}

\\]



and:



\\\[

\\boxed{

5

\\text{ neutral}

}

\\]



action-changing events.



Safety probability provides essentially no separation:



\\\[

\\boxed{

d=+0.024.

}

\\]



The strongest actionable univariate signals are:



\\\[

\\boxed{

\\hat L\_{k3}: d=+0.862

}

\\]



\\\[

\\boxed{

\\text{current mismatch}: d=+0.832

}

\\]



\\\[

\\boxed{

\\text{anchor age}: d=-0.792

}

\\]



\\\[

\\boxed{

\\hat L\_{k2}: d=+0.789

}

\\]



\\\[

\\boxed{

\\text{support distance}: d=+0.689

}

\\]



\\\[

\\boxed{

\\hat L\_{k1}: d=+0.675

}

\\]



\\\[

\\boxed{

\\text{predicted regret margin}: d=+0.566.

}

\\]



These results suggest that residual harmful expansion is associated with a systematic multivariate operating regime rather than low classifier confidence.



The most plausible interpretation is:



\\\[

\\boxed{

\\text{harder contexts}

\+

\\text{higher mismatch}

\+

\\text{younger anchors}

\+

\\text{weaker support}

\+

\\text{larger responsive transitions}.

}

\\]



\---



\## Next Research Direction



Experiment 085 should perform retrospective multivariate separability analysis using only pre-decision features from the 70 pooled action-changing events.



Realized quantities such as:



\\\[

\\text{expanded regret}

\\]



and:



\\\[

\\text{incremental regret}

\\]



must be excluded from the predictor set.



The analysis should evaluate whether harmful events can be distinguished from beneficial events using combinations of:



\- predicted loss levels,

\- predicted loss differences,

\- current mismatch,

\- anchor age,

\- trigger score,

\- support distance,

\- predicted downside,

\- predicted regret margin,

\- action step,

\- predicted under-persistence risk,

\- and other existing context variables.



Because the event sample is small, the analysis should emphasize:



\- simple models,

\- leave-one-seed-out evaluation,

\- balanced classification metrics,

\- coefficient or feature stability,

\- and avoidance of high-capacity overfitting.



The objective is not to declare a new controller.



It is to determine whether a compact and stable harmful-expansion signature exists across seeds.



The central hypothesis becomes:



\\\[

\\boxed{

\\text{residual harmful expansions are retrospectively separable}

\\atop

\\text{using a compact multivariate pre-decision feature set}.

}

\\]



If this hypothesis is supported, a candidate guard should then be frozen and evaluated prospectively on entirely fresh generation seeds.

