# Experiment 064 — Multi-Seed Generative Persistence Robustness Diagnostic

## Objective

Determine whether the safety-responsiveness persistence frontier identified in
Experiment 063 remains stable across independently generated trajectory
populations rather than only across randomized train-test partitions.

Experiment 063 established partition robustness by repeatedly reshuffling the
same 249 decision contexts.

Experiment 064 attempts to extend this analysis to true generative robustness
by reseeding Python and NumPy before regenerating the complete persistence
analysis dataset for each seed

\[
s\\in{0,1,\\ldots,9}.
]

Because external reseeding does not guarantee that upstream simulation routines
actually consume those random states, the experiment also computes a
cryptographic fingerprint of every generated decision-context dataset.

This provides an explicit test of whether each seed genuinely creates an
independent evidence population.

## Experimental Design

For each seed:

1. Python's random generator was reseeded.
2. NumPy's random generator was reseeded.
3. The complete persistence analysis dataset was regenerated.
4. Selected numerical context fields were serialized.
5. A SHA-256 dataset fingerprint was computed.
6. Persistence policies were evaluated on the resulting dataset.

The fingerprint therefore serves as a direct generative-diversity check.

If independent seeds generate independent trajectory populations, the expected
result is approximately

\[
10/10
]

unique dataset fingerprints.

## Generation Diversity Result

The experiment produced

\[
\\boxed{
1/10
}
]

unique dataset fingerprints.

The single fingerprint was

\[
\\texttt{59263bd1f1b225ea...}
]

and occurred for all

\[
10
]

seed values.

Thus

\[
D\_0
===

# D\_1

# \\cdots

D\_9
]

for the generated analysis datasets.

External changes to Python and NumPy random seeds therefore had no observable
effect on the upstream trajectory population.

## Principal Finding

Experiment 064 does **not** establish generative robustness.

Instead, it demonstrates that the current upstream simulation pipeline is
effectively deterministic with respect to externally supplied Python and NumPy
random states.

The trajectory generator therefore appears to:

* use an internally fixed seed,
* instantiate an internally seeded random generator,
* use deterministic predefined trajectories,
* or otherwise isolate its stochastic state from the external seed settings.

The critical result is

\[
\\boxed{
\\text{requested seed variation}
\\neq
\\text{actual trajectory variation}.
}
]

## Importance of the Fingerprint Safeguard

Without explicit dataset fingerprinting, the experiment would have appeared to
perform a ten-seed generative robustness study.

Policy statistics could then have been summarized across ten nominal seeds even
though every seed used exactly the same underlying evidence population.

Such a result would create false replication.

The fingerprint test therefore prevented the erroneous interpretation

\[
\\text{10 executions}
\\Rightarrow
\\text{10 independent realizations}.
]

Instead, the experiment establishes

\[
\\boxed{
\\text{10 executions}
===

\\text{1 unique generative realization}.
}
]

## Relationship to Experiment 063

Experiment 063 remains valid because it explicitly randomized the train-test
partition of the existing 249 contexts.

Its conclusions therefore concern

\[
\\boxed{
\\text{partition robustness}.
}
]

Experiment 064 attempted to measure

\[
\\boxed{
\\text{generative robustness}.
}
]

The failed diversity test establishes that these two concepts remain distinct.

The current evidence therefore supports robustness to sample partitioning but
does not yet support robustness to independently generated system
realizations.

## Reproducibility Implication

The deterministic upstream behavior is not itself a defect.

Fixed seeds are useful for reproducible simulation and controlled experiment
comparison.

However, reproducibility and robustness require different experimental modes.

A fixed-seed generator supports

\[
\\text{reproducibility},
]

whereas independent seeded generation is required to investigate

\[
\\text{distributional robustness}.
]

The simulation architecture should therefore expose the generative seed as an
explicit parameter rather than embedding it internally.

## Methodological Principle

Experiment 064 establishes an important experimental rule for the framework:

\[
\\boxed{
\\text{Never infer stochastic independence from seed labels alone.}
}
]

Independent realizations should be verified through observable generated-data
differences.

Dataset fingerprints provide a simple reproducibility mechanism for doing so.

Future multi-seed experiments should record:

* requested seed,
* effective generator seed,
* dataset fingerprint,
* trajectory count,
* analysis-context count.

This makes generative independence auditable.

## Numerical Artifacts

The experiment preserved two numerical outputs:

\[
\\texttt{
results/multiseed\_generative\_persistence\_robustness.csv
}
]

and

\[
\\texttt{
results/multiseed\_generative\_persistence\_fingerprints.csv
}.
]

The fingerprint file records the seed-to-dataset mapping and demonstrates that
all ten executions produced the same generated context population.

## Principal Conclusion

Experiment 064 is a successful diagnostic experiment but not a successful
generative robustness experiment.

All ten requested seed values generated the same analysis dataset:

\[
\\boxed{
N\_{\\text{unique datasets}}=1.
}
]

Therefore the framework's upstream trajectory-generation pathway currently
contains deterministic or internally fixed random-state behavior.

No claim about persistence-policy generative robustness should be made from
this run.

The correct conclusion is instead:

\[
\\boxed{
\\text{the generative seed must be exposed before robustness can be tested}.
}
]

## Next Research Direction

Experiment 065 should identify and parameterize the upstream source of
trajectory randomness.

The trajectory-generation API should be modified so that a caller can supply

\[
s\_{\\text{generation}}
]

explicitly.

The desired architecture is

\[
\\mathcal{D}\_s
===

G(s),
]

such that

\[
s\_i\\neq s\_j
]

produces independently generated trajectory populations while repeated use of
the same seed satisfies

\[
G(s)=G(s)
]

for reproducibility.

Experiment 065 should first verify:

\[
\\boxed{
\\text{same seed}
\\Rightarrow
\\text{same fingerprint}
}
]

and

\[
\\boxed{
\\text{different seeds}
\\Rightarrow
\\text{different fingerprints}.
}
]

Only after this seed-control validation succeeds should the full generative
persistence robustness experiment be rerun.

