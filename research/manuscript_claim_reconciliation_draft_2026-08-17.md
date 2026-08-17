# Manuscript Claim Reconciliation Draft — 2026-08-17

**Status:** proposed manuscript-facing language only. This review branch does not alter experiment code, preregistrations, generated result artifacts, active workflows, or the historical publication-candidate record on `main`.

## Purpose

Translate the reconciled hostile-review and closed-evidence quadrangulation findings into sentence-level manuscript guidance without strengthening claims beyond the committed evidence.

## Cross-repository non-conflation rule

The findings in this repository must be interpreted independently of the Adversarial-RL-Data-Poisoning-Thesis results. Similar vocabulary such as poisoning, pre-decision/pre-failure evaluation, detector limitations, or decision consequences does **not** constitute evidence of a shared causal mechanism, common latent phenomenon, cross-domain replication, or general adaptive-system law. Results from the adversarial-RL program may motivate separate questions, but they must not be used as corroborating evidence for ADT claims unless a separately specified cross-repository validation study directly tests that relationship.

## Abstract — proposed boundaries

### Permitted core result

> In the tested fixed-budget top-N ranking pipeline, exclusion-membership changes were concentrated near the selection cutoff under both the poisoning condition and a perturbation-matched label-preserving non-poison control. The matched-control comparison did not establish poisoning specificity. A separate compact harmful-expansion model showed strong retrospective outcome-informed discrimination, but two residual features require post-outcome information and therefore the model is not a valid pre-decision predictor; temporally legitimate loss-surface-only variants showed weaker exploratory discrimination in the documented event population.

### Do not state

- that Experiment 166 identifies a poisoning-specific mechanism;
- that `specificity_unresolved` proves poisoning-specific effects are absent;
- that near-cutoff composition independently or causally drives downstream action changes;
- that the approximately 0.979-AUC compact model predicts harmful expansion before the decision;
- that the non-leaking loss-surface-only models establish prospective predictive validity;
- that the ADT framework has solved harmful adaptation prediction generally;
- that these findings establish deployment, cross-domain, aerospace, or biomedical validity;
- that findings in the separate adversarial-RL repository independently corroborate an ADT mechanism or establish cross-domain replication.

## Results — Experiment 166

### Preserve the preregistered positive result

Report that the original cutoff-band localization criterion passed in the tested poisoning condition. Preserve the numerical result and preregistration chronology rather than rewriting the historical result as though it never occurred.

### Immediately report the later falsification/adjudication evidence

1. The bookkeeping-preserving permutation null reproduced the strong Criterion-2 correlation; therefore Criterion 2 is not independent mechanistic evidence.
2. Near-only switched contexts had a lower selected-action-change rate than far-only switched contexts in the downstream-specificity audit; this falsifies the proposed preferential near-switch interpretation in that analysis.
3. The prospectively frozen matched non-poison control closely matched ranking perturbation magnitude and reproduced essentially the same cutoff-localization pattern; the poison-minus-control bootstrap interval included zero under the frozen specificity rule.

`Specificity_unresolved` should be interpreted as **poisoning specificity not established by this test**, not as proof that no poisoning-specific effect exists under any condition.

### Results wording

> Experiment 166 establishes a robust near-cutoff localization pattern within the tested fixed-budget ranking pipeline. Later structural and matched-control audits constrain its interpretation: the Criterion-2 association is reproducible under a bookkeeping-preserving null, downstream changes were not preferentially concentrated among near-only switched contexts, and an adequately perturbation-matched non-poison control reproduced the localization pattern. Accordingly, these results do not establish poisoning specificity or an independent causal boundary-composition mechanism.

## Results — harmful-expansion analysis

### Retain the headline numerical performance only with a timing label

The approximately 0.979 ROC AUC result may be reported as **retrospective outcome-informed discrimination**. It must not be labeled pre-decision prediction because `loss_floor_error` uses `true_best_loss` and `expanded_action_loss_error` uses `realized_expanded_action_loss`, both post-outcome quantities.

### Prospective/exploratory result

> Models restricted to temporally legitimate loss-surface information showed weaker pooled discrimination (approximately 0.683–0.711 ROC AUC and 0.663–0.763 balanced accuracy in the supplied analyses). These results are exploratory, dataset- and evaluation-dependent, and do not yet establish prospective or population-generalizable prediction.

Do not imply that seed-held-out cross-validation repairs the leaked headline feature construction.

## Discussion — interpretation hierarchy

The Discussion should distinguish four levels explicitly:

1. **Observed phenomenon:** near-cutoff switching occurs in the tested fixed-budget ranking pipeline.
2. **Specificity:** not established for poisoning because the matched non-poison control reproduced the phenomenon under the frozen comparison rule.
3. **Mechanism/causality:** not established; one purported independent association is structurally reproducible under a null and the downstream near-only specificity prediction failed.
4. **Generalization:** untested beyond the studied ranking rule, budgets, models, perturbations, seeds, and simulated setting unless separately supported by committed artifacts.

For harmful expansion, distinguish retrospective discrimination from prospective prediction and make the confirmed timing leakage a central limitation rather than a footnote.

Any discussion of the adversarial-RL research should be contextual only. It must not imply mechanistic triangulation, statistical pooling, cross-domain validation, or independent replication of the ADT findings.

## Negative results that must remain visible

The manuscript should preserve, not bury:

- Experiment 165's failed prospective replication of the earlier recall > AP > AUC hierarchy;
- Experiment 158's failure of preregistered prediction-decision divergence criteria despite degraded global prediction metrics;
- poor standalone support-distance representations;
- conditioned-transfer failures despite strong pooled discrimination;
- Experiment 166 Criterion 2's failure under the bookkeeping-preserving null;
- falsification of preferential downstream near-switch specificity;
- unresolved poisoning specificity under the matched non-poison control;
- confirmed timing leakage in the headline harmful-expansion pre-decision interpretation.

## Conclusion — proposed wording

> The current evidence supports two narrower conclusions. First, fixed-budget ranking in the tested ADT pipeline exhibits a robust near-cutoff localization of membership changes, but the available controls do not establish that this localization is poisoning-specific or that near-cutoff composition independently causes downstream action changes. Second, temporally legitimate loss-surface-only features show exploratory discrimination for harmful expansion in the documented event population, while the strongest compact result is retrospective because it incorporates post-outcome residuals. These findings motivate stricter separation of ranking geometry, perturbation specificity, causal mechanism, and prediction-time validity in adaptive-system evaluation.

## Publication-readiness consequence

The closed-evidence adjudication supports **READY AFTER DOCUMENTATION CORRECTION** for these narrowed claims. This means no new scientific experiment is required solely to report these bounded findings accurately. It does not imply that stronger poisoning-specific, causal, prospective-prediction, cross-repository, or broad-generalization claims are ready; those would require new evidence. Final submission readiness also depends on completing the actual manuscript corrections and preserving the negative/adjudication record in the manuscript-facing materials.
