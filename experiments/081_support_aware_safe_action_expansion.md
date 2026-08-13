\# Experiment 081 — Support-Aware Safe-Action Expansion



\## Objective



Experiment 080 established that the remaining harmful cost-aware expansions are best characterized as training-support extrapolation failures.



The harmful contexts exhibited substantially larger support distances than beneficial expansions:



\\\[

d\_{5}^{\\text{harmful}}

=

5.231

\\]



versus



\\\[

d\_{5}^{\\text{beneficial}}

=

2.557.

\\]



Experiment 081 therefore converts training-support distance from a diagnostic quantity into an explicit execution constraint.



The existing cost-aware admission conditions are preserved:



\\\[

\\hat p\_{\\text{safe}}(a)

\\geq

0.60

\\]



and



\\\[

\\hat d(a)

\\leq

0.020.

\\]



A third condition is added:



\\\[

d\_{5}(x,a)

\\leq

\\tau\_s,

\\]



where \\(d\_5\\) is the mean standardized distance to the five nearest action-specific meta-training examples.



The resulting expansion rule is:



\\\[

\\boxed{

\\hat p\_{\\text{safe}}(a)\\ge0.60

\\;\\land\\;

\\hat d(a)\\le0.020

\\;\\land\\;

d\_5(x,a)\\le\\tau\_s.

}

\\]



The central question is



\\\[

\\boxed{

\\text{Can support-aware filtering preserve responsive-action recovery}

\\atop

\\text{while eliminating extrapolation-driven harmful expansions?}

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

| Support-training | 53 |

| Held-out testing | 75 |



The established primary consequence gate remained fixed at



\\\[

\\epsilon\_{\\text{primary}}

=

0.0005.

\\]



The action-level expansion conditions remained:



\\\[

\\tau\_p

=

0.60

\\]



and



\\\[

\\tau\_d

=

0.020.

\\]



Only the support threshold was swept.



\---



\## Support Threshold Sweep



The tested support-distance limits were:



\\\[

\\tau\_s

\\in

\\{

2.50,\\,

3.00,\\,

3.50,\\,

4.00,\\,

4.50,\\,

5.00,\\,

5.50

\\}.

\\]



Lower values require stronger direct support from nearby meta-training examples.



Higher values allow progressively more extrapolation.



\---



\## Primary Gate Baseline



Before support-aware expansion, the primary gate achieved:



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



Its policy performance was:



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



\## Support-Aware Results



| Support Threshold | Recall | Precision | Responsive Retention | Mean Regret | Under | Over | Entropy | Expanded | Recovered | Beneficial | Harmful |

|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|

| 2.50 | \*\*86.000%\*\* | \*\*97.556%\*\* | \*\*73.333%\*\* | \*\*0.003148\*\* | \*\*5\*\* | \*\*48\*\* | \*\*0.887\*\* | 8 | 8 | 7 | \*\*0\*\* |

| 3.00 | 88.667% | 96.889% | 78.667% | 0.003594 | 6 | 45 | 0.941 | 13 | 12 | 11 | 1 |

| 3.50 | 92.000% | 96.889% | 85.333% | 0.003594 | 6 | 43 | 0.968 | 18 | 17 | 16 | 1 |

| 4.00 | 92.000% | 96.889% | 85.333% | 0.003594 | 6 | 43 | 0.968 | 18 | 17 | 16 | 1 |

| 4.50 | 92.000% | 96.889% | 85.333% | 0.003594 | 6 | 43 | 0.968 | 18 | 17 | 16 | 1 |

| 5.00 | 92.000% | 96.889% | 85.333% | 0.003594 | 6 | 43 | 0.968 | 18 | 17 | 16 | 1 |

| 5.50 | 92.000% | 96.889% | 85.333% | 0.003594 | 6 | 43 | 0.968 | 18 | 17 | 16 | 1 |



The sweep reveals two distinct operating regimes.



\---



\## Consequence-Preserving Operating Point



The most important result occurs at



\\\[

\\boxed{

\\tau\_s=2.50.

}

\\]



At this threshold, the controller achieves:



\\\[

\\text{safe-action recall}

=

86.000\\%,

\\]



\\\[

\\text{safe-action precision}

=

97.556\\%,

\\]



\\\[

\\text{responsive-action retention}

=

73.333\\%,

\\]



while preserving:



\\\[

\\boxed{

R=0.003148

}

\\]



and



\\\[

\\boxed{

N\_{\\text{under}}=5.

}

\\]



These are exactly the same observed mean regret and under-persistence count as the primary gate.



\---



\## Zero Observed Safety-Cost Responsiveness Gain



Relative to the primary gate:



\\\[

\\text{responsive retention}

:

62.667\\%

\\rightarrow

73.333\\%.

\\]



This is an improvement of:



\\\[

\\boxed{

10.666

\\text{ percentage points}.

}

\\]



Safe-action recall improves from:



\\\[

80.000\\%

\\]



to:



\\\[

86.000\\%.

\\]



At the same time, precision improves from:



\\\[

96.889\\%

\\]



to:



\\\[

\\boxed{

97.556\\%.

}

\\]



This is especially important because the controller becomes more responsive without sacrificing observed consequence quality.



\---



\## Harmful Expansion Elimination



At



\\\[

\\tau\_s=2.50,

\\]



the controller performs expansion in



\\\[

8

\\]



contexts.



It recovers responsive actions in all



\\\[

8

\\]



of those contexts.



There are:



\\\[

\\boxed{

0

}

\\]



harmful expansion contexts.



Thus the support-aware filter successfully removes the harmful extrapolation behavior identified in Experiments 078–080.



\---



\## Beneficial Expansion Recovery



Seven of the eight expanded contexts produce beneficial action changes under the experiment's strict beneficial definition.



The eighth recovers the true responsive action without being classified as an action-changing beneficial event under that definition.



The key outcome remains:



\\\[

\\boxed{

8

\\text{ responsive contexts recovered}

}

\\]



with:



\\\[

\\boxed{

0

\\text{ harmful expansions}.

}

\\]



\---



\## Over-Persistence Reduction



The support-aware controller also reduces over-persistence from:



\\\[

55

\\]



to:



\\\[

48\.

\\]



Thus:



\\\[

\\boxed{

7

}

\\]



over-persistent decisions are removed.



This is consistent with the intended objective: restoring responsive actions that were previously hidden by an overly conservative safe-action gate.



\---



\## Action Diversity



Action entropy increases from:



\\\[

0.784

\\]



to:



\\\[

\\boxed{

0.887.

}

\\]



This indicates that the controller is no longer collapsing as strongly toward a dominant conservative persistence choice.



Importantly, this increase occurs without increasing observed mean regret or under-persistence at the \\(\\tau\_s=2.50\\) operating point.



\---



\## Precision Improvement



One of the strongest features of the \\(\\tau\_s=2.50\\) result is that safe-action precision does not merely remain high.



It improves:



\\\[

96.889\\%

\\rightarrow

97.556\\%.

\\]



This means support-aware gating is not behaving like ordinary threshold relaxation.



It is not simply making the gate wider.



Instead, it is selectively expanding in regions with stronger empirical support.



Thus:



\\\[

\\boxed{

\\text{support-aware expansion improves recall and precision simultaneously}

}

\\]



at the selected operating point.



\---



\## Intermediate Threshold \\(\\tau\_s=3.00\\)



At



\\\[

\\tau\_s=3.00,

\\]



recall improves to:



\\\[

88.667\\%.

\\]



Responsive retention reaches:



\\\[

78.667\\%.

\\]



The controller recovers:



\\\[

12

\\]



responsive contexts.



However, one harmful expansion appears.



Mean regret rises to:



\\\[

0.003594.

\\]



Under-persistence increases to:



\\\[

6\.

\\]



Therefore this threshold no longer preserves the primary gate's observed consequence performance.



\---



\## High-Responsiveness Plateau



Beginning at



\\\[

\\boxed{

\\tau\_s=3.50,

}

\\]



the results stabilize.



For every tested threshold from



\\\[

3.50

\\]



through



\\\[

5.50,

\\]



the controller produces:



\\\[

\\text{recall}

=

92.000\\%,

\\]



\\\[

\\text{precision}

=

96.889\\%,

\\]



\\\[

\\text{responsive retention}

=

85.333\\%,

\\]



\\\[

R

=

0.003594,

\\]



\\\[

N\_{\\text{under}}

=

6,

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

0.968.

\\]



The controller expands in:



\\\[

18

\\]



contexts,



recovers:



\\\[

17

\\]



responsive contexts,



and retains:



\\\[

16

\\]



beneficial action-changing expansions.



Only:



\\\[

1

\\]



harmful expansion remains.



\---



\## Stable Plateau Interpretation



The identical results from



\\\[

\\tau\_s=3.50

\\]



through



\\\[

5.50

\\]



show that there are no additional candidate expansions in that support-distance interval.



Thus the support distribution contains a discrete separation.



The principal operating regimes are effectively:



1\. strong-support consequence-preserving expansion around \\(2.50\\),

2\. broader high-responsiveness expansion beginning near \\(3.50\\).



Further threshold widening beyond \\(3.50\\) does not change behavior within the tested range.



\---



\## Two Meaningful Operating Points



Experiment 081 therefore reveals two useful controller configurations.



\### Consequence-Preserving Mode



\\\[

\\boxed{

\\tau\_s=2.50

}

\\]



with:



\\\[

R=0.003148,

\\]



\\\[

N\_{\\text{under}}=5,

\\]



\\\[

\\text{retention}=73.333\\%,

\\]



\\\[

H=0.887,

\\]



and:



\\\[

0

\\]



harmful expansions.



\### Higher-Responsiveness Mode



\\\[

\\boxed{

\\tau\_s=3.50

}

\\]



with:



\\\[

R=0.003594,

\\]



\\\[

N\_{\\text{under}}=6,

\\]



\\\[

\\text{retention}=85.333\\%,

\\]



\\\[

H=0.968,

\\]



and:



\\\[

1

\\]



harmful expansion.



These represent two different operational preferences rather than one universally optimal threshold.



\---



\## Comparison With Experiment 077



The best cost-aware operating point in Experiment 077 was:



\\\[

p=0.60,

\\qquad

d=0.020.

\\]



It achieved:



\\\[

\\text{responsive retention}

=

85.333\\%,

\\]



but with:



\\\[

R=0.004084,

\\]



\\\[

N\_{\\text{under}}=7,

\\]



and:



\\\[

2

\\]



harmful expansion contexts.



Support-aware filtering improves this architecture.



At the broader support regime beginning at



\\\[

\\tau\_s=3.50,

\\]



responsive retention remains:



\\\[

85.333\\%,

\\]



but mean regret improves to:



\\\[

\\boxed{

0.003594

}

\\]



and under-persistence decreases to:



\\\[

\\boxed{

6\.

}

\\]



Harmful expansions decrease from:



\\\[

2

\\]



to:



\\\[

1\.

\\]



Thus support-aware filtering improves consequence performance even when preserving the same responsive-action retention as the best cost-aware controller.



\---



\## Comparison With Probability-Only Expansion



Experiment 076 achieved high responsiveness through probability-only expansion, but false-safe actions caused maximum regret as high as:



\\\[

0.095188.

\\]



Experiment 081 adds two successive protections:



\\\[

\\text{predicted downside}

\\]



and



\\\[

\\text{training support}.

\\]



At the consequence-preserving support threshold, harmful expansions are completely removed.



This demonstrates the value of the layered architecture.



\---



\## Final Three-Layer Admission Rule



The strongest consequence-preserving expansion rule identified so far is:



\\\[

\\boxed{

\\hat p\_{\\text{safe}}(a)

\\geq

0.60

}

\\]



\\\[

\\boxed{

\\hat d(a)

\\leq

0.020

}

\\]



and



\\\[

\\boxed{

d\_{5}(x,a)

\\leq

2.50.

}

\\]



This combines:



1\. predicted safe membership,

2\. predicted consequence downside,

3\. empirical training support.



Each layer addresses a distinct failure mode exposed by the preceding experiments.



\---



\## Architectural Interpretation



The experimental sequence now identifies three different forms of evidence required for responsive expansion.



\### Safety Evidence



\\\[

\\hat p\_{\\text{safe}}(a)

\\]



asks:



> Is this action likely to be consequence-equivalent?



\### Consequence Evidence



\\\[

\\hat d(a)

\\]



asks:



> If the action is not safe, how costly is that mistake predicted to be?



\### Epistemic Support



\\\[

d\_5(x,a)

\\]



asks:



> Is this prediction being made in a region where the model has sufficiently nearby experience?



The controller therefore moves from a simple learned classifier toward a structured evidence system.



\---



\## Why Support Distance Adds Unique Information



Experiment 079 showed that forest uncertainty could not distinguish the harmful cases.



Experiment 080 showed that training-support distance could.



Experiment 081 demonstrates that this distinction is operationally useful.



Support distance rejects extrapolation failures even when the models exhibit:



\\\[

\\text{high safety confidence}

\\]



and



\\\[

\\text{low predicted downside}.

\\]



Therefore:



\\\[

\\boxed{

\\text{training support provides information not contained in}

\\atop

\\text{the learned point estimates or forest variance}.

}

\\]



\---



\## Main Result



Experiment 081 identifies the first operating point in this experimental sequence that improves responsive behavior while matching the primary gate's observed consequence metrics.



At:



\\\[

\\boxed{

\\tau\_s=2.50,

}

\\]



the controller improves:



\\\[

\\text{responsive retention}

:

62.667\\%

\\rightarrow

73.333\\%,

\\]



reduces over-persistence:



\\\[

55

\\rightarrow

48,

\\]



and increases entropy:



\\\[

0.784

\\rightarrow

0.887,

\\]



while preserving:



\\\[

\\boxed{

R=0.003148

}

\\]



and:



\\\[

\\boxed{

N\_{\\text{under}}=5.

}

\\]



No harmful expansion contexts are observed.



This is the strongest consequence-preserving responsiveness result obtained in the current sequence.



\---



\## Principal Conclusion



Experiment 081 validates training-support-aware gating as an effective protection against extrapolation-driven safe-action errors.



The support-aware controller demonstrates that missed responsive actions can be recovered selectively rather than by simply widening the consequence gate.



The most conservative successful operating point:



\\\[

\\boxed{

\\tau\_s=2.50

}

\\]



achieves:



\\\[

\\boxed{

86.000\\%

\\text{ safe-action recall}

}

\\]



\\\[

\\boxed{

97.556\\%

\\text{ safe-action precision}

}

\\]



\\\[

\\boxed{

73.333\\%

\\text{ responsive-action retention}

}

\\]



with:



\\\[

\\boxed{

0

\\text{ harmful expansions}

}

\\]



and no observed increase in mean regret or under-persistence.



Therefore:



\\\[

\\boxed{

\\text{support-aware epistemic gating converts the previous}

\\atop

\\text{responsiveness-safety tradeoff into a locally consequence-preserving gain}.

}

\\]



\---



\## Next Research Direction



The next experiment should test whether this result is robust rather than specific to the single generation seed and held-out partition.



Experiment 082 should perform multi-seed generative validation of the support-aware controller.



The comparison should include at least:



\- primary gate,

\- cost-aware expansion,

\- support-aware \\(\\tau\_s=2.50\\),

\- support-aware \\(\\tau\_s=3.50\\),

\- fixed \\(k=3\\),

\- responsive action oracle,

\- and action oracle.



For each generation seed, the experiment should record:



\- mean regret,

\- under-persistence,

\- over-persistence,

\- safe-action recall,

\- safe-action precision,

\- responsive-action retention,

\- action entropy,

\- harmful expansion count,

\- beneficial expansion count,

\- and support-distance statistics.



The most important question is whether the \\(\\tau\_s=2.50\\) consequence-preserving result persists across genuinely distinct generated datasets.



The central hypothesis becomes:



\\\[

\\boxed{

\\text{support-aware expansion can improve responsiveness robustly}

\\atop

\\text{without materially degrading consequence performance across seeds}.

}

\\]



If that result holds, the support-aware gate moves from a promising single-split finding toward a defensible controller principle.

