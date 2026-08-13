# Experiment 058 — Two-Stage Under-Persistence Risk Estimation

## Objective

Improve identification and estimation of dangerous under-persistence contexts
by separating risk occurrence from risk magnitude.

Experiment 057 showed that state-dependent risk-sensitive persistence control
could match the best fixed-risk policy, but its single-stage risk estimator
substantially underestimated risk in genuinely dangerous contexts.

Experiment 058 therefore introduces a two-stage risk architecture.

The first stage estimates

\[
P(C\_{\\text{under}}>0\\mid x),
]

where (C\_{\\text{under}}) is the regret associated with insufficient
persistence.

The second stage estimates conditional positive-risk magnitude:

\[
E\[
C\_{\\text{under}}
\\mid
C\_{\\text{under}}>0,x
].
]

These quantities are combined as

\[
\\hat C\_{\\text{under}}(x)
===

\\hat P\_{\\text{risk}}(x)
\\hat M\_{\\text{risk}}(x).
]

The objective is to determine whether separating risk occurrence from severity
improves risk-state estimation relative to ordinary single-stage regression.

## Experimental Partition

The analysis contained

\[
249
]

decision contexts.

The deterministic split produced:

|Partition|Contexts|
|-|-:|
|Training|174|
|Test|75|

Among the 75 test contexts,

\[
35
]

contained positive under-persistence risk.

## Risk Occurrence Model

The binary positive-risk classifier achieved:

|Metric|Value|
|-|-:|
|Accuracy|80.000%|
|Precision|76.316%|
|Recall|82.857%|
|True positive-risk contexts|35|
|Predicted positive-risk contexts|38|

The occurrence model therefore detected the majority of dangerous contexts.

Its recall was

\[
\\boxed{
82.857%
}
]

indicating that approximately five out of six positive-risk contexts were
identified by the classifier.

Precision was

\[
76.316%.
]

Thus the model introduced some conservative false positives, but avoided the
more consequential failure mode of systematically missing dangerous states.

## Single-Stage Risk Regression

The original single-stage estimator produced:

|Metric|Value|
|-|-:|
|Mean true risk|0.026381|
|Mean predicted risk|0.027270|
|Overall risk MAE|0.026030|
|Positive-risk MAE|0.029146|
|Mean true positive risk|0.056532|
|Mean predicted positive risk|0.031803|

Although aggregate mean calibration was close,

\[
0.027270
\\approx
0.026381,
]

the model substantially underestimated risk on the contexts where risk was
actually present.

The positive-risk underestimation was

\[
0.056532-0.031803
===

0.024729.
]

## Two-Stage Expected-Risk Estimation

The two-stage architecture produced:

|Metric|Value|
|-|-:|
|Mean true risk|0.026381|
|Mean predicted risk|0.033166|
|Overall risk MAE|**0.025294**|
|Positive-risk MAE|**0.025367**|
|Mean true positive risk|0.056532|
|Mean predicted positive risk|**0.042234**|

The two-stage estimator reduced overall MAE from

\[
0.026030
]

to

\[
0.025294.
]

More importantly, positive-risk MAE decreased from

\[
0.029146
]

to

\[
\\boxed{
0.025367.
}
]

This is an improvement of approximately

\[
13.0%.
]

## Improved Positive-Risk Calibration

The most important change occurred on genuinely dangerous contexts.

The single-stage estimator predicted mean positive risk

\[
0.031803.
]

The two-stage estimator increased this to

\[
0.042234.
]

The true mean was

\[
0.056532.
]

Thus the positive-risk estimation gap decreased from

\[
0.024729
]

to

\[
0.014298.
]

This corresponds to an approximate reduction in mean positive-risk
underestimation of

\[
\\boxed{
42.2%.
}
]

The two-stage structure therefore substantially reduced the attenuation of the
risk signal that limited Experiment 057.

## Conditional Risk Magnitude

The positive-risk magnitude model produced a mean predicted conditional
magnitude of

\[
\\boxed{
0.068045.
}
]

This value is higher than the unconditional true positive-risk mean because the
final expected-risk estimate also incorporates the probability that a context
actually belongs to the positive-risk regime.

The resulting two-stage estimate

\[
\\hat C\_{\\text{under}}(x)
===

\\hat P\_{\\text{risk}}(x)
\\hat M\_{\\text{risk}}(x)
]

therefore combines conservative magnitude estimation with uncertainty about
whether the dangerous regime is active.

## Interpretation

Experiment 058 confirms that under-persistence risk has a hurdle-like
structure.

Many contexts have effectively zero risk, while a smaller subset exhibits
substantial under-persistence cost.

A single regression model must simultaneously represent both regimes and tends
to regress dangerous contexts toward the dominant low-risk population.

Separating the problem into

\[
\\text{risk occurrence}
]

and

\[
\\text{risk severity}
]

reduces this attenuation.

The two-stage estimator improves positive-risk calibration while preserving
reasonable aggregate accuracy.

## Structural Finding

The results support the decomposition

\[
\\boxed{
\\text{under-persistence risk}
===

\\text{probability of danger}
\\times
\\text{severity if dangerous}.
}
]

This representation is more informative than treating risk as one continuous
target across all contexts.

The occurrence model answers

\[
\\text{Is this state dangerous?}
]

while the magnitude model answers

\[
\\text{How costly would under-persistence be if it is dangerous?}
]

This decomposition directly matches the asymmetric control structure developed
through Experiments 055–057.

## Principal Conclusion

Experiment 058 improves estimation of under-persistence risk using a two-stage
architecture.

The risk-occurrence model achieved

\[
82.857%
]

recall, while the two-stage expected-risk estimator reduced positive-risk MAE
from

\[
0.029146
]

to

\[
0.025367.
]

It also reduced mean positive-risk underestimation by approximately

\[
42.2%.
]

Therefore separating risk occurrence from risk magnitude provides a stronger
risk signal than single-stage regression.

However, the current run establishes an estimation improvement only.

It does not yet establish that the improved risk estimate yields lower
closed-loop persistence-control regret.

## Next Research Direction

Experiment 059 should integrate the two-stage expected-risk estimator directly
into the asymmetric persistence controller.

The controller should compare

\[
J\_{\\text{single}}(k\\mid x)
===

\\hat L(k\\mid x)
+
\\alpha
\\hat C\_{\\text{single}}(x)
(3-k)
]

with

\[
J\_{\\text{two-stage}}(k\\mid x)
===

\\hat L(k\\mid x)
+
\\alpha
\\hat C\_{\\text{two-stage}}(x)
(3-k).
]

Experiment 059 should evaluate:

* direct loss minimization,
* fixed global risk sensitivity,
* single-stage adaptive risk control,
* two-stage adaptive risk control,
* fixed strong persistence,
* oracle control.

The principal question is whether the improved detection and calibration of
dangerous contexts translates into lower regret, fewer under-persistence
events, and less unnecessary over-persistence.

