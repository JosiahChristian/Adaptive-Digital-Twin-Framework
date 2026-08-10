\# Experiment 019 — Confidence-Aware Mismatch Attribution



\## Objective



Extend explicit mismatch classification with a confidence-aware decision policy that distinguishes reliable diagnoses from ambiguous classifications.



Experiment 018 demonstrated that residual and adaptation-response signatures can distinguish four mismatch classes with high overall accuracy:



\- measurement noise,

\- process disturbance,

\- parameter mismatch,

\- structural change.



However, a hard classifier always returns a diagnosis even when competing class scores are nearly equal.



The objective of Experiment 019 is therefore to determine whether the classification margin can serve as an indicator of diagnostic reliability.



\---



\## Classification Margin



Let the mismatch classifier produce class scores



\\\[

s\_k^{(M)},

\\quad

s\_k^{(P)},

\\quad

s\_k^{(\\Theta)},

\\quad

s\_k^{(S)}.

\\]



Let



\\\[

s\_{(1)}

\\]



denote the largest score and



\\\[

s\_{(2)}

\\]



the second-largest score.



Define the classification margin



\\\[

m = s\_{(1)} - s\_{(2)}.

\\]



A large margin indicates that the preferred diagnosis is well separated from competing explanations.



A small margin indicates diagnostic ambiguity.



\---



\## Initial Confidence Bands



The initial confidence analysis divided classifications into three regions:



\\\[

m < 0.10

\\Rightarrow

\\text{ambiguous},

\\]



\\\[

0.10 \\leq m < 0.30

\\Rightarrow

\\text{low confidence},

\\]



and



\\\[

m \\geq 0.30

\\Rightarrow

\\text{confident}.

\\]



Across 400 classified trajectories, the observed results were:



| Confidence band | Cases | Accuracy | Mean margin |

|---|---:|---:|---:|

| Ambiguous | 7 | 57.143% | 0.042845 |

| Low confidence | 12 | 50.000% | 0.208737 |

| Confident | 381 | 99.738% | 1.805147 |



The strong separation in classification accuracy demonstrates that the score margin contains substantial information about diagnostic reliability.



\---



\## Selective Classification



A confidence-aware digital twin need not act on every classification.



Instead, define an acceptance rule



\\\[

\\mathcal{A}(m;\\tau)

=

\\begin{cases}

1, \& m \\geq \\tau,\\\\

0, \& m < \\tau,

\\end{cases}

\\]



where \\(\\tau\\) is the minimum acceptable classification margin.



Cases below the threshold are treated as uncertain diagnoses and may be deferred, observed for additional evidence, or handled using a conservative adaptation policy.



This produces a selective classifier:



\\\[

\\hat{z}

=

\\begin{cases}

\\arg\\max\_j s^{(j)}, \& m \\geq \\tau,\\\\

\\text{abstain}, \& m < \\tau.

\\end{cases}

\\]



\---



\## Threshold Sweep



The acceptance threshold was varied to characterize the tradeoff between diagnostic coverage and accepted-case accuracy.



| Threshold | Accepted | Coverage | Accuracy | Errors |

|---:|---:|---:|---:|---:|

| 0.00 | 400 | 100.00% | 97.50% | 10 |

| 0.05 | 396 | 99.00% | 97.98% | 8 |

| 0.10 | 393 | 98.25% | 98.22% | 7 |

| 0.15 | 390 | 97.50% | 98.46% | 6 |

| 0.20 | 389 | 97.25% | 98.71% | 5 |

| 0.25 | 385 | 96.25% | 98.96% | 4 |

| \*\*0.30\*\* | \*\*381\*\* | \*\*95.25%\*\* | \*\*99.74%\*\* | \*\*1\*\* |

| 0.40 | 380 | 95.00% | 99.74% | 1 |

| 0.50 | 377 | 94.25% | 99.73% | 1 |

| 0.75 | 347 | 86.75% | 99.71% | 1 |

| 1.00 | 290 | 72.50% | 100.00% | 0 |



\---



\## Empirical Operating Point



The threshold



\\\[

\\boxed{\\tau = 0.30}

\\]



provides a strong empirical operating point.



At this threshold,



\\\[

381/400 = 95.25\\%

\\]



of classifications are accepted.



Among accepted classifications,



\\\[

380/381 \\approx 99.738\\%

\\]



are correct.



The original hard classifier produced 10 errors.



After confidence-based abstention, only one error remains among accepted classifications.



Therefore,



\\\[

\\frac{9}{10}=90\\%

\\]



of the original classification errors are captured by the rejected low-margin region while retaining 95.25% of all decisions.



Increasing the threshold from \\(0.30\\) to \\(0.40\\) removes another classification without eliminating the remaining error.



More aggressive thresholds similarly reduce coverage without improving accepted-case accuracy until the threshold reaches \\(1.0\\), where perfect accepted-case accuracy is obtained at only 72.5% coverage.



This identifies \\(0.30\\) as a practical knee in the observed coverage-reliability tradeoff.



\---



\## Interpretation



Experiment 018 established that mismatch causes can be inferred from residual and adaptation-response signatures.



Experiment 019 demonstrates that the geometry of the resulting class scores also provides information about whether the inferred cause should be trusted.



The digital twin can therefore distinguish between



\\\[

\\text{diagnosis}

\\]



and



\\\[

\\text{confidence in diagnosis}.

\\]



This distinction is important because adaptation decisions may have different consequences depending on the inferred mismatch source.



A confident diagnosis may justify targeted adaptation.



An ambiguous diagnosis should instead encourage continued observation, conservative uncertainty inflation, or delayed structural intervention.



The architecture therefore becomes



\\\[

\\text{prediction disagreement}

\\rightarrow

\\text{residual characterization}

\\rightarrow

\\text{mismatch attribution}

\\rightarrow

\\text{confidence assessment}

\\rightarrow

\\text{adaptation decision}.

\\]



\---



\## Key Result



The classification margin is strongly associated with diagnostic reliability in the current experimental dataset.



Using a minimum accepted margin of



\\\[

\\tau=0.30,

\\]



the framework retains



\\\[

95.25\\%

\\]



classification coverage while achieving approximately



\\\[

99.74\\%

\\]



accuracy on accepted diagnoses.



This provides an empirical basis for confidence-aware selective mismatch attribution.



\---



\## Limitation



The confidence threshold was evaluated on the same experimental population used to characterize the mismatch classifier.



Consequently, the observed relationship between classification margin and accuracy should not yet be interpreted as evidence of out-of-sample calibration or generalization.



The next experimental stage should evaluate the attribution architecture under independently generated mismatch conditions, parameter ranges, disturbance magnitudes, and noise levels.



This distinction is necessary before confidence-aware attribution can be treated as a robust component of the adaptive digital twin.

