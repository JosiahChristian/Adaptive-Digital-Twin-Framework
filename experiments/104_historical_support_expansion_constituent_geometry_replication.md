\# Experiment 104 — Historical Support-Expansion Constituent Geometry Replication



\## Purpose



Experiment 103 identified two constituent historical calibration-state variables that strongly separated harmful from beneficial vetoes within the Experiment 101 calibration-guard population:



\- local\_error\_std

\- local\_severe\_underestimate\_fraction



The Experiment 103 standardized differences were:



\- local\_error\_std: +1.274

\- local\_severe\_underestimate\_fraction: +1.834



However, Experiment 103 contained only 22 vetoes, including only 5 harmful events.



Those outcomes had already been observed when the constituent-state hypothesis was formulated.



Experiment 104 therefore performs a separate retrospective replication using an already-consumed seed block that is independent of the Experiment 101 veto sample used for the Experiment 103 discovery.



The central question is:



\*\*Do the constituent-state directions observed in Experiment 103 reproduce among ordinary harmful versus beneficial support-baseline expansions outside the Experiment 101 discovery population?\*\*



Experiment 104 is a replication and falsification experiment.



It does not define or modify a controller.



\---



\## Replication Population



Replication seeds:



44071-44090



These seeds were previously consumed by Experiment 100.



They are distinct from the Experiment 101 controller block:



44091-44110



from which the Experiment 103 constituent-state hypothesis was derived.



Therefore Experiment 104 does not reuse the 22 Experiment 101 veto events as its replication population.



No new prospective seeds are introduced.



\---



\## Replication Target



Experiment 104 reconstructs support-baseline responsive expansions on seeds 44071-44090.



Only labeled expansions are included:



\- beneficial expansions

\- harmful expansions



The calibration guard itself is not the outcome under study.



The question is whether the historical calibration-state geometry associated with harmful support expansion reproduces outside the Experiment 101 veto-conditioned population.



\---



\## Replication Event Population



Total labeled support expansions:



39



Beneficial expansions:



37



Harmful expansions:



2



Seeds with harmful expansions:



2 / 20



The small harmful-event population is a major limitation and constrains the strength of any positive or negative replication claim.



\---



\## Constituent Geometry Results



\### Predicted Action Loss



Beneficial mean:



0.169877



Harmful mean:



0.203677



Difference:



+0.033800



Standardized effect:



+0.636



Rank AUC for harmful-high ordering:



0.622



This variable was not a primary Experiment 103 replication target.



\---



\## Local Mean Error



Beneficial mean:



0.073829



Harmful mean:



0.048380



Difference:



\-0.025449



Standardized effect:



\-0.693



Rank AUC:



0.311



This variable was not a primary Experiment 103 replication target.



\---



\## Local Error Standard Deviation



Beneficial mean:



0.052755



Harmful mean:



0.068422



Difference:



+0.015667



Standardized effect:



\\\[

\\boxed{+0.773}

\\]



Rank AUC:



\\\[

\\boxed{0.716}

\\]



Experiment 103 direction:



harmful higher



Experiment 104 direction:



harmful higher



Directional replication:



\\\[

\\boxed{\\text{TRUE}}

\\]



Thus, the elevated local calibration-error dispersion observed among harmful Experiment 101 vetoes reproduces directionally in the independent Experiment 104 support-expansion population.



The magnitude is smaller than in Experiment 103:



\\\[

+1.274 \\rightarrow +0.773,

\\]



but remains positive and nontrivial.



Because only two harmful events occur in Experiment 104, this result should be interpreted as directional replication rather than definitive validation.



\---



\## Local Underestimation Fraction



Beneficial mean:



0.119691



Harmful mean:



0.285714



Difference:



+0.166023



Standardized effect:



\\\[

\\boxed{+1.194}

\\]



Rank AUC:



\\\[

\\boxed{0.791}

\\]



This is one of the strongest separations observed in Experiment 104.



However, local\_underestimate\_fraction was \*\*not\*\* one of the two primary Experiment 103 replication features.



Its strong Experiment 104 result is therefore exploratory.



It must not be promoted post hoc into a validated second-stage controller variable based on this experiment.



The observation may motivate later analysis, but it does not replace the preregistered Experiment 103 replication targets.



\---



\## Local Severe-Underestimation Fraction



Beneficial mean:



0.038610



Harmful mean:



0.000000



Difference:



\-0.038610



Standardized effect:



\\\[

\\boxed{-0.451}

\\]



Rank AUC:



\\\[

\\boxed{0.405}

\\]



Experiment 103 direction:



harmful higher



Experiment 104 direction:



harmful lower



Directional replication:



\\\[

\\boxed{\\text{FALSE}}

\\]



This is a direct failure to reproduce the strongest Experiment 103 constituent-state result.



Experiment 103 observed:



\\\[

d=+1.834

\\]



for local severe-underestimation fraction.



Experiment 104 instead observes:



\\\[

d=-0.451.

\\]



Therefore the hypothesis that harmful support expansions generally occupy neighborhoods with larger local severe-underestimation fractions is \*\*not supported as a stable cross-population mechanism by Experiment 104\*\*.



This negative result must be retained.



\---



\## Primary Replication Result



The two Experiment 103 primary constituent-state directions were:



1\. local\_error\_std — harmful higher

2\. local\_severe\_underestimate\_fraction — harmful higher



Experiment 104 results:



1\. local\_error\_std — replicated

2\. local\_severe\_underestimate\_fraction — not replicated



Therefore:



\\\[

\\boxed{

\\text{primary directions replicated}=1/2

}

\\]



Experiment 104 is a \*\*partial replication\*\*, not a confirmation of the complete Experiment 103 constituent geometry.



\---



\## Seed-Level Stability



The replication population contains only two harmful expansions across two seeds.



Because within-seed harmful-versus-beneficial comparison requires both classes to occur within the same seed, the available seed-level evidence is extremely sparse.



For local\_error\_std:



\- informative seeds: 1

\- harmful-higher seeds: 1



For local\_severe\_underestimate\_fraction:



\- informative seeds: 1

\- harmful-higher seeds: 0



This is insufficient for a strong seed-stability claim.



\---



\## Relationship to Experiment 103



Experiment 103 suggested that, after conditioning on elevated scalar calibration risk, harmful vetoes might be characterized by:



\\\[

\\text{greater severe historical failure frequency}

\+

\\text{greater calibration-error dispersion}.

\\]



Experiment 104 does not support this complete two-variable interpretation.



Instead, it separates the two components.



\### Error Dispersion



The harmful-higher direction survives:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}

}

\\]



Experiment 103:



\\\[

d=+1.274

\\]



Experiment 104:



\\\[

d=+0.773.

\\]



\### Severe Historical Failure Frequency



The harmful-higher direction does not survive:



\\\[

\\boxed{

\\texttt{local\\\_severe\\\_underestimate\\\_fraction}

}

\\]



Experiment 103:



\\\[

d=+1.834

\\]



Experiment 104:



\\\[

d=-0.451.

\\]



Therefore the Experiment 103 severe-history result may reflect:



\- the small five-event harmful sample,

\- conditioning on the Experiment 101 calibration guard,

\- a regime-specific relationship,

\- or ordinary sampling variability.



Further evidence is required before distinguishing among these possibilities.



\---



\## Important Exploratory Observation



Experiment 104 identifies an exploratory signal in:



\\\[

\\texttt{local\\\_underestimate\\\_fraction}.

\\]



Its standardized difference is:



\\\[

+1.194

\\]



with rank AUC:



\\\[

0.791.

\\]



This observation is scientifically interesting because ordinary underestimation frequency was useful in the earlier broad calibration-risk representation and now also separates the two harmful replication events from beneficial support expansions.



However, this signal was not specified as a primary Experiment 104 replication target.



Accordingly:



\\\[

\\boxed{

\\text{exploratory evidence}

\\neq

\\text{validated controller criterion}.

}

\\]



No intervention rule should be constructed from this result alone.



\---



\## Falsification Outcome



Experiment 104 successfully performs an important falsification function.



Had Experiment 103 immediately been converted into a controller rule, local severe-underestimation fraction would likely have been treated as the strongest candidate constituent because its discovery effect size was:



\\\[

+1.834.

\\]



Experiment 104 demonstrates that this would have been premature.



On the independent replication population, the effect reverses direction.



Thus the experiment prevents a five-event discovery from being mistaken for a stable mechanism.



\---



\## What Experiment 104 Supports



Experiment 104 provides limited evidence that:



1\. Local calibration-error dispersion may contain information about harmful support expansion beyond the scalar calibration probability.



2\. The harmful-higher direction of local\_error\_std appears in both Experiment 103 and Experiment 104.



3\. Ordinary local underestimation frequency is an exploratory candidate worthy of further investigation.



4\. Constituent calibration geometry may vary across regimes and should not be inferred from one small veto-conditioned population.



\---



\## What Experiment 104 Does Not Support



Experiment 104 does not support the claim that:



1\. The complete Experiment 103 constituent geometry has replicated.



2\. Elevated local severe-underestimation fraction is a stable general marker of harmful support expansion.



3\. local\_error\_std has been sufficiently validated for controller deployment.



4\. local\_underestimate\_fraction should now become a controller threshold.



5\. A second-stage calibration guard has been solved.



6\. The selectivity problem identified in Experiments 101-103 is resolved.



\---



\## Limitations



The principal limitation is class scarcity.



The replication population contains:



\\\[

37

\\]



beneficial expansions but only:



\\\[

2

\\]



harmful expansions.



Consequently:



\- standardized effects are unstable,

\- rank AUC estimates are highly sensitive to individual events,

\- seed-level replication cannot be assessed robustly,

\- direction reversals may reflect sampling variation,

\- and positive directional replication may also reflect sampling variation.



Experiment 104 should therefore be treated as a falsification-oriented replication rather than a definitive parameter-estimation study.



\---



\## Methodological Constraint



No Experiment 104 observation may be used to silently redefine the Experiment 103 hypothesis.



In particular, the strong exploratory local\_underestimate\_fraction result may not replace the failed local\_severe\_underestimate\_fraction replication and then be described as if the original hypothesis succeeded.



The correct record is:



\\\[

\\boxed{

1/2\\text{ primary constituent directions replicated.}

}

\\]



\---



\## Scientific Interpretation



The evidence now suggests that compressing historical calibration state into one scalar risk probability may indeed discard potentially useful structure.



However, the specific structure is not yet stable enough to define.



Across Experiments 103 and 104, the most persistent candidate is:



\\\[

\\boxed{

\\text{local calibration-error dispersion}

}

\\]



rather than severe historical failure frequency.



At the same time, Experiment 104 raises an exploratory possibility involving ordinary historical underestimation frequency.



These competing possibilities require evaluation over a substantially larger historical support-expansion population.



\---



\## Experiment 104 Status



Experiment 104: COMPLETE



Primary outcome:



\\\[

\\boxed{\\text{PARTIAL REPLICATION}}

\\]



Primary Experiment 103 directions reproduced:



\\\[

\\boxed{1/2}

\\]



Replicated:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}

}

\\]



Not replicated:



\\\[

\\boxed{

\\texttt{local\\\_severe\\\_underestimate\\\_fraction}

}

\\]



Exploratory signal:



\\\[

\\boxed{

\\texttt{local\\\_underestimate\\\_fraction}

}

\\]



No new controller rule is justified.



\---



\## Next Research Direction



The next experiment should broaden the retrospective population while preserving block-level and seed-level structure.



Its purpose should be to determine whether any constituent calibration-state relationship remains stable across multiple already-consumed historical regimes.



The analysis should specifically distinguish:



\- discovery effects,

\- replication effects,

\- exploratory effects,

\- block-to-block heterogeneity,

\- seed-level stability,

\- harmful-event scarcity,

\- and pooled effects that may conceal regime dependence.



The next experiment should therefore ask:



\*\*Across multiple previously consumed seed blocks, which historical calibration-state features, if any, consistently distinguish harmful from beneficial support expansions without relying on the Experiment 101 veto-conditioned discovery sample?\*\*



No new prospective controller experiment should begin until that stability question has been answered.

