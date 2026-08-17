# Faculty Review Brief — ADT Publication Candidate

## One-sentence candidate result

In a generated adaptive-system event population, compact features available before an action-space expansion decision show strong discrimination between later harmful and beneficial expansion events, while several plausible alternative representations weaken substantially under conditioning or transfer.

## Why this may be scientifically interesting

Adaptive systems are often evaluated after an update has already changed behavior. A useful narrower problem is whether information available **before** an adaptive action can identify elevated risk of later harm. If that signal survives stronger validation, it could motivate decision-aware safeguards for adaptive computational twins without requiring a claim that the entire twin is globally safe or optimal.

## Current strongest evidence

The compact loss-surface calibration model is evaluated on 65 documented events (15 harmful, 50 beneficial) and reports:

- balanced accuracy 0.950;
- harmful-event recall 1.000;
- harmful-event precision 0.750;
- ROC AUC 0.979;
- mean fold balanced accuracy 0.939;
- mean fold ROC AUC 0.913.

These are hypothesis-strengthening results, not final publication evidence.

## Evidence against easy explanations

Two existing negative findings make the candidate more useful to review:

1. simple support-distance representations perform weakly, arguing against a generic out-of-support explanation;
2. high pooled action/proxy discrimination can collapse under within-action cross-block transfer, demonstrating that the research pipeline can expose structural confounding rather than accepting a favorable pooled score.

Recent poisoning/intervention experiments add a methodological warning: global ranking metrics and fixed-budget downstream decisions can move differently across populations. That observation should inform evaluation design but is not presently the primary publication claim.

## Questions for a faculty reviewer

A reviewer would be most useful in challenging the following points:

1. Is the harmful-expansion event definition scientifically meaningful or too tailored to the generated system?
2. Are all candidate predictor features unambiguously available before the decision/outcome, with no temporal leakage?
3. Is the event count sufficient for the proposed statistical treatment, and which uncertainty procedure is appropriate?
4. Which simpler baselines must be defeated before the compact model is interesting?
5. What constitutes a genuinely independent population in this simulator rather than another random-seed sample from effectively the same generator?
6. Which distribution shifts would be scientifically meaningful rather than arbitrary stress tests?
7. Is the current framing better positioned as adaptive systems, digital twins, safe adaptation, or decision-aware predictive modeling?
8. What additional evidence would be required before submission to a workshop, conference, or journal appropriate for an undergraduate-led faculty-supervised project?

## Evidence still required before manuscript claims

- independent/held-out population replication;
- feature-timing and leakage audit;
- harm-label sensitivity;
- one-feature and low-capacity baselines;
- uncertainty intervals/resampling appropriate to the sample size;
- calibration stability;
- action/block-conditioned evaluation;
- meaningful distribution shift;
- failure-case taxonomy.

## Claims intentionally withheld

The current work does not establish causality, deployment safety, general digital-twin robustness, transfer to arbitrary cyber-physical systems, biomedical applicability, or clinical relevance.

## Reviewer-facing repository map

- `research/problem_definition.md` — research question and evidence hierarchy
- `research/evidence_synthesis.md` — positive and negative evidence
- `research/claim_ledger.md` — allowed, provisional, falsified, and prohibited claims
- `research/publication_candidate.md` — candidate paper framing and stopping rule
- `results/absolute_loss_floor_harmful_expansion_analysis.csv` — primary current quantitative artifact

## Decision requested from future faculty supervision

The immediate question is not "is this ready to publish?" It is:

**Is the compact pre-decision harmful-expansion signal sufficiently well-motivated to justify the next round of rigorous independent validation, and if so, what experimental/statistical design would make that validation publication-relevant?**
