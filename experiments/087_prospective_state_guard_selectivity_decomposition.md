\# Experiment 087 — Prospective State-Guard Selectivity Decomposition



\## Objective



Experiment 086 prospectively validated a frozen transient-state guard on previously untouched generation seeds:



\\\[

44011\\text{--}44030.

\\]



The preregistered primary state threshold:



\\\[

\\tau\_h=0.50

\\]



reduced harmful support-aware expansions from:



\\\[

0.30

\\]



to:



\\\[

0.05

\\]



per seed while also reducing mean regret and under-persistence.



However, this safety improvement came with a responsiveness cost.



Beneficial expansion preservation was only approximately:



\\\[

66\\%.

\\]



Experiment 087 therefore analyzes the saved prospective event-level results from Experiment 086 to determine why the validated transient-state guard vetoes some genuinely beneficial responsive actions.



No new model is trained.



No generation seeds are regenerated.



No controller threshold is changed.



The central question is:



\\\[

\\boxed{

\\text{What distinguishes correctly vetoed harmful expansions}

\\atop

\\text{from unnecessarily vetoed beneficial expansions?}

}

\\]



\---



\# Validation Boundary



Experiment 087 analyzes only the previously saved file:



`results/frozen\_transient\_state\_guard\_prospective\_validation\_events.csv`



The analysis is restricted to the preregistered primary Experiment 086 specification:



\\\[

\\boxed{

\\tau\_h=0.50.

}

\\]



Because seeds:



\\\[

44011\\text{--}44030

\\]



have already been observed, all findings from Experiment 087 are retrospective with respect to this seed population.



Therefore:



\\\[

\\boxed{

\\text{Experiment 087 is diagnostic and hypothesis-generating.}

}

\\]



No new guard derived from these results may be described as prospectively validated on the same seeds.



\---



\# Baseline Expansion Population



Under the support-aware baseline, the twenty prospective seeds produced:



\\\[

\\boxed{

120

}

\\]



action-changing expansion events.



The state guard partitions those baseline events according to:



1\. realized baseline outcome,

2\. whether the \\(0.50\\) state guard vetoed the expansion.



This creates the following categories:



\\\[

\\text{harmful + vetoed}

\\]



\\\[

\\text{harmful + preserved}

\\]



\\\[

\\text{beneficial + vetoed}

\\]



\\\[

\\text{beneficial + preserved}

\\]



with neutral events retained separately.



\---



\# Selectivity Counts



The observed prospective event decomposition is:



\\\[

\\boxed{

5

\\text{ harmful vetoed}

}

\\]



\\\[

\\boxed{

1

\\text{ harmful preserved}

}

\\]



\\\[

\\boxed{

36

\\text{ beneficial vetoed}

}

\\]



\\\[

\\boxed{

64

\\text{ beneficial preserved}

}

\\]



\\\[

3

\\text{ neutral vetoed}

\\]



and:



\\\[

11

\\text{ neutral preserved}.

\\]



Thus the complete event population is:



\\\[

5+1+36+64+3+11

=

120\.

\\]



\---



\# Pooled Harmful-Veto Recall



There are:



\\\[

6

\\]



harmful baseline expansion events in total.



The guard vetoes:



\\\[

5\.

\\]



Therefore pooled harmful-veto recall is:



\\\[

\\boxed{

\\frac{5}{6}

=

83.333\\%.

}

\\]



This confirms the aggregate interpretation of Experiment 086.



The state guard captures most harmful expansions.



\---



\# Pooled Beneficial Preservation



There are:



\\\[

100

\\]



beneficial baseline expansion events.



The guard preserves:



\\\[

64\.

\\]



Therefore pooled beneficial preservation is:



\\\[

\\boxed{

64.000\\%.

}

\\]



Thus:



\\\[

36\\%

\\]



of beneficial responsive expansions are unnecessarily vetoed.



This is the selectivity cost investigated by Experiment 087.



\---



\# Total Veto Burden



The state guard vetoes:



\\\[

\\boxed{

44

}

\\]



of the 120 baseline expansion events.



These vetoes consist of:



\\\[

5

\\text{ harmful},

\\]



\\\[

36

\\text{ beneficial},

\\]



and:



\\\[

3

\\text{ neutral}.

\\]



Therefore the majority of state vetoes are applied to actions that would have been beneficial.



The controller is highly effective at harmful-event recall but remains conservative in its veto precision.



\---



\# Harmful Vetoed Events



For the five correctly vetoed harmful events, mean state-risk probability is:



\\\[

\\boxed{

0.714466.

}

\\]



Median probability is:



\\\[

0.724449.

\\]



The range is:



\\\[

\[0.592361,\\ 0.775668].

\\]



Thus all correctly vetoed harmful events lie clearly above the preregistered:



\\\[

0.50

\\]



state-risk threshold.



\---



\# Harmful Vetoed — State Variables



Mean current mismatch is:



\\\[

\\boxed{

0.506451.

}

\\]



Median mismatch is:



\\\[

0.642392.

\\]



Mean anchor age is:



\\\[

\\boxed{

17.600.

}

\\]



Median anchor age is:



\\\[

16\.

\\]



Mean trigger score is:



\\\[

\\boxed{

7.265001.

}

\\]



These events therefore remain broadly consistent with the transient-state mechanism identified in Experiments 084–086.



\---



\# Harmful Vetoed — Existing Gate Diagnostics



Mean support distance is:



\\\[

\\boxed{

2.276374.

}

\\]



Median support distance is:



\\\[

2.276560.

\\]



Mean safe-action probability is:



\\\[

0.753282.

\\]



Mean predicted downside is:



\\\[

0.006746.

\\]



Thus these harmful events remain:



\- apparently safe,

\- low-downside under the learned model,

\- and technically inside the frozen support boundary,



while lying relatively close to the upper edge of the admitted support region.



\---



\# Harmful Preserved Event



Only one harmful expansion is missed by the state guard.



Its state-risk probability is:



\\\[

\\boxed{

0.130718.

}

\\]



This is far below the preregistered veto threshold.



Its current mismatch is:



\\\[

\\boxed{

0.004101,

}

\\]



which is extremely small.



Anchor age is:



\\\[

19\.

\\]



Trigger score is:



\\\[

\\boxed{

10.795117.

}

\\]



Support distance is:



\\\[

2.291565.

\\]



Safe-action confidence is:



\\\[

0.686799.

\\]



Predicted downside is:



\\\[

0.008558.

\\]



This event does not resemble the transient-state pattern learned in Experiment 085.



Therefore the missed harmful event appears to belong to a different failure regime.



\---



\# Mechanistic Implication of the Missed Harmful Event



The state guard is highly effective against the failure mechanism it was designed to detect.



However:



\\\[

\\boxed{

\\text{not all harmful expansions are transient-state failures}.

}

\\]



The single missed event has:



\\\[

\\text{low mismatch},

\\]



\\\[

\\text{moderate anchor age},

\\]



and:



\\\[

\\text{high trigger score}.

\\]



Thus the current state classifier cannot reasonably be expected to identify it based on its frozen three-variable representation.



This indicates that at least one additional harmful-expansion mechanism remains possible.



\---



\# Beneficial Vetoed Events



The 36 unnecessarily vetoed beneficial events have mean state-risk probability:



\\\[

\\boxed{

0.741758.

}

\\]



This is actually slightly larger than the mean for harmful-vetoed events:



\\\[

0.714466.

\\]



The standardized difference is:



\\\[

\-0.189.

\\]



Thus once an event has crossed the veto boundary:



\\\[

\\boxed{

\\text{state-risk probability itself does not distinguish}

\\atop

\\text{necessary from unnecessary vetoes}.

}

\\]



This is a central Experiment 087 result.



\---



\# Beneficial Vetoed — State Variables



Mean current mismatch is:



\\\[

0.579390,

\\]



slightly larger than harmful-vetoed mismatch:



\\\[

0.506451.

\\]



Mean anchor age is:



\\\[

14.556,

\\]



compared with:



\\\[

17.600

\\]



for harmful-vetoed events.



Mean trigger score is:



\\\[

7.028511,

\\]



compared with:



\\\[

7.265001.

\\]



These differences are modest.



Therefore the same state signature appears in both:



\\\[

\\text{correct harmful vetoes}

\\]



and:



\\\[

\\text{incorrect beneficial vetoes}.

\\]



The state model is accurately identifying a transient-looking regime, but transient appearance alone does not imply that responsive action is unsafe.



\---



\# Beneficial Preserved Events



The 64 beneficial preserved events have substantially lower state-risk probability:



\\\[

\\boxed{

0.302681.

}

\\]



Mean mismatch is:



\\\[

\\boxed{

0.111855.

}

\\]



Mean anchor age is:



\\\[

\\boxed{

24.594.

}

\\]



Mean trigger score is:



\\\[

7.903136.

\\]



These values differ strongly from the beneficial-vetoed population.



Thus the state guard is clearly partitioning the prospective operating space according to the intended transient-state signature.



\---



\# Beneficial Vetoed Versus Beneficial Preserved



The strongest standardized separation is state-risk probability:



\\\[

\\boxed{

d=+3.095.

}

\\]



Mean values are:



\\\[

0.741758

\\]



versus:



\\\[

0.302681.

\\]



Current mismatch also strongly separates the groups:



\\\[

\\boxed{

d=+1.591.

}

\\]



Mean mismatch is:



\\\[

0.579390

\\]



for beneficial vetoes versus:



\\\[

0.111855

\\]



for beneficial preserved events.



Anchor age separates them in the expected direction:



\\\[

\\boxed{

d=-0.808.

}

\\]



Thus the state model is not behaving randomly.



It robustly identifies a particular adaptation regime.



The problem is that the identified regime contains both:



\\\[

\\text{harmful}

\\]



and:



\\\[

\\text{beneficial}

\\]



responsive opportunities.



\---



\# State Risk Is Necessary but Not Sufficient



Experiment 087 therefore refines the interpretation of transient-state risk.



High state risk is associated with the region in which harmful expansions occur.



But many beneficial actions also occur inside that same region.



Therefore:



\\\[

\\boxed{

\\text{high transient-state risk is not sufficient evidence}

\\atop

\\text{that a responsive action should be vetoed}.

}

\\]



The state model identifies when extra caution may be warranted.



It does not, by itself, determine whether the responsive action is actually unsafe.



\---



\# Harmful Vetoed Versus Beneficial Vetoed



This is the most important selectivity comparison.



Both groups already satisfy:



\\\[

q\_{\\text{state}}\\ge0.50.

\\]



Therefore the question becomes:



\\\[

\\boxed{

\\text{What additional information distinguishes necessary}

\\atop

\\text{from unnecessary state vetoes?}

}

\\]



\---



\# Support Distance Emerges as the Strongest Signal



Harmful-vetoed mean support distance is:



\\\[

\\boxed{

2.276374.

}

\\]



Beneficial-vetoed mean support distance is:



\\\[

1.998112.

\\]



The standardized difference is:



\\\[

\\boxed{

+0.946.

}

\\]



This is the strongest prospective diagnostic separation between the two vetoed groups.



Thus even within the already-admitted region:



\\\[

d\_5\\le2.50,

\\]



harmful events remain systematically farther from direct training support.



\---



\# Why This Is Important



Experiment 080 originally identified support extrapolation as a harmful-expansion mechanism.



Experiment 081 converted support distance into a controller gate.



Experiment 087 now shows that support distance retains additional information even \*\*inside\*\* the admitted support region.



Therefore support should not necessarily be interpreted only as a binary condition:



\\\[

d\_5\\le2.50.

\\]



Instead, its magnitude may remain informative after admission.



Conceptually:



\\\[

\\boxed{

\\text{support is graded, not merely binary}.

}

\\]



\---



\# Predicted Downside



Harmful-vetoed mean predicted downside is:



\\\[

0.006746.

\\]



Beneficial-vetoed mean downside is:



\\\[

0.004408.

\\]



Standardized separation is:



\\\[

\\boxed{

+0.400.

}

\\]



This is weaker than support distance but moves in the expected direction.



Therefore the downside model also retains some information within the state-vetoed region.



\---



\# Anchor Age



Harmful-vetoed events have mean anchor age:



\\\[

17.600

\\]



while beneficial-vetoed events have:



\\\[

14.556.

\\]



The standardized difference is:



\\\[

+0.307.

\\]



Interestingly, harmful vetoes have somewhat older anchors than beneficial vetoes.



This indicates that the original younger-anchor risk direction is not useful for distinguishing harmful from beneficial events after conditioning on a state veto.



\---



\# State Probability



Harmful-vetoed state probability:



\\\[

0.714466.

\\]



Beneficial-vetoed:



\\\[

0.741758.

\\]



Standardized difference:



\\\[

\-0.189.

\\]



Therefore increasing the state probability threshold alone is unlikely to solve the selectivity problem cleanly.



The beneficial false-positive vetoes are, if anything, assigned slightly greater state risk.



\---



\# Current Mismatch



Harmful-vetoed mismatch:



\\\[

0.506451.

\\]



Beneficial-vetoed mismatch:



\\\[

0.579390.

\\]



Standardized difference:



\\\[

\-0.163.

\\]



Thus mismatch also fails to distinguish necessary from unnecessary vetoes once the state-risk threshold has already been crossed.



\---



\# Trigger Score



Harmful-vetoed mean trigger score:



\\\[

7.265001.

\\]



Beneficial-vetoed mean:



\\\[

7.028511.

\\]



Standardized difference:



\\\[

+0.079.

\\]



This is effectively weak separation.



\---



\# Safety Probability



Harmful-vetoed safe-action probability:



\\\[

0.753282.

\\]



Beneficial-vetoed:



\\\[

0.754235.

\\]



Standardized difference:



\\\[

\\boxed{

\-0.011.

}

\\]



Thus safe-action confidence remains essentially non-discriminative.



This is consistent with several previous experiments.



\---



\# Ranked Selectivity Signals



For harmful-vetoed versus beneficial-vetoed events, the observed standardized effects are approximately:



\\\[

\\boxed{

\\text{support distance}=+0.946

}

\\]



\\\[

\\boxed{

\\text{downside score}=+0.400

}

\\]



\\\[

\\text{anchor age}=+0.307

\\]



\\\[

\\text{state probability}=-0.189

\\]



\\\[

\\text{current mismatch}=-0.163

\\]



\\\[

\\text{trigger score}=+0.079

\\]



\\\[

\\text{safety probability}=-0.011.

\\]



The dominant selectivity signal is therefore:



\\\[

\\boxed{

\\text{support distance}.

}

\\]



\---



\# Emerging Interaction Hypothesis



The prospective state guard successfully identifies a transient-risk region.



Within that region, harmful events occur at larger support distances than beneficial events.



This suggests a possible interaction:



\\\[

\\boxed{

\\text{transient-state risk}

\\times

\\text{weak training support}.

}

\\]



Conceptually, harmful responsive expansion may require both:



1\. a dynamically transient state,

2\. insufficiently strong local support for trusting the responsive action.



This can be written abstractly as:



\\\[

\\boxed{

\\text{harm risk}

\\approx

f(

q\_{\\text{state}},

d\_{\\text{support}}

).

}

\\]



\---



\# Revised Mechanistic Interpretation



The previous architecture treated state risk as an independent veto layer.



Experiment 087 suggests a more nuanced interpretation.



A high state-risk probability may mean:



> the system is currently in a transient adaptation regime.



But whether expansion is actually unsafe may depend on whether there is strong enough local evidence to support responsiveness inside that transient regime.



Thus:



\\\[

\\boxed{

\\text{transience may require support-conditioned interpretation}.

}

\\]



\---



\# High State Risk + Stronger Support



Many beneficial vetoed events exhibit:



\\\[

q\_{\\text{state}}\\ge0.50

\\]



but relatively strong local support.



These may represent contexts where the system appears dynamically transient but the learned action has enough nearby empirical support to remain safe.



\---



\# High State Risk + Weaker Support



Correctly vetoed harmful events have similar state probabilities but systematically larger support distances.



These may represent contexts where:



\\\[

\\text{transience}

\\]



and:



\\\[

\\text{epistemic weakness}

\\]



coincide.



This combination is a plausible candidate mechanism for the harmful events captured by the state guard.



\---



\# Why No Threshold Is Selected in Experiment 087



The observed means:



\\\[

2.276

\\]



for harmful vetoes and:



\\\[

1.998

\\]



for beneficial vetoes might tempt a new support cutoff.



That would be methodologically inappropriate.



The seeds:



\\\[

44011\\text{--}44030

\\]



have already been used to generate these observations.



Therefore choosing a threshold from them and evaluating that threshold on the same events would create retrospective optimization.



Accordingly:



\\\[

\\boxed{

\\text{Experiment 087 defines no new controller threshold}.

}

\\]



\---



\# Principal Conclusion



Experiment 087 explains the main selectivity limitation of the prospectively validated transient-state guard.



The \\(0.50\\) state guard achieves:



\\\[

\\boxed{

83.333\\%

\\text{ pooled harmful-veto recall}

}

\\]



but preserves only:



\\\[

\\boxed{

64.000\\%

\\text{ of beneficial expansions}.

}

\\]



The state variables strongly distinguish vetoed beneficial events from preserved beneficial events, demonstrating that the guard is correctly identifying its intended transient-state regime.



However, those same state variables do not meaningfully distinguish:



\\\[

\\text{harmful vetoes}

\\]



from:



\\\[

\\text{beneficial vetoes}.

\\]



Within the vetoed population, the strongest discriminating signal is:



\\\[

\\boxed{

\\text{support distance}

}

\\]



with standardized effect:



\\\[

\\boxed{

+0.946.

}

\\]



Therefore:



\\\[

\\boxed{

\\text{transient-state risk appears prospectively useful}

\\atop

\\text{but should likely be interpreted jointly with training support}.

}

\\]



\---



\# Secondary Conclusion



The single harmful event preserved by the state guard has:



\\\[

q\_{\\text{state}}=0.131,

\\]



extremely low mismatch,



and high trigger score.



This event lies outside the transient-state failure signature.



Therefore:



\\\[

\\boxed{

\\text{at least one additional harmful-expansion mechanism remains}.

}

\\]



Future work should avoid forcing every residual harmful event into the transient-state explanation.



\---



\# Next Research Direction



Experiment 088 should remain retrospective and diagnostic.



It should analyze interaction structure within the already-consumed prospective event population, focusing particularly on:



\\\[

q\_{\\text{state}}

\\]



and:



\\\[

d\_{\\text{support}}.

\\]



The central question should be:



\\\[

\\boxed{

\\text{Does a state-risk/support interaction separate correctly}

\\atop

\\text{vetoed harmful expansions from unnecessarily vetoed}

\\atop

\\text{beneficial expansions better than either signal alone?}

}

\\]



Candidate analyses may include:



\- simple interaction terms,

\- two-variable logistic models,

\- leave-one-seed-out evaluation,

\- coefficient stability,

\- probability ranking,

\- and veto-group discrimination.



The analysis must not define a new validated threshold on seeds:



\\\[

44011\\text{--}44030.

\\]



If a compact interaction hypothesis emerges, it should be frozen and evaluated on a new untouched future seed block.



The methodological rule remains:



\\\[

\\boxed{

\\text{diagnose on consumed seeds;

validate only on fresh seeds}.

}

\\]

