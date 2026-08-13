\# Experiment 078 — Realized Selection-Risk Decomposition



\## Objective



Experiment 077 established that cost-aware safe-action expansion is superior to probability-only expansion.



At the best tested cost-aware operating point,



\\\[

\\boxed{

p=0.60,

\\qquad

d=0.020,

}

\\]



the controller achieved:



\\\[

\\text{safe-action recall}

=

92.000\\%,

\\]



\\\[

\\text{safe-action precision}

=

96.222\\%,

\\]



\\\[

\\text{responsive-action retention}

=

85.333\\%,

\\]



with



\\\[

R

=

0.004084

\\]



and only



\\\[

2

\\]



harmful expansion contexts.



Experiment 078 freezes that operating point and studies those surviving failures directly.



The objective is not to build another controller.



It is to determine what distinguishes:



\\\[

\\boxed{

\\text{beneficial expansions}

}

\\]



from



\\\[

\\boxed{

\\text{neutral expansions}

}

\\]



and



\\\[

\\boxed{

\\text{harmful expansions}.

}

\\]



The central question is



\\\[

\\boxed{

\\text{What makes the few remaining false-safe expansions}

\\atop

\\text{survive both safety-confidence and downside filtering?}

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

| Risk-model training | 53 |

| Held-out testing | 75 |



The primary regret tolerance remained



\\\[

\\epsilon\_{\\text{primary}}

=

0.0005.

\\]



The cost-aware expansion operating point was fixed at



\\\[

\\boxed{

\\tau\_p=0.60

}

\\]



and



\\\[

\\boxed{

\\tau\_d=0.020.

}

\\]



Thus the experiment analyzes the exact configuration identified as most promising in Experiment 077.



\---



\## Expansion Outcome Categories



Each held-out context was classified into one of three categories.



\### Beneficial Expansion



An expanded action is considered beneficial when it produces a more responsive action and does not increase realized regret:



\\\[

a\_t^{\\text{expanded}}

<

a\_t^{\\text{primary}}

\\]



and



\\\[

R\_t^{\\text{expanded}}

\\leq

R\_t^{\\text{primary}}.

\\]



\### Harmful Expansion



An expansion is harmful when it increases realized regret:



\\\[

R\_t^{\\text{expanded}}

>

R\_t^{\\text{primary}}.

\\]



\### Neutral Expansion



All remaining contexts are classified as neutral.



This includes contexts in which no effective action change occurs.



\---



\## Expansion Outcome Counts



The 75 held-out contexts decomposed into:



| Outcome | Contexts | Fraction |

|---|---:|---:|

| Beneficial | 16 | 21.333% |

| Neutral | 57 | 76.000% |

| Harmful | 2 | 2.667% |



Therefore only



\\\[

\\boxed{

2/75

=

2.667\\%

}

\\]



of held-out contexts remained harmful under the best cost-aware gate.



This confirms that the cost-aware architecture is already highly selective.



\---



\## Beneficial Expansions



Beneficial expansions reduced persistence by an average of



\\\[

\\boxed{

1.438

}

\\]



action levels.



Their mean incremental regret was



\\\[

\\boxed{

0.000000.

}

\\]



Maximum incremental regret was also



\\\[

0\.

\\]



Thus these expansions delivered genuine responsiveness improvement without any realized consequence penalty.



Their mean safety confidence was



\\\[

0.775.

\\]



The mean predicted downside was



\\\[

0.004266,

\\]



while mean realized downside was



\\\[

0\.

\\]



Therefore the downside model was conservative on average for beneficial expansions.



The corresponding mean downside error was



\\\[

\-0.004266.

\\]



\---



\## Beneficial Expansion Interpretation



The beneficial cases show that the expansion mechanism can recover substantial control flexibility.



A mean action reduction of



\\\[

1.438

\\]



is large relative to the available persistence range



\\\[

\\{1,2,3\\}.

\\]



These contexts therefore represent genuine responsiveness gains rather than minor parameter adjustments.



The result confirms that the broader research direction remains valid:



\\\[

\\boxed{

\\text{safe-action expansion can recover meaningful responsiveness}

\\atop

\\text{at exactly zero realized regret in many contexts}.

}

\\]



\---



\## Neutral Expansions



Neutral contexts accounted for



\\\[

57/75

=

76.000\\%.

\\]



Their mean action step was



\\\[

0\.

\\]



Their mean incremental regret was also



\\\[

0\.

\\]



The mean safety score was



\\\[

0.752.

\\]



Mean predicted downside was



\\\[

0.004431,

\\]



while mean realized downside was



\\\[

0.004142.

\\]



The mean downside error was therefore small:



\\\[

\-0.000289.

\\]



This suggests that most neutral contexts are not problematic estimation failures.



They are primarily contexts in which the expansion mechanism does not change the executed action.



\---



\## Harmful Expansions



Only two contexts were harmful.



Their average action reduction was



\\\[

1.000.

\\]



Their mean incremental regret was



\\\[

\\boxed{

0.035122

}

\\]



and their maximum incremental regret was



\\\[

\\boxed{

0.036763.

}

\\]



These are the exact two harmful expansion cases responsible for the regret increase observed in Experiment 077.



\---



\## Safety-Confidence Failure



The harmful cases did not have low safety confidence.



Their mean safety score was



\\\[

\\boxed{

0.873.

}

\\]



This is actually higher than the beneficial-expansion mean:



\\\[

0.775.

\\]



Thus the remaining harmful cases are not borderline classifier decisions.



They are high-confidence errors.



The safety model strongly believed the actions were safe when they were not.



The corresponding mean safety overconfidence was



\\\[

\\boxed{

0.873.

}

\\]



This is a critical result.



\---



\## Downside Underestimation



The harmful contexts also exhibited severe downside underestimation.



Mean predicted downside was only



\\\[

\\boxed{

0.000397.

}

\\]



However, mean realized downside was



\\\[

\\boxed{

0.035122.

}

\\]



The mean downside estimation error was therefore



\\\[

\\boxed{

0.034725.

}

\\]



Maximum downside error reached



\\\[

\\boxed{

0.035999.

}

\\]



Thus the downside model was not merely slightly optimistic.



It failed by almost two orders of magnitude relative to its own point prediction.



\---



\## Joint Model Failure



The two harmful cases exhibit simultaneous optimistic errors:



\\\[

\\boxed{

\\text{high predicted safety}

}

\\]



and



\\\[

\\boxed{

\\text{near-zero predicted downside}

}

\\]



despite substantial realized regret.



This means the remaining failures are not adequately described as threshold-calibration problems.



Both model outputs point strongly in the wrong direction.



The surviving harmful cases therefore represent



\\\[

\\boxed{

\\text{joint model-confidence failures}.

}

\\]



\---



\## Predicted Regret Margin



Another diagnostic quantity was the predicted regret margin between the expanded action and the primary predicted minimum.



Beneficial expansions had mean predicted-regret margin



\\\[

0.006236.

\\]



Harmful expansions had mean predicted-regret margin



\\\[

0.002030.

\\]



This is counterintuitive.



The beneficial expansions were, on average, farther from the primary predicted minimum in regret space.



Therefore a simple rule such as



\\\[

\\Delta \\hat R

\\leq

\\epsilon

\\]



would not necessarily distinguish beneficial from harmful expansions.



Indeed, such a rule might reject useful beneficial expansions while retaining some harmful cases.



\---



\## Why a Simple Final Regret-Margin Guard Is Incomplete



The harmful cases do not appear to be characterized by unusually large predicted regret margins.



Instead, their predicted margins are relatively small.



Therefore the remaining failure is not obviously caused by an expansion action looking poor to the regret model.



It is caused by the learned models being jointly and confidently wrong.



This suggests that another point-estimate threshold is unlikely to solve the problem robustly.



\---



\## Model Calibration Versus Model Uncertainty



The key distinction now becomes:



\\\[

\\boxed{

\\text{prediction value}

}

\\]



versus



\\\[

\\boxed{

\\text{confidence in that prediction}.

}

\\]



The current controller uses only point estimates:



\\\[

\\hat p\_{\\text{safe}}

\\]



and



\\\[

\\hat d.

\\]



But a point prediction does not reveal whether the underlying model is stable or uncertain.



Two actions may both have



\\\[

\\hat p\_{\\text{safe}}=0.87

\\]



while one is supported consistently across the ensemble and the other results from highly variable tree-level predictions.



Similarly, a predicted downside near zero may conceal substantial ensemble dispersion.



This motivates explicit uncertainty estimation.



\---



\## Ensemble-Uncertainty Interpretation



Both the safety classifier and downside regressor are random-forest ensembles.



Therefore their internal trees naturally provide a distribution of predictions.



For the safety model, define tree-level probabilities or votes



\\\[

p^{(m)}\_t(a).

\\]



Then estimate



\\\[

\\mu\_p(a)

=

\\frac{1}{M}

\\sum\_m

p^{(m)}\_t(a)

\\]



and



\\\[

\\sigma\_p(a).

\\]



Similarly, for downside:



\\\[

d^{(m)}\_t(a)

\\]



produces



\\\[

\\mu\_d(a)

\\]



and



\\\[

\\sigma\_d(a).

\\]



These quantities may reveal uncertainty hidden by the mean predictions alone.



\---



\## Confidence-Bound Expansion Principle



A conservative uncertainty-aware expansion rule could replace the point-estimate conditions



\\\[

\\hat p\_{\\text{safe}}

\\geq

\\tau\_p

\\]



and



\\\[

\\hat d

\\leq

\\tau\_d

\\]



with confidence-bound conditions.



For safety:



\\\[

\\boxed{

\\mu\_p

\-

k\\sigma\_p

\\geq

\\tau\_p.

}

\\]



For downside:



\\\[

\\boxed{

\\mu\_d

\+

k\\sigma\_d

\\leq

\\tau\_d.

}

\\]



This penalizes uncertain optimistic predictions.



An action with high mean safety but high uncertainty would become less likely to pass the safety gate.



An action with low mean downside but high dispersion would become less likely to pass the downside gate.



\---



\## Structural Interpretation



Experiments 076–078 now reveal three increasingly refined layers.



\### Experiment 076



Probability-only expansion improves recall but admits high-cost false positives.



\### Experiment 077



Downside-aware filtering removes the worst false-positive expansions and materially improves the recall–regret frontier.



\### Experiment 078



The remaining harmful cases are not ordinary threshold errors.



They are high-confidence joint model failures characterized by:



\\\[

\\text{high predicted safety}

\\]



and



\\\[

\\text{severely underestimated downside}.

\\]



Therefore the next architectural question is not merely whether the mean prediction is favorable.



It is whether that prediction is sufficiently certain.



\---



\## Principal Conclusion



Experiment 078 isolates the remaining failure mode of the best cost-aware expansion architecture.



At



\\\[

p=0.60,

\\qquad

d=0.020,

\\]



only



\\\[

\\boxed{

2/75

=

2.667\\%

}

\\]



of contexts are harmful.



The beneficial expansions reduce persistence by an average of



\\\[

1.438

\\]



levels with exactly zero incremental regret.



However, the two harmful cases exhibit severe optimistic model error.



Their mean predicted downside is



\\\[

0.000397,

\\]



while realized downside is



\\\[

0.035122.

\\]



Their mean safety score is



\\\[

0.873,

\\]



despite the actions being truly unsafe.



Therefore:



\\\[

\\boxed{

\\text{the surviving harmful expansions are joint high-confidence}

\\atop

\\text{model failures rather than simple threshold mistakes}.

}

\\]



This strongly motivates uncertainty-aware decision rules.



\---



\## Next Research Direction



Experiment 079 should quantify predictive uncertainty for both action-safety and downside estimation.



Because both models are random forests, the experiment can use tree-level predictions to estimate:



\\\[

\\mu\_p,

\\qquad

\\sigma\_p,

\\]



and



\\\[

\\mu\_d,

\\qquad

\\sigma\_d.

\\]



The analysis should compare beneficial and harmful expansion contexts using:



\- mean safety prediction,

\- safety prediction standard deviation,

\- safety lower confidence bound,

\- mean downside prediction,

\- downside prediction standard deviation,

\- downside upper confidence bound,

\- realized downside,

\- and incremental regret.



Candidate uncertainty-aware scores include



\\\[

LCB\_p

=

\\mu\_p

\-

k\\sigma\_p

\\]



and



\\\[

UCB\_d

=

\\mu\_d

\+

k\\sigma\_d.

\\]



The experiment should test whether the two harmful contexts have:



\\\[

\\boxed{

\\text{lower safety confidence bounds}

}

\\]



or



\\\[

\\boxed{

\\text{higher downside confidence bounds}

}

\\]



than the beneficial expansions.



If so, Experiment 080 can convert those bounds into an uncertainty-aware execution gate.



The central question becomes



\\\[

\\boxed{

\\text{Can ensemble uncertainty expose the high-confidence failures}

\\atop

\\text{that point estimates fail to distinguish?}

}

\\]

