\# Experiment 074 — Action-Effective Responsiveness Analysis



\## Objective



Experiments 071–073 exposed a distinction between operating-point selection and actual persistence behavior.



Experiment 073 showed that a learned responsive-optimality model could change the selected risk level



\\\[

\\lambda

\\]



without changing the resulting policy-level regret, under-persistence, over-persistence, or action entropy.



This suggested that multiple operating points may frequently induce the same persistence action.



Experiment 074 therefore moves the analysis from operating-point space into action space.



The central question is:



\\\[

\\boxed{

\\text{How much of the remaining responsive-oracle gap is real}

\\atop

\\text{at the persistence-action level rather than only in }\\lambda\\text{-space?}

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



The same three-way partition used in the preceding experiments was retained:



| Partition | Contexts |

|---|---:|

| Base-model training | 121 |

| Regret-model training | 53 |

| Held-out testing | 75 |



The primary consequence-safe tolerance remained



\\\[

\\boxed{

\\epsilon\_{\\text{primary}}=0.0005.

}

\\]



This preserves direct comparability with Experiments 071–073.



\---



\## Operating Points and Persistence Actions



The candidate risk operating points were



\\\[

\\Lambda=

\\{0.00,\\ 0.10,\\ 0.25,\\ 1.00\\}.

\\]



Each operating point produces a persistence action



\\\[

a\_t(\\lambda)\\in\\{1,2,3\\}.

\\]



Different values of \\(\\lambda\\) need not produce different actions.



Therefore,



\\\[

\\lambda\_i\\neq\\lambda\_j

\\]



does not imply



\\\[

a\_t(\\lambda\_i)\\neq a\_t(\\lambda\_j).

\\]



This distinction is essential because the executed persistence action—not the numerical risk parameter itself—is what changes controller behavior.



\---



\## True Minimum-Regret Set



For context \\(t\\), define the true minimum-regret operating-point set



\\\[

\\Lambda\_t^\*

=

\\left\\{

\\lambda:

R\_t(\\lambda)

=

R\_t^{\\min}

\\right\\}.

\\]



The corresponding true safe-action set is



\\\[

A\_t^\*

=

\\left\\{

a\_t(\\lambda):

\\lambda\\in\\Lambda\_t^\*

\\right\\}.

\\]



The most responsive true safe action is



\\\[

a\_t^{\\text{responsive}}

=

\\min A\_t^\*.

\\]



A context contains genuine action-level responsiveness headroom whenever



\\\[

|A\_t^\*|>1.

\\]



In such a context, more than one persistence action achieves the same minimum regret.



\---



\## Predicted Safe Set



The learned regret models define



\\\[

\\hat\\Lambda\_t^{\\text{safe}}

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



The predicted safe-action set is



\\\[

\\hat A\_t^{\\text{safe}}

=

\\left\\{

a\_t(\\lambda):

\\lambda\\in

\\hat\\Lambda\_t^{\\text{safe}}

\\right\\}.

\\]



Experiment 074 compares the structure of



\\\[

\\hat A\_t^{\\text{safe}}

\\]



with the true set



\\\[

A\_t^\*.

\\]



\---



\## Safe Action-Set Structure



Among the 75 held-out contexts, predicted safe sets contained multiple distinct persistence actions in only



\\\[

20/75

=

26.667\\%.

\\]



By contrast, true minimum-regret sets contained multiple distinct actions in



\\\[

45/75

=

60.000\\%.

\\]



Thus:



\\\[

\\boxed{

26.667\\%

\\ll

60.000\\%.

}

\\]



The learned safe-set mechanism is therefore substantially narrower in action space than the true minimum-regret structure.



\---



\## True Safe Action-Set Sizes



The true minimum-regret action sets had the following distribution:



| Number of distinct safe actions | Contexts | Fraction |

|---:|---:|---:|

| 1 | 30 | 40.000% |

| 2 | 42 | 56.000% |

| 3 | 3 | 4.000% |



Therefore,



\\\[

45/75

\\]



contexts contained at least two equally minimum-regret persistence actions.



Only



\\\[

40.000\\%

\\]



of contexts truly required a unique persistence action.



This means action-level equivalence is not an exceptional condition. It is the majority case.



\---



\## Predicted Safe Action-Set Sizes



The predicted safe-action sets had the following distribution:



| Number of distinct predicted-safe actions | Contexts | Fraction |

|---:|---:|---:|

| 1 | 55 | 73.333% |

| 2 | 18 | 24.000% |

| 3 | 2 | 2.667% |



The learned system therefore predicts a singleton safe-action set in



\\\[

73.333\\%

\\]



of held-out contexts.



The true system has a singleton minimum-regret action set in only



\\\[

40.000\\%.

\\]



This is a major structural discrepancy.



\---



\## Safe-Set Contraction



The contrast can be written directly as



\\\[

P(|A\_t^\*|>1)

=

60.000\\%

\\]



while



\\\[

P(|\\hat A\_t^{\\text{safe}}|>1)

=

26.667\\%.

\\]



The difference is



\\\[

60.000\\%-26.667\\%

=

33.333

\\]



percentage points.



Therefore the learned primary gate substantially contracts the available action-equivalence structure.



This yields the central diagnostic result of Experiment 074:



\\\[

\\boxed{

\\text{The controller is not primarily failing to rank safe actions.}

\\atop

\\text{It frequently fails to expose those actions as safe candidates.}

}

\\]



\---



\## Responsiveness Headroom



A lower true safe persistence action existed in



\\\[

45/75

=

60.000\\%

\\]



of held-out contexts.



Furthermore, all 45 of these contexts admitted an exact regret-free action reduction:



\\\[

\\boxed{

45/75

=

60.000\\%.

}

\\]



Thus every context with true action-level responsiveness headroom allowed the controller to become more responsive without increasing regret.



This is a strong result.



The observed conservatism is therefore not entirely forced by the consequence objective.



In a majority of held-out contexts, a less persistent action exists with exactly equivalent minimum regret.



\---



\## Responsive Recovery: Lambda Space vs Action Space



The lexicographic baseline recovered the responsive oracle operating point with accuracy



\\\[

37.333\\%.

\\]



However, it recovered the responsive oracle persistence action with accuracy



\\\[

\\boxed{

61.333\\%.

}

\\]



Thus:



\\\[

\\text{responsive action accuracy}

\-

\\text{responsive }\\lambda\\text{ accuracy}

=

24.000

\\]



percentage points.



This confirms the hypothesis from Experiment 073.



A substantial portion of the apparent operating-point error is behaviorally irrelevant.



Different \\(\\lambda\\) values frequently collapse to the same persistence action.



Therefore:



\\\[

\\boxed{

\\lambda\\text{-level disagreement}

\\not\\Rightarrow

\\text{action-level disagreement}.

}

\\]



\---



\## The Lambda-Label Illusion



Before Experiment 074, responsive-oracle accuracy of



\\\[

37.333\\%

\\]



suggested that the learned controller was failing to recover responsive behavior in almost two-thirds of contexts.



The action-space analysis changes that interpretation.



Actual responsive-action accuracy is



\\\[

61.333\\%.

\\]



Consequently, some of the previously measured error is an artifact of representing the decision problem in operating-point space.



The controller may select the "wrong" \\(\\lambda\\) while still executing the correct responsive action.



This motivates evaluating adaptive risk mechanisms at two levels:



1\. operating-point accuracy,

2\. behavioral action accuracy.



The second is ultimately more relevant to control performance.



\---



\## Genuine Remaining Action Gap



Although action-space recovery is much stronger than lambda-space recovery, it is not complete.



Responsive action accuracy remains only



\\\[

61.333\\%.

\\]



Therefore



\\\[

38.667\\%

\\]



of held-out contexts do not recover the true responsive minimum-regret action.



The mean positive action gap was



\\\[

0.5467.

\\]



The mean positive lambda gap was



\\\[

0.4020.

\\]



The remaining problem is therefore not purely representational.



There is genuine persistence-action responsiveness still left to recover.



\---



\## Why Experiments 072 and 073 Could Not Solve the Problem



Experiment 072 attempted to improve secondary safe-membership discrimination.



Experiment 073 attempted to directly learn the least-conservative minimum-regret operating point.



Neither changed the final persistence policy.



Experiment 074 explains why.



A secondary selector can only choose among candidates admitted by the primary gate.



But the predicted safe set exposes multiple distinct actions in only



\\\[

26.667\\%

\\]



of contexts.



Therefore, in approximately three quarters of held-out contexts, the secondary selector sees only one predicted-safe action.



No tie-breaking mechanism can recover an omitted action.



Formally, if



\\\[

a\_t^{\\text{responsive}}

\\notin

\\hat A\_t^{\\text{safe}},

\\]



then any secondary policy constrained to



\\\[

\\hat A\_t^{\\text{safe}}

\\]



must fail to select



\\\[

a\_t^{\\text{responsive}}.

\\]



Thus the bottleneck occurs upstream of secondary selection.



\---



\## Primary-Gate Recall as the New Bottleneck



Earlier experiments established high minimum-set recovery in operating-point space.



However, Experiment 074 demonstrates that recovering at least one minimum-regret candidate is not the same objective as recovering the full useful equivalence structure.



A gate can successfully include a minimum-regret operating point while simultaneously excluding another minimum-regret operating point that would produce a more responsive action.



Therefore the previous metric



\\\[

\\text{minimum-set recovery}

\\]



is necessary but insufficient.



The more appropriate quantity is now safe-action-set recall.



Conceptually,



\\\[

\\text{SafeActionRecall}\_t

=

\\frac{

|A\_t^\*\\cap\\hat A\_t^{\\text{safe}}|

}{

|A\_t^\*|

}.

\\]



Even more specifically, the controller should measure whether the responsive member is retained:



\\\[

\\mathbf{1}

\\left\[

a\_t^{\\text{responsive}}

\\in

\\hat A\_t^{\\text{safe}}

\\right].

\\]



This quantity determines whether downstream responsive selection is even possible.



\---



\## Consequence-Safe Expansion



The results motivate a new design problem.



The objective should not simply be to choose



\\\[

\\arg\\min\_\\lambda \\hat R\_t(\\lambda).

\\]



Nor should it merely recover one member of the minimum-regret set.



Instead, the controller should attempt to recover the useful consequence-equivalent region:



\\\[

\\hat A\_t^{\\text{safe}}

\\approx

A\_t^\*.

\\]



The difficult part is that expansion must remain asymmetric.



False exclusion of a genuinely safe responsive action creates unnecessary conservatism.



False inclusion of a genuinely unsafe action can increase consequence regret.



Therefore future expansion should explicitly distinguish:



\\\[

\\text{safe-set false negatives}

\\]



from



\\\[

\\text{safe-set false positives}.

\\]



The former reduce responsiveness.



The latter threaten consequence preservation.



\---



\## Revised Learning Hierarchy



The experiments now suggest the following control hierarchy.



\### Stage 1 — Consequence Estimation



Estimate the regret or consequence associated with each candidate action.



\### Stage 2 — Safe-Action Set Recovery



Recover the set of actions that are consequence-equivalent or sufficiently close to the predicted optimum.



\### Stage 3 — Responsive Selection



Only after adequate safe-action coverage is established should the controller choose the most responsive candidate within that set.



This can be represented as



\\\[

x\_t

\\rightarrow

\\hat R\_t(a)

\\rightarrow

\\hat A\_t^{\\text{safe}}

\\rightarrow

a\_t^{\\text{responsive}}.

\\]



The critical insight is that Stage 2 must preserve enough action diversity for Stage 3 to matter.



\---



\## Relationship to Experiments 070–073



The recent experimental sequence now forms a coherent progression.



\### Experiment 070 — Consequence Equivalence



Established that multiple operating points frequently have identical consequences.



\### Experiment 071 — Learned Lexicographic Selection



Demonstrated strong recovery of minimum-regret operating-point membership while retaining a substantial responsive gap.



\### Experiment 072 — Secondary Safe-Membership Tie-Breaking



Showed that another safe-membership classifier does not improve behavior.



\### Experiment 073 — Responsive-Optimality Learning



Directly targeted the least-conservative safe operating point but again produced no policy-level improvement.



\### Experiment 074 — Action-Effective Responsiveness



Explained the previous failures by revealing two distinct phenomena:



\\\[

\\boxed{

\\text{operating-point redundancy}

}

\\]



and



\\\[

\\boxed{

\\text{predicted safe-action-set contraction}.

}

\\]



The first means lambda accuracy understates actual behavioral accuracy.



The second prevents secondary learners from accessing many genuinely responsive safe actions.



\---



\## Principal Conclusion



Experiment 074 establishes that the remaining responsiveness problem must be formulated in persistence-action space.



Responsive operating-point accuracy was only



\\\[

37.333\\%,

\\]



but responsive action accuracy was



\\\[

61.333\\%.

\\]



Therefore a substantial fraction of operating-point error is action-equivalent and behaviorally irrelevant.



However, the true minimum-regret structure contains multiple distinct safe actions in



\\\[

60.000\\%

\\]



of contexts, whereas the learned gate exposes multiple predicted-safe actions in only



\\\[

26.667\\%.

\\]



All



\\\[

45

\\]



contexts containing true responsiveness headroom permitted an exact regret-free action reduction.



Thus the primary learned gate is hiding a large fraction of the available responsiveness.



The central conclusion is:



\\\[

\\boxed{

\\text{The dominant remaining bottleneck is safe-action-set recall,}

\\atop

\\text{not secondary tie-breaking.}

}

\\]



\---



\## Next Research Direction



Experiment 075 should directly measure and characterize safe-action-set recall.



For every held-out context, it should quantify:



\- true safe actions,

\- predicted safe actions,

\- intersection size,

\- action-level recall,

\- action-level precision,

\- responsive-action retention,

\- false-safe action inclusion,

\- missed-safe action exclusion,

\- and the regret associated with false inclusions.



The central metric should be



\\\[

\\boxed{

P

\\left(

a\_t^{\\text{responsive}}

\\in

\\hat A\_t^{\\text{safe}}

\\right).

}

\\]



This will separate two fundamentally different failures:



\\\[

\\text{responsive action absent from predicted safe set}

\\]



from



\\\[

\\text{responsive action present but not selected}.

\\]



That distinction determines the architecture of the next controller.



If the responsive action is usually absent, the next step should improve safe-set recall.



If it is usually present but not selected, the next step should return to secondary selection.



Experiment 075 should therefore diagnose the safe-action gate before any additional learning mechanism is introduced.

