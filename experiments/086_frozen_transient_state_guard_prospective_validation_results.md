\# Experiment 086 — Frozen Transient-State Guard: Prospective Validation Results



\## Status



\\\[

\\boxed{

\\text{PROSPECTIVE EVALUATION COMPLETED}

}

\\]



Experiment 086 was preregistered before the prospective seed block was executed.



The primary controller specification was frozen at:



\\\[

\\tau\_p=0.60,

\\qquad

\\tau\_d=0.020,

\\qquad

\\tau\_s=2.50,

\\qquad

\\tau\_h=0.50.

\\]



The prospective generation seeds were frozen as:



\\\[

44011\\text{--}44030.

\\]



The \\(0.50\\) transient-state guard remained the primary specification throughout the experiment.



The \\(0.40\\) and \\(0.60\\) thresholds were evaluated only as preregistered sensitivity analyses.



\---



\# Prospective Population



The frozen transient-state model was trained only on the retrospective event population identified before Experiment 086:



\\\[

65

\\]



total retrospective action-changing events consisting of:



\\\[

50

\\text{ beneficial}

\\]



and:



\\\[

15

\\text{ harmful}.

\\]



The state model used exactly:



\\\[

\\boxed{

\\{

\\text{current mismatch},

\\text{anchor age},

\\text{trigger score}

\\}

}

\\]



as specified in the preregistration.



The prospective seed block contained:



\\\[

\\boxed{

20

}

\\]



previously untouched generated populations:



\\\[

44011,

44012,

44013,

44014,

44015,

44016,

44017,

44018,

44019,

44020,

\\]



\\\[

44021,

44022,

44023,

44024,

44025,

44026,

44027,

44028,

44029,

44030\.

\\]



No parameter was changed after prospective outcomes were observed.



\---



\# Baseline Controller



The prospective baseline was the previously frozen support-aware controller:



\\\[

\\hat p\_{\\text{safe}}(a)\\ge0.60,

\\]



\\\[

\\hat d(a)\\le0.020,

\\]



and:



\\\[

d\_5(x,a)\\le2.50.

\\]



Across the twenty prospective seeds, the support-aware baseline achieved:



\\\[

\\boxed{

\\text{mean regret}=0.006371

}

\\]



\\\[

\\boxed{

\\text{mean under-persistence}=9.40

}

\\]



\\\[

\\boxed{

\\text{mean over-persistence}=49.90

}

\\]



and:



\\\[

\\boxed{

\\text{mean action entropy}=0.898.

}

\\]



Its safe-action metrics were:



\\\[

\\text{recall}=86.531\\%,

\\]



\\\[

\\text{precision}=94.358\\%,

\\]



and:



\\\[

\\text{responsive-action retention}=78.306\\%.

\\]



The baseline produced an average of:



\\\[

5.00

\\]



beneficial action-changing expansions per seed and:



\\\[

\\boxed{

0.30

}

\\]



harmful expansions per seed.



\---



\# Primary Preregistered State Guard



The primary guard used:



\\\[

\\boxed{

\\tau\_h=0.50.

}

\\]



A support-aware expansion was vetoed when:



\\\[

P(

\\text{harmful expansion}

\\mid

X\_{\\text{state}}

)

\\geq

0.50.

\\]



The resulting controller achieved:



\\\[

\\boxed{

\\text{mean regret}=0.006256

}

\\]



\\\[

\\boxed{

\\text{mean under-persistence}=9.15

}

\\]



\\\[

\\text{mean over-persistence}=50.95

\\]



and:



\\\[

\\text{mean action entropy}=0.882.

\\]



Safe-action metrics were:



\\\[

\\text{recall}=85.435\\%,

\\]



\\\[

\\text{precision}=94.559\\%,

\\]



and:



\\\[

\\text{responsive-action retention}=76.172\\%.

\\]



The guard preserved an average of:



\\\[

3.20

\\]



beneficial expansions per seed and left only:



\\\[

\\boxed{

0.05

}

\\]



harmful expansions per seed.



\---



\# Primary Harmful-Expansion Result



The preregistered primary mechanistic outcome was the change in harmful expansion count.



The mean paired difference was:



\\\[

\\boxed{

\\Delta H=-0.250

}

\\]



harmful expansions per seed.



Thus:



\\\[

0.30

\\rightarrow

0.05.

\\]



Relative to the baseline harmful-expansion rate, this corresponds to an approximate reduction of:



\\\[

\\frac{0.30-0.05}{0.30}

=

0.8333.

\\]



Therefore:



\\\[

\\boxed{

\\text{harmful expansion decreased by approximately }83.3\\%.

}

\\]



This directly supports the primary preregistered hypothesis.



\---



\# Seed-Level Harmful-Expansion Consistency



For the primary \\(0.50\\) guard, harmful-expansion counts were:



\\\[

\\boxed{

\\text{improved in }4/20\\text{ seeds}

}

\\]



\\\[

\\boxed{

\\text{unchanged in }16/20\\text{ seeds}

}

\\]



and:



\\\[

\\boxed{

\\text{degraded in }0/20\\text{ seeds}.

}

\\]



Thus the state guard never increased the number of harmful expansions on any prospective generation seed.



The median paired harmful-expansion difference was:



\\\[

0,

\\]



because most seeds had no baseline harmful expansion to remove.



The aggregate reduction is driven by correctly vetoing harmful events in the subset of seeds where those events actually occurred.



\---



\# Mean Regret Result



The primary guard reduced mean regret from:



\\\[

0.006371

\\]



to:



\\\[

0.006256.

\\]



The mean paired difference was:



\\\[

\\boxed{

\\Delta R=-0.000115.

}

\\]



Median paired regret difference was:



\\\[

0\.

\\]



The seed-level difference range was:



\\\[

\\boxed{

\[-0.000841,\\ 0].

}

\\]



There were:



\\\[

4

\\]



seeds with improved regret,



\\\[

16

\\]



with unchanged regret,



and:



\\\[

\\boxed{

0

}

\\]



with degraded regret.



Therefore the primary guard reduced harmful expansion without producing a prospective regret penalty.



\---



\# Under-Persistence Result



Mean under-persistence decreased from:



\\\[

9.40

\\]



to:



\\\[

9.15.

\\]



The mean paired difference was:



\\\[

\\boxed{

\\Delta U=-0.250.

}

\\]



Median difference was:



\\\[

0\.

\\]



This matches the harmful-expansion reduction structurally.



The result is consistent with the earlier finding that residual harmful expansions manifested primarily as added under-persistence.



\---



\# Joint Primary Outcome



The preregistration identified the preferred pattern as:



\\\[

\\Delta H<0,

\\]



\\\[

\\Delta U\\leq0,

\\]



and:



\\\[

\\Delta R\\leq0.

\\]



The prospective primary result is:



\\\[

\\boxed{

\\Delta H=-0.250

}

\\]



\\\[

\\boxed{

\\Delta U=-0.250

}

\\]



\\\[

\\boxed{

\\Delta R=-0.000115.

}

\\]



Thus all three primary outcome directions are favorable.



The state guard therefore satisfies the strongest preregistered consequence pattern in aggregate.



\---



\# No Prospective Safety Degradation



An important aspect of the result is that the primary guard did not improve one safety metric at the expense of another.



Across twenty untouched seeds:



\- harmful expansion decreased,

\- under-persistence decreased,

\- mean regret decreased,

\- no seed showed increased harmful expansion,

\- and no seed showed increased regret.



Therefore the observed prospective safety effect is internally coherent.



\---



\# Responsiveness Cost



The state guard is not cost-free.



Responsive-action retention decreased from:



\\\[

78.306\\%

\\]



to:



\\\[

76.172\\%.

\\]



The absolute reduction was:



\\\[

\\boxed{

2.134

\\text{ percentage points}.

}

\\]



Safe-action recall decreased from:



\\\[

86.531\\%

\\]



to:



\\\[

85.435\\%.

\\]



Mean over-persistence increased from:



\\\[

49.90

\\]



to:



\\\[

50.95.

\\]



Action entropy decreased from:



\\\[

0.898

\\]



to:



\\\[

0.882.

\\]



These results demonstrate that the improved safety comes from selective conservatism.



The guard suppresses some responsive actions in order to eliminate harmful ones.



\---



\# Beneficial Expansion Preservation



The support baseline produced:



\\\[

5.00

\\]



beneficial expansions per seed.



The primary \\(0.50\\) guard retained:



\\\[

3.20.

\\]



The reported mean per-seed beneficial-preservation quantity was:



\\\[

\\boxed{

66.061\\%.

}

\\]



Thus approximately two-thirds of beneficial responsive expansions were retained.



This means the state guard does not simply collapse the expansion mechanism.



However, it does remove a substantial fraction of useful responsive actions.



\---



\# Harmful Veto Selectivity



The printed mean per-seed harmful-veto recall was:



\\\[

18.333\\%.

\\]



This quantity must be interpreted carefully.



The implementation computes harmful-veto recall separately within each seed and assigns:



\\\[

0

\\]



when a seed contains no harmful baseline expansion.



Because most prospective seeds contain no harmful baseline event, averaging those seed-level values strongly dilutes the result.



The pooled controller-level counts provide the more relevant mechanistic interpretation.



The baseline averages:



\\\[

0.30

\\]



harmful events over:



\\\[

20

\\]



seeds, implying approximately:



\\\[

6

\\]



total harmful baseline expansions.



The primary guard averages:



\\\[

0.05

\\]



over twenty seeds, implying approximately:



\\\[

1

\\]



harmful event remains.



Thus approximately:



\\\[

5/6

\\]



baseline harmful events were removed.



The pooled harmful-veto fraction is therefore approximately:



\\\[

\\boxed{

83.3\\%.

}

\\]



This distinction should be preserved in all future reporting.



\---



\# Primary Selectivity Tradeoff



The primary guard therefore produces approximately:



\\\[

\\boxed{

83.3\\%

\\text{ pooled harmful-event removal}

}

\\]



while retaining approximately:



\\\[

\\boxed{

66\\%

\\text{ of beneficial expansions}.

}

\\]



This is meaningful selectivity.



The state model preferentially suppresses harmful expansions more strongly than beneficial ones.



However, the difference is not sufficient to describe the guard as perfectly selective.



\---



\# Sensitivity Analysis: \\(\\tau\_h=0.40\\)



The more conservative sensitivity guard achieved:



\\\[

\\text{mean regret}=0.006256,

\\]



\\\[

\\text{mean under-persistence}=9.15,

\\]



\\\[

\\text{mean over-persistence}=51.20,

\\]



and:



\\\[

\\text{responsive retention}=74.732\\%.

\\]



It left:



\\\[

0.05

\\]



harmful expansions per seed, the same observed mean as the primary \\(0.50\\) guard.



However, beneficial expansions fell to:



\\\[

1.95

\\]



per seed.



Reported beneficial preservation was only:



\\\[

\\boxed{

43.759\\%.

}

\\]



Thus the \\(0.40\\) guard is substantially more conservative without improving the observed aggregate harmful-expansion result beyond the primary specification.



This supports the preregistered interpretation of \\(0.50\\) as a more balanced operating point.



\---



\# Sensitivity Analysis: \\(\\tau\_h=0.60\\)



The more permissive sensitivity guard achieved:



\\\[

\\text{mean regret}=0.006298,

\\]



\\\[

\\text{mean under-persistence}=9.20,

\\]



\\\[

\\text{mean over-persistence}=50.55,

\\]



and:



\\\[

\\text{responsive retention}=76.895\\%.

\\]



Beneficial preservation increased to:



\\\[

\\boxed{

79.956\\%.

}

\\]



However, harmful expansion increased relative to the primary guard:



\\\[

0.10

\\]



per seed versus:



\\\[

0.05.

\\]



Thus the \\(0.60\\) specification retains more responsiveness but provides weaker harmful-expansion suppression.



\---



\# Sensitivity Structure



The three preregistered thresholds reveal a coherent operating tradeoff.



\## \\(0.40\\)



More conservative:



\\\[

\\text{lower responsiveness}

\\]



with strong harmful suppression.



\## \\(0.50\\)



Intermediate:



\\\[

\\boxed{

\\text{strong harmful suppression}

\+

\\text{moderate beneficial preservation}.

}

\\]



\## \\(0.60\\)



More permissive:



\\\[

\\text{greater beneficial preservation}

\\]



but weaker harmful suppression.



This monotonic qualitative structure increases confidence that the state probability is behaving as a meaningful risk score rather than producing an arbitrary threshold artifact.



\---



\# Why the Primary Result Is Stronger Than the Sensitivity Results



The primary specification was frozen before prospective outcomes were observed:



\\\[

\\boxed{

\\tau\_h=0.50.

}

\\]



Therefore its result constitutes the actual prospective test.



The \\(0.40\\) and \\(0.60\\) findings provide context but do not replace the primary result.



Even if one sensitivity threshold had produced numerically better performance, it would remain a secondary observation requiring future prospective validation before becoming a new primary controller.



\---



\# Prospective Validation of the Retrospective Mechanism



Experiment 085 identified the retrospective signature:



\\\[

\\boxed{

\\text{younger anchor}

\+

\\text{higher current mismatch}

\+

\\text{lower trigger score}.

}

\\]



Experiment 086 froze a logistic model based only on those three quantities before evaluating fresh seeds.



The resulting guard substantially reduced harmful expansion on the untouched population.



Therefore the retrospective state signature possesses genuine prospective operational value.



This is qualitatively stronger evidence than retrospective cross-validation alone.



\---



\# From Description to Intervention



The experimental progression is now:



\\\[

\\text{084: feature decomposition}

\\]



\\\[

\\downarrow

\\]



\\\[

\\text{085: retrospective multivariate state signature}

\\]



\\\[

\\downarrow

\\]



\\\[

\\boxed{

\\text{086: frozen prospective intervention}

}

\\]



The mechanism therefore moved from:



\\\[

\\text{descriptive correlation}

\\]



to:



\\\[

\\boxed{

\\text{prospectively useful control information}.

}

\\]



\---



\# Adaptation-State Interpretation



The state guard suggests that action safety depends on more than nominal candidate-action consequence estimates.



A responsive action may satisfy:



\\\[

\\hat p\_{\\text{safe}}\\ge0.60,

\\]



\\\[

\\hat d\\le0.020,

\\]



and:



\\\[

d\_5\\le2.50,

\\]



yet still be unsafe when the adaptive system is in a transient regime.



The new state model provides evidence about whether the current adaptation regime is mature enough to trust the responsive action.



This suggests three distinct evidence layers:



\\\[

\\boxed{

\\text{action safety}

}

\\]



\\\[

\\boxed{

\\text{epistemic support}

}

\\]



and:



\\\[

\\boxed{

\\text{adaptation-state stability}.

}

\\]



\---



\# Architectural Result



The emerging controller architecture can be summarized as:



\\\[

\\boxed{

\\text{Primary consequence gate}

}

\\]



followed by:



\\\[

\\boxed{

\\text{safe-action expansion}

}

\\]



followed by:



\\\[

\\boxed{

\\text{predicted-downside filtering}

}

\\]



followed by:



\\\[

\\boxed{

\\text{training-support filtering}

}

\\]



followed by:



\\\[

\\boxed{

\\text{transient-state veto}.

}

\\]



Each layer emerged from a distinct experimentally identified failure mode.



\---



\# Progression of Failure Modes



\## Safe-Set False Negatives



Earlier experiments showed that the primary gate omitted many genuinely safe responsive actions.



This motivated expansion.



\## Unsafe Expansion



Probability-only expansion recovered responsiveness but admitted dangerous false-safe actions.



This motivated downside modeling.



\## Cost-Unaware False Positives



Downside-aware gating reduced severe expansion errors.



\## Support Extrapolation



Residual harmful events were confidently wrong but occurred far from meta-training support.



This motivated support-aware gating.



\## Residual Systematic Expansion Bias



Cross-seed validation showed that some harmful events remained even after support filtering.



\## Transient Adaptation State



Experiments 084 and 085 identified a younger-anchor / higher-mismatch / lower-trigger regime.



Experiment 086 prospectively validates that this state contains useful veto information.



\---



\# Scientific Significance



Experiment 086 is important because the state model was not merely fitted and evaluated retrospectively.



Its:



\- training population,

\- feature set,

\- preprocessing,

\- classifier family,

\- regularization,

\- primary probability threshold,

\- baseline controller,

\- and prospective seed block



were all frozen before execution.



The result therefore provides substantially stronger evidence that adaptation-state information improves controller safety.



\---



\# What Experiment 086 Establishes



Experiment 086 supports the proposition that:



\\\[

\\boxed{

\\text{transient adaptation state contains prospectively useful}

\\atop

\\text{information about harmful responsive expansion}.

}

\\]



It also supports the proposition that a frozen state-risk veto can reduce:



\\\[

\\text{harmful expansion},

\\]



\\\[

\\text{under-persistence},

\\]



and:



\\\[

\\text{mean regret}

\\]



on untouched generated populations.



\---



\# What Experiment 086 Does Not Establish



Experiment 086 does not establish that:



\- the \\(0.50\\) threshold is universally optimal,

\- the three state variables are sufficient for every environment,

\- the logistic model is the final controller architecture,

\- harmful expansion can be eliminated completely,

\- or the controller has been validated outside the current simulation family.



The result remains computational prospective validation inside the current generated adaptive-digital-twin environment.



\---



\# Primary Conclusion



The preregistered primary transient-state guard achieved:



\\\[

\\boxed{

0.30

\\rightarrow

0.05

}

\\]



mean harmful expansions per seed,



corresponding to approximately:



\\\[

\\boxed{

83.3\\%

}

\\]



aggregate harmful-expansion reduction.



Mean regret improved:



\\\[

\\boxed{

0.006371

\\rightarrow

0.006256

}

\\]



and mean under-persistence improved:



\\\[

\\boxed{

9.40

\\rightarrow

9.15.

}

\\]



No prospective seed showed increased harmful expansion.



No prospective seed showed increased regret.



At the same time, responsive-action retention decreased:



\\\[

78.306\\%

\\rightarrow

76.172\\%,

\\]



and approximately:



\\\[

66\\%

\\]



of beneficial expansions were preserved.



Therefore the prospective result is:



\\\[

\\boxed{

\\text{strong support for the transient-state guard}

}

\\]



with a measurable but controlled responsiveness cost.



\---



\# Principal Scientific Interpretation



The result suggests that safe responsive control requires distinguishing two questions:



\\\[

\\text{“Is this responsive action predicted to be safe?”}

\\]



and:



\\\[

\\boxed{

\\text{“Is the adaptive system currently stable enough}

\\atop

\\text{to trust that safety prediction?”}

}

\\]



Training-support distance addresses whether the model has nearby experience.



The transient-state guard addresses whether the evolving system itself appears to be in a stable enough regime for aggressive responsiveness.



This distinction is a central architectural insight emerging from the experimental sequence.



\---



\# Next Research Direction



Experiment 087 should not retune the transient-state threshold on seeds 44011–44030.



Those seeds now belong to the prospective validation history.



Instead, the next step should investigate \*\*selectivity improvement\*\* while preserving the prospective finding.



The current primary guard removes approximately:



\\\[

83.3\\%

\\]



of harmful expansions but preserves only about:



\\\[

66\\%

\\]



of beneficial expansions.



Thus the next research question is:



\\\[

\\boxed{

\\text{Can transient-state protection become more selective}

\\atop

\\text{without weakening its harmful-expansion suppression?}

}

\\]



Before designing a new controller, Experiment 087 should first analyze the prospective event-level output from Experiment 086.



This analysis should remain diagnostic.



It should compare:



\- harmful baseline expansions correctly vetoed,

\- harmful baseline expansions missed,

\- beneficial expansions preserved,

\- beneficial expansions unnecessarily vetoed,



using the already-saved prospective event records.



Candidate diagnostics include:



\- frozen state probability,

\- current mismatch,

\- anchor age,

\- trigger score,

\- support distance,

\- safe-action confidence,

\- predicted downside,

\- and action transition size.



The objective should be to determine whether false-positive state vetoes occupy a distinct region from correctly vetoed harmful expansions.



No new threshold should be selected on seeds:



\\\[

44011\\text{--}44030

\\]



and reported as validated.



Any revised guard motivated by this analysis must be frozen and tested on another untouched future seed population.



The next central question is:



\\\[

\\boxed{

\\text{Why does the prospectively validated state guard reject}

\\atop

\\text{some beneficial expansions, and can that selectivity}

\\atop

\\text{problem be characterized without compromising validation integrity?}

}

\\]

