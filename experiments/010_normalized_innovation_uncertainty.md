\# Experiment 010 — Normalized Innovation Uncertainty



\## Objective



Replace raw innovation-energy model-mismatch detection with a

statistically normalized innovation signal.



The purpose is to distinguish unexpected model disagreement from

innovation that is already consistent with the estimator's predicted

uncertainty.



\## Mathematical Basis



For scalar innovation



\\\[

r\_k = y\_k - \\hat{x}\_k^{-},

\\]



the innovation covariance is



\\\[

S\_k = P\_k^{-} + R.

\\]



The normalized innovation squared (NIS) is



\\\[

\\epsilon\_k = \\frac{r\_k^2}{S\_k}.

\\]



For a statistically consistent scalar Gaussian estimator,



\\\[

E\[\\epsilon\_k] \\approx 1.

\\]



Only innovation exceeding this reference level contributes directly

to the mismatch signal:



\\\[

m\_k = \\max(0,\\epsilon\_k - 1).

\\]



The smoothed mismatch indicator is



\\\[

U\_k =

\\beta U\_{k-1}

\+

(1-\\beta)m\_k.

\\]



Dynamic covariance inflation is then computed from



\\\[

\\lambda\_k =

\\lambda\_{\\min}

\+

(\\lambda\_{\\max}-\\lambda\_{\\min})

\\frac{U\_k}{U\_k+c},

\\]



with effective process-noise variance



\\\[

Q\_{\\mathrm{eff},k}

=

Q\_{\\mathrm{base}}

\+

\\lambda\_k U\_k.

\\]



\## Configuration



\- True system parameter: 0.92

\- Initial parameter estimate: 0.50

\- Learning rate: 0.08

\- Process-noise standard deviation: 0.05

\- Measurement-noise standard deviation: 0.50

\- Innovation memory: 0.50

\- Minimum inflation strength: 0.05

\- Maximum inflation strength: 0.20

\- Transition scale: 0.25

\- Simulation length: 100 steps

\- Random seed: 42



\## Results



\- Measurement RMSE: 0.458451

\- Full state-estimation RMSE: 0.372992

\- State RMSE, steps 0–24: 0.621916

\- State RMSE, steps 25–49: 0.161099

\- State RMSE, steps 50–99: 0.268105

\- Measurement RMSE, steps 50–99: 0.460190

\- Mean NIS, full trajectory: 1.257587

\- Mean NIS, steps 50–99: 0.764032

\- Final parameter estimate: 0.922372

\- Final parameter absolute error: 0.002372

\- Final state covariance: 0.094658

\- Final mismatch indicator: 0.173498

\- Final dynamic inflation strength: 0.111452

\- Final effective process-noise variance: 0.021837



\## Comparison with Experiment 009



Experiment 009 produced a full state RMSE of 0.380487.



Experiment 010 reduced this to 0.372992, an improvement of

approximately 1.97%.



Early transient RMSE improved from 0.643501 to 0.621916.



Late-stage RMSE remained essentially unchanged:



\- Experiment 009: 0.267665

\- Experiment 010: 0.268105



The final parameter error also decreased slightly from approximately

0.002415 to 0.002372.



\## Interpretation



Normalized innovation provides a more principled mismatch signal than

raw innovation energy because residual magnitude is evaluated relative

to the uncertainty predicted by the estimator.



The full-trajectory mean NIS of approximately 1.26 reflects the strong

initial model mismatch caused by the deliberately inaccurate initial

parameter estimate.



During steps 50–99, mean NIS falls to approximately 0.76. This suggests

that after adaptation the estimator becomes somewhat conservative:

predicted innovation uncertainty exceeds the residual energy actually

observed.



Individual late-stage residuals can therefore produce zero excess NIS,

preventing ordinary stochastic disagreement from automatically being

classified as model mismatch.



The results support normalized innovation as a stronger uncertainty

diagnostic while also revealing a new limitation: covariance inflation

may persist after the estimator has substantially synchronized with the

true system.



\## Conclusion



Experiment 010 demonstrates that uncertainty adaptation based on

normalized innovation can improve transient and overall state

estimation while preserving parameter convergence.



The next experiment should investigate whether uncertainty inflation

can decay or gate itself when normalized innovation indicates that the

estimator has returned to a statistically consistent regime.

