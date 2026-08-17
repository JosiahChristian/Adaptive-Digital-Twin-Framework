# Experiment 154 result: mechanism of the apparent poisoning benefit

Experiment 154 diagnosed why the 20% targeted label-concealment model outperformed the clean model on the Experiment 153 target population.

The effect was **not** a global ranking improvement. Clean ROC AUC was 0.833773 versus 0.831417 for the poisoned model, and excluded-unsafe recall was 0.819902 versus 0.819201. Average precision was nearly unchanged (0.410693 clean, 0.411223 poisoned).

The difference instead arose near the fixed top-N intervention boundary. The clean and poisoned exclusion sets had Jaccard overlap 0.924229; 3,147 candidate rows were excluded by both models, while 129 were clean-only and 129 poison-only. The poison-only slice had slightly lower unsafe prevalence (0.178295) than the clean-only slice (0.186047), so the poisoned ranking did not create a generally better hazard classifier but did alter which candidates fell around the exclusion cutoff.

At the context level, 220 of 2,799 selected actions changed. Those transitions included 41 unsafe-to-safe changes versus 22 safe-to-unsafe changes, with mean poison-minus-clean regret of -0.004092 on changed contexts. That local boundary reordering explains the observed lower total regret and unsafe count under poisoning on this population.

## Interpretation

The Experiment 153 reversal should not be interpreted as evidence that poisoning is beneficial. It is a population-specific interaction between a small score-order perturbation and a fixed intervention budget. The global hazard-ranking metrics did not improve.

The next test must therefore be prospective: hold the clean model, targeted attack, fixed-budget intervention, and diagnostic endpoints unchanged on a fresh target population and test whether the sign of the clean-versus-poison intervention difference replicates. If the apparent benefit reverses or disappears, it supports the interpretation that Experiment 153 was a target-specific boundary effect rather than a stable regularization phenomenon.
