# Experiment 061 — Pareto Safety, Regret, and Responsiveness Analysis

## Objective

Identify the efficient operating region of adaptive persistence control when
safety, regret, and responsiveness are treated as distinct objectives.

Experiment 060 demonstrated that minimizing regret alone can drive the
risk-sensitive controller toward fixed maximal persistence.

Although such policies are safe in the current regime, they can lose the
state-dependent responsiveness that motivates adaptive persistence control.

Experiment 061 therefore evaluates candidate adaptive policies in the
multi-objective space

\[
\\left(
\\mathbb{E}\[R],
N\_{\\text{under}},
N\_{\\text{over}},
H\_{\\text{norm}}
\\right),
]

where:

* (\\mathbb{E}\[R]) is mean persistence regret,
* (N\_{\\text{under}}) is the number of under-persistence decisions,
* (N\_{\\text{over}}) is the number of over-persistence decisions,
* (H\_{\\text{norm}}) is normalized persistence-action entropy.

The objective is to identify non-dominated adaptive policies rather than
prematurely reducing these quantities to a single scalar objective.

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

Adaptive candidates included:

* direct-loss persistence control,
* fixed-risk adaptive control,
* two-stage risk-sensitive control across the established multiplier sweep.

Fixed persistence policies and the oracle were retained as reference
benchmarks.

## Pareto Dominance

Policy (A) dominates policy (B) when (A) is no worse in all evaluated
objectives and strictly better in at least one.

For minimization objectives,

\[
R\_A\\leq R\_B,
]

\[
N\_{\\text{under},A}
\\leq
N\_{\\text{under},B},
]

and

\[
N\_{\\text{over},A}
\\leq
N\_{\\text{over},B}.
]

For responsiveness,

\[
H\_A\\geq H\_B.
]

A policy is Pareto-efficient if no other adaptive candidate dominates it under
these criteria.

## Pareto-Efficient Adaptive Policies

The identified adaptive Pareto frontier was:

|Policy|Mean regret|Under|Over|Entropy|Dominant action|
|-|-:|-:|-:|-:|-:|
|Two stage (2.00)|**0.000300**|**0**|65|0.000|100.000%|
|Two stage (1.00)|0.001069|**1**|63|0.153|96.000%|
|Two stage (0.25)|**0.001048**|2|**61**|**0.364**|89.333%|
|Two stage (0.10)|0.002984|6|57|0.741|69.333%|
|Direct loss|0.003988|8|**44**|**0.917**|44.000%|

The frontier exhibits a clear progression from maximum safety to maximum
responsiveness.

## Safety–Responsiveness Continuum

The adaptive frontier can be interpreted as

\[
\\boxed{
\\text{collapsed safety}
\\rightarrow
\\text{strong safety}
\\rightarrow
\\text{balanced adaptation}
\\rightarrow
\\text{high responsiveness}.
}
]

At one extreme, two-stage (2.00) achieves the lowest adaptive regret and zero
under-persistence events but has

\[
H\_{\\text{norm}}=0,
]

meaning the policy has completely collapsed to one persistence action.

At the opposite extreme, direct-loss control has

\[
H\_{\\text{norm}}=0.917,
]

but incurs

\[
8
]

under-persistence events and substantially higher regret.

The intermediate policies represent genuine tradeoffs rather than uniformly
better or worse controllers.

## Balanced Adaptive Operating Point

The two-stage policy at

\[
\\boxed{
\\alpha=0.25
}
]

remains a particularly important operating point.

It achieves mean regret

\[
0.001048
]

with only

\[
2
]

under-persistence decisions.

Its normalized entropy is

\[
0.364,
]

which is substantially greater than the fixed-risk controller while preserving
the same average regret.

This policy also produces fewer over-persistence decisions than the fixed-risk
baseline.

Thus it occupies a meaningful interior location on the Pareto frontier rather
than either extreme.

## Regret-Equivalent Responsiveness Differences

Several policies achieved identical mean regret while exhibiting materially
different responsiveness.

The strongest comparison is:

\[
\\text{fixed risk }0.010
]

versus

\[
\\text{two stage }0.25.
]

Both achieved

\[
\\boxed{
\\mathbb{E}\[R]=0.001048.
}
]

However, their normalized action entropies were

\[
0.190
]

and

\[
0.364,
]

respectively.

Thus the two-stage controller preserved substantially greater adaptive
variation at the same mean regret.

The two-stage policies at

\[
\\alpha=0.25
]

and

\[
\\alpha=0.50
]

also had identical regret but different entropy:

\[
0.364
]

versus

\[
0.287.
]

Therefore equal regret does not imply equivalent adaptive behavior.

## Safety-Constrained Operating Points

When under-persistence tolerance is constrained, the most responsive feasible
policy changes systematically.

For

\[
N\_{\\text{under}}\\leq 0,
]

only the fully conservative two-stage (2.00) policy satisfies the adaptive
candidate constraint.

For

\[
N\_{\\text{under}}\\leq 1,
]

two-stage (1.00) provides greater responsiveness while retaining very strong
safety.

For

\[
N\_{\\text{under}}\\leq 2,
]

two-stage (0.25) becomes the most responsive feasible candidate.

For

\[
N\_{\\text{under}}\\leq 6,
]

two-stage (0.10) substantially increases policy entropy.

For

\[
N\_{\\text{under}}\\leq 8,
]

the unpenalized direct-loss controller becomes feasible and maximizes adaptive
variation.

This establishes an explicit safety–responsiveness ladder.

## Composite Knee Result

The initial composite knee heuristic selected

\[
\\text{two-stage }2.00.
]

However, this policy has

\[
H\_{\\text{norm}}=0
]

and a 100% dominant-action fraction.

It therefore represents complete policy collapse rather than a meaningful
adaptive knee.

This reveals a limitation of the current scalar knee score.

A simple additive normalization of regret, under-persistence count, and
responsiveness loss can over-reward the safest low-regret extreme.

The knee-selection rule must therefore explicitly penalize or exclude collapsed
policies.

## Methodological Finding

Experiment 061 distinguishes two separate tasks:

\[
\\boxed{
\\text{Pareto-front identification}
}
]

and

\[
\\boxed{
\\text{selection of one preferred operating point}.
}
]

The Pareto-front identification is structurally meaningful because it preserves
the multi-objective tradeoff.

The current scalar knee rule is not yet sufficient because it selected the
fully collapsed policy.

Therefore operating-point selection should not be based on an unconstrained
scalarization without explicit responsiveness protection.

## Structural Interpretation

The adaptive persistence problem now has a well-defined efficient frontier.

Increasing safety progressively reduces both under-persistence frequency and
action entropy.

The sequence

\[
\\alpha=0.10
\\rightarrow
0.25
\\rightarrow
1.00
\\rightarrow
2.00
]

moves the controller from responsive adaptation toward conservative collapse.

No one policy dominates across all objectives.

This means the appropriate persistence policy depends on the acceptable safety
constraint and the value assigned to adaptive responsiveness.

## Principal Conclusion

Experiment 061 identifies a nontrivial Pareto frontier for adaptive persistence
control.

The efficient policies span:

\[
\\text{mean regret}
===

0.000300
\\text{ to }
0.003988,
]

\[
N\_{\\text{under}}
===

0
\\text{ to }
8,
]

and

\[
H\_{\\text{norm}}
===

0
\\text{ to }
0.917.
]

The two-stage (0.25) policy remains a strong balanced operating point because
it achieves low regret and low under-persistence while retaining considerably
more responsiveness than regret-equivalent fixed-risk alternatives.

However, the initial composite knee heuristic incorrectly identifies the
fully collapsed policy as the preferred knee.

Thus the next methodological requirement is a collapse-aware method for
selecting an operating point from the Pareto frontier.

## Next Research Direction

Experiment 062 should construct a **collapse-aware Pareto knee criterion**.

Candidate approaches should explicitly prevent fixed-action or nearly
fixed-action policies from being selected merely because they minimize regret.

Possible formulations include:

\[
H\_{\\text{norm}}
\\geq
H\_{\\min},
]

as an explicit responsiveness constraint,

or a collapse penalty

\[
C\_{\\text{collapse}}
===

D^\\gamma,
]

where (D) is dominant-action concentration.

Another approach is to compute geometric distance to the ideal point only after
normalizing the objectives over the adaptive Pareto frontier and excluding
degenerate entropy-zero endpoints.

Experiment 062 should compare:

* unconstrained scalar knee selection,
* entropy-constrained knee selection,
* dominant-action-constrained selection,
* geometric Pareto knee detection,
* balanced regret-equivalent operating points.

The central question is

\[
\\boxed{
\\text{Which Pareto-efficient controller best balances safety and responsiveness
without collapsing adaptation?}
]

