# Experiment 166 Stronger-Control Artifact Verification — 2026-08-17

**Scope:** publication-provenance verification only. No experiment was rerun, regenerated, retuned, or modified.

## GitHub Actions provenance

- workflow run ID: `32074736542`
- workflow artifact ID: `9303122672`
- artifact name: `experiment166-stronger-label-preserving-control`
- producing branch: `main`
- producing head SHA: `2a099bcfe339da876a7c5f0fb018c56f3776ecd9`
- artifact creation time: `2026-08-17T22:14:50Z`
- artifact expiration time: `2026-11-15T22:09:59Z`
- GitHub-reported artifact digest: `sha256:ced924c850aa5f6b5dd2923bcd6e761f00a3a15bbae620c639c4084fa876c904`

The artifact was downloaded through the GitHub connector. The downloaded ZIP independently hashed to:

`ced924c850aa5f6b5dd2923bcd6e761f00a3a15bbae620c639c4084fa876c904`

This exactly matches GitHub's recorded artifact digest.

## Preserved files

The verified archive contains:

- `summary.json`
- `summary.csv`
- `candidate_matching_diagnostics.csv`
- `paired_seed_results.csv`

## Verified summary fields

The preserved `summary.json` reports:

- status: `post_review_stronger_label_preserving_control`
- candidate count: `256`
- selected candidate index: `228`
- selected sigma: `4.0`
- selected replicate: `4`
- selected RNG seed: `16657228`
- historical poison mean exclusion Jaccard: `0.9238228511679869`
- stronger-control mean exclusion Jaccard: `0.9248528455086774`
- absolute mean-Jaccard mismatch: `0.0010299943406905099`
- historical poison membership switches: `308`
- stronger-control membership switches: `304`
- absolute switch mismatch: `4`
- match adequacy: `true`
- poison mean seed near-minus-far enrichment: `0.1362299667050161`
- stronger-control mean seed near-minus-far enrichment: `0.134384728609778`
- paired poison-minus-control mean: `0.0018452380952380949`
- seed-bootstrap 95% interval: `[0.0, 0.0055357142857142844]`
- bootstrap resamples: `10000`
- primary decision: `specificity_unresolved`
- poison fraction of switches near cutoff: `0.5032467532467533`
- stronger-control fraction of switches near cutoff: `0.5032894736842105`
- poison selected-action changes: `245`
- stronger-control selected-action changes: `243`

These values reproduce the manuscript-facing reconciliation numbers without relying on the earlier inadequate matched-control JSON committed under `results/audit/experiment_166_matched_nonpoison_control_result.json`.

## Seed-level preservation

`paired_seed_results.csv` preserves paired poison and stronger-control measurements by generation seed, including membership switches, exclusion Jaccard, near/far switch rates, the per-seed `D` enrichment quantities, selected-action changes, regret-related fields, score shifts, and the paired `S = D_poison - D_control` contrast.

This means the stronger-control publication comparison has both aggregate and seed-level preserved CI evidence available in the verified artifact.

## Adjudication

**DIRECT STRONGER-CONTROL CI PROVENANCE VERIFIED.**

The previous publication-packaging concern was discoverability, not scientific uncertainty about which numbers were produced. That provenance concern is now resolved for manuscript figure/table construction while the GitHub artifact remains retained. The artifact should still not be confused with the earlier inadequate-control result on `main`, and this verification note does not alter the historical experimental record.