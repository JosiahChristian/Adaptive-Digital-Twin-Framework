\# Experiment 110 — Pre-Action Impending Calibration-Error Prediction



\## Purpose



Experiment 109 identified a critical mechanistic result.



Among support-expansion events, realized baseline action loss error provided extremely strong retrospective discrimination between harmful and beneficial outcomes.



The best retrospective contextual model achieved:



\\\[

\\text{mean reciprocal AUC}=0.994

\\]



with:



\\\[

\\text{minimum reciprocal AUC}=0.988.

\\]



However, realized action loss error is available only after the action consequence occurs.



It therefore cannot be used directly by a pre-action controller.



Experiment 110 addresses the resulting representation problem:



\*\*Can information available before the current action outcome predict impending calibration error strongly enough to provide a valid pre-action proxy for the retrospective explanatory variable identified in Experiment 109?\*\*



This experiment is a historical representation-analysis experiment.



It does not:



\- introduce a new prospective seed block;

\- modify the controller;

\- define a new intervention threshold;

\- or use the current evaluated calibration error as an input feature.



\---



\# Historical Population



Historical seeds:



44001-44110



All of these seeds had already been consumed by previous experiments before Experiment 110.



No new prospective block is introduced.



The reconstructed historical action-context population contains:



\\\[

\\boxed{25,878}

\\]



rows.



Underestimation events:



\\\[

4,642

\\]



or:



\\\[

17.938\\%.

\\]



Severe-underestimation events:



\\\[

2,363

\\]



or:



\\\[

9.131\\%.

\\]



The severe-underestimation threshold remains fixed at:



\\\[

\\boxed{-0.050}.

\\]



\---



\# Temporal Validity Boundary



All predictors in Experiment 110 are available before the evaluated action outcome.



The current action's:



`calibration\_error`



is used only as the retrospective target.



It is never included in the predictor representation used for that same event.



Therefore:



\\\[

\\boxed{

\\text{current outcome information does not enter the predictor.}

}

\\]



This temporal constraint is central to the experiment.



\---



\# Pre-Action Historical Representation



The expanded historical representation contains:



\- `predicted\_action\_loss`

\- `local\_mean\_error`

\- `local\_median\_error`

\- `local\_error\_std`

\- `local\_underestimate\_fraction`

\- `local\_severe\_underestimate\_fraction`

\- `local\_neighbor\_distance`

\- `local\_min\_error`



These quantities summarize current predicted action loss together with historical calibration behavior in the local action-context neighborhood.



\---



\# Prediction Tasks



Experiment 110 evaluates three related targets.



\## Task 1 — Any Underestimation



Target:



\\\[

\\texttt{calibration\\\_error}<0.

\\]



This asks whether the consequence model is about to underestimate the current action consequence at all.



\---



\## Task 2 — Severe Underestimation



Target:



\\\[

\\texttt{calibration\\\_error}\\le -0.050.

\\]



This preserves the previously established severe-underestimation definition.



\---



\## Task 3 — Signed Calibration Error



Target:



\\\[

\\texttt{calibration\\\_error}

\\]



as a continuous quantity.



This asks whether pre-action historical state can estimate the direction and magnitude of the impending calibration error itself.



\---



\# Validation Design



All models are evaluated using:



\\\[

\\boxed{

\\text{leave-one-generation-seed-out validation}

}

\\]



across seeds:



44001-44110.



For each fold:



1\. one generation seed is completely held out;

2\. the model is fitted using the remaining historical seeds;

3\. predictions are produced only for the held-out seed;

4\. the procedure is repeated for all 110 seeds.



This prevents each seed from being evaluated by a model trained on its own action-context outcomes.



\---



\# Any-Underestimation Classification



The strongest model is:



\\\[

\\boxed{

\\texttt{expanded\\\_historical\\\_state}

}

\\]



with:



\\\[

\\boxed{

\\text{balanced accuracy}=70.697\\%

}

\\]



\\\[

\\boxed{

\\text{recall}=76.928\\%

}

\\]



\\\[

\\boxed{

\\text{specificity}=64.466\\%

}

\\]



\\\[

\\boxed{

\\text{ROC AUC}=0.771

}

\\]



and mean fold AUC:



\\\[

\\boxed{

0.753.

}

\\]



This outperforms the five-feature historical calibration state:



\\\[

\\text{AUC}=0.747

\\]



and substantially outperforms predicted action loss alone:



\\\[

\\text{AUC}=0.649.

\\]



Thus the expanded historical representation contains meaningful information about whether the current consequence prediction is about to be underestimated.



\---



\# Severe-Underestimation Classification



The strongest severe-underestimation model is again:



\\\[

\\boxed{

\\texttt{expanded\\\_historical\\\_state}.

}

\\]



Its performance is:



\\\[

\\boxed{

\\text{balanced accuracy}=70.481\\%

}

\\]



\\\[

\\boxed{

\\text{severe recall}=77.359\\%

}

\\]



\\\[

\\boxed{

\\text{specificity}=63.602\\%

}

\\]



\\\[

\\boxed{

\\text{ROC AUC}=0.769

}

\\]



with mean leave-one-seed-out AUC:



\\\[

\\boxed{

0.748.

}

\\]



Predicted action loss alone achieves only:



\\\[

\\text{AUC}=0.610.

\\]



Therefore the broader historical state provides substantial incremental information about impending severe consequence underestimation.



\---



\# Comparison With Simpler Historical Features



\## Historical Mean Error Only



Severe-underestimation AUC:



\\\[

0.740

\\]



This confirms that local historical calibration bias remains a major component of impending underestimation risk.



\---



\## Ordinary Underestimation Fraction Only



Severe-underestimation AUC:



\\\[

0.709.

\\]



This provides useful but weaker discrimination.



\---



\## Error Dispersion Only



Severe-underestimation AUC:



\\\[

0.541.

\\]



Thus `local\_error\_std` alone is not a strong general predictor of severe underestimation across the full action-context population.



This is important because Experiments 105-108 showed that error dispersion was useful for harmful-versus-beneficial support-expansion ranking.



The combined evidence therefore suggests:



\\\[

\\boxed{

\\texttt{local\\\_error\\\_std}

\\text{ has conditional importance rather than universal importance.}

}

\\]



It contributes useful information within broader historical representations and within support-expansion decision geometry, but it is not itself the primary global calibration-failure predictor.



\---



\# Severe-Underestimation Coefficient Structure



Within the expanded historical severe-underestimation model, the strongest coefficient is:



\\\[

\\boxed{

\\texttt{local\\\_mean\\\_error}=-2.593.

}

\\]



Sign stability:



\\\[

\\boxed{100\\%}.

\\]



This is the dominant stable precursor of impending severe underestimation.



A more negative local mean historical calibration error is associated with increased risk of severe current consequence underestimation.



\---



\## Local Neighbor Distance



Coefficient:



\\\[

\-0.734.

\\]



Sign stability:



\\\[

100\\%.

\\]



This indicates that local neighborhood geometry also contributes to the pre-action representation.



\---



\## Local Minimum Error



Coefficient:



\\\[

+0.667.

\\]



Sign stability:



\\\[

100\\%.

\\]



This quantity contributes additional stable historical information beyond mean calibration bias.



\---



\## Local Error Standard Deviation



Coefficient:



\\\[

\\boxed{+0.533}.

\\]



Sign stability:



\\\[

\\boxed{100\\%}.

\\]



Thus error dispersion remains positively associated with severe-underestimation risk after conditioning on the broader historical state.



This reconciles its weak univariate severe-underestimation performance with its usefulness in the multivariate representation.



\---



\## Local Median Error



Coefficient:



\\\[

\-0.299.

\\]



Sign stability:



\\\[

100\\%.

\\]



\---



\## Predicted Action Loss



Coefficient:



\\\[

+0.222.

\\]



Sign stability:



\\\[

100\\%.

\\]



Predicted loss contributes useful information once combined with historical calibration structure, even though its univariate discrimination is much weaker.



\---



\# Signed Calibration-Error Regression



Experiment 110 also tests whether pre-action historical state predicts the continuous realized calibration error itself.



The strongest model is:



\\\[

\\boxed{

\\texttt{expanded\\\_historical\\\_regression}.

}

\\]



Its pooled performance is:



\\\[

\\boxed{

\\text{correlation}=+0.804

}

\\]



\\\[

\\boxed{

R^2=+0.647

}

\\]



and:



\\\[

\\boxed{

\\text{MAE}=0.062084.

}

\\]



The corresponding mean fold correlation is:



\\\[

+0.552.

\\]



This is materially stronger than predicted-loss-only regression.



\---



\# Predicted-Loss-Only Regression



Performance:



\\\[

\\text{correlation}=+0.753

\\]



\\\[

R^2=+0.566

\\]



\\\[

\\text{MAE}=0.070847.

\\]



Thus historical calibration state adds predictive information beyond the current predicted action loss.



\---



\# Five-Feature Calibration Regression



Performance:



\\\[

\\text{correlation}=+0.798

\\]



\\\[

R^2=+0.636

\\]



\\\[

\\text{MAE}=0.062617.

\\]



The expanded representation improves slightly beyond this five-feature state.



\---



\# Regression Coefficient Structure



For the expanded signed-error regression, the strongest standardized coefficient is:



\\\[

\\boxed{

\\texttt{local\\\_mean\\\_error}=+0.092.

}

\\]



Sign stability:



\\\[

100\\%.

\\]



This makes mechanistic sense.



Historical calibration bias carries information about the likely sign and magnitude of the next calibration error.



Additional stable contributors include:



\- predicted action loss: \\(+0.047\\)

\- local minimum error: \\(-0.028\\)

\- local error standard deviation: \\(-0.018\\)

\- local severe-underestimation fraction: \\(+0.015\\)

\- local neighbor distance: \\(+0.013\\)



all with 100% sign stability.



\---



\# Primary Classification Finding



Experiment 110 demonstrates that impending severe consequence underestimation is predictively accessible from strictly pre-action historical state.



The strongest representation achieves:



\\\[

\\boxed{

\\text{ROC AUC}=0.769

}

\\]



and:



\\\[

\\boxed{

\\text{severe recall}=77.359\\%.

}

\\]



This is substantially better than current predicted action loss alone.



Therefore:



\\\[

\\boxed{

\\text{historical calibration experience contains transferable}

\\atop

\\text{pre-action information about impending model failure.}

}

\\]



\---



\# Primary Regression Finding



The signed current calibration error is also substantially predictable from pre-action state:



\\\[

\\boxed{

r=0.804,\\quad

R^2=0.647.

}

\\]



Therefore Experiment 109's retrospectively observed calibration-error variable is not completely inaccessible before action execution.



A meaningful portion of its variation can be estimated from valid historical and prediction-time information.



\---



\# Relationship to Experiment 109



Experiment 109 showed that realized baseline action loss error nearly completed harmful-versus-beneficial support-expansion separation retrospectively.



However, that field was temporally invalid for controller use.



Experiment 110 provides the next bridge:



\\\[

\\boxed{

\\text{realized calibration error is partly predictable}

\\atop

\\text{from pre-action historical state}.

}

\\]



This does not reproduce the near-perfect retrospective discrimination of Experiment 109.



Nor should it be interpreted as doing so.



Instead, it demonstrates that the explanatory quantity identified in Experiment 109 has a valid pre-action approximation.



\---



\# Why This Matters for Controller Selectivity



The sparse support-expansion population made it difficult to learn a reliable second-stage selector directly from harmful-versus-beneficial outcomes.



Experiment 110 instead learns about impending model error using:



\\\[

25,878

\\]



action-context observations and:



\\\[

2,363

\\]



severe-underestimation events.



This greatly increases the amount of supervision available for representation learning.



The resulting proxy can now be tested separately on the support-expansion problem.



That separation is methodologically important.



The representation is learned against calibration-error targets rather than directly optimized against the eight harmful support-expansion outcomes.



\---



\# Important Distinction



Experiment 110 does \*\*not\*\* establish that the pre-action calibration-error proxy improves controller decisions.



It establishes only that impending calibration error is predictably encoded in pre-action historical state.



The next experiment must therefore test transfer:



\\\[

\\boxed{

\\text{calibration-error proxy}

\\rightarrow

\\text{support-expansion selectivity}.

}

\\]



Only that next analysis can determine whether the representation solves any portion of the harmful-versus-beneficial selection problem.



\---



\# Temporal Validity



The experiment preserves the key temporal constraint:



\\\[

\\boxed{

\\text{prediction before outcome}.

}

\\]



The current evaluated calibration error enters only after prediction and is used exclusively to construct retrospective targets and performance metrics.



Thus Experiment 110 does not contain the outcome leakage that would invalidate the Experiment 109 explanatory variable as a controller feature.



\---



\# Limitations



Experiment 110 remains retrospective.



Although leave-one-seed-out validation is strong evidence of seed-level generalization within the historical population, the representation has not yet been frozen and tested on an untouched future seed block.



Other limitations include:



\- dependence on the current simulation architecture;

\- dependence on the current local-neighborhood representation;

\- remaining performance heterogeneity across held-out seeds;

\- imperfect severe-underestimation discrimination;

\- and no demonstration yet that the proxy improves adaptive-controller selectivity.



\---



\# What Experiment 110 Supports



Experiment 110 supports the claims that:



1\. impending underestimation can be predicted from strictly pre-action historical information;



2\. impending severe underestimation can also be predicted above chance with meaningful discrimination;



3\. historical calibration state adds substantial information beyond predicted action loss alone;



4\. local mean historical calibration error is the dominant stable predictor;



5\. local error dispersion contributes conditionally within the broader state;



6\. signed current calibration error can be predicted with substantial correlation;



7\. Experiment 109's realized calibration-error mechanism has a plausible pre-action approximation.



\---



\# What Experiment 110 Does Not Support



Experiment 110 does not establish:



1\. a new controller rule;



2\. a new intervention threshold;



3\. prospective controller improvement;



4\. perfect prediction of calibration error;



5\. causal determination of model failure;



6\. that the expanded historical state is the final optimal representation;



7\. that harmful-versus-beneficial support-expansion selectivity has been solved.



\---



\# Experiment 110 Status



Experiment 110: COMPLETE



Best pre-action severe-underestimation model:



\\\[

\\boxed{

\\texttt{expanded\\\_historical\\\_state}

}

\\]



Performance:



\\\[

\\boxed{

\\text{pooled AUC}=0.769

}

\\]



\\\[

\\boxed{

\\text{mean fold AUC}=0.748

}

\\]



\\\[

\\boxed{

\\text{balanced accuracy}=70.481\\%

}

\\]



\\\[

\\boxed{

\\text{severe recall}=77.359\\%.

}

\\]



Best signed calibration-error regression:



\\\[

\\boxed{

\\texttt{expanded\\\_historical\\\_regression}

}

\\]



with:



\\\[

\\boxed{

r=0.804

}

\\]



\\\[

\\boxed{

R^2=0.647

}

\\]



\\\[

\\boxed{

\\text{MAE}=0.062084.

}

\\]



No controller intervention is defined.



\---



\# Next Research Direction



The next experiment should test whether the Experiment 110 pre-action calibration-error representation transfers into the sparse support-expansion selectivity problem.



The representation should be frozen from Experiment 110.



The support-expansion labels must not be used to redefine its features.



The next experiment should compare, under block-held-out evaluation:



\- `local\_error\_std` alone;

\- the frozen severe-underestimation probability from the expanded historical representation;

\- the frozen predicted signed calibration error;

\- and potentially a compact combination of those frozen proxy outputs.



The primary question should be:



\*\*Does a pre-action estimate of impending calibration failure distinguish harmful from beneficial support expansions more reliably than historical error dispersion alone?\*\*



Only if the frozen proxy demonstrates incremental block-generalizable selectivity should another prospective controller intervention be considered.

