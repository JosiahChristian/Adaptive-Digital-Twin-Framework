\# Experiment 071 — Learned Lexicographic Consequence-Equivalent Operating-Point Selection



\## Objective



Experiment 070 established that consequence-equivalent operating-point choices

are widespread in the current persistence-control problem.



In particular,



\\\[

85.333\\%

\\]



of held-out contexts contained multiple exactly minimum-regret risk operating

points.



This suggested a lexicographic controller:



\\\[

\\boxed{

\\text{preserve consequence first}

}

\\]



and then



\\\[

\\boxed{

\\text{maximize responsiveness within the predicted safe equivalence class}.

}

\\]



Experiment 071 operationalizes this idea.



For each candidate operating point



\\\[

\\lambda

\\in

\\{

0,\\,

0.10,\\,

0.25,\\,

1.00

\\},

\\]



the controller estimates



\\\[

\\hat R\_t(\\lambda).

\\]



It then defines a predicted consequence-equivalent set



\\\[

\\hat\\Lambda\_t^\\epsilon

=

\\left\\{

\\lambda:

\\hat R\_t(\\lambda)

\\leq

\\hat R\_t^{\\min}

\+

\\epsilon

\\right\\},

\\]



where



\\\[

\\hat R\_t^{\\min}

=

\\min\_\\lambda

\\hat R\_t(\\lambda).

\\]



The selected operating point is the least conservative member of that set:



\\\[

\\boxed{

\\lambda\_t

=

\\min

\\hat\\Lambda\_t^\\epsilon.

}

\\]



The principal question is



\\\[

\\boxed{

\\text{Can learned equivalence classes recover responsiveness}

\\atop

\\text{without sacrificing consequence quality?}

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



The three-way partition contained:



| Partition | Contexts |

|---|---:|

| Base-model training | 121 |

| Regret-model training | 53 |

| Held-out testing | 75 |



The base-training partition was used to learn the underlying persistence-loss

and under-persistence risk models.



The regret-model partition was used to train direct regret estimators for the

four candidate risk operating points.



The test partition remained fully held out.



\---



\## Predicted Equivalence Tolerances



The tested predicted-regret tolerances were



\\\[

\\epsilon

\\in

\\{

0,\\,

0.0001,\\,

0.0005,\\,

0.0010,\\,

0.0025,\\,

0.0050,\\,

0.0100

\\}.

\\]



When



\\\[

\\epsilon=0,

\\]



the controller reduces to pure predicted-regret minimization.



Increasing \\(\\epsilon\\) enlarges the predicted consequence-equivalent set and

permits selection of a less conservative operating point when the predicted

regret difference is sufficiently small.



\---



\## Policy Performance



| Policy | Mean regret | Zero regret | Regret \\(>0.005\\) | Under | Over | Entropy | Dominant |

|---|---:|---:|---:|---:|---:|---:|---:|

| Direct loss | 0.014317 | 70.667% | 29.333% | 22 | 26 | 0.871 | 53.333% |

| Fixed \\(\\lambda=0.10\\) | 0.013249 | 74.667% | 25.333% | 19 | 34 | 0.972 | 45.333% |

| Fixed \\(\\lambda=0.25\\) | 0.009923 | 81.333% | 18.667% | 14 | 44 | 0.908 | 52.000% |

| Fixed \\(\\lambda=1.00\\) | 0.001460 | 93.333% | 6.667% | 3 | 64 | 0.190 | 94.667% |

| \\(\\epsilon=0\\) | 0.003148 | 90.667% | 9.333% | 5 | 56 | 0.695 | 73.333% |

| \\(\\epsilon=0.0001\\) | 0.003148 | 90.667% | 9.333% | 5 | 56 | 0.731 | 70.667% |

| \\(\\epsilon=0.0005\\) | \*\*0.003148\*\* | \*\*90.667%\*\* | \*\*9.333%\*\* | \*\*5\*\* | \*\*55\*\* | \*\*0.784\*\* | \*\*66.667%\*\* |

| \\(\\epsilon=0.0010\\) | 0.003594 | 89.333% | 10.667% | 6 | 55 | 0.823 | 62.667% |

| \\(\\epsilon=0.0025\\) | 0.004941 | 86.667% | 13.333% | 8 | 44 | 0.958 | 48.000% |

| \\(\\epsilon=0.0050\\) | 0.007008 | 82.667% | 17.333% | 11 | 41 | 0.991 | 40.000% |

| \\(\\epsilon=0.0100\\) | 0.008707 | 78.667% | 21.333% | 14 | 37 | 1.000 | 34.667% |

| Oracle equivalence | 0.001372 | 94.667% | 5.333% | 3 | 35 | 0.998 | 36.000% |

| Fixed \\(k=3\\) | 0.000300 | 96.000% | 4.000% | 0 | 65 | 0.000 | 100.000% |

| Action oracle | 0.000000 | 100.000% | 0.000% | 0 | 0 | 0.883 | 53.333% |



\---



\## Exact Lexicographic Baseline



At



\\\[

\\epsilon=0,

\\]



the controller achieved



\\\[

R=0.003148,

\\]



with



\\\[

5

\\]



under-persistence decisions and action entropy



\\\[

H=0.695.

\\]



This exactly reproduces the pure direct-regret operating-point policy from

Experiment 068.



Thus the lexicographic architecture nests direct regret minimization as its

zero-tolerance limiting case.



\---



\## Safe Equivalence-Recovery Region



Increasing the tolerance to



\\\[

\\epsilon=0.0001

\\]



increased entropy from



\\\[

0.695

\\]



to



\\\[

0.731

\\]



without changing:



\\\[

R=0.003148,

\\]



\\\[

N\_{\\text{under}}=5,

\\]



or the high-regret fraction.



Increasing further to



\\\[

\\boxed{

\\epsilon=0.0005

}

\\]



again preserved



\\\[

R=0.003148

\\]



and



\\\[

N\_{\\text{under}}=5.

\\]



However, entropy increased to



\\\[

\\boxed{

H=0.784

}

\\]



and dominant-action concentration decreased to



\\\[

66.667\\%.

\\]



Over-persistence also decreased:



\\\[

56

\\rightarrow

55\.

\\]



Therefore



\\\[

\\boxed{

\\epsilon=0.0005

}

\\]



is the strongest tested lexicographic tolerance that improves responsiveness

without increasing observed regret or under-persistence.



\---



\## Equivalence-Recovery Metrics



At



\\\[

\\epsilon=0,

\\]



the selected risk operating point belonged to the true minimum-regret

equivalence set in



\\\[

\\boxed{

96.000\\%

}

\\]



of test contexts.



However, it matched the least-conservative member of that true set in only



\\\[

24.000\\%

\\]



of contexts.



Thus the primary consequence-identification problem is already substantially

easier than the secondary responsiveness-selection problem.



\---



\## Effect of Increasing Tolerance



The recovery sweep was:



| \\(\\epsilon\\) | Mean \\(\\lambda\\) | Mean predicted class size | True minimum-set recovery | Responsive-oracle accuracy |

|---:|---:|---:|---:|---:|

| 0.0000 | 0.6573 | 1.573 | 96.000% | 24.000% |

| 0.0001 | 0.6153 | 1.693 | 96.000% | 29.333% |

| 0.0005 | 0.5573 | 1.987 | \*\*96.000%\*\* | \*\*37.333%\*\* |

| 0.0010 | 0.5267 | 2.133 | 94.667% | 42.667% |

| 0.0025 | 0.3747 | 2.573 | 92.000% | 50.667% |

| 0.0050 | 0.3067 | 2.800 | 88.000% | 57.333% |

| 0.0100 | 0.2480 | 3.000 | 84.000% | 57.333% |



As \\(\\epsilon\\) increases:



\\\[

\\text{mean selected }\\lambda

\\downarrow,

\\]



predicted equivalence-class size increases, and responsive-oracle accuracy

improves.



However, true minimum-set recovery eventually begins to decline.



This creates a direct diagnostic tradeoff between



\\\[

\\boxed{

\\text{equivalence-set expansion}

}

\\]



and



\\\[

\\boxed{

\\text{consequence-set contamination}.

}

\\]



\---



\## Safe Boundary



The first measurable degradation occurs at



\\\[

\\epsilon=0.0010.

\\]



At this point:



\\\[

R

=

0.003594,

\\]



under-persistence rises from



\\\[

5

\\]



to



\\\[

6,

\\]



and true minimum-set recovery decreases from



\\\[

96.000\\%

\\]



to



\\\[

94.667\\%.

\\]



Thus the empirical boundary between safe equivalence expansion and unsafe

equivalence expansion lies between



\\\[

\\boxed{

0.0005

}

\\]



and



\\\[

\\boxed{

0.0010.

}

\\]



This mirrors the threshold behavior observed with responsiveness

regularization in Experiment 069.



\---



\## High-Responsiveness Regime



At larger tolerances, the controller becomes progressively more responsive.



For



\\\[

\\epsilon=0.0025,

\\]



entropy reaches



\\\[

0.958,

\\]



but regret increases to



\\\[

0.004941.

\\]



At



\\\[

\\epsilon=0.0050,

\\]



entropy reaches



\\\[

0.991,

\\]



while regret rises to



\\\[

0.007008.

\\]



At



\\\[

\\epsilon=0.0100,

\\]



the controller reaches



\\\[

\\boxed{

H=1.000

}

\\]



with a dominant-action fraction of only



\\\[

34.667\\%.

\\]



However, mean regret rises to



\\\[

0.008707

\\]



and under-persistence increases to



\\\[

14\.

\\]



Thus unrestricted predicted-equivalence expansion eventually reproduces the

same failure mode as excessive responsiveness regularization.



\---



\## Oracle Equivalence Benchmark



The oracle equivalence controller selects the least conservative member of the

true minimum-regret set.



It achieved



\\\[

\\boxed{

R=0.001372

}

\\]



with



\\\[

3

\\]



under-persistence decisions and



\\\[

35

\\]



over-persistence decisions.



Its action entropy was



\\\[

\\boxed{

H=0.998

}

\\]



with dominant-action concentration of only



\\\[

36.000\\%.

\\]



This again demonstrates that high responsiveness and strong safety are

simultaneously achievable when the true consequence-equivalence structure is

known.



\---



\## Primary Versus Secondary Learning Problem



Experiment 071 reveals a useful decomposition.



\### Primary Problem — Safe-Set Identification



The controller must determine which operating points belong to the true

minimum-regret equivalence class.



At small tolerances, this problem is already handled relatively well.



At



\\\[

\\epsilon=0.0005,

\\]



true minimum-set recovery remains



\\\[

\\boxed{

96.000\\%.

}

\\]



\### Secondary Problem — Responsive Selection



Within the true safe set, the controller should choose the least conservative

member.



At



\\\[

\\epsilon=0.0005,

\\]



responsive-oracle accuracy is only



\\\[

37.333\\%.

\\]



Therefore the principal remaining deficiency is no longer broad

consequence-set identification.



It is accurate secondary selection inside that safe set.



\---



\## Interpretation



The controller is already capable of identifying a safe consequence region in

the overwhelming majority of held-out contexts.



However, its learned regret estimates often fail to represent the full breadth

of the true equivalence class.



Consequently, the controller remains more conservative than necessary even

when its selected operating point is consequence-optimal.



This explains why



\\\[

\\text{minimum-set recovery}

\\]



can be very high while responsiveness remains substantially below the oracle.



The next learning problem should therefore avoid perturbing the primary

consequence model unnecessarily.



Instead, it should learn a secondary responsiveness criterion conditioned on

the predicted safe set.



\---



\## Comparison With Experiment 069



Experiment 069 used global responsiveness regularization.



Its strongest zero-regret-cost result was



\\\[

\\beta=0.0025,

\\]



with



\\\[

R=0.003148,

\\qquad

H=0.846.

\\]



Experiment 071's strongest zero-regret-cost lexicographic result was



\\\[

\\epsilon=0.0005,

\\]



with



\\\[

R=0.003148,

\\qquad

H=0.784.

\\]



Thus global regularization achieved somewhat higher entropy on this single

population.



However, the lexicographic formulation has a methodological advantage:



\\\[

\\boxed{

\\text{responsiveness is only optimized after consequence preservation}.

}

\\]



It also provides direct diagnostics of true minimum-set recovery and

responsive-oracle accuracy.



Therefore the lexicographic architecture is more interpretable as a

consequence-first control hierarchy.



\---



\## Structural Interpretation



Experiments 070 and 071 together establish that the persistence operating-point

problem is naturally hierarchical.



The controller should not treat safety and responsiveness as globally

interchangeable scalar objectives.



Instead:



\\\[

\\boxed{

\\text{Stage 1: identify the consequence-safe set}

}

\\]



followed by



\\\[

\\boxed{

\\text{Stage 2: optimize responsiveness within that set}.

}

\\]



Experiment 071 shows that Stage 1 already performs well:



\\\[

96\\%

\\]



minimum-set recovery.



Stage 2 remains substantially imperfect.



This strongly motivates learning a dedicated secondary decision signal rather

than widening the primary equivalence threshold further.



\---



\## Principal Conclusion



Experiment 071 successfully operationalizes consequence-equivalent

lexicographic operating-point control.



A predicted-regret tolerance of



\\\[

\\boxed{

\\epsilon=0.0005

}

\\]



improved action entropy from



\\\[

0.695

\\]



to



\\\[

0.784

\\]



without increasing mean regret:



\\\[

R=0.003148.

\\]



Under-persistence remained fixed at



\\\[

5,

\\]



and true minimum-set recovery remained



\\\[

\\boxed{

96.000\\%.

}

\\]



However, responsive-oracle accuracy reached only



\\\[

37.333\\%.

\\]



This establishes that:



\\\[

\\boxed{

\\text{safe-set identification is largely successful}

}

\\]



while



\\\[

\\boxed{

\\text{responsive tie-breaking within the safe set remains the main bottleneck}.

}

\\]



The oracle equivalence policy confirms the opportunity, achieving both



\\\[

R=0.001372

\\]



and



\\\[

H=0.998.

\\]



\---



\## Next Research Direction



Experiment 072 should focus specifically on the secondary selection problem.



Rather than modifying the primary regret-equivalence rule, it should preserve a

conservative predicted safe set and learn a dedicated tie-breaking criterion

inside that set.



Candidate secondary signals include:



\- predicted over-persistence cost,

\- predicted unnecessary-retention probability,

\- distance from the direct-loss action,

\- predicted safe-release opportunity,

\- persistence-action diversity,

\- and probability that the least-conservative candidate remains inside the true

&#x20; minimum-regret set.



A possible hierarchical controller is



\\\[

\\hat\\Lambda\_t^{\\text{safe}}

=

\\left\\{

\\lambda:

\\hat R\_t(\\lambda)

\\leq

\\hat R\_t^{\\min}

\+

\\epsilon\_{\\text{safe}}

\\right\\},

\\]



followed by



\\\[

\\lambda\_t

=

\\arg\\min\_{\\lambda\\in\\hat\\Lambda\_t^{\\text{safe}}}

\\hat C\_{\\text{secondary}}(\\lambda).

\\]



The central question becomes



\\\[

\\boxed{

\\text{Can the controller learn which member of a predicted safe set}

\\atop

\\text{is unnecessarily conservative?}

}

\\]

