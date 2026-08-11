\# Experiment 040 — Sequential Epistemic Inference Coupled to Online Estimator Control



\## Objective



Determine whether sequentially inferred epistemic failure-state information can

drive recursive estimator control without access to the complete reference

epistemic distribution.



Experiment 038 demonstrated that reference failure-state information can be

mapped to mechanism-appropriate estimator control channels while preserving

parameter recovery.



Experiment 039 demonstrated that the epistemic state can be estimated

progressively from finite sequential evidence.



Experiment 040 couples these two components.



\## Architecture



The inferred controller implements



\\\[

D\_{1:n}

\\rightarrow

\\hat{\\boldsymbol{\\pi}}\_n

\\rightarrow

u\_n^{\\mathrm{epistemic}}

\\rightarrow

\\text{recursive estimator dynamics}.

\\]



Three controllers were compared:



1\. baseline,

2\. reference-aware failure control,

3\. inferred failure-aware control.



The reference-aware controller receives the complete condition-level epistemic

distribution and serves only as a privileged benchmark.



The inferred controller receives only the first \\(n\\) sequential epistemic

observations.



\## Evidence Budgets



Sequential evidence budgets were



\\\[

n\\in\\{5,10,20\\}.

\\]



For each evidence budget, the inferred epistemic state was constructed from the

observed prefix only.



The complete reference state did not enter the inferred controller's decision

rule.



\## Experimental Design



Four representative mismatch conditions were evaluated.



For each condition:



\- 100 sequence replicates were generated,

\- three evidence budgets were evaluated,

\- three control policies were compared,

\- policies used identical physical random seeds within each replicate.



The experiment generated



\\\[

4\\times100\\times3\\times3

=

3600

\\]



control evaluations.



\## Results



\### n = 5



| Policy | State RMSE | Parameter RMSE | Final Error | Post-Event NIS | Recovery |

|---|---:|---:|---:|---:|---:|

| Baseline | 0.3432 | 0.0099 | 0.0053 | 1.1037 | 100% |

| Reference aware | 0.3427 | 0.0097 | 0.0052 | 1.0648 | 100% |

| Inferred failure aware | 0.3441 | 0.0098 | 0.0051 | 1.0535 | 100% |



The inferred controller selected the same action as the reference-aware

controller in



\\\[

83.0\\%

\\]



of cases.



\### n = 10



| Policy | State RMSE | Parameter RMSE | Final Error | Post-Event NIS | Recovery |

|---|---:|---:|---:|---:|---:|

| Baseline | 0.3432 | 0.0099 | 0.0053 | 1.1037 | 100% |

| Reference aware | 0.3427 | 0.0097 | 0.0052 | 1.0648 | 100% |

| Inferred failure aware | 0.3436 | 0.0098 | 0.0051 | 1.0562 | 100% |



Action agreement increased to



\\\[

87.25\\%.

\\]



\### n = 20



| Policy | State RMSE | Parameter RMSE | Final Error | Post-Event NIS | Recovery |

|---|---:|---:|---:|---:|---:|

| Baseline | 0.3432 | 0.0099 | 0.0053 | 1.1037 | 100% |

| Reference aware | 0.3427 | 0.0097 | 0.0052 | 1.0648 | 100% |

| Inferred failure aware | 0.3434 | 0.0098 | 0.0051 | 1.0589 | 100% |



Action agreement increased further to



\\\[

\\boxed{

91.5\\%.

}

\\]



\## Action-Selection Convergence



Reference-action agreement increased monotonically:



\\\[

83.0\\%

\\rightarrow

87.25\\%

\\rightarrow

91.5\\%

\\]



as sequential evidence increased from 5 to 20 observations.



Thus improved epistemic estimation translates directly into increasingly

accurate control-channel selection.



\## Dynamical Convergence



The state-RMSE gap between inferred and reference-aware control decreased with

evidence:



\\\[

0.0014

\\rightarrow

0.0009

\\rightarrow

0.0007.

\\]



Parameter RMSE remained within approximately



\\\[

0.0001

\\]



of the reference-aware controller across all evidence budgets.



All policies retained



\\\[

100\\%

\\]



parameter recovery.



Thus replacing reference epistemic information with finite sequential

inference did not reproduce the adaptation failure observed in Experiment 037.



\## Innovation Consistency



Baseline post-event NIS was



\\\[

1.1037.

\\]



Reference-aware control reduced this to



\\\[

1.0648.

\\]



The inferred controller produced values between



\\\[

1.0535

\\]



and



\\\[

1.0589.

\\]



Therefore finite-evidence inferred control maintained strong innovation

consistency despite imperfect action agreement.



\## Interpretation



Experiment 040 demonstrates the integrated mapping



\\\[

\\boxed{

D\_{1:n}

\\rightarrow

\\hat{\\boldsymbol{\\pi}}\_n

\\rightarrow

u\_n^{\\mathrm{epistemic}}

\\rightarrow

\\text{recursive adaptation}.

}

\\]



The inferred controller approaches the behavior of a privileged

reference-aware controller as evidence accumulates.



The result provides a direct operational connection between epistemic-state

estimation accuracy and estimator-control quality.



\## Benign Action Mismatch



Dynamical performance remains close to reference-aware performance even when

action agreement is imperfect.



At \\(n=5\\), action agreement is only



\\\[

83\\%,

\\]



yet state and parameter estimation remain close to the reference-aware

benchmark.



This suggests that not all categorical action mismatches have equal dynamical

cost.



Some actions may occupy approximately equivalent regions of the estimator

control space.



Future work should therefore distinguish between:



\\\[

\\text{categorical action error}

\\]



and



\\\[

\\text{dynamically consequential action error}.

\\]



\## Limitation



The sequential evidence units remain population-level criterion-failure

observations derived from prior experiments.



Consequently, Experiment 040 does not yet perform single-trajectory

self-diagnosis directly from the evolving innovation stream.



The inferred controller is online with respect to evidence availability, but

the evidence itself remains population-derived.



\## Conclusion



Sequential epistemic inference successfully replaced privileged reference

failure-state information in recursive estimator control.



As evidence increased,



\\\[

83.0\\%

\\rightarrow

87.25\\%

\\rightarrow

91.5\\%

\\]



of inferred actions matched the reference-aware control action.



At the same time, inferred-control state RMSE moved toward the reference-aware

benchmark while parameter recovery remained 100%.



Experiment 040 therefore validates the architecture



\\\[

\\boxed{

\\text{sequential evidence}

\\rightarrow

\\text{epistemic-state inference}

\\rightarrow

\\text{failure-aware control}

\\rightarrow

\\text{recursive estimator dynamics}.

}

\\]

