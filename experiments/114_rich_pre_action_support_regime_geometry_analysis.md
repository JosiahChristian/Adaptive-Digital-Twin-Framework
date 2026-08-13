\# Experiment 114 — Rich Pre-Action Support Regime Geometry Analysis



\## Objective



Determine whether a richer, explicitly pre-action support/action representation can identify the historical operating-regime shift observed between support-expansion blocks `071–090` and `091–110`, and whether such a regime representation improves the transferability of the previously frozen severe-underestimation proxy for predicting harmful support expansion.



This experiment follows Experiment 113, in which a compact pre-action regime representation based on `local\_error\_std` and `severe\_underestimation\_probability` failed to provide a useful transferable regime modifier.



Experiment 114 therefore tests whether the failure of Experiment 113 resulted from an insufficiently expressive representation of the system's pre-action support geometry.



\---



\## Hypothesis



A richer pre-action representation of support geometry and predicted action consequence may contain sufficient information to distinguish the two historical operating blocks and thereby explain or improve the block-dependent relationship between the frozen severe-underestimation proxy and harmful support expansion.



The primary regime representation is frozen before observing Experiment 114 performance as:



\\\[

z =

\[

d\_{\\mathrm{context}},

d\_{\\mathrm{action}},

d\_{\\mathrm{action}}-d\_{\\mathrm{context}},

L\_{\\mathrm{pred}},

L\_{\\mathrm{relative}}

]

\\]



corresponding to:



\- `context\_support\_distance`

\- `action\_support\_distance`

\- `action\_support\_minus\_context`

\- `predicted\_action\_loss`

\- `predicted\_relative\_loss`



Action identity is excluded from the primary continuous regime representation and retained only as a secondary structural diagnostic.



\---



\## Temporal-Admissibility Constraint



All primary regime variables must be available before realization of the support-expansion outcome.



The established action-conditioned support implementation was inspected before Experiment 114 was run.



The source constructs the context support representation and action-conditioned support distances from the current test row, previously constructed support representations, predicted risk, and predicted action losses.



`predicted\_action\_loss` is obtained from the model-generated test loss prediction for the candidate action.



`predicted\_relative\_loss` is computed relative to the minimum predicted loss across candidate actions.



Realized action regret is calculated and recorded separately as an outcome variable.



Therefore the following outcome-derived quantities are explicitly excluded from regime construction:



\- realized action regret

\- realized action loss

\- action-loss prediction error

\- harmful/beneficial class

\- true-best action

\- true-responsive action

\- severe-underestimation outcome

\- any other post-action or realized consequence field



No outcome variable is permitted to enter the five-variable regime representation.



\---



\## Data-Provenance Check



The initial Experiment 114 execution searched existing result files for a historical action-conditioned representation containing the complete five-variable feature set.



The only initially available matching file was:



`results/action\_conditioned\_support\_representation\_analysis\_actions.csv`



That artifact contained:



\- 2,316 action-context rows

\- 10 generation seeds

\- seed range `44001–44010`



The Experiment 114 target support-expansion population instead consisted of the later historical blocks covering seeds `44071–44110`.



Consequently, the initial join produced:



\- target support events: 88

\- matched events: 0

\- coverage: 0/88



Experiment 114 terminated automatically rather than allowing a partial or mismatched join.



No regime-performance result was produced from the failed join.



\---



\## Historical Representation Reconstruction



To preserve the preregistered five-variable feature boundary, the representation was not weakened or altered after the provenance failure.



Instead, the established action-conditioned support representation implementation was reused unchanged for the required historical seed population.



A dedicated reconstruction wrapper:



`experiments/reconstruct\_rich\_pre\_action\_support\_geometry\_071\_110.py`



changed only:



1\. `ANALYSIS\_SEEDS`, from the original seed set to `44071–44110`; and

2\. output destinations, so the original historical Experiment 092 artifacts remained untouched.



The established action-conditioned support representation implementation generated:



`results/action\_conditioned\_support\_representation\_analysis\_071\_110.csv`



`results/action\_conditioned\_support\_representation\_analysis\_folds\_071\_110.csv`



`results/action\_conditioned\_support\_representation\_analysis\_actions\_071\_110.csv`



`results/action\_conditioned\_support\_representation\_analysis\_coefficients\_071\_110.csv`



No Experiment 114 regime classifier or harmful-outcome classifier was fit during reconstruction.



\---



\## Reconstruction Diagnostics



The reconstructed historical population contained:



\- generation seeds: 40

\- seed range: `44071–44110`

\- contexts: 2,627

\- action-context pairs: 7,881



All 2,627 contexts showed nonzero action-conditioned support-distance separation.



Mean maximum pairwise action-distance difference:



\\\[

0.315785

\\]



Maximum pairwise action-distance difference:



\\\[

3.170752

\\]



Under the previously established retrospective unsafe-action regret criterion:



\- safe action-context pairs: 6,241

\- unsafe action-context pairs: 1,640

\- unsafe fraction: 20.810%



These quantities are reconstruction diagnostics inherited from the established action-conditioned support analysis and are not themselves Experiment 114 regime-validation results.



\---



\## Final Provenance Verification



After reconstruction, Experiment 114 was rerun without changing the preregistered five-variable representation.



Source discovery found:



`results/action\_conditioned\_support\_representation\_analysis\_actions\_071\_110.csv`



with:



\\\[

88/88

\\]



matching support-expansion events.



The earlier historical source remained at:



\\\[

0/88

\\]



coverage.



The reconstructed source was therefore selected automatically.



Final joined Experiment 114 population:



\- total events: 88

\- block `071–090`: 39

\- block `091–110`: 49

\- beneficial support expansions: 80

\- harmful support expansions: 8



\---



\## Univariate Rich Pre-Action Regime Geometry



\### Context Support Distance



Block `071–090` mean:



\\\[

1.425242

\\]



Block `091–110` mean:



\\\[

1.609900

\\]



Difference:



\\\[

+0.184658

\\]



Best-orientation block AUC:



\\\[

0.703

\\]



\### Action Support Distance



Block `071–090` mean:



\\\[

1.827988

\\]



Block `091–110` mean:



\\\[

2.058932

\\]



Difference:



\\\[

+0.230944

\\]



Best-orientation block AUC:



\\\[

0.711

\\]



\### Action Support Minus Context



Block `071–090` mean:



\\\[

0.402746

\\]



Block `091–110` mean:



\\\[

0.449033

\\]



Difference:



\\\[

+0.046287

\\]



Best-orientation block AUC:



\\\[

0.590

\\]



\### Predicted Action Loss



Block `071–090` mean:



\\\[

0.171610

\\]



Block `091–110` mean:



\\\[

0.155121

\\]



Difference:



\\\[

\-0.016489

\\]



Best-orientation block AUC:



\\\[

0.564

\\]



\### Predicted Relative Loss



Block `071–090` mean:



\\\[

0.000176

\\]



Block `091–110` mean:



\\\[

0.000661

\\]



Difference:



\\\[

+0.000485

\\]



Best-orientation block AUC:



\\\[

0.546

\\]



The strongest individual regime separation occurs in the two support-distance quantities, but neither provides sufficiently strong discrimination by itself to establish a reliable operating-regime indicator.



\---



\## Leave-One-Seed-Out Rich Regime Identification



The frozen five-variable representation was evaluated using leave-one-seed-out prediction of historical block identity.



Pooled leave-one-seed-out regime AUC:



\\\[

\\boxed{0.575}

\\]



Pooled classification accuracy:



\\\[

57.955\\%

\\]



Mean seed accuracy:



\\\[

58.006\\%

\\]



This result does not support the hypothesis that the five-variable continuous representation reliably identifies the historical operating regime out of seed.



\---



\## Regime-Coefficient Stability



\### `context\_support\_distance`



Mean coefficient:



\\\[

+0.479

\\]



Mean absolute coefficient:



\\\[

0.479

\\]



Sign stability:



\\\[

100\\%

\\]



\### `action\_support\_distance`



Mean coefficient:



\\\[

+0.458

\\]



Mean absolute coefficient:



\\\[

0.458

\\]



Sign stability:



\\\[

100\\%

\\]



\### `action\_support\_minus\_context`



Mean coefficient:



\\\[

+0.052

\\]



Mean absolute coefficient:



\\\[

0.069

\\]



Sign stability:



\\\[

91.667\\%

\\]



\### `predicted\_action\_loss`



Mean coefficient:



\\\[

\-0.410

\\]



Mean absolute coefficient:



\\\[

0.434

\\]



Sign stability:



\\\[

95.833\\%

\\]



\### `predicted\_relative\_loss`



Mean coefficient:



\\\[

+0.324

\\]



Mean absolute coefficient:



\\\[

0.324

\\]



Sign stability:



\\\[

100\\%

\\]



Several coefficient directions are highly stable despite weak aggregate regime discrimination.



This indicates reproducible directional differences between the blocks but does not establish sufficient predictive separation for reliable regime identification.



\---



\## Frozen Severe-Proxy Harm Benchmark



The previously frozen severe-underestimation proxy remains the reference model.



Reciprocal block-held-out performance:



\\\[

\\text{mean AUC}=0.821

\\]



\\\[

\\text{minimum AUC}=0.764

\\]



\\\[

\\text{maximum AUC}=0.878

\\]



This benchmark is not refit using Experiment 114's regime results.



\---



\## Rich-Regime Harm Modulation



\### Rich Regime Only



\\\[

\\text{mean AUC}=0.244

\\]



\\\[

\\text{minimum AUC}=0.000

\\]



\\\[

\\text{maximum AUC}=0.488

\\]



The learned regime score alone does not provide transferable harmful-support-expansion discrimination.



\### Severe Proxy + Rich Regime



\\\[

\\text{mean AUC}=0.583

\\]



\\\[

\\text{minimum AUC}=0.527

\\]



\\\[

\\text{maximum AUC}=0.640

\\]



\### Severe Proxy × Rich-Regime Interaction



\\\[

\\text{mean AUC}=0.583

\\]



\\\[

\\text{minimum AUC}=0.527

\\]



\\\[

\\text{maximum AUC}=0.640

\\]



Relative to the frozen severe-proxy benchmark:



\\\[

\\Delta\\text{mean AUC}

=

0.583-0.821

=

\\boxed{-0.238}

\\]



and:



\\\[

\\Delta\\text{minimum AUC}

=

0.527-0.764

=

\\boxed{-0.237}

\\]



Thus, the richer continuous regime representation substantially degrades rather than improves block-held-out harm discrimination.



\---



\## Primary Result



Experiment 114 does \*\*not\*\* support the hypothesis that the frozen five-variable continuous pre-action support/action geometry provides a useful transferable operating-regime representation.



The block-identification result:



\\\[

\\boxed{\\mathrm{AUC}=0.575}

\\]



is insufficient to establish reliable regime identification.



More decisively, conditioning the frozen severe-underestimation proxy on this learned regime representation reduces mean reciprocal block-held-out AUC by:



\\\[

\\boxed{0.238}

\\]



and minimum AUC by:



\\\[

\\boxed{0.237}.

\\]



The continuous rich-regime hypothesis is therefore rejected for the present historical evidence.



\---



\## Secondary Structural Diagnostic: Action Composition



Action identity was intentionally excluded from the primary continuous regime classifier and examined only as a predefined secondary structural diagnostic.



A substantial block-dependent action-composition shift was observed.



\### Block `071–090`



Action 1:



\\\[

24/39 = 61.538\\%

\\]



Action 2:



\\\[

15/39 = 38.462\\%

\\]



\### Block `091–110`



Action 1:



\\\[

9/49 = 18.367\\%

\\]



Action 2:



\\\[

40/49 = 81.633\\%

\\]



Thus the dominant support-baseline action reverses between the two historical blocks.



Block `071–090` is primarily action 1, whereas block `091–110` is primarily action 2.



This action-composition difference is substantially larger than the discrimination obtained from the continuous five-variable regime representation.



\---



\## Interpretation of the Action-Composition Finding



The action-composition result does not establish that action identity predicts harmful support expansion.



It does not establish an action-conditioned safety threshold.



It does not establish that the previously observed block-dependent operating-point instability is caused by action identity.



However, it provides a concrete new structural hypothesis:



\\\[

\\boxed{

\\text{the severe-proxy-to-harm relationship may be action-conditioned}

}

\\]



If harmful-support-expansion geometry differs between candidate support actions, then a changing mixture of those actions across historical blocks could contribute to apparent instability in a pooled scalar operating point.



This hypothesis must be tested independently rather than retroactively incorporated into Experiment 114.



\---



\## Falsification Outcome



Experiment 114 provides a useful negative result.



The following explanation is not supported:



> A richer continuous representation of pre-action support distance and predicted loss is sufficient to identify the historical regime and stabilize the severe-proxy-to-harm relationship.



The evidence instead indicates:



1\. support-distance quantities show moderate block separation individually;

2\. their combined out-of-seed block identification remains weak;

3\. the resulting regime score strongly degrades reciprocal harm discrimination when added to the frozen severe proxy; and

4\. a large action-composition shift exists between the historical blocks and remains an independently testable structural hypothesis.



\---



\## Scientific Boundary



Experiment 114 introduces:



\- no controller modification;

\- no intervention threshold;

\- no prospective seed;

\- no safety authorization;

\- no deployable regime detector;

\- no action-conditioned decision rule.



The experiment remains a historical diagnostic and falsification analysis.



Only eight harmful support-expansion events are present in the 88-event joined population, so even future positive action-conditioned results must be interpreted conservatively and subjected to additional validation.



\---



\## Conclusion



Experiment 114 rejects the richer continuous pre-action regime-conditioning hypothesis.



The five-variable support/action representation produces only:



\\\[

\\boxed{\\mathrm{LOSO\\ regime\\ AUC}=0.575}

\\]



and its interaction with the frozen severe-underestimation proxy reduces reciprocal block-held-out harm performance from:



\\\[

\\boxed{0.821}

\\]



mean AUC to:



\\\[

\\boxed{0.583}.

\\]



At the same time, the experiment identifies a strong secondary structural difference in support-action composition:



\\\[

61.538\\%\\rightarrow18.367\\%

\\]



for action 1 and:



\\\[

38.462\\%\\rightarrow81.633\\%

\\]



for action 2 across the two blocks.



This finding motivates, but does not answer, the next research question:



> Is the pre-action severe-underestimation-risk-to-harm relationship intrinsically action-conditioned, such that pooled operating-point instability partly reflects changes in action composition rather than a globally changing scalar risk boundary?



That question is reserved for a separate experiment.

