\# Experiment 118 — Broader Controller-State Action-Harm Decomposition



\## Objective



Determine whether the cross-population association between support-expansion action identity and harmful expansion observed in Experiments 115–117 can be explained by a substantially broader representation of the controller state available before outcome realization.



Experiment 117 showed that action identity retained harmful-expansion information after adjustment for a frozen five-variable support/loss geometry. That representation, however, did not include several controller-state quantities involved in the decision process.



Experiment 118 therefore tests the stronger alternative explanation:



> The apparent action-harm association is a proxy for a broader pre-action controller state that jointly determines both action selection and harmful-expansion risk.



The central falsification question is whether action identity continues to improve cross-population harm discrimination after adjustment for this broader controller state.



No controller intervention, operating threshold, action-specific veto, or prospective policy is introduced.



\---



\## Populations



Two non-overlapping historical populations are used.



\### Early population



Seeds corresponding to the previously established `population\_001\_010` historical expansion population.



Observed expansion events:



\- 65 total events

\- action 1: 19 events

\- action 2: 46 events



The previously established harmful-expansion counts are:



\- action 1: 7 harmful

\- action 2: 8 harmful



\### Later population



Seeds:



\- 44071–44110



Observed expansion events:



\- 88 total events

\- action 1: 33 events

\- action 2: 55 events



The previously established harmful-expansion counts are:



\- action 1: 8 harmful

\- action 2: 0 harmful



\### Combined population



\- 153 expansion events

\- 23 harmful events



The populations are non-overlapping and are evaluated using reciprocal population-held-out transfer.



\---



\## Broader Pre-Action State Representation



The broader state representation was frozen before observing Experiment 118 harm-model performance.



The eleven features are:



1\. `context\_benefit\_probability`

2\. `context\_release\_probability`

3\. `context\_anchor\_age`

4\. `context\_trigger\_score`

5\. `context\_feature\_distance`

6\. `context\_current\_mismatch\_indicator`

7\. `context\_current\_parameter\_estimate`

8\. `predicted\_under\_risk`

9\. `predicted\_primary\_regret`

10\. `predicted\_expanded\_regret`

11\. `predicted\_regret\_margin`



These variables represent controller probabilities, persistence/context state, mismatch and parameter state, predicted under-risk, and predicted regret quantities available before realization of the expansion outcome.



The broader representation explicitly excludes:



\- realized regret,

\- realized loss,

\- harmful/beneficial outcome label,

\- realized incremental regret,

\- true-best action,

\- and other post-outcome quantities.



\---



\## Later-Population State Reconstruction



The required broader controller-state representation did not initially exist for the complete 44071–44110 population.



Rather than partially joining historical files or redefining the state representation, the established implementation from:



`cross\_seed\_harmful\_expansion\_feature\_decomposition.py`



was reused with only:



\- the generation-seed population changed to 44071–44110, and

\- output destinations redirected to new `\_071\_110` result files.



The reconstruction generated:



\- 88 total action-change events,

\- 72 beneficial events,

\- 8 harmful events,

\- 8 neutral events.



No Experiment 118 harm model was fit during reconstruction.



Experiment 118 then discovered the reconstructed event source and obtained complete later-population coverage:



\- matched events: 88/88.



This reconstruction preserves the established upstream feature-generation implementation rather than introducing a second implementation of the controller-state mathematics.



\---



\## Experimental Design



Three harm models are evaluated:



\### 1. Action only



Uses only support-expansion action identity.



\### 2. Broader state only



Uses the frozen eleven-variable pre-action controller-state representation.



\### 3. Broader state plus action



Uses the same eleven-variable state representation together with action identity.



Evaluation is reciprocal and population-held-out:



\- train on the early population and test on the later population,

\- train on the later population and test on the early population.



The principal endpoint is ROC AUC.



The primary comparison is:



`broader\_state\_plus\_action` versus `broader\_state\_only`.



If action identity merely proxies for the broader observable controller state, adding action should provide little or no held-out discrimination improvement.



\---



\## Can Broader Pre-Action State Predict Action Identity?



Reciprocal population-held-out action prediction produced:



| Held-out population | AUC |

|---|---:|

| population\_001\_010 | 0.424 |

| population\_071\_110 | 0.531 |



Mean action-prediction AUC:



\*\*0.478\*\*



Minimum action-prediction AUC:



\*\*0.424\*\*



Therefore, the frozen broader state does not transfer as a useful predictor of action identity across the two populations.



This argues against a simple explanation in which the broader state representation merely reconstructs which action the controller selected.



\---



\## Reciprocal Population-Held-Out Harm Prediction



| Model | Mean AUC | Minimum AUC | Maximum AUC |

|---|---:|---:|---:|

| broader state + action | \*\*0.845\*\* | \*\*0.789\*\* | \*\*0.900\*\* |

| broader state only | 0.736 | 0.605 | 0.867 |

| action only | 0.729 | 0.613 | 0.844 |



The combined broader-state-plus-action model provides the strongest transferred harm discrimination.



Relative to broader state alone:



\- mean AUC improvement: \*\*+0.108\*\*

\- minimum AUC improvement: \*\*+0.184\*\*



The improvement in minimum AUC is particularly important because it indicates that the combined representation improves the weaker of the two population-transfer directions rather than obtaining its advantage solely from one favorable population.



\---



\## Adjusted Action Effect



Within the broader-state-plus-action model, the mean action-2 coefficient is:



\*\*-1.069\*\*



Coefficient sign stability across reciprocal population fits:



\*\*100.000%\*\*



Thus, after adjustment for the broader pre-action controller state, action 2 remains associated with lower harmful-expansion risk relative to action 1 in both population-transfer fits.



The direction is consistent with the action-harm structure observed independently in Experiments 115–117.



\---



\## Broader-State Coefficient Stability



Several broader-state variables exhibit stable coefficient direction across both population fits.



\### 100% sign stability



\- `context\_anchor\_age`

\- `context\_benefit\_probability`

\- `context\_current\_mismatch\_indicator`

\- `context\_current\_parameter\_estimate`

\- `context\_feature\_distance`

\- `context\_trigger\_score`

\- `predicted\_expanded\_regret`

\- `predicted\_primary\_regret`

\- `predicted\_regret\_margin`



Within the combined broader-state-plus-action model, all eleven state variables and the action indicator exhibit 100% sign stability.



The state-only model shows weaker directional stability for:



\- `context\_release\_probability`

\- `predicted\_under\_risk`



which each exhibit 50% sign stability.



These results suggest that the broader controller state contains genuine transferable harm information, while also indicating that not every constituent is individually stable when action identity is omitted.



\---



\## Interpretation



Experiment 118 substantially strengthens the structural interpretation developed in Experiments 115–117.



First, the broader pre-action controller state itself contains meaningful cross-population harmful-expansion information:



\- mean AUC = 0.736.



This is materially stronger than the five-variable geometry-only representation evaluated in Experiment 117.



Therefore, harmful expansion is not adequately described as an action-only phenomenon.



Second, action identity remains informative after adjustment for this substantially richer state representation.



The combined model achieves:



\- mean AUC = 0.845,

\- minimum AUC = 0.789,



and improves over broader state alone by:



\- +0.108 mean AUC,

\- +0.184 minimum AUC.



Third, the adjusted action-2 coefficient remains negative with 100% sign stability.



Therefore, the observed action association is not eliminated by adjustment for the broader observable pre-action controller state tested here.



The evidence supports the provisional structural interpretation:



> Harmful support expansion is jointly structured by broader pre-action controller state and action identity.



The result does \*\*not\*\* establish that action identity is causal.



Unmeasured state variables, controller-selection mechanisms, interaction structure, and finite-sample effects remain possible explanations for the residual action association.



\---



\## Falsification Outcome



The principal alternative hypothesis tested by Experiment 118 was:



> The action-harm association disappears once sufficiently broad observable pre-action controller state is included.



That hypothesis is not supported by the present results.



Action identity adds substantial reciprocal population-held-out discrimination after broader-state adjustment, and its coefficient direction remains stable across both population fits.



At the same time, the experiment falsifies an overly simple action-only interpretation because broader state independently carries substantial harm information.



The surviving model is therefore neither:



`harm = action alone`



nor:



`harm = observable controller state alone`



but instead is consistent with:



`harm = f(controller state, action, residual interaction/latent structure)`



subject to further falsification.



\---



\## Limitations



The combined dataset contains only 23 harmful expansion events across 153 total expansion events.



The later population contains only eight harmful events, all associated with action 1.



Consequently:



\- coefficient magnitudes should not be interpreted as stable causal effect sizes,

\- ROC AUC estimates remain subject to finite-sample uncertainty,

\- the exact absence of harmful action-2 events in the later population should not be treated as universal,

\- and no action-specific intervention should yet be inferred from these results.



Experiment 116 already showed that action 2 can produce harmful expansions in an independent historical population.



The evidence therefore supports a relative action-risk association rather than an absolute safe/unsafe action classification.



\---



\## Conclusion



Experiment 118 shows that a substantially broader observable pre-action controller-state representation improves cross-population harmful-expansion prediction, but does not explain away the previously observed action association.



The strongest reciprocal population-held-out model combines broader controller state with action identity:



\*\*mean AUC = 0.845\*\*



\*\*minimum AUC = 0.789\*\*



Action identity contributes:



\*\*+0.108 mean AUC\*\*



and:



\*\*+0.184 minimum AUC\*\*



beyond broader state alone.



The adjusted action-2 coefficient remains negative with:



\*\*100% sign stability.\*\*



The evidence therefore supports continued investigation of a joint controller-state/action mechanism while remaining insufficient for causal or prospective intervention claims.



A subsequent experiment should test whether the combined signal survives stricter feature reduction and stability analysis before any prospective controller modification is considered.

