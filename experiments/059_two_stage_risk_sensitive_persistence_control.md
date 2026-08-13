# Experiment 059 — Two-Stage Risk-Sensitive Persistence Control

## Objective

Determine whether the improved two-stage under-persistence risk estimator from
Experiment 058 translates into improved persistence-control decisions.

Experiment 058 decomposed under-persistence risk into

\[
P(C\_{\\text{under}}>0\\mid x)
]

and

\[
E\[
C\_{\\text{under}}
\\mid
C\_{\\text{under}}>0,x
],
]

forming the expected-risk estimate

\[
\\hat C\_{\\text{under}}(x)
===

\\hat P\_{\\text{risk}}(x)
\\hat M\_{\\text{risk}}(x).
]

Experiment 059 integrates this estimate directly into the persistence-control
objective

\[
J(k\\mid x)
===

\\hat L(k\\mid x)
+
\\alpha
\\hat C\_{\\text{under}}(x)
(3-k).
]

The two-stage controller is compared with direct loss minimization,
single-stage adaptive risk control, fixed global risk sensitivity, fixed
persistence policies, and the oracle.

## Experimental Partition

The analysis used

\[
249
]

decision contexts divided into:

|Partition|Contexts|
|-|-:|
|Training|174|
|Test|75|

Two-stage and single-stage adaptive risk multipliers were evaluated over

\[
\\alpha
\\in
{0.25,\\ 0.50,\\ 0.75,\\ 1.00,\\ 1.50,\\ 2.00}.
]

## Principal Results

|Policy|Accuracy|Mean loss|Mean regret|Max regret|Zero regret|Regret (>0.005)|Under|Over|
|-|-:|-:|-:|-:|-:|-:|-:|-:|
|Fixed (k=1)|53.333%|0.167709|0.025602|0.103023|53.333%|46.667%|35|0|
|Fixed (k=2)|33.333%|0.147927|0.005820|0.069609|84.000%|16.000%|10|40|
|Fixed (k=3)|13.333%|**0.142408**|**0.000300**|**0.008997**|**96.000%**|**4.000%**|**0**|65|
|Direct loss|30.667%|0.146095|0.003988|0.057718|86.667%|13.333%|8|44|
|Fixed risk (0.010)|13.333%|0.143156|0.001048|0.057718|94.667%|5.333%|2|63|
|Single stage (0.25)|14.667%|0.143986|0.001879|0.057718|92.000%|8.000%|4|60|
|Two stage (0.25)|**16.000%**|0.143156|**0.001048**|0.057718|**94.667%**|**5.333%**|**2**|**61**|
|Single stage (0.50)|14.667%|0.143156|0.001048|0.057718|94.667%|5.333%|2|62|
|Two stage (0.50)|14.667%|0.143156|0.001048|0.057718|94.667%|5.333%|2|62|
|Single stage (0.75)|13.333%|0.143275|0.001168|0.057718|93.333%|6.667%|2|63|
|Two stage (0.75)|13.333%|0.143275|0.001168|0.057718|93.333%|6.667%|2|63|
|Single stage (1.00)|13.333%|0.143275|0.001168|0.057718|93.333%|6.667%|2|63|
|Two stage (1.00)|14.667%|0.143177|0.001069|0.057718|94.667%|5.333%|**1**|63|
|Single stage (1.50)|13.333%|0.143275|0.001168|0.057718|93.333%|6.667%|2|63|
|Two stage (1.50)|12.000%|0.143177|0.001069|0.057718|94.667%|5.333%|**1**|65|
|Single stage (2.00)|13.333%|0.143275|0.001168|0.057718|93.333%|6.667%|2|63|
|Two stage (2.00)|13.333%|**0.142408**|**0.000300**|**0.008997**|**96.000%**|**4.000%**|**0**|65|
|Oracle|100.000%|0.142108|0.000000|0.000000|100.000%|0.000%|0|0|

## Two-Stage Improvement at Low Risk Sensitivity

At

\[
\\alpha=0.25,
]

the two-stage controller achieved mean regret

\[
0.001048,
]

compared with

\[
0.001879
]

for the single-stage controller at the same multiplier.

This corresponds to an approximate regret reduction of

\[
\\boxed{
44.2%.
}
]

The two-stage controller also reduced under-persistence events from

\[
4
]

to

\[
2.
]

Thus the improved risk estimate from Experiment 058 translates directly into
better control when risk sensitivity is relatively weak.

## Comparison with Fixed Global Risk

The fixed-risk controller from Experiment 056 achieved

\[
\\text{mean regret}=0.001048,
]

with

\[
2
]

under-persistence events and

\[
63
]

over-persistence events.

The two-stage controller at

\[
\\alpha=0.25
]

achieved exactly the same mean regret,

\[
\\boxed{
0.001048,
}
]

with the same two under-persistence events but only

\[
\\boxed{
61
}
]

over-persistence events.

Its exact action accuracy also increased from

\[
13.333%
]

to

\[
16.000%.
]

Therefore the two-stage risk architecture matched the utility protection of the
globally tuned controller while preserving slightly greater adaptive
responsiveness.

## Near-Elimination of Under-Persistence

At

\[
\\alpha=1.00,
]

the two-stage controller reduced under-persistence errors to

\[
\\boxed{
1
}
]

while maintaining mean regret

\[
0.001069.
]

This differs only slightly from the best non-collapsed result of

\[
0.001048.
]

Thus the two-stage risk signal can nearly eliminate dangerous
under-persistence without immediately forcing every decision toward maximal
retention.

## Conservative Collapse

At

\[
\\alpha=2.00,
]

the two-stage controller achieved

\[
\\text{mean regret}=0.000300,
]

\[
\\text{zero-regret fraction}=96.000%,
]

and

\[
\\text{under-persistence count}=0.
]

These values exactly match fixed

\[
k=3.
]

The action counts likewise correspond to the maximally persistent policy.

Therefore the apparent utility optimum at

\[
\\alpha=2.00
]

is not an adaptive-control improvement.

It represents **policy collapse toward fixed strong persistence**.

This distinction is important.

A controller should not be considered superior merely because a sufficiently
large risk penalty forces it to reproduce the strongest fixed baseline.

## Adaptive-Persistence Tradeoff

Experiment 059 exposes three control regimes.

### Low risk sensitivity

At small (\\alpha), the two-stage estimator improves responsiveness while
reducing under-persistence relative to the single-stage controller.

### Intermediate risk sensitivity

At approximately

\[
\\alpha=1.00,
]

the controller nearly eliminates under-persistence while still retaining some
state-dependent action variation.

### High risk sensitivity

At

\[
\\alpha=2.00,
]

the controller collapses to fixed maximal persistence.

The relevant optimization problem is therefore not simply

\[
\\min \\mathbb{E}\[R].
]

It must also preserve useful adaptive variation.

## Structural Interpretation

The experiments now reveal two competing objectives:

\[
\\boxed{
\\text{risk protection}
}
]

and

\[
\\boxed{
\\text{adaptive responsiveness}.
}
]

A maximally conservative controller can obtain extremely low regret because
excess persistence is usually inexpensive in the current regime.

However, such a controller ceases to exploit context-dependent opportunities
for safe release.

Therefore future controllers must distinguish between beneficial
conservatism and trivial collapse to the safest fixed action.

## Principal Conclusion

Experiment 059 demonstrates that the improved two-stage risk estimator can
translate into improved persistence control.

At low risk sensitivity, the two-stage controller substantially outperformed
the corresponding single-stage policy.

At

\[
\\alpha=0.25,
]

it matched the best fixed-risk regret while reducing unnecessary
over-persistence.

At intermediate risk sensitivity, it reduced under-persistence to a single
event.

At high risk sensitivity, it matched the extremely low regret of fixed
(k=3), but only by collapsing to maximal persistence.

Therefore the next optimization criterion must explicitly account for both
regret and adaptive-policy collapse.

## Next Research Direction

Experiment 060 should introduce a **responsiveness-preserving risk objective**.

The controller should optimize a composite objective such as

\[
J
===

\\mathbb{E}\[R]
+
\\beta
C\_{\\text{collapse}},
]

where

\[
C\_{\\text{collapse}}
]

penalizes excessive concentration on a single persistence action or unnecessary
over-persistence.

Candidate measures include:

* excess-persistence count,
* deviation from the direct-loss action distribution,
* persistence-action entropy,
* safe-release opportunity loss,
* regret subject to an under-persistence constraint.

A particularly useful formulation may be

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

while maximizing policy responsiveness within that safety constraint.

The central question becomes:

\[
\\boxed{
\\text{How adaptive can the persistence controller remain while keeping
premature-release risk acceptably low?}
]

