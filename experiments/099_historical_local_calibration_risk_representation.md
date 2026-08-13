\# Experiment 099 — Historical Local Calibration-Risk Representation



\## Objective



Determine whether historical local consequence-model calibration behavior contains pre-action information about the risk of severe future consequence underestimation.



The experiment tests the hypothesis that an adaptive digital twin can estimate not only the magnitude of a predicted consequence, but also the local historical reliability of its own consequence model.



The central question is:



> Can historical prediction errors from locally similar action-context observations identify situations in which the consequence model is likely to severely underestimate realized loss?



This experiment is retrospective representation analysis only. No new controller rule or safety threshold is introduced.



\---



\## Motivation



Experiments 094–098 progressively indicated that harmful responsive expansions were more closely associated with consequence-model underestimation than with simple epistemic distance or unusually large predicted loss.



Experiment 098 provided a particularly useful prospective example.



The single harmful event vetoed by the frozen loss-ceiling guard occurred at:



\- generation seed: `44063`

\- test index: `41`

\- primary action: `3`

\- support-baseline action: `2`



Its pre-action quantities were not unusually extreme relative to the four beneficial events vetoed by the same guard:



\- predicted loss ceiling: `0.204651`

\- predicted baseline action loss: `0.197763`

\- context support distance: `1.504894`



The harmful event's predicted loss ceiling and predicted baseline action loss were both approximately at the 50th percentile of the beneficial-veto distribution.



Its context support distance was lower than every beneficial veto.



The distinguishing retrospective consequence was instead:



\\\[

\\hat L - L

=

0.197763 - 0.250827

=

\-0.053064

\\]



which crossed the previously defined severe-underestimation threshold:



\\\[

e < -0.050.

\\]



The event also produced realized regret:



\\\[

R = 0.010009.

\\]



This suggested that a static measure of current prediction magnitude may be insufficient. A more useful representation may be the historical local calibration behavior of the consequence model itself.



\---



\## Hypothesis



Let the consequence-model calibration error for historical observation \\(i\\) be



\\\[

e\_i = \\hat L\_i - L\_i,

\\]



where:



\- \\(\\hat L\_i\\) is predicted loss,

\- \\(L\_i\\) is realized loss.



Negative calibration error therefore represents consequence underestimation.



For a current context-action pair \\((x,a)\\), define a local historical neighborhood



\\\[

\\mathcal{N}\_K(x,a)

\\]



containing the \\(K\\) most similar historical observations for the same action.



A local calibration-state variable can then be represented by quantities such as



\\\[

\\bar e\_{\\mathcal N}(x,a)

=

\\frac{1}{K}

\\sum\_{i\\in\\mathcal N\_K(x,a)}

e\_i.

\\]



The hypothesis is:



\\\[

\\bar e\_{\\mathcal N}(x,a)\\downarrow

\\quad\\Longrightarrow\\quad

P(

\\text{severe consequence underestimation}

)\\uparrow.

\\]



More generally, regions with histories containing frequent or severe negative calibration errors should have elevated risk of future consequence underestimation.



\---



\## Experimental Design



\### Analysis Seeds



The experiment reconstructed seeds



\\\[

44001\\text{–}44070.

\\]



These seeds had already been consumed by previous retrospective and prospective experiments.



No fresh prospective validation block was consumed.



\### Local Neighborhood Size



\\\[

K = 7.

\\]



Historical calibration statistics were computed from the seven nearest historical observations associated with the same candidate action.



\### Severe-Underestimation Target



Severe consequence underestimation was defined as:



\\\[

\\hat L-L < -0.050.

\\]



\### Event Population



The reconstructed dataset contained:



\- action-context rows: `17,997`

\- nonsevere rows: `16,357`

\- severe-underestimation rows: `1,640`



Therefore:



\\\[

P(\\text{severe underestimation})

=

9.113\\%.

\\]



\---



\## Historical Calibration Representation



For each current action-context pair, the experiment constructed historical local features including:



1\. local mean calibration error,

2\. local median calibration error,

3\. local calibration-error standard deviation,

4\. local fraction of underestimated historical consequences,

5\. local fraction of severely underestimated historical consequences,

6\. local mean neighbor distance,

7\. local minimum historical calibration error.



The current realized consequence was not included in these predictor variables.



The current outcome was used only to construct the retrospective severe-underestimation target.



\---



\## Local Calibration Feature Separation



\### Predicted Action Loss



Nonsevere mean:



\\\[

0.259404

\\]



Severe mean:



\\\[

0.189448

\\]



Difference:



\\\[

\-0.069957

\\]



Standardized effect:



\\\[

\-0.513.

\\]



Current predicted loss therefore contained some information about severe-underestimation risk, but it was not the strongest representation.



\---



\### Local Mean Calibration Error



Nonsevere:



\\\[

0.117676

\\]



Severe:



\\\[

0.013459

\\]



Difference:



\\\[

\-0.104216

\\]



Standardized effect:



\\\[

\\boxed{-0.787}.

\\]



Because calibration error is defined as



\\\[

e=\\hat L-L,

\\]



the lower historical local mean indicates that future severe-underestimation cases occurred in neighborhoods where the consequence model had historically been substantially less conservative.



\---



\### Local Median Calibration Error



Nonsevere:



\\\[

0.123468

\\]



Severe:



\\\[

0.014784

\\]



Difference:



\\\[

\-0.108684

\\]



Standardized effect:



\\\[

\\boxed{-0.802}.

\\]



This closely reproduces the local-mean result and indicates that the effect is not solely caused by isolated extreme historical errors.



\---



\### Local Error Standard Deviation



Nonsevere:



\\\[

0.070929

\\]



Severe:



\\\[

0.070574

\\]



Difference:



\\\[

\-0.000355

\\]



Standardized effect:



\\\[

\\boxed{-0.010}.

\\]



Historical error variance provided essentially no univariate separation.



This is an important negative result.



The relevant calibration signal appears to involve the \*\*direction and bias of historical error\*\*, rather than simply greater historical prediction variability.



\---



\### Local Underestimation Fraction



Nonsevere:



\\\[

0.198674

\\]



Severe:



\\\[

0.421516

\\]



Difference:



\\\[

+0.222841

\\]



Standardized effect:



\\\[

\\boxed{+0.942}.

\\]



This was the strongest observed univariate separation.



Historical analogues of severe future-underestimation cases had underestimated realized consequence approximately:



\\\[

42.15\\%

\\]



of the time, compared with:



\\\[

19.87\\%

\\]



for nonsevere cases.



Thus:



\\\[

\\boxed{

\\text{historical local underestimation frequency}

}

\\]



contains substantial information about future consequence-model failure.



\---



\### Local Severe-Underestimation Fraction



Nonsevere:



\\\[

0.106245

\\]



Severe:



\\\[

0.233449

\\]



Difference:



\\\[

+0.127204

\\]



Standardized effect:



\\\[

\\boxed{+0.735}.

\\]



Severe current failures therefore occurred in neighborhoods containing substantially more historical severe failures.



\---



\### Local Neighbor Distance



Nonsevere:



\\\[

3.559106

\\]



Severe:



\\\[

2.933853

\\]



Difference:



\\\[

\-0.625253

\\]



Standardized effect:



\\\[

\-0.176.

\\]



Severe-underestimation cases were not simply more distant from historical support.



Their historical neighbors were, on average, somewhat closer.



This provides additional evidence that:



\\\[

\\boxed{

\\text{geometric familiarity}

\\neq

\\text{calibration reliability}.

}

\\]



A context-action pair can be geometrically familiar while still lying in a region where the consequence model has historically been biased.



\---



\### Local Minimum Calibration Error



Nonsevere:



\\\[

0.001684

\\]



Severe:



\\\[

\-0.097416

\\]



Difference:



\\\[

\-0.099100

\\]



Standardized effect:



\\\[

\\boxed{-0.668}.

\\]



The worst historical calibration error in the local neighborhood therefore provided another substantial signal of future underestimation risk.



\---



\## Leave-One-Generation-Seed-Out Classification



Models were evaluated using leave-one-generation-seed-out validation.



\### Predicted Loss Only



Balanced accuracy:



\\\[

59.617\\%

\\]



Severe recall:



\\\[

67.500\\%

\\]



Specificity:



\\\[

51.733\\%

\\]



ROC AUC:



\\\[

0.634.

\\]



Mean fold balanced accuracy:



\\\[

51.494\\%.

\\]



Mean fold AUC:



\\\[

0.571.

\\]



\---



\### Local Mean Error Only



Balanced accuracy:



\\\[

\\boxed{68.932\\%}

\\]



Severe recall:



\\\[

\\boxed{78.293\\%}

\\]



Specificity:



\\\[

59.571\\%

\\]



ROC AUC:



\\\[

\\boxed{0.754}.

\\]



Mean fold balanced accuracy:



\\\[

58.808\\%.

\\]



Mean fold AUC:



\\\[

0.728.

\\]



A single historical local calibration variable therefore substantially outperformed current predicted loss alone.



\---



\### Local Underestimation Fraction Only



Balanced accuracy:



\\\[

65.931\\%

\\]



Severe recall:



\\\[

54.390\\%

\\]



Specificity:



\\\[

77.471\\%

\\]



ROC AUC:



\\\[

0.715.

\\]



This representation traded lower severe-failure recall for substantially higher specificity.



\---



\### Local Severe-Underestimation Fraction Only



Balanced accuracy:



\\\[

62.253\\%

\\]



Severe recall:



\\\[

43.110\\%

\\]



Specificity:



\\\[

81.396\\%

\\]



ROC AUC:



\\\[

0.631.

\\]



\---



\### Local Error Standard Deviation Only



Balanced accuracy:



\\\[

46.996\\%

\\]



ROC AUC:



\\\[

0.434.

\\]



This confirms the univariate result that historical error variance alone is not a useful calibration-risk representation in this experiment.



\---



\### Local Calibration Compact Model



The compact historical calibration model used:



\- local mean error,

\- local error standard deviation,

\- local underestimation fraction,

\- local severe-underestimation fraction.



Performance:



\\\[

\\text{balanced accuracy}=68.452\\%

\\]



\\\[

\\text{severe recall}=76.098\\%

\\]



\\\[

\\text{specificity}=60.806\\%

\\]



\\\[

\\mathrm{AUC}=0.756.

\\]



\---



\### Loss + Local Calibration Model



The combined model used current predicted action loss together with historical local calibration features.



It produced the strongest pooled result:



\\\[

\\boxed{

\\text{balanced accuracy}=69.367\\%

}

\\]



\\\[

\\boxed{

\\text{severe recall}=77.683\\%

}

\\]



\\\[

\\text{severe precision}=16.664\\%

\\]



\\\[

\\text{specificity}=61.050\\%

\\]



\\\[

\\boxed{

\\mathrm{AUC}=0.760

}

\\]



with:



\\\[

\\text{mean fold balanced accuracy}=60.364\\%

\\]



and:



\\\[

\\text{mean fold AUC}=0.737.

\\]



\---



\## Coefficient Stability



The combined model produced the following dominant coefficient:



\\\[

\\boxed{

\\beta\_{\\text{local mean error}}

=

\-2.285

}

\\]



with:



\\\[

\\boxed{

100\\%\\text{ sign stability}.

}

\\]



Other combined-model coefficients were:



\- predicted action loss: `+0.431`

\- local severe-underestimate fraction: `-0.334`

\- local underestimate fraction: `+0.181`

\- local error standard deviation: `+0.054`



All reported combined-model coefficient signs were stable across all leave-one-seed-out fits.



The dominant negative coefficient on local mean error is consistent with the primary hypothesis:



\\\[

\\boxed{

\\text{less conservative historical local calibration}

\\Rightarrow

\\text{greater severe-underestimation risk}.

}

\\]



The multivariate coefficient signs for correlated local calibration variables should not, however, be interpreted independently as causal effects.



\---



\## Comparison With Static Pre-Action Loss Geometry



Earlier Experiment 095 found that the strongest pre-action severe-underestimation model based on static loss-surface geometry was the predicted loss ceiling alone:



\\\[

\\text{balanced accuracy}=67.667\\%

\\]



\\\[

\\text{severe recall}=73.333\\%

\\]



\\\[

\\mathrm{AUC}=0.652.

\\]



Experiment 099 produced:



\\\[

\\text{balanced accuracy}=69.367\\%

\\]



\\\[

\\text{severe recall}=77.683\\%

\\]



\\\[

\\mathrm{AUC}=0.760.

\\]



These experiments were not performed on identical event populations, so the numerical difference must not be treated as a formal head-to-head performance comparison.



Nevertheless, Experiment 099 provides evidence that historical local calibration information contains predictive structure not represented by current loss magnitude alone.



\---



\## Primary Finding



The principal result of Experiment 099 is:



\\\[

\\boxed{

\\text{historical local calibration behavior contains}

\\atop

\\text{substantial information about future consequence}

\\atop

\\text{underestimation risk}.

}

\\]



The strongest univariate signal was:



\\\[

\\boxed{

\\text{local underestimation fraction}

}

\\]



with standardized separation:



\\\[

\\boxed{+0.942}.

\\]



The strongest validated model combined current predicted loss with historical local calibration memory and achieved:



\\\[

\\boxed{\\mathrm{AUC}=0.760}.

\\]



Historical local mean error alone achieved:



\\\[

\\boxed{\\mathrm{AUC}=0.754},

\\]



showing that much of the useful information is carried directly by local calibration history.



\---



\## Interpretation



The evidence supports a distinction between two different forms of uncertainty.



\### Epistemic unfamiliarity



This concerns whether the current context-action pair is distant from historical experience.



\### Empirical calibration unreliability



This concerns whether the consequence model has historically predicted similar situations accurately.



The experiments now indicate that these are not equivalent.



A context can be geometrically familiar while its consequence model remains systematically unreliable.



This suggests that an adaptive digital twin may benefit from maintaining an explicit state representing its own local predictive reliability:



\\\[

z\_t^{\\text{cal}}

=

f(

e\_{1:t-1},

x\_t,

a\_t

).

\\]



Such a state would allow adaptation to depend not merely on what the twin predicts, but also on how much empirical evidence exists that predictions of that kind should be trusted.



\---



\## Important Observability Limitation



Experiment 099 uses a full-information historical calibration bank.



For every historical context, calibration errors were reconstructed for all candidate actions:



\\\[

a\\in\\{k\_1,k\_2,k\_3\\}.

\\]



The simulation therefore effectively supplies:



\\\[

L(x,k\_1),

\\quad

L(x,k\_2),

\\quad

L(x,k\_3)

\\]



for historical contexts.



This is appropriate for determining whether an action-conditioned calibration-risk representation exists in the simulated system.



It does \*\*not\*\* establish that the exact representation is directly deployable in a physical online controller.



A real system may observe only:



\\\[

L(x,a\_{\\mathrm{executed}})

\\]



unless counterfactual consequences are available through:



\- a trusted simulator,

\- an identified system model,

\- a causal estimator,

\- an off-policy estimator,

\- or another validated digital-twin reconstruction mechanism.



Therefore Experiment 099 establishes:



\\\[

\\boxed{

\\text{representational signal exists}

}

\\]



but does not yet establish:



\\\[

\\boxed{

\\text{the signal remains available under realistic}

\\atop

\\text{online observability constraints}.

}

\\]



\---



\## Falsification Status



Experiment 099 does \*\*not\*\* establish that historical local calibration memory solves the harmful-expansion problem.



Several uncertainties remain:



1\. The representation uses full-information historical action outcomes.

2\. Severe-underestimation precision remains low because the target is relatively rare.

3\. Leave-one-seed-out fold performance is weaker than pooled performance.

4\. The neighborhood size \\(K=7\\) has not yet been subjected to robustness analysis.

5\. No frozen prospective controller using this representation has been evaluated.

6\. No evidence yet establishes that the signal survives executed-action-only feedback.

7\. No evidence yet establishes generalization to different regime distributions or structural dynamics.



Accordingly, the result should be interpreted as evidence for a promising representation, not as validation of a final controller.



\---



\## Conclusion



Experiment 099 demonstrates that the digital twin's historical local prediction errors contain meaningful information about future consequence-model underestimation.



The most informative regions were not necessarily the most geometrically unfamiliar. Instead, severe future failures were associated with neighborhoods where the consequence model had historically been more optimistic.



The resulting conceptual distinction is:



\\\[

\\boxed{

\\text{support asks: ``Have I seen something like this?''}

}

\\]



while:



\\\[

\\boxed{

\\text{calibration memory asks: ``When I saw something like this,}

\\atop

\\text{were my predictions trustworthy?''}

}

\\]



The second question contains information that the first does not.



\---



\## Next Experiment



\### Experiment 100 — Observability-Constrained Historical Calibration Memory



The next experiment should determine whether the Experiment 099 signal survives when the calibration bank is restricted to historically observable outcomes rather than full counterfactual action consequences.



The central comparison will be:



\\\[

\\boxed{

\\text{full-information calibration memory}

\\quad\\text{vs}\\quad

\\text{executed-action-only calibration memory}.

}

\\]



The purpose is not to improve the classifier immediately.



The purpose is to test whether the newly identified calibration-memory mechanism remains available under a more realistic online information structure.



Only if that signal survives should calibration memory be considered for a frozen prospective controller.

