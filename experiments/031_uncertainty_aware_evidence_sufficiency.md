\# Experiment 031 — Uncertainty-Aware Evidence Sufficiency



\## Objective



Determine whether the binary evidence-sufficiency label used in previous

experiments is itself statistically stable when estimated from finite

stochastic populations.



Previous experiments defined evidence sufficiency as



\\\[

e(c)

=

\\mathbf 1\[

\\widehat A(c)\\ge0.90

\\land

\\widehat C(c)\\ge0.80

\\land

\\widehat A\_{\\mathrm{sel}}(c)\\ge0.95

].

\\]



However, each quantity is estimated from a finite population of stochastic

trajectories.



Experiment 031 therefore treats the evidence label itself as uncertain.



\---



\## Uncertainty-Aware Formulation



For operating condition \\(c\\) and population size \\(N\\), define



\\\[

\\boxed{

q(c;N)

=

P\\left(

\\widehat A\\ge0.90,

\\widehat C\\ge0.80,

\\widehat A\_{\\mathrm{sel}}\\ge0.95

\\mid

c,N

\\right).

}

\\]



In the present experiment,



\\\[

N=100.

\\]



The quantity \\(q(c;100)\\) represents the probability that an independently

generated 100-trajectory population satisfies the original evidence criterion.



Thus evidence sufficiency is no longer assumed to be intrinsically Boolean.



\---



\## Experimental Design



The eight independent operating conditions from Experiment 030 were reused.



For each operating condition:



\- 100 independent stochastic populations were generated,

\- each population contained 100 trajectories,

\- the original causal classifier remained unchanged,

\- the confidence threshold remained unchanged,

\- the original 90/80/95 evidence criterion remained unchanged.



The experiment therefore generated



\\\[

8\\times100\\times100

=

80,000

\\]



new trajectories.



The output contains



\\\[

800

\\]



independent population-level records.



\---



\## Evidence-Sufficiency Probabilities



Observed criterion-pass probabilities were:



| Condition | \\(q(c)\\) |

|---|---:|

| measurement noise 0.875 | 0.48 |

| measurement noise 0.975 | 1.00 |

| process disturbance 2.60 | 0.26 |

| process disturbance 2.90 | 0.91 |

| parameter mismatch 0.435 | 0.00 |

| parameter mismatch 0.395 | 0.68 |

| structural change 0.875 | 0.00 |

| structural change 0.855 | 0.82 |



The experiment therefore identifies robustly insufficient, robustly

sufficient, and boundary-uncertain operating conditions.



\---



\## Measurement-Noise Boundary



For measurement noise 0.875,



\\\[

q=0.48.

\\]



Across independent populations,



\\\[

E\[\\widehat A]=0.931,

\\]



\\\[

E\[\\widehat C]=0.789,

\\]



and



\\\[

E\[\\widehat A\_{\\mathrm{sel}}]=0.988.

\\]



The condition therefore lies extremely close to the operational evidence

boundary.



The criterion failure probabilities were



\\\[

P(\\widehat A<0.90)=0.10,

\\]



\\\[

P(\\widehat C<0.80)=0.51,

\\]



and



\\\[

P(\\widehat A\_{\\mathrm{sel}}<0.95)=0.02.

\\]



Coverage is therefore the dominant source of evidence-label uncertainty.



\---



\## Process-Disturbance Boundary



For process disturbance 2.60,



\\\[

q=0.26.

\\]



Mean operating statistics were



\\\[

E\[\\widehat A]=0.876,

\\]



\\\[

E\[\\widehat C]=0.809,

\\]



and



\\\[

E\[\\widehat A\_{\\mathrm{sel}}]=0.970.

\\]



Failure probabilities were



\\\[

P(\\widehat A<0.90)=0.72,

\\]



\\\[

P(\\widehat C<0.80)=0.39,

\\]



and



\\\[

P(\\widehat A\_{\\mathrm{sel}}<0.95)=0.11.

\\]



Thus hard causal-attribution accuracy is the dominant source of boundary

instability for this condition.



The single Experiment 030 population happened to satisfy the binary criterion,

but repeated-population analysis shows that most independently generated

populations do not.



\---



\## Parameter-Mismatch Boundary



For initial parameter estimate 0.395,



\\\[

q=0.68.

\\]



Mean statistics were



\\\[

E\[\\widehat A]=0.940,

\\]



\\\[

E\[\\widehat C]=0.809,

\\]



and



\\\[

E\[\\widehat A\_{\\mathrm{sel}}]=0.995.

\\]



Failure probabilities were



\\\[

P(\\widehat A<0.90)=0.01,

\\]



\\\[

P(\\widehat C<0.80)=0.32,

\\]



and



\\\[

P(\\widehat A\_{\\mathrm{sel}}<0.95)=0.

\\]



Thus this condition is more accurately described as evidence-sufficient

leaning but boundary uncertain than as deterministically insufficient.



Its `False` label in Experiment 030 reflected one finite stochastic population

rather than a stable population property.



\---



\## Robustly Insufficient Conditions



Parameter mismatch 0.435 produced



\\\[

q=0.

\\]



Structural change 0.875 also produced



\\\[

q=0.

\\]



These operating conditions remain evidence-insufficient across all 100

independently generated populations.



They therefore provide robust insufficient-evidence controls.



\---



\## Robustly Sufficient Conditions



Measurement noise 0.975 produced



\\\[

q=1.

\\]



Process disturbance 2.90 produced



\\\[

q=0.91,

\\]



and structural change 0.855 produced



\\\[

q=0.82.

\\]



These conditions exhibit substantially more stable evidence sufficiency than

the boundary conditions.



\---



\## Failure-Mode Heterogeneity



Evidence-boundary uncertainty is not generated by the same statistic for every

mismatch mechanism.



Measurement-noise uncertainty is dominated by selective coverage.



Process-disturbance uncertainty is dominated by hard causal-attribution

accuracy.



Parameter-mismatch uncertainty near the tested boundary is again dominated by

coverage.



Structural-change insufficiency at 0.875 reflects simultaneous degradation of

hard accuracy, coverage, and selective accuracy.



Therefore



\\\[

\\boxed{

\\text{evidence uncertainty is cause-conditioned}.

}

\\]



\---



\## Interpretation of Experiment 030



Experiment 030 evaluated aggregated evidence against one binary evidence label

generated from one 100-trajectory population per operating condition.



Experiment 031 demonstrates that several such labels are intrinsically

unstable under repeated stochastic sampling.



For example, parameter mismatch 0.395 received a binary `False` label in

Experiment 030 but satisfies the identical criterion in



\\\[

68\\%

\\]



of independently generated populations.



Similarly, process disturbance 2.60 received a binary `True` label in

Experiment 030 but satisfies the criterion in only



\\\[

26\\%

\\]



of independently generated populations.



Consequently, part of the apparent Experiment 030 prediction error was

actually uncertainty in the evaluation target.



\---



\## Revised Evidence Representation



The internal evidence state should therefore be represented probabilistically:



\\\[

\\boxed{

q(c;N)

=

P(

e=1

\\mid

c,N

).

}

\\]



A downstream decision may still threshold \\(q\\), but the underlying digital

twin should preserve uncertainty rather than immediately collapsing it into a

Boolean state.



This introduces at least three meaningful epistemic regimes:



\\\[

q\\approx0:

\\quad

\\text{robustly insufficient},

\\]



\\\[

0<q<1:

\\quad

\\text{boundary uncertain},

\\]



and



\\\[

q\\approx1:

\\quad

\\text{robustly sufficient}.

\\]



\---



\## Statistical Limitation



The preliminary confidence intervals reported during exploratory analysis used

a normal approximation to the binomial proportion.



This approximation is inadequate near



\\\[

q=0

\\]



and



\\\[

q=1.

\\]



Future publication-quality analysis should use Wilson-score or exact binomial

intervals.



This limitation does not alter the estimated criterion-pass frequencies or the

primary qualitative conclusions.



\---



\## Conclusion



Experiment 031 directly demonstrates that evidence sufficiency is not

appropriately represented as a deterministic binary ground-truth label near

detectability boundaries.



Several operating conditions exhibit substantial criterion-pass uncertainty

across independently generated stochastic populations.



The central result is



\\\[

\\boxed{

\\text{evidence sufficiency is itself uncertain}.

}

\\]



The appropriate statistical object is therefore not merely



\\\[

e\\in\\{0,1\\},

\\]



but



\\\[

\\boxed{

q(c;N)

=

P(

e=1

\\mid

c,N

).

}

\\]



This resolves several apparent inconsistencies observed during independent

aggregate validation and establishes the next stage of the adaptive

digital-twin evidence architecture.



\---



\## Next Research Direction



The next experiment should map



\\\[

q(c;N)

\\]



as a continuous function of mismatch magnitude for each causal mechanism.



Rather than estimating evidence uncertainty at only two operating points per

cause, a dense magnitude sweep can reveal the shape and width of each

probabilistic detectability transition.



This would replace the earlier deterministic detectability boundary



\\\[

\\delta\_j^\*

\\]



with an uncertainty-aware detectability curve



\\\[

\\boxed{

q\_j(\\delta;N).

}

\\]



\---



\## Reproducibility



Experiment:



`experiments/uncertainty\_aware\_evidence\_sufficiency.py`



Results:



`results/uncertainty\_aware\_evidence\_sufficiency.csv`

