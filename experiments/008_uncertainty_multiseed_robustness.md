\# Experiment 008 — Multi-Seed Uncertainty Robustness



\## Objective



Determine whether the performance improvements produced by innovation-driven

model-uncertainty handling persist across independent stochastic realizations.



Experiments 006 and 007 demonstrated substantial improvements under a fixed

random seed. Experiment 008 extends that analysis to 50 random seeds for six

representative uncertainty configurations.



\---



\## Experimental Design



Each configuration was evaluated over:



\\\[

N\_{\\mathrm{seeds}}=50

\\]



independent stochastic realizations.



With six configurations, the experiment therefore executed:



\\\[

6\\times50=300

\\]



simulation runs.



All physical-system parameters, estimator parameters other than the

uncertainty hyperparameters, and simulation horizons were held constant.



\---



\## Configurations



\### No-Inflation Control



\\\[

\\beta=0.50,\\qquad\\lambda=0.

\\]



\### Original Experiment 006



\\\[

\\beta=0.90,\\qquad\\lambda=0.05.

\\]



\### Moderate Inflation



\\\[

\\beta=0.50,\\qquad\\lambda=0.10.

\\]



\### Strong State-Synchronization Candidate



\\\[

\\beta=0.50,\\qquad\\lambda=0.20.

\\]



\### High-Memory Strong Inflation



\\\[

\\beta=0.90,\\qquad\\lambda=0.20.

\\]



\### Parameter-Focused Candidate



\\\[

\\beta=0.99,\\qquad\\lambda=0.20.

\\]



\---



\## Aggregate Results



| Configuration | Mean Full RMSE | Std Full RMSE | Mean Early RMSE | Mean Late RMSE | Mean Parameter Error |

|---|---:|---:|---:|---:|---:|

| No inflation | 0.964093 | 0.119154 | 1.776934 | 0.301295 | 0.005725 |

| Original Exp. 006 | 0.478688 | 0.046517 | 0.867455 | 0.230835 | 0.003863 |

| Moderate inflation | 0.392356 | 0.040852 | 0.667221 | 0.233261 | 0.003344 |

| Strong state candidate | 0.367847 | 0.037524 | 0.582815 | 0.250629 | 0.003008 |

| High-memory strong inflation | 0.406665 | 0.039689 | 0.669883 | 0.257318 | 0.003209 |

| Parameter-focused | 0.545483 | 0.048809 | 0.994270 | 0.259035 | 0.003242 |



\---



\## Full-Run Synchronization



The no-inflation control produced mean full-run state RMSE:



\\\[

0.964093.

\\]



The strong state-synchronization candidate produced:



\\\[

0.367847.

\\]



The relative reduction was approximately:



\\\[

61.8\\%.

\\]



Thus, the substantial single-seed improvement observed in Experiment 007

persisted across 50 stochastic realizations.



\---



\## Early Synchronization



The largest improvement occurred during initial model synchronization.



No-inflation mean early RMSE:



\\\[

1.776934.

\\]



Strong state-candidate mean early RMSE:



\\\[

0.582815.

\\]



This corresponds to an approximate reduction of:



\\\[

67.2\\%.

\\]



The result provides strong empirical evidence that innovation-driven

covariance inflation mitigates the severe transient caused by initial model

parameter error.



\---



\## Variability



The standard deviation of full-run RMSE for the control was:



\\\[

0.119154.

\\]



For the strong state candidate:



\\\[

0.037524.

\\]



Therefore, the uncertainty-aware configuration was not only more accurate on

average but also substantially less variable across stochastic realizations.



This indicates improved robustness to different process- and measurement-noise

sequences within the tested stochastic model.



\---



\## Late-Run Tradeoff



The configuration producing the best early and full-run synchronization did

not produce the lowest late-run RMSE.



The original Experiment 006 configuration:



\\\[

(\\beta,\\lambda)=(0.90,0.05)

\\]



produced the lowest mean late RMSE:



\\\[

0.230835.

\\]



The strong state candidate:



\\\[

(\\beta,\\lambda)=(0.50,0.20)

\\]



produced:



\\\[

0.250629.

\\]



This reveals a tradeoff between aggressive uncertainty response during model

mismatch and late-run filtering behavior after synchronization has largely

occurred.



\---



\## Parameter Identification



The no-inflation control produced mean final parameter absolute error:



\\\[

0.005725.

\\]



The strong state candidate produced:



\\\[

0.003008.

\\]



Thus, improved state synchronization was accompanied by improved average

parameter identification.



The uncertainty mechanism therefore affected both components of the coupled

state/parameter estimation process.



\---



\## Interpretation



Across 50 independent stochastic realizations, innovation-driven process

covariance inflation consistently improved synchronization relative to the

no-inflation estimator.



The results support the following mechanism:



```text

Initial model mismatch

&#x20;       ↓

Persistent prediction innovation

&#x20;       ↓

Innovation-energy mismatch signal

&#x20;       ↓

Adaptive process-covariance inflation

&#x20;       ↓

Reduced estimator overconfidence

&#x20;       ↓

Greater corrective influence from observations

&#x20;       ↓

Improved state synchronization

&#x20;       ↓

Improved adaptive parameter estimation

