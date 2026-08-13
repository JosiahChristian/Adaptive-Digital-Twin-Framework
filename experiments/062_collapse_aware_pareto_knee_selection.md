# Experiment 062 — Collapse-Aware Pareto Knee Selection

## Objective

Determine which Pareto-efficient persistence controller provides the most
defensible balance between safety, regret, and adaptive responsiveness without
collapsing to a fixed persistence action.

Experiment 061 identified the adaptive Pareto frontier but showed that a simple
composite scalar knee heuristic could incorrectly select the fully collapsed
maximum-persistence policy.

Experiment 062 therefore evaluates several collapse-aware operating-point
selection methods.

The analyzed objectives are:

\[
\\mathbb{E}\[R],
]

mean persistence regret,

\[
N\_{\\text{under}},
]

under-persistence count,

\[
N\_{\\text{over}},
]

over-persistence count, and

\[
H\_{\\text{norm}},
]

normalized persistence-action entropy.

The principal question is whether independent collapse-aware criteria converge
on the same interior Pareto policy.

## Experimental Partition

The analysis used

\[
249
]

decision contexts.

The deterministic split contained:

|Partition|Contexts|
|-|-:|
|Training|174|
|Test|75|

The Pareto frontier was reconstructed from the previously established adaptive
persistence candidates.

## Pareto Frontier

The adaptive Pareto frontier was:

|Policy|Mean regret|Under|Over|Entropy|Dominant action|
|-|-:|-:|-:|-:|-:|
|Two stage (2.00)|0.000300|0|65|0.000|100.000%|
|Two stage (1.00)|0.001069|1|63|0.153|96.000%|
|Two stage (0.25)|**0.001048**|**2**|**61**|**0.364**|**89.333%**|
|Two stage (0.10)|0.002984|6|57|0.741|69.333%|
|Direct loss|0.003988|8|44|0.917|44.000%|

This frontier again spans the continuum from conservative collapse to highly
responsive adaptation.

## Geometric Ideal-Point Selection

The geometric selection criterion normalizes the Pareto objectives and computes
distance to an ideal point representing:

\[
R=R\_{\\min},
]

\[
N\_{\\text{under}}=N\_{\\text{under,min}},
]

\[
N\_{\\text{over}}=N\_{\\text{over,min}},
]

and maximum responsiveness.

Using all Pareto policies, geometric selection identified

\[
\\boxed{
\\text{two-stage }0.25.
}
]

Its metrics were:

\[
\\mathbb{E}\[R]
===

0.001048,
]

\[
N\_{\\text{under}}
===

2,
]

\[
N\_{\\text{over}}
===

61,
]

\[
H\_{\\text{norm}}
===

0.364.
]

When the fully collapsed policy was explicitly excluded, the geometric method
again selected

\[
\\boxed{
\\text{two-stage }0.25.
}
]

Thus the geometric result is not dependent on whether the entropy-zero endpoint
is retained.

## Entropy-Constrained Selection

Explicit responsiveness constraints were imposed through

\[
H\_{\\text{norm}}
\\geq
H\_{\\min}.
]

For

\[
H\_{\\min}
===

0.10,
]

\[
0.20,
]

and

\[
0.30,
]

the selected policy was consistently

\[
\\boxed{
\\text{two-stage }0.25.
}
]

Only when the minimum entropy requirement increased to

\[
0.40
]

did the preferred policy move to

\[
\\text{two-stage }0.10.
]

The same result persisted at

\[
H\_{\\min}=0.60.
]

This demonstrates a clear threshold structure.

Moderate responsiveness requirements favor the low-regret

\[
\\alpha=0.25
]

policy.

Stronger responsiveness requirements require accepting the greater regret and
under-persistence exposure of

\[
\\alpha=0.10.
]

## Dominant-Action-Constrained Selection

Collapse was also controlled through the dominant-action fraction

\[
D
===

\\max\_k p\_k.
]

For constraints

\[
D\\leq0.99,
]

\[
D\\leq0.95,
]

and

\[
D\\leq0.90,
]

the selected policy was again

\[
\\boxed{
\\text{two-stage }0.25.
}
]

When the policy was required to satisfy

\[
D\\leq0.80,
]

selection shifted to

\[
\\text{two-stage }0.10.
]

The same result occurred for

\[
D\\leq0.70.
]

Thus both entropy-based and dominant-action-based collapse constraints identify
the same transition between the balanced and highly responsive regimes.

## Cross-Criterion Convergence

The most important result of Experiment 062 is convergence across independent
selection methods.

The following methods all selected

\[
\\boxed{
\\text{two-stage }0.25:
}
]

* geometric ideal-point selection,
* geometric selection excluding collapsed policies,
* entropy constraint (H\\geq0.10),
* entropy constraint (H\\geq0.20),
* entropy constraint (H\\geq0.30),
* dominant-action constraint (D\\leq0.99),
* dominant-action constraint (D\\leq0.95),
* dominant-action constraint (D\\leq0.90).

This convergence provides substantially stronger justification for treating
two-stage (0.25) as the preferred balanced adaptive operating point.

Its selection is not an artifact of one arbitrary scalar objective.

## Preferred Interior Operating Point

The convergent policy has

\[
\\boxed{
\\alpha^\\star=0.25.
}
]

Its operating metrics are:

\[
\\boxed{
\\mathbb{E}\[R]=0.001048,
}
]

\[
\\boxed{
N\_{\\text{under}}=2,
}
]

\[
\\boxed{
N\_{\\text{over}}=61,
}
]

\[
\\boxed{
H\_{\\text{norm}}=0.364,
}
]

and

\[
\\boxed{
D=89.333%.
}
]

This policy therefore retains measurable action diversity while preserving the
low-regret and low-under-persistence behavior established by the risk-sensitive
architecture.

## Highly Responsive Alternative

When stronger responsiveness constraints are imposed, selection moves to

\[
\\boxed{
\\text{two-stage }0.10.
}
]

This policy has

\[
H\_{\\text{norm}}=0.741
]

and dominant-action concentration

\[
69.333%.
]

However, mean regret increases to

\[
0.002984,
]

and under-persistence events increase to

\[
6.
]

Thus two-stage (0.10) represents a higher-responsiveness operating regime
rather than a uniformly superior controller.

## Collapsed Safety Endpoint

Two-stage (2.00) remains the minimum-regret adaptive candidate:

\[
\\mathbb{E}\[R]
===

0.000300,
]

with

\[
N\_{\\text{under}}
===

0. 

]

However,

\[
H\_{\\text{norm}}
===

0
]

and

\[
D
===

100%.
]

Therefore this point is best interpreted as a conservative safety endpoint, not
as a preferred adaptive knee.

## Collapse-Penalized Scalarization

The explicit collapse-penalized scalar criterion selected

\[
\\text{direct loss}.
]

This policy has the highest adaptive entropy among the learned policies:

\[
H\_{\\text{norm}}
===

0.917,
]

but also has mean regret

\[
0.003988
]

and

\[
8
]

under-persistence events.

The result indicates that the tested collapse penalty over-corrects the failure
of the original scalar knee score.

The original scalarization favored safety too strongly.

The collapse-penalized version favored responsiveness too strongly.

This reinforces the methodological advantage of explicit Pareto constraints and
geometric multi-objective selection.

## Methodological Finding

Experiment 062 demonstrates that operating-point selection is more robust when
responsiveness is represented as an explicit objective or feasibility
constraint rather than embedded through an arbitrary scalar penalty.

The result supports the hierarchy

\[
\\boxed{
\\text{Pareto frontier}
\\rightarrow
\\text{collapse constraint}
\\rightarrow
\\text{operating-point selection}.
}
]

This preserves the underlying tradeoff structure before introducing a decision
preference.

## Structural Interpretation

The persistence architecture now contains three identifiable operating regimes.

### Conservative safety regime

\[
\\alpha\\approx2.00
]

provides minimal regret but collapses adaptive behavior.

### Balanced adaptive-safe regime

\[
\\boxed{
\\alpha\\approx0.25
}
]

provides low regret, low under-persistence, and meaningful action diversity.

### High-responsiveness regime

\[
\\alpha\\approx0.10
]

provides much greater adaptive variation at the cost of increased regret and
under-persistence exposure.

Thus persistence tuning can now be interpreted in terms of operating regimes
rather than one globally optimal scalar parameter.

## Principal Conclusion

Experiment 062 resolves the knee-selection failure identified in Experiment
061.

Multiple independent collapse-aware criteria converge on

\[
\\boxed{
\\text{two-stage risk-sensitive persistence control with }
\\alpha=0.25.
}
]

This policy achieves:

\[
\\mathbb{E}\[R]
===

0.001048,
]

with only

\[
2
]

under-persistence events while maintaining normalized action entropy

\[
0.364.
]

The convergence of geometric, entropy-constrained, and dominant-action-
constrained methods provides a defensible basis for identifying this policy as
the current preferred balanced operating point.

The result also confirms that extreme safety and extreme responsiveness should
be treated as distinct operating regimes rather than allowed to define the
adaptive optimum automatically.

## Next Research Direction

Experiment 063 should test whether the selected balanced operating point

\[
\\alpha=0.25
]

generalizes beyond the single deterministic train-test partition.

The next experiment should perform a **multi-seed robustness analysis** over
trajectory generation, model fitting, and train-test partitioning.

It should compare at minimum:

* two-stage (0.25),
* two-stage (0.10),
* two-stage (1.00),
* fixed risk (0.010),
* direct-loss control,
* fixed (k=3),
* oracle control.

Metrics should include distributions of:

\[
\\mathbb{E}\[R],
]

\[
N\_{\\text{under}},
]

\[
N\_{\\text{over}},
]

\[
H\_{\\text{norm}},
]

and the frequency with which each candidate remains Pareto-efficient.

The central question becomes

\[
\\boxed{
\\text{Does the balanced adaptive operating point remain preferred across
independent realizations?}
]

