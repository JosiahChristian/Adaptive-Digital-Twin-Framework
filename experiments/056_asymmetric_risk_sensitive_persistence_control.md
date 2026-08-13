# Experiment 056 — Asymmetric Risk-Sensitive Persistence Control

## Objective

Determine whether the directional regret asymmetry identified in Experiment 055
can be exploited to improve adaptive release-persistence control.

Experiment 055 established that insufficient persistence is substantially more
costly than excessive persistence.

Mean regret under insufficient persistence was approximately 6.7 times greater
than mean regret under excessive persistence, and nearly 99% of
under-persistence decisions produced consequential regret.

Experiment 056 therefore introduces an asymmetric risk-sensitive persistence
objective.

For each candidate persistence action

\[
k\\in{1,2,3},
]

the controller begins with a predicted action loss

\[
\\hat{L}(k\\mid x)
]

and augments it with a conservative directional penalty:

\[
J(k\\mid x)
===

\\hat{L}(k\\mid x)
+
\\lambda(3-k).
]

Lower persistence levels therefore receive larger penalties because premature
release was shown to carry substantially greater downstream risk.

The selected action becomes

\[
\\hat{k}
===

\\arg\\min\_k J(k\\mid x).
]

The experiment evaluates whether increasing directional conservatism reduces
under-persistence regret without introducing excessive retention cost.

## Experimental Partition

The dataset contained

\[
249
]

decision contexts.

The deterministic partition contained:

|Partition|Contexts|
|-|-:|
|Training|174|
|Test|75|

The evaluated under-persistence penalty values were

\[
\\lambda
\\in
{0,\\ 0.002,\\ 0.005,\\ 0.010,\\ 0.020}.
]

## Principal Results

|Policy|Accuracy|Mean loss|Mean regret|Max regret|Zero regret|Regret (>0.005)|Under|Over|
|-|-:|-:|-:|-:|-:|-:|-:|-:|
|Fixed (k=1)|53.333%|0.167709|0.025602|0.103023|53.333%|46.667%|35|0|
|Fixed (k=2)|33.333%|0.147927|0.005820|0.069609|84.000%|16.000%|10|40|
|Fixed (k=3)|13.333%|**0.142408**|**0.000300**|**0.008997**|**96.000%**|**4.000%**|**0**|65|
|Exact-label model|66.667%|0.150024|0.007916|0.095188|80.000%|20.000%|12|13|
|Direct-loss model|30.667%|0.146095|0.003988|0.057718|86.667%|13.333%|8|44|
|Risk-sensitive (\\lambda=0.002)|20.000%|0.146095|0.003988|0.057718|86.667%|13.333%|8|52|
|Risk-sensitive (\\lambda=0.005)|13.333%|0.145092|0.002984|0.057718|89.333%|10.667%|6|59|
|Risk-sensitive (\\lambda=0.010)|13.333%|**0.143156**|**0.001048**|0.057718|**94.667%**|**5.333%**|**2**|63|
|Risk-sensitive (\\lambda=0.020)|10.667%|0.143275|0.001168|0.057718|93.333%|6.667%|2|65|
|Oracle|100.000%|0.142108|0.000000|0.000000|100.000%|0.000%|0|0|

## Effect of Risk Sensitivity

The unpenalized direct-loss controller produced

\[
\\text{mean regret}
===

0.003988.
]

As the asymmetric under-persistence penalty increased, mean regret changed as

\[
0.003988
\\rightarrow
0.003988
\\rightarrow
0.002984
\\rightarrow
0.001048
\\rightarrow
0.001168.
]

The best adaptive result occurred at

\[
\\boxed{
\\lambda=0.010.
}
]

At this setting, mean regret was

\[
\\boxed{
0.001048.
}
]

Relative to the unpenalized direct-loss model, this represents an approximate
regret reduction of

\[
\\boxed{
73.7%.
}
]

Thus directional risk sensitivity substantially improved adaptive persistence
decision quality.

## Under-Persistence Suppression

The direct-loss controller produced

\[
8
]

under-persistence decisions.

At

\[
\\lambda=0.005,
]

this fell to

\[
6.
]

At

\[
\\lambda=0.010,
]

the number fell further to

\[
\\boxed{
2.
}
]

The same count remained at

\[
\\lambda=0.020.
]

Thus the risk-sensitive controller successfully suppressed the high-cost error
mode identified in Experiment 055.

From the baseline direct-loss model to the best risk-sensitive policy,
under-persistence events decreased by

\[
\\boxed{
75%.
}
]

## Consequential-Regret Reduction

The unpenalized direct-loss controller produced regret greater than

\[
0.005
]

in

\[
13.333%
]

of test contexts.

At

\[
\\lambda=0.010,
]

this fell to

\[
\\boxed{
5.333%.
}
]

The zero-regret fraction simultaneously increased from

\[
86.667%
]

to

\[
\\boxed{
94.667%.
}
]

This places the adaptive risk-sensitive controller close to the fixed
strong-persistence baseline, which achieved zero regret in 96% of contexts.

## Finite Optimal Conservatism

Increasing the risk penalty beyond

\[
\\lambda=0.010
]

did not continue improving performance.

At

\[
\\lambda=0.020,
]

mean regret increased from

\[
0.001048
]

to

\[
0.001168.
]

The zero-regret fraction also declined from

\[
94.667%
]

to

\[
93.333%.
]

Therefore the optimal policy is not obtained by maximizing conservatism.

Instead, the experiment identifies a finite risk-sensitive operating point:

\[
\\boxed{
\\lambda^\\star\\approx0.010.
}
]

This establishes a genuine responsiveness-risk tradeoff.

Insufficient conservatism allows costly premature release.

Excessive conservatism increasingly collapses the adaptive policy toward fixed
strong persistence.

## Comparison with Fixed Strong Persistence

Fixed

\[
k=3
]

remains the strongest non-oracle benchmark in the current test regime.

Its mean regret is

\[
0.000300,
]

compared with

\[
0.001048
]

for the best risk-sensitive adaptive controller.

However, fixed (k=3) accomplishes this by choosing maximal persistence in
every state.

The risk-sensitive controller instead retains state-dependent action selection
while substantially reducing the costly under-persistence behavior of the
unpenalized adaptive model.

Thus Experiment 056 narrows the gap between adaptive control and the highly
conservative fixed baseline without fully collapsing to a constant policy.

## Accuracy Is Again Non-Diagnostic

The best risk-sensitive policy achieved only

\[
13.333%
]

exact-label accuracy.

Yet it achieved

\[
94.667%
]

zero-regret decisions.

This reinforces the conclusion from Experiments 052 through 055 that nominal
persistence-label accuracy is not an appropriate primary metric.

The relevant objective remains downstream control utility:

\[
\\min
\\mathbb{E}\[R].
]

A controller may disagree with the nominal oracle action while remaining nearly
utility-optimal.

## Structural Interpretation

Experiments 055 and 056 together reveal that persistence control is not only a
regret-minimization problem but a **risk-sensitive asymmetric decision
problem**.

The action-value surface contains a broad low-regret region toward stronger
persistence and a substantially steeper penalty toward insufficient
persistence.

The geometry can therefore be represented conceptually as

\[
\\boxed{
\\text{weak persistence}
\\rightarrow
\\text{high downside risk}
}
]

while

\[
\\boxed{
\\text{strong persistence}
\\rightarrow
\\text{often low marginal cost}.
}
]

A successful controller should therefore maintain a directional safety margin
against premature epistemic-memory release.

## Principal Conclusion

Experiment 056 demonstrates that explicitly penalizing under-persistence can
substantially improve adaptive persistence control.

The best tested risk penalty,

\[
\\lambda=0.010,
]

reduced mean regret by approximately

\[
73.7%
]

relative to direct mean-loss minimization.

It reduced under-persistence decisions from

\[
8
]

to

\[
2
]

and reduced consequential-regret frequency from

\[
13.333%
]

to

\[
5.333%.
]

Increasing the penalty further slightly degraded performance, demonstrating
that the controller has a finite optimal level of conservatism.

The persistence architecture should therefore be characterized as

\[
\\boxed{
\\text{adaptive}
+
\\text{regret-aware}
+
\\text{directionally risk-sensitive}.
}
]

## Next Research Direction

Experiment 057 should determine whether the risk penalty

\[
\\lambda
]

should itself become state-dependent.

A fixed global penalty assumes that the cost of premature release is constant
across epistemic contexts.

The preceding experiments suggest that this is unlikely.

Experiment 057 should therefore construct an adaptive risk policy

\[
\\lambda\_t
===

\\pi\_{\\text{risk}}
(z\_{1:t},M\_t),
]

or equivalently estimate a context-dependent under-persistence risk

\[
\\hat{C}\_{\\text{under}}(x).
]

The controller could then optimize

\[
J(k\\mid x)
===

\\hat{L}(k\\mid x)
+
\\hat{C}\_{\\text{under}}(x)(3-k).
]

The principal comparison should include:

* fixed global risk penalties,
* direct mean-loss control,
* state-dependent risk-sensitive control,
* fixed strong persistence,
* oracle control.

The goal is to preserve the low-regret protection of conservative persistence
only in states where premature release is genuinely dangerous, while recovering
greater responsiveness elsewhere.

