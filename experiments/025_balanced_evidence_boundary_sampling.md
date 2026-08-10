\# Experiment 025 — Balanced Evidence Boundary Sampling



\## Objective



Determine whether temporal residual dynamics and adaptive-response features

provide mechanism-independent indicators of evidence sufficiency when

evidence-sufficient and evidence-insufficient operating points are balanced

across mismatch mechanisms.



Experiment 024 identified strong temporal and adaptive-response separation,

but its validation population contained only one evidence-insufficient

operating point.



Experiment 025 removes that limitation.



\---



\## Experimental Design



Four mismatch mechanisms were evaluated:



1\. measurement noise,

2\. process disturbance,

3\. parameter mismatch,

4\. structural change.



For each mechanism, one operating point below the empirical evidence boundary

and one above the boundary were selected.



Each operating point was evaluated over 100 previously unused stochastic

realizations.



Thus,



\\\[

8\\times100=800

\\]



trajectories were generated.



The empirical evidence-sufficiency criterion remained



\\\[

A\\ge0.90,

\\]



\\\[

C\\ge0.80,

\\]



and



\\\[

A\_{\\mathrm{sel}}\\ge0.95.

\\]



\---



\## Empirical Boundary Validation



The intended boundary design was reproduced exactly.



| Mechanism | Insufficient operating point | Sufficient operating point |

|---|---:|---:|

| measurement noise | 0.85 | 1.00 |

| process disturbance | 2.50 | 3.00 |

| parameter mismatch | 0.45 | 0.40 |

| structural change | 0.88 | 0.85 |



The resulting population contained



\\\[

\\boxed{400\\ e=0}

\\]



and



\\\[

\\boxed{400\\ e=1}.

\\]



Therefore the experiment achieved both numerical balance and

mechanism-level balance.



\---



\## Operating-Point Results



\### Measurement Noise



At measurement-noise level 0.85,



\\\[

A=93\\%,

\\qquad

C=72\\%,

\\qquad

A\_{\\mathrm{sel}}=100\\%.

\\]



The operating point was therefore evidence-insufficient because coverage

remained below the required threshold.



At measurement-noise level 1.00,



\\\[

A=97\\%,

\\qquad

C=91\\%,

\\qquad

A\_{\\mathrm{sel}}=100\\%.

\\]



This operating point was evidence-sufficient.



\### Process Disturbance



At disturbance magnitude 2.50,



\\\[

A=86\\%,

\\qquad

C=76\\%,

\\qquad

A\_{\\mathrm{sel}}=94.737\\%.

\\]



The operating point was evidence-insufficient.



At disturbance magnitude 3.00,



\\\[

A=97\\%,

\\qquad

C=93\\%,

\\qquad

A\_{\\mathrm{sel}}=100\\%.

\\]



The operating point was evidence-sufficient.



\### Parameter Mismatch



At initial parameter estimate 0.45,



\\\[

A=84\\%,

\\qquad

C=64\\%,

\\qquad

A\_{\\mathrm{sel}}=100\\%.

\\]



The operating point was evidence-insufficient.



At initial parameter estimate 0.40,



\\\[

A=96\\%,

\\qquad

C=83\\%,

\\qquad

A\_{\\mathrm{sel}}=100\\%.

\\]



The operating point was evidence-sufficient.



\### Structural Change



At changed parameter value 0.88,



\\\[

A=73\\%,

\\qquad

C=56\\%,

\\qquad

A\_{\\mathrm{sel}}=82.143\\%.

\\]



The operating point was evidence-insufficient.



At changed parameter value 0.85,



\\\[

A=94\\%,

\\qquad

C=91\\%,

\\qquad

A\_{\\mathrm{sel}}=97.802\\%.

\\]



The operating point was evidence-sufficient.



\---



\## Global Feature Separation



Across the balanced 800-trajectory population, standardized separation was:



| Feature | Separation |

|---|---:|

| classification margin | 0.5089 |

| score spread | 0.3917 |

| event-vs-pre NIS change | 0.2676 |

| post-vs-pre NIS change | 0.0187 |

| NIS recovery ratio | 0.1129 |

| event maximum NIS | 0.2319 |

| post-event NIS persistence | 0.0093 |

| event-vs-pre autocorrelation change | 0.0693 |

| post-vs-pre autocorrelation change | 0.0213 |

| parameter shift | 0.2845 |

| cumulative parameter adaptation | 0.3491 |



No temporal or adaptive-response scalar produced strong universal separation.



The classification margin produced the largest global separation,



\\\[

D=0.5089,

\\]



but remained only moderately discriminative.



\---



\## Reassessment of Experiment 024



Experiment 024 reported strong separation for NIS recovery and cumulative

adaptive response:



\\\[

D\_{\\mathrm{recovery}}=1.1185,

\\]



and



\\\[

D\_{\\mathrm{adapt}}=1.3283.

\\]



Under balanced mechanism-level sampling these decreased to



\\\[

D\_{\\mathrm{recovery}}=0.1129,

\\]



and



\\\[

D\_{\\mathrm{adapt}}=0.3491.

\\]



Therefore those Experiment 024 effects cannot be interpreted as universal

evidence-sufficiency signatures.



They were substantially influenced by the mechanism composition of the

evidence-insufficient population.



\---



\## Within-Mechanism Evidence Structure



Although universal separation was weak, substantial within-mechanism

separation remained.



\### Measurement Noise



The strongest features were



\\\[

D\_{\\mathrm{adapt}}=0.8900,

\\]



\\\[

D\_{\\mathrm{spread}}=0.8817,

\\]



and



\\\[

D\_{\\mathrm{margin}}=0.8513.

\\]



Thus measurement-noise evidence sufficiency is associated with both

attribution-score geometry and adaptive-response magnitude.



\### Process Disturbance



The strongest features were



\\\[

D\_{\\max NIS}=0.6675,

\\]



\\\[

D\_{\\mathrm{margin}}=0.6566,

\\]



\\\[

D\_{\\mathrm{spread}}=0.6554,

\\]



\\\[

D\_{\\Delta NIS}=0.6516,

\\]



and



\\\[

D\_{\\mathrm{recovery}}=0.5263.

\\]



Process-disturbance evidence therefore appears strongly related to the

magnitude and recovery structure of the event response.



\### Parameter Mismatch



The dominant features were



\\\[

D\_{\\mathrm{margin}}=0.7605

\\]



and



\\\[

D\_{\\mathrm{spread}}=0.7297.

\\]



Temporal residual and parameter-response features were nearly

non-discriminative at this boundary.



Thus parameter-mismatch evidence sufficiency is represented primarily by

attribution-score geometry in the present architecture.



\### Structural Change



Structural change exhibited the strongest mechanism-specific signature.



The post-vs-pre parameter shift produced



\\\[

\\boxed{

D\_{\\Delta\\hat a}=7.1075

}

\\]



while



\\\[

D\_{\\mathrm{spread}}=1.9736,

\\]



\\\[

D\_{\\mathrm{margin}}=1.6543,

\\]



\\\[

D\_{\\mathrm{adapt}}=1.1026,

\\]



and



\\\[

D\_{\\Delta NIS}=1.0888.

\\]



The extremely large parameter-shift separation indicates that adaptive

parameter dynamics are highly informative about structural-change

detectability near the tested boundary.



This result is mechanism-specific and should not be interpreted as a

universal evidence statistic.



\---



\## Multiple Forms of Evidence Insufficiency



The balanced experiment also demonstrates that evidence insufficiency does not

have a single failure mode.



For measurement noise, hard classification and selective accuracy were high,

but coverage was insufficient.



For parameter mismatch, selective predictions were perfectly accurate, but

hard accuracy and coverage were insufficient.



For process disturbance, all three quantities approached but failed the

required operating criterion.



For structural change, hard accuracy, coverage, and selective accuracy all

degraded substantially.



Thus



\\\[

e=0

\\]



represents multiple forms of insufficient causal evidence rather than one

homogeneous statistical state.



\---



\## Interpretation



The results reject the hypothesis that one scalar temporal or adaptive feature

provides a mechanism-independent measure of evidence sufficiency.



Instead, the evidence signature depends strongly on the hypothesized mismatch

mechanism.



This motivates a conditional formulation:



\\\[

\\boxed{

P(e\_k=1\\mid z\_k=j,\\mathcal I\_k)

=

\\Psi\_j(

\\mathbf{s}\_k,

\\mathcal{T}\_k,

\\mathcal{A}\_k

)

}

\\]



where



\\\[

z\_k

\\]



denotes the hypothesized causal mismatch mechanism,



\\\[

\\mathbf{s}\_k

\\]



denotes attribution-score geometry,



\\\[

\\mathcal{T}\_k

\\]



denotes temporal residual structure, and



\\\[

\\mathcal{A}\_k

\\]



denotes adaptive-response behavior.



Under this formulation, evidence sufficiency is evaluated conditionally on the

candidate causal explanation rather than independently of it.



\---



\## Architectural Implication



The adaptive digital twin should not treat causal attribution and evidence

sufficiency as independent modules.



A more appropriate inference sequence is



\\\[

\\text{observe}

\\rightarrow

\\text{detect disagreement}

\\rightarrow

\\text{generate causal attribution}

\\rightarrow

\\text{evaluate cause-conditioned evidence}

\\rightarrow

\\text{adapt or abstain}.

\\]



The relevant evidence test may differ according to the proposed cause.



For example:



\- measurement-noise attribution may depend strongly on score confidence and

&#x20; adaptive-response magnitude,

\- process-disturbance attribution may depend on transient NIS dynamics,

\- parameter-mismatch attribution may depend primarily on attribution-score

&#x20; geometry,

\- structural-change attribution may depend strongly on coherent parameter

&#x20; evolution.



\---



\## Conclusion



Experiment 025 resolves the principal limitation of Experiment 024 by

constructing a perfectly balanced evidence-boundary population across all four

mismatch mechanisms.



The results show that the strong global temporal signatures observed in

Experiment 024 do not generalize as universal evidence-sufficiency indicators.



However, strong and interpretable mechanism-specific evidence signatures do

exist.



The central result is therefore



\\\[

\\boxed{

\\text{evidence sufficiency is cause-conditioned}.

}

\\]



This suggests that the next generation of the adaptive digital twin should

estimate not merely



\\\[

P(z\_k=j),

\\]



but jointly reason about



\\\[

P(z\_k=j,e\_k=1\\mid\\mathcal I\_k).

\\]



\---



\## Next Research Direction



The next experiment should construct and freeze mechanism-specific

evidence-sufficiency estimators



\\\[

\\Psi\_j

\\]



using the balanced Experiment 025 development population.



Those estimators should then be evaluated on entirely new intermediate

operating points and stochastic seeds.



This will test whether cause-conditioned evidence estimation generalizes

beyond the boundary pairs from which it was derived.



\---



\## Reproducibility



Experiment:



`experiments/balanced\_evidence\_boundary\_sampling.py`



Results:



`results/balanced\_evidence\_boundary\_sampling.csv`

