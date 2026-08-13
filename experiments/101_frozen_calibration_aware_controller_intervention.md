\# Experiment 101 — Frozen Calibration-Aware Controller Intervention



\## Purpose



Experiment 099 discovered that local historical consequence-model calibration behavior contains substantial information about future severe consequence underestimation.



Experiment 100 then prospectively validated that representation on the untouched seed block:



\\\[

44071\\text{–}44090.

\\]



The preregistered primary representation:



\\\[

\\texttt{loss\\\_plus\\\_local\\\_calibration}

\\]



outperformed:



\\\[

\\texttt{predicted\\\_loss\\\_only}

\\]



on both prospective ROC AUC and balanced accuracy.



Experiment 101 moves from:



\\\[

\\boxed{

\\text{prediction of calibration failure}

}

\\]



to:



\\\[

\\boxed{

\\text{controller intervention using calibration-risk information}.

}

\\]



The central question is:



> Can a frozen calibration-aware veto improve the support-aware adaptive controller by preventing dangerous responsive expansions while preserving useful adaptation?



\---



\# Experimental Role



Experiment 101 is the first prospective controller-intervention experiment based on the historical calibration-risk representation validated in Experiment 100.



It must remain distinct from Experiment 100.



Experiment 100 established predictive representation validity.



Experiment 101 tests whether acting on that representation improves controller behavior.



No Experiment 101 prospective outcome may be used to:



\- modify the representation,

\- choose the intervention threshold,

\- tune the classifier,

\- alter the support threshold,

\- change the severe-underestimation definition,

\- or revise the intervention logic.



\---



\# Historical Development Population



For Experiment 101, all outcomes through Experiment 100 are now historical information.



The historical development block is:



\\\[

\\boxed{

44001\\text{–}44090.

}

\\]



These seeds may be used to:



\- construct calibration-memory representations,

\- fit the frozen calibration-risk classifier,

\- and select the calibration-risk operating threshold according to the preregistered procedure below.



No seed from the Experiment 101 prospective block may enter this process.



\---



\# Untouched Prospective Seed Block



The Experiment 101 prospective validation block is frozen as:



\\\[

\\boxed{

44091\\text{–}44110.

}

\\]



This contains:



\\\[

\\boxed{

20

}

\\]



new generation seeds.



Before observing any outcomes from these seeds, the following must be frozen:



\- model specification,

\- historical development population,

\- local-neighborhood size,

\- calibration-risk threshold-selection procedure,

\- controller intervention logic,

\- baseline policy,

\- primary outcome metrics,

\- and interpretation criteria.



\---



\# Frozen Historical Calibration Representation



Experiment 101 uses the same primary representation validated in Experiment 100:



\\\[

\\boxed{

\\texttt{loss\\\_plus\\\_local\\\_calibration}.

}

\\]



Its features are:



1\. `predicted\_action\_loss`

2\. `local\_mean\_error`

3\. `local\_error\_std`

4\. `local\_underestimate\_fraction`

5\. `local\_severe\_underestimate\_fraction`



The local neighborhood size remains:



\\\[

\\boxed{

K=7.

}

\\]



No feature may be added or removed after the prospective block begins.



\---



\# Calibration Error Definition



Historical calibration error remains:



\\\[

\\boxed{

e\_i

=

\\hat L\_i-L\_i.

}

\\]



Negative values represent consequence underestimation.



Severe consequence underestimation remains:



\\\[

\\boxed{

e\_i\\le-0.050.

}

\\]



This definition is frozen before prospective evaluation.



\---



\# Historical Calibration Memory



For candidate action \\(a\\) in context \\(x\\), the controller constructs a local calibration state from historically similar action-context observations.



Representative quantities include:



\\\[

\\bar e\_{\\mathcal N}(x,a),

\\]



the mean historical calibration error,



\\\[

P(e<0\\mid\\mathcal N),

\\]



the historical underestimation fraction,



and:



\\\[

P(e\\le-0.050\\mid\\mathcal N),

\\]



the severe-underestimation fraction.



The current evaluated outcome must never enter the representation used to make its own decision.



\---



\# Frozen Calibration-Risk Classifier



The classifier family remains the Experiment 100 logistic model:



\\\[

\\boxed{

\\text{standardized logistic regression}

}

\\]



with:



\- balanced class weighting,

\- \\(C=1.0\\),

\- `liblinear` solver,

\- fixed random state,

\- and the frozen five-feature primary representation.



The classifier is trained using historical development data only.



No Experiment 101 outcome may be used for classifier fitting.



\---



\# Why the 0.50 Threshold Is Not Used Automatically



Experiment 100 evaluated classification at probability threshold:



\\\[

0.50.

\\]



That threshold was useful for reporting conventional classifier metrics but was not selected as a controller intervention boundary.



At that threshold, historical calibration memory substantially increased specificity but reduced severe-underestimation recall.



Therefore Experiment 101 does not automatically interpret:



\\\[

p=0.50

\\]



as an appropriate safety-control operating point.



Instead, an operating threshold is selected from historical data according to the frozen procedure below.



\---



\# Frozen Threshold-Selection Procedure



The primary calibration-risk threshold will be selected \*\*before prospective seeds 44091–44110 are evaluated\*\*.



Threshold selection must use only historical development data.



The procedure is:



1\. Generate out-of-fold calibration-risk probabilities across historical seeds using leave-one-generation-seed-out validation.

2\. Evaluate candidate probability thresholds on those out-of-fold predictions.

3\. Retain only thresholds achieving at least:



\\\[

\\boxed{

80\\%

}

\\]



severe-underestimation recall.

4\. Among qualifying thresholds, select the threshold with the highest nonsevere specificity.

5\. If multiple thresholds tie on specificity, choose the threshold with higher severe-event precision.

6\. If still tied, choose the higher threshold.



This produces one primary intervention threshold:



\\\[

\\boxed{

\\tau\_{\\mathrm{cal}}

}

\\]



before prospective outcomes are observed.



Once selected, this threshold is frozen.



It may not be changed after Experiment 101 begins.



\---



\# Why 80% Recall Is Frozen



The calibration-risk model is being used as a safety-oriented intervention signal.



The threshold-selection procedure therefore prioritizes retaining substantial sensitivity to severe underestimation before optimizing specificity.



The fixed historical recall constraint is:



\\\[

\\boxed{

\\text{severe recall}\\ge80\\%.

}

\\]



This value is part of the Experiment 101 preregistration and may not be altered after prospective outcomes are observed.



\---



\# Existing Controller Baseline



The primary baseline remains the support-aware safe-action-expansion controller.



The frozen parameters remain:



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



The calibration-risk intervention is layered on top of this existing architecture.



\---



\# Narrow Intervention Scope



The calibration-aware veto applies only to actions newly admitted by the support-aware expansion mechanism.



It does not remove or override actions already admitted by the primary predicted-safe action set.



Therefore:



\\\[

\\boxed{

a\\in A\_{\\mathrm{primary}}

\\Rightarrow

\\text{calibration guard cannot veto }a.

}

\\]



The intervention operates only on:



\\\[

\\boxed{

A\_{\\mathrm{support}}

\\setminus

A\_{\\mathrm{primary}}.

}

\\]



This preserves the hierarchical architecture established by earlier experiments.



\---



\# Frozen Primary Intervention Rule



For a support-admitted candidate action \\(a\\), compute the frozen calibration-risk probability:



\\\[

p\_{\\mathrm{cal}}(x,a).

\\]



The action is vetoed if:



\\\[

\\boxed{

p\_{\\mathrm{cal}}(x,a)

\\ge

\\tau\_{\\mathrm{cal}}.

}

\\]



Thus the primary policy is:



\\\[

\\boxed{

\\text{support-aware expansion}

\+

\\text{historical calibration-risk veto}.

}

\\]



The guard does not change the original primary safe set.



\---



\# Primary Policies



Experiment 101 compares two policies.



\## Policy A — Support Baseline



The existing support-aware safe-action expansion controller.



\## Policy B — Frozen Calibration-Aware Guard



The same support-aware controller plus:



\\\[

\\boxed{

p\_{\\mathrm{cal}}(x,a)\\ge\\tau\_{\\mathrm{cal}}

\\Rightarrow

\\text{veto support-admitted action}.

}

\\]



No other controller parameter differs between the two policies.



\---



\# Primary Safety Outcomes



The primary safety outcomes are:



1\. harmful support-expansion count,

2\. mean realized regret,

3\. seed-level regret degradation frequency,

4\. seed-level harmful-expansion degradation frequency.



The primary safety objective is:



\\\[

\\boxed{

\\text{reduce harmful responsive expansion without increasing regret}.

}

\\]



\---



\# Secondary Responsiveness Outcomes



The following secondary outcomes will be reported:



\- beneficial support expansions preserved,

\- beneficial expansions vetoed,

\- total veto count,

\- under-persistence,

\- over-persistence,

\- responsive retention,

\- action entropy.



These quantify the responsiveness cost of calibration-aware intervention.



\---



\# Calibration-Specific Outcomes



Experiment 101 will also report:



\- severe-underestimation expansions observed under the support baseline,

\- severe-underestimation expansions vetoed by the calibration guard,

\- severe-underestimation veto recall,

\- calibration-risk probability distributions for beneficial and harmful support expansions,

\- and calibration-risk probability distributions for severe and nonsevere expansion events.



These are diagnostic outcomes.



They may not be used to redefine the frozen threshold.



\---



\# Primary Paired Comparison



For each prospective seed \\(s\\), define:



\\\[

\\Delta R\_s

=

R\_{\\mathrm{guard},s}

\-

R\_{\\mathrm{baseline},s}.

\\]



Similarly:



\\\[

\\Delta H\_s

=

H\_{\\mathrm{guard},s}

\-

H\_{\\mathrm{baseline},s},

\\]



where \\(H\\) is harmful support-expansion count.



The experiment will report:



\- mean \\(\\Delta R\\),

\- median \\(\\Delta R\\),

\- range of \\(\\Delta R\\),

\- regret improved / unchanged / degraded seed counts,

\- mean \\(\\Delta H\\),

\- harmful improved / unchanged / degraded seed counts.



\---



\# Primary Success Pattern



The strongest favorable result would satisfy:



\\\[

\\boxed{

\\Delta H<0

}

\\]



with:



\\\[

\\boxed{

\\Delta R\\le0

}

\\]



and no meaningful increase in under-persistence.



A weaker but still informative result would show severe-underestimation reduction at a measurable responsiveness cost.



\---



\# Failure Conditions



The Experiment 101 intervention will not be considered supported if any of the following dominates:



1\. harmful expansions increase;

2\. mean regret increases materially;

3\. multiple prospective seeds experience regret degradation;

4\. under-persistence increases substantially;

5\. beneficial responsive expansions are suppressed without meaningful safety gain;

6\. severe-underestimation veto recall collapses;

7\. the selected historical threshold proves highly regime-specific;

8\. information leakage is discovered;

9\. prospective outcomes influence threshold selection or model fitting;

10\. the calibration representation is altered after the prospective block begins.



A negative result must be retained.



\---



\# Event Sparsity Constraint



Earlier prospective controller experiments encountered blocks with very few harmful support-expansion events.



Experiment 101 must therefore report the absolute number of baseline harmful expansions.



If harmful events are extremely sparse, the result must not be described as conclusive even if every observed harmful event is vetoed.



The interpretation must distinguish:



\\\[

\\boxed{

\\text{successful directional intervention}

}

\\]



from:



\\\[

\\boxed{

\\text{high-powered prospective validation}.

}

\\]



\---



\# Representation Versus Operating Point



Experiment 100 validated ranking/discrimination.



Experiment 101 separately tests an intervention operating point.



These must not be conflated.



A good ROC AUC does not guarantee a good control threshold.



Similarly, failure of one frozen intervention threshold would not automatically falsify the underlying calibration-risk representation.



\---



\# Full-Information Simulation Limitation



The historical calibration representation currently uses simulated historical consequences for candidate actions.



The simulation therefore supplies richer feedback than a physical controller may directly observe.



Accordingly, Experiment 101 tests calibration-aware intervention within the current simulation/digital-twin information structure.



It does not yet establish direct deployability under executed-action-only physical feedback.



That observability constraint remains a separate future research question.



\---



\# No Secondary Threshold Replacement



Experiment 101 has one primary calibration-risk threshold:



\\\[

\\boxed{

\\tau\_{\\mathrm{cal}}.

}

\\]



It is determined by the frozen historical threshold-selection procedure before prospective evaluation.



No alternative threshold may replace the primary threshold after prospective outcomes are observed.



Exploratory sensitivity analysis, if performed later, must be explicitly labeled secondary and cannot redefine the primary Experiment 101 result.



\---



\# Frozen Experimental Boundary



Before observing seeds:



\\\[

44091\\text{–}44110,

\\]



the following are frozen:



\- development seeds: `44001–44090`

\- prospective seeds: `44091–44110`

\- local neighborhood size: `7`

\- severe-underestimation threshold: `-0.050`

\- calibration representation: `loss\_plus\_local\_calibration`

\- classifier family and hyperparameters

\- historical threshold-selection procedure

\- severe-recall threshold-selection constraint: `>= 80%`

\- support safety threshold: `0.60`

\- support downside threshold: `0.020`

\- context-support threshold: `2.50`

\- narrow support-expansion-only veto scope

\- baseline controller

\- primary comparison

\- outcome metrics

\- interpretation constraints



No prospective outcome may be observed before these elements are implemented and frozen.



\---



\# Scientific Transition



The experimental chain is now:



\\\[

\\boxed{

099:

\\text{retrospective calibration-memory discovery}

}

\\]



\\\[

\\Downarrow

\\]



\\\[

\\boxed{

100:

\\text{frozen prospective representation validation}

}

\\]



\\\[

\\Downarrow

\\]



\\\[

\\boxed{

101:

\\text{frozen prospective calibration-aware intervention}.

}

\\]



Experiment 101 asks whether a digital twin can move beyond recognizing its own predictive unreliability and begin using that self-knowledge to make safer adaptive decisions.



The central question is:



\\\[

\\boxed{

\\text{Does historical knowledge of where the twin's consequence}

\\atop

\\text{model has been unreliable improve the decision of when}

\\atop

\\text{responsive adaptation should be trusted?}

}

\\]

---

# Frozen Historical Threshold Selection Result

The preregistered historical threshold-selection procedure was executed before any Experiment 101 prospective seed was evaluated.

Historical seeds:

\[
44001\text{–}44090.
\]

Historical out-of-fold population:

\[
22{,}275
\]

action-context observations.

Severe-underestimation events:

\[
1{,}966.
\]

Nonsevere events:

\[
20{,}309.
\]

Historical out-of-fold ROC AUC:

\[
0.758.
\]

The threshold sweep evaluated:

\[
22{,}275
\]

distinct out-of-fold probability boundaries.

The preregistered minimum severe-recall constraint was:

\[
\ge 80\%.
\]

The selected primary calibration-risk intervention threshold is:

\[
\boxed{
\tau_{\mathrm{cal}}
=
0.468010308717.
}
\]

Historical out-of-fold performance at this frozen threshold:

- severe-underestimation recall: `80.010%`
- nonsevere specificity: `57.905%`
- severe precision: `15.540%`
- balanced accuracy: `68.958%`
- flagged fraction: `45.441%`

Confusion counts:

- TP = `1573`
- FP = `8549`
- FN = `393`
- TN = `11760`

This threshold was selected exclusively from historical out-of-fold predictions according to the preregistered procedure.

No seed from:

\[
44091\text{–}44110
\]

was evaluated before this value was frozen.

Therefore:

\[
\boxed{
\tau_{\mathrm{cal}}
=
0.468010308717
}
\]

is the immutable primary Experiment 101 controller-intervention threshold.

---

## Prospective Results

Experiment 101 was executed on the frozen prospective seed block:

44091-44110

using the preregistered calibration-risk threshold:

tau_cal = 0.468010308717

The threshold was selected exclusively from leave-one-generation-seed-out historical predictions on seeds 44001-44090 before any Experiment 101 prospective outcome was evaluated.

### Prospective Policy Summary

Support baseline:

- mean regret: 0.017001
- mean under-persistence: 11.25
- mean over-persistence: 27.60
- mean harmful-expansion metric: 1.421
- responsive retention: 78.386%
- mean beneficial expansions: 2.15
- mean harmful expansions: 0.30

Calibration-aware guard:

- mean regret: 0.016694
- mean under-persistence: 11.00
- mean over-persistence: 28.10
- mean harmful-expansion metric: 1.407
- responsive retention: 77.636%
- mean beneficial expansions: 1.30
- mean harmful expansions: 0.05
- mean vetoes: 1.10

Across the prospective block, the calibration-aware guard vetoed:

- 5 harmful expansions
- 17 beneficial expansions

Severe-underestimation veto recall was:

80.000%

---

## Primary Preregistered Comparison

Relative to the support baseline, the frozen calibration-aware guard produced:

- mean change in harmful expansions: -0.250
- harmful improved / unchanged / degraded seeds: 5 / 15 / 0
- mean change in regret: -0.000306
- median change in regret: +0.000000
- regret range: [-0.001565, +0.000000]
- regret improved / unchanged / degraded seeds: 5 / 15 / 0
- mean change in under-persistence: -0.250
- mean change in beneficial expansions: -0.850
- mean change in responsive retention: -0.750%

The intervention therefore reduced harmful adaptive expansions on five prospective seeds while producing no seed-level degradation in harmful-expansion count.

The same five-versus-fifteen-versus-zero pattern was observed for regret improvement, with no prospective seed exhibiting increased regret relative to the support baseline.

---

## Interpretation

The primary Experiment 101 result supports the preregistered hypothesis that historically learned local calibration-risk information can improve prospective adaptive-controller decisions.

The intervention was frozen before the prospective seed block was evaluated. Its calibration-risk model was trained from historical seeds 44001-44090, and its decision threshold was selected from leave-one-generation-seed-out historical predictions before seeds 44091-44110 were exposed.

The prospective result therefore extends the Experiment 099-100 sequence:

1. Experiment 099 identified historical local calibration structure associated with severe consequence underestimation.
2. Experiment 100 demonstrated that the frozen representation generalized prospectively to unseen action-context outcomes.
3. Experiment 101 demonstrates that the resulting frozen calibration-risk signal can be used prospectively as a controller intervention and can reduce harmful adaptive expansions and regret.

The result is not cost-free.

The calibration-aware guard reduced mean beneficial expansions from 2.15 to 1.30 and reduced responsive retention by 0.750 percentage points. It also increased mean over-persistence from 27.60 to 28.10.

Thus, the experiment does not establish perfect discrimination between beneficial and harmful adaptation. Instead, it identifies a measurable safety-responsiveness tradeoff: historical calibration-risk information substantially reduced harmful expansion while suppressing some beneficial adaptation.

---

## Primary Conclusion

Experiment 101 provides prospective intervention evidence that a digital twin can use historical information about its own local predictive reliability to improve adaptive control decisions.

Under the frozen experimental conditions, the calibration-aware controller:

- reduced mean harmful expansions from 0.30 to 0.05 per seed,
- vetoed 5 harmful prospective expansions,
- achieved 80.000% severe-underestimation veto recall,
- reduced mean regret from 0.017001 to 0.016694,
- improved harmful-expansion and regret outcomes on 5 of 20 seeds,
- degraded neither metric on any prospective seed,
- and incurred a measurable reduction in beneficial adaptation and responsive retention.

These findings support historical calibration state as a prospective control-relevant representation rather than merely a retrospective correlate of model failure.

---

## Scientific Limitations

Experiment 101 establishes prospective evidence only within the present simulation and controller architecture.

It does not establish:

- universal generalization beyond the simulated system,
- causal identification of calibration failure as the sole mechanism of harmful adaptation,
- optimality of the selected calibration-risk threshold,
- perfect separation of beneficial and harmful expansions,
- or deployability under partial-feedback conditions in which counterfactual action consequences are unavailable.

In particular, the historical calibration representation currently depends on consequence information available within the experimental simulation framework. Establishing whether comparable calibration memory can be constructed from executed-action feedback alone remains a separate research question.

---

## Experiment 101 Status

**Primary prospective intervention result: supported.**

The frozen calibration-aware intervention reduced harmful adaptive expansion and regret on the untouched prospective seed block without degradation on either metric at the seed level, while introducing a measurable responsiveness cost.

No post hoc threshold alteration is used to replace the preregistered primary result.