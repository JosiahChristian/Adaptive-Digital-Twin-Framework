# ADT claim and falsification ledger through Experiment 160

This ledger separates supported claims from rejected or still-unresolved claims. It is intended to prevent later manuscript language from outrunning the evidence.

## Supported within the current simulation

### Context carries prospective hazard information beyond action identity
Supported by Experiments 140, 142, and 144. Context-based ranking beat action-matched random allocation; adding context to a learned action-only model improved unsafe capture and discrimination; and correct row-level context correspondence outperformed within-seed/action context permutations.

### The frozen context-informed hazard filter can improve simulated decisions
Supported by Experiment 146 and independently replicated by Experiment 148. Under clean source labels and fixed coverage, the intervention reduced both selected unsafe actions and realized regret relative to the unfiltered selector and matched random-exclusion controls.

### Targeted source-label concealment can materially alter intervention behavior
Supported by Experiment 150. The largest tested targeted concealment dose produced worse intervention endpoints than clean training and worse than matched random contamination, establishing a concrete simulator-internal vulnerability.

### The downstream effect of the same targeted corruption is heterogeneous under shifted target populations
Supported descriptively by Experiments 153-159. Across four untouched population blocks the fixed attack produced harmful, beneficial, beneficial, and mixed endpoint responses. This supports heterogeneity/non-monotonicity as an observed phenomenon, not beneficial poisoning.

## Falsified or narrowed claims

### “Partial context-tail label repair necessarily improves downstream utility”
Falsified by Experiment 153. The constrained audit did not improve either endpoint relative to the poisoned model on its untouched target block.

### “Targeted poisoning always degrades downstream intervention utility”
Falsified by Experiments 153 and 156. The same fixed attack improved both intervention endpoints on two untouched populations.

### “Prediction metrics and decision endpoints show a simple binary divergence under corruption”
The strong preregistered version was not supported by Experiment 158. Prediction degraded while unsafe selections improved slightly and regret worsened, producing a mixed decision response.

### “Poisoning is beneficial”
Not supported and explicitly rejected as an interpretation. Apparent benefit is target-population dependent, endpoint dependent, and accompanied by degradation elsewhere in the evidence set.

## Open questions

1. Do seed-level changes in global prediction quality reliably track seed-level changes in intervention utility? Experiment 160/161 is the prospective test.
2. If coupling is weak, what boundary-local quantity better predicts decision impact: candidate-set membership changes, context-level action swaps, score margins, or another local sensitivity measure?
3. Does the phenomenon persist under a different model family, corruption mechanism, or intervention budget?
4. Does it generalize beyond the current simulator/domain?

## Publication boundary
A defensible undergraduate manuscript should center on a narrow computational phenomenon, not a universal digital-twin claim: context-sensitive hazard filtering can improve decisions in the clean simulated setting, but targeted training-label corruption interacts with population shift and fixed-budget decision boundaries in non-monotonic ways that conventional global prediction metrics may not capture. The exact strength of the final metric-decoupling claim depends on Experiment 160/161 and subsequent falsification.
