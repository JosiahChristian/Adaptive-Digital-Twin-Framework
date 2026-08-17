# Research Problem Definition

## Core problem

An adaptive digital twin must decide when and how to update its internal representation as the observed system evolves. Adaptation is useful only if the twin can distinguish changes that improve future prediction or control from changes that introduce persistent error, unsafe behavior, or misleading confidence.

The research problem is therefore not simply to make a model adaptive. It is to determine whether **pre-decision information available to the twin can identify when an adaptation is likely to become harmful, and whether that information remains useful under population shift, alternative decision rules, and adversarial perturbation.**

## Primary research question

**Which pre-decision signals, if any, reliably predict harmful adaptive actions before their downstream consequences are observed?**

This question is deliberately narrower than asking whether an adaptive digital twin can be made universally safe or optimal.

## Current candidate mechanism

The strongest current evidence points toward compact loss-surface information available before an action-space expansion decision. In the documented generated event population, features derived from predicted loss and loss-floor error discriminate harmful from beneficial expansion events substantially better than simple support-distance representations.

This is a candidate predictive mechanism, not yet a general law. It must survive stronger held-out populations, timing/leakage audits, alternative harm definitions, calibration changes, and competing feature sets.

## Secondary research questions

1. **Generalization:** Does the pre-decision signal survive genuinely held-out generated populations and operating-condition shifts?
2. **Decision coupling:** When predictive quality changes, how reliably do downstream fixed-budget intervention outcomes change with it?
3. **Adversarial sensitivity:** Can small perturbations alter adaptation/intervention decisions without producing correspondingly large changes in global predictive metrics?
4. **Persistence:** Which induced adaptive effects remain after the initiating condition or intervention ends?
5. **Failure boundaries:** Under which actions, budgets, populations, or model classes does an apparent predictive mechanism weaken, reverse, or disappear?

## Evidence hierarchy

The program should distinguish four levels of evidence:

1. **Association in one generated population** — useful for hypothesis generation only.
2. **Held-out predictive evidence** — supports a bounded predictive claim when calibration and test data are separated.
3. **Prospective/shifted replication** — supports a stronger generalization claim within the tested family of populations.
4. **Cross-domain recurrence** — supports a broader computational phenomenon only when the phenomenon and success criteria are fixed before evaluating the new domain.

Movement upward in this hierarchy requires new evidence; strong metrics at a lower level cannot substitute for the missing validation.

## What would falsify the current candidate story?

The loss-surface candidate should be weakened or abandoned if, under properly separated evaluation, any of the following becomes the dominant pattern:

- performance collapses on fresh generated populations;
- predictive power disappears after correcting feature timing or leakage;
- a substantially simpler baseline explains the same signal;
- results depend critically on one harm threshold or event definition;
- action/block conditioning removes the apparent effect;
- calibration is unstable enough to make the classifier operationally meaningless;
- the signal fails repeatedly under modest distribution shifts.

A falsification is a research result, not a reason to remove the experiment from the record.

## Relationship to adversarial-RL research

Adaptive-Digital-Twin-Framework and Adversarial-RL-Data-Poisoning-Thesis are related but distinct programs. ADT asks how adaptation can be predicted, evaluated, and constrained in evolving computational twins. The adversarial-RL thesis asks when controlled poisoning can induce persistent, difficult-to-detect behavioral changes in learned policies and how such changes can be detected before gross failure.

Shared methods—held-out evaluation, preregistration, attack/perturbation analysis, decision-aware metrics, and falsification—can inform both programs without merging their claims.

## Domain boundaries

Aerospace, autonomous-guidance, and biomedical simulations are computational environments for testing methods and generalization. Evidence obtained in these environments does not by itself establish deployment readiness, vehicle safety, medical-device performance, or clinical applicability.

In particular, any later biomedical-control study should be treated as a bounded **simulated cross-domain validation environment** unless substantially stronger evidence and appropriate domain supervision justify a different interpretation.

## Current research objective

The immediate objective is to determine whether the strongest compact pre-decision signal survives the falsification gates documented in `publication_candidate.md` and `claim_ledger.md`, while retaining negative results on support distance, transfer failure, poisoning boundary effects, and prediction-versus-decision behavior as constraints on the eventual scientific claim.
