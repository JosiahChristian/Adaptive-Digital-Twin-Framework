\# Experiment 092 — Action-Conditioned Support Representation Analysis



\## Objective



Experiment 091 established that the previously used support metric was not action-conditional.



For every audited context:



\\\[

d(x,k\_1)

=

d(x,k\_2)

=

d(x,k\_3).

\\]



The previous metric therefore measured:



\\\[

\\boxed{

\\text{context-level epistemic support}

}

\\]



rather than genuine action-conditioned support.



Experiment 092 constructs a new representation designed to vary jointly with:



\\\[

x

\\]



and:



\\\[

a.

\\]



The central questions are:



\\\[

\\boxed{

\\text{Can a genuinely action-conditioned support geometry be constructed?}

}

\\]



and:



\\\[

\\boxed{

\\text{Does that geometry contain information about realized}

\\atop

\\text{action consequence beyond context support and predicted loss?}

}

\\]



No controller is modified.



No new prospective seed block is consumed.



The experiment is retrospective and representation-focused.



\---



\# Analysis Population



Experiment 092 uses generation seeds:



\\\[

44001,\\ldots,44010.

\\]



The resulting test population contains:



\\\[

\\boxed{

772

}

\\]



contexts.



For each context, all three candidate persistence actions are evaluated:



\\\[

k\_1,

\\quad

k\_2,

\\quad

k\_3.

\\]



Therefore the total action-context population is:



\\\[

772\\times3

=

\\boxed{

2316

}

\\]



pairs.



\---



\# Action Consequence Label



Each action-context pair is labeled according to realized regret.



For context \\(x\\) and action \\(a\\):



\\\[

R(x,a)

=

L(x,a)

\-

L^\*(x).

\\]



An action is labeled unsafe when:



\\\[

\\boxed{

R(x,a)>0.005.

}

\\]



Using this definition, the population contains:



\\\[

\\boxed{

1688

\\text{ safe action-context pairs}

}

\\]



and:



\\\[

\\boxed{

628

\\text{ unsafe action-context pairs}.

}

\\]



Thus:



\\\[

72.884\\%

\\]



of the action-context pairs are safe and:



\\\[

27.116\\%

\\]



are unsafe.



\---



\# Context-Support Representation



The context-support representation uses the existing context/model features:



\\\[

\\phi(x)

\\]



together with predicted risk.



The resulting support distance is:



\\\[

\\boxed{

d\_{\\text{context}}(x).

}

\\]



This quantity is independent of candidate action.



It represents local familiarity of the operating context.



\---



\# New Action-Conditioned Representation



For each candidate action \\(a\\), Experiment 092 augments the context representation with action-dependent predicted consequence geometry.



The action-conditioned representation includes:



\\\[

\\hat L\_a,

\\]



\\\[

\\hat L\_a-\\min\_j\\hat L\_j,

\\]



\\\[

\\hat L\_a-\\operatorname{mean}\_j\\hat L\_j,

\\]



a normalized relative-loss quantity:



\\\[

\\frac{

\\hat L\_a-\\min\_j\\hat L\_j

}{

\\max\_j\\hat L\_j-\\min\_j\\hat L\_j

},

\\]



and predicted action-loss rank.



Thus:



\\\[

\\boxed{

z(x,a)

=

\[

\\phi(x),

\\text{risk}(x),

\\psi(x,a)

]

}

\\]



where:



\\\[

\\psi(x,a)

\\]



contains variables that genuinely vary with both context and action.



This is fundamentally different from appending a constant action identifier.



\---



\# Action-Conditioned Support Distance



For each action:



\\\[

a\\in\\{k\_1,k\_2,k\_3\\},

\\]



Experiment 092 computes:



\\\[

\\boxed{

d\_{\\text{action}}(x,a)

}

\\]



as the mean five-nearest-neighbor distance in the action-conditioned representation.



The query for action \\(a\\) is compared against training examples corresponding to the same candidate action, but the representation coordinates now vary within that action because the predicted consequence quantities vary across contexts.



Therefore action-specific nearest-neighbor geometry is mathematically possible.



\---



\# Action-Conditional Geometry Result



The first requirement is satisfied completely.



Across:



\\\[

772

\\]



contexts, the number exhibiting nonzero action-distance separation is:



\\\[

\\boxed{

772/772.

}

\\]



Therefore:



\\\[

\\boxed{

100.000\\%

}

\\]



of contexts have:



\\\[

d\_{\\text{action}}(x,k\_1),

\\quad

d\_{\\text{action}}(x,k\_2),

\\quad

d\_{\\text{action}}(x,k\_3)

\\]



that are not all identical.



The mean maximum pairwise action-distance difference is:



\\\[

\\boxed{

0.339021.

}

\\]



The maximum observed difference is:



\\\[

\\boxed{

2.015461.

}

\\]



Thus the new representation is genuinely action-conditioned.



\---



\# Contrast With Experiment 091



Experiment 091 found:



\\\[

\\boxed{

0/237

}

\\]



contexts with action-distance separation under the old representation.



Experiment 092 finds:



\\\[

\\boxed{

772/772.

}

\\]



Therefore the representation change successfully resolves the action-invariance problem.



The key difference is that action conditioning now comes from:



\\\[

\\boxed{

\\text{action-dependent predicted consequence geometry}

}

\\]



rather than from constant action labels.



\---



\# Context Support and Unsafe Actions



Mean context-support distance for safe action-context pairs is:



\\\[

3.067169.

\\]



For unsafe pairs:



\\\[

2.996283.

\\]



The standardized difference is:



\\\[

\\boxed{

\-0.024.

}

\\]



Thus context support alone provides essentially no useful separation between safe and unsafe candidate actions in this broader action-level population.



This is expected because the same context support value is shared across all three candidate actions within a context.



\---



\# Absolute Action-Conditioned Support



Mean action-conditioned support distance is:



\\\[

3.648395

\\]



for safe pairs and:



\\\[

3.728946

\\]



for unsafe pairs.



The standardized difference is:



\\\[

\\boxed{

+0.028.

}

\\]



Therefore absolute action-conditioned distance by itself also provides only weak separation.



This is an important negative result.



The newly constructed distance is geometrically valid, but its absolute magnitude is not automatically a strong risk indicator.



\---



\# Relative Action-Conditioned Support Excess



A more informative quantity emerges by comparing action-conditioned support with context support.



Define:



\\\[

\\boxed{

E(x,a)

=

d\_{\\text{action}}(x,a)

\-

d\_{\\text{context}}(x).

}

\\]



This quantity measures how much additional epistemic distance appears after candidate-action consequence geometry is introduced.



Experiment 092 refers to this quantity as:



\\\[

\\boxed{

\\textbf{action-conditioned epistemic excess}.

}

\\]



\---



\# Epistemic Excess Separation



For safe action-context pairs:



\\\[

E\_{\\text{safe}}

=

0.581226.

\\]



For unsafe pairs:



\\\[

E\_{\\text{unsafe}}

=

\\boxed{

0.732663.

}

\\]



The standardized difference is:



\\\[

\\boxed{

+0.378.

}

\\]



This is substantially larger than the effects for either support distance alone.



Therefore:



\\\[

\\boxed{

\\text{unsafe actions tend to exhibit greater action-conditioned}

\\atop

\\text{distance relative to the familiarity of their underlying context}.

}

\\]



This is the central representation-level finding of Experiment 092.



\---



\# Predicted Action Loss



Predicted action loss also separates safe from unsafe action-context pairs.



Safe mean:



\\\[

0.151348.

\\]



Unsafe mean:



\\\[

0.169435.

\\]



Standardized difference:



\\\[

\\boxed{

+0.283.

}

\\]



Thus the learned consequence model already contains useful information about action risk.



However, its separation is weaker than the epistemic-excess effect:



\\\[

0.283

<

0.378.

\\]



\---



\# Predicted Relative Loss



Predicted loss relative to the minimum predicted action loss is:



\\\[

0.010834

\\]



for safe actions and:



\\\[

0.014446

\\]



for unsafe actions.



Standardized effect:



\\\[

\\boxed{

+0.213.

}

\\]



Again, predicted consequence geometry is informative but not sufficient.



\---



\# Classification Models



Experiment 092 evaluates six simple leave-one-generation-seed-out logistic models.



The models are:



1\. context support only,

2\. predicted action loss only,

3\. context support plus predicted loss,

4\. action-conditioned support only,

5\. context support plus action-conditioned support,

6\. context support plus predicted loss plus action-conditioned support.



\---



\# Best Retrospective Model



The strongest model is:



\\\[

\\boxed{

\\text{context support + action-conditioned support}.

}

\\]



Its pooled performance is:



\\\[

\\boxed{

59.277\\%

\\text{ balanced accuracy}

}

\\]



\\\[

51.433\\%

\\text{ unsafe-action recall}

\\]



\\\[

36.788\\%

\\text{ unsafe-action precision}

\\]



\\\[

67.121\\%

\\text{ safe specificity}

\\]



and:



\\\[

\\boxed{

\\text{ROC-AUC}=0.619.

}

\\]



Mean fold balanced accuracy is:



\\\[

59.377\\%.

\\]



Mean fold ROC-AUC is:



\\\[

0.623.

\\]



Thus the new representation provides modest but consistent retrospective discrimination.



\---



\# Context Support Only



Context support alone performs poorly.



Balanced accuracy:



\\\[

\\boxed{

48.003\\%.

}

\\]



Unsafe recall:



\\\[

76.752\\%.

\\]



Safe specificity:



\\\[

19.254\\%.

\\]



ROC-AUC:



\\\[

\\boxed{

0.452.

}

\\]



The standardized coefficient is:



\\\[

\-0.027

\\]



with:



\\\[

100\\%

\\]



sign stability.



This confirms that context familiarity alone is not enough to identify which candidate actions will be unsafe.



\---



\# Predicted Loss Only



Predicted action loss alone achieves:



\\\[

52.947\\%

\\]



balanced accuracy and:



\\\[

0.571

\\]



ROC-AUC.



The standardized coefficient is:



\\\[

\\boxed{

+0.284

}

\\]



with:



\\\[

100\\%

\\]



sign stability.



Thus larger predicted action loss consistently corresponds to greater unsafe-action probability.



However, predictive performance remains limited.



\---



\# Context Plus Predicted Loss



Adding context support to predicted action loss produces:



\\\[

51.518\\%

\\]



balanced accuracy and:



\\\[

0.566

\\]



ROC-AUC.



This does not improve over predicted loss alone.



The coefficients remain:



\\\[

\\beta\_{\\text{loss}}

=

+0.290

\\]



and:



\\\[

\\beta\_{\\text{context}}

=

\-0.059.

\\]



Both signs are stable across all folds.



\---



\# Action-Conditioned Support Only



Action-conditioned support alone achieves:



\\\[

53.408\\%

\\]



balanced accuracy,



\\\[

28.025\\%

\\]



unsafe recall,



\\\[

78.791\\%

\\]



safe specificity,



and:



\\\[

0.554

\\]



ROC-AUC.



The coefficient is:



\\\[

+0.030

\\]



with:



\\\[

100\\%

\\]



sign stability.



This confirms that absolute action-conditioned distance alone is only weakly useful.



\---



\# Context Plus Action Support



The strongest model contains:



\\\[

d\_{\\text{context}}

\\]



and:



\\\[

d\_{\\text{action}}.

\\]



Its mean standardized coefficients are:



\\\[

\\boxed{

\\beta\_{\\text{context}}

=

\-2.280

}

\\]



and:



\\\[

\\boxed{

\\beta\_{\\text{action}}

=

+2.275.

}

\\]



Both coefficients have:



\\\[

\\boxed{

100\\%

}

\\]



sign stability.



The near-equal and opposite coefficient magnitudes are striking.



\---



\# Implicit Discovery of Epistemic Excess



Because:



\\\[

\\beta\_{\\text{action}}

\\approx

\-\\beta\_{\\text{context}},

\\]



the learned logistic model is approximately forming:



\\\[

d\_{\\text{action}}

\-

d\_{\\text{context}}.

\\]



Therefore the classifier independently recovers the same quantity suggested by the univariate analysis:



\\\[

\\boxed{

E(x,a)

=

d\_{\\text{action}}(x,a)

\-

d\_{\\text{context}}(x).

}

\\]



This provides convergent evidence that relative distance is more informative than either absolute distance.



\---



\# Context + Loss + Action Support



The three-variable model includes:



\\\[

d\_{\\text{context}},

\\]



\\\[

\\hat L\_a,

\\]



and:



\\\[

d\_{\\text{action}}.

\\]



It achieves:



\\\[

56.844\\%

\\]



balanced accuracy and:



\\\[

0.613

\\]



ROC-AUC.



This is weaker than the simpler two-distance model.



Its coefficients are:



\\\[

\\beta\_{\\text{context}}

=

\-1.840,

\\]



\\\[

\\beta\_{\\text{action}}

=

+1.811,

\\]



and:



\\\[

\\beta\_{\\text{loss}}

=

+0.183.

\\]



All signs are stable across all folds.



\---



\# Why Adding Predicted Loss Does Not Help



The action-conditioned representation itself includes several quantities derived from predicted loss geometry.



Therefore:



\\\[

d\_{\\text{action}}

\\]



already contains information related to:



\\\[

\\hat L\_a.

\\]



Adding predicted action loss explicitly may therefore introduce redundancy rather than new information.



The weaker three-variable result is consistent with this interpretation.



\---



\# Geometric Interpretation



The results suggest that the relevant question is not:



\\\[

\\text{“How far is this action-context representation from training?”}

\\]



by itself.



Instead, the useful comparison is:



\\\[

\\boxed{

\\text{“How much farther does the candidate action become}

\\atop

\\text{once action-dependent consequence geometry is introduced?”}

}

\\]



This is measured by:



\\\[

E(x,a)

=

d\_{\\text{action}}(x,a)

\-

d\_{\\text{context}}(x).

\\]



\---



\# Example Conceptual Cases



\## Familiar Context, Well-Supported Action



If:



\\\[

d\_{\\text{context}}

\\]



is small and:



\\\[

d\_{\\text{action}}

\\]



is only slightly larger, then:



\\\[

E(x,a)

\\]



is small.



The candidate action's consequence geometry is consistent with the familiar context.



\---



\## Unfamiliar Context, Uniformly Unfamiliar Actions



If:



\\\[

d\_{\\text{context}}

\\]



is large but all action-conditioned distances rise similarly, then epistemic excess may remain modest.



The problem may be general context unfamiliarity rather than action-specific uncertainty.



\---



\## Familiar Context, Action-Specific Departure



If:



\\\[

d\_{\\text{context}}

\\]



is moderate or small but:



\\\[

d\_{\\text{action}}

\\]



is substantially larger for a particular candidate action, then:



\\\[

E(x,a)

\\]



becomes large.



This suggests that the action's predicted consequence geometry is unusual relative to what would be expected from context familiarity alone.



Experiment 092 finds that this pattern is more common among unsafe actions.



\---



\# Action-Conditioned Epistemic Excess



Experiment 092 therefore introduces the candidate diagnostic:



\\\[

\\boxed{

E(x,a)

=

d\_{\\text{action}}(x,a)

\-

d\_{\\text{context}}(x).

}

\\]



A positive value means that introducing action-conditioned consequence geometry increases epistemic distance beyond the context baseline.



A larger value indicates greater action-specific departure.



The experiment provides initial retrospective evidence that:



\\\[

\\boxed{

E(x,a)\\uparrow

\\quad\\Rightarrow\\quad

P(\\text{unsafe action})\\uparrow.

}

\\]



This relationship is not yet prospectively validated.



\---



\# Why This Is Different From the Old Support Metric



The previous support metric answered:



\\\[

\\boxed{

\\text{“How familiar is context }x\\text{?”}

}

\\]



The new action-conditioned epistemic excess asks:



\\\[

\\boxed{

\\text{“How unusual is action }a\\text{'s consequence geometry}

\\atop

\\text{relative to the familiarity of context }x\\text{?”}

}

\\]



These are distinct epistemic questions.



The first concerns the operating environment.



The second concerns the candidate action within that environment.



\---



\# Representation Success Versus Predictive Strength



Experiment 092 should distinguish two conclusions.



\## Representation Success



The new construction successfully creates genuine action-conditioned geometry:



\\\[

\\boxed{

100\\%

\\text{ of contexts show action-distance separation}.

}

\\]



This is a strong and unambiguous result.



\## Predictive Strength



Unsafe-action classification is only moderate:



\\\[

\\boxed{

59.277\\%

\\text{ balanced accuracy}

}

\\]



for the best model.



Therefore the representation is useful but not sufficient as a standalone consequence predictor.



This distinction prevents overclaiming.



\---



\# Relationship to Realized Consequence



The action-conditioned representation is associated with realized regret, but it does not deterministically identify unsafe actions.



That is expected.



Realized consequence depends on:



\- context dynamics,

\- model error,

\- action sensitivity,

\- safe-set structure,

\- and potentially unmodeled interactions.



The new support representation should therefore be interpreted as an epistemic diagnostic rather than a direct oracle of safety.



\---



\# Methodological Limitation



The experiment is retrospective.



Seeds:



\\\[

44001\\text{--}44010

\\]



have already appeared in earlier research stages.



Therefore the relationship between epistemic excess and unsafe actions is hypothesis-generating.



No threshold on:



\\\[

E(x,a)

\\]



should be selected from this experiment and described as prospectively validated.



\---



\# Principal Conclusion



Experiment 092 successfully constructs the first genuinely action-conditioned support representation in the framework.



Across:



\\\[

772

\\]



contexts:



\\\[

\\boxed{

772/772

}

\\]



show nonzero action-distance separation.



The most informative derived quantity is:



\\\[

\\boxed{

E(x,a)

=

d\_{\\text{action}}(x,a)

\-

d\_{\\text{context}}(x).

}

\\]



Safe action-context pairs have mean:



\\\[

0.581226,

\\]



while unsafe pairs have mean:



\\\[

\\boxed{

0.732663.

}

\\]



The standardized difference is:



\\\[

\\boxed{

+0.378.

}

\\]



The strongest leave-one-seed-out model uses context and action-conditioned support jointly:



\\\[

\\boxed{

59.277\\%

\\text{ balanced accuracy}

}

\\]



with:



\\\[

\\boxed{

\\text{ROC-AUC}=0.619.

}

\\]



Its coefficients are nearly equal and opposite:



\\\[

\\boxed{

\-2.280

}

\\]



for context support and:



\\\[

\\boxed{

+2.275

}

\\]



for action support.



This independently identifies the relative quantity:



\\\[

\\boxed{

d\_{\\text{action}}

\-

d\_{\\text{context}}.

}

\\]



\---



\# Scientific Interpretation



The results support a new epistemic distinction:



\\\[

\\boxed{

\\text{context familiarity}

}

\\]



versus:



\\\[

\\boxed{

\\text{action-conditioned epistemic excess}.

}

\\]



A context can be familiar while a particular candidate action remains unusual in its predicted consequence geometry.



Likewise, a context can be globally unfamiliar without any one action being disproportionately unsupported.



This distinction was not available under the previous action-invariant support representation.



\---



\# Next Research Direction



Experiment 093 should remain diagnostic before any controller uses:



\\\[

E(x,a).

\\]



The next question should be whether action-conditioned epistemic excess is specifically relevant to the \*\*harmful expansion events that motivated the support architecture\*\*, rather than merely to unsafe actions in general.



The analysis should use existing consumed event datasets and compare:



\- beneficial expansion actions,

\- harmful expansion actions,

\- harmful state-vetoed actions,

\- beneficial state-vetoed actions,

\- and preserved responsive actions.



For each event, Experiment 093 should reconstruct:



\\\[

d\_{\\text{context}},

\\]



\\\[

d\_{\\text{action}},

\\]



and:



\\\[

E(x,a).

\\]



The central question should be:



\\\[

\\boxed{

\\text{Does action-conditioned epistemic excess distinguish}

\\atop

\\text{harmful responsive expansions from beneficial ones}

\\atop

\\text{beyond context support alone?}

}

\\]



Only if that relationship is stable should a future experiment freeze an action-conditioned epistemic guard for evaluation on another untouched prospective seed block.

