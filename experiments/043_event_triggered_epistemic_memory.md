\# Experiment 043 — Event-Triggered Epistemic Memory



\## Objective



Determine whether an adaptive digital twin can autonomously identify a

diagnostically important event and use that inferred event location to anchor

epistemic memory.



Experiment 042 showed that retaining evidence around the known mismatch event

substantially improves long-horizon epistemic-state inference.



Experiment 043 removes the known event location from the memory-weighting rule

and replaces it with an event time inferred from trajectory-level estimator

signals.



\## Architecture



Three memory strategies were compared:



1\. uniform memory,

2\. oracle event-anchored memory,

3\. autonomously triggered event memory.



The oracle strategy uses the known mismatch event location and therefore serves

as a privileged benchmark.



The triggered strategy estimates an event location from the evolving

trajectory using a composite anomaly score derived from:



\- normalized innovation squared,

\- mismatch indicator,

\- parameter-update magnitude,

\- innovation magnitude.



The estimated event location is then used as the center of the same

event-anchored memory kernel validated in Experiment 042.



\## Important Limitation



Although the triggered memory rule does not receive the true event location,

the trigger detector still constructs its pre-event reference interval using

the known experimental event boundary.



Experiment 043 is therefore an intermediate event-localization experiment and

is not yet fully oracle-free.



\## Experimental Design



Four mismatch mechanisms were evaluated on held-out single trajectories.



Evidence horizons were



\\\[

t\\in\\{60,70,80,100\\}.

\\]



For each trajectory and horizon, epistemic-state inference was evaluated under

uniform, oracle-event, and triggered-event memory.



The experiment produced



\\\[

4800

\\]



held-out inference records.



\## Results



| Evidence time | Uniform MAE | Oracle-event MAE | Triggered-event MAE | Mean event-time error | Exact event localization |

|---:|---:|---:|---:|---:|---:|

| 60 | 0.0568 | 0.0572 | 0.0704 | 5.508 | 30.000% |

| 70 | 0.0612 | 0.0534 | 0.0690 | 6.383 | 28.750% |

| 80 | 0.0664 | 0.0527 | 0.0699 | 8.768 | 28.000% |

| 100 | 0.0751 | 0.0527 | 0.0706 | 13.010 | 27.250% |



\## Oracle Memory



The oracle event-anchored representation remained stable after sufficient

post-event evidence became available:



\\\[

0.0534

\\rightarrow

0.0527

\\rightarrow

0.0527.

\\]



This reproduces the principal result of Experiment 042: preserving

diagnostically salient event evidence prevents the epistemic degradation

observed under indiscriminate history accumulation.



\## Uniform Memory



Uniform memory degraded progressively:



\\\[

0.0568

\\rightarrow

0.0612

\\rightarrow

0.0664

\\rightarrow

0.0751.

\\]



This provides additional evidence that later adaptive behavior can dilute the

diagnostic information associated with the original mismatch.



\## Triggered Memory



Autonomously triggered memory produced approximately stable epistemic error:



\\\[

0.0704

\\rightarrow

0.0690

\\rightarrow

0.0699

\\rightarrow

0.0706.

\\]



However, it did not approach the oracle event-memory performance.



At the earlier horizons it also underperformed uniform memory.



Only at the longest tested horizon did triggered memory outperform uniform

aggregation:



\\\[

0.0706 < 0.0751

\\]



at \\(t=100\\).



Thus event-triggered memory is not yet validated as a superior inference

architecture.



\## Event Localization



The principal failure occurred in event localization.



Mean absolute event-time error increased with observation horizon:



\\\[

5.508

\\rightarrow

6.383

\\rightarrow

8.768

\\rightarrow

13.010.

\\]



Exact event localization remained low and decreased slightly:



\\\[

30.000\\%

\\rightarrow

28.750\\%

\\rightarrow

28.000\\%

\\rightarrow

27.250\\%.

\\]



Therefore the autonomous memory anchor becomes less accurately localized as

more trajectory history becomes available.



\## Interpretation



The current detector selects the largest anomaly score observed within the

available evidence prefix.



Conceptually,



\\\[

\\hat t\_e(t)

=

\\arg\\max\_{\\tau\\le t}

s\_\\tau.

\\]



This permits later residual, innovation, or adaptation excursions to replace

the original mismatch event as the memory anchor.



The increasing localization error strongly suggests that persistent epistemic

memory should not be based on repeated global maximization over the complete

history.



Instead, the architecture should distinguish between:



\\\[

\\text{detecting a new event}

\\]



and



\\\[

\\text{retaining an already detected event}.

\\]



A diagnostically important episode should become a persistent memory once its

evidence exceeds an appropriate trigger criterion.



\## Principal Result



Experiment 043 confirms that the event-memory mechanism itself remains useful,

as demonstrated by the oracle benchmark, but shows that the current autonomous

event detector is insufficient.



The failure is not primarily in memory weighting.



It is in localization and retention of the event anchor.



The result supports the architectural decomposition



\\\[

\\boxed{

\\text{event detection}

\\neq

\\text{event-memory retention}.

}

\\]



The twin requires a mechanism that detects the onset of a meaningful mismatch

and then preserves that event rather than continuously relocating its memory

toward whichever later observation is most anomalous.



\## Conclusion



Autonomous event-triggered epistemic memory did not reproduce the performance

of oracle event anchoring.



Event localization accuracy remained approximately 27–30%, while mean

localization error increased to 13 steps at the longest evidence horizon.



Nevertheless, triggered memory remained substantially more stable over time

than uniform-history inference and eventually outperformed uniform memory at

the longest horizon.



The experiment therefore identifies event localization and memory-anchor

persistence as the next architectural bottleneck.



\## Next Research Direction



The next experiment should replace global maximum-anomaly localization with an

online change-point trigger.



A candidate architecture is



\\\[

s\_t

\\rightarrow

\\text{threshold / persistence test}

\\rightarrow

\\hat t\_e

\\rightarrow

\\text{freeze memory anchor}.

\\]



Once an event has been accepted, the anchor should remain fixed unless a

separate reset or new-event criterion is satisfied.



The next experiment should also remove the remaining privileged baseline

segmentation so that event detection uses only information genuinely available

online.

