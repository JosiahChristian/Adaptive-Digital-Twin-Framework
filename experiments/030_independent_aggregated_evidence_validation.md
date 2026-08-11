\# Experiment 030 — Independent Aggregated Evidence Validation



\## Objective



Evaluate the frozen cause-conditioned aggregate evidence rules developed in

Experiment 029 using previously unseen operating points and stochastic

realizations.



No trajectory-level evidence rules or aggregate thresholds are modified after

observing validation results.



\---



\## Frozen Aggregate Rules



At batch size



\\\[

n=50,

\\]



the frozen Experiment 029 rules are



\\\[

\\hat e\_M=1

\\iff

\\hat p\_{50}\\ge0.44,

\\]



\\\[

\\hat e\_P=1

\\iff

\\hat p\_{50}\\ge0.59,

\\]



\\\[

\\hat e\_{\\Theta}=1

\\iff

\\hat p\_{50}\\ge0.50,

\\]



and



\\\[

\\hat e\_S=1

\\iff

\\hat p\_{50}\\ge0.51.

\\]



\---



\## Validation Population



Eight new physical operating points were evaluated using a previously unused

seed range.



Each condition contained



\\\[

100

\\]



new stochastic trajectories.



For each operating condition, 500 without-replacement batches of size



\\\[

n=50

\\]



were sampled.



The validation experiment therefore produced



\\\[

8\\times500=4000

\\]



aggregate decisions.



\---



\## Overall Result



The frozen aggregate architecture produced



\\\[

2954/4000

\\]



correct evidence decisions.



Therefore,



\\\[

\\boxed{

A\_{\\mathrm{aggregate}}=73.850\\%.

}

\\]



\---



\## Cause-Level Results



| Cause | Aggregate evidence accuracy |

|---|---:|

| Measurement noise | 97.1% |

| Process disturbance | 48.2% |

| Parameter mismatch | 50.1% |

| Structural change | 100.0% |



Thus independent generalization is highly mechanism dependent.



Measurement-noise and structural-change aggregate evidence models generalized

strongly, whereas process-disturbance and parameter-mismatch models did not.



\---



\## Condition-Level Results



| Condition | Evidence label | Hard | Coverage | Selective | Mean aggregate vote | Threshold | Aggregate accuracy |

|---|---:|---:|---:|---:|---:|---:|---:|

| measurement noise 0.875 | False | 96% | 73% | 100% | 0.3595 | 0.44 | 94.2% |

| measurement noise 0.975 | True | 99% | 86% | 100% | 0.6306 | 0.44 | 100% |

| process disturbance 2.60 | True | 90% | 86% | 96.512% | 0.5164 | 0.59 | 7.6% |

| process disturbance 2.90 | True | 96% | 90% | 97.778% | 0.6439 | 0.59 | 88.8% |

| parameter mismatch 0.435 | False | 80% | 54% | 100% | 0.3399 | 0.50 | 100% |

| parameter mismatch 0.395 | False | 93% | 76% | 100% | 0.6304 | 0.50 | 0.2% |

| structural change 0.875 | False | 80% | 69% | 88.406% | 0.1496 | 0.51 | 100% |

| structural change 0.855 | True | 94% | 82% | 97.561% | 1.0000 | 0.51 | 100% |



\---



\## Successful Generalization



Measurement noise exhibits clear separation.



The insufficient condition has



\\\[

E\[\\hat p\_{50}]

=

0.3595,

\\]



while the sufficient condition has



\\\[

E\[\\hat p\_{50}]

=

0.6306.

\\]



The frozen threshold



\\\[

0.44

\\]



therefore generalizes effectively.



Structural change exhibits even stronger separation:



\\\[

0.1496

\\]



for the insufficient operating point and



\\\[

1.0000

\\]



for the sufficient operating point.



Both mechanisms therefore provide evidence that cause-conditioned aggregation

can generalize beyond its development boundary pair.



\---



\## Boundary Instability



The process-disturbance and parameter-mismatch results expose a different

problem.



Evidence sufficiency is currently assigned through the hard criterion



\\\[

e(c)

=

\\mathbf1\[

A(c)\\ge0.90

\\land

C(c)\\ge0.80

\\land

A\_{\\mathrm{sel}}(c)\\ge0.95

].

\\]



Each of these quantities is estimated from a finite stochastic population.



Near a threshold, small sampling fluctuations can therefore change the binary

evidence label.



For example, process disturbance magnitude 2.60 satisfies the criterion with



\\\[

A=90\\%,

\\qquad

C=86\\%,

\\qquad

A\_{\\mathrm{sel}}=96.512\\%.

\\]



Yet a previously evaluated disturbance of magnitude 2.65 failed the criterion

primarily because its observed coverage was only 78%.



This non-monotonic empirical labeling is more plausibly explained by finite

sampling uncertainty near the boundary than by a true reversal of physical

detectability.



\---



\## Parameter-Mismatch Counterexample



The parameter-mismatch condition with initial estimate 0.395 is labeled

evidence-insufficient because



\\\[

C=76\\%<80\\%.

\\]



However,



\\\[

A=93\\%

\\]



and



\\\[

A\_{\\mathrm{sel}}=100\\%.

\\]



Its aggregated evidence statistic is



\\\[

E\[\\hat p\_{50}]

=

0.6304,

\\]



which lies well above the frozen threshold



\\\[

0.50.

\\]



By contrast, the more weakly identifiable parameter-mismatch condition at

0.435 has



\\\[

E\[\\hat p\_{50}]

=

0.3399.

\\]



Thus the aggregate statistic distinguishes these regimes strongly even though

the current hard evidence criterion assigns both the same label.



\---



\## Interpretation



Experiment 030 suggests that aggregation is no longer the only limiting

factor.



For some mechanisms, the aggregated evidence statistic varies smoothly while

the binary evidence target changes discontinuously at arbitrary empirical

performance thresholds.



The estimator may therefore be becoming more informative than the discrete

target used to evaluate it.



The current definition



\\\[

e\\in\\{0,1\\}

\\]



does not represent uncertainty in the estimated operating-point performance

statistics.



\---



\## Revised Statistical Problem



Evidence sufficiency should account for uncertainty in



\\\[

\\widehat A,

\\qquad

\\widehat C,

\\qquad

\\widehat A\_{\\mathrm{sel}}.

\\]



A more appropriate representation may be



\\\[

\\boxed{

P(

e=1

\\mid

\\widehat A,

\\widehat C,

\\widehat A\_{\\mathrm{sel}},

N

).

}

\\]



Alternatively, evidence sufficiency may be represented by a continuous score

rather than a hard Boolean state.



This would prevent an arbitrarily small change around a performance threshold

from producing a discontinuous change in the ground-truth evidence label.



\---



\## Conclusion



Independent validation of cause-conditioned aggregated evidence achieved



\\\[

73.850\\%

\\]



overall accuracy.



Measurement-noise and structural-change estimators generalized extremely well,

with 97.1% and 100% accuracy respectively.



Process-disturbance and parameter-mismatch results reveal substantial

sensitivity to the binary evidence-label definition near empirical

detectability boundaries.



Experiment 030 therefore supports two conclusions:



\\\[

\\boxed{

\\text{cause-conditioned aggregation contains generalizable information}

}

\\]



and



\\\[

\\boxed{

\\text{evidence sufficiency itself must be uncertainty-aware}.

}

\\]



\---



\## Next Research Direction



The next experiment should quantify uncertainty in the operating-point

evidence criterion.



Rather than asking only whether



\\\[

\\widehat A\\ge0.90,

\\quad

\\widehat C\\ge0.80,

\\quad

\\widehat A\_{\\mathrm{sel}}\\ge0.95,

\\]



the digital twin should estimate the probability that the underlying

population quantities satisfy those requirements.



This motivates an uncertainty-aware evidence-sufficiency formulation.

