\# Experiment 020 — Out-of-Sample Attribution Generalization



\## Objective



Evaluate whether the frozen mismatch-attribution architecture developed in

Experiments 018 and 019 generalizes to mismatch magnitudes that were not used

during classifier development.



No attribution-score weights or confidence thresholds were modified after

observing the held-out conditions.



The classifier and the selective-classification threshold



\\\[

\\tau=0.30

\\]



were therefore treated as frozen components.



\---



\## Held-Out Conditions



Eight new operating conditions were evaluated.



\### Measurement Noise



Development condition:



\\\[

\\sigma\_m=1.00.

\\]



Held-out conditions:



\\\[

\\sigma\_m=0.75

\\]



and



\\\[

\\sigma\_m=1.25.

\\]



\### Process Disturbance



Development disturbance:



\\\[

d=3.0.

\\]



Held-out disturbances:



\\\[

d=2.0

\\]



and



\\\[

d=4.0.

\\]



\### Initial Parameter Mismatch



Development estimate:



\\\[

\\hat a\_0=0.20.

\\]



Held-out estimates:



\\\[

\\hat a\_0=0.30

\\]



and



\\\[

\\hat a\_0=0.10.

\\]



\### Structural Change



Development transition:



\\\[

0.92\\rightarrow0.80.

\\]



Held-out transitions:



\\\[

0.92\\rightarrow0.85

\\]



and



\\\[

0.92\\rightarrow0.75.

\\]



Each condition was evaluated across 50 random seeds.



The resulting held-out population contained



\\\[

8\\times50=400

\\]



trajectories.



\---



\## Overall Generalization Performance



The frozen hard classifier correctly attributed



\\\[

374

\\]



of



\\\[

400

\\]



held-out trajectories.



Therefore,



\\\[

\\boxed{

\\mathrm{Accuracy}\_{hard}=93.5\\%

}

\\]



on the held-out experimental population.



This is lower than the 97.5% accuracy observed on the development population,

as expected when mismatch magnitudes are changed.



\---



\## Confidence-Aware Performance



The confidence threshold remained fixed at



\\\[

\\tau=0.30.

\\]



The selective classifier accepted



\\\[

340

\\]



of the 400 trajectories.



Thus,



\\\[

\\boxed{

\\mathrm{Coverage}=85.0\\%

}

\\]



on the held-out population.



Among accepted diagnoses,



\\\[

336

\\]



of



\\\[

340

\\]



were correct.



Therefore,



\\\[

\\boxed{

\\mathrm{Accuracy}\_{accepted}=98.824\\%

}.

\\]



The hard classifier made 26 errors.



Only four errors remained among accepted cases.



Thus confidence-based abstention captured



\\\[

22

\\]



of the



\\\[

26

\\]



held-out errors:



\\\[

\\frac{22}{26}

\\approx

84.6\\%.

\\]



This provides evidence that classification margin continues to carry useful

reliability information under the tested held-out conditions.



\---



\## Per-Condition Results



| Condition | Hard Accuracy | Coverage | Accepted Accuracy |

|---|---:|---:|---:|

| Measurement noise 0.75 | 80% | 44% | 95.45% |

| Measurement noise 1.25 | 98% | 98% | 97.96% |

| Parameter mismatch 0.10 | 100% | 100% | 100% |

| Parameter mismatch 0.30 | 96% | 94% | 100% |

| Process disturbance 2.0 | 74% | 56% | 92.86% |

| Process disturbance 4.0 | 100% | 98% | 100% |

| Structural change 0.75 | 100% | 98% | 100% |

| Structural change 0.85 | 100% | 92% | 100% |



\---



\## Generalization Pattern



The attribution architecture performs particularly strongly for large or

distinct mismatch signatures.



Perfect hard-classification accuracy was obtained for:



\- process disturbance magnitude 4.0,

\- initial parameter estimate 0.10,

\- structural change to 0.75,

\- structural change to 0.85.



The primary generalization weakness occurs for weaker mismatch conditions.



The two most difficult held-out conditions were:



\\\[

\\sigma\_m=0.75

\\]



and



\\\[

d=2.0.

\\]



These conditions are closer to nominal stochastic behavior than their

development counterparts.



\---



\## Process-Disturbance Failure Mode



The disturbance condition



\\\[

d=2.0

\\]



produced only 74% hard-classification accuracy.



Across the complete held-out population, process-disturbance errors included:



\- six classifications as parameter mismatch,

\- six classifications as structural change,

\- one classification as measurement noise.



This indicates that moderate transient disturbances can produce residual and

adaptation signatures that overlap with several alternative explanations.



The attribution problem therefore becomes increasingly ambiguous as event

magnitude decreases.



\---



\## Measurement-Noise Failure Mode



The held-out condition



\\\[

\\sigma\_m=0.75

\\]



produced 80% hard-classification accuracy.



The corresponding confidence-aware coverage was only 44%.



However, accepted-case accuracy remained approximately:



\\\[

95.45\\%.

\\]



This indicates that the confidence mechanism frequently recognized that the

moderate-noise trajectories did not produce sufficiently distinctive evidence

for reliable hard attribution.



\---



\## Strong-Mismatch Generalization



The stronger held-out perturbations were classified with very high accuracy.



For example:



\\\[

d=4.0

\\]



produced 100% hard accuracy.



Both held-out structural transitions also produced 100% hard accuracy.



These results suggest that the discovered attribution features are not tied

only to the exact development magnitudes.



Instead, they retain diagnostic usefulness across a range of mismatch

strengths.



\---



\## Interpretation



Experiment 020 provides preliminary evidence that the attribution architecture

captures repeatable structure in mismatch behavior rather than only the exact

conditions used during development.



However, attribution performance depends strongly on mismatch strength.



As the mismatch signal approaches the scale of ordinary stochastic variation,

the feature distributions increasingly overlap.



Thus the attribution problem contains an implicit detectability boundary:



\\\[

\\text{mismatch strength}

\\downarrow

\\quad\\Rightarrow\\quad

\\text{class separability}

\\downarrow.

\\]



The digital twin should therefore not be expected to produce equally reliable

causal diagnoses at every mismatch magnitude.



\---



\## Importance of Confidence-Aware Abstention



The held-out experiment also validates the usefulness of selective

classification.



The frozen confidence threshold rejected a substantial fraction of difficult

held-out trajectories while retaining very high accuracy among accepted

diagnoses.



This suggests the architecture should distinguish among:



\\\[

\\text{detected and confidently attributed mismatch},

\\]



\\\[

\\text{detected but ambiguously attributed mismatch},

\\]



and potentially



\\\[

\\text{mismatch too weak to distinguish from stochastic variation}.

\\]



These are different epistemic states and should not necessarily trigger the

same adaptive action.



\---



\## Conclusion



The frozen mismatch-attribution architecture achieved:



\\\[

93.5\\%

\\]



hard-classification accuracy across 400 held-out trajectories.



At the frozen confidence threshold



\\\[

\\tau=0.30,

\\]



the system retained 85% coverage while achieving approximately 98.82% accuracy

on accepted diagnoses.



The strongest generalization weakness occurs for moderate mismatch magnitudes,

particularly the process disturbance of magnitude 2.0 and measurement-noise

standard deviation 0.75.



The results therefore motivate characterization of an attribution

detectability boundary rather than immediate retuning of the existing rules.



\---



\## Next Research Question



How does attribution accuracy and confidence change continuously as mismatch

strength approaches nominal stochastic variation?



This motivates a magnitude-sweep experiment in which mismatch strength is

systematically varied while the attribution architecture remains frozen.



Such an experiment can estimate the relationship



\\\[

\\text{mismatch magnitude}

\\longrightarrow

\\text{detectability}

\\longrightarrow

\\text{attribution confidence}.

\\]



This provides the basis for:



\*\*Experiment 021 — Mismatch Attribution Detectability Boundary.\*\*



\---



\## Reproducibility



Experiment:



`experiments/out\_of\_sample\_attribution\_generalization.py`



Results:



`results/out\_of\_sample\_attribution\_generalization.csv`

