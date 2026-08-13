# Experiment 060 — Responsiveness-Preserving Safe Persistence Control

## Objective

Determine whether low persistence-control regret can be maintained without
collapsing the adaptive controller toward one maximally conservative action.

Experiments 056 through 059 demonstrated that stronger risk sensitivity can
substantially reduce under-persistence regret.

However, sufficiently strong risk penalties eventually reproduce fixed

\[
k=3,
]

eliminating adaptive responsiveness.

Experiment 060 therefore evaluates persistence policies using both safety and
adaptivity metrics.

In addition to mean regret and under-persistence frequency, the experiment
measures:

* normalized persistence-action entropy,
* dominant-action concentration,
* deviation from the unpenalized direct-loss controller,
* over-persistence frequency.

The central question is

\[
\\boxed{
\\text{How much adaptive variation can be preserved while maintaining low
under-persistence risk?}
}
]

## Experimental Partition

The analysis used

\[
249
]

decision contexts.

The deterministic partition contained:

|Partition|Contexts|
|-|-:|
|Training|174|
|Test|75|

Two-stage risk-sensitive policies were evaluated for

\[
\\alpha
\\in
{
0.10,,
0.25,,
0.50,,
0.75,,
1.00,,
1.25,,
1.50,,
2.00
}.
]

## Responsiveness Metrics

Policy responsiveness was quantified using normalized action entropy

\[
H\_{\\text{norm}}
===

\\frac{
-\\sum\_k p\_k\\log p\_k
}{
\\log 3
},
]

where

\[
p\_k
]

is the empirical frequency of persistence action (k).

A policy selecting only one action has

\[
H\_{\\text{norm}}=0.
]

A more heterogeneous policy has higher entropy.

Dominant-action concentration was defined as

\[
D
===

\\max\_k p\_k.
]

Thus high entropy and low dominant-action concentration indicate greater
adaptive variation.

## Principal Results

|Policy|Mean regret|Zero regret|Under|Over|Entropy|Dominant action|Deviation from direct|
|-|-:|-:|-:|-:|-:|-:|-:|
|Fixed (k=1)|0.025602|53.333%|35|0|0.000|100.000%|85.333%|
|Fixed (k=2)|0.005820|84.000%|10|40|0.000|100.000%|58.667%|
|Fixed (k=3)|**0.000300**|**96.000%**|**0**|65|0.000|100.000%|56.000%|
|Direct loss|0.003988|86.667%|8|44|**0.917**|**44.000%**|0.000%|
|Fixed risk (0.010)|0.001048|94.667%|2|63|0.190|94.667%|50.667%|
|Two stage (0.10)|0.002984|89.333%|6|57|**0.741**|69.333%|25.333%|
|Two stage (0.25)|**0.001048**|**94.667%**|**2**|**61**|**0.364**|**89.333%**|45.333%|
|Two stage (0.50)|0.001048|94.667%|2|62|0.287|92.000%|48.000%|
|Two stage (0.75)|0.001168|93.333%|2|63|0.253|93.333%|49.333%|
|Two stage (1.00)|0.001069|94.667%|**1**|63|0.153|96.000%|52.000%|
|Two stage (1.25)|0.001069|94.667%|**1**|64|0.112|97.333%|53.333%|
|Two stage (1.50)|0.001069|94.667%|**1**|65|0.064|98.667%|54.667%|
|Two stage (2.00)|**0.000300**|**96.000%**|**0**|65|**0.000**|**100.000%**|56.000%|
|Oracle|0.000000|100.000%|0|0|0.883|53.333%|69.333%|

## Unpenalized Adaptive Baseline

The direct-loss controller had the greatest responsiveness among the learned
controllers.

Its normalized entropy was

\[
\\boxed{
0.917,
}
]

and its dominant action represented only

\[
44.000%
]

of decisions.

However, this adaptability came with mean regret

\[
0.003988
]

and

\[
8
]

under-persistence decisions.

Thus unconstrained responsiveness produces materially greater safety risk.

## Fixed-Risk Baseline

The globally tuned risk-sensitive controller achieved

\[
\\text{mean regret}=0.001048
]

with only

\[
2
]

under-persistence decisions.

However, its action entropy fell to

\[
0.190,
]

and one action dominated

\[
94.667%
]

of decisions.

Therefore the fixed-risk controller obtains safety partly by suppressing
adaptive action diversity.

## Two-Stage Policy at (\\alpha=0.25)

The strongest responsiveness-preserving result occurred at

\[
\\boxed{
\\alpha=0.25.
}
]

This policy achieved exactly the same mean regret as the fixed-risk controller:

\[
\\boxed{
0.001048.
}
]

It also preserved the same:

\[
94.667%
]

zero-regret rate and

\[
2
]

under-persistence events.

However, its entropy increased from

\[
0.190
]

to

\[
\\boxed{
0.364.
}
]

Dominant-action concentration decreased from

\[
94.667%
]

to

\[
\\boxed{
89.333%.
}
]

Over-persistence decisions also decreased from

\[
63
]

to

\[
61.
]

Thus the two-stage adaptive-risk controller preserved the safety performance of
the fixed-risk controller while maintaining substantially greater action
heterogeneity.

## Responsiveness Improvement at Equal Regret

Comparing the two policies with identical mean regret:

\[
R\_{\\text{fixed}}
===

# R\_{\\text{two-stage}}

0.001048,
]

the entropy increase was

\[
0.364-0.190
===

\\boxed{
0.174.
}
]

This corresponds to an approximate relative entropy increase of

\[
\\boxed{
91.6%.
}
]

Thus two-stage state-dependent risk nearly doubled normalized action entropy at
the same average regret.

This is direct evidence that context-dependent risk information can preserve
adaptivity without sacrificing safety.

## Intermediate Responsiveness Regime

At

\[
\\alpha=0.10,
]

the two-stage policy retained substantially greater responsiveness:

\[
H\_{\\text{norm}}
===

0.741.
]

Its dominant action represented only

\[
69.333%
]

of decisions.

However, mean regret increased to

\[
0.002984,
]

and under-persistence count rose to

\[
6.
]

This demonstrates a genuine safety-responsiveness tradeoff.

Reducing conservatism restores adaptive diversity, but eventually exposes the
controller to the high-cost under-persistence mode identified in Experiment
055.

## Stronger Risk Sensitivity

As (\\alpha) increased beyond (0.25), entropy progressively declined:

\[
0.287,
\\quad
0.253,
\\quad
0.153,
\\quad
0.112,
\\quad
0.064,
\\quad
0.000.
]

At the same time, dominant-action concentration increased toward

\[
100%.
]

This provides a quantitative measure of adaptive-policy collapse.

The controller becomes progressively safer against under-persistence by
sacrificing state-dependent action diversity.

## Near-Zero Under-Persistence Regime

At

\[
\\alpha=1.00,
]

the controller produced only

\[
\\boxed{
1
}
]

under-persistence decision.

Mean regret remained low:

\[
0.001069.
]

However, entropy had fallen to

\[
0.153,
]

with one persistence action selected in

\[
96.000%
]

of contexts.

Thus very strong protection against premature release is possible before
complete collapse, but the remaining policy heterogeneity is limited.

## Complete Policy Collapse

At

\[
\\alpha=2.00,
]

the two-stage controller produced:

\[
\\text{mean regret}=0.000300,
]

\[
\\text{under}=0,
]

\[
\\text{over}=65,
]

\[
H\_{\\text{norm}}=0,
]

and

\[
D=100%.
]

These values exactly match fixed

\[
k=3.
]

Therefore

\[
\\boxed{
\\alpha=2.00
}
]

represents complete adaptive-policy collapse.

Its excellent regret is achieved by abandoning state-dependent persistence
control.

## Safety-Responsiveness Geometry

Experiment 060 reveals a continuum:

\[
\\boxed{
\\text{high responsiveness}
\\rightarrow
\\text{balanced adaptive safety}
\\rightarrow
\\text{conservative collapse}.
}
]

The direct-loss policy occupies the responsive extreme.

Fixed (k=3) occupies the maximally conservative extreme.

The two-stage controller at

\[
\\alpha=0.25
]

occupies a useful intermediate region in which low regret is maintained without
complete concentration on one persistence action.

This suggests that persistence-control optimization is inherently
multi-objective.

## Decision-Theoretic Formulation

The appropriate objective is no longer simply

\[
\\min\_\\pi
\\mathbb{E}\[R].
]

A more complete formulation is

\[
\\min\_\\pi
\\mathbb{E}\[R]
]

subject to

\[
P(\\hat{k}<k^\\star)
\\leq
\\epsilon,
]

while maximizing some responsiveness measure

\[
\\mathcal{H}(\\pi).
]

Equivalently, a composite objective may be written as

\[
J(\\pi)
===

\\mathbb{E}\[R]
+
\\lambda\_s
C\_{\\text{safety}}
---

\\lambda\_h
H\_{\\text{norm}}(\\pi).
]

This explicitly recognizes that a trivial fixed conservative policy should not
be considered equivalent to a genuinely adaptive safe controller.

## Principal Conclusion

Experiment 060 establishes that persistence safety and adaptive responsiveness
can be measured separately and optimized jointly.

The two-stage controller at

\[
\\alpha=0.25
]

matched the fixed-risk controller's mean regret of

\[
0.001048
]

while nearly doubling normalized action entropy and reducing
over-persistence.

This demonstrates that state-dependent risk modeling can preserve meaningful
adaptivity without sacrificing average safety performance.

At higher risk multipliers, entropy progressively collapsed toward zero,
culminating in exact reproduction of fixed (k=3).

Therefore future persistence controllers should explicitly optimize the
**safe-responsiveness frontier**, rather than selecting policies solely by
minimum regret.

## Next Research Direction

Experiment 061 should construct an explicit **Pareto analysis of safety,
regret, and responsiveness**.

Candidate policies should be compared in the multi-objective space

\[
(
\\mathbb{E}\[R],
,
N\_{\\text{under}},
,
H\_{\\text{norm}},
,
N\_{\\text{over}}
).
]

The analysis should identify non-dominated policies rather than reducing all
criteria to one scalar objective prematurely.

Importantly, oracle and fixed policies should be reported as reference
benchmarks rather than allowed to trivialize the adaptive-policy frontier.

Experiment 061 should identify:

* Pareto-efficient adaptive policies,
* the knee point between responsiveness and safety,
* regret-equivalent policies with different entropy,
* minimum-risk policies before collapse,
* the marginal responsiveness cost of eliminating each additional
under-persistence event.

The central question becomes

\[
\\boxed{
\\text{Where is the efficient operating region of adaptive persistence
control?}
]

