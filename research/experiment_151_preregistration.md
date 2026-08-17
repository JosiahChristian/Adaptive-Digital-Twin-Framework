# Experiment 151 preregistration: context-tail label-audit mitigation

## Motivation
Experiment 150 prospectively established that targeted unsafe-to-safe source-label concealment concentrated in the largest context-support distances can degrade the replicated hazard-filter intervention more than matched random contamination. Experiment 151 tests a deliberately simple defensive hypothesis without changing the hazard model family or intervention budget.

## Frozen defense
Use the same source population, target population, feature set, logistic model, 20% targeted contamination construction, and target exclusion count as Experiment 150.

Before fitting the poisoned model, audit source rows whose `context_support_distance` lies in the top 20% of the source distribution. This audit is assumed to recover the original label for audited rows only. No target labels are used by the audit. Fit the defended model to the corrected labels.

This is an oracle-audit *upper-bound experiment*: it does not claim that real label errors can already be identified automatically. It asks whether concentrating verification effort on the predeclared high-context tail is sufficient in principle to reverse the specific vulnerability exposed by Experiment 150.

## Controls
1. Clean-label model from the same source data.
2. Undefended 20% targeted-poisoning model.
3. 500 matched random-audit controls. Each control audits exactly the same number of source rows as the context-tail audit, sampled uniformly without replacement from source rows. A random audit corrects poisoned labels only where its sampled rows intersect the poisoned set.

All models use the exact clean-model target exclusion count from Experiment 150 so intervention coverage cannot explain differences.

## Co-primary mitigation criteria
The context-tail audit passes only if all are true:

1. defended unsafe selections < undefended targeted-poisoning unsafe selections;
2. defended total regret < undefended targeted-poisoning total regret;
3. defended unsafe selections <= the 5th percentile of matched random-audit unsafe selections;
4. defended total regret <= the 5th percentile of matched random-audit regret;
5. defended unsafe selections are no more than 10% above the clean-model unsafe count (multiplicative margin);
6. defended total regret is no more than 10% above clean-model total regret (multiplicative margin).

## Interpretation boundary
A pass supports only this statement: under the frozen simulated source/target populations and the specific targeted label-concealment attack established in Experiment 150, perfect verification of labels in a predeclared high-context tail can recover intervention performance better than equal-budget random verification and to within a 10% margin of clean performance.

It does not establish an operational poison detector, deployment safety, clinical validity, or universal robustness.
