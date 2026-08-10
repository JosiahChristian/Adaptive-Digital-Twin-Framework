\# Experiment 014 — Robustness Regime Comparison



\## Objective



Evaluate whether the uncertainty-management architectures developed in the

adaptive digital twin framework remain effective when operating assumptions are

changed.



Previous experiments primarily evaluated estimator development under one

scalar operating configuration.



Experiment 014 shifts the research question from nominal architecture

comparison to robustness:



> Which uncertainty-management principles remain useful when the physical

> system, noise environment, or model validity changes?



\---



\## Architectures Compared



Three representative architectures were evaluated.



\### Dynamic Raw-Innovation Policy — Experiment 009



Uses innovation-derived mismatch with dynamically scheduled covariance

inflation.



\### Normalized Innovation Policy — Experiment 010



Evaluates innovation relative to predicted innovation covariance before

adjusting uncertainty.



\### Persistence-Gated Policy — Experiment 012



Extends normalized innovation by requiring persistent statistical consistency

before accelerated uncertainty decay occurs.



\---



\## Robustness Regimes



Six operating regimes were evaluated.



\### Nominal



Baseline stochastic configuration.



\### High Measurement Noise



Measurement-noise standard deviation increased from:



\\\[

0.50

\\]



to:



\\\[

1.00.

\\]



\### High Process Noise



Process-noise standard deviation increased from:



\\\[

0.05

\\]



to:



\\\[

0.20.

\\]



\### Large Initial Parameter Mismatch



The initial parameter estimate was changed from:



\\\[

\\hat{a}\_0=0.50

\\]



to:



\\\[

\\hat{a}\_0=0.20.

\\]



\### Abrupt Parameter Change



The true physical parameter changed at simulation step 50 from:



\\\[

a=0.92

\\]



to:



\\\[

a=0.80.

\\]



\### Transient Disturbance



A state disturbance of magnitude:



\\\[

3.0

\\]



was injected at simulation step 50.



\---



\## Multi-Seed Protocol



Each architecture-regime combination was evaluated across:



\\\[

50

\\]



independent random seeds.



With three architectures and six regimes, the experiment executed:



\\\[

3\\times6\\times50

=

900

\\]



simulation trials.



Reported values are aggregate statistics across these stochastic

realizations.



\---



\## Full-Run State RMSE



| Regime | Dynamic Raw | Normalized Innovation | Persistence Gated |

|---|---:|---:|---:|

| Nominal | \*\*0.370825\*\* | 0.374050 | 0.374388 |

| High measurement noise | \*\*0.601233\*\* | 0.613448 | 0.614320 |

| High process noise | \*\*0.394206\*\* | 0.396419 | 0.396714 |

| Large initial mismatch | \*\*0.412887\*\* | 0.420211 | 0.420503 |

| Abrupt parameter change | 0.416130 | \*\*0.413112\*\* | 0.413881 |

| Transient disturbance | \*\*0.442191\*\* | 0.442826 | 0.444635 |



\---



\## Late-Window State RMSE



| Regime | Dynamic Raw | Normalized Innovation | Persistence Gated |

|---|---:|---:|---:|

| Nominal | \*\*0.239827\*\* | 0.249932 | 0.249815 |

| High measurement noise | 0.481825 | \*\*0.455364\*\* | 0.455807 |

| High process noise | \*\*0.304633\*\* | 0.306732 | 0.306714 |

| Large initial mismatch | \*\*0.239747\*\* | 0.249781 | 0.249653 |

| Abrupt parameter change | 0.358219 | \*\*0.351874\*\* | 0.352915 |

| Transient disturbance | \*\*0.415813\*\* | 0.416617 | 0.419719 |



\---



\## Final Parameter Error



| Regime | Dynamic Raw | Normalized Innovation | Persistence Gated |

|---|---:|---:|---:|

| Nominal | 0.003147 | \*\*0.002974\*\* | 0.003003 |

| High measurement noise | \*\*0.005908\*\* | 0.007326 | 0.007373 |

| High process noise | 0.004455 | 0.004366 | \*\*0.004358\*\* |

| Large initial mismatch | 0.003147 | \*\*0.002974\*\* | 0.003003 |

| Abrupt parameter change | 0.008864 | \*\*0.008522\*\* | 0.008580 |

| Transient disturbance | 0.003131 | \*\*0.002961\*\* | 0.002992 |



\---



\## Nominal Robustness



Under nominal conditions, the dynamic raw-innovation architecture produced the

lowest mean full-run state RMSE:



\\\[

0.370825.

\\]



Normalized innovation and persistence gating produced:



\\\[

0.374050

\\]



and:



\\\[

0.374388,

\\]



respectively.



Thus, the additional statistical and persistence logic did not improve

nominal state-estimation RMSE across the 50-seed ensemble.



\---



\## Measurement-Noise Robustness



Increasing measurement-noise standard deviation to:



\\\[

1.00

\\]



produced the largest overall degradation among the stationary noise

conditions.



Mean full-run RMSE increased to approximately:



\\\[

0.60-0.61.

\\]



The dynamic raw-innovation estimator produced the lowest full-run RMSE:



\\\[

0.601233.

\\]



However, normalized innovation produced the best late-window RMSE:



\\\[

0.455364.

\\]



This suggests that normalization may become more useful after adaptation when

sensor noise is high.



\---



\## Process-Noise Robustness



Increasing process-noise standard deviation from:



\\\[

0.05

\\]



to:



\\\[

0.20

\\]



produced substantially less degradation than the high measurement-noise

condition.



Full-run RMSE remained approximately:



\\\[

0.394-0.397.

\\]



The dynamic raw-innovation architecture again produced the lowest state RMSE,

while persistence gating produced the smallest mean final parameter error by a

small margin.



\---



\## Initial Parameter-Mismatch Robustness



Changing the initial estimate to:



\\\[

\\hat{a}\_0=0.20

\\]



increased early and full-run state error but did not strongly affect late

parameter-identification accuracy.



Dynamic raw innovation produced the lowest state RMSE.



Normalized innovation produced the smallest mean final parameter error.



This indicates that all three architectures retained the ability to recover

from substantially increased initial parameter mismatch.



\---



\## Abrupt Parameter Change



The abrupt parameter-change regime produced a qualitatively different result.



At step 50, the true parameter changed from:



\\\[

a=0.92

\\]



to:



\\\[

a=0.80.

\\]



Normalized innovation produced the best:



\- full-run state RMSE,

\- late-window state RMSE, and

\- mean final parameter error.



Full RMSE was:



\\\[

0.413112.

\\]



Late RMSE was:



\\\[

0.351874.

\\]



Mean final parameter error was:



\\\[

0.008522.

\\]



This regime is the clearest case in which normalized innovation outperformed

the raw-innovation policy.



The result suggests that statistically normalized residual information may be

especially useful when disagreement reflects an actual change in model

dynamics rather than only stochastic noise.



\---



\## Parameter-Tracking Limitation



All architectures showed substantially greater final parameter error after

the abrupt parameter change than under nominal operation.



Nominal parameter error was approximately:



\\\[

0.003.

\\]



Following the physical parameter change, error increased to approximately:



\\\[

0.0085-0.0089.

\\]



Thus, none of the current architectures demonstrates especially strong rapid

tracking of a changing physical parameter.



This identifies an important limitation of the existing adaptation law.



\---



\## Transient Disturbance



All three estimators remained operational following the injected state

disturbance.



Dynamic raw innovation produced the lowest mean state RMSE:



\\\[

0.442191.

\\]



Differences between the architectures were comparatively small.



This suggests that all three uncertainty-management mechanisms provide some

ability to recover from transient state disturbances within the tested

configuration.



\---



\## Architectural Interpretation



Experiment 014 does not support a universal ranking in which increasing

uncertainty-policy complexity consistently improves estimator robustness.



Instead, architectural strengths depend on the type of disturbance.



Dynamic raw innovation performs particularly well under:



\- nominal stochastic operation,

\- high process noise,

\- large initial parameter mismatch, and

\- transient state disturbance.



Normalized innovation becomes comparatively stronger under:



\- high late-stage measurement noise, and

\- abrupt changes in physical model parameters.



Persistence gating remains competitive but does not establish a systematic

performance advantage across the tested regimes.



\---



\## Key Finding



The robustness results indicate:



\\\[

\\boxed{

\\text{the best uncertainty policy depends on the source of mismatch}

}

\\]



Residuals caused primarily by stochastic noise do not necessarily require the

same response as residuals caused by genuine changes in the underlying system

dynamics.



This suggests that future adaptive digital twins may benefit from

\*\*mismatch classification\*\* rather than applying one uncertainty-management

policy to every type of prediction disagreement.



\---



\## Limitations



The experiment remains based on a scalar linear system.



Only six robustness regimes were tested.



The architecture parameters themselves were not retuned for individual

operating regimes.



The abrupt parameter change consisted of one deterministic change:



\\\[

0.92\\rightarrow0.80.

\\]



The transient disturbance consisted of one fixed state perturbation.



Therefore, the results establish comparative evidence within the tested

regimes rather than general robustness guarantees.



\---



\## Conclusion



Experiment 014 demonstrates that the uncertainty architectures degrade

differently as operating assumptions are violated.



Dynamic raw-innovation management provides the strongest overall

state-estimation performance across most tested regimes.



Normalized innovation provides a measurable advantage when the physical

parameter changes abruptly and during late-stage operation under high

measurement noise.



Persistence gating remains effective but does not exhibit a consistent

advantage over the simpler normalized-innovation architecture.



Most importantly, the abrupt-parameter experiment reveals that the current

adaptive law remains limited in its ability to rapidly track evolving physical

dynamics.



\---



\## Next Research Direction



The next research phase should focus less on additional covariance-management

variants and more on \*\*change detection and parameter tracking\*\*.



A useful next question is:



> Can the digital twin distinguish stochastic residual variation from a

> genuine change in physical-system dynamics and temporarily increase its

> parameter-adaptation rate when such a change is detected?



This would introduce a new capability:



\\\[

\\text{model-change detection}

\\rightarrow

\\text{adaptive learning-rate response}

\\rightarrow

\\text{rapid re-synchronization}.

\\]



\---



\## Reproducibility



Experiment:



`experiments/robustness\_regime\_comparison.py`



Results:



`results/robustness\_regime\_comparison.csv`

