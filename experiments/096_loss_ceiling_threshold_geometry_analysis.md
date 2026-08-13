\# Experiment 096 — Loss-Ceiling Threshold Geometry and Event-Concentration Analysis



\## Objective



Experiment 095 identified predicted loss ceiling,



\\\[

\\boxed{

C(x)=\\max\_a \\hat L\_a(x),

}

\\]



as the strongest compact pre-action indicator of future severe consequence underestimation.



However, Experiment 095 used a logistic classifier and did not establish whether the ceiling signal possesses a coherent operational threshold structure.



Experiment 096 therefore analyzes the retrospective threshold geometry of:



\\\[

\\boxed{

C(x).

}

\\]



The central questions are:



\\\[

\\boxed{

\\text{Are severe-underestimation events concentrated above}

\\atop

\\text{a coherent ceiling boundary?}

}

\\]



and:



\\\[

\\boxed{

\\text{Does a stable tradeoff region exist between severe-event}

\\atop

\\text{recall and preservation of non-severe and beneficial events?}

}

\\]



No new model is trained.



No controller is modified.



No prospective seed block is consumed.



All thresholds are evaluated descriptively on already-consumed event data.



\---



\# Analysis Population



Experiment 096 reads the event-level output of Experiment 095:



`results/pre\_action\_consequence\_underestimation\_risk\_analysis\_events.csv`



The population contains:



\\\[

\\boxed{

65

}

\\]



responsive expansion events.



Among them:



\\\[

\\boxed{

15

}

\\]



are severe-underestimation events,



\\\[

\\boxed{

15

}

\\]



are harmful-expansion events,



and:



\\\[

\\boxed{

50

}

\\]



are beneficial-expansion events.



Thus:



\\\[

\\boxed{

23.077\\%

}

\\]



of events satisfy the severe-underestimation criterion.



\---



\# Severe Underestimation Definition



Experiment 095 defined severe underestimation using:



\\\[

e\_a

=

\\hat L\_a-L(x,a)

\\]



with the target:



\\\[

\\boxed{

e\_a<-0.05.

}

\\]



Experiment 096 retains that target unchanged.



The threshold sweep applies only to:



\\\[

C(x),

\\]



not to the definition of the severe outcome.



\---



\# Ceiling Threshold Rule



For descriptive ceiling threshold:



\\\[

\\tau,

\\]



define:



\\\[

\\boxed{

G\_\\tau(x)

=

\\mathbf 1\[

C(x)\\ge\\tau

].

}

\\]



An event is considered flagged when:



\\\[

C(x)\\ge\\tau.

\\]



The retrospective sweep covers:



\\\[

\\boxed{

0.100

\\le

\\tau

\\le

0.220

}

\\]



in increments of:



\\\[

\\boxed{

0.005.

}

\\]



\---



\# Evaluation Quantities



For each threshold, Experiment 096 reports:



\- fraction of all events flagged,

\- severe-underestimation recall,

\- non-severe specificity,

\- severe-event precision,

\- balanced accuracy,

\- severe-event risk lift,

\- harmful-expansion recall,

\- beneficial-expansion preservation,

\- and seed-level stability.



These statistics describe threshold geometry only.



They are not prospective controller-performance estimates.



\---



\# Low-Threshold Region



At:



\\\[

\\tau=0.100,

\\]



the rule flags:



\\\[

51/65

=

78.462\\%

\\]



of all events.



Severe-underestimation recall is:



\\\[

\\boxed{

100\\%.

}

\\]



However, specificity is only:



\\\[

28.000\\%.

\\]



Severe precision is:



\\\[

29.412\\%.

\\]



Balanced accuracy is:



\\\[

64.000\\%.

\\]



Beneficial preservation is only:



\\\[

28.000\\%.

\\]



Thus very low ceiling thresholds preserve complete severe-event recall only by flagging most of the event population.



\---



\# Transition Toward a Useful Tradeoff Region



As the threshold rises, specificity and beneficial preservation improve while severe recall remains relatively high.



At:



\\\[

\\tau=0.120,

\\]



the rule achieves:



\\\[

86.667\\%

\\]



severe recall and:



\\\[

42.000\\%

\\]



specificity.



At:



\\\[

\\tau=0.125,

\\]



severe recall remains:



\\\[

80.000\\%

\\]



while specificity improves to:



\\\[

50.000\\%.

\\]



At:



\\\[

\\tau=0.130,

\\]



the rule maintains:



\\\[

80.000\\%

\\]



severe recall with:



\\\[

56.000\\%

\\]



specificity.



These results indicate a gradual tradeoff transition rather than an abrupt boundary.



\---



\# Best Pooled Balanced-Accuracy Point



The maximum pooled balanced accuracy occurs at:



\\\[

\\boxed{

\\tau=0.135.

}

\\]



At this threshold:



\\\[

\\boxed{

80.000\\%

}

\\]



of severe-underestimation events are flagged.



Non-severe specificity is:



\\\[

\\boxed{

60.000\\%.

}

\\]



Severe-event precision is:



\\\[

\\boxed{

37.500\\%.

}

\\]



Balanced accuracy is:



\\\[

\\boxed{

70.000\\%.

}

\\]



The flagged fraction is:



\\\[

\\boxed{

49.231\\%.

}

\\]



Thus approximately half of the event population is flagged.



\---



\# Harmful-Expansion Behavior at 0.135



At:



\\\[

\\tau=0.135,

\\]



harmful-expansion recall is:



\\\[

\\boxed{

86.667\\%.

}

\\]



Beneficial-expansion preservation is:



\\\[

\\boxed{

62.000\\%.

}

\\]



Thus the retrospective ceiling boundary identifies most harmful expansion events while preserving a majority of beneficial expansions.



\---



\# Severe-Event Risk Lift at 0.135



The background severe-event prevalence is:



\\\[

23.077\\%.

\\]



Among events flagged at:



\\\[

\\tau=0.135,

\\]



severe-event precision is:



\\\[

37.500\\%.

\\]



The resulting prevalence lift is:



\\\[

\\boxed{

1.625.

}

\\]



Therefore the flagged subset is approximately:



\\\[

1.625

\\]



times as enriched for severe-underestimation events as the full event population.



\---



\# More Selective Tradeoff Point



At:



\\\[

\\boxed{

\\tau=0.155,

}

\\]



the rule becomes more selective.



The flagged fraction falls to:



\\\[

\\boxed{

43.077\\%.

}

\\]



Severe-underestimation recall becomes:



\\\[

\\boxed{

73.333\\%.

}

\\]



Specificity rises to:



\\\[

\\boxed{

66.000\\%.

}

\\]



Precision rises to:



\\\[

\\boxed{

39.286\\%.

}

\\]



Balanced accuracy is:



\\\[

\\boxed{

69.667\\%.

}

\\]



Thus only:



\\\[

0.333

\\]



percentage points of balanced accuracy are lost relative to the best pooled point.



\---



\# Harmful and Beneficial Events at 0.155



At:



\\\[

\\tau=0.155,

\\]



harmful-expansion recall remains:



\\\[

\\boxed{

86.667\\%.

}

\\]



Beneficial preservation rises to:



\\\[

\\boxed{

70.000\\%.

}

\\]



This makes \\(0.155\\) a more selective retrospective operating point than \\(0.135\\).



\---



\# Risk Lift at 0.155



At:



\\\[

\\tau=0.155,

\\]



severe-event precision is:



\\\[

39.286\\%.

\\]



Risk lift becomes:



\\\[

\\boxed{

1.702.

}

\\]



This is greater than the lift at \\(0.135\\).



Thus the more selective threshold flags fewer events but produces a somewhat more concentrated severe-event subgroup.



\---



\# Retrospective Tradeoff Band



The results suggest that the most informative threshold region is approximately:



\\\[

\\boxed{

0.135

\\text{ to }

0.155.

}

\\]



Within this band:



\- severe recall remains between approximately \\(73\\%\\) and \\(80\\%\\),

\- harmful recall remains \\(86.667\\%\\),

\- specificity improves from \\(60\\%\\) to \\(66\\%\\),

\- beneficial preservation improves from \\(62\\%\\) to \\(70\\%\\),

\- and balanced accuracy remains near \\(70\\%\\).



Thus the signal exhibits a meaningful retrospective tradeoff band.



\---



\# No Sharp Single Boundary



The threshold sweep does not reveal an abrupt phase transition.



Performance evolves gradually as:



\\\[

\\tau

\\]



increases.



For example:



\\\[

\\tau=0.130

\\]



gives:



\\\[

80\\%

\\]



severe recall and:



\\\[

56\\%

\\]



specificity.



At:



\\\[

0.135,

\\]



specificity improves to:



\\\[

60\\%

\\]



without reducing severe recall.



At:



\\\[

0.140,

\\]



severe recall then falls to:



\\\[

73.333\\%.

\\]



At:



\\\[

0.155,

\\]



specificity improves further while recall remains at:



\\\[

73.333\\%.

\\]



This pattern indicates a broad tradeoff region rather than a unique natural cutoff.



\---



\# High-Threshold Region



Above approximately:



\\\[

0.160,

\\]



severe-event recall begins falling rapidly.



At:



\\\[

\\tau=0.160,

\\]



severe recall is:



\\\[

60.000\\%.

\\]



At:



\\\[

0.170,

\\]



it is:



\\\[

40.000\\%.

\\]



At:



\\\[

0.190,

\\]



it falls to:



\\\[

20.000\\%.

\\]



At:



\\\[

0.205,

\\]



it is only:



\\\[

6.667\\%.

\\]



Therefore very high ceiling thresholds sacrifice most of the severe-event signal.



\---



\# Extreme Tail Failure



At:



\\\[

\\tau=0.220,

\\]



only:



\\\[

1/65

\\]



events are flagged.



Severe recall becomes:



\\\[

\\boxed{

0\\%.

}

\\]



Thus the largest predicted ceiling values are not uniquely associated with severe calibration failure.



This directly rejects an extreme-tail-only interpretation.



\---



\# Upper-Tail Concentration Analysis



Experiment 096 also evaluates the upper:



\\\[

50\\%,

40\\%,

30\\%,

20\\%,

10\\%

\\]



of the observed ceiling distribution.



This tests whether severe failures are concentrated in the most extreme predicted-ceiling tail.



\---



\# Upper 50% of Ceiling Values



The upper-half threshold is:



\\\[

0.131250.

\\]



The flagged fraction is approximately:



\\\[

50.769\\%.

\\]



This region contains:



\\\[

\\boxed{

80.000\\%

}

\\]



of severe-underestimation events.



Severe precision is:



\\\[

36.364\\%.

\\]



Risk lift is:



\\\[

1.576.

\\]



Harmful-expansion recall is:



\\\[

86.667\\%.

\\]



Beneficial preservation is:



\\\[

60.000\\%.

\\]



\---



\# Upper 40%



For the upper:



\\\[

40\\%

\\]



of ceiling values:



\\\[

\\tau

=

0.159885.

\\]



Severe recall falls to:



\\\[

\\boxed{

60.000\\%.

}

\\]



Harmful recall is:



\\\[

73.333\\%.

\\]



Beneficial preservation is:



\\\[

70.000\\%.

\\]



\---



\# Upper 30%



For the upper:



\\\[

30\\%,

\\]



severe recall is only:



\\\[

\\boxed{

40.000\\%.

}

\\]



Harmful recall is:



\\\[

53.333\\%.

\\]



\---



\# Upper 20%



For the upper:



\\\[

20\\%,

\\]



severe recall falls to:



\\\[

\\boxed{

20.000\\%.

}

\\]



The risk lift returns to:



\\\[

1.000,

\\]



meaning severe events are no longer enriched relative to their background prevalence.



\---



\# Upper 10%



For the upper:



\\\[

10\\%

\\]



of ceiling values:



\\\[

\\boxed{

6.667\\%

}

\\]



of severe events are captured.



Risk lift is only:



\\\[

0.619.

\\]



Thus the most extreme ceiling tail is actually less enriched for severe underestimation than the full event population.



\---



\# Tail-Concentration Conclusion



The upper-tail analysis rejects the hypothesis that severe calibration failures are concentrated only in the highest predicted-ceiling contexts.



Instead:



\\\[

\\boxed{

\\text{the useful signal occupies a broad moderately elevated}

\\atop

\\text{ceiling regime}.

}

\\]



This distinction is important.



The mechanism is not:



\\\[

\\boxed{

C(x)\\text{ extremely large}

\\Rightarrow

\\text{severe failure}.

}

\\]



It is closer to:



\\\[

\\boxed{

C(x)\\text{ moderately elevated}

\\Rightarrow

\\text{increased calibration-failure risk}.

}

\\]



\---



\# Severe Underestimation and Harmful Expansion Are Not Identical



At several thresholds:



\\\[

\\text{harmful recall}

\\neq

\\text{severe-underestimation recall}.

\\]



For example, at:



\\\[

\\tau=0.125,

\\]



severe recall is:



\\\[

80.000\\%

\\]



while harmful recall is:



\\\[

86.667\\%.

\\]



Therefore the severe-underestimation and harmful-expansion labels are related but not identical event sets.



This distinction should be retained in future controller design.



A calibration-risk signal is not mathematically equivalent to a harmful-expansion detector.



\---



\# Seed-Level Stability at 0.135



Severe-underestimation events occur in:



\\\[

\\boxed{

6

}

\\]



of the analyzed generation seeds.



At:



\\\[

\\tau=0.135,

\\]



mean seed-level severe recall among those seeds is:



\\\[

\\boxed{

86.111\\%.

}

\\]



Minimum severe recall across those seeds is:



\\\[

\\boxed{

50.000\\%.

}

\\]



Mean seed specificity is:



\\\[

62.185\\%.

\\]



Minimum specificity is:



\\\[

33.333\\%.

\\]



Mean seed harmful recall is:



\\\[

\\boxed{

92.857\\%.

}

\\]



Mean beneficial preservation is:



\\\[

66.529\\%.

\\]



\---



\# Seed-Level Stability at 0.155



At:



\\\[

\\tau=0.155,

\\]



mean seed severe recall is:



\\\[

\\boxed{

82.778\\%.

}

\\]



Minimum seed severe recall remains:



\\\[

50.000\\%.

\\]



Mean seed specificity improves to:



\\\[

\\boxed{

65.793\\%.

}

\\]



Minimum specificity remains:



\\\[

33.333\\%.

\\]



Mean harmful recall remains:



\\\[

\\boxed{

92.857\\%.

}

\\]



Mean beneficial preservation improves to:



\\\[

\\boxed{

71.016\\%.

}

\\]



\---



\# Seed-Stability Interpretation



The signal persists across seeds, but the operating statistics are not tightly stable.



The minimum severe recall of:



\\\[

50\\%

\\]



and minimum specificity of:



\\\[

33.333\\%

\\]



show that individual generation seeds can behave substantially differently from the pooled population.



Therefore:



\\\[

\\boxed{

\\text{the threshold band is cross-seed persistent but not}

\\atop

\\text{uniformly stable}.

}

\\]



This argues against treating any retrospective threshold as already validated.



\---



\# Descriptive Operating Points



Experiment 096 identifies two particularly informative retrospective landmarks.



\## Higher-Recall Landmark



\\\[

\\boxed{

\\tau=0.135.

}

\\]



This gives:



\\\[

80\\%

\\]



severe recall,



\\\[

60\\%

\\]



specificity,



and:



\\\[

70\\%

\\]



balanced accuracy.



\## More Selective Landmark



\\\[

\\boxed{

\\tau=0.155.

}

\\]



This gives:



\\\[

73.333\\%

\\]



severe recall,



\\\[

66\\%

\\]



specificity,



and:



\\\[

69.667\\%

\\]



balanced accuracy.



These should be interpreted only as descriptive operating points.



\---



\# Why 0.135 Is Not Yet a Controller Threshold



The value:



\\\[

0.135

\\]



maximizes pooled balanced accuracy on already-observed data.



Therefore selecting it directly as a controller threshold would constitute retrospective optimization.



It cannot be described as prospectively validated.



The correct statement is:



\\\[

\\boxed{

0.135

\\text{ is the best pooled retrospective balanced-accuracy landmark}.

}

\\]



\---



\# Why 0.155 Is Also Not Yet a Controller Threshold



Likewise:



\\\[

0.155

\\]



was identified after observing the retrospective threshold curve.



Its advantage is greater selectivity and beneficial preservation.



However, it too remains data-derived.



Therefore it is a candidate design point, not a validated policy parameter.



\---



\# Principal Finding



Experiment 096 demonstrates that predicted loss ceiling has meaningful threshold geometry.



The useful retrospective region lies approximately between:



\\\[

\\boxed{

0.135

}

\\]



and:



\\\[

\\boxed{

0.155.

}

\\]



Within that band, the signal achieves useful severe-event enrichment while maintaining substantial harmful-event recall and beneficial-event preservation.



However, the relationship is broad rather than sharply thresholded.



\---



\# Principal Negative Finding



Severe underestimation is not concentrated in the extreme high-ceiling tail.



The upper:



\\\[

10\\%

\\]



of ceiling values captures only:



\\\[

\\boxed{

6.667\\%

}

\\]



of severe events.



Therefore:



\\\[

\\boxed{

\\text{extreme predicted ceiling is not the failure regime}.

}

\\]



The relevant regime is moderately elevated predicted consequence severity.



\---



\# Operational Interpretation



The loss ceiling should therefore be viewed as a continuous calibration-risk indicator rather than a naturally binary variable.



The retrospective threshold sweep suggests that a binary guard may still be useful, but any such boundary will represent an engineering tradeoff rather than a discovered physical discontinuity.



This distinction matters for future controller design.



\---



\# What Experiment 096 Establishes



Experiment 096 supports the propositions that:



1\. predicted loss ceiling has coherent retrospective threshold structure;

2\. severe failures become enriched in a moderately elevated ceiling regime;

3\. approximately \\(0.135\\)–\\(0.155\\) forms a useful retrospective tradeoff band;

4\. the signal is not confined to the extreme ceiling tail;

5\. and cross-seed behavior is directionally persistent but not tightly uniform.



\---



\# What Experiment 096 Does Not Establish



Experiment 096 does not establish:



\- a validated ceiling guard,

\- a prospectively optimal threshold,

\- a universal ceiling boundary,

\- that \\(0.135\\) should be deployed,

\- that \\(0.155\\) should be deployed,

\- or that calibration-risk vetoing will improve controller regret.



Those questions require prospective evaluation.



\---



\# Prospective Design Implication



Experiment 096 provides enough structure to justify a preregistered prospective calibration-aware controller experiment.



However, only one primary threshold should be frozen before observing a new seed block.



Testing multiple thresholds and choosing the best after observing the prospective results would weaken the distinction between validation and tuning.



A second threshold could be included only as a clearly labeled sensitivity analysis.



\---



\# Candidate Primary Designs



Two retrospective operating landmarks are available.



\## Candidate A — Higher Recall



\\\[

\\tau\_C=0.135.

\\]



Advantages:



\- higher severe-event recall,

\- best pooled retrospective balanced accuracy.



Cost:



\- more events flagged,

\- lower beneficial preservation.



\## Candidate B — Greater Selectivity



\\\[

\\tau\_C=0.155.

\\]



Advantages:



\- greater specificity,

\- greater beneficial preservation,

\- greater severe-event enrichment.



Cost:



\- somewhat lower severe-event recall.



Neither is yet prospectively validated.



\---



\# Final Scientific Interpretation



Experiments 094–096 now support the following chain:



\\\[

\\boxed{

\\text{harmful responsive expansion}

}

\\]



is associated with:



\\\[

\\boxed{

\\text{absolute consequence underestimation}

}

\\]



which is partially predictable from:



\\\[

\\boxed{

\\text{predicted loss-surface severity}

}

\\]



and most compactly represented by:



\\\[

\\boxed{

C(x)=\\max\_a\\hat L\_a(x).

}

\\]



The ceiling signal does not define a sharp natural threshold.



Instead, it identifies a broader calibration-risk regime.



\---



\# Next Research Direction



The next experiment should be the first prospective test of a frozen calibration-aware guard.



Before touching new seeds, the experiment design should preregister:



1\. one primary loss-ceiling threshold,

2\. the exact veto logic,

3\. the baseline controller,

4\. primary safety metrics,

5\. responsiveness-cost metrics,

6\. and the untouched prospective seed range.



A clean primary design would compare:



\\\[

\\boxed{

\\text{existing support-aware controller}

}

\\]



against:



\\\[

\\boxed{

\\text{support-aware controller}

\+

\\text{frozen loss-ceiling guard}.

}

\\]



The guard should apply only to responsive expansions, not to actions already selected by the primary safe set.



A secondary sensitivity threshold may be included, but the primary threshold must be designated before observing the prospective outcomes.



The next experiment should therefore preregister the prospective calibration-aware guard before any new seed is generated or evaluated.

