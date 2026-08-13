\# Experiment 094 — Absolute Loss-Floor Harmful-Expansion Analysis



\## Objective



Experiment 093 showed that action-conditioned epistemic excess does not specifically explain harmful responsive expansion.



The strongest retrospective signal instead emerged from:



\\\[

\\boxed{

\\text{absolute predicted action loss}.

}

\\]



Experiment 094 therefore investigates whether harmful responsive expansions occur in contexts where the entire predicted loss surface is elevated, and whether those predicted losses are calibrated to realized consequence.



The central questions are:



\\\[

\\boxed{

\\text{Are harmful expansions associated with elevated predicted}

\\atop

\\text{loss-floor and loss-surface severity?}

}

\\]



and:



\\\[

\\boxed{

\\text{Are those predicted losses systematically miscalibrated}

\\atop

\\text{relative to realized consequence?}

}

\\]



The experiment is retrospective.



No controller threshold is defined.



No new prospective seed block is consumed.



\---



\# Analysis Population



Experiment 094 analyzes the same existing responsive expansion population used in Experiments 093 and earlier harmful-expansion analyses.



Generation seeds:



\\\[

44001,\\ldots,44010.

\\]



The event population contains:



\\\[

\\boxed{

65

}

\\]



responsive expansion events:



\\\[

\\boxed{

50

\\text{ beneficial}

}

\\]



and:



\\\[

\\boxed{

15

\\text{ harmful}.

}

\\]



For every event, the full predicted three-action loss surface is reconstructed.



\---



\# Predicted Loss Surface



For each context \\(x\\), the predicted persistence-action losses are:



\\\[

\\hat L\_1(x),

\\]



\\\[

\\hat L\_2(x),

\\]



and:



\\\[

\\hat L\_3(x).

\\]



Experiment 094 derives four contextual summary quantities.



\## Predicted Loss Floor



\\\[

\\boxed{

F(x)

=

\\min\_a \\hat L\_a(x).

}

\\]



\## Predicted Loss Mean



\\\[

\\boxed{

M(x)

=

\\frac{1}{3}

\\sum\_a

\\hat L\_a(x).

}

\\]



\## Predicted Loss Ceiling



\\\[

\\boxed{

C(x)

=

\\max\_a \\hat L\_a(x).

}

\\]



\## Predicted Loss Spread



\\\[

\\boxed{

S(x)

=

C(x)-F(x).

}

\\]



These describe the absolute level and dispersion of the predicted consequence surface.



\---



\# Expanded-Action Predicted Loss



For the responsive expansion action \\(a\_e\\), Experiment 094 also records:



\\\[

\\boxed{

\\hat L\_{a\_e}(x).

}

\\]



The relative predicted loss is:



\\\[

\\boxed{

\\hat L\_{a\_e}(x)-F(x).

}

\\]



This distinction allows the experiment to separate:



\- absolute predicted consequence,

\- from relative action ranking.



\---



\# Predicted Loss Floor



Beneficial responsive expansions have mean predicted loss floor:



\\\[

0.115905.

\\]



Harmful expansions have:



\\\[

\\boxed{

0.144640.

}

\\]



Difference:



\\\[

\\boxed{

+0.028734.

}

\\]



Standardized effect:



\\\[

\\boxed{

+0.683.

}

\\]



Thus harmful responsive expansions occur in contexts with meaningfully higher predicted minimum consequence.



\---



\# Predicted Loss Mean



The predicted surface mean is:



\\\[

0.124059

\\]



for beneficial events and:



\\\[

\\boxed{

0.159230

}

\\]



for harmful events.



Difference:



\\\[

+0.035172.

\\]



Standardized effect:



\\\[

\\boxed{

+0.799.

}

\\]



This separation is stronger than the loss-floor effect.



\---



\# Predicted Loss Ceiling



The predicted ceiling is:



\\\[

0.132677

\\]



for beneficial expansions and:



\\\[

\\boxed{

0.171673

}

\\]



for harmful expansions.



Difference:



\\\[

+0.038996.

\\]



Standardized effect:



\\\[

\\boxed{

+0.875.

}

\\]



This is the strongest univariate separation among the pure predicted loss-level summaries.



\---



\# Predicted Loss Spread



Predicted loss spread increases from:



\\\[

0.016772

\\]



for beneficial events to:



\\\[

\\boxed{

0.027033

}

\\]



for harmful events.



Difference:



\\\[

+0.010261.

\\]



Standardized effect:



\\\[

\\boxed{

+0.778.

}

\\]



Thus harmful contexts are not only elevated in predicted consequence but also more action-sensitive according to the learned loss surface.



\---



\# Predicted Expanded-Action Loss



Beneficial expansion actions have mean:



\\\[

0.115915.

\\]



Harmful expansion actions have:



\\\[

\\boxed{

0.144640.

}

\\]



Difference:



\\\[

+0.028725.

\\]



Standardized effect:



\\\[

\\boxed{

+0.683.

}

\\]



This is effectively identical to the predicted floor.



\---



\# Relative Predicted Loss



Predicted relative loss is:



\\\[

0.000010

\\]



for beneficial expansions and:



\\\[

0.000000

\\]



for harmful expansions.



Thus:



\\\[

\\boxed{

\\hat L\_{a\_e}

\\approx

F(x)

}

\\]



for both event classes.



This means harmful expansion does not arise because the controller selects an action that looks poor relative to its alternatives.



Instead, the expanded action generally appears to be the predicted best action.



\---



\# Absolute Versus Relative Consequence



The results reveal an important distinction.



The controller correctly identifies approximately:



\\\[

\\boxed{

\\text{the predicted minimum-loss action}

}

\\]



while harmful contexts still exhibit larger absolute predicted consequence.



Therefore:



\\\[

\\boxed{

\\text{relative optimization can appear correct even when}

\\atop

\\text{absolute consequence remains severe}.

}

\\]



The relevant warning signal is not poor rank.



It is elevated overall predicted loss-surface severity.



\---



\# Realized Best Loss



The true best achievable loss differs much more strongly between event classes.



Beneficial contexts:



\\\[

0.087974.

\\]



Harmful contexts:



\\\[

\\boxed{

0.203055.

}

\\]



Difference:



\\\[

\\boxed{

+0.115082.

}

\\]



Standardized effect:



\\\[

\\boxed{

+1.829.

}

\\]



Thus harmful expansion events occur in contexts that are genuinely much more difficult even under the optimal action.



\---



\# Realized Expanded-Action Loss



The realized expanded-action loss is:



\\\[

0.087974

\\]



for beneficial events and:



\\\[

\\boxed{

0.258635

}

\\]



for harmful events.



Difference:



\\\[

\\boxed{

+0.170661.

}

\\]



Standardized effect:



\\\[

\\boxed{

+2.739.

}

\\]



This is an extremely large separation.



\---



\# Incremental Regret



Beneficial responsive expansions have:



\\\[

0

\\]



mean incremental regret.



Harmful expansions have:



\\\[

\\boxed{

0.055580.

}

\\]



Standardized effect:



\\\[

\\boxed{

+6.437.

}

\\]



This quantity defines the realized harmful-expansion mechanism and therefore serves as an outcome variable rather than a deployable predictor.



\---



\# Loss-Floor Calibration Error



Define:



\\\[

\\boxed{

e\_F(x)

=

F(x)-L^\*(x).

}

\\]



For beneficial contexts:



\\\[

e\_F

=

\\boxed{

+0.027932.

}

\\]



For harmful contexts:



\\\[

e\_F

=

\\boxed{

\-0.058416.

}

\\]



Difference:



\\\[

\-0.086347.

\\]



Standardized effect:



\\\[

\\boxed{

\-1.745.

}

\\]



The sign reverses between the two event classes.



\---



\# Interpretation of Loss-Floor Error



For beneficial events:



\\\[

F(x)>L^\*(x)

\\]



on average.



Thus the predicted loss floor is mildly conservative.



For harmful events:



\\\[

\\boxed{

F(x)<L^\*(x).

}

\\]



Thus the predicted loss floor is systematically too optimistic.



The model underestimates the minimum achievable realized consequence in harmful contexts.



\---



\# Expanded-Action Calibration Error



Define:



\\\[

\\boxed{

e\_a(x)

=

\\hat L\_{a\_e}(x)

\-

L(x,a\_e).

}

\\]



Beneficial events have:



\\\[

e\_a

=

\\boxed{

+0.027942.

}

\\]



Harmful events have:



\\\[

e\_a

=

\\boxed{

\-0.113995.

}

\\]



Difference:



\\\[

\\boxed{

\-0.141937.

}

\\]



Standardized effect:



\\\[

\\boxed{

\-2.949.

}

\\]



This is one of the strongest mechanistic separations in the experimental sequence.



\---



\# Expanded-Action Underestimation



The sign of:



\\\[

e\_a

\\]



means that harmful events are characterized by severe consequence underestimation.



The model predicts approximately:



\\\[

\\hat L\_{a\_e}

\\approx

0.145

\\]



while realized expanded-action loss is approximately:



\\\[

L(x,a\_e)

\\approx

0.259.

\\]



Thus the mean underestimation is roughly:



\\\[

\\boxed{

0.114.

}

\\]



This is much larger than the absolute difference between beneficial and harmful predicted loss.



\---



\# Absolute Calibration Error



The absolute loss-floor error increases from:



\\\[

0.044048

\\]



to:



\\\[

\\boxed{

0.068145.

}

\\]



Standardized effect:



\\\[

+0.686.

\\]



The absolute expanded-action loss error increases much more strongly:



\\\[

0.044058

\\rightarrow

\\boxed{

0.113995.

}

\\]



Standardized effect:



\\\[

\\boxed{

+1.873.

}

\\]



Therefore harmful expansion is strongly associated with poor absolute action-level calibration.



\---



\# Predicted Floor to True-Loss Ratio



The ratio:



\\\[

\\frac{

F(x)

}{

L^\*(x)

}

\\]



is:



\\\[

1.859391

\\]



for beneficial contexts and:



\\\[

\\boxed{

0.759042

}

\\]



for harmful contexts.



Difference:



\\\[

\-1.100350.

\\]



Standardized effect:



\\\[

\\boxed{

\-1.175.

}

\\]



Thus beneficial contexts are generally conservatively predicted, while harmful contexts are systematically underpredicted.



\---



\# Calibration Regime Split



Experiment 094 therefore identifies two qualitatively different calibration regimes.



\## Beneficial Expansion Regime



The learned loss model tends to satisfy:



\\\[

\\boxed{

\\hat L

>

L

}

\\]



on average.



The prediction is conservative.



\## Harmful Expansion Regime



The learned loss model tends to satisfy:



\\\[

\\boxed{

\\hat L

<

L.

}

\\]



The prediction is optimistic.



This sign reversal is a major mechanistic result.



\---



\# Global Loss-Floor Calibration



Across all 65 events, linear calibration of:



\\\[

F(x)

\\]



against:



\\\[

L^\*(x)

\\]



produces slope:



\\\[

\\boxed{

1.170

}

\\]



and intercept:



\\\[

\-0.028858.

\\]



Correlation is:



\\\[

\\boxed{

0.641.

}

\\]



Mean absolute residual is:



\\\[

0.046065.

\\]



Thus the predicted floor carries meaningful information about true best loss, but calibration remains imperfect.



\---



\# Global Expanded-Action Calibration



Predicted expanded-action loss against realized expanded-action loss gives slope:



\\\[

\\boxed{

1.337

}

\\]



and intercept:



\\\[

\-0.036525.

\\]



Correlation is:



\\\[

\\boxed{

0.610.

}

\\]



Mean absolute residual is:



\\\[

0.057502.

\\]



Thus predicted action consequence is moderately correlated with realized action consequence, but event-level errors remain large.



\---



\# Predicted-Loss-Floor Classification



Using only the predicted floor gives:



\\\[

66.333\\%

\\]



balanced accuracy,



\\\[

66.667\\%

\\]



harmful recall,



\\\[

66.000\\%

\\]



beneficial specificity,



and:



\\\[

\\boxed{

\\text{ROC-AUC}=0.708.

}

\\]



The standardized coefficient is:



\\\[

\\boxed{

+0.810

}

\\]



with:



\\\[

\\boxed{

100\\%

}

\\]



sign stability.



Thus higher predicted loss floor consistently corresponds to greater harmful-expansion probability.



\---



\# Predicted Loss Mean Classification



Predicted loss mean improves thresholded classification:



\\\[

\\boxed{

73.000\\%

\\text{ balanced accuracy}

}

\\]



with:



\\\[

80.000\\%

\\]



harmful recall and:



\\\[

66.000\\%

\\]



beneficial specificity.



ROC-AUC is:



\\\[

0.707.

\\]



The standardized coefficient is:



\\\[

\\boxed{

+0.928

}

\\]



with:



\\\[

100\\%

\\]



sign stability.



\---



\# Predicted Loss Ceiling Classification



The strongest standalone predicted-surface classifier by balanced accuracy is the predicted ceiling.



It achieves:



\\\[

\\boxed{

76.333\\%

\\text{ balanced accuracy}

}

\\]



with:



\\\[

\\boxed{

86.667\\%

\\text{ harmful recall}

}

\\]



\\\[

66.000\\%

\\text{ beneficial specificity}

\\]



and:



\\\[

\\text{ROC-AUC}=0.711.

\\]



The standardized coefficient is:



\\\[

\\boxed{

+0.991

}

\\]



with:



\\\[

100\\%

\\]



sign stability.



Thus:



\\\[

\\boxed{

C(x)\\uparrow

\\Rightarrow

P(\\text{harmful expansion})\\uparrow

}

\\]



is a strong retrospective relationship.



\---



\# Predicted Loss Spread Classification



Predicted spread achieves:



\\\[

70.333\\%

\\]



balanced accuracy,



\\\[

66.667\\%

\\]



harmful recall,



\\\[

74.000\\%

\\]



beneficial specificity,



and:



\\\[

0.683

\\]



pooled ROC-AUC.



Mean fold ROC-AUC is:



\\\[

\\boxed{

0.870.

}

\\]



Its coefficient is:



\\\[

\\boxed{

+0.705

}

\\]



with:



\\\[

100\\%

\\]



sign stability.



This indicates that action-sensitivity of the predicted surface also carries meaningful information.



\---



\# Surface-Level Mechanism



The predicted loss surface therefore has two relevant properties in harmful contexts.



\## Elevated Level



The:



\\\[

\\text{floor},

\\]



\\\[

\\text{mean},

\\]



and:



\\\[

\\text{ceiling}

\\]



are all higher.



\## Greater Dispersion



The spread is also larger.



Therefore the deployable pre-action pattern is better described as:



\\\[

\\boxed{

\\textbf{elevated predicted loss-surface severity}

}

\\]



rather than simply:



\\\[

\\text{high loss floor}.

\\]



\---



\# Compact Surface Models



The floor-plus-spread model achieves:



\\\[

66.333\\%

\\]



balanced accuracy.



The three-variable surface model using:



\\\[

F(x),

\\]



\\\[

S(x),

\\]



and:



\\\[

\\hat L\_{a\_e}

\\]



achieves:



\\\[

67.333\\%

\\]



balanced accuracy.



Neither outperforms the predicted ceiling alone.



Thus additional surface complexity does not automatically improve pooled discrimination.



\---



\# Strong Retrospective Calibration Model



The `calibration\_compact` model contains:



\\\[

F(x),

\\]



\\\[

e\_F(x),

\\]



and:



\\\[

e\_a(x).

\\]



It achieves:



\\\[

\\boxed{

95.000\\%

\\text{ balanced accuracy}

}

\\]



with:



\\\[

\\boxed{

100.000\\%

\\text{ harmful recall}

}

\\]



\\\[

75.000\\%

\\text{ harmful precision}

\\]



\\\[

\\boxed{

90.000\\%

\\text{ beneficial specificity}

}

\\]



and:



\\\[

\\boxed{

\\text{ROC-AUC}=0.979.

}

\\]



Mean fold balanced accuracy is:



\\\[

93.887\\%.

\\]



Mean fold AUC is:



\\\[

0.913.

\\]



This is the strongest retrospective classifier observed in Experiment 094.



\---



\# Calibration-Model Coefficients



The dominant coefficient is:



\\\[

\\boxed{

\\beta\_{e\_a}

=

\-2.593.

}

\\]



The loss-floor-error coefficient is:



\\\[

+0.507.

\\]



The predicted-floor coefficient is:



\\\[

+0.503.

\\]



All coefficient signs are stable across:



\\\[

\\boxed{

100\\%

}

\\]



of evaluated folds.



The expanded-action calibration error therefore dominates the retrospective classifier.



\---



\# Critical Deployability Distinction



The calibration model must not be interpreted as a deployable controller.



Both:



\\\[

e\_F(x)

\\]



and:



\\\[

e\_a(x)

\\]



depend on realized quantities.



Specifically:



\\\[

e\_F(x)

=

F(x)-L^\*(x)

\\]



requires knowledge of:



\\\[

L^\*(x),

\\]



and:



\\\[

e\_a(x)

=

\\hat L\_a-L(x,a)

\\]



requires realized action consequence.



These quantities are unavailable before acting.



Therefore:



\\\[

\\boxed{

\\text{the calibration model is a retrospective failure detector,}

\\atop

\\text{not a decision-time safety guard}.

}

\\]



\---



\# Deployable Versus Post-Outcome Variables



\## Available Before Action



The controller can know:



\\\[

F(x),

\\]



\\\[

M(x),

\\]



\\\[

C(x),

\\]



\\\[

S(x),

\\]



\\\[

\\hat L\_a.

\\]



These are legitimate candidate pre-action risk signals.



\## Available Only After Outcome



The controller cannot know:



\\\[

L^\*(x),

\\]



\\\[

L(x,a),

\\]



\\\[

e\_F(x),

\\]



\\\[

e\_a(x),

\\]



or realized incremental regret before the consequence occurs.



These variables are diagnostic targets rather than controller inputs.



\---



\# Ranking Calibration Versus Absolute Calibration



The expanded action usually satisfies:



\\\[

\\hat L\_a

\\approx

F(x).

\\]



Thus the model is generally selecting the predicted best action.



Yet harmful contexts still show severe:



\\\[

\\hat L\_a-L(x,a)<0.

\\]



This means the key failure is not necessarily action ranking.



It is:



\\\[

\\boxed{

\\text{absolute consequence calibration}.

}

\\]



Therefore:



\\\[

\\boxed{

\\text{ranking calibration}

\\neq

\\text{absolute consequence calibration}.

}

\\]



A model may rank actions correctly while remaining dangerously optimistic about all available actions.



\---



\# Relation to Experiment 090



Experiment 090 found that the harder prospective block exhibited:



\- greater predicted loss separation,

\- lower predicted risk,

\- lower predicted downside,

\- and greater realized under-persistence.



Experiment 094 adds a mechanistic interpretation.



Elevated loss-surface severity may be a pre-action indicator that the controller is operating in a region where its nominal safety-confidence systems are overly optimistic.



This creates a plausible bridge between:



\\\[

\\text{cross-regime model disagreement}

\\]



and:



\\\[

\\text{event-level harmful consequence underestimation}.

\\]



\---



\# Relation to Experiment 093



Experiment 093 showed that action-conditioned epistemic excess does not explain harmful responsive expansion well.



Experiment 094 finds a much stronger mechanism:



\\\[

\\boxed{

\\text{absolute loss-surface severity}

\+

\\text{consequence underestimation}.

}

\\]



Thus the research direction shifts from:



\\\[

\\text{support geometry}

\\]



toward:



\\\[

\\boxed{

\\text{calibration-risk prediction}.

}

\\]



\---



\# What Experiment 094 Establishes



Experiment 094 supports the following retrospective propositions.



First:



\\\[

\\boxed{

\\text{harmful responsive expansions occur in contexts with}

\\atop

\\text{higher predicted loss-surface level and spread}.

}

\\]



Second:



\\\[

\\boxed{

\\text{those contexts are genuinely more costly in realized consequence}.

}

\\]



Third:



\\\[

\\boxed{

\\text{the learned loss model severely underestimates realized}

\\atop

\\text{expanded-action consequence in harmful events}.

}

\\]



Fourth:



\\\[

\\boxed{

\\text{absolute calibration failure is substantially more informative}

\\atop

\\text{than the support-derived mechanisms tested in Experiment 093}.

}

\\]



\---



\# What Experiment 094 Does Not Establish



Experiment 094 does not establish that:



\- a specific predicted-loss threshold should be deployed,

\- the calibration errors can be known before acting,

\- predicted loss ceiling is universally optimal,

\- the loss model is globally miscalibrated,

\- or a new controller guard has been prospectively validated.



The experiment remains retrospective.



\---



\# Principal Conclusion



Harmful responsive expansion is associated with an elevated and dispersed predicted loss surface.



The strongest deployable univariate surface signal is:



\\\[

\\boxed{

C(x)

=

\\max\_a\\hat L\_a(x),

}

\\]



which achieves:



\\\[

\\boxed{

76.333\\%

\\text{ balanced accuracy}

}

\\]



and:



\\\[

\\boxed{

86.667\\%

\\text{ harmful recall}.

}

\\]



However, the deeper retrospective mechanism is calibration failure.



For harmful events:



\\\[

\\boxed{

\\hat L\_a-L(x,a)

=

\-0.113995

}

\\]



on average.



For beneficial events:



\\\[

\\boxed{

\\hat L\_a-L(x,a)

=

+0.027942.

}

\\]



The standardized difference is:



\\\[

\\boxed{

\-2.949.

}

\\]



Therefore:



\\\[

\\boxed{

\\text{harmful expansion is strongly associated with severe}

\\atop

\\text{absolute consequence underestimation}.

}

\\]



\---



\# Final Scientific Interpretation



The controller appears capable of identifying the action that looks best relative to alternatives while still being dangerously optimistic about the absolute consequence level.



This creates the distinction:



\\\[

\\boxed{

\\text{“Which action looks best?”}

}

\\]



versus:



\\\[

\\boxed{

\\text{“How much should the predicted consequence surface itself be trusted?”}

}

\\]



Experiment 094 suggests that the second question is now central.



\---



\# Next Research Direction



Experiment 095 should remain retrospective and diagnostic.



It should ask whether the severe post-outcome calibration failure identified here can itself be predicted using only variables available before action selection.



The target should be a pre-action estimate of:



\\\[

\\boxed{

P(

\\hat L\_a-L(x,a)

<

\-\\delta

\\mid

X\_{\\text{pre-action}}

)

}

\\]



for an explicitly defined underestimation severity criterion.



Candidate predictors may include:



\- predicted loss floor,

\- predicted loss mean,

\- predicted loss ceiling,

\- predicted loss spread,

\- predicted action loss,

\- predicted risk,

\- safety probability,

\- predicted downside,

\- context support,

\- transient-state probability,

\- mismatch,

\- anchor age,

\- trigger score,

\- and relevant loss-geometry contrasts.



Experiment 095 should compare simple compact models and leave-one-seed-out stability.



No new controller should be defined yet.



The central question is:



\\\[

\\boxed{

\\text{Can severe future consequence underestimation be recognized}

\\atop

\\text{before the responsive action is executed?}

}

\\]



Only if a stable pre-action calibration-risk signal emerges should a later experiment freeze a prospective calibration-aware guard.

