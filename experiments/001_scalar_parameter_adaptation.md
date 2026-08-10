\# Experiment 001 — Scalar Parameter Adaptation



\## Objective



Evaluate whether an adaptive digital-twin model can estimate an unknown parameter of a noisy scalar dynamical system from sequential observations.



The experiment also compares an unnormalized parameter-update rule with a normalized adaptation rule after instability was observed in the baseline implementation.



\---



\## System Model



The true discrete-time system is:



\\\[

x\_{k+1} = a x\_k + u\_k

\\]



where:



\- \\(x\_k\\) is the true system state,

\- \\(a\\) is the unknown system parameter,

\- \\(u\_k\\) is the control/process input.



The experiment uses:



\\\[

a = 0.92

\\]



and:



\\\[

u\_k = 1.0

\\]



The digital twin begins with an incorrect parameter estimate:



\\\[

\\hat{a}\_0 = 0.50

\\]



\---



\## Observation Model



The true state is observed with additive Gaussian noise:



\\\[

y\_k = x\_k + v\_k

\\]



with:



\\\[

v\_k \\sim \\mathcal{N}(0, 0.15^2)

\\]



A fixed random seed of `42` is used so both adaptation experiments receive the same reproducible noise sequence.



\---



\## Twin Prediction



The digital twin predicts:



\\\[

\\hat{x}\_{k+1}

=

\\hat{a}\_k \\hat{x}\_k + u\_k

\\]



and computes prediction error:



\\\[

e\_k

=

y\_{k+1} - \\hat{x}\_{k+1}

\\]



For this initial experiment, the latest observation is used directly as the next state estimate rather than applying a separate filtering or state-estimation algorithm.



\---



\# Experiment 001A — Unnormalized Baseline



\## Adaptation Rule



The baseline parameter update was:



\\\[

\\hat{a}\_{k+1}

=

\\hat{a}\_k

\+

\\eta e\_k \\hat{x}\_k

\\]



with learning rate:



\\\[

\\eta = 0.08

\\]



\## Observation



The parameter estimate initially moved toward the true value:



```text

0.5000

0.5317

0.6442

0.8376

0.8916

