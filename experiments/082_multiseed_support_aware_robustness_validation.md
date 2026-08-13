\# Experiment 082 — Multi-Seed Support-Aware Robustness Validation



\## Objective



Experiment 081 identified a promising support-aware operating point at



\\\[

\\tau\_s=2.50

\\]



that, on development seed



\\\[

44000,

\\]



improved responsiveness while matching the primary gate's observed mean regret and under-persistence.



Because that operating point was discovered on a single development environment, Experiment 082 tests whether the result generalizes across genuinely distinct generated datasets.



To avoid validation leakage, the support thresholds were frozen before this experiment.



The validation seeds were:



\\\[

\\boxed{

44001,\\,

44002,\\,

44003,\\,

44004,\\,

44005,\\,

44006,\\,

44007,\\,

44008,\\,

44009,\\,

44010

}

\\]



and development seed



\\\[

44000

\\]



was deliberately excluded.



The central hypothesis was:



\\\[

\\boxed{

\\text{support-aware expansion improves responsiveness across seeds}

\\atop

\\text{without materially degrading consequence performance.}

}

\\]



The experiment compares:



\- the primary gate,

\- unfiltered cost-aware expansion,

\- support-aware expansion at \\(\\tau\_s=2.50\\),

\- support-aware expansion at \\(\\tau\_s=3.50\\),

\- the responsive-action oracle,

\- fixed \\(k=3\\),

\- and the unrestricted action oracle.



\---



\## Frozen Controller Parameters



The action-level safety-confidence threshold remained:



\\\[

\\boxed{

\\tau\_p=0.60.

}

\\]



The downside threshold remained:



\\\[

\\boxed{

\\tau\_d=0.020.

}

\\]



The two support thresholds carried forward from Experiment 081 were:



\\\[

\\boxed{

\\tau\_s=2.50

}

\\]



and



\\\[

\\boxed{

\\tau\_s=3.50.

}

\\]



No support threshold was tuned using the ten validation seeds.



\---



\## Validation Protocol



For each generation seed, the complete model stack was retrained independently.



Each generated dataset was split into:



1\. base-model training data,

2\. meta-model training data,

3\. held-out test data.



Thus each validation seed represents an independent realization of:



\- the trajectory population,

\- base loss and risk learning,

\- regret-model fitting,

\- action-safety learning,

\- downside estimation,

\- support geometry,

\- and held-out policy evaluation.



The final results therefore measure robustness to regenerated system populations rather than repeated evaluation on a single fixed dataset.



\---



\# Multi-Seed Results



\## Primary Baseline



Across the ten validation seeds, the primary gate achieved:



\\\[

\\boxed{

\\text{mean regret}

=

0.006225

}

\\]



with standard deviation



\\\[

0.002916.

\\]



Median regret was



\\\[

0.006076,

\\]



with seed-level range:



\\\[

\[0.002749,\\ 0.013601].

\\]



Mean under-persistence was:



\\\[

\\boxed{

6.70

}

\\]



with maximum seed-level under-persistence:



\\\[

16\.

\\]



Mean over-persistence was:



\\\[

51.40.

\\]



Mean action entropy was:



\\\[

0.715.

\\]



Safe-action metrics were:



\\\[

\\text{recall}

=

83.300\\%,

\\]



\\\[

\\text{precision}

=

94.892\\%,

\\]



and



\\\[

\\text{responsive retention}

=

72.102\\%.

\\]



This provides the principal multi-seed reference point.



\---



\# Unfiltered Cost-Aware Expansion



The cost-aware controller without support filtering achieved:



\\\[

\\text{mean regret}

=

0.008569.

\\]



Regret standard deviation was:



\\\[

0.003375.

\\]



The seed-level regret range was:



\\\[

\[0.003290,\\ 0.016734].

\\]



Mean under-persistence increased to:



\\\[

10.50,

\\]



with a maximum of:



\\\[

21\.

\\]



Mean over-persistence fell to:



\\\[

41.60.

\\]



Mean entropy increased substantially:



\\\[

0.899.

\\]



Safe-action recall reached:



\\\[

92.743\\%.

\\]



Responsive-action retention reached:



\\\[

88.702\\%.

\\]



However, safe-action precision decreased to:



\\\[

90.299\\%.

\\]



The controller produced an average of:



\\\[

3.90

\\]



harmful expansions per seed, with a maximum of:



\\\[

8\.

\\]



Mean beneficial expansions were:



\\\[

12.60

\\]



per seed.



Mean recovered responsive contexts were:



\\\[

12.80.

\\]



Thus unfiltered cost-aware expansion strongly improves responsiveness but incurs a substantial safety cost across seeds.



\---



\# Support-Aware Expansion at \\(\\tau\_s=2.50\\)



The conservative support-aware controller achieved:



\\\[

\\boxed{

\\text{mean regret}

=

0.007302

}

\\]



with standard deviation:



\\\[

0.003315.

\\]



Median regret was:



\\\[

0.007144.

\\]



Seed-level regret ranged from:



\\\[

0.002749

\\]



to:



\\\[

0.016272.

\\]



Mean under-persistence was:



\\\[

\\boxed{

8.20

}

\\]



with maximum:



\\\[

20\.

\\]



Mean over-persistence decreased to:



\\\[

47.30.

\\]



Mean entropy increased to:



\\\[

0.826.

\\]



Safe-action recall increased to:



\\\[

\\boxed{

86.824\\%

}

\\]



and responsive-action retention increased to:



\\\[

\\boxed{

78.889\\%.

}

\\]



Safe-action precision remained high:



\\\[

93.575\\%.

\\]



The controller produced an average of:



\\\[

\\boxed{

1.50

}

\\]



harmful expansions per seed.



Maximum harmful expansions in any seed were:



\\\[

4\.

\\]



Mean beneficial expansions were:



\\\[

5.00.

\\]



Mean recovered responsive contexts were:



\\\[

5.20.

\\]



\---



\# Responsiveness Improvement Relative to Primary Gate



The primary gate achieved responsive-action retention:



\\\[

72.102\\%.

\\]



Support-aware \\(2.50\\) achieved:



\\\[

78.889\\%.

\\]



The absolute improvement was therefore:



\\\[

\\boxed{

6.787

\\text{ percentage points}.

}

\\]



Safe-action recall increased from:



\\\[

83.300\\%

\\]



to:



\\\[

86.824\\%.

\\]



Mean over-persistence decreased from:



\\\[

51.40

\\]



to:



\\\[

47.30.

\\]



Entropy increased from:



\\\[

0.715

\\]



to:



\\\[

0.826.

\\]



Thus the controller consistently moves behavior toward greater responsiveness.



\---



\# Consequence Cost Relative to Primary Gate



The development-seed result from Experiment 081 did not generalize as a universally consequence-neutral improvement.



Mean regret increased from:



\\\[

0.006225

\\]



to:



\\\[

0.007302.

\\]



The absolute increase was:



\\\[

0.001077.

\\]



Relative to the primary mean, this is approximately:



\\\[

17.3\\%.

\\]



Mean under-persistence increased from:



\\\[

6.70

\\]



to:



\\\[

8.20.

\\]



Therefore:



\\\[

\\boxed{

\\text{support-aware }2.50

\\text{ improves responsiveness but does not preserve}

\\atop

\\text{baseline consequence performance across all validation seeds.}

}

\\]



This directly falsifies the strongest single-seed generalization hypothesis from Experiment 081.



\---



\# Validation Falsification Result



Experiment 081 suggested:



\\\[

\\text{more responsiveness}

\\]



with:



\\\[

\\text{no observed safety cost}

\\]



on seed



\\\[

44000\.

\\]



Experiment 082 demonstrates that this property does not hold robustly across independent generated populations.



The correct multi-seed conclusion is therefore:



\\\[

\\boxed{

\\text{support-aware expansion improves the responsiveness-safety frontier,}

\\atop

\\text{but does not universally preserve primary-gate consequence performance.}

}

\\]



This is a stronger scientific conclusion because it distinguishes a development-set success from a robustly generalizable guarantee.



\---



\# Support Filtering Still Generalizes



Although the zero-cost property does not generalize, support-aware filtering itself remains useful.



Compare the unfiltered cost-aware controller with support-aware \\(2.50\\).



\## Mean Regret



\\\[

0.008569

\\rightarrow

\\boxed{

0.007302

}.

\\]



\## Mean Under-Persistence



\\\[

10.50

\\rightarrow

\\boxed{

8.20

}.

\\]



\## Mean Harmful Expansions



\\\[

3.90

\\rightarrow

\\boxed{

1.50

}.

\\]



\## Maximum Harmful Expansions



\\\[

8

\\rightarrow

\\boxed{

4

}.

\\]



Thus training-support gating substantially reduces the consequence cost of responsive expansion.



This validates the architectural finding from Experiments 080 and 081 even though it does not eliminate all failures.



\---



\# Support-Aware Expansion at \\(\\tau\_s=3.50\\)



The more permissive support-aware configuration achieved:



\\\[

\\text{mean regret}

=

0.008509.

\\]



Regret standard deviation was:



\\\[

0.003389.

\\]



The seed-level regret range was:



\\\[

\[0.003290,\\ 0.016734].

\\]



Mean under-persistence was:



\\\[

9.90.

\\]



Maximum under-persistence was:



\\\[

21\.

\\]



Mean over-persistence decreased to:



\\\[

43.20.

\\]



Mean entropy increased to:



\\\[

0.887.

\\]



Safe-action recall reached:



\\\[

90.699\\%.

\\]



Safe-action precision was:



\\\[

92.019\\%.

\\]



Responsive-action retention was:



\\\[

85.739\\%.

\\]



Mean harmful expansions were:



\\\[

3.20

\\]



with maximum:



\\\[

7\.

\\]



Mean beneficial expansions were:



\\\[

10.30.

\\]



Mean recovered responsive contexts were:



\\\[

10.50.

\\]



\---



\# Comparison of the Two Support Modes



The conservative support mode:



\\\[

\\tau\_s=2.50

\\]



achieves:



\\\[

R=0.007302,

\\]



\\\[

N\_{\\text{under}}=8.20,

\\]



\\\[

\\text{retention}=78.889\\%,

\\]



and:



\\\[

1.50

\\]



mean harmful expansions.



The aggressive support mode:



\\\[

\\tau\_s=3.50

\\]



achieves:



\\\[

R=0.008509,

\\]



\\\[

N\_{\\text{under}}=9.90,

\\]



\\\[

\\text{retention}=85.739\\%,

\\]



and:



\\\[

3.20

\\]



mean harmful expansions.



Thus \\(\\tau\_s=3.50\\) buys additional responsiveness at substantial additional safety cost.



The conservative threshold remains the stronger candidate for further study.



\---



\# Comparison With Unfiltered Cost-Aware Expansion



The aggressive support controller at



\\\[

\\tau\_s=3.50

\\]



nearly approaches the unfiltered cost-aware controller.



Cost-aware:



\\\[

R=0.008569,

\\]



\\\[

N\_{\\text{under}}=10.50,

\\]



\\\[

\\text{retention}=88.702\\%.

\\]



Support \\(3.50\\):



\\\[

R=0.008509,

\\]



\\\[

N\_{\\text{under}}=9.90,

\\]



\\\[

\\text{retention}=85.739\\%.

\\]



Thus the larger support threshold retains some protective benefit, but much of the strong extrapolation filter disappears.



This reinforces the importance of the tighter threshold.



\---



\# Responsive-Action Oracle



The responsive-action oracle achieved:



\\\[

\\text{mean regret}

=

0.003602.

\\]



Regret standard deviation was:



\\\[

0.003181.

\\]



Median regret was:



\\\[

0.002345.

\\]



The seed-level range was:



\\\[

\[0.001594,\\ 0.012563].

\\]



Mean under-persistence was:



\\\[

3.70.

\\]



Mean over-persistence was:



\\\[

38.00.

\\]



Mean entropy was:



\\\[

0.914.

\\]



The responsive-action oracle has:



\\\[

100\\%

\\]



safe-action recall,



\\\[

100\\%

\\]



precision,



and



\\\[

100\\%

\\]



responsive-action retention.



\---



\# Why the Responsive-Action Oracle Has Nonzero Regret



The responsive-action oracle does not select from all possible persistence actions without restriction.



It chooses the least-persistent action among the minimum-regret actions represented by the candidate risk-policy family.



Therefore:



\\\[

R\_{\\text{responsive oracle}}

\\neq

0

\\]



in general.



The unrestricted action oracle remains the true zero-regret benchmark.



This distinction is important when interpreting the oracle gap.



\---



\# Fixed \\(k=3\\)



The fixed maximal-persistence policy achieved:



\\\[

\\boxed{

\\text{mean regret}

=

0.001793

}

\\]



with standard deviation:



\\\[

0.001045.

\\]



Mean under-persistence was:



\\\[

\\boxed{

0\.

}

\\]



Mean over-persistence was:



\\\[

64.50.

\\]



Entropy was:



\\\[

\\boxed{

0\.

}

\\]



Thus fixed \\(k=3\\) remains an extremely safe but behaviorally degenerate policy.



Its strong regret performance does not solve the adaptive responsiveness objective.



\---



\# Action Oracle



The unrestricted action oracle achieved:



\\\[

\\boxed{

R=0

}

\\]



across every seed.



Mean under-persistence was:



\\\[

0\.

\\]



Mean over-persistence was:



\\\[

0\.

\\]



Mean entropy was:



\\\[

0.920.

\\]



This remains the theoretical upper benchmark for adaptive action selection.



\---



\# Robustness Interpretation



Experiment 082 changes the interpretation of the support-aware architecture.



The result is not:



\\\[

\\boxed{

\\text{support gating eliminates the responsiveness-safety tradeoff}.

}

\\]



Instead, the correct conclusion is:



\\\[

\\boxed{

\\text{support gating shifts the tradeoff frontier in a favorable direction}.

}

\\]



It reduces harmful expansions substantially relative to cost-aware expansion while retaining useful responsive recovery.



However, it does not provide a cross-seed guarantee of zero additional consequence cost.



\---



\# Development Versus Validation



The experimental distinction between seed



\\\[

44000

\\]



and seeds



\\\[

44001\\text{--}44010

\\]



is methodologically important.



Seed



\\\[

44000

\\]



was used to:



\- identify the support-extrapolation failure mode,

\- select the support-distance metric,

\- identify the \\(2.50\\) and \\(3.50\\) operating points.



Therefore it belongs to the development process.



The ten new seeds were evaluated only after those choices were fixed.



This means Experiment 082 functions as a genuine out-of-development validation rather than an extension of threshold tuning.



\---



\# Falsification as a Positive Research Outcome



The failure of the exact zero-cost hypothesis is scientifically valuable.



Had the experiment only evaluated seed



\\\[

44000,

\\]



the controller might have been described too strongly as consequence-preserving.



Multi-seed validation shows that this claim would not be justified.



Instead, the evidence supports the narrower and more defensible statement:



\\\[

\\boxed{

\\text{support-aware gating improves responsive recovery}

\\atop

\\text{while reducing, but not eliminating, the safety cost of expansion.}

}

\\]



This strengthens the credibility of the experimental program.



\---



\# Remaining Question



The aggregate averages do not reveal whether the safety cost is:



1\. weakly distributed across nearly every seed, or

2\. concentrated in a small number of difficult generated populations.



This distinction matters.



If harmful expansions are concentrated in a few seeds, the dominant issue may be distribution shift.



If most seeds exhibit a similar modest cost, the controller may instead have a systematic calibration bias.



Thus the next diagnostic should work at the seed level rather than introducing another learned controller.



\---



\# Principal Conclusion



Experiment 082 provides the first genuine multi-seed validation of the support-aware safe-action controller.



The conservative support configuration:



\\\[

\\boxed{

\\tau\_s=2.50

}

\\]



improves mean responsive-action retention from:



\\\[

72.102\\%

\\]



to:



\\\[

78.889\\%,

\\]



improves safe-action recall from:



\\\[

83.300\\%

\\]



to:



\\\[

86.824\\%,

\\]



reduces mean over-persistence from:



\\\[

51.40

\\]



to:



\\\[

47.30,

\\]



and increases mean entropy from:



\\\[

0.715

\\]



to:



\\\[

0.826.

\\]



However, mean regret increases:



\\\[

0.006225

\\rightarrow

0.007302,

\\]



and mean under-persistence increases:



\\\[

6.70

\\rightarrow

8.20.

\\]



Therefore the zero-observed-safety-cost result from Experiment 081 does not generalize across independent generation seeds.



At the same time, support-aware gating materially improves over unfiltered cost-aware expansion by reducing:



\\\[

\\text{mean harmful expansions}

:

3.90

\\rightarrow

1.50

\\]



and reducing mean regret:



\\\[

0.008569

\\rightarrow

0.007302.

\\]



The central conclusion is therefore:



\\\[

\\boxed{

\\text{training-support-aware gating is a robustly useful safety filter,}

\\atop

\\text{but not a universal consequence-preservation guarantee.}

}

\\]



\---



\## Next Research Direction



Experiment 083 should perform seed-level failure decomposition using the already-generated Experiment 082 validation results.



No new controller parameters should be tuned against the validation seeds.



The analysis should determine, for each generation seed:



\- primary mean regret,

\- support-aware mean regret,

\- regret delta,

\- primary under-persistence,

\- support-aware under-persistence,

\- under-persistence delta,

\- responsive-retention gain,

\- safe-action-recall gain,

\- over-persistence reduction,

\- beneficial expansion count,

\- harmful expansion count,

\- recovered responsive contexts,

\- and the ratio of beneficial to harmful expansions.



The experiment should then characterize whether harmful expansion is:



\\\[

\\boxed{

\\text{seed-concentrated}

}

\\]



or



\\\[

\\boxed{

\\text{systematically distributed}.

}

\\]



It should identify:



\- the number of seeds where support \\(2.50\\) matches or improves primary regret,

\- the number where regret increases,

\- the number with zero harmful expansions,

\- the worst seed-level safety degradation,

\- and the relationship between responsive gain and safety cost.



The central question becomes:



\\\[

\\boxed{

\\text{Is the remaining multi-seed consequence cost driven by}

\\atop

\\text{rare distribution-shift failures or a systematic expansion bias?}

}

\\]



The answer should determine whether the next research step should focus on distribution-shift detection, calibration, or a fundamentally different expansion objective.

