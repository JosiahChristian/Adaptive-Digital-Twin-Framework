\# Experiment 086 — Frozen Transient-State Guard: Prospective Validation



\## Status



\\\[

\\boxed{

\\text{PREREGISTERED BEFORE PROSPECTIVE-SEED EXECUTION}

}

\\]



Experiment 086 is a prospective validation experiment.



Its controller specification, primary hypothesis, seed population, primary comparison, and evaluation criteria are defined before any outcome from the prospective seed block is examined.



No result from generation seeds:



\\\[

44011,\\ldots,44030

\\]



may be used to modify the Experiment 086 primary specification and subsequently be reported as validation on the same seed block.



\---



\# Motivation



Experiments 084 and 085 identified a recurring retrospective signature associated with harmful support-aware expansion.



Experiment 085 found that a simple state-only logistic model using:



\\\[

X\_{\\text{state}}

=

\\{

\\text{current mismatch},

\\text{anchor age},

\\text{trigger score}

\\}

\\]



provided the strongest pooled retrospective harmful-expansion classification among the tested feature families.



Its pooled leave-one-generation-seed-out performance was:



\\\[

\\text{balanced accuracy}

=

69.667\\%,

\\]



\\\[

\\text{harmful recall}

=

73.333\\%,

\\]



\\\[

\\text{beneficial specificity}

=

66.000\\%,

\\]



and:



\\\[

\\text{ROC-AUC}

=

0.717.

\\]



The mean standardized coefficients were:



\\\[

\\boxed{

\\beta\_{\\text{anchor age}}=-0.757

}

\\]



\\\[

\\boxed{

\\beta\_{\\text{current mismatch}}=+0.644

}

\\]



\\\[

\\boxed{

\\beta\_{\\text{trigger score}}=-0.360.

}

\\]



All three coefficient signs were stable across every evaluable leave-one-generation-seed-out fit.



The resulting retrospective signature was:



\\\[

\\boxed{

\\text{younger anchor}

\+

\\text{higher current mismatch}

\+

\\text{lower trigger score}.

}

\\]



However, Experiment 085 explicitly did not establish a validated controller guard.



Experiment 086 tests whether this retrospectively discovered state signature has prospective operational value.



\---



\# Scientific Question



The central question is:



\\\[

\\boxed{

\\text{Can a frozen transient-state risk model reduce harmful}

\\atop

\\text{support-aware expansions on completely untouched seeds?}

}

\\]



The experiment specifically tests whether the dynamic state of adaptation contains information that improves the existing support-aware admission mechanism.



\---



\# Existing Frozen Support-Aware Controller



The baseline controller for Experiment 086 is the support-aware expansion architecture previously evaluated with:



\\\[

\\boxed{

\\tau\_p=0.60

}

\\]



for safe-action probability,



\\\[

\\boxed{

\\tau\_d=0.020

}

\\]



for predicted downside,



and:



\\\[

\\boxed{

\\tau\_s=2.50

}

\\]



for training-support distance.



A candidate responsive action is therefore admitted by the baseline only when:



\\\[

\\hat p\_{\\text{safe}}(a)

\\geq

0.60,

\\]



\\\[

\\hat d(a)

\\leq

0.020,

\\]



and:



\\\[

d\_5(x,a)

\\leq

2.50.

\\]



These thresholds remain unchanged in Experiment 086.



\---



\# Frozen State-Risk Model



Experiment 086 introduces one additional layer.



A logistic harmful-expansion classifier is trained using the complete retrospective beneficial/harmful event population from Experiment 084.



The training population contains:



\\\[

N=65

\\]



events:



\\\[

50

\\text{ beneficial}

\\]



and:



\\\[

15

\\text{ harmful}.

\\]



The model uses exactly three predictors:



\\\[

\\boxed{

X\_{\\text{state}}

=

\\{

\\text{current mismatch},

\\text{anchor age},

\\text{trigger score}

\\}.

}

\\]



No additional features may be introduced after prospective evaluation begins.



The preprocessing and classifier specification are frozen as:



\- training-data standardization,

\- class-weighted logistic regression,

\- L2-equivalent regularization,

\- \\(C=1.0\\),

\- deterministic random state,

\- no prospective retraining.



The scaler and logistic model are fitted once using the retrospective event population.



They are then frozen for all prospective seeds.



For a candidate expansion event, the model produces:



\\\[

q\_t

=

P(

\\text{harmful expansion}

\\mid

X\_{\\text{state},t}

).

\\]



\---



\# Primary State Guard



The primary preregistered state-risk threshold is:



\\\[

\\boxed{

\\tau\_h=0.50.

}

\\]



A candidate action that already satisfies the support-aware baseline admission criteria is permitted only if:



\\\[

\\boxed{

q\_t<0.50.

}

\\]



If:



\\\[

q\_t\\geq0.50,

\\]



the responsive expansion is vetoed and the controller retains the primary-gate action.



Thus the primary Experiment 086 controller is:



\\\[

\\boxed{

\\text{support-aware}\_{2.50}

\+

\\text{state-veto}\_{0.50}.

}

\\]



The value:



\\\[

0.50

\\]



is selected before prospective execution because it is the natural classification boundary of the logistic model.



It is not selected through prospective threshold optimization.



\---



\# Sensitivity Specifications



Two additional state thresholds are preregistered:



\\\[

\\boxed{

\\tau\_h=0.40

}

\\]



and:



\\\[

\\boxed{

\\tau\_h=0.60.

}

\\]



These are sensitivity analyses only.



They will be evaluated to determine whether the qualitative behavior of the state guard depends strongly on the exact probability threshold.



The three specifications are therefore:



\\\[

\\text{state guard}\_{0.40},

\\]



\\\[

\\boxed{

\\text{state guard}\_{0.50}

}

\\quad\\text{PRIMARY},

\\]



and:



\\\[

\\text{state guard}\_{0.60}.

\\]



The \\(0.40\\) and \\(0.60\\) variants may not replace the \\(0.50\\) specification as the primary prospective test after outcomes are observed.



\---



\# Prospective Seed Population



Experiment 086 uses exactly twenty new generation seeds:



\\\[

\\boxed{

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

}

\\]



\\\[

\\boxed{

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

}

\\]



These seeds were not used in Experiments 082–085.



They therefore constitute the prospective evaluation population for the frozen Experiment 086 hypothesis.



The seed list itself is frozen before execution.



\---



\# No Adaptive Intervention



Once Experiment 086 begins, the following are prohibited until all twenty prospective seeds have been evaluated:



\- changing the state feature set,

\- changing model regularization,

\- changing class weights,

\- changing preprocessing,

\- changing the support threshold,

\- changing the downside threshold,

\- changing the safe-probability threshold,

\- changing the primary state threshold,

\- excluding unfavorable seeds,

\- selecting a subset of contexts,

\- retraining the state model on prospective observations,

\- or redefining harmful and beneficial outcomes.



Any modification motivated by Experiment 086 results must become a new experiment using another untouched seed block.



\---



\# Baseline Comparison



The primary comparison is:



\\\[

\\boxed{

\\text{state guard}\_{0.50}

\\quad\\text{vs.}\\quad

\\text{support-aware}\_{2.50}.

}

\\]



Both controllers operate on identical generated contexts within each seed.



This permits paired seed-level and event-level comparison.



\---



\# Primary Outcomes



Three outcomes are designated as primary.



\## Harmful Expansions



Let:



\\\[

H\_s^{B}

\\]



denote the number of harmful action-changing expansions under the support-aware baseline for seed \\(s\\).



Let:



\\\[

H\_s^{G}

\\]



denote the corresponding number under the state-guarded controller.



Define:



\\\[

\\Delta H\_s

=

H\_s^{G}

\-

H\_s^{B}.

\\]



Improvement corresponds to:



\\\[

\\boxed{

\\Delta H\_s<0.

}

\\]



Across the complete prospective population, the primary mechanistic hypothesis is:



\\\[

\\boxed{

\\sum\_s H\_s^{G}

<

\\sum\_s H\_s^{B}.

}

\\]



\---



\## Mean Regret



For each seed:



\\\[

\\Delta R\_s

=

R\_s^{G}

\-

R\_s^{B}.

\\]



The preferred result is:



\\\[

\\boxed{

\\Delta R\_s\\leq0

}

\\]



in aggregate.



The guard should not achieve apparent safety merely by producing a substantial increase in overall regret.



\---



\## Under-Persistence Errors



For each seed:



\\\[

\\Delta U\_s

=

U\_s^{G}

\-

U\_s^{B}.

\\]



The desired direction is:



\\\[

\\boxed{

\\Delta U\_s\\leq0.

}

\\]



Because prior experiments established a close relationship between harmful expansion and under-persistence error, this is a major consequence-level endpoint.



\---



\# Secondary Outcomes



Secondary outcomes include:



\- beneficial expansions,

\- beneficial expansions preserved,

\- beneficial expansions vetoed,

\- neutral expansions,

\- responsive-action retention,

\- safe-action recall,

\- safe-action precision,

\- over-persistence count,

\- action entropy,

\- expansion count,

\- veto count,

\- state-risk probability,

\- and seed-level paired performance.



These outcomes provide diagnostic interpretation but do not replace the preregistered primary comparison.



\---



\# Guard Selectivity



The guard should distinguish harmful expansions from beneficial expansions rather than simply vetoing all responsive behavior.



Define harmful-veto recall:



\\\[

\\text{HVR}

=

\\frac{

N\_{\\text{harmful vetoed}}

}{

N\_{\\text{harmful baseline expansions}}

}.

\\]



Define beneficial preservation:



\\\[

\\text{BP}

=

\\frac{

N\_{\\text{beneficial preserved}}

}{

N\_{\\text{beneficial baseline expansions}}

}.

\\]



A useful guard should increase HVR while maintaining substantial BP.



A controller that eliminates harmful expansions only by eliminating nearly all beneficial expansion will not be interpreted as a successful selective mechanism.



\---



\# Mechanistic Prediction



Experiment 085 implies that high state-risk probabilities should preferentially occur when:



\\\[

\\text{anchor age}

\\]



is smaller,



\\\[

\\text{current mismatch}

\\]



is larger,



and:



\\\[

\\text{trigger score}

\\]



is smaller.



Therefore Experiment 086 predicts that vetoed events should, on average, exhibit:



\\\[

\\boxed{

\\text{younger anchors}

}

\\]



\\\[

\+

\\]



\\\[

\\boxed{

\\text{higher mismatch}

}

\\]



\\\[

\+

\\]



\\\[

\\boxed{

\\text{lower trigger scores}.

}

\\]



This provides a prospective test not only of controller performance but also of the mechanism inferred retrospectively.



\---



\# Primary Hypothesis



The primary preregistered hypothesis is:



\\\[

\\boxed{

H\_1:

\\text{The frozen }0.50\\text{ transient-state guard reduces}

\\atop

\\text{harmful support-aware expansions on seeds }44011\\text{--}44030.

}

\\]



The corresponding null is:



\\\[

\\boxed{

H\_0:

\\text{The frozen state guard does not reduce harmful expansion}

\\atop

\\text{on the prospective seed population.}

}

\\]



\---



\# Consequence-Preservation Hypothesis



A second preregistered expectation is that harmful-expansion reduction should not require substantial degradation of consequence performance.



The preferred pattern is:



\\\[

\\boxed{

\\Delta H<0,

\\qquad

\\Delta U\\leq0,

\\qquad

\\Delta R\\leq0.

}

\\]



This represents the strongest prospective result.



However, all observed tradeoffs will be reported directly.



\---



\# Interpretation Framework



Experiment 086 will be interpreted using the following qualitative outcome classes.



\## Strong Support



Strong support occurs if the primary \\(0.50\\) guard:



\- reduces harmful expansions,

\- reduces or preserves under-persistence performance,

\- reduces or preserves mean regret,

\- and retains a substantial fraction of beneficial expansions.



This would provide strong evidence that the retrospective state signature has genuine controller value.



\---



\## Partial Support



Partial support occurs if harmful expansions decrease but:



\- regret increases modestly,

\- under-persistence does not improve,

\- or beneficial-expansion preservation is weak.



This would indicate that the state signal generalizes but requires a better decision architecture.



\---



\## Mechanistic Support Without Controller Improvement



If state-risk probability prospectively distinguishes harmful from beneficial events but the binary veto does not improve overall controller performance, the result will be interpreted as support for the mechanism but not for the proposed intervention.



\---



\## No Prospective Support



If the primary guard fails to reduce harmful expansion or performs no better than baseline while sacrificing beneficial responsiveness, the retrospective signature will not be considered prospectively operational.



The result will be retained as a negative finding.



\---



\# Sensitivity Analysis Interpretation



The \\(0.40\\) and \\(0.60\\) thresholds are evaluated only after preserving the \\(0.50\\) specification as primary.



If either sensitivity threshold performs better than \\(0.50\\), that result may motivate a future hypothesis.



It will not retroactively redefine Experiment 086's primary test.



Therefore:



\\\[

\\boxed{

\\text{best sensitivity result}

\\neq

\\text{primary prospective result}.

}

\\]



This protects the experiment from threshold-selection bias.



\---



\# Statistical Perspective



The prospective population contains:



\\\[

20

\\]



generation seeds.



Seed-level outcomes will therefore be emphasized alongside pooled context-level quantities.



For each primary metric, Experiment 086 should report:



\- mean seed-level difference,

\- median seed-level difference,

\- number of improved seeds,

\- number of unchanged seeds,

\- number of degraded seeds,

\- minimum and maximum seed-level difference,

\- and aggregate totals.



Because the experiment is designed primarily as prospective computational validation rather than a large-sample inferential trial, effect direction, magnitude, consistency, and paired seed structure are emphasized over isolated significance testing.



\---



\# Reproducibility Requirements



The implementation must record:



\- prospective generation seed,

\- controller specification,

\- state-risk threshold,

\- state-risk probability,

\- baseline action,

\- guarded action,

\- whether expansion occurred,

\- whether a veto occurred,

\- whether the baseline expansion was beneficial, harmful, or neutral,

\- regret,

\- under-persistence status,

\- over-persistence status,

\- safe-set metrics,

\- responsiveness metrics,

\- and relevant state variables.



Aggregate and seed-level CSV outputs must be saved.



Event-level veto diagnostics should also be preserved.



\---



\# Prospective Integrity Rule



The following rule governs all subsequent interpretation:



\\\[

\\boxed{

\\text{Observe first. Explain second. Modify only in a new experiment.}

}

\\]



If Experiment 086 fails, the failure is part of the result.



No parameter will be altered and rerun on seeds:



\\\[

44011\\text{--}44030

\\]



as though the altered specification were still prospective.



Any revised architecture must use a separately designated future seed population.



\---



\# Expected Scientific Contribution



If successful, Experiment 086 will establish a progression from:



\\\[

\\text{safe-action prediction}

\\]



to:



\\\[

\\text{support-aware admission}

\\]



to:



\\\[

\\boxed{

\\text{adaptation-state-aware admission}.

}

\\]



This would imply that safe responsive control in the adaptive digital twin requires more than estimating whether an action is nominally safe.



It would require reasoning about whether the system is currently in a sufficiently stable adaptive regime to trust that estimate.



The architecture would therefore distinguish:



\\\[

\\text{action safety},

\\]



\\\[

\\text{epistemic support},

\\]



and:



\\\[

\\text{transient adaptation risk}.

\\]



\---



\# Preregistered Conclusion Boundary



No conclusion about Experiment 086 is made in this document.



At preregistration time:



\\\[

\\boxed{

\\text{the outcomes of seeds }44011\\text{--}44030

\\text{ are unknown}.

}

\\]



The primary specification is:



\\\[

\\boxed{

\\tau\_p=0.60,

\\quad

\\tau\_d=0.020,

\\quad

\\tau\_s=2.50,

\\quad

\\tau\_h=0.50.

}

\\]



The prospective seed population is:



\\\[

\\boxed{

44011\\text{--}44030.

}

\\]



The primary question is frozen as:



\\\[

\\boxed{

\\text{Does the }0.50\\text{ transient-state guard reduce harmful}

\\atop

\\text{expansion without degrading consequence performance?}

}

\\]



Only after this specification is saved should the Experiment 086 implementation be constructed and the prospective seed block executed.

