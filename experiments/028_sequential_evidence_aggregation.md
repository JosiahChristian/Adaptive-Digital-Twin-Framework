\# Experiment 028 — Sequential Evidence Aggregation



\## Objective



Determine whether the evidence-sufficiency signal identified in Experiment 027

becomes more statistically identifiable when information is aggregated across

multiple stochastic trajectories from the same operating condition.



Experiment 027 demonstrated that deterministic single-trajectory evidence

rules do not reliably recover an evidence-sufficiency property defined at the

operating-condition population level.



Experiment 028 therefore tests the revised hypothesis



\\\[

\\boxed{

\\text{evidence sufficiency becomes more identifiable through aggregation}.

}

\\]



\---



\## Data Source



Experiment 028 uses the frozen independent validation population generated in

Experiment 027:



`results/cause\_conditioned\_evidence\_validation.csv`



The dataset contains



\\\[

800

\\]



trajectories distributed across eight operating conditions.



No underlying simulations are rerun.



\---



\## Aggregated Evidence Statistic



For an operating condition, let the frozen Experiment 026 trajectory-level

evidence decision for realization \\(i\\) be



\\\[

\\hat e\_i\\in\\{0,1\\}.

\\]



For a batch containing \\(n\\) trajectories, define the aggregated evidence-vote

fraction



\\\[

\\boxed{

\\hat p\_n

=

\\frac{1}{n}

\\sum\_{i=1}^{n}\\hat e\_i.

}

\\]



The batch sizes investigated are



\\\[

n\\in\\{1,2,5,10,20,50\\}.

\\]



For every operating condition and batch size, 500 random without-replacement

subsamples are generated from the existing 100-trajectory validation

population.



\---



\## Hypothesis



If single-trajectory stochasticity is an important source of the Experiment

027 validation failure, increasing \\(n\\) should reduce the variability of



\\\[

\\hat p\_n.

\\]



More importantly, evidence-sufficient and evidence-insufficient operating

conditions should become increasingly distinguishable.



Standardized separation is measured as



\\\[

D\_n

=

\\frac{

|\\mu\_{1,n}-\\mu\_{0,n}|

}{

\\sqrt{

\\frac{

\\sigma\_{1,n}^{2}

\+

\\sigma\_{0,n}^{2}

}{2}

}

},

\\]



where the subscripts \\(1\\) and \\(0\\) denote evidence-sufficient and

evidence-insufficient operating conditions.



\---



\## Results



The aggregated distributions produced:



| Batch size | Sufficient mean | Sufficient std | Insufficient mean | Insufficient std | Separation |

|---:|---:|---:|---:|---:|---:|

| 1 | 0.6356 | 0.4814 | 0.4967 | 0.5002 | 0.2830 |

| 2 | 0.6192 | 0.3642 | 0.4653 | 0.3543 | 0.4282 |

| 5 | 0.6228 | 0.2771 | 0.4785 | 0.2212 | 0.5754 |

| 10 | 0.6237 | 0.2435 | 0.4693 | 0.1522 | 0.7603 |

| 20 | 0.6236 | 0.2215 | 0.4806 | 0.1008 | 0.8313 |

| 50 | 0.6247 | 0.2070 | 0.4801 | 0.0547 | 0.9554 |



Standardized separation therefore increased monotonically from



\\\[

D\_1=0.2830

\\]



to



\\\[

\\boxed{

D\_{50}=0.9554.

}

\\]



The result supports the hypothesis that aggregation reduces the uncertainty

associated with individual stochastic realizations.



\---



\## Condition-Level Behavior at n = 50



At



\\\[

n=50,

\\]



the aggregated vote fractions were:



| Condition | Evidence sufficient | Mean vote fraction | Std |

|---|---:|---:|---:|

| measurement\_noise\_0.90 | True | 0.3893 | 0.0486 |

| measurement\_noise\_0.95 | True | 0.5082 | 0.0540 |

| process\_disturbance\_2.65 | False | 0.4686 | 0.0495 |

| process\_disturbance\_2.85 | True | 0.5977 | 0.0475 |

| parameter\_mismatch\_0.425 | False | 0.4607 | 0.0510 |

| parameter\_mismatch\_0.385 | True | 0.6375 | 0.0512 |

| structural\_change\_0.87 | False | 0.5109 | 0.0497 |

| structural\_change\_0.86 | True | 0.9907 | 0.0100 |



\---



\## Cause Dependence



Although global separation improves substantially with aggregation, the

condition-level results show that a universal vote-fraction threshold is not

sufficient.



In particular,



\\\[

e(M\_{0.90})=1

\\]



while



\\\[

E\[\\hat p\_{50}]

\\approx0.389.

\\]



By contrast,



\\\[

e(S\_{0.87})=0

\\]



while



\\\[

E\[\\hat p\_{50}]

\\approx0.511.

\\]



Therefore an aggregated evidence statistic cannot be interpreted independently

of mismatch mechanism.



The appropriate formulation remains cause-conditioned:



\\\[

\\boxed{

P(

e=1

\\mid

\\mathcal I\_{1:n},

z=j

).

}

\\]



Thus cause conditioning is required not only for trajectory-level feature

construction but also for interpretation of accumulated evidence.



\---



\## Interpretation



Experiment 028 demonstrates two simultaneous effects.



First, aggregation reduces stochastic variability.



As the number of accumulated trajectories increases, the distribution of the

estimated vote fraction becomes increasingly concentrated.



Second, aggregation alone does not create a universal evidence scale.



Different mismatch mechanisms exhibit different mappings between accumulated

trajectory evidence and population-level evidence sufficiency.



The resulting architecture is therefore hierarchical:



\\\[

\\text{detect mismatch}

\\rightarrow

\\text{attribute cause}

\\rightarrow

\\text{accumulate cause-conditioned evidence}

\\rightarrow

\\text{estimate sufficiency}

\\rightarrow

\\text{adapt / wait / abstain}.

\\]



\---



\## Statistical Limitation



The 500 aggregation replicates at each batch size are not 500 independent

physical experiments.



They are repeated without-replacement subsamples from the same 100

Experiment 027 validation trajectories available for each operating

condition.



Experiment 028 therefore measures the statistical effect of aggregation

within the existing independent validation population.



It does not establish independent generalization of a newly constructed

aggregated evidence estimator.



A subsequent experiment must evaluate such an estimator using previously

unseen stochastic trajectories and operating conditions.



\---



\## Conclusion



Experiment 028 supports the hypothesis that evidence aggregation improves

statistical identifiability.



Standardized sufficient-versus-insufficient separation increased from



\\\[

0.2830

\\]



for individual trajectories to



\\\[

0.9554

\\]



for batches of 50 trajectories.



However, the condition-level results reject the hypothesis that one universal

aggregated vote threshold can represent evidence sufficiency.



Evidence accumulation must remain conditioned on the inferred mismatch cause.



The revised formulation is therefore



\\\[

\\boxed{

P(

e=1

\\mid

\\mathcal I\_{1:n},

z=j

).

}

\\]



\---



\## Next Research Direction



The next experiment should construct a cause-conditioned sequential evidence

estimator and evaluate how classification performance changes with accumulated

sample size.



The estimator should be developed without modifying the frozen Experiment 026

trajectory rules.



A subsequent independent experiment should then evaluate the resulting

aggregated estimator using new stochastic seeds and new operating points.



\---



\## Reproducibility



Input:



`results/cause\_conditioned\_evidence\_validation.csv`



Experiment:



`experiments/sequential\_evidence\_aggregation.py`



Results:



`results/sequential\_evidence\_aggregation.csv`

