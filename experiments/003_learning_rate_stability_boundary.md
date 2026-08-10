\# Experiment 003 — Learning-Rate Stability Boundary



\## Objective



Characterize the transition from rapid convergence to oscillatory and unbounded behavior as the learning rate of the normalized adaptive law is increased.



Experiment 002 showed that increasing the learning rate through:



\\\[

\\eta = 0.40

\\]



improved finite-horizon convergence.



However, that experiment did not identify an upper stability boundary.



\---



\## Adaptive Law



The normalized parameter update is:



\\\[

\\hat{a}\_{k+1}

=

\\hat{a}\_k

\+

\\eta

\\frac{

e\_k \\hat{x}\_k

}{

\\epsilon + \\hat{x}\_k^2

}

\\]



where:



\- \\(\\eta\\) is the learning rate,

\- \\(e\_k\\) is prediction error,

\- \\(\\hat{x}\_k\\) is the previous estimated state, and

\- \\(\\epsilon\\) is the normalization constant.



\---



\## Controlled Conditions



Measurement noise was eliminated:



\\\[

\\sigma = 0

\\]



The true parameter remained:



\\\[

a = 0.92

\\]



The initial estimate remained:



\\\[

\\hat{a}\_0 = 0.50

\\]



The simulation horizon remained:



\\\[

N = 60

\\]



All other model parameters were held constant.



\---



\## Experimental Procedure



An initial coarse sweep established that:



\\\[

\\eta = 2.0

\\]



remained convergent while:



\\\[

\\eta = 3.0

\\]



was strongly unbounded.



A second sweep narrowed the transition to the interval:



\\\[

2.0 \\le \\eta \\le 2.2

\\]



A final sweep evaluated the interval:



\\\[

\\eta \\in \[2.00, 2.20]

\\]



at increments of:



\\\[

0.01

\\]



\---



\## Behavioral Metrics



The experiment recorded:



\- final parameter estimate,

\- final absolute parameter error,

\- prediction RMSE,

\- maximum parameter error,

\- number of parameter-error sign changes,

\- sustained convergence step, and

\- behavioral classification.



Sustained convergence required:



\\\[

|a-\\hat{a}\_k| \\le 0.01

\\]



for the remainder of the simulation.



The experimental boundedness threshold was:



\\\[

|\\hat{a}\_k| < 2

\\]



throughout the simulation.



This boundedness threshold is an experimental classification criterion and should not be interpreted as a formal mathematical stability boundary.



\---



\## Fine-Sweep Results



| Learning Rate | Final \\(\\hat{a}\\) | Abs. Error | RMSE | Sign Changes | Convergence | Classification |

|---:|---:|---:|---:|---:|---:|---|

| 2.00 | 0.920000 | 0.000000 | 0.054222 | 0 | 1 | convergent |

| 2.01 | 0.920422 | 0.000422 | 0.054449 | 59 | 1 | convergent-oscillatory |

| 2.02 | 0.921512 | 0.001512 | 0.055993 | 59 | 1 | convergent-oscillatory |

| 2.03 | 0.924040 | 0.004040 | 0.062287 | 59 | 1 | convergent-oscillatory |

| 2.04 | 0.929542 | 0.009542 | 0.082128 | 59 | 1 | convergent-oscillatory |

| 2.05 | 0.941011 | 0.021011 | 0.130886 | 59 | — | bounded-oscillatory |

| 2.06 | 0.964173 | 0.044173 | 0.231005 | 59 | — | bounded-oscillatory |

| 2.07 | 1.009801 | 0.089801 | 0.419719 | 59 | — | bounded-oscillatory |

| 2.08 | 1.097894 | 0.177895 | 0.763262 | 59 | — | bounded-oscillatory |

| 2.09 | 1.265108 | 0.345108 | 1.378395 | 59 | — | bounded-oscillatory |

| 2.10 | 1.577877 | 0.657877 | 2.468168 | 59 | — | bounded-oscillatory |

| 2.11 | 2.155390 | 1.235390 | 4.382399 | 59 | — | unbounded |

| 2.12 | 3.209459 | 2.289459 | 7.719345 | 59 | — | unbounded |

| 2.13 | 5.113221 | 4.193221 | 13.495460 | 59 | — | unbounded |

| 2.14 | 8.518627 | 7.598627 | 23.427204 | 59 | — | unbounded |

| 2.15 | 14.556024 | 13.636024 | 40.396229 | 59 | — | unbounded |

| 2.16 | 25.170916 | 24.250916 | 69.213228 | 59 | — | unbounded |

| 2.17 | 43.688667 | 42.768667 | 117.865787 | 59 | — | unbounded |

| 2.18 | 75.755671 | 74.835672 | 199.546766 | 59 | — | unbounded |

| 2.19 | 130.898875 | 129.978875 | 335.935552 | 59 | — | unbounded |

| 2.20 | 225.095376 | 224.175376 | 562.481015 | 59 | — | unbounded |



Raw results:



`results/scalar\_learning\_rate\_boundary.csv`



\---



\## Observed Regimes



\### Regime I — Clean Convergence



At:



\\\[

\\eta = 2.00

\\]



the estimate converged rapidly without detected sign changes.



\---



\### Regime II — Convergent Oscillation



For:



\\\[

2.01 \\le \\eta \\le 2.04

\\]



the parameter error changed sign at every available transition, but its magnitude remained sufficiently small to satisfy the sustained convergence criterion.



This indicates an alternating error mode with sufficiently controlled amplitude over the tested horizon.



\---



\### Regime III — Bounded Nonconvergent Oscillation



For:



\\\[

2.05 \\le \\eta \\le 2.10

\\]



the estimate continued alternating around the true parameter but no longer remained within the specified convergence tolerance.



The oscillation amplitude increased as the learning rate increased.



\---



\### Regime IV — Experimental Unbounded Classification



Beginning at:



\\\[

\\eta = 2.11

\\]



the trajectory violated the experiment's parameter bound:



\\\[

|\\hat{a}| < 2

\\]



and was therefore classified as unbounded.



The magnitude of the parameter error increased rapidly as the learning rate increased further.



\---



\## Empirical Transition Regions



Under the current finite-horizon definitions, loss of sustained convergence occurs between:



\\\[

2.04 < \\eta \\le 2.05

\\]



The first violation of the selected boundedness criterion occurs between:



\\\[

2.10 < \\eta \\le 2.11

\\]



These are empirical classification boundaries for this experiment, not formal asymptotic stability limits.



\---



\## Key Observation



Every tested learning rate above:



\\\[

\\eta = 2.00

\\]



produced 59 parameter-error sign changes over the 60-step experiment.



This indicates a persistent alternating error mode.



As the learning rate increased, the alternating mode transitioned from small-amplitude convergence to larger bounded oscillation and finally to rapidly increasing amplitude.



This behavior suggests that the experimentally observed transition may be explainable through the error dynamics of the normalized adaptive update.



\---



\## Conclusion



The normalized adaptive law exhibits qualitatively distinct learning-rate regimes.



Increasing the learning rate initially accelerates parameter identification, but sufficiently aggressive adaptation introduces alternating parameter-error behavior.



Under the current experimental definitions:



\- clean convergence was observed at \\(\\eta=2.00\\),

\- oscillatory convergence occurred from \\(\\eta=2.01\\) through \\(\\eta=2.04\\),

\- bounded nonconvergent oscillation occurred from \\(\\eta=2.05\\) through \\(\\eta=2.10\\), and

\- the selected boundedness criterion was first violated at \\(\\eta=2.11\\).



These findings motivate analytical investigation of the parameter-error dynamics.



\---



\## Next Research Step



Derive an approximate parameter-error recursion for the normalized adaptive law and determine whether the observed transition near:



\\\[

\\eta \\approx 2

\\]



can be predicted theoretically.



The theoretical prediction can then be compared directly with the numerical experiment.



\---



\## Reproducibility



Experiment implementation:



`experiments/scalar\_learning\_rate\_boundary.py`



Shared simulation:



`simulation/adaptive\_scalar\_system.py`



Fine-sweep results:



`results/scalar\_learning\_rate\_boundary.csv`

