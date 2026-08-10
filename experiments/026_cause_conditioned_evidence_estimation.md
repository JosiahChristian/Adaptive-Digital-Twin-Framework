\# Experiment 026 — Cause-Conditioned Evidence Estimation



\## Objective



Determine whether evidence sufficiency can be estimated more effectively when

the evidence test is conditioned on the hypothesized causal mismatch mechanism.



Experiment 025 demonstrated that evidence-sufficiency signatures are strongly

mechanism-dependent. Experiment 026 therefore develops separate interpretable

evidence rules for:



1\. measurement noise,

2\. process disturbance,

3\. parameter mismatch,

4\. structural change.



The Experiment 025 balanced population is used exclusively as the development

population.



\---



\## Mathematical Formulation



Rather than estimating evidence sufficiency with one universal function,



\\\[

\\hat e = \\Psi(\\mathcal I),

\\]



the cause-conditioned architecture uses



\\\[

\\boxed{

\\hat e\_j = \\Psi\_j(\\mathcal I)

}

\\]



for candidate mismatch mechanism



\\\[

j.

\\]



More generally,



\\\[

P(e\_k=1\\mid z\_k=j,\\mathcal I\_k)

=

\\Psi\_j(

\\mathbf{s}\_k,

\\mathcal{T}\_k,

\\mathcal{A}\_k

),

\\]



where



\\\[

\\mathbf{s}\_k

\\]



represents attribution-score geometry,



\\\[

\\mathcal{T}\_k

\\]



represents temporal residual structure, and



\\\[

\\mathcal{A}\_k

\\]



represents adaptive-response behavior.



\---



\## Development Population



The development population is the balanced Experiment 025 dataset:



\\\[

N=800.

\\]



It contains



\\\[

400

\\]



evidence-sufficient trajectories and



\\\[

400

\\]



evidence-insufficient trajectories.



Each of the four mismatch mechanisms contributes one sufficient and one

insufficient operating point, with 100 stochastic realizations per operating

point.



This population is used for rule discovery only.



\---



\## Candidate Feature Families



\### Measurement Noise



Candidate features:



\- classification margin,

\- score spread,

\- post-event cumulative absolute parameter update.



\### Process Disturbance



Candidate features:



\- classification margin,

\- score spread,

\- event maximum NIS,

\- event-vs-pre NIS change,

\- NIS recovery ratio.



\### Parameter Mismatch



Candidate features:



\- classification margin,

\- score spread.



\### Structural Change



Candidate features:



\- post-vs-pre parameter shift,

\- score spread,

\- classification margin,

\- post-event cumulative absolute parameter update,

\- event-vs-pre NIS change.



\---



\## Rule Search



For each mismatch mechanism, single-feature threshold rules and two-feature

conjunctive rules were evaluated.



Threshold candidates were generated from empirical feature quantiles.



Both threshold directions were considered:



\\\[

x\\ge\\tau

\\]



and



\\\[

x\\le\\tau.

\\]



Two-feature rules had the form



\\\[

(x\_1\\ \\square\_1\\ \\tau\_1)

\\land

(x\_2\\ \\square\_2\\ \\tau\_2).

\\]



Candidate selection considered balanced accuracy, total accuracy, precision,

recall, and model parsimony.



\---



\## Development Results



\### Measurement Noise



The best single-feature rule achieved



\\\[

67.5\\%

\\]



accuracy.



The best two-feature rule achieved



\\\[

71.5\\%

\\]



accuracy.



Its precision was



\\\[

73.118\\%

\\]



and recall was



\\\[

68.0\\%.

\\]



The pair reduced false negatives from 52 to 32 relative to the best

single-feature rule.



The additional complexity therefore produced a meaningful change in

development performance.



The selected rule is



\\\[

\\boxed{

\\hat e\_M=1

\\iff

m\\ge0.5162128944

\\land

U\_{\\mathrm{post}}\\ge0.0953430901

}

\\]



where



\\\[

m

\\]



is classification margin and



\\\[

U\_{\\mathrm{post}}

\\]



is post-event cumulative absolute parameter adaptation.



Development performance:



\\\[

A=71.5\\%,

\\]



\\\[

P=73.118\\%,

\\]



\\\[

R=68.0\\%.

\\]



The rule produced



\\\[

FP=25,

\\qquad

FN=32.

\\]



\---



\## Process Disturbance



The best single-feature rule achieved



\\\[

65.0\\%

\\]



accuracy.



The best pair achieved



\\\[

67.0\\%.

\\]



The two-feature rule therefore improved accuracy by only two percentage

points while retaining the same recall.



The additional complexity was not considered sufficiently justified.



The selected parsimonious rule is



\\\[

\\boxed{

\\hat e\_P=1

\\iff

\\rho\_{\\mathrm{NIS}}

\\le

0.3401323777

}

\\]



where



\\\[

\\rho\_{\\mathrm{NIS}}

\\]



is the NIS recovery ratio.



Development performance:



\\\[

A=65.0\\%,

\\]



\\\[

P=62.5\\%,

\\]



\\\[

R=75.0\\%.

\\]



The rule produced



\\\[

FP=45,

\\qquad

FN=25.

\\]



\---



\## Parameter Mismatch



The best single-feature rule achieved



\\\[

67.0\\%

\\]



accuracy.



The best two-feature rule achieved only



\\\[

67.5\\%.

\\]



The pair removed one false positive while leaving false negatives unchanged.



The improvement was therefore insufficient to justify additional complexity.



The selected rule is



\\\[

\\boxed{

\\hat e\_{\\Theta}=1

\\iff

m\\ge0.5733833425

}

\\]



where



\\\[

m

\\]



is classification margin.



Development performance:



\\\[

A=67.0\\%,

\\]



\\\[

P=67.0\\%,

\\]



\\\[

R=67.0\\%.

\\]



The rule produced



\\\[

FP=33,

\\qquad

FN=33.

\\]



\---



\## Structural Change



Structural change produced a qualitatively different result.



The best single-feature rule achieved



\\\[

\\boxed{99.5\\%}

\\]



development accuracy.



Precision was



\\\[

99.010\\%

\\]



and recall was



\\\[

100\\%.

\\]



The rule produced



\\\[

TP=100,

\\]



\\\[

TN=99,

\\]



\\\[

FP=1,

\\]



and



\\\[

FN=0.

\\]



The best two-feature rule produced no improvement.



The selected rule is therefore



\\\[

\\boxed{

\\hat e\_S=1

\\iff

\\Delta\\hat a\_{\\mathrm{post-pre}}

\\le

\-0.04926012886

}

\\]



where



\\\[

\\Delta\\hat a\_{\\mathrm{post-pre}}

\\]



is the post-event parameter-estimate shift relative to the pre-event

parameter estimate.



\---



\## Frozen Cause-Conditioned Rules



The Experiment 026 development process produces the following frozen

specification.



| Cause | Frozen evidence rule |

|---|---|

| Measurement noise | classification margin >= 0.5162128944 AND post cumulative absolute parameter update >= 0.0953430901 |

| Process disturbance | recovery ratio NIS <= 0.3401323777 |

| Parameter mismatch | classification margin >= 0.5733833425 |

| Structural change | parameter shift post-vs-pre <= -0.04926012886 |



These features, threshold directions, and numerical thresholds are frozen

after Experiment 026.



They must not be modified in response to Experiment 027 validation results.



\---



\## Interpretation



Cause-conditioning improves the conceptual organization of evidence

estimation, but it does not make all evidence-sufficiency decisions

deterministic.



Measurement noise, process disturbance, and parameter mismatch achieve only

moderate development accuracy using simple deterministic rules.



This suggests that evidence sufficiency near a detectability boundary may be

intrinsically stochastic or may require a richer probabilistic representation.



Structural change is fundamentally different in the present experimental

system.



Its evidence state is almost perfectly separated by coherent post-event

parameter evolution.



Thus the digital twin can distinguish between merely observing disagreement

and observing disagreement accompanied by persistent evolution of its learned

dynamical representation.



\---



\## Architectural Implication



The resulting architecture is



\\\[

\\text{observe}

\\rightarrow

\\text{detect disagreement}

\\rightarrow

\\text{attribute cause}

\\rightarrow

\\text{evaluate cause-conditioned evidence}

\\rightarrow

\\text{adapt or abstain}.

\\]



The evidence test is not universal.



Instead,



\\\[

\\boxed{

\\Psi\_M

\\neq

\\Psi\_P

\\neq

\\Psi\_{\\Theta}

\\neq

\\Psi\_S.

}

\\]



Different hypothesized causes require different forms of supporting evidence.



\---



\## Probabilistic Extension



The moderate performance of three deterministic estimators suggests that the

more general formulation should remain probabilistic:



\\\[

\\boxed{

P(e\_k=1\\mid z\_k=j,\\mathcal I\_k)

}

\\]



rather than forcing every evidence state into a deterministic Boolean

decision.



The deterministic Experiment 026 rules should therefore be interpreted as

interpretable baseline estimators against which later probabilistic models may

be compared.



\---



\## Methodological Constraint



Experiment 026 is a development experiment.



All rule selection and threshold tuning occur exclusively on the Experiment

025 balanced development population.



After completion of Experiment 026, the selected rules are frozen.



Experiment 027 must use:



\- new operating points,

\- new stochastic seeds,

\- identical features,

\- identical threshold directions,

\- identical numerical thresholds.



No post-validation tuning is permitted.



\---



\## Conclusion



Experiment 026 establishes the first cause-conditioned evidence-sufficiency

estimators for the adaptive digital twin.



The results show that evidence sufficiency has heterogeneous causal structure.



Structural-change evidence can be estimated almost perfectly from coherent

parameter evolution, while the remaining mismatch mechanisms retain

substantial uncertainty near their detectability boundaries.



The resulting frozen rules provide an interpretable baseline for independent

generalization testing.



\---



\## Next Research Direction



Experiment 027 should perform independent cause-conditioned evidence

validation.



The frozen Experiment 026 rules will be evaluated on previously unseen

intermediate operating points and stochastic seeds.



The central question becomes



\\\[

\\boxed{

\\text{Do cause-conditioned evidence rules generalize beyond their development boundaries?}

}

\\]



\---



\## Reproducibility



Development population:



`results/balanced\_evidence\_boundary\_sampling.csv`



Experiment:



`experiments/cause\_conditioned\_evidence\_estimation.py`



Results:



`results/cause\_conditioned\_evidence\_estimation.csv`

