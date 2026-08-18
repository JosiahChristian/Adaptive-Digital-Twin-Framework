# SMPT final packaging audit — 2026-08-18

Status: **PASS EXCEPT AUTHOR METADATA / FINAL IMMUTABLE SNAPSHOT IDENTIFIER**.

## Mechanical checks completed

- Venue source contains the migrated scientific body and retains the venue-neutral `manuscript.md` as scientific source of truth.
- Abstract length: **169 words**, below the frozen <=250-word gate.
- Highlights: **5** separate highlights; character counts including punctuation are **79, 65, 76, 67, 70**, respectively. All are <=85 characters.
- Bibliography-key audit corrected the venue source to use only keys present in `references.bib`: `splettstoesser2023selfadaptive`, `qiu2025digitaltwins`, `builesmontano2025digitaltwin`, `elmachtoub2022smart`, `elmachtoub2020decisiontrees`, `mandi2022decisionfocused`, `chen2015spectral`, `asudeh2018stable`, and `kapoor2023leakage`.
- No citation is used as evidence for the internal experimental adjudication; literature remains contextual.
- Table 1 balances favorable and later falsifying/adjudicating evidence.
- Figure 1 and Figure 2 are wired to the filenames produced by `plot_experiment166_stronger_control.py`.
- The plotting script refuses to render unless the preserved stronger-control artifact SHA-256 equals `ced924c850aa5f6b5dd2923bcd6e761f00a3a15bbae620c639c4084fa876c904` and the artifact reports both `match_adequacy_pass=true` and `primary_decision=specificity_unresolved`.
- Historical inadequate-control output is not used for the matched-control figures.
- Data/code statement distinguishes tracked evidence from the preserved Actions artifact.
- Generative-AI disclosure remains explicit.

## Figure rendering state

The two ADT figure-generation paths were already end-to-end rendering-tested against the digest-verified recovered Actions artifact during publication engineering. The LaTeX source now points to exactly those generated filenames. Binary figure files are intentionally not recreated from a different source or copied from the earlier inadequate control.

## Compile-oriented source audit

The source uses `elsarticle`, `amsmath`, `amssymb`, `booktabs`, `graphicx`, and `url`; bibliography style is `elsarticle-num`. Cross-reference labels are unique. The remaining compile dependency is the presence of the official Elsevier class/bibliography environment and the two generated figure files in `research/manuscript/generated/`. A final compile should be performed from the exact submission snapshot after author metadata is inserted.

## Stable archival citation gate

Do **not** cite mutable `main` as the archival research object. At submission freeze, create/tag an immutable repository release (and DOI-backed archive if available) from the exact accepted submission commit, then replace the generic repository wording with that immutable identifier. Until the branch stops changing, inserting a commit hash now would immediately become stale.

## Only author-supplied gate

Verified author name, affiliation, postal address, corresponding-author e-mail, and any required researcher identifier remain intentionally blank. No values are inferred.
