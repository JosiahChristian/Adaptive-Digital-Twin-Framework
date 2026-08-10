\# Experiment 011 — Consistency-Gated Uncertainty Decay



\## Objective



Determine whether accelerated model-uncertainty decay can reduce residual

covariance inflation after the adaptive digital twin reaches a statistically

consistent operating regime.



Experiment 010 used normalized innovation squared (NIS) as the mismatch

signal but retained a nontrivial mismatch indicator and covariance inflation

late in the trajectory.



Experiment 011 introduces an explicit consistency gate that accelerates

mismatch decay when normalized innovation indicates statistically ordinary

residual behavior.



\---



\## Consistency Criterion



Normalized innovation squared is:



\\\[

\\epsilon\_k

=

\\frac{r\_k^2}{S\_k}.

\\]



The consistency gate activates when:



\\\[

\\epsilon\_k \\le \\tau.

\\]



The experiment used:



\\\[

\\tau=1.0.

\\]



When the gate is active, the mismatch indicator receives accelerated decay:



\\\[

U\_k

\\leftarrow

\\rho U\_k

\\]



with:



\\\[

\\rho=0.70.

\\]



The underlying exponentially weighted mismatch update remains:



\\\[

U\_k

=

\\beta U\_{k-1}

\+

(1-\\beta)m\_k

\\]



where:



\\\[

m\_k

=

\\max(0,\\epsilon\_k-1).

\\]



\---



\## Configuration



The estimator retained the Experiment 010 settings:



\\\[

\\beta=0.50

\\]



\\\[

\\lambda\_{\\min}=0.05

\\]



\\\[

\\lambda\_{\\max}=0.20

\\]



\\\[

c=0.25.

\\]



Additional consistency parameters were:



\\\[

\\tau=1.0

\\]



and:



\\\[

\\rho=0.70.

\\]



The physical system, noise levels, learning rate, initial conditions,

simulation horizon, and random seed were unchanged.



\---



\## Gate Activity



The consistency gate activated:



\\\[

61

\\]



times over the 100-step trajectory.



Thus, the gate was active during:



\\\[

61\\%

\\]



of simulation steps.



The gate therefore had a substantial influence on the estimator rather than

representing a rarely triggered edge condition.



\---



\## Results



Measurement RMSE:



\\\[

0.458451.

\\]



Full state-estimation RMSE:



\\\[

0.383603.

\\]



Early-window RMSE:



\\\[

\\mathrm{RMSE}\_{0:24}

=

0.646691.

\\]



Intermediate-window RMSE:



\\\[

\\mathrm{RMSE}\_{25:49}

=

0.149550.

\\]



Late-window RMSE:



\\\[

\\mathrm{RMSE}\_{50:99}

=

0.272058.

\\]



Mean NIS over the complete trajectory:



\\\[

1.309454.

\\]



Mean NIS over steps 50–99:



\\\[

0.790297.

\\]



Final parameter estimate:



\\\[

\\hat{a}\_{99}

=

0.922742.

\\]



Final parameter absolute error:



\\\[

0.002742.

\\]



\---



\## Uncertainty Reduction



Experiment 010 ended with mismatch indicator:



\\\[

U\_{99}

=

0.173498.

\\]



Experiment 011 reduced this to:



\\\[

U\_{99}

=

0.064330.

\\]



This represents a reduction of approximately:



\\\[

62.9\\%.

\\]



Final dynamic inflation strength decreased from:



\\\[

0.111452

\\]



to:



\\\[

0.080699.

\\]



Final effective process-noise variance decreased from:



\\\[

0.021837

\\]



to:



\\\[

0.007691.

\\]



Thus, the consistency gate successfully reduced residual uncertainty inflation.



\---



\## Comparison with Experiment 010



| Metric | Experiment 010 | Experiment 011 |

|---|---:|---:|

| Full state RMSE | 0.372992 | 0.383603 |

| Early RMSE | 0.621916 | 0.646691 |

| Intermediate RMSE | 0.161099 | 0.149550 |

| Late RMSE | 0.268105 | 0.272058 |

| Final parameter error | 0.002372 | 0.002742 |

| Final mismatch indicator | 0.173498 | 0.064330 |

| Final dynamic inflation | 0.111452 | 0.080699 |

| Final effective Q | 0.021837 | 0.007691 |



Experiment 011 improved intermediate-window state estimation while reducing

stored uncertainty substantially.



However, full-run, early, and late state RMSE were slightly worse than

Experiment 010.



Final parameter-identification accuracy also decreased.



\---



\## Interpretation



The experiment demonstrates that reducing uncertainty inflation does not

automatically improve physical state estimation.



Although NIS-based consistency indicates that observed residuals are

statistically compatible with predicted uncertainty, aggressive decay of the

mismatch indicator can remove useful robustness.



The result suggests:



\\\[

\\text{statistical consistency}

\\neq

\\text{minimum estimation error}.

\\]



Some retained model uncertainty can remain beneficial even after the filter

enters an apparently consistent regime.



\---



\## Middle-Window Improvement



Experiment 011 reduced intermediate-window RMSE from:



\\\[

0.161099

\\]



to:



\\\[

0.149550.

\\]



This indicates that the gating mechanism is not intrinsically detrimental.



Instead, the effectiveness of uncertainty decay appears to depend on when and

how strongly it is applied.



The current gate likely removes uncertainty too aggressively during portions

of the trajectory where residual model uncertainty remains useful.



\---



\## Conclusion



Consistency-gated uncertainty decay successfully reduced stale mismatch memory

and covariance inflation.



However, the selected gate parameters did not improve overall state-estimation

performance relative to Experiment 010.



The experiment therefore identifies a tradeoff between:



\- estimator conservatism,

\- statistical consistency,

\- state-estimation accuracy, and

\- parameter-identification accuracy.



The result motivates a more selective uncertainty-decay policy rather than

uniform accelerated decay whenever:



\\\[

\\epsilon\_k\\le1.

\\]



\---



\## Next Research Question



Can uncertainty decay require \*\*persistent consistency\*\* rather than a single

consistent observation?



A persistence-based gate could activate only after several consecutive or

predominantly consistent NIS observations.



This may preserve model-uncertainty protection during transient stochastic

fluctuations while still allowing covariance inflation to relax after genuine

synchronization.



\---



\## Reproducibility



Estimator:



`simulation/consistency\_gated\_estimator.py`



Experiment:



`experiments/consistency\_gated\_uncertainty.py`



Results:



`results/consistency\_gated\_uncertainty.csv`



Tests:



`tests/test\_consistency\_gated\_estimator.py`

