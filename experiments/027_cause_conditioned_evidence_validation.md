\# Experiment 027 — Independent Cause-Conditioned Evidence Validation



\## Objective



Evaluate the frozen cause-conditioned evidence-sufficiency rules developed in

Experiment 026 on previously unseen operating points and stochastic

realizations.



No features, threshold directions, or numerical thresholds are modified after

observing validation results.



\---



\## Frozen Rules



The Experiment 026 rules were evaluated without modification.



\### Measurement Noise



\\\[

\\hat e\_M=1

\\iff

m\\ge0.5162128944

\\land

U\_{\\mathrm{post}}\\ge0.0953430901.

\\]



\### Process Disturbance



\\\[

\\hat e\_P=1

\\iff

\\rho\_{\\mathrm{NIS}}\\le0.3401323777.

\\]



\### Parameter Mismatch



\\\[

\\hat e\_{\\Theta}=1

\\iff

m\\ge0.5733833425.

\\]



\### Structural Change



\\\[

\\hat e\_S=1

\\iff

\\Delta\\hat a\_{\\mathrm{post-pre}}

\\le-0.04926012886.

\\]



\---



\## Independent Validation Design



Eight previously unseen intermediate operating points were evaluated.



Each operating point contained 100 stochastic realizations using a new seed

range beginning at 3000.



The resulting validation population contained



\\\[

N=800

\\]



trajectories.



Evidence sufficiency remained defined at the operating-point level by



\\\[

e(c)=

\\mathbf 1\[

A(c)\\ge0.90

\\land

C(c)\\ge0.80

\\land

A\_{\\mathrm{sel}}(c)\\ge0.95

].

\\]



\---



\## Validation Results



Frozen-rule trajectory-level evidence accuracy was:



| Cause | Accuracy |

|---|---:|

| Measurement noise | 45.0% |

| Process disturbance | 56.5% |

| Parameter mismatch | 59.0% |

| Structural change | 74.0% |



Overall accuracy was



\\\[

\\boxed{

58.625\\%

}

\\]



or



\\\[

469/800.

\\]



The strong development performance of the Experiment 026 rules therefore did

not generalize to independent intermediate operating points.



\---



\## Operating-Point Results



| Condition | Evidence sufficient | Hard accuracy | Coverage | Selective accuracy | Predicted sufficient |

|---|---:|---:|---:|---:|---:|

| measurement\_noise\_0.90 | True | 92.0% | 81.0% | 100.0% | 39.0% |

| measurement\_noise\_0.95 | True | 93.0% | 87.0% | 98.851% | 51.0% |

| process\_disturbance\_2.65 | False | 91.0% | 78.0% | 96.154% | 47.0% |

| process\_disturbance\_2.85 | True | 95.0% | 92.0% | 97.826% | 60.0% |

| parameter\_mismatch\_0.425 | False | 91.0% | 68.0% | 98.529% | 46.0% |

| parameter\_mismatch\_0.385 | True | 97.0% | 86.0% | 100.0% | 64.0% |

| structural\_change\_0.87 | False | 88.0% | 65.0% | 92.308% | 51.0% |

| structural\_change\_0.86 | True | 92.0% | 82.0% | 95.122% | 99.0% |



The operating-point labels remain internally consistent with the predefined

criterion.



The principal validation failure therefore lies in trajectory-level evidence

prediction rather than an obvious inconsistency in the evidence-sufficiency

definition.



\---



\## Statistical-Level Mismatch



Experiment 027 exposes a fundamental distinction.



Evidence sufficiency is defined as a property of an operating condition:



\\\[

e(c)=

\\mathbf 1\[

A(c)\\ge0.90

\\land

C(c)\\ge0.80

\\land

A\_{\\mathrm{sel}}(c)\\ge0.95

].

\\]



These quantities are population statistics estimated from repeated stochastic

realizations.



The Experiment 026 estimators instead attempted to infer this population

property from a single realization:



\\\[

\\hat e\_i=\\Psi\_j(\\mathcal I\_i).

\\]



Consequently,



\\\[

\\boxed{

\\text{trajectory evidence}

\\neq

\\text{population evidence sufficiency}.

}

\\]



A trajectory from an evidence-sufficient operating condition may exhibit weak

realized evidence, while a trajectory from an evidence-insufficient condition

may exhibit unusually strong realized evidence.



\---



\## Structural-Change Example



The structural-change validation points provide a particularly clear example.



At the insufficient operating point,



\\\[

a'=0.87,

\\]



the mean parameter-shift feature was



\\\[

\-0.049844

\\]



with standard deviation



\\\[

0.004005.

\\]



This distribution lies almost directly on the frozen threshold



\\\[

\-0.049260.

\\]



The frozen rule therefore predicted sufficient evidence for approximately



\\\[

51\\%

\\]



of trajectories.



However, the operating point itself failed the evidence criterion:



\\\[

A=88\\%,

\\qquad

C=65\\%,

\\qquad

A\_{\\mathrm{sel}}=92.308\\%.

\\]



At



\\\[

a'=0.86,

\\]



the mean parameter shift moved to



\\\[

\-0.059399

\\]



with standard deviation



\\\[

0.004142.

\\]



The rule predicted sufficient evidence for



\\\[

99\\%

\\]



of trajectories, while the operating point satisfied the evidence criterion.



This indicates that the parameter-shift feature contains meaningful

population-level information even though a deterministic trajectory-level

threshold does not reliably represent evidence sufficiency near the boundary.



\---



\## Interpretation



Experiment 027 rejects the hypothesis that the frozen deterministic

trajectory-level rules provide general evidence-sufficiency estimators.



The result does not imply that the selected features contain no useful

information.



Instead, the validation distributions show systematic feature movement across

several evidence boundaries while retaining substantial trajectory-level

overlap.



This suggests that evidence sufficiency is better treated as a latent

population-level property inferred from accumulated stochastic evidence.



\---



\## Revised Formulation



The next formulation should replace the deterministic single-trajectory model



\\\[

\\hat e\_i=\\Psi\_j(\\mathcal I\_i)

\\]



with a sequential or aggregated estimator such as



\\\[

\\boxed{

P(

e=1

\\mid

\\mathcal I\_{1:n},

z=j

)

}

\\]



where evidence is accumulated across observations, windows, or repeated

realizations.



The decision architecture then becomes



\\\[

\\text{detect}

\\rightarrow

\\text{attribute}

\\rightarrow

\\text{accumulate cause-conditioned evidence}

\\rightarrow

P(e=1)

\\rightarrow

\\text{adapt / wait / abstain}.

\\]



\---



\## Methodological Outcome



No Experiment 026 thresholds are modified after validation.



The validation failure is retained as a research result.



Experiment 027 therefore provides evidence against threshold retuning and in

favor of reformulating evidence sufficiency at the appropriate statistical

level.



\---



\## Conclusion



Independent validation produced an overall frozen-rule evidence accuracy of



\\\[

58.625\\%.

\\]



The deterministic cause-conditioned rules therefore failed to generalize as

trajectory-level evidence-sufficiency estimators.



The failure reveals a deeper modeling issue: evidence sufficiency is defined

from population behavior but was being predicted from individual stochastic

realizations.



The next research stage should investigate whether cause-conditioned evidence

can instead be estimated through sequential aggregation and probabilistic

inference.



\---



\## Next Research Direction



Experiment 028 should investigate sequential evidence aggregation.



The central question becomes



\\\[

\\boxed{

\\text{How much cause-conditioned evidence must accumulate before the twin can

reliably infer that its mismatch attribution is sufficiently identifiable?}

}

\\]



\---



\## Reproducibility



Experiment:



`experiments/cause\_conditioned\_evidence\_validation.py`



Results:



`results/cause\_conditioned\_evidence\_validation.csv`



Frozen rule source:



`experiments/026\_cause\_conditioned\_evidence\_estimation.md`

