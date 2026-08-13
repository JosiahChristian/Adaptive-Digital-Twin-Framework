\# Experiment 103 — Calibration-Guard Constituent State Geometry Analysis



\## Purpose



Experiment 101 demonstrated that a frozen historical calibration-risk intervention could prospectively reduce harmful support expansions and regret.



Experiment 102 then showed that the scalar calibration-risk probability was not sufficient to solve the intervention's selectivity problem by simple threshold escalation.



Within the 22 Experiment 101 vetoes, harmful events actually had lower calibration-risk probabilities on average than beneficial vetoes.



Experiment 103 therefore examines the constituent pre-action calibration-state variables that generated the Experiment 101 calibration-risk probability.



The central question is:



\*\*Do harmful and beneficial vetoes reach similar aggregate calibration-risk probabilities through different internal historical calibration-state geometries?\*\*



This experiment is diagnostic only.



It does not:



\- introduce new prospective seeds,

\- fit a new controller,

\- define a new intervention threshold,

\- replace the Experiment 101 calibration probability,

\- or alter the Experiment 101 result.



\---



\## Source Population



Experiment 103 reconstructs the 22 support-expansion events vetoed by the frozen Experiment 101 calibration-aware controller.



The veto population contains:



\- beneficial vetoes: 17

\- harmful vetoes: 5



The veto events occurred across seeds:



44094, 44095, 44096, 44097, 44098, 44099, 44100, 44101, 44103, 44104, 44105, 44108, and 44110.



All of these seeds had already been consumed by Experiment 101.



No new prospective data were generated.



\---



\## Frozen Calibration Representation



Experiment 101 used the Experiment 100 primary calibration representation:



\- predicted\_action\_loss

\- local\_mean\_error

\- local\_error\_std

\- local\_underestimate\_fraction

\- local\_severe\_underestimate\_fraction



The Experiment 101 scalar calibration probability was generated from these five variables using the frozen standardized logistic model.



Experiment 103 reconstructs these same five constituent quantities for the exact support-baseline action involved in each veto.



\---



\## Constituent-State Separation



\### Scalar Calibration Probability



Beneficial mean:



0.627705



Harmful mean:



0.566103



Difference:



\-0.061603



Standardized effect:



\-0.771



This reproduces the Experiment 102 result.



Within the already-vetoed population, harmful events do not have larger aggregate calibration-risk probabilities than beneficial events.



\---



\## Predicted Action Loss



Beneficial mean:



0.142071



Harmful mean:



0.138027



Difference:



\-0.004044



Standardized effect:



\-0.145



Predicted action loss provides little separation between harmful and beneficial vetoes.



\---



\## Local Mean Calibration Error



Beneficial mean:



0.016970



Harmful mean:



0.014350



Difference:



\-0.002620



Standardized effect:



\-0.122



Local mean error also provides little separation within the veto-conditioned population.



This differs from Experiment 099, where local mean error was one of the strongest predictors of severe underestimation across the full action-context population.



This suggests that a variable can be useful for identifying the broad calibration-risk regime without necessarily separating outcomes after conditioning on entry into that regime.



\---



\## Local Error Standard Deviation



Beneficial mean:



0.063231



Harmful mean:



0.088253



Difference:



+0.025022



Standardized effect:



\\\[

\\boxed{+1.274}

\\]



Historical local calibration-error variability therefore provides substantial separation between harmful and beneficial Experiment 101 vetoes.



Harmful vetoes occurred in neighborhoods where historical calibration outcomes were more dispersed.



\---



\## Local Underestimation Fraction



Beneficial mean:



0.369748



Harmful mean:



0.371429



Difference:



+0.001681



Standardized effect:



+0.014



Ordinary historical underestimation frequency provides essentially no separation between the two veto classes.



Again, this differs from its usefulness across the broader action-context population in Experiment 099.



\---



\## Local Severe-Underestimation Fraction



Beneficial mean:



0.117647



Harmful mean:



0.314286



Difference:



+0.196639



Standardized effect:



\\\[

\\boxed{+1.834}

\\]



This is the strongest constituent-state separation observed in Experiment 103.



Harmful vetoes occurred in historical neighborhoods containing substantially more severe consequence-underestimation events.



This suggests that once the twin has already entered a broad calibration-risk regime, the \*\*severity structure\*\* of historical failures may be more informative than general underestimation frequency.



\---



\## Harmful Event Profiles



\### Seed 44096 — Test Index 22



Calibration probability:



0.638082



Constituent profile:



\- predicted\_action\_loss: 0.189453

\- local\_mean\_error: 0.012203

\- local\_error\_std: 0.096197

\- local\_underestimate\_fraction: 0.428571

\- local\_severe\_underestimate\_fraction: 0.285714



Relative to beneficial vetoes:



\- predicted action loss percentile: 94.118%

\- local error standard-deviation percentile: 94.118%

\- severe-underestimation fraction percentile: 88.235%



This harmful event therefore combined high predicted loss with elevated historical calibration dispersion and elevated severe-failure frequency.



\---



\### Seed 44097 — Test Index 22



Calibration probability:



0.652996



Constituent profile:



\- predicted\_action\_loss: 0.137883

\- local\_mean\_error: -0.007579

\- local\_error\_std: 0.103012

\- local\_underestimate\_fraction: 0.571429

\- local\_severe\_underestimate\_fraction: 0.428571



Relative to beneficial vetoes:



\- local error standard-deviation percentile: 94.118%

\- local underestimation fraction percentile: 94.118%

\- local severe-underestimation fraction percentile: 100.000%



The severe-underestimation fraction is:



\\\[

0.428571

\\]



which exceeds every beneficial veto.



Its standardized distance relative to the beneficial severe-fraction distribution is:



\\\[

\\boxed{z=+2.690}.

\\]



This is the most extreme constituent-state profile among the harmful vetoes.



\---



\### Seed 44101 — Test Index 5



Calibration probability:



0.534127



Constituent profile:



\- predicted\_action\_loss: 0.106811

\- local\_mean\_error: 0.015768

\- local\_error\_std: 0.083618

\- local\_underestimate\_fraction: 0.285714

\- local\_severe\_underestimate\_fraction: 0.285714



Its severe-underestimation fraction lies near the 88th percentile relative to beneficial vetoes.



Its calibration probability is only moderately above the Experiment 101 threshold, yet its historical severe-failure fraction remains elevated.



\---



\### Seed 44103 — Test Index 4



Calibration probability:



0.521347



Constituent profile:



\- predicted\_action\_loss: 0.113596

\- local\_mean\_error: 0.019874

\- local\_error\_std: 0.083721

\- local\_underestimate\_fraction: 0.285714

\- local\_severe\_underestimate\_fraction: 0.285714



Again, the scalar probability is relatively modest, while severe historical failure frequency remains elevated.



\---



\### Seed 44108 — Test Index 38



Calibration probability:



0.483961



Constituent profile:



\- predicted\_action\_loss: 0.142394

\- local\_mean\_error: 0.031484

\- local\_error\_std: 0.074719

\- local\_underestimate\_fraction: 0.285714

\- local\_severe\_underestimate\_fraction: 0.285714



This event is particularly informative because its scalar calibration probability lies only slightly above the frozen Experiment 101 threshold:



\\\[

0.483961.

\\]



Nevertheless, its local severe-underestimation fraction again lies near the 88th percentile relative to beneficial vetoes.



This reinforces the Experiment 102 finding that harmfulness is not monotonically ordered by the aggregate probability score.



\---



\## Relationship Between Aggregate Probability and Constituents



Within the 22 veto events, calibration probability correlates strongly with:



\### Local Mean Error



\\\[

r=-0.781

\\]



\### Local Underestimation Fraction



\\\[

r=+0.793

\\]



These relationships are consistent with the structure of the original severe-underestimation classifier.



However, calibration probability is essentially uncorrelated with the two variables that most strongly distinguish harmful from beneficial vetoes:



\### Local Error Standard Deviation



\\\[

r=+0.013

\\]



\### Local Severe-Underestimation Fraction



\\\[

r=-0.026

\\]



This is a central Experiment 103 result.



The scalar calibration-risk probability emphasizes dimensions that predict severe underestimation across the full population, but the variables that distinguish harmful versus beneficial support expansions \*\*after conditioning on elevated calibration risk\*\* appear to be different.



\---



\## Conditional Geometry Interpretation



The experiments now suggest two distinct statistical problems.



\### Broad Calibration-Risk Detection



Across the full action-context population, useful predictors include:



\- local mean calibration error,

\- ordinary local underestimation frequency,

\- predicted action loss.



These variables help determine whether the consequence model is at elevated risk of severe underestimation.



\### Within-Risk Selectivity



After conditioning on:



\\\[

p\_{\\mathrm{cal}}\\ge\\tau\_{\\mathrm{cal}},

\\]



and restricting attention to support-admitted responsive expansions, harmful versus beneficial outcomes appear more associated with:



\- local severe-underestimation frequency,

\- local calibration-error dispersion.



Thus:



\\\[

\\boxed{

\\text{risk detection}

\\neq

\\text{within-risk action selectivity}.

}

\\]



A representation that performs well for the first problem need not solve the second.



\---



\## Hierarchical Interpretation



Experiment 103 motivates, but does not yet validate, a hierarchical control architecture.



Conceptually:



\\\[

\\text{Stage 1}

\\]



asks:



\*\*Is the consequence model locally unreliable enough that additional caution is justified?\*\*



This is represented by the prospectively validated Experiment 100/101 calibration-risk signal.



Then:



\\\[

\\text{Stage 2}

\\]



would ask:



\*\*Within that unreliable regime, does the historical neighborhood contain evidence of repeated severe consequence-model failures associated with this type of action?\*\*



The second stage may depend more strongly on:



\\\[

\\texttt{local\\\_severe\\\_underestimate\\\_fraction}

\\]



and:



\\\[

\\texttt{local\\\_error\\\_std}.

\\]



This interpretation remains a research hypothesis.



Experiment 103 does not define a second-stage controller.



\---



\## Why No New Threshold Is Defined



Only five harmful veto events are available in the Experiment 101 prospective block.



Four of those events have:



\\\[

\\texttt{local\\\_severe\\\_underestimate\\\_fraction}=0.285714

\\]



and one has:



\\\[

0.428571.

\\]



It would be tempting to turn approximately:



\\\[

0.285714

\\]



into a new intervention threshold.



That would be methodologically inappropriate.



The value is being observed after outcomes are known and from a population containing only five harmful events.



Therefore Experiment 103 does \*\*not\*\* define a threshold on severe-underestimation fraction, error variance, or any combination of constituent features.



\---



\## Primary Finding



The strongest pre-action constituent-state separation within the Experiment 101 veto population is:



\\\[

\\boxed{

\\texttt{local\\\_severe\\\_underestimate\\\_fraction}

}

\\]



with standardized difference:



\\\[

\\boxed{+1.834}.

\\]



The second strongest is:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}

}

\\]



with standardized difference:



\\\[

\\boxed{+1.274}.

\\]



By contrast:



\- predicted action loss,

\- local mean error,

\- and ordinary underestimation fraction



provide little harmful-versus-beneficial separation after conditioning on the existing calibration guard.



\---



\## Scientific Meaning



Experiment 103 provides evidence that the internal historical calibration state contains information that is lost when compressed into a single scalar calibration-risk probability.



The scalar probability remains prospectively useful as a broad danger signal, as demonstrated in Experiments 100 and 101.



However, the veto-conditioned population reveals a second structure:



\\\[

\\boxed{

\\text{repeated severe historical failure}

\+

\\text{greater historical error dispersion}

}

\\]



is more characteristic of harmful than beneficial responsive expansions.



This offers a plausible explanation for why threshold escalation failed in Experiment 102.



\---



\## Limitations



Experiment 103 is based on:



\- 22 veto events,

\- only 5 harmful vetoes,

\- one simulation architecture,

\- and already-observed Experiment 101 outcomes.



Therefore:



\- effect sizes may be unstable,

\- the observed severe-history pattern may be regime-specific,

\- no causal claim is established,

\- no new controller rule is justified,

\- and no prospective selectivity improvement has yet been demonstrated.



The constituent-state hypothesis requires replication on a larger historical support-expansion population before it should influence controller design.



\---



\## Experiment 103 Status



Experiment 103: COMPLETE



Primary diagnostic finding:



\*\*Harmful and beneficial Experiment 101 vetoes exhibit different internal calibration-state geometry despite overlapping aggregate calibration-risk probabilities.\*\*



Strongest constituent separation:



\- local severe-underestimation fraction: effect +1.834

\- local error standard deviation: effect +1.274



Simple scalar probability escalation remains unsupported.



\---



\## Next Research Direction



The next experiment should test whether the constituent-state pattern identified in Experiment 103 replicates across a broader population of already-consumed historical support-expansion events.



The central question should be:



\*\*Across historical support expansions, does elevated local severe-underestimation frequency and calibration-error dispersion consistently characterize harmful adaptations relative to beneficial adaptations?\*\*



This replication should use only previously consumed seeds.



No new controller threshold or prospective intervention should be defined unless that broader historical evidence supports the constituent-state mechanism.

