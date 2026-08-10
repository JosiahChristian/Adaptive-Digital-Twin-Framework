\# Experiment 004 — Kalman State Estimation



\## Objective



Evaluate whether recursive state estimation can improve the quality of state information available to the adaptive digital twin when the physical system is observed through noisy measurements.



Previous scalar experiments used the current observation directly as the estimated system state.



This experiment introduces a scalar Kalman filter that explicitly distinguishes:



\\\[

\\text{physical state}

\\neq

\\text{sensor measurement}

\\neq

\\text{estimated state}.

\\]



The immediate objective is to validate the state estimator independently before integrating it with online parameter adaptation.



\---



\## System Model



The stochastic scalar system is represented as:



\\\[

x\_{k+1}

=

a x\_k

\+

u\_k

\+

w\_k,

\\]



where:



\- \\(x\_k\\) is the physical system state,

\- \\(a\\) is the system parameter,

\- \\(u\_k\\) is the known process input, and

\- \\(w\_k\\) represents process noise.



The measurement model is:



\\\[

y\_k

=

x\_k

\+

v\_k,

\\]



where \\(v\_k\\) represents measurement noise.



\---



\## Experimental Configuration



The experiment used:



\\\[

a=0.92

\\]



and:



\\\[

u\_k=1.

\\]



The simulation horizon was:



\\\[

N=60.

\\]



Process-noise standard deviation:



\\\[

\\sigma\_w=0.05.

\\]



Measurement-noise standard deviation:



\\\[

\\sigma\_v=0.50.

\\]



Therefore:



\\\[

Q=\\sigma\_w^2=0.0025

\\]



and:



\\\[

R=\\sigma\_v^2=0.25.

\\]



The random seed was fixed at:



`42`



to provide deterministic reproducibility of the initial experiment.



\---



\## Kalman Prediction



The predicted state is:



\\\[

\\hat{x}\_k^-

=

a\\hat{x}\_{k-1}

\+

u\_k.

\\]



The predicted covariance is:



\\\[

P\_k^-

=

a^2P\_{k-1}

\+

Q.

\\]



\---



\## Measurement Update



The Kalman gain is:



\\\[

K\_k

=

\\frac{P\_k^-}

{P\_k^-+R}.

\\]



The innovation is:



\\\[

y\_k-\\hat{x}\_k^-.

\\]



The corrected state estimate is:



\\\[

\\hat{x}\_k

=

\\hat{x}\_k^-

\+

K\_k

\\left(

y\_k-\\hat{x}\_k^-

\\right).

\\]



The updated covariance is:



\\\[

P\_k

=

(1-K\_k)P\_k^-.

\\]



The Kalman gain therefore determines how strongly the estimator corrects its model prediction using the current sensor measurement.



\---



\## Results



The raw measurement RMSE was:



\\\[

\\mathrm{RMSE}\_{measurement}

=

0.453740.

\\]



The Kalman-filtered state-estimation RMSE was:



\\\[

\\mathrm{RMSE}\_{filtered}

=

0.089972.

\\]



The relative RMSE reduction was:



\\\[

\\frac{

0.453740-0.089972

}{

0.453740

}

\\times100

\\approx

80.17\\%.

\\]



Thus, for this experimental realization, the Kalman estimator reduced state-estimation RMSE by approximately:



\\\[

\\boxed{80.17\\%}

\\]



relative to using the noisy sensor measurements directly.



\---



\## Covariance Behavior



After the first measurement update, the estimated covariance was approximately:



\\\[

P\_0=0.193125.

\\]



By the final simulation step:



\\\[

P\_{59}

\\approx

0.012201.

\\]



The covariance approached a nearly constant value during the later portion of the experiment.



This behavior is consistent with the scalar filter approaching a steady uncertainty regime under fixed system dynamics and constant process- and measurement-noise assumptions.



\---



\## Representative Observations



At simulation step 5:



\\\[

x\_k

\\approx

4.92256

\\]



while the noisy measurement was:



\\\[

y\_k

\\approx

5.50434.

\\]



The raw measurement error was therefore approximately:



\\\[

0.58178.

\\]



The Kalman estimate was:



\\\[

\\hat{x}\_k

\\approx

4.91429,

\\]



corresponding to an estimation error of approximately:



\\\[

\-0.00827.

\\]



This individual observation illustrates the estimator's ability to reject a relatively large measurement disturbance by combining the measurement with the dynamical model.



The aggregate RMSE results provide the more meaningful measure of performance across the complete experiment.



\---



\## Interpretation



The experiment demonstrates that explicitly estimating the system state can substantially improve the state information supplied to a model-based digital twin.



The Kalman filter combines two imperfect sources of information:



1\. a model-based state prediction, and

2\. a noisy physical measurement.



Rather than treating the sensor measurement as the physical state itself, the estimator recursively balances prediction and observation according to their modeled uncertainty.



For the tested configuration, this produced substantially lower state-estimation error than direct use of the measurements.



\---



\## Important Limitation



The Kalman filter in this experiment was supplied with the true system parameter:



\\\[

a=0.92.

\\]



Therefore, this experiment evaluates state estimation under a correctly specified process model.



It does not yet represent the complete adaptive digital-twin problem, because a real adaptive twin may not know the true system parameter in advance.



Additionally, the approximately 80.17% RMSE reduction is a result from one deterministic random-seed realization and should not yet be interpreted as a general performance guarantee.



Future robustness experiments should evaluate the estimator across multiple stochastic realizations and noise conditions.



\---



\## Architectural Significance



The framework now contains two independently validated capabilities:



\### Online Parameter Adaptation



The adaptive subsystem estimates an unknown model parameter:



\\\[

\\hat{a}\_k.

\\]



\### Recursive State Estimation



The Kalman subsystem estimates the hidden physical state:



\\\[

\\hat{x}\_k.

\\]



The next architectural step is to combine these components so that the adaptive digital twin estimates both:



\\\[

\\boxed{

\\text{system state}

\+

\\text{model parameter}

}

\\]



during system operation.



\---



\## Next Research Question



What happens when the Kalman state estimator no longer receives the true system parameter and instead operates using the digital twin's evolving estimate:



\\\[

\\hat{a}\_k?

\\]



The next experiment will integrate recursive state estimation with online parameter adaptation and evaluate the coupled estimator-adaptation dynamics.



\---



\## Reproducibility



Kalman implementation:



`simulation/scalar\_kalman\_filter.py`



Experiment implementation:



`experiments/scalar\_kalman\_experiment.py`



Raw results:



`results/scalar\_kalman\_estimation.csv`



Automated tests:



`tests/test\_scalar\_kalman\_filter.py`

