\# Experiment 038 — Online Failure-State-Conditioned Estimator Control



\## Objective



Determine whether epistemic failure-state information can be coupled directly

to the recursive adaptive estimator without destroying the parameter-recovery

mechanism observed under baseline adaptation.



Experiment 037 showed that generic uncertainty-aware suppression of adaptation

could reduce intervention exposure while simultaneously preventing parameter

recovery. Experiment 038 therefore separates parameter learning from process

uncertainty control.



\## Hypothesis



Failure-state information should control the estimator channel associated with

the inferred epistemic limitation rather than uniformly suppress adaptation.



In particular,



\- coverage failure should delay commitment while preserving learning,

\- hard-accuracy failure should increase process uncertainty while preserving

&#x20; most parameter adaptation,

\- selective-accuracy failure should restrict high-impact intervention without

&#x20; disabling estimation.



\## Method



Four representative mismatch conditions were evaluated:



\- measurement noise,

\- process disturbance,

\- parameter mismatch,

\- structural change.



For each condition, 100 independent trajectories were evaluated under three

policies:



1\. baseline,

2\. generic uncertainty,

3\. failure-aware control.



The policies acted inside the recursive normalized-innovation estimator.



The experiment therefore modified the actual estimator dynamics rather than

applying policy effects after trajectory generation.



Total trajectories:



\\\[

4 \\times 100 \\times 3 = 1200.

\\]



Reference epistemic failure probabilities were obtained from the

criterion-component failure decomposition and used to select estimator-control

actions.



\## Results



\### Aggregate performance



| Policy | State RMSE | Parameter RMSE | Final parameter error | Cumulative update | Post-event NIS | Recovery |

|---|---:|---:|---:|---:|---:|---:|

| Baseline | 0.3461 | 0.0099 | 0.0050 | 0.7552 | 1.1048 | 100% |

| Generic uncertainty | 0.3506 | 0.0099 | 0.0049 | 0.7530 | 1.0673 | 100% |

| Failure-aware | 0.3450 | 0.0097 | 0.0049 | 0.7444 | 1.0658 | 100% |



The failure-aware controller preserved complete parameter recovery while

achieving the lowest aggregate state RMSE, parameter RMSE, and post-event NIS.



\### Process disturbance



The strongest mechanism-specific improvement occurred under process

disturbance.



| Policy | State RMSE | Parameter RMSE | Final parameter error | Post-event NIS | Recovery |

|---|---:|---:|---:|---:|---:|

| Baseline | 0.4158 | 0.0097 | 0.0040 | 1.3766 | 100% |

| Generic uncertainty | 0.4158 | 0.0097 | 0.0040 | 1.3766 | 100% |

| Failure-aware | 0.4083 | 0.0089 | 0.0034 | 1.2558 | 100% |



Failure-aware covariance modulation therefore improved state estimation,

parameter estimation, and innovation consistency without sacrificing recovery.



\## Interpretation



The failure of Experiment 037 was not evidence that epistemic control should be

removed from the adaptive twin. It showed that epistemic caution had been

coupled to the wrong dynamical channel.



Experiment 038 demonstrates the distinction



\\\[

\\text{epistemic uncertainty}

\\not\\Rightarrow

\\text{less adaptation}.

\\]



Instead,



\\\[

\\text{epistemic state}

\\rightarrow

\\text{channel-specific control}.

\\]



Parameter learning can remain active while uncertainty inflation, commitment,

and intervention permissions are controlled independently.



The result supports a layered adaptive architecture in which epistemic

diagnosis determines \*how\* the twin responds to uncertainty rather than simply

reducing adaptation globally.



\## Limitation



The failure-state probabilities used by the controller are reference

condition-level distributions obtained from prior experiments. They are not yet

estimated online from the current trajectory.



Consequently, this experiment validates the control semantics under recursive

dynamics, but not yet the complete online inference-control loop.



\## Conclusion



Failure-state-conditioned estimator control resolves the adaptation-suppression

failure observed in Experiment 037.



Across all tested mismatch mechanisms, parameter recovery remained 100%.

Aggregate estimator performance was preserved or improved, with the strongest

benefit appearing under process disturbance.



These results support the architectural principle



\\\[

\\boxed{

\\text{epistemic state}

\\rightarrow

\\text{control-channel selection}

\\rightarrow

\\text{adaptive estimator dynamics}

}

\\]



and motivate replacing reference failure-state distributions with online

trajectory-derived epistemic-state estimates.

