\# Experiment 006 — Model-Uncertainty-Aware State Estimation



\## Objective



Evaluate whether innovation-driven process-covariance inflation can improve

state estimation when an adaptive digital twin begins with a substantially

incorrect process model.



Experiment 005 demonstrated that the coupled state/parameter estimator could

learn the unknown system parameter, but the Kalman filter became highly

confident before the model itself became accurate.



Experiment 006 tests the hypothesis that explicitly increasing process

uncertainty during persistent prediction mismatch can reduce this premature

confidence and improve digital-twin synchronization.



\---



\## Baseline Problem



The true scalar system parameter is:



\\\[

a = 0.92.

\\]



The digital twin begins with:



\\\[

\\hat{a}\_0 = 0.50.

\\]



Experiment 005 produced an early state-estimation RMSE of:



\\\[

\\mathrm{RMSE}\_{0:24}=1.640203.

\\]



Despite substantial model mismatch, the state covariance rapidly decreased.



This demonstrated that Kalman covariance represents uncertainty relative to

the assumed model and does not automatically represent uncertainty in the

validity of the model itself.



\---



\## Hypothesis



Persistent prediction disagreement can provide an observable indicator of

model mismatch.



The Kalman innovation is:



\\\[

r\_k = y\_k-\\hat{x}\_k^-.

\\]



An exponentially weighted innovation-energy indicator is defined as:



\\\[

U\_k =

\\beta U\_{k-1}

\+

(1-\\beta)r\_k^2.

\\]



The effective process-noise variance becomes:



\\\[

Q\_{\\mathrm{effective},k}

=

Q\_{\\mathrm{base}}

\+

\\lambda U\_k.

\\]



The experiment uses:



\\\[

\\beta=0.90

\\]



and:



\\\[

\\lambda=0.05.

\\]



These values are initial experimental settings rather than theoretically

optimal parameters.



\---



\## Causal Architecture



The process covariance used for the current prediction depends only on

mismatch information available before the current measurement arrives.



After the new measurement is observed:



1\. the innovation is calculated,

2\. the mismatch indicator is updated,

3\. effective process uncertainty is updated, and

4\. the new uncertainty level becomes available for the following prediction.



Thus, the current observation does not retroactively modify the prediction

that generated its own innovation.



\---



\## Experimental Configuration



The physical system and stochastic conditions were held consistent with

Experiment 005.



True parameter:



\\\[

a=0.92

\\]



Initial parameter estimate:



\\\[

\\hat{a}\_0=0.50

\\]



Process input:



\\\[

u\_k=1

\\]



Process-noise standard deviation:



\\\[

\\sigma\_w=0.05

\\]



Measurement-noise standard deviation:



\\\[

\\sigma\_v=0.50

\\]



Simulation horizon:



\\\[

N=100

\\]



Random seed:



`42`



This allows direct comparison with the baseline integrated estimator.



\---



\## Aggregate Results



Raw measurement RMSE was:



\\\[

\\mathrm{RMSE}\_{measurement}=0.458451.

\\]



Full-run uncertainty-aware state-estimation RMSE was:



\\\[

\\mathrm{RMSE}\_{state}=0.493092.

\\]



The full-run estimator therefore remained slightly worse than the raw

measurement because the initial synchronization transient was still present.



However, the transient was substantially reduced relative to Experiment 005.



\---



\## Early Synchronization Performance



Experiment 005:



\\\[

\\mathrm{RMSE}\_{0:24}=1.640203.

\\]



Experiment 006:



\\\[

\\mathrm{RMSE}\_{0:24}=0.877279.

\\]



This represents an approximate reduction of:



\\\[

46.5\\%.

\\]



Innovation-driven covariance inflation therefore substantially reduced the

initial state-estimation transient.



\---



\## Intermediate Performance



For steps 25–49:



Experiment 005:



\\\[

0.382821

\\]



Experiment 006:



\\\[

0.183725.

\\]



This represents an approximate reduction of:



\\\[

52.0\\%.

\\]



\---



\## Late-Run Performance



For steps 50–99:



Experiment 005 state RMSE:



\\\[

0.372701.

\\]



Experiment 006 state RMSE:



\\\[

0.290847.

\\]



Thus, uncertainty handling improved late-run performance by approximately:



\\\[

22.0\\%

\\]



relative to the previous integrated estimator.



Raw measurement RMSE over the same interval was:



\\\[

0.460190.

\\]



Therefore, the uncertainty-aware state estimator reduced late-run RMSE

relative to raw measurements by approximately:



\\\[

36.8\\%.

\\]



\---



\## Parameter Identification



The final parameter estimate was:



\\\[

\\hat{a}\_{99}=0.923882.

\\]



The final absolute parameter error was:



\\\[

|a-\\hat{a}\_{99}|=0.003882.

\\]



Experiment 005 produced a final absolute parameter error of approximately:



\\\[

0.007893.

\\]



Thus, the uncertainty-aware architecture improved parameter identification

as well as state estimation in this experimental realization.



\---



\## Covariance Behavior



The final state covariance was:



\\\[

P\_{99}=0.045373.

\\]



For comparison, Experiment 005 ended with covariance near:



\\\[

P\_{99}=0.012639.

\\]



The uncertainty-aware estimator therefore retained greater estimated

uncertainty while simultaneously producing better late-run state estimates.



This demonstrates an important distinction:



> Lower covariance does not necessarily imply greater physical accuracy when

> model uncertainty is omitted from the estimator.



\---



\## Innovation-Driven Model Uncertainty



At the final simulation step:



\\\[

U\_{99}=0.271433.

\\]



The corresponding effective process-noise variance was:



\\\[

Q\_{\\mathrm{effective},99}=0.016072.

\\]



The physical process-noise variance alone was:



\\\[

Q\_{\\mathrm{base}}=0.0025.

\\]



The estimator therefore continued to represent prediction mismatch as

additional uncertainty rather than assuming the process model was perfectly

specified.



\---



\## Interpretation



Experiment 006 provides empirical support for the hypothesis that

innovation-driven covariance inflation can mitigate premature estimator

confidence during adaptive model synchronization.



The observed sequence is:



```text

Incorrect model parameter

&#x20;       ↓

Prediction mismatch

&#x20;       ↓

Large/persistent innovation

&#x20;       ↓

Mismatch indicator increases

&#x20;       ↓

Effective process covariance increases

&#x20;       ↓

Estimator retains greater uncertainty

&#x20;       ↓

Measurements receive greater corrective influence

&#x20;       ↓

State estimate improves

&#x20;       ↓

Parameter adaptation improves model fidelity

