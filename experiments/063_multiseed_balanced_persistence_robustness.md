# Experiment 063 — Multi-Seed Balanced Persistence Robustness

## Objective

Determine whether the preferred persistence-control operating regimes identified
under the original deterministic train-test partition remain stable across
independent randomized data partitions.

Experiments 060–062 identified a balanced adaptive operating point near

\[
\\alpha=0.25
]

under one deterministic partition.

However, operating-point selection from a single split may reflect accidental
properties of the training and test composition.

Experiment 063 therefore evaluates the principal persistence policies across

\[
10
]

independent randomized train-test partitions.

The analysis tests robustness of:

* mean regret,
* under-persistence frequency,
* over-persistence frequency,
* action entropy,
* Pareto efficiency.

## Scope of Robustness Analysis

The underlying analysis dataset contained

\[
249
]

decision contexts.

For each seed

\[
s\\in{0,1,\\ldots,9},
]

the contexts were randomly reordered and divided into independent training and
test partitions.

The evaluated policies were:

* direct-loss persistence control,
* fixed-risk control with penalty (0.010),
* two-stage risk control with (\\alpha=0.10),
* two-stage risk control with (\\alpha=0.25),
* two-stage risk control with (\\alpha=1.00),
* fixed (k=3),
* oracle persistence control.

This experiment therefore measures **partition robustness**.

It does not yet regenerate an independent trajectory population for every seed.

## Multi-Seed Results

|Policy|Mean regret|Regret std.|Median regret|Regret range|Mean under|Max under|Mean over|Mean entropy|Min entropy|Pareto frequency|
|-|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|
|Direct loss|**0.007287**|0.002103|0.007158|0.003394–0.011428|4.70|7|**46.10**|**0.944**|**0.890**|**100%**|
|Fixed risk (0.010)|0.007757|0.002462|0.007190|0.004211–0.012293|3.00|5|65.00|0.316|0.223|10%|
|Two stage (0.10)|0.007504|**0.002073**|0.007355|0.004211–0.010949|4.20|5|52.70|0.810|0.702|40%|
|Two stage (0.25)|0.007597|0.002180|0.007124|0.004211–0.011340|3.70|5|56.50|0.658|0.501|40%|
|Two stage (1.00)|0.007688|0.002187|**0.006877**|0.005368–0.011957|**1.10**|**2**|64.90|0.327|0.153|**100%**|
|Fixed (k=3)|0.008013|0.002400|0.007127|0.005373–0.012576|**0.00**|**0**|70.10|0.000|0.000|0%|
|Oracle|0.000000|0.000000|0.000000|0.000000–0.000000|0.00|0|0.00|0.716|0.611|reference|

## Failure of Single-Split Operating-Point Dominance

Experiment 062 identified

\[
\\alpha=0.25
]

as the preferred interior operating point under the original deterministic
partition.

Across randomized partitions, however, two-stage (0.25) was Pareto-efficient
in only

\[
\\boxed{
40%
}
]

of evaluated splits.

Its mean regret was

\[
0.007597,
]

with mean under-persistence count

\[
3.70.
]

Therefore the apparent dominance of

\[
\\alpha=0.25
]

does not generalize strongly across partition realizations.

The previous result should consequently be interpreted as a
split-conditioned operating point rather than a globally robust optimum.

## Robust Responsive Endpoint

The direct-loss controller was Pareto-efficient in

\[
\\boxed{
100%
}
]

of randomized partitions.

It achieved the lowest mean regret among the evaluated learned adaptive
policies:

\[
\\boxed{
0.007287.
}
]

Its mean normalized action entropy was

\[
\\boxed{
0.944,
}
]

with minimum entropy across all seeds

\[
0.890.
]

Thus direct-loss control exhibits highly robust adaptive responsiveness.

However, this responsiveness is accompanied by mean under-persistence count

\[
4.70,
]

with a maximum of

\[
7.
]

The direct-loss controller therefore represents a robust responsive endpoint
rather than a robust safe operating point.

## Robust Safety-Adaptive Endpoint

The two-stage controller with

\[
\\boxed{
\\alpha=1.00
}
]

was also Pareto-efficient in

\[
\\boxed{
100%
}
]

of randomized partitions.

Its mean under-persistence count was only

\[
\\boxed{
1.10,
}
]

and no partition produced more than

\[
\\boxed{
2
}
]

under-persistence decisions.

Mean regret remained

\[
0.007688.
]

Action entropy remained nonzero:

\[
\\overline{H}
===

0.327,
]

with minimum observed entropy

\[
0.153.
]

Therefore two-stage (1.00) provides a robust safety-oriented adaptive regime
without collapsing completely to fixed maximal persistence.

## Emergent Robust Frontier

The multi-seed results reveal two particularly stable adaptive regimes:

\[
\\boxed{
\\text{direct loss}
}
]

and

\[
\\boxed{
\\text{two-stage }1.00.
}
]

Direct loss provides high responsiveness and relatively low mean regret.

Two-stage (1.00) provides substantially stronger protection against
under-persistence while retaining some adaptive action variation.

Both remained Pareto-efficient across every randomized split.

This suggests that the robust control problem is better represented by a
persistent tradeoff between these regimes than by one universally preferred
intermediate multiplier.

## Intermediate Risk Policies

Two-stage (0.10) and two-stage (0.25) were each Pareto-efficient in only

\[
40%
]

of splits.

Two-stage (0.10) maintained relatively high mean entropy:

\[
0.810,
]

with mean under-persistence count

\[
4.20.
]

Two-stage (0.25) reduced mean under-persistence to

\[
3.70
]

while reducing mean entropy to

\[
0.658.
]

Neither policy displayed the cross-partition Pareto stability of direct loss or
two-stage (1.00).

Thus intermediate penalty settings appear more sensitive to sample
composition.

## Fixed-Risk Policy Robustness

Fixed-risk control with penalty

\[
0.010
]

was Pareto-efficient in only

\[
10%
]

of randomized partitions.

Its mean regret was

\[
0.007757,
]

with mean action entropy

\[
0.316.
]

This indicates that a globally fixed asymmetric penalty is less robust than the
state-dependent two-stage architecture.

In particular, two-stage (1.00) achieved a similar average entropy while
providing much stronger Pareto stability.

## Reassessment of Fixed Strong Persistence

A major result concerns fixed

\[
k=3.
]

Under the original deterministic partition, fixed strong persistence achieved
exceptionally low regret and appeared close to the oracle.

Across randomized partitions, its mean regret increased to

\[
\\boxed{
0.008013.
}
]

This was worse than every evaluated learned adaptive policy.

Although fixed (k=3) completely eliminated under-persistence,

\[
N\_{\\text{under}}=0,
]

it produced mean over-persistence count

\[
70.10
]

and zero action entropy.

It was Pareto-efficient in

\[
\\boxed{
0%
}
]

of adaptive-policy comparisons.

Therefore the exceptional performance of fixed strong persistence on the
original split was not robust.

This is strong evidence that conclusions based on one partition can materially
overstate the value of maximal conservatism.

## Regret Variability

All learned adaptive policies exhibited nonzero regret variation across
partitions.

Direct loss produced

\[
\\sigma\_R=0.002103.
]

Two-stage (0.10) produced

\[
\\sigma\_R=0.002073.
]

Two-stage (0.25) produced

\[
\\sigma\_R=0.002180.
]

Two-stage (1.00) produced

\[
\\sigma\_R=0.002187.
]

Thus no tested adaptive policy is insensitive to partition composition.

Robustness must therefore be treated as a distributional property rather than
inferred from a single test result.

## Structural Interpretation

Experiment 063 changes the interpretation of the safe-responsive persistence
frontier.

The previous experiments suggested a single preferred balanced operating point

\[
\\alpha=0.25.
]

The multi-seed analysis instead supports a more robust two-regime structure:

\[
\\boxed{
\\text{responsive adaptive regime}
\\leftrightarrow
\\text{safety-adaptive regime}.
}
]

The responsive regime is represented by direct-loss control.

The safety-adaptive regime is represented by two-stage (1.00).

Intermediate policies can remain useful, but their Pareto status is less
stable across partitions.

## Methodological Conclusion

The experiment demonstrates why operating-point selection must be validated
across independent realizations.

A policy selected from one deterministic partition may appear Pareto-optimal or
geometrically preferred without maintaining that status under resampling.

Therefore future persistence-policy claims should report:

\[
E\[R],
]

\[
\\operatorname{Var}(R),
]

Pareto frequency,

safety-event distributions,

and responsiveness distributions across multiple realizations.

Single-split optimality is insufficient evidence for robust controller
selection.

## Principal Conclusion

Experiment 063 does not confirm

\[
\\alpha=0.25
]

as a uniquely robust balanced operating point.

Instead, two policies remained Pareto-efficient across all 10 randomized
partitions:

\[
\\boxed{
\\text{direct-loss control}
}
]

and

\[
\\boxed{
\\text{two-stage risk control at }\\alpha=1.00.
}
]

Direct loss provides robust responsiveness with

\[
\\overline{H}=0.944,
]

while two-stage (1.00) provides robust safety with mean under-persistence

\[
1.10.
]

Fixed maximal persistence was never Pareto-efficient and produced worse mean
regret than every tested learned adaptive policy.

The robust persistence problem therefore appears to contain a genuine
safety-responsiveness frontier rather than one universally optimal multiplier.

## Limitation

The randomized seeds in Experiment 063 change the train-test partition of the
existing

\[
249
]

decision contexts.

They do not yet generate independent underlying trajectory populations.

Thus the results establish **partition robustness**, not full generative
robustness.

This distinction should be preserved in subsequent interpretation.

## Next Research Direction

Experiment 064 should extend robustness analysis from randomized partitioning to
**independent trajectory realizations**.

Each seed should regenerate the underlying dynamical trajectories before model
training and persistence-policy evaluation.

The experiment should determine whether the robust frontier between

\[
\\text{direct loss}
]

and

\[
\\text{two-stage }1.00
]

survives changes in the actual simulated evidence population.

Metrics should include:

* mean and variance of regret,
* under-persistence distributions,
* over-persistence distributions,
* entropy distributions,
* Pareto-efficiency frequency,
* fixed-(k=3) robustness,
* policy-rank stability.

The central question becomes

\[
\\boxed{
\\text{Does the safety-responsiveness frontier persist across independently
generated system realizations?}
]

