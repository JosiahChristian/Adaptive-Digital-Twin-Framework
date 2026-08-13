\# Experiment 105 — Cross-Block Constituent Stability Analysis



\## Purpose



Experiments 103 and 104 investigated whether the internal historical calibration-state geometry associated with harmful support expansions contains structure that is lost when compressed into the scalar calibration-risk probability.



Experiment 103 identified two strong constituent signals within the Experiment 101 veto-conditioned population:



\- `local\_error\_std`

\- `local\_severe\_underestimate\_fraction`



Experiment 104 then tested those directions on a separate already-consumed historical block and produced only a partial replication.



In particular:



\- `local\_error\_std` replicated directionally,

\- `local\_severe\_underestimate\_fraction` reversed direction,

\- and `local\_underestimate\_fraction` emerged as a strong exploratory signal.



Experiment 105 therefore broadens the analysis from single-block replication to explicit cross-block stability.



The central question is:



\*\*Which constituent historical calibration-state variables maintain harmful-versus-beneficial direction and ranking behavior across multiple already-consumed support-expansion blocks?\*\*



Experiment 105 is a stability and falsification analysis.



It does not:



\- define a new controller threshold,

\- fit a new intervention rule,

\- introduce a new prospective seed block,

\- or modify the Experiment 101 calibration-aware controller.



\---



\## Historical Blocks



Experiment 105 analyzes two already-consumed blocks.



\### Block 1



`block\_071\_090`



Seeds:



44071-44090



This block was originally consumed by Experiment 100.



\### Block 2



`block\_091\_110`



Seeds:



44091-44110



This block was originally consumed by Experiment 101.



No new prospective outcomes are generated.



\---



\## Support-Expansion Event Populations



\### Block 071-090



Beneficial support expansions:



37



Harmful support expansions:



2



Total labeled support expansions:



39



Seeds containing harmful support expansions:



2



\### Block 091-110



Beneficial support expansions:



43



Harmful support expansions:



6



Total labeled support expansions:



49



Seeds containing harmful support expansions:



6



The harmful-event population remains small in both blocks.



Accordingly, Experiment 105 focuses on directional consistency and block heterogeneity rather than treating pooled effect sizes as definitive parameter estimates.



\---



\# Block-Level Results



\## Predicted Action Loss



\### Block 071-090



Difference:



\\\[

+0.033800

\\]



Standardized effect:



\\\[

+0.636

\\]



Rank AUC:



\\\[

0.622

\\]



Harmful higher:



yes



\### Block 091-110



Difference:



\\\[

\-0.024295

\\]



Standardized effect:



\\\[

\-0.808

\\]



Rank AUC:



\\\[

0.267

\\]



Harmful higher:



no



\### Cross-Block Interpretation



Predicted action loss reverses direction between blocks.



Direction stability:



\\\[

\\boxed{50\\%}

\\]



Mean standardized effect:



\\\[

\-0.086

\\]



Effect range:



\\\[

\[-0.808,\\ +0.636]

\\]



Mean rank AUC:



\\\[

0.445

\\]



Therefore predicted action loss is not a stable harmful-high selector across these blocks.



\---



\## Local Mean Calibration Error



\### Block 071-090



Difference:



\\\[

\-0.025449

\\]



Standardized effect:



\\\[

\-0.693

\\]



Rank AUC:



\\\[

0.311

\\]



\### Block 091-110



Difference:



\\\[

\-0.039288

\\]



Standardized effect:



\\\[

\-1.045

\\]



Rank AUC:



\\\[

0.217

\\]



\### Cross-Block Interpretation



Local mean error is directionally stable in the sense that harmful events have lower values in both blocks.



However, because Experiment 105 defines harmful-high stability as the primary selector orientation, harmful-higher blocks are:



\\\[

0/2.

\\]



Mean standardized effect:



\\\[

\-0.869

\\]



Effect range:



\\\[

\[-1.045,\\ -0.693]

\\]



Mean rank AUC:



\\\[

0.264

\\]



Thus, local mean error shows consistent inverse association with harmful support expansion but is not naturally interpretable as a harmful-high second-stage selector without reversing its orientation.



This variable remains scientifically relevant but is not the most direct candidate for a simple monotonic harmful-high rule.



\---



\## Local Error Standard Deviation



\### Block 071-090



Beneficial versus harmful difference:



\\\[

+0.015667

\\]



Standardized effect:



\\\[

+0.773

\\]



Rank AUC:



\\\[

0.716

\\]



Harmful higher:



yes



\### Block 091-110



Difference:



\\\[

+0.030733

\\]



Standardized effect:



\\\[

+1.672

\\]



Rank AUC:



\\\[

0.895

\\]



Harmful higher:



yes



\### Cross-Block Stability



Harmful-higher blocks:



\\\[

\\boxed{2/2}

\\]



Direction stability:



\\\[

\\boxed{100\\%}

\\]



Mean standardized effect:



\\\[

\\boxed{+1.223}

\\]



Effect range:



\\\[

\\boxed{\[+0.773,\\ +1.672]}

\\]



Mean rank AUC:



\\\[

\\boxed{0.806}

\\]



This is one of the strongest and most stable constituent-state signals observed across the two historical blocks.



The harmful-higher direction reproduces in both blocks despite different event populations and different harmful-event counts.



\---



\## Local Underestimation Fraction



\### Block 071-090



Difference:



\\\[

+0.166023

\\]



Standardized effect:



\\\[

+1.194

\\]



Rank AUC:



\\\[

0.791

\\]



Harmful higher:



yes



\### Block 091-110



Difference:



\\\[

+0.163898

\\]



Standardized effect:



\\\[

+0.903

\\]



Rank AUC:



\\\[

0.752

\\]



Harmful higher:



yes



\### Cross-Block Stability



Harmful-higher blocks:



\\\[

\\boxed{2/2}

\\]



Direction stability:



\\\[

\\boxed{100\\%}

\\]



Mean standardized effect:



\\\[

\\boxed{+1.049}

\\]



Effect range:



\\\[

\\boxed{\[+0.903,\\ +1.194]}

\\]



Mean rank AUC:



\\\[

\\boxed{0.771}

\\]



This variable therefore reproduces strongly across both historical blocks.



Although it was exploratory in Experiment 104, Experiment 105 now shows that its harmful-higher direction is not confined to one block.



Accordingly, `local\_underestimate\_fraction` becomes a serious candidate for further historical selectivity analysis.



It is still not yet a validated controller criterion.



\---



\## Local Severe-Underestimation Fraction



\### Block 071-090



Difference:



\\\[

\-0.038610

\\]



Standardized effect:



\\\[

\-0.451

\\]



Rank AUC:



\\\[

0.405

\\]



Harmful higher:



no



\### Block 091-110



Difference:



\\\[

+0.225914

\\]



Standardized effect:



\\\[

+2.397

\\]



Rank AUC:



\\\[

0.934

\\]



Harmful higher:



yes



\### Cross-Block Stability



Harmful-higher blocks:



\\\[

1/2

\\]



Direction stability:



\\\[

\\boxed{50\\%}

\\]



Mean standardized effect:



\\\[

+0.973

\\]



Effect range:



\\\[

\\boxed{\[-0.451,\\ +2.397]}

\\]



Mean rank AUC:



\\\[

0.670

\\]



This is a critical example of why block-level analysis is necessary.



The average effect is large and positive, but the effect reverses direction between blocks.



Therefore the pooled or average magnitude would substantially overstate the stability of this feature.



The correct interpretation is:



\\\[

\\boxed{

\\texttt{local\\\_severe\\\_underestimate\\\_fraction}

\\text{ is regime-unstable across the analyzed blocks.}

}

\\]



\---



\# Cross-Block Stability Summary



The constituent signals separate naturally into three categories.



\## Stable Harmful-High Signals



\### Local Error Standard Deviation



Direction stability:



\\\[

100\\%

\\]



Mean effect:



\\\[

+1.223

\\]



Mean rank AUC:



\\\[

0.806

\\]



\### Local Underestimation Fraction



Direction stability:



\\\[

100\\%

\\]



Mean effect:



\\\[

+1.049

\\]



Mean rank AUC:



\\\[

0.771

\\]



These are the only two constituent variables that maintain the same harmful-higher direction across both blocks.



\---



\## Stable Inverse Signal



\### Local Mean Error



Direction is consistently harmful-lower.



Mean effect:



\\\[

\-0.869

\\]



Mean rank AUC under harmful-high orientation:



\\\[

0.264

\\]



This may still carry useful information if explicitly oriented in the inverse direction.



However, Experiment 105 does not redefine or transform it into a controller score.



\---



\## Unstable Signals



\### Predicted Action Loss



Direction stability:



\\\[

50\\%

\\]



Effect range crosses zero strongly.



\### Local Severe-Underestimation Fraction



Direction stability:



\\\[

50\\%

\\]



Effect range:



\\\[

\[-0.451,\\ +2.397]

\\]



These variables should not be treated as stable harmful-high selectors based on the present evidence.



\---



\# Primary Finding



The strongest cross-block result is:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}

}

\\]



and:



\\\[

\\boxed{

\\texttt{local\\\_underestimate\\\_fraction}

}

\\]



both maintain:



\\\[

\\boxed{100\\%\\text{ harmful-higher direction stability}}

\\]



across the two analyzed historical blocks.



Their mean standardized effects are:



\\\[

\\boxed{

+1.223

}

\\]



and:



\\\[

\\boxed{

+1.049

}

\\]



respectively.



Their mean harmful-high rank AUC values are:



\\\[

\\boxed{

0.806

}

\\]



and:



\\\[

\\boxed{

0.771.

}

\\]



These are the most stable constituent-state relationships identified so far for distinguishing harmful from beneficial support expansions.



\---



\# Relationship to Experiments 103 and 104



Experiment 103 originally identified:



\- local\_error\_std

\- local\_severe\_underestimate\_fraction



as strong harmful-versus-beneficial separators within the Experiment 101 veto-conditioned population.



Experiment 104 then showed:



\- local\_error\_std replicated,

\- local\_severe\_underestimate\_fraction did not,

\- local\_underestimate\_fraction emerged exploratorily.



Experiment 105 resolves that tension more clearly.



Across both reconstructed historical blocks:



\### local\_error\_std



remains stable.



\### local\_underestimate\_fraction



also remains stable.



\### local\_severe\_underestimate\_fraction



does not.



Therefore the current evidence favors:



\\\[

\\boxed{

\\text{error dispersion}

\+

\\text{ordinary underestimation frequency}

}

\\]



over:



\\\[

\\boxed{

\\text{severe-underestimation frequency alone}

}

\\]



as the more stable constituent geometry.



\---



\# Why Pooled Effects Are Insufficient



Experiment 105 demonstrates that a large average effect can be misleading when the direction changes across blocks.



For example:



\\\[

\\texttt{local\\\_severe\\\_underestimate\\\_fraction}

\\]



has a positive mean effect:



\\\[

+0.973,

\\]



yet its block-specific effects are:



\\\[

\-0.451

\\]



and:



\\\[

+2.397.

\\]



A pooled or average-only analysis could therefore incorrectly suggest stable usefulness.



The appropriate interpretation must preserve:



\- block direction,

\- block magnitude,

\- event scarcity,

\- and regime heterogeneity.



\---



\# Harmful-Event Scarcity



The total harmful support-expansion population remains small:



\\\[

2+6=8

\\]



harmful events across the two blocks.



Beneficial expansions total:



\\\[

37+43=80.

\\]



Thus:



\\\[

\\boxed{

80\\text{ beneficial}

\\quad\\text{vs}\\quad

8\\text{ harmful}.

}

\\]



This is a larger harmful population than Experiments 103 or 104 individually, but it remains insufficient for a strong final controller-design claim.



The stable direction of the two leading features is encouraging, but effect magnitudes and ranking estimates remain sensitive to small numbers of harmful events.



\---



\# What Experiment 105 Supports



Experiment 105 supports the claim that:



1\. `local\_error\_std` is directionally stable across both analyzed historical support-expansion blocks.



2\. `local\_underestimate\_fraction` is directionally stable across both blocks.



3\. The two variables both show nontrivial harmful-high rank separation.



4\. `local\_severe\_underestimate\_fraction` is not stable across blocks despite its large effect in Experiment 103.



5\. Cross-block analysis materially changes the interpretation compared with single-block or pooled analysis.



\---



\# What Experiment 105 Does Not Support



Experiment 105 does not establish that:



1\. either stable feature is causally responsible for harmful adaptation;



2\. either feature should be immediately converted into a controller threshold;



3\. a two-feature selector is already validated;



4\. the observed relationships will generalize prospectively to a new regime;



5\. the selectivity cost of Experiment 101 has been solved;



6\. the calibration-aware controller should yet be modified.



\---



\# Current Best Constituent Candidates



Based on cross-block stability, the strongest current candidates for further historical selectivity analysis are:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}

}

\\]



and:



\\\[

\\boxed{

\\texttt{local\\\_underestimate\\\_fraction}.

}

\\]



The next analysis should test whether these two features jointly define a more selective harmful-expansion region than either alone.



That analysis should preserve block-held-out validation.



\---



\# Next Research Question



The next scientific question is:



\*\*Can a compact two-feature representation based on local calibration-error dispersion and ordinary historical underestimation frequency distinguish harmful from beneficial support expansions in a block-generalizable way?\*\*



The proper next step is not to deploy a new controller.



Instead, a historical decision-geometry analysis should evaluate:



\- each feature individually,

\- the two-feature combination,

\- interaction structure,

\- block-held-out discrimination,

\- seed stability,

\- and sensitivity to the small harmful-event population.



Only if that compact representation survives block-held-out validation should a new prospective intervention be considered.



\---



\## Experiment 105 Status



Experiment 105: COMPLETE



Primary stability result:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}

\\text{ and }

\\texttt{local\\\_underestimate\\\_fraction}

}

\\]



are the only constituent features in the analyzed set with:



\\\[

\\boxed{100\\%\\text{ harmful-higher direction stability}}

\\]



across both historical blocks.



No new controller rule is defined.

