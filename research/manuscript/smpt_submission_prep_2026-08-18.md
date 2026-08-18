# Simulation Modelling Practice and Theory Submission Preparation — 2026-08-18

**Target:** Simulation Modelling Practice and Theory (Elsevier)

**Scientific rule:** venue formatting must not broaden the frozen manuscript claims.

## Fit statement for editor/cover letter

This manuscript contributes a reproducible validity study for simulation-based adaptive decision pipelines. It examines two methodological failure modes relevant to modelling and simulation evaluation: (1) apparent mechanism specificity under fixed-budget ranking, tested with prospectively frozen matched controls and structural falsification analyses; and (2) apparent pre-decision predictive performance caused by post-outcome feature timing. The work emphasizes experimental design, validation/verification, selection/comparison procedures, uncertainty, and reproducible adjudication rather than deployment claims.

## Required/appropriate manuscript metadata

### Proposed title

**Decision-Time Validity and Cutoff Geometry in a Fixed-Budget Adaptive Digital-Twin Pipeline**

Retain the current title unless later editorial review identifies a scope problem. Do not insert “poisoning-specific mechanism,” “causal,” “robust predictor,” or deployment language.

### Proposed keywords — 7 maximum

1. simulation validation
2. digital twin
3. decision-time validity
4. top-k selection
5. ranking stability
6. data leakage
7. falsification

### Proposed highlights — 3–5 bullets, each ≤85 characters

- Fixed-budget ranking concentrated membership changes near the selection cutoff.
- A perturbation-matched non-poison control reproduced the localization pattern.
- Structural tests rejected the original independent mechanism interpretation.
- Post-outcome residuals invalidated a headline pre-decision prediction claim.
- Prospective controls materially narrowed conclusions from strong initial results.

Before submission, mechanically verify the 85-character limit including spaces.

## Abstract gate

SMPT requires a concise factual abstract of no more than 250 words. The current abstract is intended to remain below that limit. Final typesetting must re-count words after any venue-specific edits.

The abstract must preserve:

- the original localization observation;
- the matched non-poison comparison;
- `specificity_unresolved` as “not established,” not “absent”;
- the retrospective status of the ~0.979 AUC compact model;
- the exploratory status of temporally legitimate models.

## Article structure

SMPT asks for clearly numbered sections/subsections. The current manuscript already follows that structure. Final conversion should retain numbered sections and cross-references.

Recommended final order:

1. Introduction
2. Methods
3. Results
4. Negative and Failed Results
5. Discussion
6. Limitations
7. Conclusion
8. Declaration of generative AI and AI-assisted technologies
9. Data/code availability and reproducibility statement
10. Acknowledgements, if any
11. References

## Generative-AI disclosure

Elsevier's current author guidance requires disclosure when generative AI or AI-assisted tools were used in manuscript preparation. A publication-safe draft statement is:

> **Declaration of generative AI and AI-assisted technologies in the manuscript preparation process.** During preparation of this work, the author used OpenAI ChatGPT to assist with research-document organization, manuscript drafting/editing, literature-search support, and adversarial claim auditing. All numerical results, methodological descriptions, citations, and scientific interpretations retained in the manuscript were subsequently checked against the cited primary literature or committed experimental artifacts, and the author takes full responsibility for the content of the article.

This declaration must not imply that ChatGPT conducted the scientific experiments or generated the primary results.

## Data/code availability draft

> **Data and code availability.** Experiment code, preregistrations, tracked result summaries, audit records, manuscript source maps, and reproducible figure-generation code are maintained in the project repository. The stronger Experiment 166 matched-control output used for the specificity adjudication was preserved as a GitHub Actions artifact; its workflow run, head commit, artifact identifier, and SHA-256 digest are recorded in the manuscript provenance audit. Figure-generation code verifies the archived artifact digest before rendering. Historical weaker-control results remain preserved separately and are not substituted for the stronger-control output.

Before submission, replace repository-relative descriptions with the exact archival/public repository citation expected by the venue. Do not cite a mutable branch as the permanent research record if a release/DOI can be created first.

## Figures and tables

SMPT requires figures as separate files with captions and tables as editable text.

Planned main-paper displays:

- Table 1: balanced Experiment 166 adjudication ledger.
- Figure 1: poison versus stronger matched-control cutoff localization.
- Figure 2: retrospective versus temporally legitimate harmful-expansion discrimination.

The stronger-control figure must be generated only through the digest-gated manuscript script using the verified CI artifact. The earlier inadequate control must never appear as the stronger comparison.

## Reference style

SMPT permits consistent reference formatting at initial submission and uses numbered square-bracket citations. The existing numbered manuscript citations are compatible. DOI metadata should remain in the BibTeX source where available.

## Submission-mode recommendation

Use the subscription publication route initially unless the author independently chooses gold open access or has institutional/funder coverage. The journal is hybrid, so choosing subscription does not change scientific review.

## Final SMPT pre-submission gates

- [ ] Move manuscript into current Elsevier editable template (.tex preferred if stable).
- [ ] Confirm abstract ≤250 words.
- [ ] Mechanically verify 3–5 highlights, each ≤85 characters.
- [ ] Confirm 1–7 keywords.
- [ ] Add author/corresponding-author and affiliation information accurately.
- [ ] Add generative-AI disclosure.
- [ ] Add data/code availability statement with stable repository/archive identifier.
- [ ] Render final figures from provenance-checked scripts.
- [ ] Provide captions as requested and editable tables.
- [ ] Run citation/reference consistency check.
- [ ] Run final whole-package hostile review after formatting.
- [ ] Do not merge the review PR merely because submission files are complete.
