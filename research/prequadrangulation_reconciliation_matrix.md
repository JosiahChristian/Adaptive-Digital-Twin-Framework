# Pre-Quadrangulation Reconciliation Matrix

## Purpose

This is a coordination artifact for reconciling independent reviews after they are returned. It does not alter scientific claims, experimental results, preregistrations, manuscript conclusions, or active experimental machinery.

## Freeze rule

Until the external Claude pre-quadrangulation review and the independent ChatGPT audit are both available, this matrix may be used to record provenance and review logistics only. Do not use it to promote/downgrade manuscript claims, launch remediation experiments, alter preregistered analyses, or rewrite the Abstract/Discussion/conclusion.

## Reviewer lanes

- **E — Experiment lane:** committed experimental artifacts and chronology.
- **S — Synthesis lane:** evidence/claim consistency and mechanistic challenge.
- **I — Independent audit lane:** literature, statistical/reporting, reproducibility, figures/tables audit.
- **C — Claude external lane:** independent hostile pre-quadrangulation review.

No finding is accepted by vote. Every finding is adjudicated against primary committed evidence.

## Finding matrix

| ID | Reviewer | Repository / experiment | Exact finding | Primary artifact(s) cited | Claim(s) affected | Severity proposed | New computation needed? | New experiment needed? | Documentation-only? | Cross-review agreement | Evidence-based disposition | Resolution artifact / commit | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | — | — | — | — | — | awaiting reviews |

## Allowed dispositions after both reviews arrive

- **ALREADY ADDRESSED** — primary evidence directly resolves the criticism.
- **VALID / UNRESOLVED** — criticism survives inspection and remains open.
- **PARTIALLY VALID** — core issue is real but scope/severity requires narrowing.
- **NOT SUPPORTED** — criticism conflicts with the committed evidence; rationale required.
- **ANALYSIS REQUIRED** — existing artifacts can adjudicate the issue without a new experiment.
- **NEW EXPERIMENT REQUIRED** — current evidence cannot resolve the issue prospectively.
- **WORDING / REPORTING CHANGE** — evidence is adequate but manuscript/documentation language is not.

## Adjudication fields required for every major or fatal finding

1. Exact reviewer statement, preserved without strengthening or weakening it.
2. Exact primary artifact and commit used to adjudicate it.
3. Whether the issue concerns design, implementation, inference, unit of analysis, reproducibility, interpretation, generalization, or reporting.
4. Whether the issue existed before outcomes were observed or arises from post-outcome interpretation.
5. Whether the proposed remedy can be performed on existing frozen artifacts or requires untouched data/new experimental machinery.
6. Minimum sufficient remedy; avoid expanding into a broad experiment program unless necessary.
7. Effect on manuscript claims, recorded only after the external and independent reviews are both reconciled.

## Experiment 166 mandatory reconciliation topics

These rows must be populated from the independent reviews rather than pre-decided here:

- structural/mathematical coupling of cutoff localization;
- structural/mathematical coupling of `net_unsafe_crossing` and `delta_unsafe_selected`;
- row/context/seed unit-of-analysis and dependence;
- Mantel–Haenszel appropriateness and variance assumptions;
- preregistration fidelity and chronology;
- generic ranking-instability alternative explanation;
- meaning of high exclusion-set Jaccard overlap;
- distinction among description, association, mediation, and causal mechanism;
- external/generalization limits.

## Claim-change lock

The manuscript Discussion, Abstract, conclusions, and strongest-claim ledger remain provisional until the external pre-quadrangulation review is reconciled with the independent audit and committed evidence. Negative, failed, partial, and non-replicating results must remain visible during reconciliation.
