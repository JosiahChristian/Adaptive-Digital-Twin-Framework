\# Experiment 085 — Retrospective Multivariate Harmful-Expansion Separability



\## Objective



Experiment 084 established that residual harmful support-aware expansions exhibit several pre-decision feature differences from beneficial expansions across ten validation seeds.



The strongest actionable univariate signals included:



\\\[

\\text{predicted loss},

\\]



\\\[

\\text{current mismatch},

\\]



\\\[

\\text{anchor age},

\\]



\\\[

\\text{support distance},

\\]



\\\[

\\text{predicted regret margin},

\\]



and:



\\\[

\\text{action step}.

\\]



However, Experiment 084 analyzed these signals primarily one variable at a time.



Experiment 085 asks whether harmful expansions possess a compact multivariate signature that generalizes across generation seeds.



The central question is:



\\\[

\\boxed{

\\text{Can harmful expansions be retrospectively separated}

\\atop

\\text{from beneficial expansions using only pre-decision information?}

}

\\]



The experiment is deliberately constrained because only:



\\\[

\\boxed{15}

\\]



harmful events are available.



The goal is therefore not maximum classification performance.



The goal is to determine whether a simple, interpretable, cross-seed-stable signal exists.



\---



\# Experimental Population



The input is the event-level dataset produced by Experiment 084:



`results/cross\_seed\_harmful\_expansion\_feature\_decomposition\_events.csv`



Across generation seeds:



\\\[

44001,\\ldots,44010,

\\]



Experiment 084 recorded:



\\\[

70

\\]



support-aware action-changing events.



These consisted of:



\\\[

50

\\text{ beneficial},

\\]



\\\[

15

\\text{ harmful},

\\]



and:



\\\[

5

\\text{ neutral}.

\\]



Experiment 085 excludes the neutral events because the classification problem is specifically:



\\\[

\\boxed{

\\text{beneficial}

\\quad\\text{vs.}\\quad

\\text{harmful}.

}

\\]



The resulting analysis population is:



\\\[

\\boxed{

N=65

}

\\]



with:



\\\[

N\_{\\text{beneficial}}=50

\\]



and:



\\\[

N\_{\\text{harmful}}=15.

\\]



\---



\# Leakage Prevention



Only variables available before execution of the expanded action are permitted as predictors.



Realized outcome variables are excluded.



In particular, Experiment 085 does not use:



\- expanded regret,

\- incremental regret,

\- realized expanded-action consequence,

\- or any other post-decision quantity.



This distinction is essential because Experiment 084 showed that realized regret trivially separates harmful from beneficial events.



Such information cannot be used by an online controller before the action is executed.



Therefore:



\\\[

\\boxed{

X\_t

\\text{ contains only pre-decision information.}

}

\\]



\---



\# Validation Strategy



The experiment uses:



\\\[

\\boxed{

\\text{leave-one-generation-seed-out validation}.

}

\\]



For each fold, all events belonging to one generation seed are withheld.



The model is trained on events from the remaining seeds and evaluated on the held-out seed.



Thus events generated from the same seed never appear simultaneously in training and testing.



Conceptually:



\\\[

\\mathcal D\_{\\text{train}}

=

\\bigcup\_{s\\neq s^\*}

\\mathcal D\_s

\\]



and:



\\\[

\\mathcal D\_{\\text{test}}

=

\\mathcal D\_{s^\*}.

\\]



This is substantially stronger than randomly splitting the 65 events because a random event split could allow closely related observations from the same generated population to appear on both sides of the validation boundary.



\---



\# Classifier



Each feature family is evaluated using class-weighted logistic regression.



Continuous predictors are standardized using training-fold statistics before fitting the classifier.



The model therefore takes the form:



\\\[

P(

Y=\\text{harmful}\\mid X

)

=

\\sigma(

\\beta\_0+\\beta^\\top Z

),

\\]



where:



\\\[

\\sigma(z)

=

\\frac{1}{1+e^{-z}}

\\]



and \\(Z\\) denotes standardized predictors.



Class weighting compensates for the imbalance:



\\\[

50:15

\\]



between beneficial and harmful events.



A classification threshold of:



\\\[

0.50

\\]



is used throughout.



No threshold optimization is performed.



\---



\# Feature Families



Five deliberately constrained feature families are compared.



\## Gate Features



The gate model contains:



\\\[

\\{

\\text{support distance},

\\text{downside score},

\\text{predicted regret margin},

\\text{action step}

\\}.

\\]



This tests whether variables closely associated with the existing expansion mechanism are sufficient to identify harmful events.



\---



\## State Features



The state model contains only:



\\\[

\\{

\\text{current mismatch},

\\text{anchor age},

\\text{trigger score}

\\}.

\\]



This tests the hypothesis emerging from Experiment 084 that harmful expansion is associated with a particular dynamic operating regime.



\---



\## Loss Geometry



The loss-geometry model contains:



\\\[

\\hat L\_{k1},

\\quad

\\hat L\_{k2},

\\quad

\\hat L\_{k3},

\\]



and the pairwise differences:



\\\[

\\hat L\_{k1}-\\hat L\_{k2},

\\]



\\\[

\\hat L\_{k1}-\\hat L\_{k3},

\\]



\\\[

\\hat L\_{k2}-\\hat L\_{k3}.

\\]



This tests whether the shape and level of the learned action-loss surface distinguish harmful expansion.



\---



\## Compact Combined Signature



The compact combined model contains seven variables:



\\\[

\\{

\\hat L\_{k3},

\\text{current mismatch},

\\text{anchor age},

\\text{support distance},

\\text{predicted regret margin},

\\text{action step},

\\text{downside score}

\\}.

\\]



These were selected from the strongest pre-decision signals observed in Experiment 084.



\---



\## Extended Combined Signature



The extended model contains fourteen available pre-decision diagnostics spanning:



\- loss levels,

\- loss differences,

\- state variables,

\- support,

\- regret prediction,

\- action transition size,

\- downside,

\- and predicted under-persistence risk.



This model tests whether broader information improves discrimination.



Because the dataset contains only 15 harmful events, the extended model is treated cautiously.



\---



\# Pooled Out-of-Seed Performance



The leave-one-seed-out predictions are pooled across the 65 events.



The results are:



| Feature Set | Balanced Accuracy | Harmful Recall | Harmful Precision | Beneficial Specificity | ROC-AUC |

|---|---:|---:|---:|---:|---:|

| State | \*\*69.667%\*\* | \*\*73.333%\*\* | 39.286% | 66.000% | 0.717 |

| Combined Compact | 62.667% | 53.333% | 36.364% | 72.000% | 0.707 |

| Gate | 61.667% | 53.333% | 34.783% | 70.000% | 0.680 |

| Loss Geometry | 59.667% | 53.333% | 32.000% | 66.000% | 0.716 |

| Combined Extended | 59.333% | 46.667% | 33.333% | 72.000% | 0.693 |



The strongest pooled model is therefore:



\\\[

\\boxed{

\\text{state}.

}

\\]



\---



\# State-Model Confusion Structure



The state model produces:



\\\[

TP=11,

\\]



\\\[

FP=17,

\\]



\\\[

FN=4,

\\]



and:



\\\[

TN=33.

\\]



Therefore:



\\\[

\\boxed{

11/15

}

\\]



harmful expansions are identified.



This corresponds to:



\\\[

\\boxed{

73.333\\%

}

\\]



harmful recall.



At the same time:



\\\[

33/50

\\]



beneficial expansions are correctly retained, producing:



\\\[

66.000\\%

\\]



beneficial specificity.



The model therefore demonstrates meaningful but incomplete retrospective separability.



\---



\# Best Retrospective Feature Set



The best pooled result is:



\\\[

\\boxed{

X\_{\\text{state}}

=

\\{

\\text{anchor age},

\\text{current mismatch},

\\text{trigger score}

\\}.

}

\\]



Performance is:



\\\[

\\boxed{

\\text{balanced accuracy}=69.667\\%

}

\\]



\\\[

\\boxed{

\\text{harmful recall}=73.333\\%

}

\\]



\\\[

\\boxed{

\\text{beneficial specificity}=66.000\\%

}

\\]



and:



\\\[

\\boxed{

\\text{ROC-AUC}=0.717.

}

\\]



The fact that only three state variables outperform the larger models is important.



The remaining harmful-expansion problem appears to contain a meaningful dynamic-state signature rather than requiring a large high-dimensional classifier.



\---



\# State Coefficient Stability



The three state coefficients are exceptionally stable across leave-one-seed-out fits.



\## Anchor Age



Mean standardized coefficient:



\\\[

\\boxed{

\-0.757

}

\\]



with:



\\\[

\\boxed{

100\\%

}

\\]



sign stability.



Thus younger anchors are consistently associated with greater harmful-expansion probability.



\---



\## Current Mismatch



Mean standardized coefficient:



\\\[

\\boxed{

+0.644

}

\\]



with:



\\\[

\\boxed{

100\\%

}

\\]



sign stability.



Thus larger current mismatch is consistently associated with greater harmful-expansion probability.



\---



\## Trigger Score



Mean standardized coefficient:



\\\[

\\boxed{

\-0.360

}

\\]



with:



\\\[

\\boxed{

100\\%

}

\\]



sign stability.



Thus lower trigger scores are consistently associated with greater harmful-expansion probability.



\---



\# State-Signature Hypothesis



The state model therefore identifies the following directional signature:



\\\[

\\boxed{

\\text{younger anchor}

\+

\\text{higher mismatch}

\+

\\text{lower trigger score}

}

\\]



as the strongest compact retrospective signature of harmful expansion.



This result strengthens the mechanism suggested by Experiment 084.



A recently refreshed anchor does not necessarily imply that the system has reached a stable regime.



If mismatch remains elevated, reducing persistence may still be unsafe.



The trigger score contributes additional information about the surrounding transition regime.



\---



\# Gate-Model Findings



The gate model achieves:



\\\[

61.667\\%

\\]



balanced accuracy and:



\\\[

0.680

\\]



ROC-AUC.



Its strongest coefficients are:



\\\[

\\boxed{

\\text{support distance}: +0.972

}

\\]



and:



\\\[

\\boxed{

\\text{action step}: +0.704.

}

\\]



Both exhibit:



\\\[

\\boxed{

100\\%

}

\\]



sign stability.



This independently confirms two Experiment 084 observations.



Harmful expansion becomes more likely as admitted actions move farther from training support and as the responsive persistence reduction becomes larger.



Predicted regret margin is also generally positive:



\\\[

+0.305,

\\]



although its sign stability is lower:



\\\[

88.889\\%.

\\]



Predicted downside contributes little after the other gate variables are included.



\---



\# Loss-Geometry Findings



The loss-geometry model does not provide the strongest pooled classification:



\\\[

\\text{balanced accuracy}=59.667\\%.

\\]



However, it achieves:



\\\[

\\boxed{

\\text{ROC-AUC}=0.716,

}

\\]



which is nearly identical to the state model's:



\\\[

0.717.

\\]



Its fold-level behavior is also comparatively stable.



The most important coefficient is:



\\\[

\\boxed{

\\hat L\_{k2}-\\hat L\_{k3}: -0.567

}

\\]



with 100% sign stability.



Predicted loss at maximal persistence is:



\\\[

\\boxed{

\\hat L\_{k3}: +0.331

}

\\]



with 100% sign stability.



The individual predicted loss levels are all positive:



\\\[

\\hat L\_{k1}: +0.304,

\\]



\\\[

\\hat L\_{k2}: +0.280,

\\]



\\\[

\\hat L\_{k3}: +0.331.

\\]



These results reinforce the interpretation that harmful expansions occur in generally harder predicted operating contexts.



\---



\# Compact Combined Model



The seven-variable compact model achieves:



\\\[

62.667\\%

\\]



balanced accuracy,



\\\[

53.333\\%

\\]



harmful recall,



\\\[

72.000\\%

\\]



beneficial specificity,



and:



\\\[

0.707

\\]



ROC-AUC.



Its strongest stable coefficients are:



\\\[

\\boxed{

\\text{support distance}: +0.809

}

\\]



\\\[

\\boxed{

\\hat L\_{k3}: +0.685

}

\\]



\\\[

\\boxed{

\\text{current mismatch}: +0.308

}

\\]



\\\[

\\boxed{

\\text{action step}: +0.288

}

\\]



and:



\\\[

\\boxed{

\\text{anchor age}: -0.218.

}

\\]



Each of these has:



\\\[

100\\%

\\]



sign stability.



Therefore the major mechanisms discovered separately remain directionally consistent when combined.



However, combining them does not improve pooled classification.



\---



\# Extended Model



The fourteen-feature extended model produces:



\\\[

59.333\\%

\\]



balanced accuracy,



\\\[

46.667\\%

\\]



harmful recall,



and:



\\\[

0.693

\\]



ROC-AUC.



Thus increasing model dimensionality does not improve generalization.



This is an important negative result.



Given only:



\\\[

15

\\]



harmful events, the larger predictor space appears unnecessary and potentially counterproductive.



Therefore:



\\\[

\\boxed{

\\text{more features do not imply a better harmful-expansion model}.

}

\\]



\---



\# Fold Stability



Mean fold-level balanced accuracies are:



\\\[

\\text{state}=69.832\\%,

\\]



\\\[

\\text{compact}=73.092\\%,

\\]



\\\[

\\text{gate}=68.146\\%,

\\]



\\\[

\\text{loss geometry}=71.146\\%,

\\]



and:



\\\[

\\text{extended}=71.306\\%.

\\]



However, mean fold performance alone is insufficient because some held-out seeds contain very small event populations and some contain only one class.



The minimum evaluable fold balanced accuracies reveal substantial variation.



For the state model:



\\\[

\\boxed{

30.769\\%.

}

\\]



For the compact model:



\\\[

26.923\\%.

\\]



For the gate model:



\\\[

30.769\\%.

\\]



For the extended model:



\\\[

26.923\\%.

\\]



The loss-geometry model is more stable by this measure:



\\\[

\\boxed{

56.250\\%

}

\\]



minimum fold balanced accuracy.



Thus the state signature has strong coefficient-direction stability but uneven seed-level classification performance.



\---



\# Coefficient Stability Versus Predictive Stability



Experiment 085 reveals an important distinction.



The direction of several mechanisms is extremely stable:



\\\[

\\text{anchor age}<0,

\\]



\\\[

\\text{current mismatch}>0,

\\]



\\\[

\\text{trigger score}<0,

\\]



\\\[

\\text{support distance}>0,

\\]



\\\[

\\text{action step}>0.

\\]



Yet classification performance varies substantially across held-out seeds.



Therefore:



\\\[

\\boxed{

\\text{stable coefficient direction}

\\neq

\\text{uniform predictive performance}.

}

\\]



This prevents us from interpreting the retrospective classifier as a finished controller guard.



Instead, the stable coefficients provide evidence about the underlying failure regime.



\---



\# Why the State Model Matters



The state model is particularly interesting because none of its variables directly represents the learned safe-membership probability.



The model instead describes the temporal and dynamical state of the adaptive system.



The strongest harmful-expansion signature is therefore not:



\\\[

\\text{low safety confidence}.

\\]



It is approximately:



\\\[

\\boxed{

\\text{recent anchor}

\+

\\text{persistent mismatch}

\+

\\text{lower trigger evidence}.

}

\\]



This suggests that the residual safety failure may arise from \*\*premature responsiveness during transient adaptation\*\*.



The controller may possess enough evidence to classify a lower-persistence action as nominally safe while still lacking enough evidence that the evolving system has stabilized around its recent anchor.



\---



\# Emerging Mechanistic Interpretation



The results from Experiments 079 through 085 increasingly support a layered interpretation.



The safe-action classifier answers approximately:



\\\[

\\text{“Could this action be safe?”}

\\]



Training-support distance asks:



\\\[

\\text{“Have we seen enough nearby evidence?”}

\\]



The newly identified state signature may be answering a different question:



\\\[

\\boxed{

\\text{“Has the system remained dynamically stable long enough}

\\atop

\\text{to trust the responsive action?”}

}

\\]



This distinction is important.



A candidate action may simultaneously have:



\- high predicted safety,

\- acceptable predicted downside,

\- adequate training support,



while still being dangerous because the current adaptive state is transient.



Experiment 085 therefore suggests that \*\*temporal adaptation state\*\* may be a missing dimension of the expansion gate.



\---



\# What Experiment 085 Does Not Establish



Experiment 085 does not establish that the state model should be inserted directly into the controller.



The same ten seeds were previously used to:



\- discover the harmful-expansion problem,

\- characterize support distance,

\- evaluate support-aware expansion,

\- decompose seed-level failures,

\- and identify candidate features.



Therefore the current feature selection and interpretation are adaptive with respect to these seeds.



Even leave-one-seed-out evaluation cannot convert the entire analysis history into untouched prospective validation.



Accordingly:



\\\[

\\boxed{

\\text{Experiment 085 is retrospective hypothesis generation.}

}

\\]



It is not prospective controller validation.



\---



\# Principal Conclusion



Experiment 085 demonstrates that residual harmful support-aware expansions contain a meaningful multivariate pre-decision signature.



Among five deliberately constrained feature families, the simplest state model performs best on pooled out-of-seed predictions:



\\\[

\\boxed{

\\text{balanced accuracy}=69.667\\%

}

\\]



\\\[

\\boxed{

\\text{harmful recall}=73.333\\%

}

\\]



\\\[

\\boxed{

\\text{beneficial specificity}=66.000\\%

}

\\]



\\\[

\\boxed{

\\text{ROC-AUC}=0.717.

}

\\]



Its three coefficients are directionally stable across every evaluable leave-one-seed-out fit:



\\\[

\\boxed{

\\text{anchor age}: -0.757

}

\\]



\\\[

\\boxed{

\\text{current mismatch}: +0.644

}

\\]



\\\[

\\boxed{

\\text{trigger score}: -0.360.

}

\\]



Thus the strongest compact retrospective signature is:



\\\[

\\boxed{

\\text{younger anchor}

\+

\\text{higher current mismatch}

\+

\\text{lower trigger score}.

}

\\]



Support distance and action-step magnitude remain independently stable risk indicators, while predicted loss geometry confirms that harmful events occur in more difficult learned operating regimes.



However, substantial seed-to-seed variation remains.



Therefore the correct conclusion is:



\\\[

\\boxed{

\\text{a stable retrospective mechanism signature has been identified,}

\\atop

\\text{but no new controller guard has yet been validated}.

}

\\]



\---



\# Next Research Direction



The next experiment should convert the retrospective state signature into a \*\*frozen prospective hypothesis\*\* before examining any new generation seeds.



The purpose should not be to search broadly for a better classifier.



Instead, a simple guard should be defined from the already observed directional structure.



Conceptually, the guard should become more conservative when the system exhibits some combination of:



\\\[

\\text{young anchor},

\\]



\\\[

\\text{high current mismatch},

\\]



and:



\\\[

\\text{low trigger score}.

\\]



The specification must be frozen before fresh-seed outcomes are examined.



Fresh generation seeds should then evaluate whether the guard:



1\. reduces harmful expansions,

2\. reduces under-persistence errors,

3\. preserves beneficial responsive recoveries,

4\. preserves overall regret performance,

5\. and generalizes beyond seeds used during hypothesis development.



The central prospective question becomes:



\\\[

\\boxed{

\\text{Does a frozen transient-state guard reduce harmful}

\\atop

\\text{support-aware expansion on untouched generation seeds?}

}

\\]



A successful result would transform the current retrospective mechanism into genuine out-of-sample controller evidence.



A failed result would be equally informative, demonstrating that the observed state signature is descriptive rather than operationally generalizable.

