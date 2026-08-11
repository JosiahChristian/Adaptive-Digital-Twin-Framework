\# Experiment 039 — Online Epistemic-State Inference



\## Objective



Determine whether epistemic failure-state probabilities can be estimated

progressively from sequentially accumulated finite evidence without using the

reference failure-state distribution as an input to inference.



Experiment 035 established finite-batch probabilistic failure-state estimation.

Experiment 038 demonstrated that failure-state information can control the

recursive estimator without suppressing parameter recovery.



Experiment 039 bridges these results by converting finite-batch epistemic

estimation into sequential evidence accumulation.



\## Hypothesis



As the amount of observed evidence increases, the estimated marginal and joint

epistemic-state distributions should converge toward the complete

condition-level reference distributions.



For evidence budget \\(n\\),



\\\[

\\hat{\\mathbf p}\_{F,n}

=

\\begin{bmatrix}

\\hat P(F\_A) \\\\

\\hat P(F\_C) \\\\

\\hat P(F\_S)

\\end{bmatrix}

\\]



and



\\\[

\\hat{\\boldsymbol{\\pi}}\_n

\\]



denote the marginal and joint failure-state estimates.



The expected relationship is



\\\[

E\_5 > E\_{10} > E\_{20},

\\]



where \\(E\_n\\) denotes estimation error after \\(n\\) observations.



\## Method



Criterion-failure observations from Experiment 033 were grouped by operating

condition.



For each condition, the complete condition population was used only to define

the reference distribution for evaluation.



For each of 500 sequence replicates, the condition population was randomly

ordered and progressively observed at evidence budgets



\\\[

n \\in \\{5,10,20\\}.

\\]



The epistemic estimator received only the observations available within the

current evidence prefix.



Marginal estimates were



\\\[

\\hat P(F\_A)

=

\\frac{1}{n}

\\sum\_{i=1}^{n}

\\mathbf{1}(F\_{A,i}),

\\]



with analogous definitions for \\(F\_C\\) and \\(F\_S\\).



The joint epistemic state was represented over eight mutually exclusive modes:



\- pass all criteria,

\- accuracy failure only,

\- coverage failure only,

\- selective-accuracy failure only,

\- accuracy and coverage failure,

\- accuracy and selective-accuracy failure,

\- coverage and selective-accuracy failure,

\- failure of all three criteria.



Estimation quality was measured using:



1\. marginal mean absolute error,

2\. joint total-variation distance,

3\. joint Jensen-Shannon divergence.



The reference distribution was used exclusively for evaluation and did not

enter the epistemic estimator.



Across 17 operating conditions, 500 sequence replicates, and three evidence

budgets, the experiment generated



\\\[

17 \\times 500 \\times 3

=

25{,}500

\\]



evaluation records.



\## Results



\### Aggregate convergence



| Evidence budget | Marginal MAE | Joint TV | Joint JS |

|---:|---:|---:|---:|

| 5 | 0.0813 | 0.1944 | 0.0969 |

| 10 | 0.0555 | 0.1342 | 0.0520 |

| 20 | 0.0336 | 0.0815 | 0.0220 |



All three estimation-error measures decreased monotonically as evidence

accumulated.



Therefore,



\\\[

E\_5 > E\_{10} > E\_{20}.

\\]



\### Cause-conditioned convergence



Marginal MAE decreased monotonically for every mismatch mechanism.



Measurement noise:



\\\[

0.0684

\\rightarrow

0.0500

\\rightarrow

0.0309.

\\]



Parameter mismatch:



\\\[

0.0489

\\rightarrow

0.0337

\\rightarrow

0.0214.

\\]



Process disturbance:



\\\[

0.1085

\\rightarrow

0.0740

\\rightarrow

0.0439.

\\]



Structural change:



\\\[

0.0813

\\rightarrow

0.0537

\\rightarrow

0.0324.

\\]



Process disturbance remained the most difficult epistemic state to estimate,

while parameter mismatch produced the smallest estimation error.



Nevertheless, every mismatch mechanism exhibited convergence with increasing

evidence.



\## Comparison with Finite-Batch Estimation



Experiment 035 produced aggregate errors:



| Evidence | Marginal MAE | Joint TV | Joint JS |

|---:|---:|---:|---:|

| 5 | 0.0814 | 0.1936 | 0.0961 |

| 10 | 0.0550 | 0.1333 | 0.0513 |

| 20 | 0.0336 | 0.0822 | 0.0224 |



Experiment 039 produced:



| Evidence | Marginal MAE | Joint TV | Joint JS |

|---:|---:|---:|---:|

| 5 | 0.0813 | 0.1944 | 0.0969 |

| 10 | 0.0555 | 0.1342 | 0.0520 |

| 20 | 0.0336 | 0.0815 | 0.0220 |



The near-equivalence of these results indicates that the validated finite-batch

epistemic estimator retains its convergence behavior when expressed as

progressively accumulated sequential evidence.



\## Interpretation



Experiment 039 establishes the intermediate mapping



\\\[

D\_{1:n}

\\rightarrow

\\hat{\\boldsymbol{\\pi}}\_n.

\\]



The adaptive system no longer requires the complete reference epistemic

distribution in order to construct its current failure-state estimate.



Instead, uncertainty about epistemic state decreases naturally as evidence

accumulates.



This provides the inference component required for a closed-loop architecture

of the form



\\\[

D\_{1:n}

\\rightarrow

\\hat{\\boldsymbol{\\pi}}\_n

\\rightarrow

u\_n^{\\mathrm{epistemic}}

\\rightarrow

\\text{adaptive estimator}.

\\]



\## Limitation



The sequential observations in this experiment are population-level criterion

failure observations presented in randomized order.



Consequently, the experiment demonstrates sequential finite-evidence epistemic

inference, but does not yet establish single-trajectory real-time inference

directly from the evolving physical-system measurements.



The distinction is important: the estimator is online with respect to evidence

availability, but the evidence units themselves remain population-level

observations.



\## Conclusion



Sequential accumulation of finite evidence produced increasingly accurate

estimates of both marginal and joint epistemic failure-state distributions.



Marginal MAE decreased from



\\\[

0.0813

\\rightarrow

0.0555

\\rightarrow

0.0336,

\\]



while joint total variation decreased from



\\\[

0.1944

\\rightarrow

0.1342

\\rightarrow

0.0815.

\\]



Jensen-Shannon divergence decreased simultaneously from



\\\[

0.0969

\\rightarrow

0.0520

\\rightarrow

0.0220.

\\]



The convergence occurred across every tested mismatch mechanism and closely

matched the finite-batch behavior observed in Experiment 035.



Experiment 039 therefore validates sequential epistemic-state inference as the

bridge between probabilistic failure-state estimation and online

failure-conditioned adaptive control.

