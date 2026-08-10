\# Experiment 023 — Independent Evidence-Sufficiency Validation



\## Objective



Evaluate the frozen evidence-sufficiency estimator developed in Experiment 022

using new stochastic realizations and operating points that were not used for

threshold selection.



The candidate estimator was frozen as



\\\[

\\hat e

=

\\mathbf{1}

\[

m \\ge 0.20

\\land

\\Delta s \\ge 1.00

],

\\]



where \\(m\\) is the attribution classification margin and \\(\\Delta s\\) is the

total attribution-score spread.



No estimator thresholds were modified during validation.



\---



\## Validation Design



Eight intermediate operating points were evaluated across the four mismatch

mechanisms.



Each operating point was simulated using 60 new stochastic realizations,

producing



\\\[

8 \\times 60 = 480

\\]



independent validation trajectories.



Evidence-sufficiency ground truth was determined independently at the

operating-point level using the empirical detectability criterion



\\\[

A \\ge 0.90,

\\]



\\\[

C \\ge 0.80,

\\]



and



\\\[

A^{\\mathrm{sel}} \\ge 0.95.

\\]



Thus the evidence estimator was evaluated against empirical causal

identifiability rather than individual classification correctness.



\---



\## Aggregate Results



The frozen estimator achieved



\\\[

350/480

\\]



correct evidence-sufficiency predictions, corresponding to



\\\[

\\boxed{72.917\\%}

\\]



accuracy.



Precision was



\\\[

\\boxed{89.402\\%},

\\]



while recall was



\\\[

\\boxed{78.333\\%}.

\\]



The confusion counts were



\\\[

TP=329,

\\qquad

TN=21,

\\qquad

FP=39,

\\qquad

FN=91.

\\]



The estimator therefore remained relatively reliable when declaring evidence

sufficient, but rejected a substantial fraction of trajectories belonging to

empirically identifiable operating regimes.



\---



\## Condition-Level Results



| Condition | Evidence label | Predicted sufficient | Evidence accuracy | Classification accuracy |

|---|---:|---:|---:|---:|

| measurement noise 0.90 | True | 53.333% | 53.333% | 95.000% |

| measurement noise 1.10 | True | 88.333% | 88.333% | 96.667% |

| process disturbance 2.25 | False | 65.000% | 35.000% | 78.333% |

| process disturbance 2.75 | True | 90.000% | 90.000% | 93.333% |

| parameter mismatch 0.375 | True | 65.000% | 65.000% | 95.000% |

| parameter mismatch 0.325 | True | 85.000% | 85.000% | 100.000% |

| structural change 0.865 | True | 70.000% | 70.000% | 91.667% |

| structural change 0.845 | True | 96.667% | 96.667% | 100.000% |



The degradation was therefore not isolated to a single causal mechanism.



Instead, estimator performance deteriorated primarily near empirical

detectability boundaries.



\---



\## Critical Counterexample



The process-disturbance operating point at magnitude 2.25 provides the clearest

counterexample to a score-geometry-only evidence estimator.



This operating point failed the empirical evidence-sufficiency criterion and

was therefore labeled



\\\[

e=0.

\\]



Nevertheless, the frozen estimator declared sufficient evidence for



\\\[

65\\%

\\]



of its trajectories.



Its mean classification margin was



\\\[

m=1.141,

\\]



and its mean total score spread was



\\\[

\\Delta s=2.566.

\\]



Both values lie substantially above the frozen estimator thresholds.



Therefore,



\\\[

m\\ge0.20

\\]



and



\\\[

\\Delta s\\ge1.00

\\]



can simultaneously hold even when the underlying operating regime is not

empirically identifiable.



This demonstrates that strong internal separation among causal scores does not

necessarily imply that sufficient physical evidence exists to justify the

causal decision.



\---



\## Interpretation



Experiment 022 established that evidence sufficiency leaves a statistical

signature in attribution-score geometry.



Experiment 023 demonstrates that this signature is not sufficient for robust

generalization.



In particular,



\\\[

\\boxed{

\\text{attribution confidence}

\\neq

\\text{causal identifiability}

}

\\]



and



\\\[

\\boxed{

\\text{score separation}

\\not\\Rightarrow

\\text{evidence sufficiency}.

}

\\]



A causal classifier can exhibit a strong internal preference even when the

underlying observations do not support reliable discrimination among physical

mismatch mechanisms.



This is especially important near detectability boundaries.



\---



\## Architectural Consequence



Evidence sufficiency should not be modeled solely as a static function of

attribution-score geometry.



Instead, the results motivate a broader representation



\\\[

e\_k

=

\\Psi(

\\mathbf{s}\_k,

\\mathcal{T}\_k,

\\mathcal{A}\_k

),

\\]



where



\\\[

\\mathbf{s}\_k

\\]



represents causal-attribution score geometry,



\\\[

\\mathcal{T}\_k

\\]



represents temporal residual structure, and



\\\[

\\mathcal{A}\_k

\\]



represents the observed adaptive response of the digital twin.



Candidate temporal evidence includes normalized innovation evolution,

persistence, autocorrelation, event-to-post-event recovery, and related

residual statistics.



Candidate adaptive-response evidence includes parameter-update magnitude,

parameter trajectory, adaptation strength, and effective uncertainty response.



\---



\## Conclusion



The frozen score-geometry evidence estimator did not generalize sufficiently

to independent operating points.



Its validation accuracy decreased from the exploratory



\\\[

88.33\\%

\\]



to



\\\[

72.92\\%.

\\]



This result is retained rather than corrected through post-validation threshold

tuning.



The experiment therefore falsifies the stronger hypothesis that classification

margin and attribution-score spread alone provide a robust estimator of causal

evidence sufficiency.



At the same time, it supports a more general hypothesis:



\\\[

\\boxed{

\\text{causal identifiability is a dynamical property of accumulated evidence,

not merely a property of instantaneous classifier confidence.}

}

\\]



\---



\## Next Research Direction



The next experiment will investigate whether temporal residual structure and

adaptive-response dynamics provide information about evidence sufficiency that

is absent from attribution-score geometry.



The objective is not to retune the failed estimator.



The objective is to determine what additional observable information is

required for the digital twin to recognize the limits of its own causal

inference.



\---



\## Reproducibility



Experiment:



`experiments/evidence\_sufficiency\_validation.py`



Results:



`results/evidence\_sufficiency\_validation.csv`

