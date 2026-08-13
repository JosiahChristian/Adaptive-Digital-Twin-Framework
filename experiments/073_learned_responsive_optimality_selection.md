\# Experiment 073 — Learned Responsive-Optimality Selection



\## Objective



Experiments 071 and 072 established that the primary consequence-safe set can be identified with high accuracy, but that a secondary safe-membership model does not improve responsive tie-breaking.



Experiment 073 therefore changes the secondary learning target.



Instead of estimating



\\\[

P

\\left(

\\lambda\\in\\Lambda\_t^\*

\\right),

\\]



the model directly estimates whether a candidate is the least-conservative member of the true minimum-regret equivalence set:



\\\[

y\_t^{\\text{responsive}}(\\lambda)

=

\\mathbf{1}

\\left\[

\\lambda

=

\\min \\Lambda\_t^\*

\\right].

\\]



The primary consequence-safe gate remains unchanged:



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



The responsive model is therefore only allowed to rank candidates already admitted by the consequence-first primary gate.



The central question is



\\\[

\\boxed{

\\text{Can direct responsive-optimality learning improve ordering}

\\atop

\\text{within an already safe operating-point set?}

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

| Responsive-model training | 53 |

| Held-out testing | 75 |



The base-training partition was used to train the underlying persistence-loss and under-persistence risk models.



The responsive-training partition was used to train:



\- direct regret estimators for the primary safe set,

\- and candidate-specific responsive-optimality classifiers.



The final 75 contexts remained held out.



\---



\## Primary Consequence Gate



The primary predicted-safe set uses the Experiment 071 tolerance



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

\\min\_{\\lambda'}

\\hat R\_t(\\lambda')

\+

0.0005

\\right\\}.

\\]



This gate remains responsible for consequence preservation.



The secondary model cannot introduce a candidate from outside this set.



\---



\## Responsive Learning Target



For each context, define the true minimum-regret set



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



The true responsive operating point is



\\\[

\\lambda\_t^{\\text{responsive}}

=

\\min \\Lambda\_t^\*.

\\]



Each candidate-specific classifier is trained against



\\\[

y\_t(\\lambda)

=

\\mathbf{1}

\\left\[

\\lambda

=

\\lambda\_t^{\\text{responsive}}

\\right].

\\]



Thus the secondary model estimates



\\\[

\\hat P\_t^{\\text{responsive}}(\\lambda)

\\approx

P

\\left(

\\lambda

=

\\lambda\_t^{\\text{responsive}}

\\mid

x\_t

\\right).

\\]



Within the primary predicted-safe set, the selected operating point is



\\\[

\\lambda\_t

=

\\arg\\max\_{

\\lambda\\in

\\hat\\Lambda\_t^{\\text{primary}}

}

\\hat P\_t^{\\text{responsive}}(\\lambda).

\\]



Ties favor the less-conservative candidate.



\---



\## Policy Performance



The held-out policy results were:



| Policy | Mean regret | Zero regret | Regret \\(>0.005\\) | Under | Over | Entropy | Dominant |

|---|---:|---:|---:|---:|---:|---:|---:|

| Direct loss | 0.014317 | 70.667% | 29.333% | 22 | 26 | 0.871 | 53.333% |

| Fixed \\(\\lambda=0.10\\) | 0.013249 | 74.667% | 25.333% | 19 | 34 | 0.972 | 45.333% |

| Fixed \\(\\lambda=0.25\\) | 0.009923 | 81.333% | 18.667% | 14 | 44 | 0.908 | 52.000% |

| Fixed \\(\\lambda=1.00\\) | 0.001460 | 93.333% | 6.667% | 3 | 64 | 0.190 | 94.667% |

| Lexicographic baseline | 0.003148 | 90.667% | 9.333% | 5 | 55 | 0.784 | 66.667% |

| Responsive-optimality model | 0.003148 | 90.667% | 9.333% | 5 | 55 | 0.784 | 66.667% |

| Oracle equivalence | 0.001372 | 94.667% | 5.333% | 3 | 35 | 0.998 | 36.000% |

| Fixed \\(k=3\\) | 0.000300 | 96.000% | 4.000% | 0 | 65 | 0.000 | 100.000% |

| Action oracle | 0.000000 | 100.000% | 0.000% | 0 | 0 | 0.883 | 53.333% |



\---



\## No Policy-Level Improvement



The responsive-optimality model produced exactly the same policy-level outcome as the deterministic lexicographic baseline.



Both achieved



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



The zero-regret fraction remained



\\\[

90.667\\%,

\\]



and the high-regret fraction remained



\\\[

9.333\\%.

\\]



Therefore the new responsive learning target did not produce a measurable improvement in final persistence behavior.



\---



\## Recovery Metrics



The deterministic lexicographic baseline achieved



\\\[

\\bar\\lambda\_{\\text{baseline}}

=

0.5573,

\\]



\\\[

\\text{minimum-set recovery}

=

96.000\\%,

\\]



and



\\\[

\\text{responsive-oracle accuracy}

=

37.333\\%.

\\]



The responsive-optimality model achieved



\\\[

\\bar\\lambda\_{\\text{responsive}}

=

0.6053,

\\]



\\\[

\\text{minimum-set recovery}

=

96.000\\%,

\\]



and



\\\[

\\text{responsive-oracle accuracy}

=

36.000\\%.

\\]



Thus the learned secondary model preserved consequence-safe membership but slightly worsened the operating-point responsiveness metric.



\---



\## Movement in the Wrong Direction



The learned responsive model increased mean selected risk strength from



\\\[

0.5573

\\]



to



\\\[

0.6053.

\\]



Therefore the model became more conservative on average.



Responsive-oracle accuracy simultaneously decreased from



\\\[

37.333\\%

\\]



to



\\\[

36.000\\%.

\\]



This indicates that direct classification of the least-conservative safe operating point did not recover the desired ordering signal.



The failure is not catastrophic because the primary consequence gate continues to protect policy-level regret.



However, the secondary learner does not provide useful improvement.



\---



\## Important Invariance



Although mean selected \\(\\lambda\\) changed, the final policy metrics did not.



Specifically,



\\\[

\\bar\\lambda

:

0.5573

\\rightarrow

0.6053

\\]



while



\\\[

R,

\\]



\\\[

N\_{\\text{under}},

\\]



\\\[

N\_{\\text{over}},

\\]



and



\\\[

H

\\]



all remained unchanged.



This is an important structural clue.



It suggests that many of the differing risk-level selections produced the same downstream persistence action.



Therefore:



\\\[

\\boxed{

\\text{operating-point identity}

\\neq

\\text{effective persistence behavior}.

}

\\]



The secondary learner may be making mistakes in \\(\\lambda\\)-space that are behaviorally irrelevant in action space.



\---



\## Action-Level Redundancy Hypothesis



Suppose two operating points satisfy



\\\[

\\lambda\_i

\\neq

\\lambda\_j

\\]



but induce



\\\[

a\_t(\\lambda\_i)

=

a\_t(\\lambda\_j).

\\]



Then selecting either operating point produces identical persistence behavior.



A secondary model trained to distinguish the two \\(\\lambda\\) labels is solving a harder problem than the controller actually needs to solve.



This may explain why:



\\\[

\\text{mean selected }\\lambda

\\]



changes while



\\\[

\\text{action entropy}

\\]



does not.



The model may be rearranging operating-point labels inside action-equivalent regions.



\---



\## Relationship to Experiment 070



Experiment 070 already established extensive action equivalence.



Every held-out context contained at least one pair of action-equivalent operating points.



The largest exact action-equivalence class had size:



\- 2 in 29.333% of contexts,

\- 3 in 53.333%,

\- 4 in 17.333%.



Thus action redundancy is extremely common.



Experiment 073 now provides additional evidence that this redundancy matters for learning.



The secondary learner can alter \\(\\lambda\\)-level decisions without changing effective control behavior.



\---



\## Why the Secondary Label May Be Mis-Specified



The target



\\\[

\\lambda\_t^{\\text{responsive}}

=

\\min\\Lambda\_t^\*

\\]



assumes that the least-conservative risk parameter is itself the meaningful endpoint.



However, the digital twin ultimately executes a persistence action



\\\[

a\_t.

\\]



If several risk levels all produce the same action, ordering those risk levels has no behavioral value.



The more meaningful secondary question may instead be:



\\\[

\\boxed{

\\text{Which consequence-safe candidate produces the most responsive}

\\atop

\\text{persistence action?}

}

\\]



This suggests replacing operating-point-level responsive optimality with action-effective responsiveness.



\---



\## Emerging Action-Effective Objective



For each safe candidate, define its executed persistence action



\\\[

a\_t(\\lambda).

\\]



Within the true minimum-regret set, define the most responsive safe action as



\\\[

a\_t^{\\text{responsive}}

=

\\min\_{

\\lambda\\in\\Lambda\_t^\*

}

a\_t(\\lambda),

\\]



assuming lower persistence depth corresponds to greater responsiveness.



The secondary learner could then target



\\\[

P

\\left(

a\_t(\\lambda)

=

a\_t^{\\text{responsive}}

\\mid

x\_t

\\right).

\\]



Alternatively, candidates could first be collapsed into action-equivalence classes, and the controller could rank those classes rather than individual \\(\\lambda\\) values.



This removes label distinctions that do not affect behavior.



\---



\## Training-Data Limitation



Experiment 073 also uses only



\\\[

53

\\]



secondary-training contexts.



The responsive-optimality target may be highly imbalanced because many contexts share the same responsive oracle level.



Therefore the negative result may reflect both:



1\. action-level redundancy, and

2\. limited secondary training support.



The present experiment does not distinguish these explanations completely.



However, the observed invariance of policy metrics despite changing mean \\(\\lambda\\) strongly motivates action-level analysis first.



\---



\## Structural Interpretation



Experiments 071–073 now reveal a hierarchy of increasingly precise questions.



\### Experiment 071



Can the controller identify the consequence-safe set?



Result:



\\\[

96\\%

\\]



minimum-set recovery.



\### Experiment 072



Can a second model improve safe-set membership discrimination?



Result:



No.



The secondary signal was redundant.



\### Experiment 073



Can a model directly predict the least-conservative safe operating point?



Result:



No policy-level improvement.



The model slightly worsened responsive-oracle accuracy and became more conservative in \\(\\lambda\\)-space.



However, downstream behavior remained unchanged.



This suggests that the remaining problem should be formulated in action space rather than operating-point label space.



\---



\## Principal Conclusion



Experiment 073 directly targets responsive operating-point ordering but does not improve the learned lexicographic controller.



The responsive-optimality model preserved



\\\[

96.000\\%

\\]



minimum-set recovery but reduced responsive-oracle accuracy from



\\\[

37.333\\%

\\]



to



\\\[

36.000\\%.

\\]



Mean selected risk strength increased:



\\\[

0.5573

\\rightarrow

0.6053.

\\]



Despite this change, all principal policy metrics remained identical:



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



Therefore:



\\\[

\\boxed{

\\text{improving the identity of the selected }\\lambda

\\text{ is not necessarily equivalent}

\\atop

\\text{to improving persistence behavior}.

}

\\]



The evidence points toward action-equivalent redundancy as the next structural issue to investigate.



\---



\## Next Research Direction



Experiment 074 should analyze action-effective responsiveness inside consequence-safe operating-point sets.



For every held-out context, it should determine:



\- the number of distinct persistence actions represented inside the predicted safe set,

\- the number of distinct actions represented inside the true minimum-regret set,

\- how often multiple risk levels collapse to the same action,

\- how often the lexicographic baseline and responsive model select different \\(\\lambda\\) values but the same action,

\- how often a more responsive safe action actually exists,

\- and the potential regret-free action reduction available.



Define the true safe-action set



\\\[

A\_t^\*

=

\\left\\{

a\_t(\\lambda):

\\lambda\\in\\Lambda\_t^\*

\\right\\}.

\\]



Then define the responsive safe action as



\\\[

a\_t^{\\text{responsive}}

=

\\min A\_t^\*.

\\]



The key distinction becomes



\\\[

\\boxed{

\\text{operating-point responsiveness}

\\neq

\\text{action-effective responsiveness}.

}

\\]



Experiment 074 should therefore ask:



\\\[

\\boxed{

\\text{How much of the remaining responsive-oracle gap is real}

\\atop

\\text{at the persistence-action level rather than only at the }\\lambda\\text{-label level?}

}

\\]

