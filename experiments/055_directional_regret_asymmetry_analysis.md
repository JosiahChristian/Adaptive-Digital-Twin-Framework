# Experiment 055 — Directional Regret Asymmetry Analysis

## Objective

Determine whether persistence-control errors exhibit directional asymmetry.

Experiment 054 showed that direct per-action loss prediction substantially
reduced regret relative to exact-label persistence classification and shifted
the learned controller toward stronger persistence.

This suggested that errors toward insufficient persistence may be systematically
more costly than errors toward excessive persistence.

Experiment 055 therefore evaluates the full counterfactual persistence-action
space.

For every decision context and every candidate action

\[
k\in\{1,2,3\},
\]

regret is defined as

\[
R(k)
=
L(k)-L(k^\star),
\]

where \(k^\star\) is the true minimum-loss persistence action.

Non-optimal decisions are divided into:

\[
k<k^\star
\]

for insufficient persistence, and

\[
k>k^\star
\]

for excessive persistence.

## Experimental Scope

The analysis contained

\[
249
\]

decision contexts.

All three persistence actions were evaluated in every context, producing

\[
249\times 3
=
747
\]

counterfactual action decisions.

The resulting directional distribution was:

| Decision direction | Count | Fraction |
|---|---:|---:|
| Insufficient persistence | 92 | 12.316% |
| Excessive persistence | 406 | 54.351% |
| Optimal | 249 | 33.333% |

## Directional Regret Summary

| Direction | \(n\) | Mean regret | Median regret | Max regret | Positive regret | Regret \(>0.005\) |
|---|---:|---:|---:|---:|---:|---:|
| Insufficient persistence | 92 | **0.052757** | **0.056018** | 0.103023 | **100.000%** | **98.913%** |
| Excessive persistence | 406 | 0.007824 | 0.000000 | 0.188204 | 15.025% | 14.532% |
| Optimal | 249 | 0.000000 | 0.000000 | 0.000000 | 0.000% | 0.000% |

The directional difference is substantial.

Mean regret under insufficient persistence was

\[
0.052757,
\]

compared with

\[
0.007824
\]

for excessive persistence.

The resulting mean-regret asymmetry ratio is approximately

\[
\boxed{
\frac{0.052757}{0.007824}
=
6.743.
}
\]

Thus insufficient persistence produced approximately 6.7 times greater average
regret than excessive persistence.

## Consequential-Regret Asymmetry

The asymmetry becomes even stronger when only materially consequential errors
are considered.

For insufficient persistence,

\[
98.913\%
\]

of decisions produced regret greater than

\[
0.005.
\]

For excessive persistence, the corresponding fraction was only

\[
14.532\%.
\]

Therefore nearly every insufficient-persistence error was consequential, while
most excessive-persistence errors were effectively harmless.

This establishes that persistence-control mistakes cannot be treated as
directionally symmetric.

## Action-Pair Regret

Pairwise counterfactual regret was:

| Optimal action | Selected action | \(n\) | Mean regret | Median regret | Max regret | Regret \(>0.005\) |
|---:|---:|---:|---:|---:|---:|---:|
| \(k^\*=1\) | \(k=2\) | 172 | 0.008748 | 0.000000 | 0.188204 | 17.442% |
| \(k^\*=1\) | \(k=3\) | 172 | 0.009680 | 0.000000 | 0.188204 | 16.279% |
| \(k^\*=2\) | \(k=1\) | 62 | **0.057615** | **0.060571** | 0.103023 | **100.000%** |
| \(k^\*=2\) | \(k=3\) | 62 | **0.000111** | 0.000000 | 0.006872 | **1.613%** |
| \(k^\*=3\) | \(k=1\) | 15 | 0.046044 | 0.056052 | 0.088454 | 93.333% |
| \(k^\*=3\) | \(k=2\) | 15 | 0.039388 | 0.037813 | 0.069609 | 100.000% |

The most revealing comparison occurs when

\[
k^\star=2.
\]

Selecting insufficient persistence,

\[
k=1,
\]

produced mean regret

\[
\boxed{
0.057615.
}
\]

Selecting excessive persistence,

\[
k=3,
\]

produced mean regret of only

\[
\boxed{
0.000111.
}
\]

Thus moving one persistence level downward from the optimum was highly costly,
while moving one persistence level upward was almost always utility-equivalent.

This is direct evidence of directional action-cost asymmetry.

## Strong-Persistence Contexts

When the true optimal action was

\[
k^\star=3,
\]

both downward errors were costly.

Choosing

\[
k=1
\]

produced mean regret

\[
0.046044,
\]

while choosing

\[
k=2
\]

produced mean regret

\[
0.039388.
\]

Both error types had positive regret in

\[
100\%
\]

of evaluated cases.

Thus when the system genuinely requires strong persistence, reducing
confirmation depth carries a consistently meaningful penalty.

## Regret by Optimal Persistence

Aggregating all non-optimal alternatives by true optimal persistence produced:

| True optimum | Non-optimal actions | Mean regret | Median regret | Max regret | Positive regret | Regret \(>0.005\) |
|---:|---:|---:|---:|---:|---:|---:|
| \(k^\*=1\) | 344 | 0.009214 | 0.000000 | 0.188204 | 17.442% | 16.860% |
| \(k^\*=2\) | 124 | 0.028863 | 0.007517 | 0.103023 | 50.806% | 50.806% |
| \(k^\*=3\) | 30 | **0.042716** | **0.038118** | 0.088454 | **100.000%** | **96.667%** |

The cost of selecting the wrong persistence action therefore increases strongly
with the persistence level actually required by the system.

When

\[
k^\star=1,
\]

most stronger-persistence alternatives are harmless.

When

\[
k^\star=3,
\]

nearly every weaker-persistence alternative is consequential.

## Structural Interpretation

Experiment 055 establishes that the persistence-action space is fundamentally
asymmetric.

The system exhibits the pattern

\[
\boxed{
\text{insufficient persistence}
\gg
\text{excessive persistence}
}
\]

in expected regret.

Excess retention is often utility-equivalent to the nominal optimum.

Premature release, in contrast, frequently destroys useful epistemic memory
before sufficient evidence exists to justify forgetting.

This explains the strong performance of fixed \(k=3\) observed in Experiments
053 and 054.

Strong persistence is frequently not the nominal optimal label, yet it usually
lies within a low-regret region of the action-value surface.

The reverse is not true.

Choosing weak persistence when stronger confirmation is required produces large
and systematic regret.

## Decision-Theoretic Consequence

A persistence controller should therefore not use a symmetric loss function.

The cost structure should distinguish between

\[
C(k<k^\star)
\]

and

\[
C(k>k^\star).
\]

The experimental evidence implies

\[
\boxed{
C(k<k^\star)
>
C(k>k^\star)
}
\]

over the current operating regime.

This motivates an asymmetric persistence objective in which premature release
receives substantially greater penalty than excess retention.

Such an objective would align the learner with the actual consequences of
persistence errors rather than nominal action-label distance.

## Principal Conclusion

Experiment 055 confirms a strong directional asymmetry in persistence-control
regret.

Insufficient persistence produced approximately

\[
\boxed{
6.7\times
}
\]

the mean regret of excessive persistence.

Nearly

\[
99\%
\]

of insufficient-persistence decisions generated consequential regret, compared
with approximately

\[
14.5\%
\]

of excessive-persistence decisions.

The asymmetry is particularly pronounced when the optimal persistence is
moderate or strong.

Therefore premature memory release represents a substantially greater control
risk than excess memory retention.

The persistence controller should consequently become explicitly
risk-sensitive and directionally cost-aware.

## Next Research Direction

Experiment 056 should construct an **asymmetric risk-sensitive persistence
controller**.

Rather than minimizing predicted mean loss alone, the controller should include
a directional risk penalty of the form

\[
J(k\mid x)
=
\hat{L}(k\mid x)
+
\lambda
\hat{R}_{\text{under}}(k\mid x),
\]

where

\[
\hat{R}_{\text{under}}
\]

represents estimated risk associated with selecting insufficient persistence.

Candidate architectures should compare:

- direct mean-loss minimization,
- asymmetric cost-sensitive loss prediction,
- conservative persistence bias,
- regret-penalized action selection,
- oracle control.

Evaluation should determine whether directional risk sensitivity can reduce
high-regret premature-release events without introducing substantial excess
retention cost.

The central objective becomes

\[
\boxed{
\text{minimize catastrophic under-persistence while preserving adaptive
release responsiveness}.
}
\]
