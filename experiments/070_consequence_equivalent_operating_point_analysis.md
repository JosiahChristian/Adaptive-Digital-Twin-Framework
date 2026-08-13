\# Experiment 070 — Consequence-Equivalent Operating-Point Analysis



\## Objective



Experiment 069 demonstrated that responsiveness could be increased substantially

without increasing measured regret over a nontrivial range of regularization

strengths.



In particular, the policies associated with



\\\[

\\beta \\in \\{0,\\;0.001,\\;0.0025\\}

\\]



all achieved the same mean regret,



\\\[

R=0.003148,

\\]



and the same number of under-persistence decisions,



\\\[

5,

\\]



despite producing substantially different action distributions.



This suggested that multiple risk operating points may frequently be

consequence-equivalent.



Experiment 070 directly tests that hypothesis.



For each held-out context and each candidate operating point



\\\[

\\lambda \\in \\{0,\\;0.10,\\;0.25,\\;1.00\\},

\\]



the experiment evaluates:



1\. the resulting persistence action,

2\. the realized regret,

3\. exact action equivalence,

4\. exact regret equivalence,

5\. minimum-regret equivalence,

6\. near-regret equivalence under several tolerances,

7\. and the amount of conservatism that can be removed without increasing

&#x20;  consequence.



The central question is



\\\[

\\boxed{

\\text{How much responsiveness is hidden inside consequence-equivalent}

\\atop

\\text{operating-point choices?}

}

\\]



\---



\## Experimental Design



The experiment used generation seed



\\\[

44000\.

\\]



A total of



\\\[

249

\\]



decision contexts were generated.



The same partition structure used in the preceding operating-point experiments

was retained:



| Partition | Contexts |

|---|---:|

| Base-model training | 121 |

| Meta partition | 53 |

| Held-out testing | 75 |



The meta partition was not required for the present diagnostic analysis.



The base-training partition was used to fit the underlying loss and

under-persistence risk models.



All equivalence measurements were then performed on the 75 held-out test

contexts.



\---



\## Candidate Operating Points



The available risk strengths were



\\\[

\\Lambda

=

\\{0,\\;0.10,\\;0.25,\\;1.00\\}.

\\]



Each operating point produces a persistence action



\\\[

a\_t(\\lambda).

\\]



Its realized regret is



\\\[

R\_t(\\lambda)

=

L\_t(a\_t(\\lambda))

\-

L\_t(a\_t^\*).

\\]



Experiment 070 distinguishes two forms of equivalence.



\### Action Equivalence



Two operating points are action-equivalent when



\\\[

\\lambda\_i \\sim\_a \\lambda\_j

\\iff

a\_t(\\lambda\_i)=a\_t(\\lambda\_j).

\\]



\### Regret Equivalence



Two operating points are consequence-equivalent when



\\\[

\\lambda\_i \\sim\_R \\lambda\_j

\\iff

R\_t(\\lambda\_i)=R\_t(\\lambda\_j).

\\]



Regret equivalence is broader than action equivalence.



Different persistence actions can still have identical realized loss and

therefore identical regret.



\---



\## Exact Equivalence Results



Every held-out context contained action-equivalent operating points:



\\\[

\\boxed{

75/75 = 100\\%

}.

\\]



Every held-out context also contained regret-equivalent operating points:



\\\[

\\boxed{

75/75 = 100\\%

}.

\\]



Thus operating-point redundancy is universal in this test population.



However, the stronger result concerns equivalence across all four candidate

risk levels.



All four operating points produced the same persistence action in



\\\[

13/75

\\]



contexts, or



\\\[

17.333\\%.

\\]



In contrast, all four operating points produced the same realized regret in



\\\[

55/75

\\]



contexts, or



\\\[

\\boxed{

73.333\\%

}.

\\]



This large difference confirms that consequence equivalence is substantially

broader than action equivalence.



\---



\## Exact Action-Equivalence Class Sizes



The largest exact action-equivalence class in each context had the following

distribution:



| Largest class size | Contexts | Fraction |

|---:|---:|---:|

| 2 | 22 | 29.333% |

| 3 | 40 | 53.333% |

| 4 | 13 | 17.333% |



No context had a largest class of size one.



Therefore every context contained at least two operating points that produced

the same persistence action.



More than half of all contexts contained at least three action-equivalent risk

levels.



\---



\## Exact Regret-Equivalence Class Sizes



The corresponding regret-equivalence distribution was even more concentrated:



| Largest class size | Contexts | Fraction |

|---:|---:|---:|

| 2 | 5 | 6.667% |

| 3 | 15 | 20.000% |

| 4 | 55 | 73.333% |



Thus nearly three quarters of the held-out contexts satisfy



\\\[

R\_t(0)

=

R\_t(0.10)

=

R\_t(0.25)

=

R\_t(1.00).

\\]



In those contexts, the regret objective alone provides no reason to prefer one

risk operating point over another.



The controller therefore possesses substantial secondary decision freedom.



\---



\## Minimum-Regret Equivalence



The most important equivalence relation for control is not merely whether some

pair of operating points has equal regret.



Instead, define



\\\[

R\_t^{\\min}

=

\\min\_{\\lambda\\in\\Lambda}

R\_t(\\lambda).

\\]



The exact minimum-regret set is



\\\[

\\Lambda\_t^\*

=

\\left\\{

\\lambda:

R\_t(\\lambda)=R\_t^{\\min}

\\right\\}.

\\]



Experiment 070 found that



\\\[

64/75

\\]



contexts contained more than one member of this set.



Therefore,



\\\[

\\boxed{

85.333\\%

}

\\]



of held-out contexts contained multiple exactly minimum-regret operating

points.



This is the central result of Experiment 070.



\---



\## Free Reduction in Conservatism



In every one of the 64 contexts with multiple minimum-regret operating points,

a less-conservative member of the minimum-regret set was available.



Thus



\\\[

\\boxed{

64/75 = 85.333\\%

}

\\]



of all test contexts permit some reduction in operating-point conservatism

without increasing realized regret.



The mean size of the exact minimum-regret equivalence class was



\\\[

\\boxed{

3.373

}

\\]



out of four possible operating points.



Therefore the typical context does not possess a single uniquely optimal

risk posture.



It possesses a broad set of consequence-equivalent choices.



\---



\## Operating-Point Span



Across the exact minimum-regret equivalence sets, the average span between the

least and most conservative available operating points was



\\\[

\\boxed{

0.8227

}.

\\]



Given that the full operating-point range is



\\\[

1.00-0.00=1.00,

\\]



this represents an exceptionally large amount of available operating-point

freedom.



The result explains why Experiment 069 could substantially alter the

controller's action distribution before measured regret changed.



The regularizer was initially moving the policy within broad regions of exact

consequence equivalence rather than forcing a genuine safety tradeoff.



\---



\## Responsive Minimum-Regret Operating Point



Within each exact minimum-regret equivalence class, define the responsive

choice as



\\\[

\\lambda\_t^{\\text{responsive}}

=

\\min

\\Lambda\_t^\*.

\\]



The mean responsive minimum-regret operating point was



\\\[

\\boxed{

0.1673

}.

\\]



This value is especially important because it agrees with the oracle mean

operating point observed in the preceding adaptive operating-point experiments.



The result demonstrates that the oracle's low average risk strength does not

require accepting additional regret.



Instead, the oracle frequently exploits the least-conservative member of a

large minimum-regret equivalence class.



\---



\## Epsilon-Equivalence Analysis



To determine whether the observed phenomenon depended on exact numerical

equality, Experiment 070 also evaluated



\\\[

\\Lambda\_t^\\epsilon

=

\\left\\{

\\lambda:

R\_t(\\lambda)

\\leq

R\_t^{\\min}+\\epsilon

\\right\\}

\\]



for



\\\[

\\epsilon

\\in

\\{

0,\\,

0.0001,\\,

0.0005,\\,

0.001,\\,

0.0025,\\,

0.005

\\}.

\\]



The results were identical at every tested tolerance:



| \\(\\epsilon\\) | Multi-member contexts | Mean class size | Mean span | Responsive mean \\(\\lambda\\) |

|---:|---:|---:|---:|---:|

| 0 | 64 (85.333%) | 3.373 | 0.8227 | 0.1673 |

| 0.0001 | 64 (85.333%) | 3.373 | 0.8227 | 0.1673 |

| 0.0005 | 64 (85.333%) | 3.373 | 0.8227 | 0.1673 |

| 0.0010 | 64 (85.333%) | 3.373 | 0.8227 | 0.1673 |

| 0.0025 | 64 (85.333%) | 3.373 | 0.8227 | 0.1673 |

| 0.0050 | 64 (85.333%) | 3.373 | 0.8227 | 0.1673 |



This is a significant finding.



The observed equivalence structure is not an artifact of selecting a loose

near-optimality tolerance.



The available responsiveness is already present at



\\\[

\\boxed{

\\epsilon=0

}.

\\]



\---



\## Exact Versus Approximate Equivalence



Because the epsilon sweep produces no additional equivalence classes through



\\\[

\\epsilon=0.005,

\\]



the held-out contexts appear to possess a strongly discrete consequence

structure.



Operating-point changes often either:



1\. produce no change in realized consequence, or

2\. cross a meaningful decision boundary and produce a regret increase larger

&#x20;  than the tested tolerance range.



This helps explain the sharp transition observed in Experiment 069.



Small regularization coefficients moved the controller among exactly

equivalent choices.



Once the regularization became sufficiently strong, it began crossing genuine

consequence boundaries.



That transition occurred between



\\\[

\\beta=0.0025

\\]



and



\\\[

\\beta=0.005.

\\]



Experiment 070 therefore provides a structural explanation for the empirical

frontier observed in Experiment 069.



\---



\## Why Global Regularization Is Incomplete



Experiment 069 used the scalarized objective



\\\[

\\hat J\_t(\\lambda)

=

\\hat R\_t(\\lambda)

\+

\\beta C(\\lambda).

\\]



This successfully demonstrated that unnecessary conservatism could be removed.



However, a global coefficient \\(\\beta\\) has an inherent limitation.



The same regularization pressure is applied in contexts where responsiveness

is free and contexts where stronger persistence is genuinely required.



Experiment 070 shows that these cases should be treated differently.



When multiple operating points are consequence-equivalent, responsiveness can

be optimized aggressively.



When the minimum-regret operating point is unique, consequence preservation

should dominate.



This motivates a lexicographic rather than globally scalarized objective.



\---



\## Lexicographic Control Principle



The new control rule can be expressed in two stages.



\### Stage 1 — Consequence Preservation



Estimate the minimum achievable regret:



\\\[

\\hat R\_t^{\\min}

=

\\min\_\\lambda

\\hat R\_t(\\lambda).

\\]



Construct a predicted consequence-equivalent set:



\\\[

\\hat\\Lambda\_t^\\epsilon

=

\\left\\{

\\lambda:

\\hat R\_t(\\lambda)

\\leq

\\hat R\_t^{\\min}+\\epsilon

\\right\\}.

\\]



\### Stage 2 — Responsiveness Selection



Within that set, choose the least conservative operating point:



\\\[

\\lambda\_t

=

\\min

\\hat\\Lambda\_t^\\epsilon.

\\]



The resulting rule is therefore



\\\[

\\boxed{

\\text{preserve predicted consequence first;}

}

\\]



followed by



\\\[

\\boxed{

\\text{maximize responsiveness among consequence-equivalent choices.}

}

\\]



This differs fundamentally from the global regularization used in Experiment

069\.



Responsiveness becomes a secondary objective rather than a competing primary

objective.



\---



\## Structural Interpretation



Experiments 067 through 070 now establish a coherent progression.



\### Experiment 067



Exact operating-point classification preserved responsiveness but produced

excessive regret because label error did not correspond directly to control

consequence.



\### Experiment 068



Direct regret estimation substantially reduced regret but became overly

conservative because pure consequence minimization did not distinguish among

equivalent safe choices.



\### Experiment 069



Responsiveness regularization demonstrated that some of this conservatism

could be removed without additional regret.



\### Experiment 070



Direct equivalence analysis explains why.



The operating-point action space contains extensive redundancy.



In



\\\[

85.333\\%

\\]



of held-out contexts, multiple operating points achieve exactly minimum

regret.



Thus the controller's problem is not always



\\\[

\\text{Which single operating point is optimal?}

\\]



More often, it is



\\\[

\\boxed{

\\text{Which member of the optimal equivalence class should be selected?}

}

\\]



That is a fundamentally different decision problem.



\---



\## Principal Conclusion



Experiment 070 provides strong evidence that consequence-equivalent

operating-point choices are a dominant structural property of the current

persistence-control problem.



Every held-out context contained both action and regret equivalence.



All four operating points were regret-equivalent in



\\\[

73.333\\%

\\]



of contexts.



More importantly,



\\\[

\\boxed{

85.333\\%

}

\\]



of contexts contained multiple exactly minimum-regret operating points.



In every one of those contexts, a less-conservative minimum-regret operating

point was available.



The mean exact minimum-regret class contained



\\\[

3.373

\\]



of the four candidate risk levels, with an average operating-point span of



\\\[

0.8227.

\\]



Furthermore, expanding the equivalence tolerance from



\\\[

0

\\]



to



\\\[

0.005

\\]



did not change the result.



Therefore:



\\\[

\\boxed{

\\text{the responsiveness identified in Experiment 069 is not merely cheap;}

\\atop

\\text{in a large majority of contexts, it is exactly consequence-free.}

}

\\]



This strongly supports replacing global responsiveness regularization with a

lexicographic consequence-first control architecture.



\---



\## Next Research Direction



Experiment 071 should operationalize the structure discovered here.



The learned controller should estimate



\\\[

\\hat R\_t(\\lambda)

\\]



for every candidate operating point.



It should then construct



\\\[

\\hat\\Lambda\_t^\\epsilon

=

\\left\\{

\\lambda:

\\hat R\_t(\\lambda)

\\leq

\\min\_{\\lambda'}

\\hat R\_t(\\lambda')

\+

\\epsilon

\\right\\}.

\\]



The selected operating point should be



\\\[

\\boxed{

\\lambda\_t

=

\\min

\\hat\\Lambda\_t^\\epsilon

}.

\\]



Several predicted-equivalence tolerances should be evaluated because model

estimation error means that exact equality of predicted regrets is unlikely

even when true consequences are identical.



Experiment 071 should compare:



\- pure direct-regret selection,

\- responsiveness-regularized selection,

\- learned lexicographic equivalence selection,

\- oracle equivalence selection,

\- fixed strong-risk control,

\- fixed \\(k=3\\),

\- and the action oracle.



The primary metrics should remain:



\- mean regret,

\- high-regret frequency,

\- under-persistence,

\- over-persistence,

\- action entropy,

\- dominant-action fraction,

\- selected mean risk level,

\- predicted equivalence-class size,

\- and true minimum-regret equivalence recovery.



The central question becomes



\\\[

\\boxed{

\\text{Can a learned controller identify consequence-equivalent choices}

\\atop

\\text{and exploit them to recover responsiveness without sacrificing safety?}

}

\\]

