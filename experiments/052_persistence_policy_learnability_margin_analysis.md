\# Experiment 052 — Persistence-Policy Learnability Margin Analysis



\## Objective



Determine whether the performance limitations of the adaptive

release-persistence policy observed in Experiment 051 arise primarily from

insufficient model capability or from weak intrinsic separation between the

available persistence actions.



Experiment 051 demonstrated that release-confirmation depth can be treated as a

state-dependent decision variable



\[

k\_t

===



\\pi\_{\\text{release persistence}}

(z\_{1:t},M\_t),

]



with the learned policy selecting among



\[

k\\in{1,2,3}.

]



However, the adaptive policy did not consistently outperform the best fixed

persistence strategy.



Experiment 052 therefore measures the \*\*learnability margin\*\* between competing

persistence actions.



For each decision context, the best-vs-second utility margin is defined as



\[

\\Delta

======



U^{(1)}-U^{(2)},

]



where (U^{(1)}) is the utility of the best persistence decision and

(U^{(2)}) is the utility of the second-best decision.



Equivalently, under a loss formulation,



\[

\\Delta

======



L^{(2)}-L^{(1)}.

]



A small margin indicates that two or more persistence actions produce nearly

equivalent outcomes and therefore may be intrinsically difficult to

distinguish from available trajectory evidence.



A large margin indicates a decision for which the preferred persistence action

is more clearly separated and should therefore be easier to learn reliably.



\## Decision Contexts



The analysis contained



\[

N=249

]



persistence-decision contexts.



The optimal persistence-action distribution was:



| Best persistence | Count | Fraction |

| ---------------: | ----: | -------: |

|            (k=1) |   172 |  69.076% |

|            (k=2) |    62 |  24.900% |

|            (k=3) |    15 |   6.024% |



Immediate confirmation was therefore optimal most frequently.



However, approximately



\[

30.924%

]



of contexts favored a persistence depth greater than one, confirming the

state-dependent structure identified in Experiment 051.



\## Utility Margin Summary



Across all decision contexts:



| Margin statistic             |        Value |

| ---------------------------- | -----------: |

| Mean best-vs-second margin   |     0.007883 |

| Median best-vs-second margin | \*\*0.000000\*\* |

| Mean best-vs-worst spread    |     0.024366 |

| Median best-vs-worst spread  | \*\*0.000000\*\* |

| Mean relative margin         |      15.934% |

| Median relative margin       |   \*\*0.000%\*\* |



The most important result is



\[

\\boxed{

\\operatorname{median}(\\Delta)=0.

}

]



Thus at least half of the evaluated decision contexts contain no measurable

utility separation between the best persistence action and its nearest

competitor.



The median best-vs-worst spread is also zero, indicating that exact or

effectively exact utility equivalence can extend across the full persistence

action set.



This demonstrates that a substantial fraction of release-persistence decisions

are not merely difficult classification problems.



They are intrinsically low-margin decisions.



\## Meaningful-Margin Prevalence



The fraction of decision contexts exceeding selected best-vs-second margin

thresholds was:



| Margin threshold | Fraction exceeding threshold |

| ---------------: | ---------------------------: |

|        (>0.0000) |                      18.474% |

|        (>0.0005) |                      18.072% |

|        (>0.0010) |                      18.072% |

|        (>0.0025) |                      18.072% |

|        (>0.0050) |                      17.269% |

|        (>0.0100) |                      14.859% |



Only



\[

18.474%

]



of decision contexts had any strictly positive best-vs-second margin.



Therefore approximately



\[

\\boxed{

81.526%

}

]



of contexts produced zero best-vs-second separation.



Even after requiring only a very small margin,



\[

\\Delta>0.001,

]



the prevalence remained just



\[

18.072%.

]



This result indicates that the majority of persistence labels are generated in

regions where competing actions are utility-equivalent or nearly

utility-equivalent.



\## Margin by Optimal Persistence Depth



Margin structure differed substantially according to the optimal persistence

action.



| Best persistence | (n) | Mean margin | Median margin | Mean best-vs-worst spread |

| ---------------: | --: | ----------: | ------------: | ------------------------: |

|            (k=1) | 172 |    0.008435 |      0.000000 |                  0.009993 |

|            (k=2) |  62 |    0.000111 |      0.000000 |                  0.057615 |

|            (k=3) |  15 |    0.033681 |      0.036763 |                  0.051751 |



\### Immediate persistence: (k=1)



Although (k=1) was the most frequently optimal action, its median margin was



\[

0\.

]



Thus many states labeled (k=1) are not strongly separated from alternative

persistence depths.



The mean margin of



\[

0.008435

]



is driven by a smaller subset of more clearly separated contexts.



\### Intermediate persistence: (k=2)



The (k=2) class exhibits the weakest best-vs-second separation:



\[

\\boxed{

\\text{mean margin}\_{k=2}=0.000111

}

]



with a median of zero.



This means that states for which (k=2) is technically optimal are almost

always extremely close to at least one competing action.



Interestingly, the mean best-vs-worst spread is comparatively large:



\[

0.057615.

]



Therefore (k=2) may frequently be distinguishable from the worst persistence

decision while remaining nearly indistinguishable from the best competing

action.



This is an important distinction between \*\*action rejection\*\* and \*\*exact

action identification\*\*.



\### Strong persistence: (k=3)



The (k=3) class is rare but strongly separated.



Its mean margin is



\[

0.033681,

]



and its median margin is



\[

\\boxed{

0.036763.

}

]



Unlike (k=1) and (k=2), the median (k=3) decision therefore has a

substantial positive utility advantage over its nearest competitor.



This suggests that strong-persistence states, although uncommon, may be the

most statistically identifiable persistence decisions in the system.



\## Pairwise Preference Structure



Pairwise comparisons produced:



| Comparison     | First action better | Second action better |         Tie |

| -------------- | ------------------: | -------------------: | ----------: |

| (k=1) vs (k=2) |             15.261% |              27.711% |     57.028% |

| (k=1) vs (k=3) |             12.048% |              30.924% |     57.028% |

| (k=2) vs (k=3) |              3.614% |               8.032% | \*\*88.353%\*\* |



The persistence actions therefore exhibit extensive pairwise equivalence.



More than half of all contexts were ties between (k=1) and either (k=2)

or (k=3).



The strongest equivalence occurred between moderate and strong persistence:



\[

\\boxed{

P(k=2\\sim k=3)=88.353%.

}

]



Thus (k=2) and (k=3) differ in utility in only a small fraction of the

evaluated states.



This helps explain why exact three-class persistence prediction is difficult:

the system frequently provides almost no outcome-based reason to prefer one of

these two actions.



\## Interpretation



Experiment 052 demonstrates that persistence-policy learning is fundamentally a

\*\*low-margin decision problem\*\*.



The learned controller in Experiment 051 was asked to infer a discrete action

label even though most decision contexts provide little or no utility

separation between competing actions.



Therefore classification error does not necessarily imply meaningful control

error.



A prediction such as



\[

k=2

]



when the nominal optimum is



\[

k=3

]



may be labeled incorrect even when the two actions produce identical or nearly

identical downstream utility.



This distinction implies that conventional exact-label classification accuracy

is not an adequate measure of persistence-policy quality.



The relevant quantity is closer to \*\*regret\*\*:



\[

R\_t

===



U\_t(k\_t^\\star)-U\_t(\\hat{k}\_t),

]



where (k\_t^\\star) is the nominal optimal persistence action and

(\\hat{k}\_t) is the learned action.



When the utility margin is near zero,



\[

R\_t\\approx 0

]



even if



\[

\\hat{k}\_t\\neq k\_t^\\star.

]



Thus the adaptive controller may be substantially more successful than exact

action agreement alone would suggest.



\## Structural Finding



The results reveal three distinct persistence-decision regimes:



\[

\\boxed{

\\text{indifferent}

;\\rightarrow;

\\text{weakly separated}

;\\rightarrow;

\\text{strongly separated}.

}

]



In indifferent regions, multiple persistence actions are effectively

equivalent.



In weakly separated regions, exact action prediction is statistically fragile

and may offer little practical benefit.



In strongly separated regions, action selection matters materially and should

receive greater learning emphasis.



This suggests that release-persistence control should not be formulated as an

ordinary equally weighted multiclass classification problem.



Instead, training should account explicitly for action-value separation.



\## Principal Conclusion



The performance gap observed in Experiment 051 is explained in substantial

part by weak intrinsic learnability margins.



The majority of persistence-decision contexts do not contain a uniquely

dominant action with meaningful utility separation.



Only approximately



\[

18%

]



of contexts exhibit a positive best-vs-second margin, while the median margin

across the complete dataset is zero.



The (k=2) class is particularly ambiguous, whereas the rare (k=3) decisions

possess substantially stronger utility margins.



Therefore the remaining adaptive-policy error cannot be interpreted simply as

model inadequacy.



A large fraction of the target structure itself is effectively

non-identifiable under exact-label learning.



The appropriate objective is consequently not



\[

\\boxed{

\\text{predict the nominal persistence label exactly}

}

]



but rather



\[

\\boxed{

\\text{avoid materially suboptimal persistence decisions}.

}

]



\## Next Research Direction



Experiment 053 should replace uniform exact-label persistence learning with a

\*\*margin-aware or regret-aware persistence policy\*\*.



Training importance should increase with the utility consequence of choosing

the wrong action.



For example, each decision context may receive a weight



\[

w\_t=f(\\Delta\_t),

]



where larger utility margins produce greater training weight.



Alternatively, the learner may directly estimate action utilities



\[

\\hat{U}\_t(k),

\\qquad

k\\in{1,2,3},

]



and select



\[

\\hat{k}\_t

=========



\\arg\\max\_k \\hat{U}\_t(k),

]



rather than learning nominal persistence labels directly.



Evaluation should compare exact action accuracy with utility regret,



\[

R\_t

===



U\_t(k\_t^\\star)-U\_t(\\hat{k}\_t),

]



to determine whether a policy can achieve near-optimal persistence control even

when exact action identification remains intrinsically ambiguous.



This would transform persistence-policy learning from a classification problem

into a utility-sensitive decision problem.



