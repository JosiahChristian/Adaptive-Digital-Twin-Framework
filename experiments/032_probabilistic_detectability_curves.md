\# Experiment 032 — Probabilistic Detectability Curves



\## Objective



Replace the deterministic notion of an evidence-sufficiency boundary with a

probabilistic formulation that explicitly represents finite-population

uncertainty.



For mismatch mechanism \\(j\\), magnitude \\(\\delta\\), and population size \\(n\\),

define



\\\[

q\_j(\\delta;n)

=

P\\left(

E\_j(\\delta;\\mathcal{D}\_n)=1

\\right),

\\]



where \\(E\_j\\) denotes satisfaction of the operational evidence-sufficiency

criterion



\\\[

A \\ge 0.90,

\\qquad

C \\ge 0.80,

\\qquad

S \\ge 0.95.

\\]



The experiment estimates \\(q\_j(\\delta;100)\\) across mismatch magnitudes for

measurement noise, process disturbance, parameter mismatch, and structural

change.



\## Method



For each mismatch mechanism and magnitude, repeated independent populations of

100 trajectories were generated.



For every population, the mismatch classifier was evaluated and the following

population-level quantities were computed:



\- hard classification accuracy \\(A\\),

\- selective coverage \\(C\\),

\- selective accuracy \\(S\\),

\- Boolean evidence sufficiency.



The empirical evidence-sufficiency probability was estimated as



\\\[

\\hat q\_j(\\delta;100)

=

\\frac{

\\text{number of evidence-sufficient populations}

}{

\\text{number of population replicates}

}.

\\]



Wilson score intervals were computed for the estimated probability.



A total of 36 mismatch operating points were evaluated.



\## Results



All four mechanisms exhibited monotone nondecreasing empirical detectability

curves over the tested magnitude ranges.



Approximate transition locations obtained by linear interpolation were:



| Mechanism | \\(\\delta\_{10}\\) | \\(\\delta\_{50}\\) | \\(\\delta\_{90}\\) | Transition width |

|---|---:|---:|---:|---:|

| Measurement noise | 0.8278 | 0.8729 | 0.9100 | 0.0822 |

| Process disturbance | 2.5429 | 2.6889 | 2.7950 | 0.2521 |

| Parameter mismatch | 0.5019 | 0.5255 | 0.5411 | 0.0392 |

| Structural change | 0.0536 | 0.0595 | 0.0675 | 0.0139 |



where



\\\[

\\delta\_p

=

\\inf\\{

\\delta:

q\_j(\\delta;100)\\ge p

\\},

\\]



with interpolation between sampled operating points, and



\\\[

W\_j

=

\\delta\_{90}-\\delta\_{10}.

\\]



Structural change exhibited the sharpest transition in its native mismatch

parameterization, while process disturbance exhibited the broadest.



The structural-change transition was particularly clear:



\\\[

q(0.050)=0,

\\quad

q(0.055)=0.14,

\\quad

q(0.060)=0.54,

\\quad

q(0.065)=0.88,

\\quad

q(0.070)=0.92,

\\quad

q(0.075)=0.98.

\\]



Measurement noise and parameter mismatch showed evidence that selective

coverage is an important limiting component near their probabilistic

detectability transitions.



For measurement noise,



\\\[

\\delta=0.85:

\\quad

A=0.918,\\;

C=0.751,\\;

S=0.984,\\;

q=0.18,

\\]



whereas



\\\[

\\delta=0.90:

\\quad

A=0.938,\\;

C=0.830,\\;

S=0.987,\\;

q=0.88.

\\]



For parameter mismatch,



\\\[

\\delta=0.520:

\\quad

A=0.931,\\;

C=0.795,\\;

S=0.993,\\;

q=0.36,

\\]



followed by



\\\[

\\delta=0.545:

\\quad

A=0.967,\\;

C=0.884,\\;

S=0.995,\\;

q=1.00.

\\]



\## Interpretation



The evidence-sufficiency boundary is not appropriately represented as a single

deterministic mismatch magnitude.



Instead, finite-population sampling induces a transition region in which the

probability of satisfying the operational criterion increases from near zero

to near one.



The resulting probabilistic detectability curve provides three quantities that

a deterministic threshold cannot:



1\. transition location,

2\. transition width,

3\. uncertainty in the probability of evidence sufficiency.



The four mismatch mechanisms exhibit distinct transition geometries.



This indicates that detectability is mechanism-dependent not only in the

location of the transition but also in its sharpness.



Because mismatch magnitudes have mechanism-specific physical meanings,

transition widths should primarily be interpreted within mechanism rather than

as directly commensurate physical scales across mechanisms.



\## Conclusion



Experiment 032 establishes empirical probabilistic detectability curves for all

four mismatch mechanisms.



Across the tested operating points,



\\\[

q\_j(\\delta\_{k+1};100)

\\ge

q\_j(\\delta\_k;100),

\\]



for every mechanism and adjacent sampled magnitude.



The results support replacing the deterministic evidence-sufficiency boundary

with the probabilistic object



\\\[

q\_j(\\delta;n).

\\]



The next question is therefore not merely where evidence becomes sufficient,

but which component of the operational criterion controls the probability of

sufficiency throughout the transition region.

