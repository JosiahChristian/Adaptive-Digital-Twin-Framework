\# Experiment 077 — Cost-Aware Safe-Action Expansion



\## Objective



Experiment 076 demonstrated that action-level safe-set expansion can recover many responsive actions excluded by the conservative primary gate.



However, probability-only expansion admitted rare but expensive false-safe actions.



At active thresholds, maximum false-safe regret reached



\\\[

0.095188.

\\]



Experiment 077 therefore augments safe-action probability with a separate estimate of downside.



For each excluded action \\(a\\), the controller estimates:



\\\[

\\hat p\_t^{\\text{safe}}(a)

=

P

\\left(

a\\in A\_t^\*

\\mid

x\_t

\\right)

\\]



and



\\\[

\\hat d\_t(a)

=

\\widehat{

\\text{regret incurred if }a\\text{ is not actually safe}

}.

\\]



An action is admitted only when it satisfies both



\\\[

\\hat p\_t^{\\text{safe}}(a)

\\geq

\\tau\_p

\\]



and



\\\[

\\hat d\_t(a)

\\leq

\\tau\_d.

\\]



The central question is



\\\[

\\boxed{

\\text{Can explicit downside filtering recover responsive actions}

\\atop

\\text{while rejecting high-cost false-safe expansions?}

}

\\]



\---



\## Experimental Design



The experiment used generation seed



\\\[

44000

\\]



and generated



\\\[

249

\\]



decision contexts.



The partition remained:



| Partition | Contexts |

|---|---:|

| Base-model training | 121 |

| Cost-model training | 53 |

| Held-out testing | 75 |



The primary consequence-safe tolerance remained



\\\[

\\boxed{

\\epsilon\_{\\text{primary}}

=

0.0005.

}

\\]



Thus all improvements are measured relative to the same high-precision primary gate used in Experiments 071–076.



\---



\## Primary Gate Baseline



The primary gate achieved:



\\\[

\\text{safe-action recall}

=

80.000\\%,

\\]



\\\[

\\text{safe-action precision}

=

96.889\\%,

\\]



and



\\\[

\\text{responsive-action retention}

=

62.667\\%.

\\]



Its policy performance was



\\\[

R

=

0.003148,

\\]



\\\[

N\_{\\text{under}}

=

5,

\\]



\\\[

N\_{\\text{over}}

=

55,

\\]



and



\\\[

H

=

0.784.

\\]



This remains the consequence-preserving reference point.



\---



\## Expansion Models



Experiment 077 uses two learned action-level quantities.



\### Safe-Membership Probability



For each action



\\\[

a\\in\\{1,2,3\\},

\\]



the classifier estimates



\\\[

\\hat p\_t^{\\text{safe}}(a).

\\]



This is the same structural signal introduced in Experiment 076.



\### Downside Estimate



A separate regression model estimates



\\\[

\\hat d\_t(a),

\\]



where the target is



\\\[

d\_t(a)

=

\\begin{cases}

0,

\&

a\\in A\_t^\*,

\\\\\[4pt]

R\_t(a),

\&

a\\notin A\_t^\*.

\\end{cases}

\\]



Thus safe actions receive zero downside, while unsafe actions are labeled by the magnitude of their realized regret.



The expansion rule becomes



\\\[

a

\\in

\\hat A\_t^{\\text{expanded}}

\\]



only when



\\\[

\\hat p\_t^{\\text{safe}}(a)

\\geq

\\tau\_p

\\]



and



\\\[

\\hat d\_t(a)

\\leq

\\tau\_d.

\\]



\---



\## Threshold Grid



The tested safety-confidence thresholds were



\\\[

\\tau\_p

\\in

\\{

0.60,\\,

0.70,\\,

0.80

\\}.

\\]



The tested downside limits were



\\\[

\\tau\_d

\\in

\\{

0.005,\\,

0.010,\\,

0.020,\\,

0.040,\\,

0.080

\\}.

\\]



This produced



\\\[

3\\times5=15

\\]



cost-aware operating points.



\---



\## Cost-Aware Expansion Results



| \\(p\\) | \\(d\\) | Recall | Precision | Retention | Regret | Under | Over | Entropy |

|---:|---:|---:|---:|---:|---:|---:|---:|---:|

| 0.60 | 0.005 | 87.333% | 96.222% | 76.000% | 0.004084 | 7 | 50 | 0.888 |

| 0.60 | 0.010 | 90.667% | 96.222% | 82.667% | 0.004084 | 7 | 45 | 0.954 |

| 0.60 | 0.020 | \*\*92.000%\*\* | \*\*96.222%\*\* | \*\*85.333%\*\* | \*\*0.004084\*\* | \*\*7\*\* | \*\*43\*\* | \*\*0.971\*\* |

| 0.60 | 0.040 | 93.778% | 93.556% | 89.333% | 0.007241 | 11 | 37 | 1.000 |

| 0.60 | 0.080 | 95.111% | 92.889% | 92.000% | 0.008010 | 12 | 35 | 0.998 |

| 0.70 | 0.005 | 84.667% | 95.556% | 72.000% | 0.004084 | 7 | 52 | 0.877 |

| 0.70 | 0.010 | 87.333% | 95.556% | 77.333% | 0.004084 | 7 | 48 | 0.934 |

| 0.70 | 0.020 | 88.000% | 95.556% | 78.667% | 0.004084 | 7 | 47 | 0.946 |

| 0.70 | 0.040 | 89.111% | 94.889% | 81.333% | 0.004892 | 8 | 44 | 0.968 |

| 0.70 | 0.080 | 89.778% | 94.889% | 82.667% | 0.004892 | 8 | 43 | 0.975 |

| 0.80 | 0.005 | 82.667% | 95.556% | 68.000% | 0.004084 | 7 | 54 | 0.854 |

| 0.80 | 0.010 | 85.333% | 95.556% | 73.333% | 0.004084 | 7 | 50 | 0.915 |

| 0.80 | 0.020 | 86.000% | 95.556% | 74.667% | 0.004084 | 7 | 49 | 0.927 |

| 0.80 | 0.040 | 86.000% | 95.556% | 74.667% | 0.004084 | 7 | 49 | 0.927 |

| 0.80 | 0.080 | 86.000% | 95.556% | 74.667% | 0.004084 | 7 | 49 | 0.927 |



\---



\## Best Cost-Aware Region



The most informative operating region occurs when



\\\[

\\tau\_d

\\leq

0.020.

\\]



Across several safety thresholds in this region, mean regret remains fixed at



\\\[

\\boxed{

0.004084

}

\\]



with



\\\[

N\_{\\text{under}}

=

7\.

\\]



However, responsiveness varies substantially.



The strongest tested point within this regret plateau is



\\\[

\\boxed{

\\tau\_p=0.60,

\\qquad

\\tau\_d=0.020.

}

\\]



It achieved:



\\\[

\\text{recall}

=

92.000\\%,

\\]



\\\[

\\text{precision}

=

96.222\\%,

\\]



\\\[

\\text{responsive retention}

=

85.333\\%,

\\]



\\\[

R

=

0.004084,

\\]



\\\[

N\_{\\text{under}}

=

7,

\\]



\\\[

N\_{\\text{over}}

=

43,

\\]



and



\\\[

H

=

0.971.

\\]



\---



\## Improvement in Responsive Retention



Relative to the primary gate,



\\\[

62.667\\%

\\]



responsive retention increased to



\\\[

85.333\\%.

\\]



This is an absolute improvement of



\\\[

\\boxed{

22.666

\\text{ percentage points}.

}

\\]



The cost-aware controller recovered



\\\[

17

\\]



previously excluded responsive contexts at this operating point.



The number of expansion contexts was



\\\[

19\.

\\]



Only



\\\[

2

\\]



of those expansions were harmful.



Thus expansion efficiency was high.



\---



\## Expansion Efficiency



At



\\\[

p=0.60,

\\qquad

d=0.020,

\\]



the model expanded the gate in



\\\[

19

\\]



contexts.



It recovered responsive actions in



\\\[

17

\\]



of them.



Therefore approximately



\\\[

\\frac{17}{19}

\\approx

89.5\\%

\\]



of expansions recovered a previously unavailable responsive action.



Only



\\\[

2

\\]



contexts introduced newly false-safe actions.



This is substantially more selective than permissive probability-only expansion.



\---



\## Downside Reduction Relative to Experiment 076



Experiment 076 allowed maximum false-safe regret up to



\\\[

0.095188

\\]



across active probability-only expansion thresholds.



Under the tighter cost-aware regime of Experiment 077, maximum false-safe regret was reduced to



\\\[

\\boxed{

0.036763

}

\\]



for the operating points with



\\\[

d\\leq0.020

\\]



and



\\\[

p=0.60.

\\]



The corresponding mean false-safe regret was



\\\[

\\boxed{

0.035122.

}

\\]



Thus the downside model successfully filters out the most severe false-positive expansions.



This confirms the central hypothesis of Experiment 077:



\\\[

\\boxed{

\\text{explicit downside estimation adds useful information}

\\atop

\\text{beyond safe-membership probability alone}.

}

\\]



\---



\## Cost of Remaining False Positives



Despite the reduction in false-positive severity, aggregate policy regret still increases.



The primary baseline achieved



\\\[

R=0.003148,

\\]



while the strongest cost-aware responsive operating point achieved



\\\[

R=0.004084.

\\]



Under-persistence increased from



\\\[

5

\\]



to



\\\[

7\.

\\]



Therefore the remaining harmful expansions are still consequential enough to degrade the overall safety objective.



This means downside filtering improves the expansion mechanism but does not yet fully solve the problem.



\---



\## Regret Plateau



An important structural feature appears in the results.



Several combinations produce exactly



\\\[

R=0.004084

\\]



and



\\\[

N\_{\\text{under}}=7.

\\]



Within this plateau, responsiveness varies considerably.



For example:



\\\[

p=0.80,\\ d=0.005

\\]



produces responsive retention



\\\[

68.000\\%,

\\]



while



\\\[

p=0.60,\\ d=0.020

\\]



produces



\\\[

85.333\\%

\\]



with the same aggregate regret and under-persistence count.



Therefore, within the measured regime,



\\\[

\\boxed{

p=0.60,\\ d=0.020

}

\\]



strictly dominates the more conservative members of the same regret plateau on responsiveness.



\---



\## Breakdown at Larger Downside Thresholds



When the downside gate is relaxed to



\\\[

d=0.040

\\]



or



\\\[

d=0.080,

\\]



the safety degradation becomes much stronger.



For example,



\\\[

p=0.60,\\ d=0.040

\\]



achieves



\\\[

H=1.000

\\]



and



\\\[

89.333\\%

\\]



responsive retention.



However, regret rises to



\\\[

0.007241

\\]



with



\\\[

11

\\]



under-persistence decisions.



At



\\\[

p=0.60,\\ d=0.080,

\\]



regret rises further to



\\\[

0.008010

\\]



with



\\\[

12

\\]



under-persistence decisions.



Therefore downside limits above approximately



\\\[

0.020

\\]



allow increasingly dangerous expansions.



\---



\## Safety Probability and Downside Are Complementary



Experiment 077 demonstrates that the two learned quantities capture different aspects of the expansion problem.



Safety probability estimates



\\\[

\\text{how likely the action is to be safe}.

\\]



Downside estimation approximates



\\\[

\\text{how costly the action is if that belief is wrong}.

\\]



An action with high estimated safety probability may still have unacceptable tail consequence.



Conversely, an action with moderate confidence may be reasonable to admit when its predicted downside is very small.



Therefore:



\\\[

\\boxed{

\\text{confidence}

\\neq

\\text{consequence}.

}

\\]



The controller benefits from modeling both.



\---



\## Comparison With Experiment 076



The most promising probability-only point in Experiment 076 was



\\\[

\\tau=0.80.

\\]



It achieved:



\\\[

\\text{retention}

=

74.667\\%,

\\]



\\\[

R

=

0.004084,

\\]



and



\\\[

N\_{\\text{under}}

=

7\.

\\]



Experiment 077 reaches the same policy regret and under-persistence level at



\\\[

p=0.60,\\ d=0.020,

\\]



but improves responsive retention to



\\\[

\\boxed{

85.333\\%.

}

\\]



Entropy also increases:



\\\[

0.927

\\rightarrow

0.971.

\\]



Over-persistence decreases:



\\\[

49

\\rightarrow

43\.

\\]



Thus explicit downside modeling produces a substantially better responsiveness profile at the same observed aggregate regret.



\---



\## Remaining Failure Mode



The cost-aware gate still selects the minimum action in the expanded set:



\\\[

a\_t

=

\\min

\\hat A\_t^{\\text{expanded}}.

\\]



This rule is maximally responsive once an action is admitted.



However, admission uncertainty remains imperfect.



The two harmful expansion contexts at the best operating point suggest that the remaining regret increase may arise from either:



1\. underestimated downside,

2\. overestimated safe-membership probability,

3\. insufficient feature discrimination,

4\. or overly aggressive action selection after expansion.



The present experiment does not distinguish those causes.



\---



\## Selection After Expansion



The current architecture assumes:



\\\[

\\text{admitted}

\\Rightarrow

\\text{safe enough to choose}.

\\]



This may be too aggressive.



An expanded set can contain a lower-persistence candidate that barely passes the gate.



Choosing the minimum action immediately converts a small estimation error into a control decision.



A more conservative downstream rule could evaluate incremental regret before moving from the primary action to the expanded action.



For example, define



\\\[

\\Delta \\hat R\_t(a)

=

\\hat R\_t(a)

\-

\\hat R\_t(a\_{\\text{primary}}).

\\]



The controller could require



\\\[

\\Delta \\hat R\_t(a)

\\leq

\\tau\_\\Delta

\\]



before executing the lower action.



This introduces a second consequence check after expansion.



\---



\## Structural Interpretation



Experiments 075–077 now establish a clear progression.



\### Experiment 075



Safe-action recall is the dominant remaining bottleneck.



\### Experiment 076



Action-level probability models can recover the missed responsive actions, but probability-only expansion admits rare high-cost errors.



\### Experiment 077



Explicit downside estimation successfully suppresses the most severe false-positive expansions and improves responsiveness at a given regret level.



However, a small number of harmful expansions still remain.



Thus the next issue is no longer broad safe-set recovery.



It is the detailed structure of the surviving harmful expansion decisions.



\---



\## Principal Conclusion



Experiment 077 confirms that cost-aware expansion is superior to probability-only expansion.



At



\\\[

\\boxed{

p=0.60,

\\qquad

d=0.020,

}

\\]



the controller achieves:



\\\[

\\boxed{

92.000\\%

\\text{ safe-action recall}

}

\\]



\\\[

\\boxed{

96.222\\%

\\text{ safe-action precision}

}

\\]



\\\[

\\boxed{

85.333\\%

\\text{ responsive-action retention}

}

\\]



with



\\\[

R=0.004084,

\\]



\\\[

N\_{\\text{under}}=7,

\\]



and



\\\[

H=0.971.

\\]



Seventeen responsive contexts are recovered, while only two harmful expansion contexts remain.



Maximum false-safe regret is reduced from the



\\\[

0.095188

\\]



seen under probability-only expansion to



\\\[

\\boxed{

0.036763.

}

\\]



Therefore:



\\\[

\\boxed{

\\text{downside-aware filtering materially improves safe-action expansion}.

}

\\]



However, the controller still does not recover additional responsiveness at zero observed safety cost.



The remaining harmful expansion contexts must be analyzed directly.



\---



\## Next Research Direction



Experiment 078 should perform a realized-selection-risk decomposition of the surviving harmful expansions.



The analysis should focus on the best cost-aware operating point:



\\\[

\\boxed{

p=0.60,

\\qquad

d=0.020.

}

\\]



For every expansion context, it should record:



\- primary action,

\- expanded action,

\- true safe-action set,

\- safety probability,

\- predicted downside,

\- realized regret,

\- incremental regret relative to the primary action,

\- whether downside was underestimated,

\- whether safety confidence was overestimated,

\- and whether the expanded action was more responsive but unsafe.



The experiment should separate:



\\\[

\\boxed{

\\text{beneficial expansion}

}

\\]



from



\\\[

\\boxed{

\\text{neutral expansion}

}

\\]



and



\\\[

\\boxed{

\\text{harmful expansion}.

}

\\]



It should also determine whether the two remaining harmful contexts are separable by:



\- safety score,

\- downside score,

\- predicted regret margin,

\- action step size,

\- or other existing features.



The central question becomes



\\\[

\\boxed{

\\text{What distinguishes the few harmful expansions that survive}

\\atop

\\text{both safety-confidence and downside filtering?}

}

\\]

