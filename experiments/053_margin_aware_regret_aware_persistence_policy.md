# Experiment 053 — Margin-Aware / Regret-Aware Persistence Policy

## Objective

Determine whether release-persistence learning should be optimized for
decision utility rather than exact persistence-label accuracy.

Experiment 052 demonstrated that persistence-policy learning is fundamentally
a low-margin problem. The median best-vs-second action margin was zero, and
only a small fraction of decision contexts exhibited meaningful utility
separation.

This implies that predicting the nominal persistence label incorrectly does
not necessarily produce a materially suboptimal control action.

Experiment 053 therefore compares:

1. fixed persistence policies,
2. an exact-label learned persistence classifier,
3. a margin-weighted learned classifier, and
4. an oracle persistence policy,

using both conventional classification accuracy and utility regret.

For a selected persistence action \(\hat{k}\), regret is defined as

\[
R
=
L(\hat{k})-L(k^\star),
\]

where \(k^\star\) is the minimum-loss persistence action.

The principal hypothesis is that

\[
\text{classification error}
\neq
\text{decision error}.
\]

## Experimental Partition

The persistence-margin dataset contained

\[
N=249
\]

decision contexts.

The deterministic train-test split produced:

| Partition | Contexts |
|---|---:|
| Training | 174 |
| Test | 75 |

The learned models were evaluated on the 75-context held-out test partition.

## Compared Policies

The evaluated policies were:

\[
k=1,
\qquad
k=2,
\qquad
k=3,
\]

as fixed baselines, together with:

- an exact-label random-forest persistence classifier,
- a margin-weighted random-forest classifier,
- an oracle selecting the minimum-loss action.

The margin-weighted learner increased training importance for contexts with
larger best-vs-second utility margins.

Thus ambiguous near-tie contexts contributed less influence than contexts in
which persistence choice materially changed downstream loss.

## Principal Results

| Policy | Accuracy | Mean loss | Mean regret | Median regret | Max regret | Zero regret |
|---|---:|---:|---:|---:|---:|---:|
| Fixed \(k=1\) | 53.333% | 0.167709 | 0.025602 | 0.000000 | 0.103023 | 53.333% |
| Fixed \(k=2\) | 33.333% | 0.147927 | 0.005820 | 0.000000 | 0.069609 | 84.000% |
| Fixed \(k=3\) | 13.333% | 0.142408 | **0.000300** | 0.000000 | **0.008997** | **96.000%** |
| Exact-label model | **66.667%** | 0.150024 | 0.007916 | 0.000000 | 0.095188 | 80.000% |
| Margin-weighted model | 33.333% | 0.148746 | 0.006638 | 0.000000 | 0.069609 | 84.000% |
| Oracle | 100.000% | **0.142108** | 0.000000 | 0.000000 | 0.000000 | 100.000% |

## Exact-Label Learning

The exact-label classifier achieved the highest learned classification
accuracy:

\[
\boxed{
66.667\%
}
\]

but its mean regret was

\[
0.007916.
\]

Its zero-regret fraction was

\[
80.000\%.
\]

Therefore one fifth of its test decisions produced measurable utility loss.

Most importantly, high label accuracy did not translate into the lowest
decision regret.

## Margin-Weighted Learning

The margin-weighted classifier achieved only

\[
33.333\%
\]

exact-label accuracy.

However, its mean regret improved to

\[
0.006638,
\]

compared with

\[
0.007916
\]

for the exact-label classifier.

This corresponds to an approximate regret reduction of

\[
16.1\%.
\]

The fraction of zero-regret decisions also increased from

\[
80.000\%
\]

to

\[
84.000\%.
\]

Thus margin-aware weighting reduced utility loss despite substantially reducing
nominal classification accuracy.

This directly confirms that exact-label accuracy is not an adequate objective
for this persistence-control problem.

## Fixed Strong-Persistence Result

The most important result of Experiment 053 is the behavior of fixed

\[
k=3.
\]

Its exact-label accuracy was only

\[
13.333\%.
\]

Under a conventional classification interpretation, this policy appears very
poor.

Yet its mean regret was only

\[
\boxed{
0.000300
}
\]

and its zero-regret fraction was

\[
\boxed{
96.000\%.
}
\]

Its maximum regret was also only

\[
0.008997,
\]

far below the maximum regret of the learned exact-label model:

\[
0.095188.
\]

Therefore fixed \(k=3\) was nominally incorrect in most contexts while being
almost always utility-equivalent to the oracle.

This is a direct empirical manifestation of the low-margin structure identified
in Experiment 052.

## Accuracy-Regret Decoupling

The experiment establishes a strong decoupling between

\[
\text{action-label accuracy}
\]

and

\[
\text{control utility}.
\]

For example,

\[
\text{accuracy}_{k=3}
=
13.333\%
\]

while

\[
\text{zero-regret}_{k=3}
=
96.000\%.
\]

Conversely, the exact-label learner achieved

\[
66.667\%
\]

accuracy but only

\[
80.000\%
\]

zero-regret performance.

Hence

\[
\boxed{
\text{predicting the nominal optimum}
\neq
\text{avoiding meaningful regret}.
}
\]

In low-margin regimes, multiple actions may be operationally equivalent even
when only one is labeled as the nominal optimum.

## Interpretation

Experiment 053 validates the central conclusion of Experiment 052.

Persistence-policy learning should not be framed primarily as multiclass
classification.

The system contains large regions of action-value equivalence, so exact labels
encode distinctions that often have negligible control consequence.

The correct optimization target is therefore not

\[
\max
P(\hat{k}=k^\star),
\]

but rather

\[
\min
\mathbb{E}
\left[
L(\hat{k})-L(k^\star)
\right].
\]

This converts the persistence problem from label prediction into
cost-sensitive decision control.

The margin-weighted learner moved in this direction by assigning greater
training importance to consequential decisions.

Its reduced regret despite reduced accuracy provides direct evidence that the
learning objective is beginning to align more closely with system utility.

## Structural Implication

The strong performance of fixed \(k=3\) reveals an additional property.

The persistence-action space appears asymmetric.

Choosing stronger persistence is frequently label-suboptimal but
utility-equivalent, whereas choosing insufficient persistence can produce much
larger regret.

This suggests that persistence control may have an asymmetric error structure:

\[
\boxed{
\text{premature release risk}
>
\text{excess retention cost}
}
\]

for much of the current experimental regime.

Therefore the decision architecture may benefit from explicitly modeling
directional action costs rather than treating all persistence mistakes equally.

## Principal Conclusion

Experiment 053 demonstrates that exact-label persistence accuracy is a poor
proxy for adaptive digital-twin control quality.

The margin-weighted learner reduced mean regret relative to the conventional
exact-label learner even though its classification accuracy fell substantially.

More importantly, fixed strong persistence achieved nearly oracle-level utility
despite extremely low nominal-label accuracy.

The central result is therefore:

\[
\boxed{
\text{utility-equivalent actions should not be penalized as classification
errors}.
}
\]

The persistence-control problem should henceforth be evaluated primarily in
terms of regret, consequential error, and downstream system utility.

## Next Research Direction

Experiment 054 should move beyond margin-weighted classification and directly
learn the action-value structure.

Instead of predicting a persistence label

\[
\hat{k},
\]

the model should estimate

\[
\hat{L}(k\mid z_{1:t},M_t)
\]

for each

\[
k\in\{1,2,3\}.
\]

The persistence action can then be chosen through

\[
\hat{k}
=
\arg\min_k
\hat{L}(k\mid z_{1:t},M_t).
\]

This would constitute a direct **regret-minimizing persistence controller**.

Experiment 054 should compare:

- exact-label classification,
- margin-weighted classification,
- direct per-action loss prediction,
- fixed persistence baselines,
- oracle action selection.

The principal metric should become

\[
\boxed{
\mathbb{E}[R]
}
\]

rather than exact-label accuracy.

A secondary objective should quantify asymmetric regret, particularly whether
errors toward insufficient persistence produce systematically larger losses
than errors toward excessive persistence.
