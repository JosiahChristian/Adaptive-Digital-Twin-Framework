\# Experiment 029 — Cause-Conditioned Aggregated Evidence Estimation



\## Objective



Determine whether cause-conditioned aggregation of trajectory-level evidence

can recover evidence sufficiency more reliably than deterministic

single-trajectory inference.



Experiments 026 and 027 showed that individual stochastic trajectories do not

reliably determine an evidence-sufficiency property defined at the

operating-condition population level.



Experiment 028 showed that aggregation reduces stochastic variability but also

demonstrated that one universal aggregated evidence threshold is inappropriate.



Experiment 029 therefore develops mechanism-specific aggregated evidence

estimators.



\---



\## Development Population



Experiment 029 returns to the balanced Experiment 025 development population.



This population contains:



\\\[

800

\\]



trajectories,



\\\[

400

\\]



evidence-sufficient trajectories, and



\\\[

400

\\]



evidence-insufficient trajectories.



Each causal mechanism contains one sufficient and one insufficient operating

condition with 100 stochastic realizations per condition.



The frozen Experiment 026 trajectory-level evidence rules are applied without

modification.



\---



\## Aggregated Evidence Statistic



For mismatch mechanism \\(j\\), let



\\\[

\\hat e\_i^{(j)}

\\in

\\{0,1\\}

\\]



denote the frozen Experiment 026 evidence decision for trajectory \\(i\\).



For a batch of \\(n\\) trajectories from the same operating condition, define



\\\[

\\boxed{

\\hat p\_n^{(j)}

=

\\frac{1}{n}

\\sum\_{i=1}^{n}

\\hat e\_i^{(j)}.

}

\\]



The tested batch sizes are



\\\[

n

\\in

\\{1,2,5,10,20,50\\}.

\\]



For every cause and batch size, repeated without-replacement subsampling is

used to characterize the distribution of the aggregated vote fraction.



\---



\## Cause-Conditioned Threshold Model



For each cause and batch size, a threshold rule of the form



\\\[

\\hat e\_j^{(n)}

=

\\mathbf 1

\[

\\hat p\_n^{(j)}

\\ \\square\_j\\

\\tau\_j(n)

]

\\]



is selected from the development population.



Both threshold directions are considered.



The objective is not to modify the frozen trajectory-level evidence rules.



Instead, the experiment asks whether accumulation of their stochastic outputs

produces a stable operating-condition statistic.



\---



\## Measurement Noise



Development accuracy changes with aggregation as follows:



| Batch size | Accuracy |

|---:|---:|

| 1 | 73.6% |

| 2 | 72.3% |

| 5 | 85.4% |

| 10 | 93.1% |

| 20 | 98.3% |

| 50 | 100.0% |



At



\\\[

n=50,

\\]



the selected rule is



\\\[

\\boxed{

\\hat e\_M^{(50)}=1

\\iff

\\hat p\_{50}^{(M)}

\\ge0.44.

}

\\]



The mean aggregated vote fractions are



\\\[

E\[

\\hat p\_{50}^{(M)}

\\mid

e=1

]

=

0.68012

\\]



and



\\\[

E\[

\\hat p\_{50}^{(M)}

\\mid

e=0

]

=

0.25024.

\\]



Development accuracy is



\\\[

100\\%.

\\]



\---



\## Process Disturbance



Development accuracy changes as:



| Batch size | Accuracy |

|---:|---:|

| 1 | 66.3% |

| 2 | 69.7% |

| 5 | 75.9% |

| 10 | 85.2% |

| 20 | 94.4% |

| 50 | 99.9% |



At



\\\[

n=50,

\\]



the selected rule is



\\\[

\\boxed{

\\hat e\_P^{(50)}=1

\\iff

\\hat p\_{50}^{(P)}

\\ge0.59.

}

\\]



Mean aggregated vote fractions are



\\\[

E\[

\\hat p\_{50}^{(P)}

\\mid

e=1

]

=

0.75068

\\]



and



\\\[

E\[

\\hat p\_{50}^{(P)}

\\mid

e=0

]

=

0.44964.

\\]



Development accuracy is



\\\[

99.9\\%.

\\]



\---



\## Parameter Mismatch



Development accuracy changes as:



| Batch size | Accuracy |

|---:|---:|

| 1 | 67.1% |

| 2 | 67.0% |

| 5 | 80.4% |

| 10 | 86.5% |

| 20 | 95.7% |

| 50 | 100.0% |



At



\\\[

n=50,

\\]



the selected rule is



\\\[

\\boxed{

\\hat e\_{\\Theta}^{(50)}=1

\\iff

\\hat p\_{50}^{(\\Theta)}

\\ge0.50.

}

\\]



Mean aggregated vote fractions are



\\\[

E\[

\\hat p\_{50}^{(\\Theta)}

\\mid

e=1

]

=

0.66684

\\]



and



\\\[

E\[

\\hat p\_{50}^{(\\Theta)}

\\mid

e=0

]

=

0.33172.

\\]



Development accuracy is



\\\[

100\\%.

\\]



\---



\## Structural Change



Structural change already exhibits strong separation at the trajectory level.



Development accuracy is



\\\[

99.5\\%

\\]



for



\\\[

n=1,

\\]



and reaches



\\\[

100\\%

\\]



for every tested batch size



\\\[

n\\ge2.

\\]



At



\\\[

n=50,

\\]



the selected rule is



\\\[

\\boxed{

\\hat e\_S^{(50)}=1

\\iff

\\hat p\_{50}^{(S)}

\\ge0.51.

}

\\]



Mean aggregated vote fractions are



\\\[

E\[

\\hat p\_{50}^{(S)}

\\mid

e=1

]

=

1.00000

\\]



and



\\\[

E\[

\\hat p\_{50}^{(S)}

\\mid

e=0

]

=

0.01056.

\\]



Development accuracy is



\\\[

100\\%.

\\]



\---



\## Frozen Aggregated Rules



The Experiment 029 development process produces the following frozen

\\(n=50\\) aggregate rules:



| Cause | Frozen aggregated evidence rule |

|---|---|

| Measurement noise | \\(\\hat p\_{50}\\ge0.44\\) |

| Process disturbance | \\(\\hat p\_{50}\\ge0.59\\) |

| Parameter mismatch | \\(\\hat p\_{50}\\ge0.50\\) |

| Structural change | \\(\\hat p\_{50}\\ge0.51\\) |



These thresholds are frozen after Experiment 029.



They must not be modified in response to Experiment 030 validation results.



\---



\## Interpretation



The results support the hypothesis that the weak performance of

single-trajectory evidence rules is substantially attributable to stochastic

realization variability.



For the first three mismatch mechanisms, aggregation produces a pronounced

increase in development accuracy as the number of accumulated trajectories

grows.



Conceptually,



\\\[

\\hat e\_i^{(j)}

\\]



is a noisy trajectory-level indicator.



The aggregated quantity



\\\[

\\hat p\_n^{(j)}

\\]



estimates the probability that the cause-conditioned trajectory evidence rule

fires under the current operating condition.



As



\\\[

n

\\]



increases, this population quantity becomes increasingly stable.



\---



\## Statistical-Level Interpretation



Experiment 027 identified a mismatch between the target and predictor:



\\\[

e(c)

\\]



is an operating-condition property, while



\\\[

\\hat e\_i

\\]



is a trajectory-level statistic.



Experiment 029 addresses that mismatch by estimating an operating-condition

quantity from repeated trajectory evidence:



\\\[

\\hat p\_n^{(j)}

\\rightarrow

P(

\\hat e^{(j)}=1

\\mid

c

)

\\]



as the number of accumulated realizations increases.



The evidence architecture is therefore better represented as



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



than as a deterministic single-trajectory threshold.



\---



\## Cause Dependence



The four frozen aggregate thresholds differ:



\\\[

0.44,

\\quad

0.59,

\\quad

0.50,

\\quad

0.51.

\\]



Therefore even after aggregation, evidence sufficiency remains

cause-conditioned.



There is no evidence supporting one universal vote threshold for all mismatch

mechanisms.



\---



\## Limitation



The near-perfect \\(n=50\\) performance is development performance.



The aggregate thresholds were selected using repeated subsamples of the same

balanced Experiment 025 operating conditions.



Consequently, these results do not establish generalization to new physical

conditions.



The development population also contains only one evidence-sufficient and one

evidence-insufficient operating point per mismatch mechanism.



The apparent separation could therefore be local to those boundary pairs.



\---



\## Conclusion



Experiment 029 demonstrates that cause-conditioned evidence aggregation can

transform weak trajectory-level evidence rules into highly separable

operating-condition statistics on the development population.



At



\\\[

n=50,

\\]



development accuracy reaches approximately



\\\[

100\\%

\\]



for all four mismatch mechanisms.



The resulting architecture is



\\\[

\\text{attribute cause}

\\rightarrow

\\text{accumulate cause-conditioned trajectory evidence}

\\rightarrow

\\hat p\_n^{(j)}

\\rightarrow

\\text{infer evidence sufficiency}.

\\]



\---



\## Next Research Direction



Experiment 030 must independently validate the frozen \\(n=50\\) aggregate rules

using:



\- new physical operating points,

\- new stochastic seeds,

\- unchanged Experiment 026 trajectory rules,

\- unchanged Experiment 029 aggregate thresholds.



No post-validation tuning is permitted.



The central question is



\\\[

\\boxed{

\\text{Does cause-conditioned evidence aggregation generalize beyond the

development boundary pairs?}

}

\\]



\---



\## Reproducibility



Development population:



`results/balanced\_evidence\_boundary\_sampling.csv`



Frozen trajectory rules:



`experiments/026\_cause\_conditioned\_evidence\_estimation.md`



Experiment:



`experiments/cause\_conditioned\_aggregated\_evidence.py`



Results:



`results/cause\_conditioned\_aggregated\_evidence.csv`

