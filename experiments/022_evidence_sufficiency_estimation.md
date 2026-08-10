\# Experiment 022 — Evidence Sufficiency Estimation



\## Objective



Determine whether observable attribution-score geometry can distinguish

operating regimes containing sufficient evidence for reliable causal

attribution from weak or non-identifiable regimes.



This experiment follows the mismatch-attribution detectability analysis of

Experiment 021.



The central question is not whether an individual causal classification is

correct.



Instead, the question is whether the observational regime itself contains

sufficient information to support reliable causal inference.



\---



\## Evidence-Sufficiency Definition



For mismatch mechanism \\(j\\) and mismatch magnitude \\(\\delta\\), Experiment 021

defined an operationally identifiable region using



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



Operating points satisfying all three conditions were assigned the

evidence-sufficiency label



\\\[

e=1.

\\]



Operating points failing one or more conditions were assigned



\\\[

e=0.

\\]



The label therefore describes the empirical identifiability of an operating

regime rather than the correctness of an individual classification.



This distinction prevents the evidence layer from being defined circularly by

the classification decision it is intended to guard.



\---



\## Dataset



Out-of-sample attribution trajectories from the previous generalization

experiment were matched to operating points represented in the Experiment 021

detectability sweep.



The resulting dataset contained



\\\[

300

\\]



trajectories.



Of these,



\\\[

200

\\]



were associated with evidence-sufficient operating regimes and



\\\[

100

\\]



were associated with evidence-insufficient operating regimes.



\---



\## Candidate Observable Features



Only quantities available from the attribution mechanism were considered.



The candidate features were:



\\\[

m

=

s\_{(1)}-s\_{(2)},

\\]



the classification margin,



\\\[

s\_{\\max},

\\]



the largest attribution score,



\\\[

s\_{(2)},

\\]



the second-largest attribution score,



\\\[

\\bar s,

\\]



the mean attribution score,



\\\[

\\Delta s

=

s\_{\\max}-s\_{\\min},

\\]



the total score spread, and



\\\[

r

=

\\frac{s\_{(1)}}{s\_{(2)}+\\epsilon},

\\]



the ratio between the two largest attribution scores.



No true mismatch class, true mismatch magnitude, or individual classification

correctness was used as an evidence-estimator input.



\---



\## Feature Separation



All candidate score-geometry features differed between evidence-sufficient and

evidence-insufficient regimes.



For classification margin,



\\\[

\\mu\_{e=1}=2.2287,

\\qquad

\\mu\_{e=0}=0.4600.

\\]



For maximum attribution score,



\\\[

\\mu\_{e=1}=4.2715,

\\qquad

\\mu\_{e=0}=1.2834.

\\]



For total score spread,



\\\[

\\mu\_{e=1}=4.1271,

\\qquad

\\mu\_{e=0}=1.1578.

\\]



For the top-to-second score ratio,



\\\[

\\mu\_{e=1}=2.5565,

\\qquad

\\mu\_{e=0}=1.6188.

\\]



Thus evidence-sufficient regimes tend to produce both stronger and more

strongly separated causal-attribution scores.



\---



\## Standardized Feature Separation



A standardized separation statistic was defined as



\\\[

D\_f

=

\\frac{

|\\mu\_{f,1}-\\mu\_{f,0}|

}{

\\sqrt{

\\left(

\\sigma\_{f,1}^2+\\sigma\_{f,0}^2

\\right)/2

}

}.

\\]



Observed values were approximately:



| Feature | Standardized separation |

|---|---:|

| classification margin | 1.2291 |

| top score | 1.1147 |

| second score | 0.8860 |

| mean score | 1.0618 |

| score spread | 1.1176 |

| top-to-second ratio | 1.0359 |



Classification margin was the strongest individual separator.



However, previous experiments demonstrated that classification margin alone

cannot guarantee causal identifiability.



In particular, weak mismatch regimes may produce confident but incorrect

causal classifications.



\---



\## Margin-Only Baseline



A family of margin-only evidence rules of the form



\\\[

\\hat e

=

\\mathbf{1}\[m\\ge\\tau\_m]

\\]



was evaluated.



At



\\\[

\\tau\_m=0.20,

\\]



the rule produced



\\\[

77.67\\%

\\]



accuracy,



\\\[

75.48\\%

\\]



precision, and



\\\[

98.5\\%

\\]



recall.



The corresponding confusion counts were



\\\[

TP=197,

\\quad

TN=36,

\\quad

FP=64,

\\quad

FN=3.

\\]



Thus a low margin threshold preserves nearly all sufficient-evidence cases but

incorrectly declares many insufficient regimes to be sufficient.



\---



\## Two-Dimensional Evidence Rules



Candidate rules combining classification margin with an additional

score-geometry feature were evaluated.



The general form was



\\\[

\\hat e

=

\\mathbf{1}

\[

m\\ge\\tau\_m

\\land

g(s)\\ge\\tau\_g

].

\\]



The best tested rule for each feature family was:



| Secondary feature | Accuracy | Precision | Recall | FP | FN |

|---|---:|---:|---:|---:|---:|

| top score | 86.67% | 84.19% | 98.5% | 37 | 3 |

| second score | 84.33% | 91.35% | 84.5% | 16 | 31 |

| mean score | 85.00% | 91.44% | 85.5% | 16 | 29 |

| score spread | 88.33% | 86.67% | 97.5% | 30 | 5 |

| top-to-second ratio | 85.00% | 91.44% | 85.5% | 16 | 29 |



The highest overall accuracy was obtained by combining classification margin

with total attribution-score spread.



\---



\## Candidate Evidence-Sufficiency Estimator



The selected candidate rule is



\\\[

\\boxed{

\\hat e

=

\\mathbf{1}

\[

m\\ge0.20

\\land

\\Delta s\\ge1.00

]

}

\\]



where



\\\[

m=s\_{(1)}-s\_{(2)}

\\]



and



\\\[

\\Delta s=s\_{\\max}-s\_{\\min}.

\\]



On the exploratory dataset this rule produced



\\\[

88.33\\%

\\]



accuracy,



\\\[

86.67\\%

\\]



precision, and



\\\[

97.5\\%

\\]



recall.



Its confusion counts were



\\\[

TP=195,

\\quad

TN=70,

\\quad

FP=30,

\\quad

FN=5.

\\]



Relative to the margin-only rule at the same margin threshold, false

evidence-sufficiency declarations decreased from



\\\[

64

\\]



to



\\\[

30,

\\]



while false insufficiency declarations increased only from



\\\[

3

\\]



to



\\\[

5\.

\\]



\---



\## Interpretation



The candidate estimator combines two different forms of diagnostic separation.



The classification margin



\\\[

m=s\_{(1)}-s\_{(2)}

\\]



measures local separation between the two leading causal hypotheses.



The total score spread



\\\[

\\Delta s=s\_{\\max}-s\_{\\min}

\\]



measures global separation across the complete causal hypothesis set.



The evidence rule therefore requires both a locally distinguishable preferred

cause and meaningful global structure in the attribution-score field.



Conceptually,



\\\[

\\text{evidence sufficiency}

\\approx

\\text{local causal separation}

\+

\\text{global diagnostic structure}.

\\]



\---



\## Important Limitation



The candidate thresholds



\\\[

\\tau\_m=0.20

\\]



and



\\\[

\\tau\_{\\Delta s}=1.00

\\]



were selected using the same exploratory dataset on which their performance was

measured.



Therefore the reported performance is not an estimate of out-of-sample

generalization.



The current experiment establishes a candidate evidence-sufficiency mechanism,

not a validated one.



The thresholds must now be frozen and evaluated on independently generated

operating points and stochastic realizations.



\---



\## Conclusion



Experiment 022 provides evidence that empirical causal identifiability leaves

an observable signature in attribution-score geometry.



Classification confidence is informative but insufficient by itself.



Combining classification margin with total score spread substantially reduced

false declarations of evidence sufficiency while preserving high sensitivity

to identifiable regimes.



The resulting candidate estimator is



\\\[

\\boxed{

\\hat e

=

\\mathbf{1}

\[

m\\ge0.20

\\land

\\Delta s\\ge1.00

].

}

\\]



This estimator will remain frozen during subsequent independent validation.



\---



\## Next Research Direction



The next experiment will test the frozen evidence-sufficiency estimator on new

stochastic realizations and operating points not used for threshold selection.



No evidence-estimator thresholds will be modified during that evaluation.



This creates the progression



\\\[

\\text{empirical detectability}

\\rightarrow

\\text{observable evidence geometry}

\\rightarrow

\\text{candidate evidence estimator}

\\rightarrow

\\text{independent validation}.

\\]



\---



\## Reproducibility



Experiment:



`experiments/evidence\_sufficiency\_estimation.py`



Results:



`results/evidence\_sufficiency\_estimation.csv`

