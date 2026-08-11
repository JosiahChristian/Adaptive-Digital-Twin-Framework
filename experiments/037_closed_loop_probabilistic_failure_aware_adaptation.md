\# Experiment 037 — Closed-Loop Probabilistic Failure-Aware Adaptation Proxy



\## Objective



Test whether the policy actions developed in Experiments 034–036 produce

beneficial adaptation behavior when their adaptation and uncertainty semantics

are applied to realized estimator trajectories.



This experiment is a proxy closed-loop study. Policy actions are applied to

the parameter-update sequence after the underlying trajectory has already been

generated. Consequently, the modified actions do not influence subsequent

innovations, covariances, or estimator states.



\## Results



| Policy | State Proxy RMSE | Parameter RMSE | Final Parameter Error | Cumulative Update | Recovery |

|---|---:|---:|---:|---:|---:|

| baseline | 0.7337 | 0.0099 | 0.0052 | 0.7559 | 100% |

| generic uncertainty | 0.5991 | 0.3218 | 0.3224 | 0.1890 | 0% |

| probabilistic failure-aware | 0.6563 | 0.3867 | 0.3870 | 0.0756 | 0% |



The result is consistent across all four mismatch mechanisms.



\## Interpretation



The conservative action semantics developed in earlier decision-cost

experiments do not transfer directly to parameter adaptation.



Both uncertainty-aware policies strongly suppress cumulative parameter

adaptation. This prevents the estimator from reaching the true parameter and

eliminates recovery.



The strongest suppression occurs under the probabilistic failure-aware policy,

which also produces the largest parameter error.



Therefore,



\\\[

\\boxed{

\\text{decision conservatism}

\\neq

\\text{adaptation suppression}.

}

\\]



A policy can correctly decide to avoid causal commitment while still needing

to preserve or redirect estimator adaptation.



\## State-Proxy Limitation



The reported state proxy is not a true independently simulated state-error

metric.



It is constructed from the innovation sequence and uncertainty scaling.

Consequently, increasing uncertainty scale can mechanically reduce the proxy

without improving the underlying state estimate.



No strong dynamical conclusion should therefore be drawn from the lower proxy

RMSE of the generic policy.



\## Mechanism-Level Result



For every tested mismatch mechanism, baseline adaptation achieved 100%

recovery while both conservative proxy policies achieved 0%.



The failure is therefore systematic rather than mechanism specific.



\## Conclusion



Experiment 037 rejects the naive hypothesis that the action parameters from

the abstract decision-cost policy can be transferred directly into adaptation

scaling.



Aggressive suppression of parameter updates destroys estimator recovery.



The next experiment must move the policy inside the estimator loop and,

critically, distinguish between:



1\. causal commitment,

2\. parameter adaptation,

3\. uncertainty inflation,

4\. structural intervention.



These controls should no longer be represented by one generic adaptation

scale.



\## Next Research Direction



Experiment 038 should implement a genuinely online closed-loop estimator in

which policy actions affect future covariance, innovation, and parameter

updates.



Rather than suppressing all adaptation, the policy should test differentiated

actions such as:



\- preserve parameter learning while delaying causal commitment,

\- increase process uncertainty without shrinking parameter updates,

\- freeze only structural intervention,

\- reduce adaptation only when the inferred failure state specifically warrants

&#x20; it.



The central question becomes



\\\[

\\boxed{

\\text{Which control channel should each epistemic failure state modify?}

}

\\]

