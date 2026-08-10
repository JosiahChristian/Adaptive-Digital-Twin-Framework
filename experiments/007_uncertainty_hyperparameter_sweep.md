\# Experiment 007 — Uncertainty Hyperparameter Sweep



\## Objective



Evaluate whether the performance improvement observed in Experiment 006 is

robust across a region of uncertainty-model hyperparameters rather than

dependent on a single selected configuration.



The uncertainty-aware estimator uses two primary parameters:



\\\[

\\beta

\\]



which controls the memory of the exponentially weighted innovation-energy

indicator, and:



\\\[

\\lambda

\\]



which controls the strength of process-covariance inflation.



\---



\## Uncertainty Model



The mismatch indicator is:



\\\[

U\_k

=

\\beta U\_{k-1}

\+

(1-\\beta)r\_k^2

\\]



where:



\\\[

r\_k

=

y\_k-\\hat{x}\_k^-.

\\]



The effective process-noise variance is:



\\\[

Q\_{\\mathrm{effective},k}

=

Q\_{\\mathrm{base}}

\+

\\lambda U\_k.

\\]



Thus:



\- larger \\(\\beta\\) produces longer mismatch memory,

\- smaller \\(\\beta\\) produces faster response to new innovation information,

\- larger \\(\\lambda\\) produces stronger covariance inflation, and

\- \\(\\lambda=0\\) removes the uncertainty-feedback mechanism entirely.



\---



\## Experimental Grid



The following innovation-memory values were tested:



\\\[

\\beta

\\in

\\{

0.50,\\,

0.70,\\,

0.90,\\,

0.95,\\,

0.99

\\}.

\\]



The following covariance-inflation strengths were tested:



\\\[

\\lambda

\\in

\\{

0,\\,

0.01,\\,

0.025,\\,

0.05,\\,

0.10,\\,

0.20

\\}.

\\]



This produced:



\\\[

5\\times6=30

\\]



hyperparameter configurations.



The physical-system parameters, stochastic configuration, simulation horizon,

and random seed were held constant to isolate the effect of the uncertainty

hyperparameters.



\---



\## Control Condition



The:



\\\[

\\lambda=0

\\]



configurations serve as a no-inflation control.



For every tested value of \\(\\beta\\), the no-inflation condition reproduced the

same baseline integrated-estimator results:



\\\[

\\mathrm{RMSE}\_{full}

=

0.882416

\\]



\\\[

\\mathrm{RMSE}\_{0:24}

=

1.640203

\\]



\\\[

\\mathrm{RMSE}\_{50:99}

=

0.372701

\\]



and final parameter error:



\\\[

|a-\\hat{a}|

=

0.007893.

\\]



This is expected because \\(\\beta\\) affects only the mismatch indicator. When:



\\\[

\\lambda=0,

\\]



the mismatch indicator no longer affects the effective process covariance.



The identical control behavior provides an experimental consistency check.



\---



\## Broad Performance Pattern



Across most tested values of \\(\\beta\\), increasing:



\\\[

\\lambda

\\]



reduced the severe early state-estimation transient observed in the original

integrated estimator.



This indicates that the benefit observed in Experiment 006 was not isolated

to the original:



\\\[

(\\beta,\\lambda)

=

(0.90,0.05)

\\]



configuration.



Instead, the results show a broader region in which innovation-driven

covariance inflation improves adaptive synchronization.



\---



\## Original Experiment 006 Configuration



Experiment 006 used:



\\\[

\\beta=0.90

\\]



and:



\\\[

\\lambda=0.05.

\\]



The resulting metrics were:



\\\[

\\mathrm{RMSE}\_{full}

=

0.493092

\\]



\\\[

\\mathrm{RMSE}\_{0:24}

=

0.877279

\\]



\\\[

\\mathrm{RMSE}\_{25:49}

=

0.183725

\\]



\\\[

\\mathrm{RMSE}\_{50:99}

=

0.290847

\\]



with final parameter error:



\\\[

0.003882.

\\]



These results already represented a substantial improvement over the

no-inflation control.



\---



\## Strongest Full-Run State-Estimation Configuration



Within the tested grid, the lowest full-run state RMSE occurred at:



\\\[

\\boxed{

\\beta=0.50,\\quad

\\lambda=0.20

}

\\]



with:



\\\[

\\mathrm{RMSE}\_{full}

=

0.372677.

\\]



The corresponding early-window RMSE was:



\\\[

\\mathrm{RMSE}\_{0:24}

=

0.619639.

\\]



Intermediate-window RMSE:



\\\[

\\mathrm{RMSE}\_{25:49}

=

0.171012.

\\]



Late-window RMSE:



\\\[

\\mathrm{RMSE}\_{50:99}

=

0.266791.

\\]



Final parameter error was:



\\\[

|a-\\hat{a}|

=

0.001554.

\\]



Compared with the no-inflation baseline, this configuration substantially

improved both state synchronization and parameter identification.



\---



\## Effect of Covariance-Inflation Strength



For the lower-memory configurations:



\\\[

\\beta=0.50

\\]



and:



\\\[

\\beta=0.70,

\\]



increasing \\(\\lambda\\) through the tested range generally reduced early state

RMSE and final parameter error.



For example, at:



\\\[

\\beta=0.50,

\\]



the early state RMSE changed from:



\\\[

1.640203

\\]



with:



\\\[

\\lambda=0

\\]



to:



\\\[

0.619639

\\]



with:



\\\[

\\lambda=0.20.

\\]



This supports the hypothesis that stronger uncertainty inflation can prevent

premature confidence during severe initial model mismatch.



\---



\## Effect of Innovation Memory



Lower-memory configurations generally produced stronger early synchronization

than very high-memory configurations.



For example:



\\\[

\\beta=0.50

\\]



responds relatively quickly to changes in innovation energy.



By contrast:



\\\[

\\beta=0.99

\\]



retains substantial historical influence in the mismatch indicator.



The high-memory configurations reduced error relative to the no-inflation

baseline but generally retained larger early transients.



This suggests that excessive mismatch memory can delay the estimator's

response to abrupt model error.



\---



\## State-Estimation vs. Parameter-Identification Tradeoff



The hyperparameter pair that produced the lowest state-estimation error was

not identical to the pair that produced the lowest final parameter error.



The lowest final parameter error in the tested grid occurred at approximately:



\\\[

\\beta=0.99,\\quad

\\lambda=0.20

\\]



with:



\\\[

|a-\\hat{a}|

\\approx

5.83\\times10^{-4}.

\\]



However, that configuration produced substantially worse state-estimation

performance than:



\\\[

\\beta=0.50,\\quad

\\lambda=0.20.

\\]



This demonstrates that:



\\\[

\\text{state-estimation accuracy}

\\]



and:



\\\[

\\text{parameter-identification accuracy}

\\]



are related but distinct optimization objectives.



A hyperparameter setting cannot be described as universally optimal without

first defining the performance objective.



\---



\## Candidate Configurations for Robustness Testing



The following configurations capture distinct behaviors from the sweep:



\### No-Inflation Control



\\\[

\\beta=0.50,\\quad

\\lambda=0.

\\]



\### Original Experiment 006



\\\[

\\beta=0.90,\\quad

\\lambda=0.05.

\\]



\### Moderate Inflation Candidate



\\\[

\\beta=0.50,\\quad

\\lambda=0.10.

\\]



\### Strong State-Synchronization Candidate



\\\[

\\beta=0.50,\\quad

\\lambda=0.20.

\\]



\### Higher-Memory Strong-Inflation Candidate



\\\[

\\beta=0.90,\\quad

\\lambda=0.20.

\\]



\### Parameter-Focused Candidate



\\\[

\\beta=0.99,\\quad

\\lambda=0.20.

\\]



These configurations will be evaluated across multiple stochastic

realizations in the next experiment.



\---



\## Interpretation



Experiment 007 provides evidence that innovation-driven covariance inflation

has a broad performance region rather than a single favorable parameter point.



The mechanism appears to improve synchronization because:



```text

Model mismatch

&#x20;     ↓

Innovation energy

&#x20;     ↓

Mismatch indicator

&#x20;     ↓

Effective process covariance

&#x20;     ↓

Reduced premature confidence

&#x20;     ↓

Greater measurement correction

&#x20;     ↓

Improved state synchronization

