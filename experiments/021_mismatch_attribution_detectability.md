\# Experiment 021 — Mismatch Attribution Detectability Boundary



\## Objective



Characterize how mismatch-attribution performance changes as the magnitude of

physical mismatch varies from weak, near-nominal conditions to strongly

identifiable conditions.



The attribution architecture and confidence threshold developed previously were

held fixed throughout the experiment.



No classifier weights or confidence thresholds were retuned during the sweep.



The confidence threshold remained



\\\[

\\tau = 0.30.

\\]



\---



\## Experimental Design



Four mismatch mechanisms were investigated:



1\. measurement noise,

2\. process disturbance,

3\. parameter mismatch,

4\. structural change.



For each mechanism, mismatch magnitude was systematically varied while all

attribution rules remained frozen.



Fifty stochastic realizations were evaluated at every operating point.



The experiment contained 26 operating points and therefore



\\\[

26 \\times 50 = 1300

\\]



simulated trajectories.



\---



\## Performance Measures



For mismatch class \\(j\\) and mismatch strength \\(\\delta\\), define hard

attribution accuracy as



\\\[

A\_j(\\delta)

=

P(\\hat z=j \\mid z=j,\\delta).

\\]



Selective coverage is



\\\[

C\_j(\\delta)

=

P(m\\ge\\tau \\mid z=j,\\delta),

\\]



where \\(m\\) denotes classification margin and



\\\[

\\tau=0.30.

\\]



Accuracy among accepted diagnoses is



\\\[

A\_j^{\\mathrm{sel}}(\\delta)

=

P(

\\hat z=j

\\mid

z=j,

m\\ge\\tau,

\\delta

).

\\]



The mean classification margin



\\\[

\\bar m\_j(\\delta)

\\]



was also recorded as a measure of diagnostic separation.



\---



\## Measurement-Noise Sweep



Measurement-noise standard deviation was varied over



\\\[

0.55,\\,

0.65,\\,

0.75,\\,

0.85,\\,

1.00,\\,

1.25,\\,

1.50.

\\]



Observed hard accuracy increased as



\\\[

50\\%,

62\\%,

80\\%,

92\\%,

94\\%,

98\\%,

98\\%.

\\]



Coverage increased from 24% at the weakest tested condition to 98% at the

strongest conditions.



Mean classification margin increased from approximately



\\\[

0.22

\\]



to



\\\[

1.53.

\\]



Thus stronger measurement-noise mismatch produced increasingly separable

diagnostic evidence.



\---



\## Process-Disturbance Sweep



Process-disturbance magnitude was varied over



\\\[

0.5,\\,

1.0,\\,

1.5,\\,

2.0,\\,

2.5,\\,

3.0,\\,

4.0.

\\]



Hard attribution accuracy was



\\\[

6\\%,

16\\%,

40\\%,

74\\%,

86\\%,

92\\%,

100\\%.

\\]



The corresponding mean classification margin increased from approximately



\\\[

0.22

\\]



at disturbance magnitude 0.5 to



\\\[

4.89

\\]



at magnitude 4.0.



This is the clearest detectability transition observed in the experiment.



At weak disturbance strengths, the residual response is insufficiently

distinctive for reliable causal attribution.



At stronger disturbance magnitudes, the diagnostic signature becomes highly

separable.



\---



\## Weak-Signal Confidence Failure



Confidence-aware abstention is useful only after the mismatch enters a region

where classification margin is meaningfully associated with correctness.



For process disturbance,



\\\[

d=0.5

\\]



produced only approximately 7.14% accuracy among accepted diagnoses.



At



\\\[

d=1.0,

\\]



accepted-case accuracy was 0%.



Therefore, confidence margin alone does not guarantee reliable attribution

outside the identifiable operating region.



A classifier may be confidently incorrect when the causal signal is too weak

relative to stochastic variation.



This motivates distinguishing between confidence and identifiability.



\---



\## Parameter-Mismatch Sweep



Parameter mismatch was represented by



\\\[

\\delta\_\\theta

=

|a-\\hat a\_0|.

\\]



The tested mismatch strengths were approximately



\\\[

0.47,\\,

0.52,\\,

0.57,\\,

0.62,\\,

0.72,\\,

0.82.

\\]



Hard attribution accuracy increased as



\\\[

82\\%,

92\\%,

94\\%,

96\\%,

100\\%,

100\\%.

\\]



At mismatch strength



\\\[

\\delta\_\\theta=0.52,

\\]



coverage reached 86% and accepted-case accuracy reached approximately 97.67%.



At larger mismatch strengths, attribution became essentially perfect under the

tested conditions.



\---



\## Structural-Change Sweep



Structural-change magnitude was represented by



\\\[

\\delta\_S

=

|a\_{\\mathrm{pre}}-a\_{\\mathrm{post}}|.

\\]



The tested strengths were approximately



\\\[

0.02,\\,

0.04,\\,

0.07,\\,

0.10,\\,

0.12,\\,

0.17.

\\]



The first three operating points produced:



| Structural mismatch | Hard accuracy | Coverage | Accepted accuracy |

|---:|---:|---:|---:|

| 0.02 | 38% | 34% | 47.06% |

| 0.04 | 76% | 50% | 88% |

| 0.07 | 100% | 92% | 100% |



All tested structural mismatches of magnitude 0.07 or greater produced 100%

hard attribution accuracy.



The transition between mismatch strengths 0.04 and 0.07 is particularly sharp.



\---



\## Operational Detectability Criterion



For exploratory purposes, define an operational attribution criterion requiring



\\\[

A\_j(\\delta)\\ge0.90,

\\]



\\\[

C\_j(\\delta)\\ge0.80,

\\]



and



\\\[

A\_j^{\\mathrm{sel}}(\\delta)\\ge0.95.

\\]



The first tested operating point satisfying all three conditions was:



| Mismatch mechanism | First qualifying tested magnitude |

|---|---:|

| Measurement noise | 1.00 |

| Process disturbance | 3.00 |

| Parameter mismatch | 0.52 |

| Structural change | 0.07 |



These quantities should not be interpreted as universal mathematical

thresholds.



They are empirical operational boundaries under the present simulation,

feature set, classifier, confidence threshold, stochastic model, and sampled

magnitude grid.



\---



\## Interval Interpretation



Because mismatch magnitude was evaluated on a discrete grid, the experiment

does not identify the exact transition point.



Instead, it bounds the transition between neighboring sampled magnitudes.



For example, process disturbance failed the operational criterion at



\\\[

d=2.5

\\]



and satisfied it at



\\\[

d=3.0.

\\]



Therefore the tested experiment supports the interval statement



\\\[

2.5 < \\delta\_P^\* \\le 3.0.

\\]



Similarly, structural change failed the criterion at



\\\[

\\delta\_S=0.04

\\]



and satisfied it at



\\\[

\\delta\_S=0.07,

\\]



giving



\\\[

0.04 < \\delta\_S^\* \\le 0.07.

\\]



Future experiments can refine these intervals using denser sweeps.



\---



\## Interpretation



The results support the existence of class-dependent attribution

detectability regions.



As mismatch strength increases,



\\\[

\\text{physical mismatch}

\\uparrow

\\]



generally produces



\\\[

\\text{diagnostic separation}

\\uparrow,

\\]



which produces



\\\[

\\text{attribution reliability}

\\uparrow.

\\]



However, the mapping is mechanism dependent.



There is therefore no evidence for a single universal mismatch magnitude at

which causal attribution becomes reliable.



Instead, each mismatch mechanism possesses its own empirical detectability

profile.



\---



\## Epistemic States



The results motivate distinguishing at least three diagnostic states:



\\\[

\\text{weak or non-identifiable mismatch},

\\]



\\\[

\\text{ambiguous attribution},

\\]



and



\\\[

\\text{reliably attributable mismatch}.

\\]



This distinction is important for adaptive digital twins because adaptive

action should depend not only on the predicted cause of mismatch but also on

whether the available observations contain enough information to support that

causal diagnosis.



\---



\## Conclusion



Experiment 021 mapped attribution behavior across 1,300 simulated trajectories

covering 26 mismatch operating points.



All four mismatch mechanisms exhibited improved attribution performance as

their diagnostic signatures became stronger.



The experiment provides empirical evidence for mechanism-specific

detectability regions and demonstrates that confidence and identifiability are

related but distinct concepts.



Most importantly, weak mismatch can produce confident but incorrect

attribution.



Therefore an adaptive digital twin should not interpret classifier confidence

as sufficient evidence of causal identifiability.



\---



\## Next Research Direction



The current experiment identifies detectability boundaries using a discrete

magnitude sweep.



The next step is to determine whether the digital twin can explicitly estimate

when a mismatch lies inside or outside an identifiable region.



This suggests augmenting causal attribution with an explicit

\*\*identifiability or evidence-sufficiency layer\*\* before attribution is allowed

to drive adaptation.



Such an architecture would implement the sequence



\\\[

\\text{detect disagreement}

\\rightarrow

\\text{evaluate evidence sufficiency}

\\rightarrow

\\text{attribute cause}

\\rightarrow

\\text{evaluate attribution confidence}

\\rightarrow

\\text{select adaptation}.

\\]



This provides the basis for the next stage of the adaptive digital-twin

architecture.



\---



\## Reproducibility



Experiment:



`experiments/mismatch\_attribution\_detectability.py`



Results:



`results/mismatch\_attribution\_detectability.csv`

