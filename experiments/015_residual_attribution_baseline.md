# Experiment 015 — Residual Attribution Baseline

## Objective

Determine whether distinct sources of digital-twin mismatch produce distinguishable statistical signatures in the estimator innovation sequence.

This experiment marks a transition from uncertainty adaptation based only on the magnitude of prediction disagreement toward uncertainty adaptation based on the inferred cause of that disagreement.

The four mismatch regimes considered are:

1. increased measurement noise,
2. process disturbance,
3. parameter mismatch,
4. structural change.

The central question is:

> Can residual statistics provide enough information to distinguish why the digital twin disagrees with the observed system?

---

## Motivation

Previous experiments established that innovation-driven uncertainty adaptation can substantially improve state estimation.

However, the existing uncertainty-management architectures treat disagreement primarily as evidence that the model should become more uncertain.

This leaves an important ambiguity.

A large innovation may result from:

- inaccurate measurements,
- an external process disturbance,
- incorrect model parameters,
- or a change in the underlying system dynamics.

These causes should not necessarily produce the same adaptive response.

Measurement uncertainty should primarily modify the interpretation of sensor information.

Process disturbances should primarily increase process uncertainty.

Parameter mismatch should strengthen parameter adaptation.

Structural change may require model or regime adaptation.

Therefore, a more capable adaptive digital twin should attempt to infer the source of residual disagreement before deciding how to adapt.

---

## Experimental Design

For each mismatch regime, 100 stochastic simulations were generated.

This produced

\[
4 \times 100 = 400
\]

total trajectories.

For every trajectory, the innovation sequence was summarized using the following statistical features:

\[
\overline{|\nu|}
\]

mean absolute innovation,

\[
\overline{\mathrm{NIS}}
\]

mean normalized innovation squared,

\[
P(\mathrm{NIS}>1),
\]

\[
P(\mathrm{NIS}>3),
\]

maximum NIS,

the longest consecutive run for which

\[
\mathrm{NIS}>1,
\]

and the lag-one innovation autocorrelation

\[
\rho_1
=
\operatorname{corr}(\nu_k,\nu_{k-1}).
\]

These quantities represent several different characteristics of residual behavior:

- magnitude,
- statistical inconsistency,
- extreme events,
- persistence,
- and temporal correlation.

---

## Results

The mean feature values across 100 simulations per regime were:

| Feature | Measurement Noise | Process Disturbance | Parameter Mismatch | Structural Change |
|---|---:|---:|---:|---:|
| Mean absolute innovation | 0.997815 | 0.687926 | 0.833808 | 0.693314 |
| Mean NIS | 1.248053 | 1.649225 | 1.853928 | 1.567478 |
| Fraction NIS > 1 | 0.363800 | 0.397600 | 0.453100 | 0.415900 |
| Fraction NIS > 3 | 0.117800 | 0.151000 | 0.208900 | 0.163600 |
| Maximum NIS | 10.757659 | 26.001097 | 14.204711 | 13.499468 |
| Longest NIS run > 1 | 4.510000 | 7.000000 | 16.530000 | 7.110000 |
| Lag-1 innovation autocorrelation | 0.156582 | 0.359940 | 0.609492 | 0.483207 |

---

## Interpretation

The results demonstrate that different mismatch mechanisms produce different residual signatures.

### Measurement Noise

Measurement noise produces the largest mean absolute innovation:

\[
\overline{|\nu|}
\approx
0.998.
\]

However, its temporal correlation is the smallest:

\[
\rho_1
\approx
0.157.
\]

This is consistent with disagreement that is relatively large but weakly persistent.

Large residual magnitude alone is therefore insufficient evidence of model failure.

---

### Process Disturbance

Process disturbance produces the largest maximum NIS:

\[
\max(\mathrm{NIS})
\approx
26.0.
\]

Its longest inconsistent run remains relatively moderate:

\[
L_{\mathrm{NIS}>1}
\approx
7.0.
\]

This suggests a signature characterized by strong excursions rather than the prolonged inconsistency observed under parameter mismatch.

---

### Parameter Mismatch

Parameter mismatch produces the strongest persistence signature.

Its mean NIS is the largest:

\[
\overline{\mathrm{NIS}}
\approx
1.854,
\]

and the longest run above the consistency threshold is substantially greater than for every other regime:

\[
L_{\mathrm{NIS}>1}
\approx
16.53.
\]

It also produces the largest lag-one innovation autocorrelation:

\[
\rho_1
\approx
0.609.
\]

These results indicate that incorrect model parameters generate temporally persistent and correlated prediction errors.

This is particularly important because persistence may provide evidence that disagreement originates within the digital model rather than from isolated measurement fluctuations.

---

### Structural Change

Structural change produces a more ambiguous signature.

Its mean absolute innovation,

\[
0.693,
\]

is very close to the process-disturbance value,

\[
0.688.
\]

Its longest inconsistent run is also similar:

\[
7.11
\quad\text{versus}\quad
7.00.
\]

However, structural change exhibits substantially greater lag-one autocorrelation:

\[
0.483
\quad\text{versus}\quad
0.360.
\]

This suggests that structural change contains stronger temporal organization even when global residual magnitude and threshold statistics overlap with those of a process disturbance.

---

## Key Finding

The experiment provides evidence that residual disagreement contains information about its underlying cause.

No single statistic completely separates all four regimes.

Instead, the mismatch mechanisms occupy different regions of a multidimensional residual-feature space.

Conceptually,

\[
\mathbf{f}
=
\begin{bmatrix}
\overline{|\nu|} \\
\overline{\mathrm{NIS}} \\
P(\mathrm{NIS}>1) \\
P(\mathrm{NIS}>3) \\
\max(\mathrm{NIS}) \\
L_{\mathrm{NIS}>1} \\
\rho_1
\end{bmatrix}
\]

acts as an observable signature generated by an underlying latent mismatch cause

\[
z
\in
\{
M,P,\Theta,S
\},
\]

where the classes correspond to measurement uncertainty, process disturbance, parameter mismatch, and structural change.

The attribution problem can therefore be expressed as

\[
P(z\mid\mathbf{f}).
\]

This provides an empirical bridge between innovation-based uncertainty estimation and causal residual attribution.

---

## Limitation of Global Features

The current features summarize entire trajectories.

This discards information about when disagreement occurs and how the estimator responds afterward.

This limitation is particularly important for distinguishing process disturbances from structural changes.

A transient disturbance and a persistent dynamical change may produce similar global statistics while having very different temporal signatures.

Therefore, the next experiment should explicitly represent residual evolution around the mismatch event.

Define windows such as

\[
W_{\mathrm{pre}}=[35,49],
\]

\[
W_{\mathrm{event}}=[50,59],
\]

and

\[
W_{\mathrm{post}}=[60,79].
\]

Features can then measure changes such as

\[
\Delta\overline{\epsilon}
=
\overline{\epsilon}_{\mathrm{event}}
-
\overline{\epsilon}_{\mathrm{pre}},
\]

and recovery behavior such as

\[
\rho_{\mathrm{recovery}}
=
\frac{
\overline{\epsilon}_{\mathrm{post}}
}{
\overline{\epsilon}_{\mathrm{event}}+\varepsilon
}.
\]

A transient disturbance should produce a different event-to-recovery trajectory than a persistent structural change.

---

## Conclusion

Experiment 015 establishes a residual-attribution baseline.

The results show that measurement noise, process disturbance, parameter mismatch, and structural change do not produce identical innovation statistics.

In particular:

- measurement noise produces large but weakly correlated residuals,
- process disturbances produce strong residual excursions,
- parameter mismatch produces persistent and highly correlated inconsistency,
- structural change occupies an intermediate region with stronger temporal correlation than process disturbance.

The remaining overlap demonstrates that global trajectory statistics alone are not sufficient for robust attribution.

The next stage should therefore incorporate temporal residual structure before introducing a formal classifier.

This motivates Experiment 016:

**Temporal Residual Attribution Features.**