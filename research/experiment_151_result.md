# Experiment 151 result: context-tail label-audit mitigation

Experiment 151 passed all six preregistered mitigation criteria.

Under the frozen 20% targeted unsafe-to-safe source-label concealment attack, the undefended model selected 392 unsafe actions with total realized regret 16.20742687464437 across 3,015 target contexts. The clean model selected 323 unsafe actions with regret 15.161576106369107.

The frozen context-tail audit inspected 1,576 of 7,881 source rows (20%) ranked by context-support distance. Under this specific constructed attack, that audit intersected all 328 poisoned source rows. Restoring the verified labels on audited rows therefore returned the defended model exactly to the clean-model endpoints: 323 unsafe selections and total regret 15.161576106369107.

By contrast, 500 equal-budget random audits had mean unsafe selections 392.022 and mean regret 16.202536563143905; their 5th-percentile thresholds were 391 unsafe selections and regret 16.16281637560894. The context-tail audit beat both thresholds and was within the preregistered 10% clean-performance margins.

## Interpretation

This is an oracle-audit upper bound, not an operational poison detector. The result establishes that the vulnerability identified in Experiment 150 is highly concentrated in the same predeclared context-support tail used by the attack, and that perfect verification of that region is sufficient in this simulation to recover the clean intervention result. Because the attack itself targets the highest context-support distances, exact recovery is structurally favorable to this defense and must not be presented as general adversarial robustness.

The next defensible question is therefore whether a *partial* and budget-constrained audit that cannot simply cover the entire attacked tail still provides disproportionate mitigation relative to equal-budget random verification. That test should use an untouched target population and freeze the audit budget below the poison count before target outcomes are observed.
