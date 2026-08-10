\# Experiment 005 — Integrated Adaptive State and Parameter Estimation



\## Objective



Integrate recursive state estimation and online parameter adaptation into a single scalar digital-twin architecture.



Previous experiments validated these components independently:



\- Experiments 001–003 investigated online parameter adaptation.

\- Experiment 004 investigated Kalman state estimation using the correct system parameter.



This experiment removes that assumption.



The Kalman estimator begins with an incorrect model parameter and must operate using the digital twin's evolving estimate:



\\\[

\\hat{a}\_k.

\\]



The objective is to determine whether the coupled system can recover both:



\\\[

\\hat{x}\_k

\\]



and:



\\\[

\\hat{a}\_k

\\]



from noisy observations.



\---



\## Physical System



The true stochastic system is:



\\\[

x\_{k+1}

=

a x\_k

\+

u\_k

\+

w\_k.

\\]



The true parameter is:



\\\[

a=0.92.

\\]



The process input is:



\\\[

u\_k=1.

\\]



The twin begins with:



\\\[

\\hat{a}\_0=0.50.

\\]



Thus, the estimator initially operates with substantial model error.



\---



\## Measurement Model



Measurements are generated according to:



\\\[

y\_k

=

x\_k

\+

v\_k.

\\]



Process noise:



\\\[

\\sigma\_w=0.05.

\\]



Measurement noise:



\\\[

\\sigma\_v=0.50.

\\]



The simulation was executed for:



\\\[

N=100

\\]



steps with random seed:



`42`.



\---



\## Coupled Digital-Twin Architecture



The integrated estimator operates recursively:



```text

Current parameter estimate

&#x20;       ↓

Kalman model prediction

&#x20;       ↓

Noisy sensor measurement

&#x20;       ↓

Innovation

&#x20;       ↓

Kalman state correction

&#x20;       ↓

Updated state estimate

&#x20;       ↓

Normalized parameter adaptation

&#x20;       ↓

New parameter estimate

&#x20;       ↺

