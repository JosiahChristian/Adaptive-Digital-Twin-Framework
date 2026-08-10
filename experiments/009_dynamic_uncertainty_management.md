\# Experiment 009 — Dynamic Uncertainty Management



\## Objective



Evaluate whether the adaptive digital twin can dynamically adjust its

model-uncertainty response during operation rather than using one fixed

covariance-inflation strength.



Experiments 007 and 008 revealed a tradeoff:



\- stronger covariance inflation improved initial synchronization,

\- more conservative inflation produced stronger late-run filtering.



Experiment 009 investigates whether a mismatch-dependent inflation schedule

can combine these behaviors within one estimator.



\---



\## Dynamic Inflation Policy



The uncertainty mechanism continues to use the innovation-energy mismatch

indicator:



\\\[

U\_k

=

\\beta U\_{k-1}

\+

(1-\\beta)r\_k^2.

\\]



Instead of using a fixed inflation strength, the estimator computes:



\\\[

\\lambda\_k

=

\\lambda\_{\\min}

\+

(\\lambda\_{\\max}-\\lambda\_{\\min})

\\frac{U\_k}{U\_k+c}.

\\]



The effective process-noise variance is then:



\\\[

Q\_{\\mathrm{effective},k}

=

Q\_{\\mathrm{base}}

\+

\\lambda\_k U\_k.

\\]



\---



\## Policy Parameters



The experiment used:



\\\[

\\beta=0.50

\\]



\\\[

\\lambda\_{\\min}=0.05

\\]



\\\[

\\lambda\_{\\max}=0.20

\\]



and transition scale:



\\\[

c=0.25.

\\]



These values were selected to connect the conservative and aggressive

inflation regimes identified in previous experiments.



They are experimental settings rather than theoretically optimal values.



\---



\## Intended Behavior



For small mismatch:



\\\[

U\_k\\rightarrow0,

\\]



the policy approaches:



\\\[

\\lambda\_k\\rightarrow\\lambda\_{\\min}.

\\]



For large mismatch:



\\\[

U\_k\\rightarrow\\infty,

\\]



the policy approaches:



\\\[

\\lambda\_k\\rightarrow\\lambda\_{\\max}.

\\]



The intended architecture is therefore:



```text

Low mismatch

&#x20;   ↓

Low inflation

&#x20;   ↓

More model trust



High mismatch

&#x20;   ↓

High inflation

&#x20;   ↓

More measurement correction

