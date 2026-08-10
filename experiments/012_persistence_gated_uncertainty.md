\# Experiment 012 — Persistence-Gated Uncertainty Decay



\## Objective



Evaluate whether accelerated model-uncertainty decay should require persistent

statistical consistency rather than a single low-NIS observation.



Experiment 011 demonstrated that instantaneous consistency gating substantially

reduced residual uncertainty, but slightly degraded overall state and parameter

estimation.



Experiment 012 tests whether requiring multiple consecutive statistically

consistent observations preserves useful model uncertainty while still

removing stale mismatch memory.



\---



\## Motivation



Experiment 011 applied accelerated mismatch decay whenever:



\\\[

\\epsilon\_k \\le 1.

\\]



However, one statistically consistent observation provides limited evidence

that the adaptive digital twin has genuinely entered a synchronized regime.



A single observation can be influenced by stochastic process and measurement

noise.



Experiment 012 therefore introduces a persistence requirement.



\---



\## Persistence Rule



An observation is classified as statistically consistent when:



\\\[

\\epsilon\_k \\le \\tau

\\]



with:



\\\[

\\tau=1.

\\]



A consistency counter increments for each consecutive consistent observation.



If:



\\\[

\\epsilon\_k > \\tau,

\\]



the counter immediately resets to zero.



Accelerated mismatch decay activates only after:



\\\[

N=3

\\]



consecutive consistent observations.



When active:



\\\[

U\_k

\\leftarrow

\\rho U\_k

\\]



with:



\\\[

\\rho=0.70.

\\]



\---



\## State-Machine Interpretation



The persistence logic behaves as:



```text

consistent observation

&#x20;       ↓

count = 1



consistent observation

&#x20;       ↓

count = 2



consistent observation

&#x20;       ↓

count = 3

&#x20;       ↓

accelerated uncertainty decay



inconsistent observation

&#x20;       ↓

count = 0

