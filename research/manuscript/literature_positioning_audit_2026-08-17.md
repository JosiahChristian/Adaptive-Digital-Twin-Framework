# Literature Positioning Audit — 2026-08-17

**Status:** review-branch manuscript support record. External literature provides context only and cannot supersede committed ADT experimental adjudications.

## Governing rule

For every manuscript statement, distinguish:

- **external methodological context** — what prior literature establishes generally;
- **internal empirical evidence** — what the ADT artifacts establish in this pipeline;
- **prohibited inference** — claims that cannot be imported from the literature into the ADT result.

## Source-to-claim map

### Adaptive digital twins and decision support

**Sources:** Qiu et al. (2025); Splettstößer, Ellwein & Wortmann (2023); Builes-Montaño et al. (2025).

**Permitted use:** demonstrate that digital-twin research includes adaptive control, self-adaptive architectures, and decision-support applications.

**Not permitted:** infer deployment validity, biomedical validity, automotive validity, or real-world effectiveness for the present ADT framework.

### Predict-then-optimize / decision-focused learning

**Sources:** Elmachtoub & Grigas (2022); Elmachtoub, Liang & McNellis (2020); Mandi et al. (2022); Heuton et al. (2025).

**Permitted use:** establish that downstream decision quality can be a distinct objective from conventional prediction error and that top-K intervention is a recognized decision setting.

**Not permitted:** claim that these papers prove the ADT prediction-decision findings, validate Experiment 166, or establish a general ADT law.

### Top-K boundary separation and ranking stability

**Sources:** Chen & Suh (2015); Asudeh et al. (2018).

**Permitted use:** establish that top-K identification can depend on score separation near the K/K+1 boundary and that ranking stability under small scoring-rule changes is a studied problem.

**Not permitted:** claim that Experiment 166 is mathematically forced by top-K ranking, that the matched-control result proves a universal ranking law, or that poisoning has no possible specific effect.

### Prediction-time leakage

**Source:** Kapoor & Narayanan (2023).

**Permitted use:** establish that data leakage can inflate ML-based scientific claims and that information availability is a core validity issue.

**Not permitted:** use the paper as evidence that the ADT harmful-expansion model leaks. That finding comes from the committed feature definitions and timing audit.

## Citation verification notes

- Qiu et al.: Scientific Reports 15, 11078 (2025), DOI 10.1038/s41598-025-91243-1.
- Splettstößer, Ellwein & Wortmann: Procedia CIRP 119, 867-872 (2023), DOI 10.1016/j.procir.2023.03.131.
- Builes-Montaño et al.: Scientific Reports 15, 39738 (2025), DOI 10.1038/s41598-025-23165-x.
- Elmachtoub & Grigas: Management Science 68(1), 9-26, DOI 10.1287/mnsc.2020.3922.
- Mandi et al., Heuton et al., Chen & Suh: bibliographic metadata taken from the corresponding PMLR proceedings records.
- Asudeh et al.: Proceedings of the VLDB Endowment 12(3), 237-250 (2018).
- Kapoor & Narayanan: Patterns 4(9), 100804 (2023), DOI 10.1016/j.patter.2023.100804.

## Adjudication

The literature-positioning pass introduces no new empirical support for poisoning specificity, causal mechanism, or prospective harmful-expansion prediction. It provides a defensible scholarly frame for the already-narrowed manuscript claims and explicitly preserves competing explanations and scope limitations.
