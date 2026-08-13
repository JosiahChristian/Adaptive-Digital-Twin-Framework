\# Experiment 072 — Learned Secondary Responsive Tie-Breaking



\## Objective



Experiment 071 established a hierarchical operating-point architecture in which

the controller first identifies a predicted consequence-safe set and then

selects a less-conservative member of that set.



At the strongest consequence-preserving operating point,



\\\[

\\epsilon=0.0005,

\\]



the learned lexicographic controller achieved



\\\[

96.000\\%

\\]



true minimum-regret-set recovery.



However, responsive-oracle accuracy remained only



\\\[

37.333\\%.

\\]



This indicated that the principal remaining deficiency was not broad safe-set

identification.



It was secondary selection within that safe set.



Experiment 072 therefore introduces a learned secondary model intended to

estimate whether each candidate operating point belongs to the true

minimum-regret equivalence class.



The architecture is constrained hierarchically:



\\\[

\\boxed{

\\text{primary regret gate}

\\rightarrow

\\text{secondary safety confidence}

\\rightarrow

\\text{responsive tie-break}

}

\\]



The secondary model is not permitted to select an operating point outside the

primary predicted-safe set.



The central question is



\\\[

\\boxed{

\\text{Can a learned secondary safety signal distinguish unnecessarily}

\\atop

\\text{conservative members of an already-safe candidate set?}

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

| Secondary-model training | 53 |

| Held-out testing | 75 |



The base-training partition was used to fit the underlying persistence-loss

and under-persistence risk models.



The secondary-training partition was used to fit:



1\. the direct regret models defining the primary predicted-safe set, and

2\. a secondary candidate-level model estimating true minimum-set membership.



The final 75 contexts remained held out for evaluation.



\---



\## Primary Consequence-Safe Set



Experiment 071 identified



\\\[

\\epsilon=0.0005

\\]



as the strongest tested predicted-regret tolerance that improved responsiveness

without increasing measured regret or under-persistence.



Experiment 072 therefore fixes the primary tolerance at



\\\[

\\boxed{

\\epsilon\_{\\text{primary}}=0.0005.

}

\\]



For each context,



\\\[

\\hat\\Lambda\_t^{\\text{primary}}

=

\\left\\{

\\lambda:

\\hat R\_t(\\lambda)

\\leq

\\hat R\_t^{\\min}

\+

0.0005

\\right\\}.

\\]



The mean primary safe-set size on the held-out population was



\\\[

\\boxed{

1.987

}.

\\]



\---



\## Secondary Learning Target



For each candidate operating point, the secondary model was trained to estimate

whether that candidate belongs to the true minimum-regret set:



\\\[

y\_t(\\lambda)

=

\\mathbf{1}

\\left\[

\\lambda\\in\\Lambda\_t^\*

\\right].

\\]



Thus the secondary prediction approximates



\\\[

\\hat p\_t(\\lambda)

\\approx

P

\\left(

\\lambda\\in\\Lambda\_t^\*

\\mid

x\_t

\\right).

\\]



The controller then applies a confidence threshold



\\\[

\\tau

\\]



within the primary safe set.



Candidates satisfying



\\\[

\\hat p\_t(\\lambda)\\geq\\tau

\\]



are admitted to the secondary feasible set.



If multiple candidates remain, the least-conservative candidate is selected.



If none satisfy the threshold, the controller falls back to the minimum

predicted-regret member of the primary safe set.



\---



\## Tested Secondary Thresholds



The tested confidence thresholds were



\\\[

\\tau

\\in

\\{

0.50,\\,

0.60,\\,

0.70,\\,

0.80,\\,

0.90

\\}.

\\]



The objective was to determine whether stricter secondary confidence would

remove falsely safe low-\\(\\lambda\\) candidates while preserving genuinely

responsive minimum-regret choices.



\---



\## Baseline Performance



The fixed primary lexicographic baseline reproduced Experiment 071 at



\\\[

\\epsilon=0.0005.

\\]



Its performance was:



\\\[

R=0.003148,

\\]



\\\[

N\_{\\text{under}}=5,

\\]



\\\[

N\_{\\text{over}}=55,

\\]



\\\[

H=0.784,

\\]



and dominant-action concentration



\\\[

66.667\\%.

\\]



Its mean selected operating point was



\\\[

\\bar\\lambda=0.5573.

\\]



True minimum-set recovery was



\\\[

\\boxed{

96.000\\%

}

\\]



while responsive-oracle accuracy was



\\\[

\\boxed{

37.333\\%.

}

\\]



\---



\## Policy Performance



Every tested secondary threshold produced the same policy-level outcome as the

primary lexicographic baseline.



| Policy | Mean regret | Zero regret | Regret \\(>0.005\\) | Under | Over | Entropy | Dominant |

|---|---:|---:|---:|---:|---:|---:|---:|

| Lexicographic baseline | 0.003148 | 90.667% | 9.333% | 5 | 55 | 0.784 | 66.667% |

| Secondary \\(\\tau=0.50\\) | 0.003148 | 90.667% | 9.333% | 5 | 55 | 0.784 | 66.667% |

| Secondary \\(\\tau=0.60\\) | 0.003148 | 90.667% | 9.333% | 5 | 55 | 0.784 | 66.667% |

| Secondary \\(\\tau=0.70\\) | 0.003148 | 90.667% | 9.333% | 5 | 55 | 0.784 | 66.667% |

| Secondary \\(\\tau=0.80\\) | 0.003148 | 90.667% | 9.333% | 5 | 55 | 0.784 | 66.667% |

| Secondary \\(\\tau=0.90\\) | 0.003148 | 90.667% | 9.333% | 5 | 55 | 0.784 | 66.667% |



No tested threshold changed:



\- mean regret,

\- zero-regret fraction,

\- high-regret frequency,

\- under-persistence,

\- over-persistence,

\- action entropy,

\- or dominant-action concentration.



\---



\## Recovery Metrics



The baseline achieved:



\\\[

\\bar\\lambda=0.5573,

\\]



\\\[

\\text{minimum-set recovery}=96.000\\%,

\\]



\\\[

\\text{responsive-oracle accuracy}=37.333\\%.

\\]



Every secondary threshold produced exactly the same values:



\\\[

\\boxed{

\\bar\\lambda=0.5573

}

\\]



\\\[

\\boxed{

\\text{minimum-set recovery}=96.000\\%

}

\\]



and



\\\[

\\boxed{

\\text{responsive-oracle accuracy}=37.333\\%.

}

\\]



Thus the learned secondary safety signal did not alter the final selected

operating points.



\---



\## Secondary Feasible-Set Size



For thresholds



\\\[

\\tau

\\in

\\{

0.50,\\,

0.60,\\,

0.70,\\,

0.80

\\},

\\]



the mean secondary feasible-set size was



\\\[

\\boxed{

1.987,

}

\\]



exactly equal to the mean primary safe-set size.



Therefore the secondary model admitted essentially every candidate already

admitted by the primary regret gate.



At



\\\[

\\tau=0.90,

\\]



the mean secondary feasible-set size decreased slightly to



\\\[

1.907.

\\]



However, this reduction still did not change the selected policy.



The removed candidates were therefore not the candidates controlling the final

least-conservative choice.



\---



\## Secondary Model Redundancy



The result indicates that the secondary model learned a signal highly aligned

with primary predicted-safe-set membership.



Empirically,



\\\[

\\boxed{

\\text{secondary safety score}

\\approx

\\text{primary safe-set membership}.

}

\\]



This is understandable because both learning stages target closely related

quantities.



The primary regret models estimate whether a candidate has near-minimum

consequence.



The secondary model estimates whether a candidate belongs to the true

minimum-regret set.



Because the primary architecture already achieved



\\\[

96\\%

\\]



minimum-set recovery, the secondary target provides little additional

discriminative information.



\---



\## Why Threshold Tuning Does Not Solve the Problem



The invariance across



\\\[

\\tau=0.50

\\]



through



\\\[

\\tau=0.90

\\]



shows that the limitation is not simply an improperly chosen secondary

confidence threshold.



If threshold calibration were the main problem, policy behavior would be

expected to change as the feasible set narrowed.



Instead, nearly all thresholds reproduce the primary candidate set, and even

the strictest tested threshold leaves the selected decisions unchanged.



Therefore:



\\\[

\\boxed{

\\text{the secondary target itself is redundant}.

}

\\]



Further threshold tuning on this target is unlikely to solve the

responsiveness-selection problem.



\---



\## Comparison With Oracle Equivalence



The oracle equivalence controller achieved:



\\\[

R=0.001372,

\\]



\\\[

N\_{\\text{under}}=3,

\\]



\\\[

N\_{\\text{over}}=35,

\\]



and



\\\[

H=0.998.

\\]



Its dominant-action concentration was only



\\\[

36.000\\%.

\\]



Thus a large gap remains between learned and oracle responsive selection.



However, Experiment 072 demonstrates that the gap is not primarily caused by a

failure to identify candidates belonging to the true safe set.



The secondary model largely agrees with the primary safe-set mechanism.



The missing information concerns the ordering of candidates \*within\* the safe

set.



\---



\## Revised Secondary Learning Problem



The previous secondary target was



\\\[

P

\\left(

\\lambda\\in\\Lambda\_t^\*

\\right).

\\]



But the unresolved decision is actually:



\\\[

\\boxed{

\\text{Which member of }\\Lambda\_t^\*

\\text{ is the least conservative one?}

}

\\]



The next secondary target should therefore distinguish the responsive member

of the safe set directly.



Define



\\\[

\\lambda\_t^{\\text{responsive}}

=

\\min

\\Lambda\_t^\*.

\\]



Then a candidate-level target can be written as



\\\[

y\_t^{\\text{responsive}}(\\lambda)

=

\\mathbf{1}

\\left\[

\\lambda

=

\\lambda\_t^{\\text{responsive}}

\\right].

\\]



Equivalently, the model should estimate



\\\[

P

\\left(

\\lambda

=

\\min\\Lambda\_t^\*

\\mid

x\_t

\\right).

\\]



This is fundamentally different from estimating general safe-set membership.



\---



\## Structural Interpretation



Experiments 071 and 072 now separate two learning problems even more sharply.



\### Safe Membership



The current architecture identifies candidates belonging to the consequence-safe

region with high accuracy.



This problem is already largely solved.



\### Responsive Ordering



The controller still does not reliably distinguish which safe candidate is the

least conservative.



This problem remains poorly learned.



Experiment 072 demonstrates that simply adding another safe-membership model

does not address that gap.



The secondary model must target the missing ordering information explicitly.



\---



\## Principal Conclusion



Experiment 072 successfully tests a learned secondary safety gate but finds no

improvement over the primary lexicographic controller.



Across all tested thresholds,



\\\[

\\tau

\\in

\\{

0.50,\\,

0.60,\\,

0.70,\\,

0.80,\\,

0.90

\\},

\\]



policy performance remained exactly:



\\\[

R=0.003148,

\\]



\\\[

N\_{\\text{under}}=5,

\\]



\\\[

N\_{\\text{over}}=55,

\\]



and



\\\[

H=0.784.

\\]



True minimum-set recovery remained



\\\[

96.000\\%

\\]



and responsive-oracle accuracy remained



\\\[

37.333\\%.

\\]



The secondary feasible set was almost identical to the primary safe set.



Therefore:



\\\[

\\boxed{

\\text{learning safe-set membership twice does not improve responsive}

\\atop

\\text{tie-breaking}.

}

\\]



The unresolved problem is not whether a candidate is safe.



It is identifying the least-conservative safe candidate.



\---



\## Next Research Direction



Experiment 073 should replace the secondary safe-membership target with a

direct responsive-optimality target.



For each context, define



\\\[

\\lambda\_t^{\\text{responsive}}

=

\\min

\\Lambda\_t^\*.

\\]



The secondary learner should estimate either:



\\\[

P

\\left(

\\lambda

=

\\lambda\_t^{\\text{responsive}}

\\mid

x\_t

\\right),

\\]



or a candidate-specific responsiveness utility conditioned on consequence

safety.



The primary regret gate should remain unchanged.



Only candidates inside



\\\[

\\hat\\Lambda\_t^{\\text{primary}}

\\]



should remain eligible for secondary selection.



A candidate secondary decision rule is



\\\[

\\lambda\_t

=

\\arg\\max\_{

\\lambda

\\in

\\hat\\Lambda\_t^{\\text{primary}}

}

\\hat P

\\left(

\\lambda

=

\\lambda\_t^{\\text{responsive}}

\\right).

\\]



The experiment should compare:



\- primary lexicographic selection,

\- responsive-optimality scoring,

\- least-\\(\\lambda\\) deterministic tie-breaking,

\- oracle equivalence selection,

\- fixed strong-risk control,

\- fixed \\(k=3\\),

\- and the action oracle.



The principal evaluation metrics should include:



\- mean regret,

\- under-persistence,

\- over-persistence,

\- action entropy,

\- minimum-set recovery,

\- responsive-oracle accuracy,

\- responsive rank accuracy,

\- and mean selected \\(\\lambda\\).



The central question becomes



\\\[

\\boxed{

\\text{Can the controller learn the ordering of safe operating points}

\\atop

\\text{rather than merely their membership?}

}

\\]

