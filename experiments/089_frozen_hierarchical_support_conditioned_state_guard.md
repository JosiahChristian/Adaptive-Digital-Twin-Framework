\# Experiment 089 — Frozen Hierarchical Support-Conditioned State Guard



\## Status



\\\[

\\boxed{

\\text{PROSPECTIVE EVALUATION COMPLETED}

}

\\]



Experiment 089 evaluated a frozen hierarchical support-conditioned state guard on a new prospective seed block:



\\\[

44031\\text{--}44050.

\\]



The hierarchical rule was fixed before those seed outcomes were observed.



The frozen controller parameters were:



\\\[

\\tau\_p=0.60,

\\qquad

\\tau\_d=0.020,

\\qquad

\\tau\_s=2.50,

\\qquad

\\tau\_h=0.50,

\\qquad

\\tau\_{\\text{selective}}=2.00.

\\]



The revised veto rule was:



\\\[

\\boxed{

\\text{veto expansion iff }

q\_{\\text{state}}\\ge0.50

\\land

d\_{\\text{support}}>2.00.

}

\\]



The experiment compares:



1\. the support-aware baseline,

2\. the previously validated unconditional state guard,

3\. the new hierarchical support-conditioned state guard.



\---



\# Motivation



Experiment 086 prospectively demonstrated that the frozen transient-state guard reduces harmful support-aware expansion.



However, the primary \\(0.50\\) state guard also vetoed a substantial number of beneficial responsive actions.



Experiment 087 showed that within the state-vetoed population, support distance was the strongest diagnostic separating:



\\\[

\\text{harmful vetoes}

\\]



from:



\\\[

\\text{beneficial vetoes}.

\\]



Experiment 088 then showed that support distance alone outperformed:



\- state probability alone,

\- state probability plus support,

\- and an explicit state-support interaction



for retrospective selectivity discrimination.



The resulting architectural hypothesis was therefore hierarchical rather than multivariate:



\\\[

\\boxed{

\\text{state risk identifies the caution regime}

}

\\]



followed by:



\\\[

\\boxed{

\\text{graded support determines whether the veto is necessary}.

}

\\]



Experiment 089 prospectively tests that hypothesis.



\---



\# Prospective Seed Population



The untouched prospective generation seeds were:



\\\[

\\boxed{

44031,

44032,

44033,

44034,

44035,

44036,

44037,

44038,

44039,

44040,

}

\\]



\\\[

\\boxed{

44041,

44042,

44043,

44044,

44045,

44046,

44047,

44048,

44049,

44050\.

}

\\]



Thus:



\\\[

\\boxed{

20

}

\\]



new generated populations were evaluated.



\---



\# Frozen Baseline Expansion Architecture



The support-aware baseline retained the previously established expansion criteria:



\\\[

\\hat p\_{\\text{safe}}(a)\\ge0.60,

\\]



\\\[

\\hat d(a)\\le0.020,

\\]



and:



\\\[

d\_{\\text{support}}(a)\\le2.50.

\\]



Therefore the candidate action must first pass all three baseline requirements before either state-based guard is considered.



\---



\# Unconditional State Guard



The previously validated Experiment 086 controller vetoes any support-admitted expansion satisfying:



\\\[

\\boxed{

q\_{\\text{state}}\\ge0.50.

}

\\]



No support-conditioning requirement is applied after admission.



This controller provides the high-protection reference point for Experiment 089.



\---



\# Hierarchical Support-Conditioned State Guard



The new prospective rule is:



\\\[

\\boxed{

q\_{\\text{state}}\\ge0.50

}

\\]



and:



\\\[

\\boxed{

d\_{\\text{support}}>2.00.

}

\\]



Both conditions must hold for the responsive expansion to be vetoed.



Thus:



\\\[

\\boxed{

\\text{veto}

=

(q\_{\\text{state}}\\ge0.50)

\\land

(d\_{\\text{support}}>2.00).

}

\\]



The original support-admission condition remains:



\\\[

d\_{\\text{support}}\\le2.50.

\\]



Therefore the architecture partitions support into three conceptual regions.



\---



\# Hierarchical Support Regions



\## Region 1 — Unsupported Expansion



If:



\\\[

d\_{\\text{support}}>2.50,

\\]



the action is rejected by the existing support gate.



\---



\## Region 2 — Weakly Supported Transient Expansion



If:



\\\[

2.00<d\_{\\text{support}}\\le2.50,

\\]



the action is admitted by the base support gate but remains eligible for transient-state veto.



A veto occurs when:



\\\[

q\_{\\text{state}}\\ge0.50.

\\]



\---



\## Region 3 — Stronger-Support Expansion



If:



\\\[

d\_{\\text{support}}\\le2.00,

\\]



the state-risk model does not veto the action under Experiment 089.



This reflects the prospective hypothesis that stronger local support may justify responsiveness even inside a transient-looking operating regime.



\---



\# Prospective Policy Summary



The three controllers produced the following mean results.



| Policy | Mean Regret | Mean Under | Mean Over | Entropy | Recall | Precision | Retention | Beneficial | Harmful |

|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|

| Support Baseline | 0.017331 | 28.50 | 17.60 | 0.526 | 97.000% | 96.217% | 96.150% | 2.65 | 0.70 |

| State Guard 0.50 | \*\*0.017260\*\* | \*\*28.35\*\* | 18.35 | 0.541 | 96.204% | \*\*96.522%\*\* | 94.632% | 1.30 | \*\*0.50\*\* |

| Hierarchical Guard | 0.017298 | 28.45 | 18.05 | 0.532 | 96.699% | 96.336% | \*\*95.585%\*\* | \*\*2.15\*\* | 0.60 |



The results form a clear operating hierarchy.



\---



\# Support Baseline



The support-aware baseline achieved:



\\\[

\\boxed{

R=0.017331

}

\\]



with mean under-persistence:



\\\[

\\boxed{

28.50.

}

\\]



Mean over-persistence was:



\\\[

17.60.

\\]



Mean entropy was:



\\\[

0.526.

\\]



Safe-action recall was:



\\\[

97.000\\%.

\\]



Precision was:



\\\[

96.217\\%.

\\]



Responsive-action retention was:



\\\[

\\boxed{

96.150\\%.

}

\\]



The baseline produced:



\\\[

2.65

\\]



beneficial expansions per seed and:



\\\[

\\boxed{

0.70

}

\\]



harmful expansions per seed.



\---



\# Unconditional State Guard



The unconditional \\(0.50\\) state guard achieved:



\\\[

\\boxed{

R=0.017260.

}

\\]



Mean under-persistence improved to:



\\\[

\\boxed{

28.35.

}

\\]



Mean over-persistence increased to:



\\\[

18.35.

\\]



Mean entropy was:



\\\[

0.541.

\\]



Safe-action recall decreased to:



\\\[

96.204\\%.

\\]



Precision increased to:



\\\[

96.522\\%.

\\]



Responsive retention decreased to:



\\\[

94.632\\%.

\\]



Beneficial expansions fell to:



\\\[

1.30

\\]



per seed.



Harmful expansions fell to:



\\\[

\\boxed{

0.50

}

\\]



per seed.



\---



\# Hierarchical Guard



The hierarchical support-conditioned state guard achieved:



\\\[

\\boxed{

R=0.017298.

}

\\]



Mean under-persistence was:



\\\[

\\boxed{

28.45.

}

\\]



Mean over-persistence was:



\\\[

18.05.

\\]



Mean entropy was:



\\\[

0.532.

\\]



Safe-action recall was:



\\\[

96.699\\%.

\\]



Precision was:



\\\[

96.336\\%.

\\]



Responsive-action retention was:



\\\[

\\boxed{

95.585\\%.

}

\\]



Beneficial expansions averaged:



\\\[

\\boxed{

2.15

}

\\]



per seed.



Harmful expansions averaged:



\\\[

\\boxed{

0.60

}

\\]



per seed.



\---



\# Primary Comparison With Support Baseline



Relative to the support baseline, the hierarchical guard produced:



\\\[

\\boxed{

\\Delta H=-0.100

}

\\]



harmful expansions per seed.



It improved harmful-expansion count in:



\\\[

\\boxed{

2/20

}

\\]



seeds,



was unchanged in:



\\\[

18/20,

\\]



and degraded in:



\\\[

\\boxed{

0/20.

}

\\]



Thus the hierarchical guard did not increase harmful expansion in any prospective seed.



\---



\# Mean Regret Change



The hierarchical guard changed mean regret by:



\\\[

\\boxed{

\\Delta R=-0.000033.

}

\\]



Median regret change was:



\\\[

0\.

\\]



The observed range was:



\\\[

\[-0.000486,\\ 0].

\\]



Regret improved in:



\\\[

\\boxed{

2/20

}

\\]



seeds,



was unchanged in:



\\\[

18/20,

\\]



and degraded in:



\\\[

\\boxed{

0/20.

}

\\]



Thus the hierarchical guard produced no prospective seed-level regret degradation.



\---



\# Under-Persistence Change



Mean under-persistence changed by:



\\\[

\\boxed{

\\Delta U=-0.050.

}

\\]



Thus the hierarchical controller retained a favorable consequence direction relative to the support baseline.



\---



\# Beneficial Expansion Cost



Relative to baseline, the hierarchical controller changed beneficial expansions by:



\\\[

\\boxed{

\\Delta B=-0.500

}

\\]



per seed.



This is substantially smaller than the unconditional state guard's:



\\\[

\\boxed{

\\Delta B=-1.350.

}

\\]



Therefore support conditioning recovers a meaningful fraction of the beneficial responsive actions suppressed by unconditional state vetoing.



\---



\# Responsive Retention Change



The hierarchical controller changes responsive-action retention relative to baseline by:



\\\[

\\boxed{

\-0.565

\\text{ percentage points}.

}

\\]



By contrast, the unconditional state guard changes retention by:



\\\[

\-1.518

\\text{ percentage points}.

\\]



Thus the hierarchical architecture reduces the responsiveness cost by approximately:



\\\[

1.518-0.565

=

\\boxed{

0.953

\\text{ percentage points}.

}

\\]



\---



\# Beneficial Preservation



The unconditional state guard reports mean beneficial preservation:



\\\[

81.439\\%.

\\]



The hierarchical guard improves this to:



\\\[

\\boxed{

91.659\\%.

}

\\]



This is one of the principal prospective findings.



The hierarchical controller retains substantially more useful responsive behavior.



\---



\# Safety Comparison With Unconditional State Guard



The improved selectivity is not free.



The unconditional state guard reduces harmful expansions from:



\\\[

0.70

\\]



to:



\\\[

0.50.

\\]



The hierarchical guard reduces them only to:



\\\[

0.60.

\\]



Therefore:



\\\[

\\boxed{

\\text{hierarchical conditioning gives back part of the safety gain}.

}

\\]



The same structure appears in regret.



Unconditional state guard:



\\\[

R=0.017260.

\\]



Hierarchical guard:



\\\[

R=0.017298.

\\]



Support baseline:



\\\[

R=0.017331.

\\]



Thus the hierarchical controller sits between the baseline and unconditional state guard.



\---



\# Under-Persistence Comparison



Support baseline:



\\\[

28.50.

\\]



Hierarchical guard:



\\\[

28.45.

\\]



Unconditional state guard:



\\\[

28.35.

\\]



Again, the hierarchical controller produces an intermediate safety operating point.



\---



\# Responsive-Retention Comparison



Support baseline:



\\\[

96.150\\%.

\\]



Hierarchical guard:



\\\[

\\boxed{

95.585\\%.

}

\\]



Unconditional state guard:



\\\[

94.632\\%.

\\]



Thus the hierarchical controller also occupies an intermediate responsiveness operating point.



\---



\# Three Operating Modes



Experiment 089 establishes three distinct controller modes.



\## Maximum Responsiveness



The support baseline provides the greatest responsive retention:



\\\[

\\boxed{

96.150\\%.

}

\\]



But it also has the largest harmful-expansion rate:



\\\[

0.70.

\\]



\---



\## Maximum State-Based Protection



The unconditional state guard provides the strongest safety result:



\\\[

\\boxed{

R=0.017260

}

\\]



and:



\\\[

\\boxed{

0.50

\\text{ harmful expansions per seed}.

}

\\]



But it sacrifices the most responsiveness.



\---



\## Intermediate Hierarchical Mode



The hierarchical guard provides:



\\\[

\\boxed{

R=0.017298,

}

\\]



\\\[

\\boxed{

0.60

\\text{ harmful expansions},

}

\\]



and:



\\\[

\\boxed{

95.585\\%

\\text{ responsive retention}.

}

\\]



This represents a more selective compromise.



\---



\# Pareto-Style Interpretation



The three controllers can therefore be interpreted as points along a safety-responsiveness frontier:



\\\[

\\boxed{

\\text{support baseline}

\\rightarrow

\\text{hierarchical guard}

\\rightarrow

\\text{unconditional state guard}.

}

\\]



Moving from left to right:



\- harmful expansion decreases,

\- regret decreases slightly,

\- under-persistence decreases,

\- but beneficial responsiveness also decreases.



Thus Experiment 089 does not identify a universally dominant controller.



Instead, it identifies:



\\\[

\\boxed{

\\text{a meaningful operational frontier}.

}

\\]



\---



\# Prospective Support for the Hierarchical Hypothesis



The prospective hypothesis was that conditioning state vetoing on weaker support would recover beneficial responsive actions while retaining some safety protection.



This prediction is supported.



Relative to the unconditional state guard, the hierarchical controller:



\- preserves more beneficial expansions,

\- retains more responsive actions,

\- vetoes fewer contexts,

\- while still improving harmful expansion, regret, and under-persistence relative to the support baseline.



Therefore:



\\\[

\\boxed{

\\text{support conditioning improves state-guard selectivity prospectively}.

}

\\]



\---



\# Partial Rather Than Complete Preservation of Safety



The stronger version of the hypothesis would have required the hierarchical guard to preserve the full harmful-expansion reduction of the unconditional state guard.



That did not occur.



The unconditional guard achieves:



\\\[

\\Delta H=-0.200

\\]



per seed.



The hierarchical guard achieves:



\\\[

\\Delta H=-0.100.

\\]



Therefore:



\\\[

\\boxed{

\\text{approximately half of the mean harmful-expansion improvement}

\\atop

\\text{relative to baseline is retained}.

}

\\]



This is a partial safety-preservation result rather than complete preservation.



\---



\# Different Prospective Regime



The absolute operating regime in Experiment 089 is substantially harsher than the earlier Experiment 086 seed block.



Experiment 086 support-baseline mean regret was approximately:



\\\[

0.006371.

\\]



Experiment 089 support-baseline mean regret is:



\\\[

\\boxed{

0.017331.

}

\\]



Experiment 086 mean baseline under-persistence was approximately:



\\\[

9.40.

\\]



Experiment 089 baseline under-persistence is:



\\\[

\\boxed{

28.50.

}

\\]



Thus the new prospective block presents substantially larger consequence difficulty.



Despite this, both state-based guards still move harmful expansion and regret in favorable directions.



This is a meaningful robustness observation.



However, Experiment 089 does not independently identify the cause of the regime difference.



Therefore it should not be described as formal distribution-shift validation without further analysis.



\---



\# Mean Harmful-Veto Recall Caveat



The printed mean per-seed harmful-veto recalls were:



\\\[

9.167\\%

\\]



for the unconditional state guard and:



\\\[

6.250\\%

\\]



for the hierarchical guard.



As in Experiment 086, these statistics average seed-level recall values that are set to zero for seeds containing no harmful baseline event.



They should therefore not be interpreted as pooled event-level harmful-veto recall.



A future diagnostic may compute pooled veto counts directly from the event file.



The present prospective conclusions rely on the directly observed harmful-expansion policy outcomes rather than those diluted mean-per-seed recall values.



\---



\# Why the \\(2.00\\) Boundary Remains a Hypothesis



The selective support boundary:



\\\[

\\boxed{

2.00

}

\\]



was frozen before seeds:



\\\[

44031\\text{--}44050

\\]



were evaluated.



Therefore Experiment 089 provides genuine prospective evidence for that rule.



However, it does not establish that:



\\\[

2.00

\\]



is an optimal support threshold.



No threshold sweep was conducted prospectively.



The result should therefore be interpreted as validation of one frozen hierarchical specification, not threshold optimization.



\---



\# Architectural Interpretation



The emerging control architecture is increasingly hierarchical.



The system first asks:



\\\[

\\boxed{

\\text{Is the action predicted consequence-equivalent?}

}

\\]



Then:



\\\[

\\boxed{

\\text{Is the predicted downside acceptable?}

}

\\]



Then:



\\\[

\\boxed{

\\text{Is there sufficient training support?}

}

\\]



Then:



\\\[

\\boxed{

\\text{Is the adaptive system in a transient-risk state?}

}

\\]



Finally, Experiment 089 adds:



\\\[

\\boxed{

\\text{If transient, is support weak enough to justify vetoing}

\\atop

\\text{the otherwise responsive action?}

}

\\]



This separates global support admission from graded support selectivity.



\---



\# Scientific Progression



The relevant experimental chain is now:



\\\[

\\text{080: support distance identifies extrapolation}

\\]



\\\[

\\downarrow

\\]



\\\[

\\text{081: support-aware admission}

\\]



\\\[

\\downarrow

\\]



\\\[

\\text{082--084: residual harmful structure}

\\]



\\\[

\\downarrow

\\]



\\\[

\\text{085: transient-state signature}

\\]



\\\[

\\downarrow

\\]



\\\[

\\text{086: prospective state-veto validation}

\\]



\\\[

\\downarrow

\\]



\\\[

\\text{087: state-veto selectivity decomposition}

\\]



\\\[

\\downarrow

\\]



\\\[

\\text{088: support dominates within vetoed region}

\\]



\\\[

\\downarrow

\\]



\\\[

\\boxed{

\\text{089: prospective hierarchical state-support validation}.

}

\\]



\---



\# What Experiment 089 Establishes



Experiment 089 supports the proposition that:



\\\[

\\boxed{

\\text{conditioning transient-state vetoes on graded support}

\\atop

\\text{can recover responsiveness prospectively}.

}

\\]



It also supports the proposition that this recovery can occur while retaining:



\\\[

\\boxed{

\\text{some harmful-expansion protection}

}

\\]



and without observed seed-level regret degradation.



\---



\# What Experiment 089 Does Not Establish



Experiment 089 does not establish:



\- that the hierarchical guard dominates the unconditional state guard,

\- that \\(2.00\\) is an optimal support boundary,

\- that every operating regime favors hierarchical conditioning,

\- that all harmful mechanisms are captured,

\- or that the architecture is validated beyond the current simulation family.



The result is specifically a prospective computational comparison on seeds:



\\\[

44031\\text{--}44050.

\\]



\---



\# Principal Conclusion



The frozen hierarchical guard prospectively improves selectivity relative to unconditional transient-state vetoing.



Compared with the support baseline, it achieves:



\\\[

\\boxed{

\\Delta H=-0.100

}

\\]



\\\[

\\boxed{

\\Delta R=-0.000033

}

\\]



\\\[

\\boxed{

\\Delta U=-0.050,

}

\\]



with:



\\\[

0

\\]



seeds showing increased harmful expansion and:



\\\[

0

\\]



seeds showing increased regret.



At the same time, it preserves:



\\\[

\\boxed{

91.659\\%

}

\\]



of beneficial expansions on the mean per-seed measure and reduces responsive retention by only:



\\\[

\\boxed{

0.565

\\text{ percentage points}

}

\\]



relative to baseline.



The unconditional state guard provides greater safety improvement but substantially larger responsiveness loss.



Therefore the central Experiment 089 conclusion is:



\\\[

\\boxed{

\\text{support-conditioned state vetoing provides a prospectively}

\\atop

\\text{validated intermediate safety-responsiveness operating point}.

}

\\]



\---



\# Final Architectural Interpretation



The accumulated evidence now supports three controller modes rather than one universally optimal policy.



\### Responsive Mode



Use the support-aware baseline when maximum responsiveness is preferred.



\### Protective Mode



Use unconditional transient-state vetoing when stronger harmful-expansion suppression is preferred.



\### Balanced Hierarchical Mode



Use support-conditioned transient-state vetoing when greater beneficial preservation is preferred while retaining partial safety protection.



Thus:



\\\[

\\boxed{

\\text{the controller can expose an interpretable operating frontier}

\\atop

\\text{rather than hiding the safety-responsiveness tradeoff}

\\atop

\\text{inside a single opaque parameterization}.

}

\\]



\---



\# Next Research Direction



The next experiment should not retune the \\(2.00\\) support boundary on seeds:



\\\[

44031\\text{--}44050.

\\]



Those seeds now belong to the validation history.



A useful next step is first to characterize why the Experiment 089 prospective population is much harsher than the Experiment 086 population.



Experiment 090 should therefore be diagnostic rather than another controller modification.



It should compare seed blocks:



\\\[

44011\\text{--}44030

\\]



and:



\\\[

44031\\text{--}44050

\\]



using already-generated outputs or regenerated context statistics without changing controller parameters.



The analysis should examine whether the increase in baseline regret and under-persistence is associated with changes in:



\- context difficulty,

\- predicted losses,

\- mismatch,

\- anchor age,

\- trigger score,

\- predicted risk,

\- true optimal persistence distribution,

\- safe-action-set structure,

\- and support geometry.



The central question becomes:



\\\[

\\boxed{

\\text{Why does the second prospective seed block produce}

\\atop

\\text{substantially greater consequence difficulty, and do the}

\\atop

\\text{state-based guards remain structurally robust across that change?}

}

\\]



This would determine whether the observed difference represents:



\- ordinary finite-sample variation,

\- a meaningful generated regime shift,

\- or a structural change in the controller's decision environment.

