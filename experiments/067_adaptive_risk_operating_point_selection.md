\# Experiment 067 — Adaptive Risk Operating-Point Selection



\## Objective



Determine whether persistence-control risk sensitivity should itself become a

context-dependent adaptive decision variable.



Experiment 066 established that persistence policies form a robust

safety–responsiveness Pareto structure across genuinely different generated

trajectory populations.



However, the previous experiments still selected one global risk multiplier



\\\[

\\lambda

\\]



for all decision contexts.



Experiment 067 therefore investigates



\\\[

\\lambda\_t

=

\\pi\_{\\text{risk}}(z\_{1:t},M\_t,\\hat r\_t),

\\]



where the digital twin selects its persistence-risk operating point from the

current epistemic context.



The central question is



\\\[

\\boxed{

\\text{Can the twin become conservative only when necessary}

}

\\]



while remaining responsive when additional persistence protection provides no

benefit?



\---



\## Experimental Design



The experiment used generation seed



\\\[

44000

\\]



and produced



\\\[

249

\\]



persistence-decision contexts.



A three-way data partition was used:



| Partition | Contexts |

|---|---:|

| Base-model training | 121 |

| Operating-point selector training | 53 |

| Held-out testing | 75 |



The base-training partition was used to learn:



\- persistence-action loss models,

\- under-persistence risk occurrence,

\- and under-persistence risk magnitude.



A separate selector-training partition was then used to learn which risk

operating point was preferable in each context.



The held-out test partition was not used for either training stage.



This separation prevents the operating-point selector from being trained on

the same observations used to fit its underlying loss and risk models.



\---



\## Candidate Risk Operating Points



The available risk strengths were



\\\[

\\lambda

\\in

\\{

0,\\,

0.10,\\,

0.25,\\,

1.00

\\}.

\\]



Here,



\\\[

\\lambda=0

\\]



corresponds to direct predicted-loss minimization.



Increasing \\(\\lambda\\) progressively increases the penalty associated with

predicted under-persistence risk.



Thus the action space for Experiment 067 is no longer simply persistence depth.



The controller first selects a risk posture and that posture subsequently

determines the persistence action.



\---



\## Operating-Point Selector



The learned selector achieved exact risk-level classification accuracy of



\\\[

\\boxed{

65.333\\%

}.

\\]



Its mean selected risk strength was



\\\[

\\bar{\\lambda}\_{\\text{learned}}

=

0.2547,

\\]



compared with



\\\[

\\bar{\\lambda}\_{\\text{oracle}}

=

0.1673.

\\]



The learned selector was therefore more conservative on average than the

context-wise oracle.



\---



\## Selected Operating-Point Distribution



The learned policy selected:



| Risk strength | Count | Fraction |

|---:|---:|---:|

| \\(0.00\\) | 49 | 65.333% |

| \\(0.10\\) | 6 | 8.000% |

| \\(0.25\\) | 2 | 2.667% |

| \\(1.00\\) | 18 | 24.000% |



The oracle operating-point distribution was:



| Risk strength | Count | Fraction |

|---:|---:|---:|

| \\(0.00\\) | 56 | 74.667% |

| \\(0.10\\) | 3 | 4.000% |

| \\(0.25\\) | 5 | 6.667% |

| \\(1.00\\) | 11 | 14.667% |



Both policies therefore exhibit genuinely context-dependent operating-point

selection.



Neither collapses to one global value of \\(\\lambda\\).



The oracle result is particularly informative because nearly three quarters of

contexts prefer



\\\[

\\lambda=0.

\\]



Consequently, strong risk protection is useful selectively rather than

universally.



\---



\## Policy Performance



The principal held-out results were:



| Policy | Mean regret | Zero regret | Under | Over | Entropy |

|---|---:|---:|---:|---:|---:|

| Direct loss | 0.014317 | 70.667% | 22 | 26 | 0.871 |

| Fixed \\(\\lambda=0.10\\) | 0.013249 | 74.667% | 19 | 34 | 0.972 |

| Fixed \\(\\lambda=0.25\\) | 0.009923 | 81.333% | 14 | 44 | 0.908 |

| Fixed \\(\\lambda=1.00\\) | 0.001460 | 93.333% | 3 | 64 | 0.190 |

| Adaptive \\(\\lambda\\) | 0.007043 | 80.000% | 13 | 38 | 1.000 |

| Oracle \\(\\lambda\\) | 0.001372 | 94.667% | 3 | 35 | 0.998 |

| Fixed \\(k=3\\) | 0.000300 | 96.000% | 0 | 65 | 0.000 |

| Action oracle | 0.000000 | 100.000% | 0 | 0 | 0.883 |



\---



\## Improvement Over Direct Loss Control



Adaptive operating-point selection reduced mean regret from



\\\[

0.014317

\\]



for direct loss control to



\\\[

0.007043.

\\]



This corresponds to an approximate reduction of



\\\[

\\boxed{

50.8\\%

}

\\]



in mean regret.



Under-persistence decisions were reduced from



\\\[

22

\\]



to



\\\[

13,

\\]



an approximate reduction of



\\\[

\\boxed{

40.9\\%

}.

\\]



The fraction of zero-regret decisions increased from



\\\[

70.667\\%

\\]



to



\\\[

80.000\\%.

\\]



Thus learned operating-point adaptation provides a substantial improvement over

unprotected direct loss minimization.



\---



\## Responsiveness Preservation



The learned adaptive policy achieved action entropy



\\\[

\\boxed{

H=0.9995

}

\\]



with a dominant-action fraction of only



\\\[

34.667\\%.

\\]



This is the highest action entropy among the evaluated non-oracle policies.



Therefore the improvement in safety was not obtained by collapsing onto one

conservative persistence action.



This sharply contrasts with fixed three-step persistence:



\\\[

H\_{k=3}=0.

\\]



Fixed \\(k=3\\) achieved extremely low regret and eliminated under-persistence,

but did so through complete action collapse.



The learned adaptive policy instead retained substantial context-dependent

variation.



\---



\## Comparison With Strong Fixed Risk Control



Fixed



\\\[

\\lambda=1.00

\\]



achieved mean regret



\\\[

0.001460

\\]



and only



\\\[

3

\\]



under-persistence decisions.



This substantially outperformed the learned adaptive selector on raw safety and

regret.



However, its action entropy was only



\\\[

0.1895,

\\]



and one persistence action accounted for



\\\[

94.667\\%

\\]



of decisions.



Thus strong fixed risk sensitivity approaches a nearly collapsed conservative

controller.



The comparison exposes the continuing tradeoff:



\\\[

\\boxed{

\\text{low regret and strong safety}

\\quad\\leftrightarrow\\quad

\\text{adaptive responsiveness}.

}

\\]



\---



\## Oracle Operating-Point Result



The most important result is produced by the oracle operating-point selector.



Oracle-\\(\\lambda\\) achieved



\\\[

\\boxed{

R=0.001372

}

\\]



with



\\\[

94.667\\%

\\]



zero-regret decisions and only



\\\[

3

\\]



under-persistence decisions.



At the same time, it maintained action entropy



\\\[

\\boxed{

H=0.9981

}

\\]



and a dominant-action fraction of only



\\\[

36.0\\%.

\\]



This result is fundamentally different from fixed conservative persistence.



It demonstrates that near-conservative safety can coexist with extremely high

action diversity when the correct risk operating point is selected

contextually.



Therefore the limitation observed in the learned adaptive policy is not caused

by the candidate operating-point architecture.



It is caused primarily by imperfect operating-point selection.



\---



\## Oracle Gap



The learned adaptive policy achieved



\\\[

R\_{\\text{adaptive}}

=

0.007043,

\\]



while the oracle operating-point policy achieved



\\\[

R\_{\\text{oracle-}\\lambda}

=

0.001372.

\\]



The difference is approximately



\\\[

0.005672.

\\]



Thus a substantial amount of achievable performance remains unrealized by the

current selector.



The selector's



\\\[

65.333\\%

\\]



exact classification accuracy is therefore not sufficient to characterize its

decision quality.



Some operating-point classification errors are effectively harmless, while

others produce substantial persistence regret.



This implies that operating-point selection is an asymmetric decision problem.



\---



\## Classification Is Not the Correct Objective



Experiment 067 reveals a structural problem with treating risk operating-point

selection as ordinary classification.



The classifier is trained to predict



\\\[

\\lambda\_t^\*,

\\]



but classification loss treats every incorrect risk label similarly.



Persistence-control consequences do not.



For example, selecting a neighboring operating point that produces the same

persistence action may incur zero regret.



Conversely, selecting an insufficiently conservative operating point in a

high-risk context can produce substantial regret.



Therefore



\\\[

\\boxed{

\\text{operating-point classification error}

\\neq

\\text{operating-point decision regret}.

}

\\]



This mirrors the earlier persistence-policy result in which exact-label

prediction was inferior to direct consequence prediction.



\---



\## Interpretation



Experiment 067 establishes that context-dependent risk allocation is viable in

principle.



The learned controller successfully uses multiple risk operating points and

improves substantially over direct loss minimization while preserving very high

action diversity.



However, ordinary classification does not recover the full value available

from the operating-point action space.



The oracle result demonstrates the latent opportunity:



\\\[

\\boxed{

\\text{near-conservative safety}

\+

\\text{high responsiveness}

}

\\]



is achievable when the correct risk posture is selected.



The remaining research problem is therefore not whether adaptive risk

allocation is useful.



It is how to learn the consequences of alternative risk allocations accurately

enough to choose among them.



\---



\## Principal Conclusion



Experiment 067 advances persistence control from a fixed global risk posture to

context-dependent risk allocation.



The learned adaptive selector reduced regret and under-persistence relative to

direct loss control while maintaining nearly maximal action entropy.



However, it remained substantially inferior to both strong fixed risk control

and the oracle operating-point selector in raw regret.



Most importantly, oracle operating-point selection simultaneously achieved



\\\[

R=0.001372

\\]



and



\\\[

H=0.9981.

\\]



Therefore,



\\\[

\\boxed{

\\text{safe persistence does not inherently require policy collapse}.

}

\\]



The correct context-dependent risk allocation can preserve responsiveness while

approaching conservative safety.



The current bottleneck is the learning objective used to select that operating

point.



\---



\## Next Research Direction



Experiment 068 should replace exact operating-point classification with direct

contextual consequence estimation.



For every candidate



\\\[

\\lambda

\\in

\\{

0,\\,

0.10,\\,

0.25,\\,

1.00

\\},

\\]



the controller should estimate a context-conditioned quantity such as



\\\[

\\hat J\_t(\\lambda)

=

\\mathbb{E}

\\left\[

R\_t(\\lambda)

\\mid

z\_{1:t},M\_t

\\right].

\\]



The selected operating point should then satisfy



\\\[

\\lambda\_t

=

\\arg\\min\_{\\lambda}

\\hat J\_t(\\lambda).

\\]



This changes the learning problem from



\\\[

\\boxed{

\\text{Which risk label is correct?}

}

\\]



to



\\\[

\\boxed{

\\text{What is the expected consequence of each risk posture?}

}

\\]



The objective of Experiment 068 is therefore to determine whether direct

regret-aware operating-point selection can close the gap between the learned

adaptive controller and the oracle-\\(\\lambda\\) policy while retaining the

high responsiveness demonstrated in Experiment 067.

