\# Experiment 024 — Temporal Evidence Sufficiency



\## Objective



Determine whether temporal residual dynamics and adaptive-response behavior

contain information about causal evidence sufficiency that is absent from

static attribution-score geometry.



Experiment 023 demonstrated that the frozen score-geometry estimator



\\\[

\\hat e

=

\\mathbf{1}

\[

m \\ge 0.20

\\land

\\Delta s \\ge 1.00

]

\\]



generalized poorly to intermediate operating conditions.



The present experiment therefore investigates whether evidence sufficiency is

better reflected by the dynamical evolution of estimator disagreement and

adaptation.



\---



\## Methodological Correction



An initial implementation attempted to associate Experiment 023 validation

trajectories with temporal features generated in earlier experiments.



That construction was rejected because the temporal and adaptive-response

features did not originate from the same physical trajectories as the

validation classifications.



The generated dataset from that attempt was removed before interpretation.



The corrected experiment regenerated all 480 validation trajectories using the

same validation conditions and stochastic seeds as Experiment 023 and extracted

temporal and adaptive-response features directly from each corresponding

trajectory.



Thus each observation has the form



\\\[

e\_i

\\leftrightarrow

\\{

\\mathbf{s}\_i,

\\mathcal{T}\_i,

\\mathcal{A}\_i

\\},

\\]



where the score geometry, temporal residual structure, adaptive response, and

evidence label all correspond to the same realization.



\---



\## Validation Dataset



Eight intermediate operating points were evaluated with 60 stochastic

realizations per condition:



\\\[

8\\times60=480.

\\]



The evidence labels reproduced Experiment 023 exactly.



Seven operating points satisfied the empirical evidence-sufficiency criterion,

producing



\\\[

420

\\]



evidence-sufficient trajectories.



The process-disturbance operating point at magnitude 2.25 remained

evidence-insufficient, producing



\\\[

60

\\]



evidence-insufficient trajectories.



Its hard causal-classification accuracy was



\\\[

78.33\\%,

\\]



below the required detectability criterion.



\---



\## Candidate Evidence Features



The experiment evaluated static score geometry together with temporal and

adaptive-response features.



Static features included:



\\\[

m,

\\]



the classification margin, and



\\\[

\\Delta s,

\\]



the total attribution-score spread.



Temporal features included:



\\\[

\\Delta\\overline{\\mathrm{NIS}}\_{\\mathrm{event-pre}},

\\]



\\\[

\\Delta\\overline{\\mathrm{NIS}}\_{\\mathrm{post-pre}},

\\]



the event-to-post-event NIS recovery ratio,



\\\[

\\max(\\mathrm{NIS})\_{\\mathrm{event}},

\\]



post-event NIS persistence, and changes in lag-one innovation

autocorrelation.



Adaptive-response features included the post-event parameter shift and

cumulative absolute parameter adaptation.



\---



\## Standardized Separation



For feature \\(f\\), separation between sufficient and insufficient trajectories

was measured using



\\\[

D\_f

=

\\frac{

|\\mu\_{f,1}-\\mu\_{f,0}|

}{

\\sqrt{

(\\sigma\_{f,1}^{2}+\\sigma\_{f,0}^{2})/2

}

}.

\\]



Observed standardized separations were:



| Feature | Separation |

|---|---:|

| classification margin | 0.0655 |

| score spread | 0.3814 |

| event-vs-pre NIS change | 0.9462 |

| post-vs-pre NIS change | 0.0146 |

| NIS recovery ratio | 1.1185 |

| event maximum NIS | 0.9140 |

| post-event NIS persistence | 0.0620 |

| event-vs-pre autocorrelation change | 0.8841 |

| post-vs-pre autocorrelation change | 0.0075 |

| post-vs-pre parameter shift | 0.8567 |

| cumulative post-event parameter update | 1.3283 |



The strongest observed separator was cumulative post-event parameter

adaptation.



\---



\## Static Score Geometry



The classification margin exhibited almost no separation between the two

evidence regimes:



\\\[

D\_m=0.0655.

\\]



Total attribution-score spread remained weak:



\\\[

D\_{\\Delta s}=0.3814.

\\]



This independently reinforces the conclusion of Experiment 023 that static

classifier confidence is not a robust representation of causal

identifiability.



\---



\## Temporal Residual Structure



Several temporal features exhibited substantially stronger separation.



The mean event-to-pre-event NIS change was



\\\[

0.7362

\\]



for sufficient trajectories and



\\\[

1.7320

\\]



for insufficient trajectories.



The corresponding standardized separation was



\\\[

D=0.9462.

\\]



Event maximum NIS increased from a sufficient-regime mean of



\\\[

8.019

\\]



to an insufficient-regime mean of



\\\[

16.544,

\\]



with



\\\[

D=0.9140.

\\]



The event-to-pre-event change in innovation autocorrelation also separated the

groups:



\\\[

D=0.8841.

\\]



These results indicate that the temporal structure of disagreement contains

information not represented by the final causal-score margin.



\---



\## Recovery Dynamics



The NIS recovery ratio produced one of the strongest separations.



Evidence-sufficient trajectories had mean recovery ratio



\\\[

0.8115,

\\]



while evidence-insufficient trajectories had mean recovery ratio



\\\[

0.4134.

\\]



The standardized separation was



\\\[

\\boxed{

D\_{\\mathrm{recovery}}=1.1185.

}

\\]



Thus the evolution of inconsistency following an event appears more informative

about identifiability than instantaneous classifier confidence alone.



\---



\## Adaptive Response



The strongest feature in the experiment was cumulative post-event absolute

parameter adaptation.



Evidence-sufficient trajectories had mean cumulative adaptation



\\\[

0.08693,

\\]



while the evidence-insufficient regime had mean



\\\[

0.05761.

\\]



The standardized separation was



\\\[

\\boxed{

D\_{\\mathrm{adapt}}=1.3283.

}

\\]



The post-event parameter shift also showed substantial separation:



\\\[

D=0.8567.

\\]



This suggests that evidence sufficiency may depend not only on disagreement

between prediction and observation, but also on whether that disagreement

produces a coherent response in the adaptive model.



\---



\## Interpretation



The evidence-insufficient process-disturbance regime did not exhibit weak

prediction disagreement.



Instead, it produced stronger event inconsistency than the sufficient

population while producing a comparatively weaker cumulative adaptive

response.



This distinction motivates the hypothesis that



\\\[

\\text{evidence sufficiency}

\\neq

\\text{magnitude of disagreement}.

\\]



A more appropriate representation may be



\\\[

\\boxed{

e\_k

=

\\Psi(

\\mathbf{s}\_k,

\\mathcal{T}\_k,

\\mathcal{A}\_k

),

}

\\]



where evidence sufficiency depends jointly on causal-score geometry, temporal

residual structure, and adaptive response.



The digital twin may therefore need to evaluate not merely whether its

prediction is wrong, but whether the observed disagreement evolves in a manner

that supports discrimination among competing physical explanations.



\---



\## Limitation



The present validation set contains seven evidence-sufficient operating points

but only one evidence-insufficient operating point.



Consequently, the observed feature separations partly characterize the

specific dynamics of the process-disturbance 2.25 condition.



They cannot yet establish that temporal or adaptive-response features provide a

mechanism-independent estimator of evidence sufficiency.



Additional evidence-insufficient operating points from measurement-noise,

parameter-mismatch, and structural-change regimes are required before a new

evidence estimator should be constructed.



\---



\## Conclusion



Experiment 024 provides evidence that temporal residual dynamics and adaptive

response contain substantially more information about empirical causal

identifiability than static attribution-score geometry in the current

validation set.



The strongest observed features were



\\\[

\\boxed{

\\text{cumulative adaptive response}

}

\\]



and



\\\[

\\boxed{

\\text{NIS recovery dynamics}.

}

\\]



However, the experiment does not yet justify constructing a new universal

evidence-sufficiency rule.



The next step is to expand the evidence-insufficient population across causal

mechanisms and determine whether these dynamical signatures persist.



\---



\## Next Research Direction



The next experiment should deliberately sample operating points on both sides

of the detectability boundary for every mismatch mechanism.



This will test whether



\\\[

\\mathcal{T}\_k

\\]



and



\\\[

\\mathcal{A}\_k

\\]



encode evidence sufficiency itself or merely distinguish the current

process-disturbance boundary condition.



Only after that test should a second-generation evidence-sufficiency estimator

be constructed.



\---



\## Reproducibility



Experiment:



`experiments/temporal\_evidence\_sufficiency.py`



Results:



`results/temporal\_evidence\_sufficiency.csv`

