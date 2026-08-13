\# Experiment 090 — Cross-Prospective-Block Regime-Shift Decomposition



\## Objective



Experiment 090 compares two already-consumed prospective seed blocks:



\\\[

44011\\text{--}44030

\\]



and:



\\\[

44031\\text{--}44050.

\\]



These correspond to the prospective populations used in Experiments 086 and 089.



The purpose is diagnostic only.



No new controller is introduced.



No thresholds are changed.



No new seed block is evaluated.



The central question is:



\\\[

\\boxed{

\\text{Why did the second prospective block exhibit substantially}

\\atop

\\text{greater regret and under-persistence than the first?}

}

\\]



The analysis decomposes the difference across:



\- true consequence geometry,

\- true optimal persistence,

\- true safe-action-set structure,

\- predicted loss geometry,

\- predicted risk,

\- support geometry,

\- and context variables.



\---



\# Motivation



Experiment 086 evaluated the support baseline on seeds:



\\\[

44011\\text{--}44030

\\]



and observed mean regret of approximately:



\\\[

0.006371

\\]



with mean under-persistence:



\\\[

9.40.

\\]



Experiment 089 evaluated the same baseline architecture on seeds:



\\\[

44031\\text{--}44050

\\]



and observed mean regret:



\\\[

0.017331

\\]



with mean under-persistence:



\\\[

28.50.

\\]



Thus the second prospective population was substantially more difficult.



Experiment 090 asks whether this change reflects:



1\. ordinary finite-sample variation,

2\. a meaningful change in generated operating regime,

3\. model-representation shift,

4\. or some combination of these effects.



\---



\# Reconstruction Population



The two blocks are reconstructed using the same model-training and test-splitting architecture.



\## Block 086



Seeds:



\\\[

44011,\\ldots,44030.

\\]



Total reconstructed test contexts:



\\\[

\\boxed{

1683\.

}

\\]



\## Block 089



Seeds:



\\\[

44031,\\ldots,44050.

\\]



Total reconstructed test contexts:



\\\[

\\boxed{

1813\.

}

\\]



The unequal context counts result from the generated datasets rather than manual filtering.



\---



\# Support-Baseline Consequence Shift



Mean support-baseline regret changes from:



\\\[

0.006366

\\]



in block 086 to:



\\\[

\\boxed{

0.017393

}

\\]



in block 089.



The difference is:



\\\[

\\boxed{

+0.011027.

}

\\]



The standardized difference is:



\\\[

\\boxed{

+0.425.

}

\\]



Thus the consequence penalty is substantially larger in the second block.



\---



\# Under-Persistence Shift



The fraction of contexts classified as under-persistent under the support baseline changes from:



\\\[

0.111705

\\]



to:



\\\[

\\boxed{

0.314396.

}

\\]



The absolute change is:



\\\[

\\boxed{

+0.202691.

}

\\]



The standardized difference is:



\\\[

\\boxed{

+0.507.

}

\\]



Thus the second prospective block contains a substantially greater under-persistence burden.



\---



\# Over-Persistence Shift



Over-persistence changes in the opposite direction.



Block 086:



\\\[

0.592989.

\\]



Block 089:



\\\[

\\boxed{

0.194153.

}

\\]



Difference:



\\\[

\-0.398835.

\\]



Standardized effect:



\\\[

\\boxed{

\-0.898.

}

\\]



Therefore the dominant controller error mode changes markedly between the two blocks.



Block 086 is characterized primarily by over-persistence.



Block 089 is characterized much more strongly by under-persistence.



\---



\# True Optimal Persistence Distribution



The true best-action distribution changes between the two prospective populations.



\## Block 086



\\\[

k\_1:

1098/1683

=

65.241\\%.

\\]



\\\[

k\_2:

490/1683

=

29.115\\%.

\\]



\\\[

k\_3:

95/1683

=

5.645\\%.

\\]



\## Block 089



\\\[

k\_1:

1052/1813

=

58.025\\%.

\\]



\\\[

k\_2:

669/1813

=

36.900\\%.

\\]



\\\[

k\_3:

92/1813

=

5.074\\%.

\\]



Thus the main structural change is:



\\\[

\\boxed{

k\_1\\downarrow

}

\\]



and:



\\\[

\\boxed{

k\_2\\uparrow.

}

\\]



The frequency of \\(k\_3\\)-optimal contexts remains nearly unchanged.



\---



\# Interpretation of the Optimal-Action Shift



The second block requires intermediate persistence more often.



The shift from:



\\\[

29.115\\%

\\]



to:



\\\[

36.900\\%

\\]



for \\(k\_2\\) means that overly responsive \\(k\_1\\) decisions are more likely to be genuinely under-persistent.



This directly helps explain the increased under-persistence rate observed in block 089.



The decision environment is therefore not merely noisier.



Its optimal-action structure has changed.



\---



\# True Safe-Action-Set Structure



The strongest structural change appears in the size of the true safe-action set.



\## Block 086



Singleton safe sets:



\\\[

1127/1683

=

66.964\\%.

\\]



Two-action safe sets:



\\\[

537/1683

=

31.907\\%.

\\]



Three-action safe sets:



\\\[

19/1683

=

1.129\\%.

\\]



\## Block 089



Singleton safe sets:



\\\[

1605/1813

=

\\boxed{

88.527\\%.

}

\\]



Two-action safe sets:



\\\[

198/1813

=

\\boxed{

10.921\\%.

}

\\]



Three-action safe sets:



\\\[

10/1813

=

0.552\\%.

\\]



This is one of the most important Experiment 090 findings.



\---



\# Collapse of Consequence Equivalence



The mean true safe-action-set size changes from:



\\\[

1.341652

\\]



to:



\\\[

\\boxed{

1.120243.

}

\\]



Standardized effect:



\\\[

\\boxed{

\-0.522.

}

\\]



Thus the second block offers much less opportunity for alternative persistence actions to remain consequence-equivalent.



In practical terms:



\\\[

\\boxed{

\\text{there is much less room for “free” responsiveness}.

}

\\]



A responsive reduction in persistence is more likely to move outside the true minimum-loss action set.



\---



\# True Consequence Difficulty



The true best achievable loss increases from:



\\\[

0.108537

\\]



to:



\\\[

\\boxed{

0.121283.

}

\\]



The standardized effect is:



\\\[

+0.150.

\\]



Thus the second block is intrinsically somewhat harder even under the true best action.



\---



\# True Action-Loss Separation



True loss spread changes from:



\\\[

0.018031

\\]



to:



\\\[

\\boxed{

0.026000.

}

\\]



The absolute increase is:



\\\[

0.007968.

\\]



This corresponds to an increase of approximately:



\\\[

44\\%.

\\]



The standardized effect is:



\\\[

\\boxed{

+0.247.

}

\\]



Therefore selecting the wrong persistence action carries a larger consequence penalty in block 089.



This reinforces the singleton-safe-set result.



\---



\# Learned Loss Geometry



The predicted loss models exhibit a much larger shift than the true loss surface.



\## Predicted \\(k\_1\\) Loss



\\\[

0.162163

\\rightarrow

\\boxed{

0.240715

}

\\]



with effect:



\\\[

+0.886.

\\]



\## Predicted \\(k\_2\\) Loss



\\\[

0.169622

\\rightarrow

\\boxed{

0.294818

}

\\]



with effect:



\\\[

+1.349.

\\]



\## Predicted \\(k\_3\\) Loss



\\\[

0.183219

\\rightarrow

\\boxed{

0.363139

}

\\]



with effect:



\\\[

\\boxed{

+1.504.

}

\\]



All three predicted losses increase substantially.



\---



\# Predicted Loss Spread



Predicted action-loss spread changes from:



\\\[

0.037533

\\]



to:



\\\[

\\boxed{

0.131986.

}

\\]



The difference is:



\\\[

+0.094453.

\\]



The standardized effect is:



\\\[

\\boxed{

+1.229.

}

\\]



This is one of the largest model-level shifts observed.



Therefore the learned loss model views the second prospective population as dramatically more action-sensitive.



\---



\# True Versus Predicted Loss Separation



The true loss spread increases with effect:



\\\[

+0.247.

\\]



The predicted loss spread increases with effect:



\\\[

\\boxed{

+1.229.

}

\\]



Thus the model-level change is much larger than the underlying true-loss change.



Conceptually:



\\\[

\\boxed{

\\text{the environment really becomes more action-sensitive}

}

\\]



but:



\\\[

\\boxed{

\\text{the learned loss representation amplifies that change}.

}

\\]



This mismatch may be important for understanding the controller's behavior in block 089.



\---



\# Predicted Risk Moves in the Opposite Direction



The two-stage predicted risk decreases from:



\\\[

0.021926

\\]



to:



\\\[

\\boxed{

0.012216.

}

\\]



Difference:



\\\[

\-0.009710.

\\]



Standardized effect:



\\\[

\\boxed{

\-0.698.

}

\\]



This is notable because the true environment simultaneously becomes:



\- more singleton-dominated,

\- more under-persistence-sensitive,

\- and more costly when the wrong action is chosen.



Therefore the predicted risk model becomes less alarmed while the true action-selection consequences become more severe.



\---



\# Internal Model Disagreement



Experiment 090 therefore reveals a potentially important internal disagreement.



The learned loss representation implies:



\\\[

\\boxed{

\\text{actions matter much more}.

}

\\]



The learned risk representation implies:



\\\[

\\boxed{

\\text{under-persistence risk is lower}.

}

\\]



At the same time, the realized environment shows:



\\\[

\\boxed{

\\text{under-persistence is substantially more common}.

}

\\]



This combination suggests that the controller's learned subsystems are not shifting coherently across regimes.



That does not establish a calibration defect by itself, but it identifies an important diagnostic target.



\---



\# Primary Predicted Safe-Set Size



The predicted primary safe-action-set size changes only modestly:



\\\[

1.090909

\\rightarrow

1.060121.

\\]



Standardized effect:



\\\[

\-0.114.

\\]



Thus the learned primary gate becomes only slightly narrower.



This is small relative to the true safe-set collapse:



\\\[

1.341652

\\rightarrow

1.120243.

\\]



Therefore the representation of consequence-equivalence changes less than the underlying truth.



\---



\# Support-Expanded Safe-Set Size



The support-aware predicted action-set size changes from:



\\\[

1.184789

\\]



to:



\\\[

1.136790.

\\]



Standardized effect:



\\\[

\-0.125.

\\]



Again, the predicted safe-action structure changes much less than the true safe-action structure.



This means block 089 contains a larger mismatch between:



\\\[

\\text{true action equivalence}

\\]



and:



\\\[

\\text{learned action-set flexibility}.

\\]



\---



\# Context-Level Shifts



Several context variables differ meaningfully between the two blocks.



\## Release Probability



\\\[

0.407348

\\rightarrow

\\boxed{

0.318501

}

\\]



with effect:



\\\[

\-0.524.

\\]



\## Current Parameter Estimate



\\\[

0.907986

\\rightarrow

0.916496

\\]



with effect:



\\\[

+0.417.

\\]



\## Benefit Probability



\\\[

0.672835

\\rightarrow

0.709418

\\]



with effect:



\\\[

+0.398.

\\]



\## Current Mismatch



\\\[

0.563776

\\rightarrow

0.396042

\\]



with effect:



\\\[

\-0.286.

\\]



\## Feature Distance



\\\[

0.795802

\\rightarrow

0.856125

\\]



with effect:



\\\[

+0.218.

\\]



\## Trigger Score



\\\[

9.630927

\\rightarrow

8.542634

\\]



with effect:



\\\[

\-0.156.

\\]



\## Anchor Age



\\\[

24.584076

\\rightarrow

23.841147

\\]



with effect:



\\\[

\-0.051.

\\]



\---



\# Mismatch Is Not the Primary Explanation



Current mismatch actually decreases:



\\\[

0.564

\\rightarrow

0.396.

\\]



Therefore the substantially greater difficulty of block 089 cannot be explained simply by larger mismatch.



Likewise, anchor age changes very little.



This distinguishes the block-level regime change from the transient-state failure mechanism identified in Experiments 084–086.



The second prospective population appears difficult for broader structural reasons.



\---



\# Lower Release Probability



Release probability decreases substantially:



\\\[

0.407

\\rightarrow

0.319.

\\]



This shift is consistent with an environment where persistence may need to be maintained more often.



Combined with the increase in \\(k\_2\\)-optimal contexts, this supports the interpretation that the second block genuinely favors more persistence.



\---



\# Higher Benefit Probability



Benefit probability increases:



\\\[

0.673

\\rightarrow

0.709.

\\]



This indicates that the generated context mixture changes in multiple dimensions rather than simply becoming globally adverse.



The regime shift is therefore not reducible to a single scalar notion of difficulty.



\---



\# Safety Confidence and Downside Prediction



For the ultimately selected support-baseline action, mean safety confidence increases:



\\\[

0.773203

\\rightarrow

\\boxed{

0.852185.

}

\\]



Standardized effect:



\\\[

+0.417.

\\]



Predicted downside decreases:



\\\[

0.004560

\\rightarrow

\\boxed{

0.001692.

}

\\]



Standardized effect:



\\\[

\-0.408.

\\]



Thus the learned action-level safety machinery becomes more confident in the second block even though realized under-persistence becomes much worse.



This is another important indication of cross-regime calibration tension.



\---



\# Combined Model-Confidence Pattern



Block 089 simultaneously exhibits:



\\\[

\\boxed{

\\text{higher safe-action confidence}

}

\\]



\\\[

\+

\\]



\\\[

\\boxed{

\\text{lower predicted downside}

}

\\]



\\\[

\+

\\]



\\\[

\\boxed{

\\text{lower predicted risk}

}

\\]



while realized under-persistence rises sharply.



Therefore:



\\\[

\\boxed{

\\text{the learned safety stack becomes more confident}

\\atop

\\text{in a regime where true action equivalence becomes narrower}.

}

\\]



This is likely one of the most important architectural findings from Experiment 090.



\---



\# Support-Distance Observation



Experiment 090 reports:



\\\[

\\text{support distance}\_{k1}

=

\\text{support distance}\_{k2}

=

\\text{support distance}\_{k3}

\\]



at the aggregate level.



For block 086:



\\\[

4.987768

\\]



is reported for all three actions.



For block 089:



\\\[

2.803131

\\]



is reported for all three actions.



The selected-action distance has the same aggregate values.



This exact equality requires an implementation audit.



\---



\# Support-Metric Implementation Audit



The current support mechanism constructs action-specific feature vectors by appending:



\\\[

a,

\\]



\\\[

a-1,

\\]



and:



\\\[

3-a.

\\]



However, a separate `StandardScaler` is fitted for each action-specific training matrix.



Within any one action-specific matrix, the appended action coordinates are constants.



For example, for action \\(k\_1\\), every training point has the same appended action coordinates.



The same is true separately for \\(k\_2\\) and \\(k\_3\\).



Standardizing a constant feature within each action-specific scaler gives zero variance and effectively removes that coordinate from Euclidean distance.



The remaining context/model features are identical across the three action-specific support spaces.



This creates the possibility that:



\\\[

\\boxed{

d(x,k\_1)

=

d(x,k\_2)

=

d(x,k\_3)

}

\\]



for every context.



\---



\# Revised Interpretation if the Audit Is Confirmed



If exact action-level equality is confirmed, the existing metric should not be described as:



\\\[

\\text{action-specific epistemic support}.

\\]



Instead it should be interpreted as:



\\\[

\\boxed{

\\text{context-level epistemic support}.

}

\\]



That would mean the support gate has been answering approximately:



\\\[

\\boxed{

\\text{“How familiar is this operating context?”}

}

\\]



rather than:



\\\[

\\text{“How well supported is this particular action?”}

\\]



This distinction is scientifically important.



\---



\# Does This Invalidate Prior Support Experiments?



No.



The observed computational effects of the support metric remain real.



Experiments 080–089 still demonstrate that the measured support quantity contains useful predictive and control information.



What changes is the interpretation of that information.



If the audit confirms context-level rather than action-level support, previous conclusions should be reframed accordingly.



For example:



\\\[

\\text{“weak action support increases harmful-expansion risk”}

\\]



would become:



\\\[

\\boxed{

\\text{“weak local context support increases harmful-expansion risk.”}

}

\\]



\---



\# Why Selected Support Distance Can Exceed 2.50



Experiment 090 reports mean selected support distance above the admission threshold:



\\\[

4.988

\\]



for block 086 and:



\\\[

2.803

\\]



for block 089.



This is not necessarily an error.



The \\(2.50\\) support threshold applies only when admitting an action that is not already in the primary predicted action set.



If the final selected action is already contained in the primary set, it is not required to pass the support-expansion threshold.



Therefore:



\\\[

\\boxed{

d\_{\\text{selected}}>2.50

}

\\]



can occur legitimately.



The audit concern is not the magnitude itself.



It is the apparent equality across all actions.



\---



\# Principal Regime-Shift Finding



Experiment 090 demonstrates that the second prospective block represents a meaningfully different decision regime.



The most important structural changes are:



\\\[

\\boxed{

\\text{singleton true-safe sets}

:

66.964\\%

\\rightarrow

88.527\\%

}

\\]



\\\[

\\boxed{

k\_2\\text{-optimal contexts}

:

29.115\\%

\\rightarrow

36.900\\%

}

\\]



\\\[

\\boxed{

\\text{true loss spread}

:

0.018031

\\rightarrow

0.026000

}

\\]



and:



\\\[

\\boxed{

\\text{predicted loss spread}

:

0.037533

\\rightarrow

0.131986.

}

\\]



Therefore block 089 is substantially more action-sensitive and offers much less consequence-equivalent flexibility.



\---



\# Principal Model-Calibration Finding



At the same time:



\\\[

\\text{predicted risk}

\\]



decreases,



\\\[

\\text{predicted downside}

\\]



decreases,



and:



\\\[

\\text{safety confidence}

\\]



increases.



Thus the learned safety machinery becomes more confident while the true consequence geometry becomes less forgiving.



This identifies a cross-regime model-consistency problem worthy of future investigation.



\---



\# Principal Support Finding



Experiment 090 also identifies a likely implementation-level interpretation issue in the support metric.



The support-distance outputs suggest that the current support representation may be:



\\\[

\\boxed{

\\text{context-specific}

}

\\]



rather than:



\\\[

\\boxed{

\\text{action-specific}.

}

\\]



This must be verified before further controller development depends on an action-conditional interpretation.



\---



\# Overall Conclusion



Experiment 090 supports three conclusions.



\## 1. The second prospective block is genuinely different



It contains:



\- narrower true safe-action sets,

\- more \\(k\_2\\)-optimal contexts,

\- larger true action-loss separation,

\- and substantially greater under-persistence.



Therefore the 086-to-089 difference is not adequately explained as simple random fluctuation.



\---



\## 2. The learned safety stack becomes overconfident relative to the new regime



Block 089 exhibits:



\- lower predicted risk,

\- lower predicted downside,

\- higher safety confidence,



despite:



\- more under-persistence,

\- narrower true safe sets,

\- and larger true consequence separation.



Therefore cross-regime calibration deserves explicit study.



\---



\## 3. The support metric requires a representation audit



The equality of support distances across actions suggests that the current construction may encode local context familiarity rather than true action-conditioned support.



The metric remains useful, but its scientific meaning may need to be revised.



\---



\# Next Research Direction



The next experiment should \*\*not\*\* introduce another controller.



Experiment 091 should be an implementation audit of the support metric.



It should directly test whether:



\\\[

d(x,k\_1)

=

d(x,k\_2)

=

d(x,k\_3)

\\]



for individual contexts rather than merely at aggregate level.



The audit should:



1\. evaluate action-specific distances context by context,

2\. report the maximum absolute pairwise action-distance difference,

3\. count contexts with nonzero action-distance separation,

4\. inspect standardized action-feature variance,

5\. verify whether appended action coordinates collapse under separate per-action scaling,

6\. compare the current metric with a deliberately shared action-conditioned representation.



The central audit question is:



\\\[

\\boxed{

\\text{Is the current support metric truly action-conditional,}

\\atop

\\text{or is it mathematically equivalent to context-level support?}

}

\\]



No controller behavior should be modified until this is resolved.



If the current metric is confirmed to be context-level, the prior experimental record should be preserved but terminology should be updated.



A future experiment may then construct genuinely action-conditioned support and compare it against the validated context-support architecture on an untouched seed block.

