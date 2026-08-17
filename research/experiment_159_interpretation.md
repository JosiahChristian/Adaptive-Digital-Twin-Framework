# Experiment 159 — Cross-Population Interpretation

## Purpose

Experiment 159 places four population blocks under the same clean-versus-poisoned decision comparison to determine whether the previously observed fixed-budget effects have a stable direction across populations.

This document interprets the committed result without modifying the active experimental pipeline.

## Result pattern

The four blocks do **not** support a simple claim that poisoning consistently improves or consistently worsens downstream intervention outcomes.

| Block | Δ AUC | Δ unsafe selected | Δ regret | Directional reading |
|---|---:|---:|---:|---|
| 511–550 | -0.02285 | +69 | +1.04585 | prediction and decision outcomes worsen |
| 551–590 | -0.00236 | -19 | -0.90024 | near-flat prediction; downstream outcomes improve |
| 591–630 | +0.00183 | -24 | -0.92216 | near-flat prediction; downstream outcomes improve |
| 631–670 | -0.02557 | -3 | +0.54000 | prediction worsens; downstream metrics are mixed |

Across the four blocks, poisoning selects fewer unsafe actions in three blocks and more unsafe actions in one. Regret improves in two blocks and worsens in two. Global AUC improves in only one block and degrades in three.

## Strongest defensible interpretation

The current evidence supports **population-sensitive coupling between predictive perturbation and fixed-budget decision outcomes**.

Small or moderate changes in global ranking quality do not determine the sign of downstream intervention effects. In two blocks, global prediction is almost unchanged while both unsafe selections and regret improve. In another block, a substantial AUC degradation accompanies a large worsening in unsafe selections. In the final block, prediction degrades while unsafe-selection count changes little and regret worsens.

This is stronger than treating any single reversal as an anomaly, but narrower than claiming a universal prediction–decision divergence law.

## What Experiment 159 rules out

The four-block synthesis argues against several overly simple stories:

- poisoning is generally beneficial;
- poisoning is generally harmful in every downstream metric;
- global ROC AUC alone determines fixed-budget intervention quality;
- the earlier beneficial-looking boundary effect has one stable sign across populations;
- one population is sufficient to characterize the decision consequence of the perturbation.

## Candidate scientific direction

A more productive question is now:

**Which properties of the score distribution near the intervention cutoff determine whether a perturbation changes downstream decisions beneficially, harmfully, or negligibly?**

That question is mechanistic and falsifiable. It suggests examining local quantities around the cutoff—margin density, rank instability, unsafe/safe composition, score gaps, and perturbation magnitude—rather than relying primarily on global discrimination metrics.

This should remain a candidate direction until the active experiment lane independently decides whether and how to test it.

## Claim boundary

Experiment 159 does not establish a deployment-relevant adversarial vulnerability, beneficial poisoning, reliable regularization, or a universal law relating prediction degradation to control decisions. It is evidence that the mapping from model-level perturbation to fixed-budget decision consequence is population-sensitive and cannot be summarized by global predictive metrics alone.
