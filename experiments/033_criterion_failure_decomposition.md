\# Experiment 033 — Criterion-Component Failure Decomposition



\## Objective



Determine which components of the operational evidence-sufficiency criterion

control the probabilistic detectability transitions observed in Experiment

032\.



Evidence sufficiency is defined by



\\\[

A\\ge0.90,

\\qquad

C\\ge0.80,

\\qquad

S\\ge0.95,

\\]



where



\\\[

A

\\]



is hard causal-classification accuracy,



\\\[

C

\\]



is selective coverage, and



\\\[

S

\\]



is selective accuracy.



Define the failure events



\\\[

F\_A=\\{A<0.90\\},

\\]



\\\[

F\_C=\\{C<0.80\\},

\\]



and



\\\[

F\_S=\\{S<0.95\\}.

\\]



Then



\\\[

1-q

=

P(

F\_A\\cup F\_C\\cup F\_S

).

\\]



Experiment 033 decomposes this failure probability into mutually exclusive

criterion-failure modes.



\---



\## Failure-State Representation



Each independently generated population is assigned to exactly one of eight

states:



\\\[

\\text{pass},

\\]



\\\[

A,

\\quad

C,

\\quad

S,

\\]



\\\[

A\\cap C,

\\quad

A\\cap S,

\\quad

C\\cap S,

\\]



or



\\\[

A\\cap C\\cap S.

\\]



For mismatch mechanism \\(j\\) and magnitude \\(\\delta\\), define the

failure-state distribution



\\\[

\\boxed{

\\boldsymbol{\\pi}\_j(\\delta)

=

\[

P(\\text{pass}),

P(A),

P(C),

P(S),

P(A\\cap C),

P(A\\cap S),

P(C\\cap S),

P(A\\cap C\\cap S)

].

}

\\]



The probabilistic evidence-sufficiency quantity is therefore



\\\[

q\_j(\\delta)

=

P(\\text{pass}).

\\]



\---



\## Measurement Noise



Measurement-noise detectability is primarily limited by selective coverage.



At



\\\[

\\delta=0.85,

\\]



the evidence-sufficiency probability was



\\\[

q=0.20.

\\]



Marginal failure probabilities were



\\\[

P(F\_A)=0.22,

\\]



\\\[

P(F\_C)=0.80,

\\]



and



\\\[

P(F\_S)=0.06.

\\]



The dominant exclusive failure mode was



\\\[

\\boxed{

C\\text{-only}=0.56.

}

\\]



At



\\\[

\\delta=0.90,

\\]



the evidence-sufficiency probability increased to



\\\[

q=0.76.

\\]



Coverage remained the dominant residual limitation:



\\\[

C\\text{-only}=0.18.

\\]



At



\\\[

\\delta=0.95,

\\]



\\\[

q=0.98,

\\]



and the only remaining observed failure mode was



\\\[

C\\text{-only}=0.02.

\\]



The measurement-noise transition is therefore approximately



\\\[

\\boxed{

A\\cap C

\\rightarrow

C

\\rightarrow

\\text{pass}.

}

\\]



Selective accuracy contributes little to the transition.



\---



\## Process Disturbance



Process-disturbance detectability exhibits a different transition structure.



At



\\\[

\\delta=2.50,

\\]



\\\[

q=0.10,

\\]



with



\\\[

P(F\_A)=0.88,

\\qquad

P(F\_C)=0.70,

\\qquad

P(F\_S)=0.30.

\\]



The dominant exclusive failure mode was



\\\[

\\boxed{

A\\cap C=0.44.

}

\\]



At



\\\[

\\delta=2.60,

\\]



the same coupled mode remained dominant:



\\\[

A\\cap C=0.34.

\\]



At



\\\[

\\delta=2.70,

\\]



coverage had largely recovered,



\\\[

P(F\_C)=0.06,

\\]



while hard accuracy still failed in



\\\[

46\\%

\\]



of independently generated populations.



The dominant mode became



\\\[

\\boxed{

A\\text{-only}=0.34.

}

\\]



At



\\\[

\\delta=2.80,

\\]



hard accuracy remained the primary residual limitation:



\\\[

A\\text{-only}=0.18.

\\]



By



\\\[

\\delta=2.90,

\\]



\\\[

q=0.96.

\\]



The process-disturbance transition is therefore approximately



\\\[

\\boxed{

A\\cap C

\\rightarrow

A

\\rightarrow

\\text{pass}.

}

\\]



Thus hard causal-attribution accuracy is the final major bottleneck for

process-disturbance detectability.



\---



\## Parameter Mismatch



Parameter mismatch exhibits a particularly clear sequential failure

transition.



At



\\\[

\\delta=0.495,

\\]



\\\[

q=0,

\\]



with



\\\[

P(F\_A)=0.72,

\\qquad

P(F\_C)=1.00,

\\qquad

P(F\_S)=0.02.

\\]



The dominant failure mode was



\\\[

\\boxed{

A\\cap C=0.70.

}

\\]



At



\\\[

\\delta=0.520,

\\]



hard accuracy had largely recovered:



\\\[

P(F\_A)=0.06.

\\]



Coverage remained insufficient in



\\\[

58\\%

\\]



of populations.



The dominant exclusive mode became



\\\[

\\boxed{

C\\text{-only}=0.52.

}

\\]



At



\\\[

\\delta=0.545,

\\]



all 50 independently generated populations satisfied the evidence criterion:



\\\[

q=1.

\\]



The parameter-mismatch transition is therefore



\\\[

\\boxed{

A\\cap C

\\rightarrow

C

\\rightarrow

\\text{pass}.

}

\\]



Coverage is the final limiting quantity near the detectability boundary.



\---



\## Structural Change



Structural change exhibits the richest criterion-failure transition.



At



\\\[

\\delta=0.050,

\\]



\\\[

q=0,

\\]



with



\\\[

P(F\_A)=1,

\\qquad

P(F\_C)=1,

\\qquad

P(F\_S)=0.82.

\\]



The dominant failure state was



\\\[

\\boxed{

A\\cap C\\cap S=0.82.

}

\\]



Thus weak structural mismatch simultaneously degrades hard classification,

coverage, and selective accuracy.



At



\\\[

\\delta=0.055,

\\]



the transition becomes heterogeneous.



The two largest exclusive failure modes were



\\\[

C\\text{-only}=0.28

\\]



and



\\\[

A\\cap C\\cap S=0.28.

\\]



At



\\\[

\\delta=0.060,

\\]



\\\[

q=0.50.

\\]



Coverage-only failure was the largest individual mode:



\\\[

C\\text{-only}=0.18,

\\]



although several coupled failure states remained present.



At



\\\[

\\delta=0.065,

\\]



coverage failure disappeared completely:



\\\[

P(F\_C)=0.

\\]



The remaining failures were dominated by selective-accuracy effects:



\\\[

S\\text{-only}=0.06,

\\]



and



\\\[

A\\cap S=0.06.

\\]



At



\\\[

\\delta=0.070

\\]



and



\\\[

\\delta=0.075,

\\]



the only observed failure state was



\\\[

\\boxed{

S\\text{-only}=0.04.

}

\\]



Structural change therefore follows the approximate sequence



\\\[

\\boxed{

A\\cap C\\cap S

\\rightarrow

\\text{mixed failure}

\\rightarrow

C

\\rightarrow

A/S

\\rightarrow

S

\\rightarrow

\\text{pass}.

}

\\]



\---



\## Mechanism-Specific Transition Structure



The four mismatch mechanisms therefore exhibit distinct criterion-failure

pathways.



\### Measurement Noise



\\\[

A\\cap C

\\rightarrow

C

\\rightarrow

\\text{pass}.

\\]



Primary final bottleneck:



\\\[

\\boxed{\\text{coverage}}.

\\]



\### Process Disturbance



\\\[

A\\cap C

\\rightarrow

A

\\rightarrow

\\text{pass}.

\\]



Primary final bottleneck:



\\\[

\\boxed{\\text{hard causal accuracy}}.

\\]



\### Parameter Mismatch



\\\[

A\\cap C

\\rightarrow

C

\\rightarrow

\\text{pass}.

\\]



Primary final bottleneck:



\\\[

\\boxed{\\text{coverage}}.

\\]



\### Structural Change



\\\[

A\\cap C\\cap S

\\rightarrow

\\text{mixed}

\\rightarrow

C

\\rightarrow

A/S

\\rightarrow

S

\\rightarrow

\\text{pass}.

\\]



Primary late-stage bottleneck:



\\\[

\\boxed{\\text{selective accuracy}}.

\\]



\---



\## Interpretation



Experiment 032 showed that each mismatch mechanism possesses a probabilistic

detectability curve



\\\[

q\_j(\\delta).

\\]



Experiment 033 demonstrates that the scalar probability \\(q\_j(\\delta)\\) alone

does not fully characterize the epistemic state of the digital twin.



Two operating points can have similar values of



\\\[

q

\\]



while exhibiting fundamentally different reasons for evidence insufficiency.



The richer representation is therefore the failure-state distribution



\\\[

\\boxed{

\\boldsymbol{\\pi}\_j(\\delta).

}

\\]



This distribution identifies not only whether sufficient evidence exists, but

which criterion component prevents sufficiency.



\---



\## Architectural Implication



The digital twin can distinguish among several qualitatively different

epistemic states.



Coverage failure,



\\\[

F\_C,

\\]



indicates that too few realizations support confident causal attribution.



Hard-accuracy failure,



\\\[

F\_A,

\\]



indicates that the causal attribution itself remains unreliable.



Selective-accuracy failure,



\\\[

F\_S,

\\]



indicates that even the accepted high-confidence decisions retain excessive

classification error.



These states may require different responses.



A future evidence-aware adaptation policy may therefore condition its action

on



\\\[

\\boldsymbol{\\pi}\_j

\\]



rather than only on



\\\[

q\_j.

\\]



\---



\## Conclusion



Experiment 033 establishes that probabilistic detectability transitions have

mechanism-specific internal structure.



Measurement noise and parameter mismatch are ultimately coverage-limited.



Process disturbance is ultimately hard-accuracy-limited.



Structural change progresses through a multi-stage transition and becomes

selective-accuracy-limited near full detectability.



Thus the appropriate evidence representation is not merely



\\\[

q\_j(\\delta),

\\]



but the richer epistemic state



\\\[

\\boxed{

\\boldsymbol{\\pi}\_j(\\delta).

}

\\]



This representation provides a direct description of why evidence is

insufficient and creates the foundation for cause- and failure-aware adaptive

decision policies.



\---



\## Reproducibility



Experiment:



`experiments/criterion\_failure\_decomposition.py`



Results:



`results/criterion\_failure\_decomposition.csv`

