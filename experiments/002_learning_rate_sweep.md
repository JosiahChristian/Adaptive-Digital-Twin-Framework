\# Experiment 002 — Learning-Rate Sensitivity



\## Objective



Investigate how the learning rate of the normalized adaptive law affects parameter-identification accuracy, prediction error, convergence speed, and boundedness.



The preceding measurement-noise experiments showed that a residual parameter-estimation error remained even when measurement noise was zero.



This experiment isolates the learning rate as a possible contributor.



\---



\## Research Question



How does the learning rate \\(\\eta\\) affect convergence of the normalized scalar adaptive digital twin over a fixed 60-step simulation horizon?



\---



\## Controlled Conditions



Measurement noise was eliminated:



\\\[

\\sigma = 0

\\]



The true system parameter remained:



\\\[

a = 0.92

\\]



The initial twin parameter remained:



\\\[

\\hat{a}\_0 = 0.50

\\]



The simulation horizon remained:



\\\[

N = 60

\\]



All other model parameters were held at their established baseline values.



\---



\## Learning Rates



The following learning rates were evaluated:



\\\[

\\eta \\in

\\{

0.01,\\,

0.02,\\,

0.04,\\,

0.08,\\,

0.12,\\,

0.20,\\,

0.40

\\}

\\]



\---



\## Convergence Criterion



Sustained convergence was defined as the first simulation step at which:



\\\[

|a-\\hat{a}\_k| \\le 0.01

\\]



and the estimate remained within that tolerance for every subsequent step.



This criterion distinguishes sustained convergence from temporarily entering the target region.



\---



\## Results



| Learning Rate | Final \\(\\hat{a}\\) | Absolute Error | Prediction RMSE | Sustained Convergence Step |

|---:|---:|---:|---:|---:|

| 0.01 | 0.684334 | 0.235666 | 3.161234 | Not reached |

| 0.02 | 0.788523 | 0.131477 | 2.373997 | Not reached |

| 0.04 | 0.879796 | 0.040204 | 1.494321 | Not reached |

| 0.08 | 0.916510 | 0.003490 | 0.807599 | 47 |

| 0.12 | 0.919728 | 0.000272 | 0.541886 | 31 |

| 0.20 | 0.919999 | \\(1.16 \\times 10^{-6}\\) | 0.322498 | 19 |

| 0.40 | 0.920000 | \\(8.74 \\times 10^{-14}\\) | 0.162710 | 9 |



All tested configurations remained bounded according to the experiment's boundedness criterion.



Raw results:



`results/scalar\_learning\_rate\_sweep.csv`



\---



\## Observations



\### Low Learning Rates



Learning rates between:



\\\[

0.01 \\le \\eta \\le 0.04

\\]



did not reach the specified convergence tolerance within the 60-step simulation horizon.



These configurations remained bounded but adapted slowly.



\---



\### Intermediate Learning Rates



At:



\\\[

\\eta = 0.08

\\]



sustained convergence occurred at step 47.



Increasing the learning rate to:



\\\[

\\eta = 0.12

\\]



reduced the sustained convergence step to 31 while also decreasing final parameter error and prediction RMSE.



\---



\### Higher Tested Learning Rates



At:



\\\[

\\eta = 0.20

\\]



sustained convergence occurred at step 19.



At:



\\\[

\\eta = 0.40

\\]



sustained convergence occurred at step 9.



The \\(\\eta=0.40\\) condition produced the lowest parameter error and prediction RMSE among the learning rates evaluated in this experiment.



\---



\## Interpretation



Within the tested range, increasing the learning rate accelerated parameter identification.



The low-rate configurations did not necessarily demonstrate failure of the adaptive law. Instead, the finite 60-step horizon was insufficient for those configurations to approach the true parameter closely.



The residual zero-noise error previously observed at:



\\\[

\\eta = 0.08

\\]



therefore appears to be substantially influenced by finite-horizon convergence behavior.



\---



\## Important Limitation



The results do \*\*not\*\* establish:



\\\[

\\eta = 0.40

\\]



as an optimal learning rate.



No instability boundary was identified because every tested learning rate remained bounded.



Higher learning rates may eventually introduce overshoot, oscillation, or divergence.



Therefore, the present result establishes only that increasing \\(\\eta\\) through the tested range improved finite-horizon convergence for this scalar configuration.



\---



\## Next Research Question



Where is the transition between rapid normalized adaptation and unstable or undesirable adaptive behavior?



A subsequent experiment should extend the learning-rate range beyond:



\\\[

\\eta = 0.40

\\]



and characterize:



\- convergence speed,

\- overshoot,

\- oscillatory behavior,

\- parameter error,

\- prediction RMSE, and

\- boundedness.



\---



\## Reproducibility



Experiment implementation:



`experiments/scalar\_learning\_rate\_sweep.py`



Shared simulation implementation:



`simulation/adaptive\_scalar\_system.py`



Results:



`results/scalar\_learning\_rate\_sweep.csv`

