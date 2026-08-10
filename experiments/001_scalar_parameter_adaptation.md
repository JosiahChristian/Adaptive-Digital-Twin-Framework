\# Experiment 001 — Scalar Parameter Adaptation



\## Objective



Evaluate whether an adaptive digital-twin model can estimate an unknown parameter of a noisy scalar dynamical system from sequential observations.



The experiment also compares an unnormalized parameter-update rule with a normalized adaptation rule after instability was observed in the baseline implementation.



\---



\## System Model



The true discrete-time system is:



\\\[

x\_{k+1} = a x\_k + u\_k

\\]



where:



\- \\(x\_k\\) is the true system state,

\- \\(a\\) is the unknown system parameter,

\- \\(u\_k\\) is the control/process input.



The experiment uses:



\\\[

a = 0.92

\\]



and:



\\\[

u\_k = 1.0

\\]



The digital twin begins with an incorrect parameter estimate:



\\\[

\\hat{a}\_0 = 0.50

\\]



\---



\## Observation Model



The true state is observed with additive Gaussian noise:



\\\[

y\_k = x\_k + v\_k

\\]



with:



\\\[

v\_k \\sim \\mathcal{N}(0, 0.15^2)

\\]



A fixed random seed of `42` is used so both adaptation experiments receive the same reproducible noise sequence.



\---



\## Twin Prediction



The digital twin predicts:



\\\[

\\hat{x}\_{k+1}

=

\\hat{a}\_k \\hat{x}\_k + u\_k

\\]



and computes prediction error:



\\\[

e\_k

=

y\_{k+1} - \\hat{x}\_{k+1}

\\]



For this initial experiment, the latest observation is used directly as the next state estimate rather than applying a separate filtering or state-estimation algorithm.



\---



\# Experiment 001A — Unnormalized Baseline



\## Adaptation Rule



The baseline parameter update was:



\\\[

\\hat{a}\_{k+1}

=

\\hat{a}\_k

\+

\\eta e\_k \\hat{x}\_k

\\]



with learning rate:



\\\[

\\eta = 0.08

\\]



\## Observation



The parameter estimate initially moved toward the true value:



```text

0.5000

0.5317

0.6442

0.8376

0.8916

---

# Multi-Seed Measurement Noise Robustness

## Objective

The initial measurement-noise sweep used a single random seed (`42`).

Although the single-seed experiment remained bounded across all tested noise levels, the final parameter estimate appeared to improve as measurement noise increased through approximately:

\[
\sigma = 0.50
\]

A single realization of random measurement noise is insufficient to determine whether that behavior represents a systematic effect or an artifact of the selected noise sequence.

A multi-seed robustness experiment was therefore performed.

---

## Experimental Protocol

The normalized adaptive law was evaluated across six measurement-noise conditions:

\[
\sigma \in
\{
0.00,\,
0.05,\,
0.15,\,
0.30,\,
0.50,\,
1.00
\}
\]

For each noise level, the experiment was repeated across:

\[
50
\]

independent random seeds.

This produced:

\[
6 \times 50 = 300
\]

total adaptive-system runs.

All other primary model parameters were held constant.

The experiment recorded:

- mean final parameter estimate,
- standard deviation of the final parameter estimate,
- mean absolute parameter error,
- standard deviation of absolute parameter error,
- mean prediction RMSE,
- standard deviation of prediction RMSE, and
- number of bounded runs.

---

## Results

| Noise Std. Dev. | Mean Final \(\hat{a}\) | Std. Dev. \(\hat{a}\) | Mean \(|a-\hat{a}|\) | Mean Prediction RMSE | Bounded Runs |
|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.916510 | 0.000000 | 0.003490 | 0.807599 | 50 / 50 |
| 0.05 | 0.916533 | 0.000350 | 0.003467 | 0.809810 | 50 / 50 |
| 0.15 | 0.916667 | 0.001054 | 0.003333 | 0.829806 | 50 / 50 |
| 0.30 | 0.917089 | 0.002126 | 0.003095 | 0.895842 | 50 / 50 |
| 0.50 | 0.918058 | 0.003597 | 0.003349 | 1.038405 | 50 / 50 |
| 1.00 | 0.922586 | 0.007628 | 0.006270 | 1.549402 | 50 / 50 |

Raw aggregate results:

`results/scalar_noise_multiseed.csv`

---

## Observations

### 1. Boundedness

All:

\[
300 / 300
\]

runs remained within the experiment's boundedness criterion.

This provides substantially stronger empirical evidence for numerical robustness than the original single-seed experiment, although it does not constitute a general proof of stability.

---

### 2. Prediction Error

Mean prediction RMSE increased as measurement noise increased:

```text
σ = 0.00  -> RMSE ≈ 0.808
σ = 0.15  -> RMSE ≈ 0.830
σ = 0.50  -> RMSE ≈ 1.038
σ = 1.00  -> RMSE ≈ 1.549