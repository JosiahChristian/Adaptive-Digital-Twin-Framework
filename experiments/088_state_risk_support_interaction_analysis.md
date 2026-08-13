\# Experiment 088 — State-Risk × Support Interaction Analysis



\## Objective



Experiment 087 showed that the prospectively validated transient-state guard is highly effective at catching harmful expansions, but it also vetoes many beneficial responsive actions.



Within the state-vetoed population, the strongest retrospective discriminator between:



\\\[

\\text{harmful vetoes}

\\]



and:



\\\[

\\text{beneficial vetoes}

\\]



was training-support distance.



Experiment 088 therefore tests whether harmful-veto selectivity is best explained by:



1\. state-risk probability alone,

2\. support distance alone,

3\. the additive combination of state risk and support,

4\. or an explicit interaction between state risk and support.



The central question is:



\\\[

\\boxed{

\\text{Does a state-risk/support interaction improve discrimination}

\\atop

\\text{among already state-vetoed expansion events?}

}

\\]



\---



\## Analysis Population



The input is:



`results/prospective\_state\_guard\_selectivity\_decomposition\_events.csv`



Only events vetoed by the primary \\(0.50\\) state guard are included.



The resulting population contains:



\\\[

\\boxed{

41

}

\\]



events:



\\\[

\\boxed{

5

\\text{ harmful vetoes}

}

\\]



and:



\\\[

\\boxed{

36

\\text{ beneficial vetoes}.

}

\\]



This is a deliberately small retrospective selectivity analysis.



Because only five harmful events are available, model complexity is kept minimal.



\---



\## Validation Strategy



The analysis uses:



\\\[

\\boxed{

\\text{leave-one-generation-seed-out validation}.

}

\\]



Events from one generation seed are held out at a time.



The model is trained using vetoed events from the remaining seeds and evaluated on the held-out population.



This preserves seed-level separation within the already-consumed prospective block.



The experiment remains retrospective because seeds:



\\\[

44011\\text{--}44030

\\]



have already been examined.



\---



\# Candidate Models



Four simple logistic models are compared.



\## State Only



\\\[

M\_1:

\\quad

q\_{\\text{state}}

\\]



where:



\\\[

q\_{\\text{state}}

=

P(

\\text{harmful expansion}

\\mid

X\_{\\text{state}}

).

\\]



\---



\## Support Only



\\\[

M\_2:

\\quad

d\_{\\text{support}}.

\\]



\---



\## State Plus Support



\\\[

M\_3:

\\quad

q\_{\\text{state}}

\+

d\_{\\text{support}}.

\\]



\---



\## Explicit Interaction



\\\[

M\_4:

\\quad

q\_{\\text{state}}

\+

d\_{\\text{support}}

\+

q\_{\\text{state}}

d\_{\\text{support}}.

\\]



The interaction model directly tests whether harmful selectivity depends on the joint magnitude of transient-state risk and support weakness.



\---



\# Model Performance



The pooled leave-one-seed-out results are:



| Model | Balanced Accuracy | Harmful Recall | Harmful Precision | Beneficial Specificity | ROC-AUC |

|---|---:|---:|---:|---:|---:|

| Support Only | \*\*73.333%\*\* | \*\*80.000%\*\* | 25.000% | \*\*66.667%\*\* | \*\*0.722\*\* |

| State + Support | 70.556% | 80.000% | 22.222% | 61.111% | 0.689 |

| State × Support Interaction | 70.556% | 80.000% | 22.222% | 61.111% | 0.683 |

| State Only | 32.222% | 20.000% | 4.762% | 44.444% | 0.361 |



The strongest model is therefore:



\\\[

\\boxed{

\\text{support distance alone}.

}

\\]



\---



\# Support-Only Model



The support-only model achieves:



\\\[

\\boxed{

73.333\\%

\\text{ balanced accuracy}

}

\\]



with:



\\\[

\\boxed{

80.000\\%

\\text{ harmful recall}.

}

\\]



It identifies:



\\\[

4/5

\\]



harmful vetoed events.



The confusion structure is:



\\\[

TP=4,

\\]



\\\[

FP=12,

\\]



\\\[

FN=1,

\\]



\\\[

TN=24.

\\]



Thus:



\\\[

\\boxed{

24/36

}

\\]



beneficial vetoes are correctly recognized as non-harmful.



Beneficial specificity is:



\\\[

\\boxed{

66.667\\%.

}

\\]



ROC-AUC is:



\\\[

\\boxed{

0.722.

}

\\]



\---



\# Support Coefficient Stability



The support-only standardized coefficient is:



\\\[

\\boxed{

+1.243.

}

\\]



Its sign is positive in:



\\\[

\\boxed{

100\\%

}

\\]



of leave-one-seed-out fits.



Thus:



\\\[

\\boxed{

\\text{greater support distance consistently predicts harmful vetoes}.

}

\\]



This independently confirms Experiment 087.



\---



\# State-Only Model



The state-only model performs poorly within the vetoed population.



Balanced accuracy is:



\\\[

\\boxed{

32.222\\%.

}

\\]



Harmful recall is:



\\\[

20.000\\%.

\\]



Beneficial specificity is:



\\\[

44.444\\%.

\\]



ROC-AUC is:



\\\[

\\boxed{

0.361.

}

\\]



The state coefficient is:



\\\[

\-0.253

\\]



with dominant sign stability:



\\\[

92.857\\%.

\\]



Thus higher state probability is not associated with greater harm after conditioning on the fact that all events have already crossed the state-veto boundary.



\---



\# Conditional Interpretation of State Risk



This result does not contradict the prospective success of the state guard.



The state model remains useful for identifying the broader transient-risk regime.



However, once the population is restricted to:



\\\[

q\_{\\text{state}}\\ge0.50,

\\]



state probability no longer ranks harmfulness effectively.



Therefore:



\\\[

\\boxed{

\\text{state risk identifies when caution is warranted}

}

\\]



but:



\\\[

\\boxed{

\\text{state risk does not determine which vetoes are truly necessary}

}

\\]



within the high-risk region.



\---



\# State Plus Support



The additive two-variable model achieves:



\\\[

70.556\\%

\\]



balanced accuracy,



\\\[

80.000\\%

\\]



harmful recall,



\\\[

61.111\\%

\\]



beneficial specificity,



and:



\\\[

0.689

\\]



ROC-AUC.



This is worse than support alone.



The standardized support coefficient remains:



\\\[

\\boxed{

+1.241

}

\\]



with:



\\\[

100\\%

\\]



sign stability.



The state coefficient remains negative:



\\\[

\-0.254.

\\]



Therefore adding state probability contributes no meaningful selectivity improvement after the state gate has already been applied.



\---



\# Explicit Interaction Model



The interaction model includes:



\\\[

q\_{\\text{state}},

\\]



\\\[

d\_{\\text{support}},

\\]



and:



\\\[

q\_{\\text{state}}

d\_{\\text{support}}.

\\]



Its pooled performance is:



\\\[

70.556\\%

\\]



balanced accuracy,



\\\[

80.000\\%

\\]



harmful recall,



\\\[

61.111\\%

\\]



beneficial specificity,



and:



\\\[

0.683

\\]



ROC-AUC.



Thus the explicit interaction does not outperform support alone.



The coefficients are:



\\\[

\\text{support distance}

=

+1.170,

\\]



\\\[

\\text{state probability}

=

\-0.356,

\\]



and:



\\\[

\\text{state}\\times\\text{support}

=

+0.153.

\\]



All three coefficient signs are stable across the evaluated folds.



However, the interaction term is much smaller than the support term.



Therefore:



\\\[

\\boxed{

\\text{the interaction adds complexity without improving discrimination}.

}

\\]



\---



\# Rejection of the Interaction Hypothesis



Experiment 088 directly tests the hypothesis:



\\\[

\\text{harmful selectivity}

\\approx

f(

q\_{\\text{state}}

\\times

d\_{\\text{support}}

).

\\]



The results do not support the interaction model as the superior retrospective representation.



Instead:



\\\[

\\boxed{

d\_{\\text{support}}

\\text{ alone performs best}.

}

\\]



Therefore the stronger interpretation is not that state risk and support must be multiplied or jointly modeled.



The data support a simpler staged architecture.



\---



\# Two-Stage Conditioning Interpretation



The results suggest:



\\\[

\\boxed{

\\text{Stage 1: transient-state risk identifies the caution region}

}

\\]



followed by:



\\\[

\\boxed{

\\text{Stage 2: support distance determines whether a veto}

\\atop

\\text{within that region is likely necessary}.

}

\\]



This is conceptually different from treating the variables as interchangeable predictors in a single model.



State risk and support appear to play different roles.



\---



\# State Risk as a Region Detector



The state guard prospectively demonstrated that the transient-state signature contains useful information.



Its role can now be interpreted approximately as:



\\\[

\\boxed{

\\text{Is the system in a transient regime where responsive}

\\atop

\\text{expansion deserves additional scrutiny?}

}

\\]



This is a regime-level question.



\---



\# Support Distance as a Selectivity Signal



Within that regime, support distance asks:



\\\[

\\boxed{

\\text{How strongly supported is the responsive action by}

\\atop

\\text{nearby training experience?}

}

\\]



Experiment 088 shows that this second question is more informative for distinguishing:



\\\[

\\text{necessary veto}

\\]



from:



\\\[

\\text{unnecessary veto}.

\\]



\---



\# Fold Stability



The support-only model has:



\\\[

\\boxed{

86.111\\%

}

\\]



mean evaluable fold balanced accuracy.



Its minimum evaluable fold balanced accuracy is:



\\\[

\\boxed{

75.000\\%.

}

\\]



Mean fold ROC-AUC is:



\\\[

\\boxed{

0.958.

}

\\]



The support-containing additive and interaction models show the same fold-level summary.



The state-only model performs much worse:



\\\[

16.667\\%

\\]



mean fold balanced accuracy,



with minimum:



\\\[

0\\%.

\\]



Because there are only:



\\\[

5

\\]



harmful events in total, these fold-level metrics should be interpreted cautiously.



Nevertheless, the direction of the support relationship is highly consistent.



\---



\# Small-Sample Limitation



Experiment 088 contains only:



\\\[

5

\\]



harmful examples.



Therefore:



\\\[

\\boxed{

\\text{the observed performance estimates have high uncertainty}.

}

\\]



A single harmful event corresponds to:



\\\[

20

\\]



percentage points of harmful recall.



The result should therefore be interpreted primarily as mechanistic evidence rather than as a precise estimate of future classifier performance.



\---



\# Why Simplicity Matters



The fact that:



\\\[

\\text{support only}

\\]



outperforms:



\\\[

\\text{state + support}

\\]



and:



\\\[

\\text{state + support + interaction}

\\]



is scientifically useful.



It suggests that the selectivity problem does not require a more complicated learned classifier.



The simplest useful hypothesis is:



\\\[

\\boxed{

\\text{within the transient-risk regime, weaker support}

\\atop

\\text{is associated with genuinely harmful responsive expansion}.

}

\\]



This provides a more interpretable architecture.



\---



\# Emerging Hierarchical Controller Principle



The accumulated evidence suggests the following hierarchy:



\\\[

\\boxed{

\\text{safe-action confidence}

}

\\]



\\\[

\\downarrow

\\]



\\\[

\\boxed{

\\text{predicted downside}

}

\\]



\\\[

\\downarrow

\\]



\\\[

\\boxed{

\\text{basic support admission}

}

\\]



\\\[

\\downarrow

\\]



\\\[

\\boxed{

\\text{transient-state caution detection}

}

\\]



\\\[

\\downarrow

\\]



\\\[

\\boxed{

\\text{graded support selectivity}.

}

\\]



The final stage would not necessarily reject every transient-state expansion.



Instead, it could distinguish high-risk transient contexts with weaker support from high-risk transient contexts with stronger empirical backing.



\---



\# No New Guard Is Validated Here



Experiment 088 uses the already-consumed:



\\\[

44011\\text{--}44030

\\]



seed block.



Therefore no threshold or learned rule derived from this analysis is prospectively validated.



The result is:



\\\[

\\boxed{

\\text{retrospective selectivity evidence only}.

}

\\]



Any modified state-support guard must be frozen before evaluation on another untouched seed population.



\---



\# Principal Conclusion



Experiment 088 shows that the selectivity limitation of the transient-state guard is not solved by further use of state probability itself.



Within the 41 state-vetoed expansion events:



\\\[

5

\\]



were harmful and:



\\\[

36

\\]



were beneficial.



The best retrospective discriminator is:



\\\[

\\boxed{

\\text{support distance alone}.

}

\\]



Its performance is:



\\\[

\\boxed{

73.333\\%

\\text{ balanced accuracy}

}

\\]



\\\[

\\boxed{

80.000\\%

\\text{ harmful recall}

}

\\]



\\\[

\\boxed{

66.667\\%

\\text{ beneficial specificity}

}

\\]



with:



\\\[

\\boxed{

\\text{ROC-AUC}=0.722.

}

\\]



The support coefficient is:



\\\[

\\boxed{

+1.243

}

\\]



with:



\\\[

\\boxed{

100\\%

}

\\]



sign stability.



Adding state probability or an explicit state-support interaction does not improve discrimination.



Therefore the central conclusion is:



\\\[

\\boxed{

\\text{state risk is useful for identifying the caution regime,}

\\atop

\\text{while graded support is the stronger signal for deciding}

\\atop

\\text{whether a veto inside that regime is actually necessary}.

}

\\]



\---



\# Next Research Direction



The next experiment should convert this retrospective hierarchy into a frozen prospective hypothesis.



A revised controller should not introduce a complex interaction model unless additional evidence justifies it.



The simplest hypothesis is that the transient-state veto should only be enforced when both:



\\\[

q\_{\\text{state}}\\ge0.50

\\]



and local support is sufficiently weak.



Conceptually:



\\\[

\\boxed{

\\text{veto}

=

\\text{high transient-state risk}

\\land

\\text{weak support}.

}

\\]



However, the support criterion must be frozen before any new seed outcomes are examined.



The current seeds:



\\\[

44011\\text{--}44030

\\]



must not be reused for prospective validation.



Experiment 089 should therefore:



1\. preregister a revised hierarchical guard,

2\. specify its support criterion before execution,

3\. designate a completely untouched generation-seed block,

4\. preserve the existing \\(0.50\\) state threshold,

5\. compare the revised guard against both the support baseline and the prospectively validated Experiment 086 state guard,

6\. measure harmful expansions, regret, under-persistence, and beneficial preservation.



The central prospective question becomes:



\\\[

\\boxed{

\\text{Can support-conditioned state vetoing preserve the harmful}

\\atop

\\text{reduction of Experiment 086 while recovering more}

\\atop

\\text{beneficial responsive expansions?}

}

\\]



Any threshold used in Experiment 089 must be frozen before the new prospective seed block is executed.

