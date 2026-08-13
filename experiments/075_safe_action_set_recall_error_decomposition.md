\# Experiment 075 — Safe-Action-Set Recall and Error Decomposition



\## Objective



Experiment 074 established that the dominant remaining responsiveness problem is not primarily secondary tie-breaking.



The learned controller often fails earlier by excluding genuinely safe persistence actions from the predicted consequence-safe set.



Experiment 075 therefore decomposes the remaining error into two distinct failure modes:



\\\[

\\boxed{

\\text{gate failure}

}

\\]



when the true responsive action is not admitted into the predicted safe-action set, and



\\\[

\\boxed{

\\text{selection failure}

}

\\]



when the responsive action is available but the controller fails to choose it.



The experiment also measures the broader quality of the predicted safe-action set using:



\\\[

\\text{SafeActionRecall}

=

\\frac{

|A\_t^\*\\cap\\hat A\_t^{\\text{safe}}|

}{

|A\_t^\*|

},

\\]



and



\\\[

\\text{SafeActionPrecision}

=

\\frac{

|A\_t^\*\\cap\\hat A\_t^{\\text{safe}}|

}{

|\\hat A\_t^{\\text{safe}}|

}.

\\]



The central question is



\\\[

\\boxed{

\\text{Is the remaining responsiveness gap caused mainly by}

\\atop

\\text{safe-action exclusion or by poor selection after admission?}

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



The three-way partition remained:



| Partition | Contexts |

|---|---:|

| Base-model training | 121 |

| Regret-model training | 53 |

| Held-out testing | 75 |



The primary predicted-regret tolerance remained



\\\[

\\boxed{

\\epsilon\_{\\text{primary}}=0.0005.

}

\\]



This preserves direct comparability with Experiments 071 through 074.



\---



\## True Safe-Action Set



For each held-out context, define the true minimum-regret operating-point set



\\\[

\\Lambda\_t^\*

=

\\left\\{

\\lambda:

R\_t(\\lambda)=R\_t^{\\min}

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



The true responsive action is



\\\[

a\_t^{\\text{responsive}}

=

\\min A\_t^\*.

\\]



\---



\## Predicted Safe-Action Set



The learned regret models produce



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

\\lambda\\in\\hat\\Lambda\_t^{\\text{safe}}

\\right\\}.

\\]



Experiment 075 evaluates the overlap between



\\\[

A\_t^\*

\\]



and



\\\[

\\hat A\_t^{\\text{safe}}.

\\]



\---



\## Safe-Action-Set Quality



Mean safe-action recall was



\\\[

\\boxed{

80.000\\%

}.

\\]



Mean safe-action precision was



\\\[

\\boxed{

96.889\\%

}.

\\]



This asymmetry is highly informative.



The learned gate is not primarily over-permissive.



Instead, it is predominantly conservative:



\\\[

\\boxed{

\\text{high precision}

\\quad+\\quad

\\text{lower recall}.

}

\\]



The controller usually avoids admitting unsafe actions, but it excludes too many genuinely safe actions.



\---



\## Responsive Action Retention



The true responsive action remained available in the predicted safe set in



\\\[

47/75

\\]



contexts:



\\\[

\\boxed{

62.667\\%

}.

\\]



The responsive action was excluded in



\\\[

28/75

\\]



contexts:



\\\[

\\boxed{

37.333\\%

}.

\\]



Thus in more than one third of the held-out population, the controller is structurally incapable of choosing the most responsive safe action because that action is removed before secondary selection begins.



\---



\## Error Decomposition



The final responsive-action outcomes decompose into:



| Outcome | Contexts | Fraction |

|---|---:|---:|

| Gate failure | 28 | 37.333% |

| Selection failure | 1 | 1.333% |

| Correct responsive selection | 46 | 61.333% |



This is the central result of Experiment 075.



Gate failures outnumber selection failures by



\\\[

\\frac{28}{1}

=

28\.

\\]



Therefore:



\\\[

\\boxed{

\\text{the dominant remaining error occurs before the selector acts.}

}

\\]



\---



\## Gate Failure Definition



A gate failure occurs when



\\\[

a\_t^{\\text{responsive}}

\\notin

\\hat A\_t^{\\text{safe}}.

\\]



There were



\\\[

\\boxed{

28

}

\\]



such contexts.



In every one of those cases, no downstream tie-breaking or ranking procedure can recover the true responsive action because it is not present in the admissible candidate set.



This formally explains why the secondary-learning experiments produced little or no improvement.



\---



\## Selection Failure Definition



A selection failure occurs when



\\\[

a\_t^{\\text{responsive}}

\\in

\\hat A\_t^{\\text{safe}}

\\]



but the selected action is not



\\\[

a\_t^{\\text{responsive}}.

\\]



Only



\\\[

\\boxed{

1/75

=

1.333\\%

}

\\]



of contexts exhibited this failure.



Thus once the responsive action survives the gate, the existing lexicographic selection rule almost always chooses it correctly.



This is a major architectural result:



\\\[

\\boxed{

\\text{responsive selection is nearly solved conditional on action retention.}

}

\\]



\---



\## Correct Responsive Selection



The baseline controller selected the true responsive minimum-regret action in



\\\[

46/75

\\]



contexts:



\\\[

\\boxed{

61.333\\%

}.

\\]



This exactly matches the responsive-action accuracy identified in Experiment 074.



Experiment 075 explains the remaining 38.667% error:



\\\[

37.333\\%

\\]



comes from gate exclusion, while only



\\\[

1.333\\%

\\]



comes from downstream selection.



\---



\## Safe-Set False Negatives



Contexts containing at least one missed true-safe action totaled



\\\[

28/75

=

37.333\\%.

\\]



Across those contexts, the total number of missed safe actions was



\\\[

\\boxed{

29\.

}

\\]



Furthermore, the predicted safe-action set collapsed to a singleton while the true safe-action set contained multiple actions in



\\\[

25/75

\\]



contexts:



\\\[

\\boxed{

33.333\\%

}.

\\]



This directly quantifies the contraction observed qualitatively in Experiment 074.



\---



\## False-Negative Conservatism



The false-negative pattern is especially important because missed actions are not random alternatives.



Many of the omitted actions correspond to lower persistence and therefore greater responsiveness.



The controller is effectively converting a truly multi-action minimum-regret region into an artificially unique conservative choice.



This can be summarized as



\\\[

\\boxed{

|A\_t^\*|>1

\\quad\\longrightarrow\\quad

|\\hat A\_t^{\\text{safe}}|=1.

}

\\]



This occurs in one third of the held-out contexts.



\---



\## Safe-Set False Positives



False-safe action inclusion occurred in only



\\\[

3/75

\\]



contexts:



\\\[

\\boxed{

4.000\\%

}.

\\]



The total number of false-safe actions was



\\\[

3\.

\\]



Thus safe-set overexpansion is currently rare.



This is consistent with the high mean safe-action precision of



\\\[

96.889\\%.

\\]



\---



\## Cost of False-Safe Inclusion



Although false positives were rare, they were not harmless.



The mean realized regret associated with false-safe actions was



\\\[

\\boxed{

0.044397

}.

\\]



The maximum false-safe regret was



\\\[

\\boxed{

0.095188.

}

\\]



This creates an important asymmetry.



Missing a genuinely safe action causes unnecessary conservatism.



Including a genuinely unsafe action can produce substantial regret.



Therefore the next controller cannot simply enlarge the safe set indiscriminately.



\---



\## Error Asymmetry



The safe-action-set problem now contains two qualitatively different risks.



\### False Negative



A true-safe action is excluded:



\\\[

a\\in A\_t^\*

\\quad\\text{but}\\quad

a\\notin\\hat A\_t^{\\text{safe}}.

\\]



Consequence:



\\\[

\\text{lost responsiveness}.

\\]



\### False Positive



An unsafe action is admitted:



\\\[

a\\notin A\_t^\*

\\quad\\text{but}\\quad

a\\in\\hat A\_t^{\\text{safe}}.

\\]



Consequence:



\\\[

\\text{potentially large regret}.

\\]



Because false-positive regret can be large, the expansion problem must be asymmetric and risk-sensitive.



\---



\## Why Simple Epsilon Expansion Is Insufficient



Experiments 069 and 071 already showed that widening a global tolerance eventually increases under-persistence and regret.



Experiment 075 explains why.



A larger global tolerance can recover some missed true-safe actions, but it can also admit the rare high-cost false-safe actions whose regret reaches values near



\\\[

0.095.

\\]



Thus a single global



\\\[

\\epsilon

\\]



cannot distinguish safe false negatives from dangerous false positives.



A better mechanism must estimate candidate-specific inclusion confidence.



\---



\## Primary Gate Is the Bottleneck



The recent experimental sequence now yields a decisive hierarchy.



\### Secondary Selection Quality



Conditional on responsive-action retention, only



\\\[

1/47

\\]



retained contexts fail at selection.



Therefore conditional selection accuracy is approximately



\\\[

\\frac{46}{47}

\\approx

97.9\\%.

\\]



This indicates that the downstream selector is already highly effective when the appropriate action is available.



\### Primary Gate Quality



The responsive action is absent entirely in



\\\[

28/75

\\]



contexts.



Therefore the overwhelming majority of remaining error is caused by insufficient safe-action coverage.



This establishes:



\\\[

\\boxed{

\\text{safe-action-set recall is the dominant remaining bottleneck.}

}

\\]



\---



\## Revised Performance Objective



The controller should no longer optimize only minimum predicted regret or operating-point classification accuracy.



The next target should explicitly preserve:



\\\[

\\text{high safe-action precision}

\\]



while increasing:



\\\[

\\text{safe-action recall}.

\\]



A useful constrained objective is



\\\[

\\max

\\quad

\\text{Recall}

\\]



subject to



\\\[

\\text{FalseSafeRegret}

\\leq

\\delta.

\\]



Equivalently, candidate expansion should be permitted only when the probability of true safe membership is sufficiently high relative to the cost of a false inclusion.



\---



\## Candidate-Specific Expansion Principle



For an excluded candidate action \\(a\\), define



\\\[

p\_t^{\\text{safe}}(a)

=

P

\\left(

a\\in A\_t^\*

\\mid

x\_t

\\right).

\\]



Expansion can then use a threshold



\\\[

\\tau.

\\]



An excluded action is added to the predicted safe set when



\\\[

p\_t^{\\text{safe}}(a)

\\geq

\\tau.

\\]



Different thresholds produce a recall–precision frontier.



The important distinction from Experiment 072 is that this model should target \*\*action-level safe membership\*\*, not operating-point-level membership.



This removes redundant \\(\\lambda\\)-labels and directly addresses the missing action identified by Experiment 075.



\---



\## Structural Interpretation



Experiments 071 through 075 now form a coherent diagnostic chain.



\### Experiment 071



Established strong minimum-regret operating-point recovery.



\### Experiment 072



Showed that another operating-point safe-membership model adds no value.



\### Experiment 073



Showed that responsive \\(\\lambda\\)-classification does not improve behavior.



\### Experiment 074



Revealed that action-level responsiveness is the correct representation and exposed safe-action-set contraction.



\### Experiment 075



Quantified that contraction and demonstrated that nearly all remaining responsive error is gate failure rather than selection failure.



The research problem has therefore moved upstream from secondary decision-making to candidate-set construction.



\---



\## Principal Conclusion



Experiment 075 establishes that the learned consequence-safe gate is highly precise but insufficiently sensitive.



Mean safe-action precision is



\\\[

\\boxed{

96.889\\%

}

\\]



while mean recall is only



\\\[

\\boxed{

80.000\\%.

}

\\]



The true responsive action is excluded in



\\\[

\\boxed{

37.333\\%

}

\\]



of contexts.



The final error decomposition is:



\\\[

\\boxed{

37.333\\%

\\text{ gate failure}

}

\\]



versus



\\\[

\\boxed{

1.333\\%

\\text{ selection failure}.

}

\\]



Therefore:



\\\[

\\boxed{

\\text{the remaining responsiveness problem is overwhelmingly a}

\\atop

\\text{safe-action-set recall problem}.

}

\\]



However, safe-set expansion must be controlled carefully because false-safe actions, while rare, produced mean regret



\\\[

0.044397

\\]



and maximum regret



\\\[

0.095188.

\\]



The next controller must therefore improve recall without materially degrading precision or admitting high-regret unsafe actions.



\---



\## Next Research Direction



Experiment 076 should introduce calibrated asymmetric safe-action-set expansion.



The primary predicted safe set should remain unchanged.



For actions excluded by that gate, a new action-level model should estimate



\\\[

\\hat p\_t^{\\text{safe}}(a)

=

P

\\left(

a\\in A\_t^\*

\\mid

x\_t

\\right).

\\]



Several confidence thresholds should then be evaluated.



An excluded action should be added only when



\\\[

\\hat p\_t^{\\text{safe}}(a)

\\geq

\\tau.

\\]



The resulting expanded set is



\\\[

\\hat A\_t^{\\text{expanded}}(\\tau)

=

\\hat A\_t^{\\text{primary}}

\\cup

\\left\\{

a:

\\hat p\_t^{\\text{safe}}(a)

\\geq

\\tau

\\right\\}.

\\]



Experiment 076 should measure:



\- safe-action recall,

\- safe-action precision,

\- responsive-action retention,

\- gate-failure rate,

\- selection-failure rate,

\- false-safe inclusion frequency,

\- mean and maximum false-safe regret,

\- final policy regret,

\- under-persistence,

\- over-persistence,

\- action entropy,

\- and dominant-action concentration.



The principal objective is



\\\[

\\boxed{

\\text{increase responsive-action retention while preserving}

\\atop

\\text{high precision and bounded false-safe regret}.

}

\\]



The central question becomes



\\\[

\\boxed{

\\text{Can calibrated action-level expansion recover missed safe actions}

\\atop

\\text{without opening the gate to dangerous false positives?}

}

\\]

