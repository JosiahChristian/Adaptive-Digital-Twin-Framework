# Experiment 054 — Direct Regret-Minimizing Persistence Control

## Objective

Determine whether release-persistence control improves when the learner predicts
the downstream loss of each available persistence action directly rather than
predicting a nominal optimal persistence label.

Experiments 052 and 053 established that persistence control is a low-margin,
utility-sensitive decision problem.

Experiment 052 showed that most persistence contexts contain little or no
utility separation between competing actions.

Experiment 053 then demonstrated that exact-label accuracy can be strongly
decoupled from downstream decision quality.

Experiment 054 therefore replaces direct multiclass persistence prediction with
per-action loss estimation.

For each persistence action

\[
k\\in{1,2,3},
]

the controller estimates

\[
\\hat{L}(k\\mid x),
]

where (x) represents the current epistemic and memory context.

The selected persistence action is then

\[
\\hat{k}
===

\\arg\\min\_k
\\hat{L}(k\\mid x).
]

The principal optimization target is expected regret rather than classification
accuracy.

## Experimental Partition

The dataset contained

\[
N=249
]

decision contexts.

The deterministic train-test partition produced:

|Partition|Contexts|
|-|-:|
|Training|174|
|Test|75|

## Compared Policies

The experiment compared:

* fixed (k=1),
* fixed (k=2),
* fixed (k=3),
* an exact-label persistence classifier,
* a direct per-action loss model,
* an oracle minimum-loss controller.

For each test context, regret was defined as

\[
R
===

## L(\\hat{k})

L(k^\\star),
]

where (k^\\star) is the true minimum-loss persistence action.

## Principal Results

|Policy|Accuracy|Mean loss|Mean regret|Median regret|Max regret|Zero regret|Regret (>0.005)|
|-|-:|-:|-:|-:|-:|-:|-:|
|Fixed (k=1)|53.333%|0.167709|0.025602|0.000000|0.103023|53.333%|46.667%|
|Fixed (k=2)|33.333%|0.147927|0.005820|0.000000|0.069609|84.000%|16.000%|
|Fixed (k=3)|13.333%|0.142408|**0.000300**|0.000000|**0.008997**|**96.000%**|**4.000%**|
|Exact-label model|**66.667%**|0.150024|0.007916|0.000000|0.095188|80.000%|20.000%|
|Direct-loss model|30.667%|0.146095|**0.003988**|0.000000|0.057718|**86.667%**|**13.333%**|
|Oracle|100.000%|**0.142108**|0.000000|0.000000|0.000000|100.000%|0.000%|

## Direct-Loss Versus Exact-Label Learning

The exact-label classifier achieved

\[
66.667%
]

classification accuracy.

The direct-loss model achieved only

\[
30.667%.
]

However, classification accuracy is not the primary control objective.

The exact-label model produced mean regret

\[
R\_{\\text{exact}}
===

0.007916,
]

while the direct-loss controller produced

\[
R\_{\\text{direct}}
===

0.003988.
]

Thus direct per-action loss prediction reduced mean regret by approximately

\[
\\boxed{
49.6%
}
]

relative to exact-label learning.

The direct-loss model also reduced mean selected loss from

\[
0.150024
]

to

\[
0.146095.
]

This provides direct evidence that learning the action-value structure is more
appropriate than learning nominal persistence labels.

## Consequential-Regret Reduction

The exact-label learner produced regret greater than

\[
0.005
]

in

\[
20.000%
]

of test contexts.

The direct-loss controller reduced this fraction to

\[
13.333%.
]

Thus the direct controller reduced the prevalence of consequential errors by

\[
6.667
]

percentage points.

Its zero-regret fraction simultaneously increased from

\[
80.000%
]

to

\[
86.667%.
]

Therefore direct loss prediction improved both average regret and the
frequency with which the selected action was utility-equivalent to the oracle.

## Action-Selection Structure

The exact-label classifier selected:

|Persistence|Frequency|
|-:|-:|
|(k=1)|41.333%|
|(k=2)|56.000%|
|(k=3)|2.667%|

The direct-loss controller selected:

|Persistence|Frequency|
|-:|-:|
|(k=1)|14.667%|
|(k=2)|41.333%|
|(k=3)|44.000%|

The direct-loss architecture therefore produced a major redistribution toward
stronger persistence.

In particular, selection of

\[
k=3
]

increased from

\[
2.667%
]

under exact-label learning to

\[
44.000%
]

under direct loss optimization.

At the same time, selection of immediate persistence

\[
k=1
]

fell from

\[
41.333%
]

to

\[
14.667%.
]

This indicates that the action-value learner discovered that stronger
persistence can frequently achieve near-minimum downstream loss even when it is
not the nominal classification target.

## Fixed Strong-Persistence Baseline

Fixed

\[
k=3
]

remained an unusually strong baseline.

Its mean regret was only

\[
0.000300,
]

with zero regret in

\[
96.000%
]

of test contexts.

Its exact-label accuracy was nevertheless only

\[
13.333%.
]

This again demonstrates that persistence labels contain distinctions that are
often practically irrelevant to downstream utility.

The oracle mean loss was

\[
0.142108,
]

while fixed (k=3) achieved

\[
0.142408.
]

The absolute difference was therefore only

\[
0.000300.
]

This result suggests a strong utility asymmetry in the current persistence
regime, although directional regret should be measured explicitly before
drawing a definitive conclusion regarding asymmetric error costs.

## Interpretation

Experiment 054 demonstrates that direct per-action loss prediction is a more
appropriate learning architecture for persistence control than exact-label
classification.

The classifier attempts to recover

\[
k^\\star,
]

even when several persistence actions have nearly equivalent utility.

The direct-loss model instead estimates the quantity that actually matters:

\[
L(k\\mid x).
]

This allows the controller to make decisions that may be nominally different
from the labeled optimum while remaining close to optimal in downstream
performance.

The central result is therefore:

\[
\\boxed{
\\text{lower classification accuracy can coexist with substantially lower
control regret}.
}
]

The experiment moves the persistence architecture from classification toward
decision-theoretic control.

## Principal Conclusion

Direct action-loss modeling reduced mean regret by approximately

\[
49.6%
]

relative to exact-label learning.

It also increased zero-regret decisions and reduced the frequency of
consequential regret.

The direct-loss controller achieved these improvements despite substantially
lower exact-label accuracy.

Therefore persistence learning should no longer be optimized primarily for
categorical agreement with an oracle label.

The appropriate objective is

\[
\\boxed{
\\min\_{\\pi}
\\mathbb{E}
\\left\[
L(\\pi(x))-L(k^\\star)
\\right].
}
]

Experiment 054 provides empirical support for treating release persistence as
a regret-minimizing control problem.

## Next Research Direction

Experiment 055 should explicitly characterize the **directional regret
asymmetry** of persistence errors.

For each non-optimal decision, errors should be partitioned into:

\[
\\hat{k}<k^\\star
]

for insufficient persistence, and

\[
\\hat{k}>k^\\star
]

for excessive persistence.

The experiment should quantify:

* mean directional regret,
* maximum directional regret,
* consequential-regret frequency,
* action-pair-specific regret,
* conditional regret by true optimal persistence depth.

This will determine whether premature release is systematically more costly
than excess retention.

If such asymmetry is confirmed, the next-generation persistence controller
should incorporate asymmetric action costs directly into its optimization
objective.

