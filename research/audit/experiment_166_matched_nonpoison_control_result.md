# Experiment 166 matched non-poisoning control result

Status: **completed post-review control; formal specificity decision inconclusive because the prospectively frozen match-adequacy gate failed**.

The control protocol was committed before any control outcome was generated at commit `432d8ff8f0320d9f9864deb4ed9c5e9b47eb7ecb`. GitHub Actions run `32074187109` completed successfully and preserved the generated output bundle as artifact `9302866987` (SHA-256 `f418a35ea82b539ab08abcb30caf18cb4cc86eb76b3d4524d8cfc4f3cc3224f2`). Historical Experiment 166 artifacts remain unchanged.

## Match gate

The frozen design generated 128 stratified clean-label bootstrap fits and selected candidate 39 (bootstrap seed 16655039) by the precommitted lexicographic matching rule.

Historical poison perturbation: mean exclusion Jaccard = 0.9238228511679869; total membership switches = 308; mean absolute score shift = 0.06710396153224119.

Selected clean-label control: mean exclusion Jaccard = 0.9888190680014233; total membership switches = 42; mean absolute score shift = 0.014329547354100544.

The absolute Jaccard mismatch was 0.06499621683343637, exceeding the frozen <=0.010 gate. The switch-count mismatch was 266, also exceeding the frozen <=10% of 308 gate. Therefore `match_adequacy_pass = false`.

## Endpoint retained but not admissible for the specificity claim

The historical poison mean seed-level near-minus-far switch-rate difference was 0.1362299667050161. The selected control also showed positive cutoff localization, with mean difference 0.03835232494002062 and a seed-bootstrap 95% interval [0.0249036415859413, 0.052636803706526264].

The paired poison-minus-control estimate was 0.0978776417649955 with bootstrap 95% interval [0.06583455480431329, 0.1302567556498833]. Under the frozen protocol this otherwise directional result **cannot be interpreted as poisoning-specific**, because the non-poisoning perturbation was much weaker than the poison perturbation and the match gate failed first.

The control produced 42 total membership switches, 90.476% of which were near the clean cutoff, and 29 selected-action changes. The poison perturbation produced 308 switches, 50.325% near the clean cutoff, and 245 selected-action changes. These diagnostics reinforce the magnitude mismatch rather than repairing it.

## Scientific interpretation

This is a preserved negative/failed-control result, not a reason to alter the gate after seeing data. It establishes two useful facts: ordinary stratified clean-label bootstrap refitting can itself generate statistically positive near-cutoff localization, so cutoff localization is not unique to label poisoning in a qualitative sense; however, the attempted control did not perturb the ranking nearly enough to answer whether the *magnitude* of Experiment 166 localization is poisoning-specific at matched perturbation strength.

The correct formal result is therefore **inconclusive due to inadequate perturbation matching**. The next scientifically meaningful step, if separately authorized after this observed failure, is a newly frozen stronger label-preserving perturbation family capable of matching the historical exclusion displacement without using unsafe target outcomes or localization endpoints for tuning. The present 128-candidate design must not be extended post hoc.
