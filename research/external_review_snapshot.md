# External Pre-Quadrangulation Review Snapshot

## Frozen reviewer snapshot

The external Claude pre-quadrangulation review should evaluate the repository state at:

`d1e3285707ed788a39c7e883c157a8a359cde7db`

Commit message: `Add external research review evidence index`

This SHA intentionally captures the reviewer-access index and the research package as it existed before the later independent-audit/synthesis updates. Later commits must not silently change the evidence target for Claude's first-pass review.

## SHA-pinned entry point

Raw evidence index:

`https://raw.githubusercontent.com/JosiahChristian/Adaptive-Digital-Twin-Framework/d1e3285707ed788a39c7e883c157a8a359cde7db/RESEARCH_REVIEW_INDEX.md`

GitHub snapshot:

`https://github.com/JosiahChristian/Adaptive-Digital-Twin-Framework/tree/d1e3285707ed788a39c7e883c157a8a359cde7db`

When following an evidence path listed in the index, replace `/main/` in a raw URL with `/d1e3285707ed788a39c7e883c157a8a359cde7db/` if necessary so the reviewed artifact remains pinned to this snapshot.

## Independence rule

The external reviewer should not be given conclusions from the later independent ChatGPT audit before completing the first-pass review. This allows convergence or disagreement on issues such as Experiment 166 structural coupling, unit of analysis, inferential assumptions, and preregistration fidelity to remain informative.

## Post-snapshot commits

Commits after the pinned SHA may contain audit, synthesis, documentation, or coordination changes. They are not part of the frozen first-pass external-review target. They may be introduced later during reconciliation as responses, independent findings, or updated documentation.

This snapshot pin does not freeze active experiments globally; it freezes only the evidence state being supplied to the external reviewer.
