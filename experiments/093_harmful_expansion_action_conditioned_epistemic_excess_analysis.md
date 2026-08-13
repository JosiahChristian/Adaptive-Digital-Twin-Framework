\# Experiment 093 — Harmful-Expansion Action-Conditioned Epistemic-Excess Analysis



\## Objective



Experiment 092 introduced a genuinely action-conditioned support representation and defined:



\\\[

\\boxed{

E(x,a)

=

d\_{\\text{action}}(x,a)

\-

d\_{\\text{context}}(x)

}

\\]



as:



\\\[

\\boxed{

\\text{action-conditioned epistemic excess}.

}

\\]



In the general action-context population, larger epistemic excess was associated with unsafe actions.



Experiment 093 asks whether that same quantity specifically explains the harmful responsive-expansion failure mode.



The central question is:



\\\[

\\boxed{

\\text{Does action-conditioned epistemic excess distinguish}

\\atop

\\text{harmful responsive expansions from beneficial ones?}

}

\\]



The experiment is retrospective.



No controller threshold is defined.



No prospective seed block is consumed.



\---



\# Analysis Population



The analysis uses the existing harmful-expansion event population from generation seeds:



\\\[

44001,\\ldots,44010.

\\]



The input event file is:



`results/cross\_seed\_harmful\_expansion\_feature\_decomposition\_events.csv`



Only beneficial and harmful responsive expansion events are retained.



The resulting population contains:



\\\[

\\boxed{

65

}

\\]



events:



\\\[

\\boxed{

50

\\text{ beneficial}

}

\\]



and:



\\\[

\\boxed{

15

\\text{ harmful}.

}

\\]



For every event, Experiment 093 reconstructs the context and action-conditioned support geometry introduced in Experiment 092.



\---



\# Reconstructed Quantities



For each responsive expansion event, the following quantities are calculated:



\\\[

d\_{\\text{context}}(x),

\\]



\\\[

d\_{\\text{action}}(x,a),

\\]



\\\[

E(x,a)

=

d\_{\\text{action}}(x,a)

\-

d\_{\\text{context}}(x),

\\]



\\\[

\\hat L\_a,

\\]



and:



\\\[

\\hat L\_a-\\min\_j\\hat L\_j.

\\]



These permit direct comparison of:



\- context familiarity,

\- action-conditioned support,

\- epistemic excess,

\- absolute predicted action loss,

\- and relative predicted action loss.



\---



\# Context Support



Beneficial expansions have mean context-support distance:



\\\[

1.460865.

\\]



Harmful expansions have:



\\\[

1.477424.

\\]



The difference is:



\\\[

+0.016559.

\\]



The standardized effect is:



\\\[

\\boxed{

+0.057.

}

\\]



Thus context familiarity alone provides essentially no meaningful separation between harmful and beneficial responsive expansions in this event population.



\---



\# Absolute Action-Conditioned Support



Beneficial expansions have mean action-conditioned distance:



\\\[

1.932128.

\\]



Harmful expansions have:



\\\[

1.919207.

\\]



The difference is:



\\\[

\-0.012921.

\\]



The standardized effect is:



\\\[

\\boxed{

\-0.043.

}

\\]



Thus absolute action-conditioned support distance also provides negligible separation.



\---



\# Action-Conditioned Epistemic Excess



Beneficial expansions have mean:



\\\[

\\boxed{

E\_{\\text{beneficial}}

=

0.471264.

}

\\]



Harmful expansions have:



\\\[

\\boxed{

E\_{\\text{harmful}}

=

0.441784.

}

\\]



Therefore:



\\\[

\\Delta E

=

E\_{\\text{harmful}}

\-

E\_{\\text{beneficial}}

=

\\boxed{

\-0.029480.

}

\\]



The standardized difference is:



\\\[

\\boxed{

\-0.120.

}

\\]



This direction is opposite the simple hypothesis that harmful responsive expansions would exhibit greater action-conditioned epistemic excess.



\---



\# Negative Epistemic-Excess Result



Experiment 092 showed that larger:



\\\[

E(x,a)

\\]



was associated with unsafe actions in the general action-context population.



Experiment 093 shows that this relationship does not transfer cleanly to the specific harmful-expansion event population.



Therefore:



\\\[

\\boxed{

\\text{action-conditioned epistemic excess is not a useful}

\\atop

\\text{standalone discriminator of harmful responsive expansion}.

}

\\]



This is a central negative result.



\---



\# Epistemic-Excess-Only Classification



The leave-one-generation-seed-out epistemic-excess model achieves:



\\\[

\\boxed{

53.000\\%

\\text{ balanced accuracy}

}

\\]



with:



\\\[

60.000\\%

\\]



harmful recall,



\\\[

25.000\\%

\\]



harmful precision,



\\\[

46.000\\%

\\]



beneficial specificity,



and:



\\\[

\\boxed{

\\text{ROC-AUC}=0.464.

}

\\]



Thus the model performs only slightly above chance on thresholded balanced accuracy and below random ranking performance by AUC.



\---



\# Epistemic-Excess Coefficient



The epistemic-excess-only logistic model has mean standardized coefficient:



\\\[

\\boxed{

\-0.126.

}

\\]



Its sign is stable across:



\\\[

\\boxed{

100\\%

}

\\]



of evaluated folds.



This means the retrospective classifier consistently assigns lower harmful probability to larger epistemic excess.



Therefore the negative direction is not merely a single-fold anomaly.



\---



\# Predicted Action Loss



A much stronger signal emerges from absolute predicted action loss.



Beneficial expansion actions have mean predicted loss:



\\\[

0.115915.

\\]



Harmful expansion actions have:



\\\[

\\boxed{

0.144640.

}

\\]



The difference is:



\\\[

\\boxed{

+0.028725.

}

\\]



The standardized effect is:



\\\[

\\boxed{

+0.683.

}

\\]



This is the strongest univariate separation among the tested quantities.



\---



\# Predicted-Loss-Only Classification



The predicted-action-loss-only model achieves:



\\\[

\\boxed{

66.333\\%

\\text{ balanced accuracy}

}

\\]



with:



\\\[

66.667\\%

\\]



harmful recall,



\\\[

37.037\\%

\\]



harmful precision,



\\\[

66.000\\%

\\]



beneficial specificity,



and:



\\\[

\\boxed{

\\text{ROC-AUC}=0.708.

}

\\]



This model therefore provides substantially stronger discrimination than any support-derived quantity.



\---



\# Predicted-Loss Coefficient Stability



The predicted-action-loss coefficient is:



\\\[

\\boxed{

+0.809.

}

\\]



Its sign is stable across:



\\\[

\\boxed{

100\\%

}

\\]



of leave-one-seed-out folds.



Thus:



\\\[

\\boxed{

\\hat L\_a\\uparrow

\\quad\\Rightarrow\\quad

P(\\text{harmful expansion})\\uparrow

}

\\]



is a highly stable retrospective relationship in this event population.



\---



\# Relative Predicted Loss



Predicted loss relative to the minimum predicted loss in the same context is:



\\\[

0.000010

\\]



for beneficial expansions and:



\\\[

0.000000

\\]



for harmful expansions.



The difference is effectively zero.



The standardized effect is:



\\\[

\-0.160.

\\]



Thus harmful expansions are not characterized by choosing actions that look relatively poor compared with other candidate actions.



Instead, the expanded action is usually approximately the predicted minimum-loss action.



\---



\# Absolute Versus Relative Loss



This distinction is important.



For many harmful expansion events:



\\\[

\\hat L\_a

\\approx

\\min\_j\\hat L\_j.

\\]



Therefore the controller can correctly identify the locally predicted best action while still entering a context where:



\\\[

\\hat L\_a

\\]



itself is elevated.



Conceptually:



\\\[

\\boxed{

\\text{“best predicted action”}

\\neq

\\text{“low absolute predicted consequence.”}

}

\\]



This suggests that relative action ranking and absolute consequence level should be treated as different control signals.



\---



\# Possible Failure Pattern



The harmful-expansion pattern may therefore be approximated as:



\\\[

\\boxed{

\\hat L\_a

\\text{ is elevated}

}

\\]



while:



\\\[

\\boxed{

\\hat L\_a-\\min\_j\\hat L\_j

\\approx0.

}

\\]



The action looks best relative to its alternatives, but the entire predicted loss floor is high.



This is a fundamentally different mechanism from epistemic support failure.



\---



\# Best Retrospective Multivariate Model



The highest pooled balanced accuracy is produced by:



\\\[

\\boxed{

\\text{context support}

\+

\\text{predicted action loss}

\+

\\text{epistemic excess}.

}

\\]



Its performance is:



\\\[

\\boxed{

66.667\\%

\\text{ balanced accuracy}

}

\\]



with:



\\\[

73.333\\%

\\]



harmful recall,



\\\[

35.484\\%

\\]



harmful precision,



\\\[

60.000\\%

\\]



beneficial specificity,



and:



\\\[

0.665

\\]



ROC-AUC.



Mean fold balanced accuracy is:



\\\[

70.856\\%.

\\]



Mean fold ROC-AUC is:



\\\[

0.711.

\\]



\---



\# Multivariate Coefficients



The three-variable model has mean coefficients:



\\\[

\\boxed{

\\beta\_{\\hat L\_a}

=

+1.003

}

\\]



\\\[

\\boxed{

\\beta\_E

=

\-0.293

}

\\]



and:



\\\[

\\boxed{

\\beta\_{d\_{\\text{context}}}

=

+0.285.

}

\\]



All three coefficient signs are stable across:



\\\[

\\boxed{

100\\%

}

\\]



of evaluated folds.



Predicted action loss clearly dominates in coefficient magnitude.



\---



\# Why the Multivariate Model Does Not Replace Predicted Loss Alone



Although the three-variable model has slightly greater thresholded balanced accuracy:



\\\[

66.667\\%

\\]



versus:



\\\[

66.333\\%,

\\]



its ROC-AUC is lower:



\\\[

0.665

\\]



versus:



\\\[

\\boxed{

0.708

}

\\]



for predicted action loss alone.



Therefore the more complex model does not provide uniformly stronger discrimination.



The small balanced-accuracy difference should not be interpreted as evidence that the extra variables materially improve ranking quality.



\---



\# Loss Plus Epistemic Excess



The model using:



\\\[

\\hat L\_a

\\]



and:



\\\[

E(x,a)

\\]



achieves:



\\\[

63.333\\%

\\]



balanced accuracy and:



\\\[

0.677

\\]



ROC-AUC.



This is weaker than predicted loss alone.



Its coefficients are:



\\\[

\\beta\_{\\hat L\_a}

=

+0.904

\\]



and:



\\\[

\\beta\_E

=

\-0.340.

\\]



Both signs are stable across every fold.



Therefore epistemic excess does not add clear incremental harmful-expansion information to predicted loss.



\---



\# Support-Derived Models



Support-derived models perform poorly.



\## Context Support Only



\\\[

44.000\\%

\\]



balanced accuracy and:



\\\[

0.360

\\]



ROC-AUC.



\## Action Support Only



\\\[

42.667\\%

\\]



balanced accuracy and:



\\\[

0.343

\\]



ROC-AUC.



\## Context Plus Action Support



\\\[

48.333\\%

\\]



balanced accuracy and:



\\\[

0.407

\\]



ROC-AUC.



\## Context Plus Epistemic Excess



\\\[

48.333\\%

\\]



balanced accuracy and:



\\\[

0.411

\\]



ROC-AUC.



Thus support geometry does not explain this specific failure mode well.



\---



\# Separation Between Experiments 092 and 093



Experiments 092 and 093 answer different questions.



\## Experiment 092



In the broad action-context population:



\\\[

E(x,a)

\\]



is associated with unsafe action consequence.



This establishes that action-conditioned epistemic excess carries some general action-level information.



\## Experiment 093



Within the much narrower population of actual responsive expansion events:



\\\[

E(x,a)

\\]



does not distinguish harmful from beneficial outcomes.



Therefore:



\\\[

\\boxed{

\\text{a useful general action-risk representation need not}

\\atop

\\text{explain the specific residual failure mode of a controller}.

}

\\]



This distinction is important.



\---



\# Scientific Value of the Negative Result



The correct response to the Experiment 092 finding would have been tempting:



\\\[

\\text{use large }E(x,a)\\text{ as a controller veto}.

\\]



Experiment 093 shows that this would not be well supported for harmful responsive expansion.



Thus the experimental sequence successfully prevents premature controller adoption.



The representation remains mathematically valid and potentially useful for other tasks.



It simply does not appear to target the harmful-expansion mechanism directly.



\---



\# No Epistemic-Excess Guard



Experiment 093 therefore explicitly rejects the immediate controller hypothesis:



\\\[

\\boxed{

\\text{“veto responsive expansion when }E(x,a)\\text{ is large.”}

}

\\]



No threshold on:



\\\[

E(x,a)

\\]



should advance to prospective controller testing based on the current evidence.



\---



\# Emerging Absolute-Loss Hypothesis



The strongest remaining signal is:



\\\[

\\boxed{

\\text{absolute predicted action loss}.

}

\\]



The data suggest a new diagnostic question:



\\\[

\\boxed{

\\text{Does harmful responsive expansion occur when the predicted}

\\atop

\\text{loss floor is elevated even though the chosen action is}

\\atop

\\text{locally optimal relative to alternatives?}

}

\\]



This shifts attention away from support geometry toward consequence-level calibration.



\---



\# Predicted Loss Floor



Define the predicted loss floor:



\\\[

\\boxed{

F(x)

=

\\min\_a \\hat L\_a(x).

}

\\]



Because responsive expansion actions are generally near the predicted minimum-loss action, harmful events may be associated with:



\\\[

F(x)

\\]



being large.



This would represent a contextual consequence warning rather than an action-ranking warning.



\---



\# Potential Architectural Interpretation



The controller currently reasons strongly about:



\\\[

\\hat L\_a-\\min\_j\\hat L\_j

\\]



when determining whether actions are approximately equivalent.



Experiment 093 suggests that it may also need to reason about:



\\\[

\\boxed{

\\min\_j\\hat L\_j

}

\\]



itself.



A context where every available action has relatively high predicted loss may deserve different treatment from a context where the best predicted action has low absolute consequence.



\---



\# Methodological Limitation



The harmful-expansion population remains small:



\\\[

15

\\]



harmful events.



Therefore all retrospective classifier metrics carry substantial uncertainty.



A single event corresponds to:



\\\[

6.667

\\]



percentage points of harmful recall.



The results should therefore be interpreted primarily through:



\- effect direction,

\- coefficient stability,

\- comparison across representations,

\- and consistency with the existing failure decomposition.



\---



\# Principal Conclusion



Experiment 093 finds that action-conditioned epistemic excess does not specifically explain harmful responsive expansion.



The key results are:



\\\[

\\boxed{

E\_{\\text{beneficial}}

=

0.471264

}

\\]



\\\[

\\boxed{

E\_{\\text{harmful}}

=

0.441784

}

\\]



with:



\\\[

\\boxed{

d=-0.120.

}

\\]



Epistemic excess alone achieves:



\\\[

53.000\\%

\\]



balanced accuracy and:



\\\[

0.464

\\]



ROC-AUC.



In contrast, predicted action loss exhibits:



\\\[

\\boxed{

d=+0.683

}

\\]



and achieves:



\\\[

\\boxed{

66.333\\%

\\text{ balanced accuracy}

}

\\]



with:



\\\[

\\boxed{

\\text{ROC-AUC}=0.708.

}

\\]



Thus:



\\\[

\\boxed{

\\text{absolute predicted consequence is substantially more}

\\atop

\\text{informative for harmful expansion than epistemic excess}.

}

\\]



\---



\# Final Interpretation



The current evidence supports the following distinction:



\\\[

\\boxed{

\\text{action-conditioned epistemic excess}

}

\\]



is useful for understanding general action-level uncertainty,



while:



\\\[

\\boxed{

\\text{absolute predicted action loss}

}

\\]



is more relevant to the specific harmful responsive-expansion mechanism.



Therefore the research should not force the support representation into a role the data do not support.



\---



\# Next Research Direction



Experiment 094 should investigate absolute-loss calibration and contextual loss-floor elevation.



The central quantities should include:



\\\[

F(x)

=

\\min\_a\\hat L\_a(x),

\\]



\\\[

\\operatorname{mean}\_a\\hat L\_a(x),

\\]



\\\[

\\max\_a\\hat L\_a(x),

\\]



\\\[

\\max\_a\\hat L\_a(x)-\\min\_a\\hat L\_a(x),

\\]



and the expanded action's:



\\\[

\\hat L\_a.

\\]



These should be compared between beneficial and harmful expansion events.



The analysis should ask:



\\\[

\\boxed{

\\text{Are harmful expansions concentrated in contexts where}

\\atop

\\text{the entire predicted loss surface is elevated?}

}

\\]



It should also compare predicted loss quantities against realized:



\\\[

L^\*(x),

\\]



realized expanded-action loss,



and incremental regret.



No controller threshold should be selected until the calibration structure is understood.



Only if a stable absolute-loss mechanism is identified should a future prospective experiment define and freeze an absolute-consequence guard.

