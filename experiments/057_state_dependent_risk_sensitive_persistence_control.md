# Experiment 057 — State-Dependent Risk-Sensitive Persistence Control

## Objective

Determine whether the fixed asymmetric persistence-risk penalty identified in
Experiment 056 can be improved by making risk sensitivity state-dependent.

Experiment 056 demonstrated that an asymmetric under-persistence penalty

\[
\lambda=0.010
\]

substantially reduced adaptive-controller regret.

However, a fixed global penalty assumes that premature-release risk is uniform
across epistemic contexts.

Experiment 057 therefore learns a context-dependent estimate of
under-persistence risk.

For each decision context \(x\), define the true under-persistence risk as the
maximum regret associated with selecting a persistence action below the optimal
level:

\[
C_{\text{under}}(x)
=
\max_{k<k^\star}
\left[
L(k\mid x)-L(k^\star\mid x)
\right].
\]

A regression model estimates

\[
\hat C_{\text{under}}(x),
\]

and persistence actions are selected according to

\[
J(k\mid x)
=
\hat L(k\mid x)
+
\alpha
\hat C_{\text{under}}(x)
(3-k).
\]

The experiment evaluates whether context-dependent risk sensitivity can retain
the protection of conservative persistence while reducing unnecessary
over-persistence.

## Experimental Partition

The dataset contained

\[
249
\]

decision contexts.

The deterministic split produced:

| Partition | Contexts |
|---|---:|
| Training | 174 |
| Test | 75 |

The adaptive risk multipliers were

\[
\alpha
\in
\{0.25,\ 0.50,\ 1.00,\ 1.50,\ 2.00\}.
\]

The fixed-risk benchmark retained the Experiment 056 penalty

\[
\lambda=0.010.
\]

## Under-Persistence Risk Estimator

Risk-estimation performance on the test partition was:

| Metric | Value |
|---|---:|
| Mean true risk | 0.026381 |
| Mean predicted risk | 0.027270 |
| Risk MAE | 0.026030 |
| Positive-risk contexts | 35 |
| Mean true risk on positive contexts | 0.056532 |
| Mean predicted risk on positive contexts | 0.031803 |

The global mean prediction was close to the global mean true risk:

\[
0.027270
\approx
0.026381.
\]

However, this apparent calibration concealed substantial context-level error.

The risk-estimation MAE was

\[
\boxed{
0.026030,
}
\]

which is nearly as large as the mean true risk itself.

More importantly, on contexts in which under-persistence risk was genuinely
positive, the estimator predicted

\[
0.031803
\]

against a true mean of

\[
0.056532.
\]

Thus dangerous contexts were systematically underestimated on average.

## Principal Results

| Policy | Accuracy | Mean loss | Mean regret | Max regret | Zero regret | Regret \(>0.005\) | Under | Over |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fixed \(k=1\) | 53.333% | 0.167709 | 0.025602 | 0.103023 | 53.333% | 46.667% | 35 | 0 |
| Fixed \(k=2\) | 33.333% | 0.147927 | 0.005820 | 0.069609 | 84.000% | 16.000% | 10 | 40 |
| Fixed \(k=3\) | 13.333% | **0.142408** | **0.000300** | **0.008997** | **96.000%** | **4.000%** | **0** | 65 |
| Direct-loss model | 30.667% | 0.146095 | 0.003988 | 0.057718 | 86.667% | 13.333% | 8 | 44 |
| Fixed risk \(0.010\) | 13.333% | **0.143156** | **0.001048** | 0.057718 | **94.667%** | **5.333%** | **2** | 63 |
| Adaptive risk \(0.25\) | 14.667% | 0.143986 | 0.001879 | 0.057718 | 92.000% | 8.000% | 4 | 60 |
| Adaptive risk \(0.50\) | **14.667%** | **0.143156** | **0.001048** | 0.057718 | **94.667%** | **5.333%** | **2** | **62** |
| Adaptive risk \(1.00\) | 13.333% | 0.143275 | 0.001168 | 0.057718 | 93.333% | 6.667% | 2 | 63 |
| Adaptive risk \(1.50\) | 13.333% | 0.143275 | 0.001168 | 0.057718 | 93.333% | 6.667% | 2 | 63 |
| Adaptive risk \(2.00\) | 13.333% | 0.143275 | 0.001168 | 0.057718 | 93.333% | 6.667% | 2 | 63 |
| Oracle | 100.000% | 0.142108 | 0.000000 | 0.000000 | 100.000% | 0.000% | 0 | 0 |

## Best Adaptive Risk Policy

The best state-dependent policy occurred at

\[
\boxed{
\alpha=0.50.
}
\]

It achieved mean regret

\[
\boxed{
0.001048,
}
\]

exactly matching the best fixed-risk policy from Experiment 056.

Its zero-regret fraction was

\[
94.667\%,
\]

and consequential-regret frequency was

\[
5.333\%.
\]

It also produced only

\[
2
\]

under-persistence decisions.

Thus state-dependent risk sensitivity successfully reproduced the protection of
the globally tuned risk-sensitive controller.

## Reduction in Conservatism

Although adaptive risk did not reduce mean regret below the fixed-risk
benchmark, it achieved the same utility performance with slightly less
over-persistence.

The fixed-risk controller produced

\[
63
\]

over-persistence decisions.

The adaptive \(\alpha=0.50\) controller produced

\[
62.
\]

Its nominal action accuracy also increased from

\[
13.333\%
\]

to

\[
14.667\%.
\]

The difference is small, but it establishes that context-dependent risk
modulation can preserve the same regret level without being strictly identical
to the fixed conservative controller.

## Risk-Multiplier Behavior

The adaptive sweep produced mean regrets:

\[
\alpha=0.25:
\quad
0.001879,
\]

\[
\alpha=0.50:
\quad
0.001048,
\]

\[
\alpha=1.00:
\quad
0.001168,
\]

\[
\alpha=1.50:
\quad
0.001168,
\]

\[
\alpha=2.00:
\quad
0.001168.
\]

The best result therefore occurs at an intermediate multiplier rather than at
maximum risk sensitivity.

This again demonstrates that persistence conservatism has a finite useful
operating region.

## Comparison with Direct-Loss Control

The direct-loss controller achieved mean regret

\[
0.003988.
\]

The best adaptive-risk controller achieved

\[
0.001048.
\]

This corresponds to a regret reduction of approximately

\[
\boxed{
73.7\%.
}
\]

Under-persistence decisions fell from

\[
8
\]

to

\[
2,
\]

while zero-regret performance increased from

\[
86.667\%
\]

to

\[
94.667\%.
\]

Therefore learned risk modulation retains the major benefit established by the
fixed asymmetric penalty.

## Risk-Estimation Bottleneck

The adaptive controller did not outperform the fixed-risk benchmark.

The principal limitation appears to be the learned risk estimator.

Although its aggregate mean was well calibrated, its context-level MAE was
large:

\[
0.026030.
\]

Furthermore, on genuinely dangerous contexts it underestimated average risk by

\[
0.056532-0.031803
=
\boxed{
0.024729.
}
\]

Thus the controller is receiving an attenuated risk signal precisely in the
states where under-persistence protection matters most.

This suggests that the next performance bottleneck is no longer the
risk-sensitive decision rule.

It is **risk-state identification and calibration**.

## Structural Interpretation

Experiment 057 establishes that under-persistence risk is in principle usable
as a state-dependent control signal.

A learned risk function can reproduce the utility performance of the best fixed
risk penalty while modestly reducing excess persistence.

However, ordinary regression does not yet separate dangerous contexts sharply
enough to improve beyond the globally tuned policy.

The problem has therefore evolved from

\[
\text{which persistence action is best?}
\]

to

\[
\text{where is insufficient persistence actually dangerous?}
\]

This is a risk-detection problem rather than merely a loss-regression problem.

## Principal Conclusion

State-dependent risk sensitivity matched the best fixed asymmetric controller
but did not outperform it.

The best adaptive multiplier,

\[
\alpha=0.50,
\]

achieved

\[
\boxed{
\text{mean regret}=0.001048
}
\]

with only two under-persistence decisions and a 94.667% zero-regret rate.

It also produced one fewer over-persistence decision than the fixed-risk
controller.

However, the learned under-persistence risk estimator substantially
underestimated risk in positive-risk contexts.

Therefore the current limitation is best characterized as

\[
\boxed{
\text{risk estimation}
>
\text{risk-sensitive control}
}
\]

in terms of where further architectural improvement is required.

## Next Research Direction

Experiment 058 should improve under-persistence risk identification using a
two-stage or hurdle-style architecture.

Rather than regressing risk magnitude directly across a dataset dominated by
zero-risk contexts, the model should separately estimate

\[
P(C_{\text{under}}>0\mid x)
\]

and

\[
E[
C_{\text{under}}
\mid
C_{\text{under}}>0,x
].
\]

The resulting expected risk can be formed as

\[
\hat C_{\text{under}}(x)
=
\hat P_{\text{risk}}(x)
\,
\hat M_{\text{risk}}(x).
\]

Experiment 058 should compare:

- single-stage risk regression,
- binary positive-risk classification,
- conditional positive-risk magnitude regression,
- two-stage expected-risk estimation,
- fixed global risk sensitivity,
- oracle persistence control.

The key question is whether separating **risk occurrence** from **risk
magnitude** improves identification of the high-cost states that the current
regressor systematically underestimates.
