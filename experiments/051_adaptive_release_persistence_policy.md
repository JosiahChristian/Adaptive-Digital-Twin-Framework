\# Experiment 051 — Adaptive Release-Persistence Policy



\## Objective



Determine whether release-confirmation depth can itself be learned as an

adaptive decision variable rather than fixed globally.



Experiment 050 demonstrated a responsiveness–retention tradeoff between

confirmation depths



\[

k\\in{1,2,3}.

]



Immediate release confirmation improved intermediate-horizon epistemic

accuracy, while stronger persistence substantially reduced premature release

and produced the best long-horizon result.



Experiment 051 therefore learns an adaptive release-persistence policy



\[

k\_t

===



\\pi\_{\\text{release persistence}}

(z\_{1:t},M\_t),

]



allowing the digital twin to select the amount of release confirmation required

from its current epistemic and memory context.



\## Training Target Distribution



The learned persistence-policy training targets were:



| Persistence depth | Training targets |

| ----------------: | ---------------: |

|             (k=1) |              172 |

|             (k=2) |               62 |

|             (k=3) |               15 |



The target distribution is strongly weighted toward immediate release

confirmation, but includes examples requiring both moderate and strong

persistence.



This establishes that the training data contain nontrivial variation in the

preferred release-confirmation depth.



\## Principal Results



Epistemic MAE was:



| Evidence time | Fixed (k=1) | Fixed (k=2) | Fixed (k=3) | Adaptive persistence |

| ------------: | ----------: | ----------: | ----------: | -------------------: |

|            60 |      0.0560 |      0.0560 |      0.0560 |           \*\*0.0560\*\* |

|            70 |  \*\*0.0564\*\* |      0.0574 |      0.0574 |               0.0574 |

|            80 |  \*\*0.0576\*\* |      0.0579 |      0.0586 |               0.0577 |

|           100 |      0.0591 |      0.0590 |  \*\*0.0577\*\* |               0.0588 |



At (t=60), all persistence strategies were equivalent.



At (t=70), the adaptive policy matched the more persistent fixed strategies

but did not recover the advantage of immediate release.



At (t=80), the adaptive policy achieved



\[

MAE=0.0577,

]



which was close to the best fixed result of 0.0576 and better than fixed

(k=2) and (k=3).



At (t=100), adaptive persistence achieved



\[

MAE=0.0588,

]



improving over fixed (k=1), but remaining above the best result of



\[

\\boxed{

MAE\_{t=100}=0.0577

}

]



obtained by fixed (k=3).



\## Adoption Behavior



Memory-adoption rates were:



| Evidence time | Fixed (k=1) | Fixed (k=2) | Fixed (k=3) | Adaptive persistence |

| ------------: | ----------: | ----------: | ----------: | -------------------: |

|            60 |     16.250% |     16.250% |     16.250% |              16.250% |

|            70 |     29.000% |     32.000% |     32.000% |              32.000% |

|            80 |     31.250% |     36.250% |     39.000% |              37.500% |

|           100 |     36.750% |     42.750% |     47.750% |              44.750% |



The adaptive policy progressively moved away from the low-persistence behavior

of fixed (k=1) as the evidence horizon increased.



At (t=80), its adoption rate fell between fixed (k=2) and fixed (k=3).



At (t=100), adaptive persistence again occupied an intermediate position:



\[

42.750%

<

44.750%

<

47.750%.

]



Thus the learned policy does not merely reproduce one fixed confirmation depth.



\## Adaptive Persistence Selection



Across adaptive decisions, the learned policy selected:



| Selected persistence | Count |

| -------------------: | ----: |

|                (k=1) |   286 |

|                (k=2) |   130 |

|                (k=3) |   128 |



The policy therefore actively used all three available persistence depths.



Although (k=1) remained the most frequent choice, the combined number of

(k=2) and (k=3) selections was substantial:



\[

130+128=258.

]



This indicates that the learned controller identified a meaningful subset of

states in which stronger temporal confirmation was preferred.



\## Interpretation



Experiment 051 demonstrates that release persistence is learnable as a

state-dependent control variable.



The learned policy does not collapse to a single global persistence setting.

Instead, it switches among immediate, moderate, and strong confirmation

requirements according to the observed trajectory and epistemic-memory state.



However, adaptive selection does not yet consistently outperform the best

fixed persistence depth.



The results expose a distinction between two questions:



\[

\\boxed{

\\text{Can the preferred persistence depth vary by state?}

}

]



and



\[

\\boxed{

\\text{Can that variation be learned reliably enough to improve performance?}

}

]



Experiment 051 provides evidence for the first, but only partial evidence for

the second.



The adaptive controller performs close to the fixed-policy envelope at several

horizons, particularly at (t=80), but does not consistently identify the

horizon-specific best action.



This suggests that the limiting factor may no longer be the release-control

architecture itself, but the statistical separability of the persistence

decisions available to the learner.



\## Principal Conclusion



Adaptive release persistence is feasible and produces nontrivial

state-dependent confirmation behavior.



The learned controller uses all three persistence depths and interpolates

between the responsiveness of immediate release and the retention stability of

strong confirmation.



However, the adaptive policy does not dominate the best fixed persistence

policy.



Its performance indicates that some persistence decisions may be only weakly

distinguishable from one another under the available evidence.



Therefore the next question is not simply whether persistence depth can be

predicted.



It is whether the performance differences between competing persistence

actions are sufficiently large and sufficiently observable to be learnable.



\## Next Research Direction



Experiment 052 should quantify the \*\*learnability margin\*\* of the persistence

policy.



For each decision state, define the difference between the best persistence

action and its nearest competitor through an action-value or loss margin such

as



\[

\\Delta\_t

========



\## L\_t^{(2)}



L\_t^{(1)},

]



where (L\_t^{(1)}) is the loss associated with the best persistence decision

and (L\_t^{(2)}) is the loss of the second-best decision.



Small values of



\[

\\Delta\_t

]



indicate intrinsically ambiguous decisions in which multiple persistence

actions produce nearly equivalent outcomes.



Large margins indicate states in which the preferred action should be

statistically easier to learn.



Experiment 052 should therefore determine whether the remaining performance

gap of adaptive release persistence is caused primarily by model inadequacy or

by weak intrinsic separation between competing persistence decisions.



