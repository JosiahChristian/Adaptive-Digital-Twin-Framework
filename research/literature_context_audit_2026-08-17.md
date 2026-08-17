# Literature-context audit — 2026-08-17

## Scope

Review/synthesis artifact only. This note does not alter experimental evidence or use outside literature to rescue an internally unsupported claim. Primary repository artifacts remain authoritative for claims about this research program.

## 1. Ranking/top-k stability context

Relevant primary literature:

- Devic, Korolova, Kempe, and Sharan (ICML 2024), *Stability and Multigroup Fairness in Ranking with Uncertain Predictions*: https://proceedings.mlr.press/v235/devic24a.html
- Liang, Soloff, Barber, and Willett (2025), *Assumption-free stability for ranking problems*: https://arxiv.org/abs/2506.02257
- Zuk, Ein-Dor, and Domany (2012), *Ranking Under Uncertainty*: https://arxiv.org/abs/1206.5280
- Heuton et al. (ICML 2025), *Decision-aware Training of Spatiotemporal Forecasting Models to Select a Top-K Subset of Sites for Intervention*: https://proceedings.mlr.press/v267/heuton25a.html

These works provide external methodological context for two ideas relevant to the ADT decision-aware line: rankings/top-k sets can be sensitive to small perturbations when scores are close, and fixed-budget top-K intervention quality is a decision objective that need not be identical to broad predictive fit.

### Implication for Experiment 166

This literature does **not** prove the ADT Experiment 166 result or its mechanism. It does make a generic order-statistic/top-k instability explanation scientifically plausible independent of poisoning. That context is consistent with the internal matched label-preserving control, which reproduced near-cutoff localization at nearly the same perturbation magnitude.

Accordingly, literature context strengthens the need to avoid poisoning-specific mechanistic wording; the actual claim boundary still comes from the committed matched-control and structural-coupling audits, not from analogy to prior papers.

## 2. Prediction-time leakage context

Relevant methodological literature:

- Seneviratne et al. (2023), *A framework for understanding label leakage in machine learning for health care*: https://pmc.ncbi.nlm.nih.gov/articles/PMC10746313/
- Mishra et al. (2026), *A taxonomy for detecting and preventing temporal data leakage in machine learning-based build prediction*: https://pmc.ncbi.nlm.nih.gov/articles/PMC13215522/

Both sources explicitly distinguish retrospective variables from information legitimately available at the intended prediction time. This is directly relevant as methodology, although the application domains differ from ADT.

### Implication for harmful-expansion prediction

The repository audit found that `loss_floor_error` and `expanded_action_loss_error` require realized outcome quantities. The literature therefore supports the methodological principle used in the audit: cross-validation cannot transform a post-outcome variable into a prospective predictor.

The literature is not needed to establish the leakage; the feature definitions in the committed artifacts already establish it. The outside sources simply place that adjudication within standard predictive-validity practice.

## 3. Decision-aware evaluation context

The Heuton et al. top-K intervention work explicitly motivates decision-aware objectives under scarce intervention budgets. This is relevant to the ADT observation that global ranking metrics and fixed-budget downstream outcomes can move differently.

It does not establish a universal prediction-decision divergence law. It supports treating global predictive fit and intervention-level utility as distinct evaluation targets when a pipeline ultimately selects a fixed subset.

## Literature-facing claim boundary

Permitted positioning:

> The ADT findings sit within a broader methodological setting where top-k decisions can be sensitive to score perturbations and where decision-aware evaluation may differ from global predictive metrics. The repository's own matched-control evidence, however, indicates that the Experiment 166 localization is not currently poisoning-specific, and the harmful-expansion headline model contains post-outcome leakage that prevents a pre-decision interpretation.

Do not use the literature to imply that Experiment 166 is theoretically proven, universally generic, or causal; nor to rehabilitate the leaked predictor.
