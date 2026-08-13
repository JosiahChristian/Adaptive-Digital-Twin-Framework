\# Experiment 097 — Frozen Loss-Ceiling Calibration Guard Prospective Validation



\## Objective



Experiments 094–096 identified a prospective calibration-risk signal based on predicted loss-surface severity.



The strongest compact pre-action quantity was:



\\\[

\\boxed{

C(x)

=

\\max\_a \\hat L\_a(x)

}

\\]



where:



\\\[

\\hat L\_a(x)

\\]



is the predicted loss for candidate action \\(a\\).



Experiment 096 identified a retrospective tradeoff band around:



\\\[

0.135

\\text{ to }

0.155.

\\]



Before observing any new prospective outcomes, Experiment 097 preregistered:



\\\[

\\boxed{

\\tau\_C=0.155

}

\\]



as the primary frozen calibration-guard threshold.



A lower threshold:



\\\[

0.135

\\]



was retained only as a secondary sensitivity analysis.



The central prospective question is:



\\\[

\\boxed{

\\text{Can a frozen loss-ceiling guard prevent harmful}

\\atop

\\text{support-admitted responsive expansion without}

\\atop

\\text{degrading regret or under-persistence?}

}

\\]



\---



\# Prospective Seed Block



The untouched prospective seed range is:



\\\[

\\boxed{

44051\\text{--}44070.

}

\\]



This contains:



\\\[

\\boxed{

20

}

\\]



generation seeds.



The seed block was frozen before observing the Experiment 097 outcomes.



\---



\# Existing Support-Aware Baseline



The baseline controller uses:



\\\[

\\text{safety threshold}=0.60,

\\]



\\\[

\\text{downside threshold}=0.020,

\\]



and:



\\\[

\\text{context-support threshold}=2.50.

\\]



The existing support quantity is interpreted, following Experiment 091, as:



\\\[

\\boxed{

\\text{context-level epistemic support}.

}

\\]



The calibration guard does not replace this support mechanism.



It is layered on top of it.



\---



\# Preregistered Primary Ceiling Rule



The primary ceiling threshold is:



\\\[

\\boxed{

\\tau\_C=0.155.

}

\\]



The guard operates only on actions newly admitted by support-aware safe-action expansion.



The rule is:



\\\[

\\boxed{

\\text{veto a support-admitted responsive expansion if}

\\quad

C(x)\\ge0.155.

}

\\]



where:



\\\[

C(x)

=

\\max\_a\\hat L\_a(x).

\\]



\---



\# Narrow Scope of the Guard



The ceiling rule does not override actions already contained in the primary predicted-safe action set.



Therefore:



\\\[

\\boxed{

\\text{primary-safe action}

\\Rightarrow

\\text{not vetoed by the ceiling guard}.

}

\\]



The rule applies only to:



\\\[

\\boxed{

\\text{new actions admitted by the support-expansion layer}.

}

\\]



This preserves the existing primary gate and limits the calibration mechanism to the residual responsive-expansion decision.



\---



\# Secondary Sensitivity Rule



A secondary sensitivity threshold is also evaluated:



\\\[

\\boxed{

\\tau\_C=0.135.

}

\\]



This threshold was identified retrospectively as the best pooled balanced-accuracy landmark in Experiment 096.



However:



\\\[

\\boxed{

0.135

}

\\]



is not the preregistered primary threshold.



The primary Experiment 097 interpretation must therefore be based on:



\\\[

\\boxed{

0.155.

}

\\]



The sensitivity result cannot replace the primary result after observing prospective outcomes.



\---



\# Severe Underestimation Outcome



Experiment 097 retains the severe-underestimation definition from Experiment 095:



\\\[

e\_a

=

\\hat L\_a-L(x,a).

\\]



A baseline support expansion is classified as severely underestimated when:



\\\[

\\boxed{

e\_a<-0.050.

}

\\]



This realized quantity is used only for post-outcome evaluation.



It is not available to the guard at action-selection time.



\---



\# Prospective Support Baseline



Across the 20 prospective seeds, the support baseline produces mean regret:



\\\[

\\boxed{

0.019547.

}

\\]



Mean under-persistence is:



\\\[

29.05.

\\]



Mean over-persistence is:



\\\[

6.90.

\\]



Mean action entropy is:



\\\[

0.519.

\\]



Responsive retention is:



\\\[

\\boxed{

97.841\\%.

}

\\]



Mean beneficial expansion events per seed are:



\\\[

0.40.

\\]



Mean harmful expansion events per seed are:



\\\[

\\boxed{

0.05.

}

\\]



Thus harmful support-expansion events are rare in this prospective block.



\---



\# Event Sparsity



A mean harmful count of:



\\\[

0.05

\\]



across:



\\\[

20

\\]



seeds corresponds to:



\\\[

\\boxed{

1

}

\\]



harmful support-expansion event in the entire prospective block.



This is a critical limitation for interpretation.



Experiment 097 therefore provides a prospective directional test under low event prevalence rather than a high-powered validation of harmful-event reduction.



\---



\# Primary Guard Policy Summary



With:



\\\[

\\boxed{

\\tau\_C=0.155,

}

\\]



mean regret becomes:



\\\[

\\boxed{

0.019543.

}

\\]



Mean under-persistence remains:



\\\[

\\boxed{

29.05.

}

\\]



Mean over-persistence becomes:



\\\[

7.10.

\\]



Mean entropy becomes:



\\\[

0.520.

\\]



Responsive retention becomes:



\\\[

\\boxed{

98.012\\%.

}

\\]



Mean beneficial expansion events per seed become:



\\\[

0.20.

\\]



Mean harmful expansion events become:



\\\[

\\boxed{

0.00.

}

\\]



\---



\# Primary Harmful-Expansion Result



The support baseline produces one harmful expansion event.



The frozen \\(0.155\\) ceiling guard vetoes that event.



Therefore:



\\\[

\\boxed{

\\text{baseline harmful vetoed}

=

1\.

}

\\]



Across seeds:



\\\[

\\boxed{

\\text{harmful improved/unchanged/degraded}

=

1/19/0.

}

\\]



Mean harmful-event change is:



\\\[

\\boxed{

\\Delta H

=

\-0.050

\\text{ events per seed}.

}

\\]



No seed experiences an increase in harmful expansion.



\---



\# Primary Regret Result



Mean regret changes by:



\\\[

\\boxed{

\\Delta R

=

\-0.000003.

}

\\]



Median regret change is:



\\\[

\\boxed{

0\.

}

\\]



The seed-level range is:



\\\[

\\boxed{

\[-0.000066,\\ 0.000000].

}

\\]



Therefore no seed experiences increased regret.



The seed-level count is:



\\\[

\\boxed{

\\text{regret improved/unchanged/degraded}

=

1/19/0.

}

\\]



The same seed in which the harmful expansion is removed is the only seed with measurable regret improvement.



\---



\# Under-Persistence Result



Mean under-persistence change is:



\\\[

\\boxed{

\\Delta\\text{Under}

=

0\.

}

\\]



Thus the calibration-aware veto does not increase under-persistence in the prospective block.



This is important because vetoing responsive actions could, in principle, reintroduce persistence errors.



That effect is not observed here.



\---



\# Responsive Retention



Responsive retention changes from:



\\\[

97.841\\%

\\]



to:



\\\[

\\boxed{

98.012\\%.

}

\\]



The change is:



\\\[

\\boxed{

+0.171\\%.

}

\\]



Thus the frozen ceiling guard does not reduce the measured responsive-retention metric in this block.



\---



\# Severe-Underestimation Capture



The primary guard achieves:



\\\[

\\boxed{

100.000\\%

}

\\]



severe-underestimation veto recall among the baseline expansion events observed in this prospective block.



Therefore every baseline support-expansion event satisfying:



\\\[

e\_a<-0.050

\\]



is vetoed by the preregistered \\(0.155\\) rule.



This is a favorable prospective transfer of the calibration-risk mechanism discovered retrospectively in Experiments 094–096.



\---



\# Beneficial-Expansion Cost



The primary guard also vetoes:



\\\[

\\boxed{

4

}

\\]



beneficial baseline expansion events.



Mean beneficial expansion count therefore falls from:



\\\[

0.40

\\]



to:



\\\[

0.20

\\]



per seed.



The paired mean change is:



\\\[

\\boxed{

\\Delta\\text{Beneficial}

=

\-0.200.

}

\\]



Thus the safety gain is not free.



The guard removes one harmful expansion while also suppressing four beneficial responsive expansions.



\---



\# Primary Selectivity Tradeoff



The prospective primary result can therefore be summarized as:



\\\[

\\boxed{

1

\\text{ harmful expansion vetoed}

}

\\]



with:



\\\[

\\boxed{

4

\\text{ beneficial expansions vetoed}.

}

\\]



This identifies selectivity as the main remaining limitation of the ceiling guard.



\---



\# Secondary 0.135 Sensitivity Result



The lower sensitivity threshold:



\\\[

0.135

\\]



also eliminates the single harmful baseline expansion.



Mean harmful-event change is:



\\\[

\-0.050.

\\]



Mean regret change is again:



\\\[

\-0.000003.

\\]



Under-persistence change remains:



\\\[

0\.

\\]



Therefore the sensitivity threshold provides no additional observed safety benefit in this prospective block.



\---



\# Sensitivity Cost



The \\(0.135\\) rule vetoes:



\\\[

\\boxed{

5

}

\\]



beneficial baseline expansions.



This is one more beneficial veto than the preregistered \\(0.155\\) rule.



Mean beneficial-event change becomes:



\\\[

\\boxed{

\-0.250

}

\\]



per seed.



Responsive retention is:



\\\[

98.069\\%.

\\]



\---



\# Primary Versus Sensitivity Threshold



The two prospective rules produce the same observed harmful-event and regret outcomes:



\\\[

\\boxed{

1

\\text{ harmful veto}

}

\\]



and:



\\\[

\\boxed{

\\Delta R=-0.000003.

}

\\]



However:



\\\[

0.155

\\]



vetoes:



\\\[

4

\\]



beneficial events,



while:



\\\[

0.135

\\]



vetoes:



\\\[

5\.

\\]



Therefore the lower threshold is more conservative without providing additional observed harmful-event reduction.



\---



\# Importance of Preregistration



Experiment 097 designated:



\\\[

\\boxed{

0.155

}

\\]



as the primary threshold before observing prospective outcomes.



This prevents the sensitivity threshold from replacing the primary result after the fact.



The correct interpretation is therefore:



\\\[

\\boxed{

\\text{the preregistered 0.155 guard produced the primary}

\\atop

\\text{successful prospective result}.

}

\\]



The \\(0.135\\) result is supportive sensitivity information only.



\---



\# Prospective Mechanism Transfer



Experiments 094–096 identified the retrospective sequence:



\\\[

\\text{elevated predicted loss-surface severity}

\\]



\\\[

\\Downarrow

\\]



\\\[

\\text{increased risk of severe consequence underestimation}

\\]



\\\[

\\Downarrow

\\]



\\\[

\\text{increased risk of harmful support expansion}.

\\]



Experiment 097 tests a frozen pre-action ceiling rule based on that mechanism.



The rule captures:



\\\[

\\boxed{

100\\%

}

\\]



of observed severe-underestimation support expansions and removes the only observed harmful support expansion.



Thus the mechanism transfers prospectively in this block.



\---



\# What the Result Demonstrates



Experiment 097 provides prospective evidence that a calibration-aware ceiling condition can improve the residual support-expansion decision.



Specifically, the preregistered rule:



\- removes the only harmful expansion observed,

\- catches every observed severe-underestimation expansion,

\- does not increase regret on any seed,

\- does not increase under-persistence,

\- and does not reduce responsive retention.



These are favorable directional outcomes.



\---



\# Why the Evidence Is Not Conclusive



Only:



\\\[

\\boxed{

1

}

\\]



harmful support-expansion event occurs under the baseline.



Therefore harmful-event recall is based on a single event.



Likewise, the mean regret improvement:



\\\[

\-0.000003

\\]



is generated by one improved seed.



This means Experiment 097 does not provide strong statistical evidence for a universal effect.



It provides:



\\\[

\\boxed{

\\textbf{successful but low-event prospective validation}.

}

\\]



\---



\# Regime Dependence



The support-expansion mechanism is relatively inactive in this prospective block.



Baseline mean meaningful expansion outcomes are approximately:



\\\[

0.40

\+

0.05

=

\\boxed{

0.45

}

\\]



events per seed.



This is substantially sparser than some earlier experimental regimes.



Therefore the calibration guard has relatively few opportunities to alter behavior.



This reinforces the broader finding that expansion opportunity and failure prevalence vary substantially across generation-seed blocks.



\---



\# Relationship to Experiment 090



Experiment 090 demonstrated that different prospective blocks can possess substantially different action-loss and safe-set geometry.



Experiment 097 adds another example of block-level variation.



The new block has high overall under-persistence but very sparse harmful support-expansion activity.



Thus:



\\\[

\\boxed{

\\text{global controller difficulty}

\\neq

\\text{frequency of residual support-expansion failures}.

}

\\]



Different failure mechanisms can dominate in different regimes.



\---



\# Calibration Guard Versus General Controller Performance



Mean baseline regret in this block is approximately:



\\\[

0.019547,

\\]



which is large compared with some earlier blocks.



Yet only one harmful support expansion occurs.



Therefore most of the block's regret is not caused by the support-expansion layer.



The ceiling guard should consequently be interpreted as a targeted correction to a specific residual failure mechanism rather than a solution to the block's broader control difficulty.



\---



\# Selectivity Is the Remaining Problem



The main prospective weakness is not failure to detect the harmful event.



The primary rule detects it.



The problem is that the rule also vetoes four beneficial expansions.



Thus the next technical question is:



\\\[

\\boxed{

\\text{Can harmful high-ceiling veto candidates be distinguished}

\\atop

\\text{from beneficial high-ceiling veto candidates?}

}

\\]



This is now a selectivity problem.



\---



\# Why Immediate Threshold Retuning Is Not Appropriate



One response would be to move the threshold again.



Experiment 097 does not justify that.



The \\(0.155\\) threshold already removed the harmful event, and lowering it to \\(0.135\\) only increased beneficial vetoes.



Therefore further threshold tuning risks fitting the current block rather than learning the failure mechanism.



The next analysis should examine the vetoed-event population directly.



\---



\# Principal Prospective Finding



The preregistered primary rule:



\\\[

\\boxed{

C(x)\\ge0.155

}

\\]



reduces mean harmful support expansion from:



\\\[

0.05

\\]



to:



\\\[

\\boxed{

0.00

}

\\]



events per seed.



It produces:



\\\[

\\boxed{

1/19/0

}

\\]



improved/unchanged/degraded seeds for both harmful-event count and regret.



It causes:



\\\[

\\boxed{

0

}

\\]



increase in mean under-persistence.



It achieves:



\\\[

\\boxed{

100\\%

}

\\]



observed severe-underestimation veto recall.



\---



\# Primary Cost



The same rule vetoes:



\\\[

\\boxed{

4

}

\\]



beneficial expansions.



Thus the prospective result reveals a safety-selectivity tradeoff.



The current ceiling rule appears directionally useful but comparatively coarse.



\---



\# Final Scientific Interpretation



Experiment 097 provides the first prospective evidence that absolute consequence-calibration information can improve the support-aware safe-action-expansion architecture.



The evidence supports:



\\\[

\\boxed{

\\text{predicted loss-surface severity}

}

\\]



as a distinct control signal from:



\\\[

\\text{context support},

\\]



\\\[

\\text{transient-state risk},

\\]



and:



\\\[

\\text{the existing safety/downside stack}.

\\]



The calibration-aware guard successfully addresses the one observed harmful expansion in its preregistered prospective block.



However, beneficial vetoes show that the ceiling alone is not sufficiently selective.



\---



\# What Experiment 097 Establishes



Experiment 097 supports the following claims:



1\. a frozen loss-ceiling guard can be implemented prospectively without modifying the primary predicted-safe action set;

2\. the preregistered \\(0.155\\) rule removes the only observed harmful support expansion;

3\. the rule captures all observed severe-underestimation expansion events;

4\. no prospective seed experiences regret degradation;

5\. mean under-persistence does not increase;

6\. and the lower \\(0.135\\) sensitivity threshold offers no additional observed safety benefit while sacrificing another beneficial expansion.



\---



\# What Experiment 097 Does Not Establish



Experiment 097 does not establish:



\- statistically conclusive harmful-event reduction,

\- universal superiority of \\(0.155\\),

\- that calibration guarding solves the broader under-persistence problem,

\- that every high-ceiling support expansion should be vetoed,

\- or that the current ceiling guard has adequate selectivity for final deployment.



The low harmful-event count prevents stronger claims.



\---



\# Next Research Direction



Experiment 098 should remain diagnostic.



It should decompose the prospective events vetoed by the preregistered:



\\\[

\\boxed{

0.155

}

\\]



guard.



The relevant event population consists of:



\\\[

\\boxed{

5

}

\\]



baseline support expansions vetoed by the primary guard:



\\\[

1

\\]



harmful and:



\\\[

4

\\]



beneficial.



The analysis should compare pre-action quantities including:



\- predicted loss floor,

\- mean,

\- ceiling,

\- spread,

\- expanded-action predicted loss,

\- safety score,

\- downside score,

\- predicted risk,

\- context support distance,

\- current mismatch,

\- anchor age,

\- trigger score,

\- action step,

\- and predicted regret margin where available.



The central question should be:



\\\[

\\boxed{

\\text{What distinguishes the harmful high-ceiling veto candidate}

\\atop

\\text{from the beneficial high-ceiling veto candidates?}

}

\\]



Because the event population is extremely small, Experiment 098 should avoid fitting a complex classifier.



It should instead emphasize direct event-level decomposition, standardized comparisons where meaningful, and comparison against the earlier retrospective harmful-expansion signatures.



No new threshold or controller rule should be defined until the selectivity mechanism is better understood.

