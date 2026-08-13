\# Experiment 079 — Ensemble Uncertainty Safe-Action Analysis



\## Objective



Experiment 078 isolated the two harmful expansion contexts that survive the best cost-aware safe-action gate.



Those failures exhibited:



\\\[

\\text{high safety confidence}

\\]



and



\\\[

\\text{near-zero predicted downside}

\\]



despite substantial realized regret.



This suggested a possible uncertainty failure.



Because both the safety and downside models are random forests, Experiment 079 examines tree-to-tree prediction dispersion as an internal ensemble uncertainty signal.



For action-safety prediction, define



\\\[

\\mu\_p(a)

\\]



and



\\\[

\\sigma\_p(a),

\\]



where \\(\\mu\_p\\) is the mean tree-level safe-membership prediction and \\(\\sigma\_p\\) is the standard deviation across trees.



For downside prediction, define



\\\[

\\mu\_d(a)

\\]



and



\\\[

\\sigma\_d(a).

\\]



The experiment then constructs confidence-style bounds:



\\\[

LCB\_p(k)

=

\\mu\_p

\-

k\\sigma\_p

\\]



and



\\\[

UCB\_d(k)

=

\\mu\_d

\+

k\\sigma\_d.

\\]



The central question is



\\\[

\\boxed{

\\text{Do the harmful expansions exhibit greater ensemble uncertainty}

\\atop

\\text{than the beneficial expansions?}

}

\\]



If so, the uncertainty signal could be used as a conservative execution gate.



\---



\## Experimental Design



The experiment used generation seed



\\\[

44000

\\]



and generated



\\\[

249

\\]



decision contexts.



The partition remained:



| Partition | Contexts |

|---|---:|

| Base-model training | 121 |

| Uncertainty-model training | 53 |

| Held-out testing | 75 |



The action-expansion operating point was fixed at the best cost-aware configuration from Experiment 077:



\\\[

\\boxed{

\\tau\_p=0.60

}

\\]



and



\\\[

\\boxed{

\\tau\_d=0.020.

}

\\]



This ensures that Experiment 079 analyzes the same beneficial and harmful expansion regime identified in Experiments 077 and 078.



\---



\## Ensemble Safety Statistics



For each random-forest safety classifier, each tree produces an individual safe-membership prediction.



The mean tree prediction is



\\\[

\\mu\_p(a)

=

\\frac{1}{M}

\\sum\_{m=1}^{M}

p\_m(a).

\\]



The corresponding ensemble dispersion is



\\\[

\\sigma\_p(a)

=

\\sqrt{

\\frac{1}{M}

\\sum\_{m=1}^{M}

\\left(

p\_m(a)-\\mu\_p(a)

\\right)^2

}.

\\]



Large \\(\\sigma\_p\\) would indicate disagreement across trees.



Small \\(\\sigma\_p\\) would indicate ensemble consensus.



\---



\## Ensemble Downside Statistics



Similarly, each tree in the downside regressor produces a candidate downside prediction.



The ensemble mean is



\\\[

\\mu\_d(a)

=

\\frac{1}{M}

\\sum\_{m=1}^{M}

d\_m(a).

\\]



The ensemble standard deviation is



\\\[

\\sigma\_d(a).

\\]



If the harmful expansions were caused by uncertainty hidden by the point estimate, one would expect



\\\[

\\sigma\_d^{\\text{harmful}}

>

\\sigma\_d^{\\text{beneficial}}.

\\]



Experiment 079 tests this directly.



\---



\## Outcome Groups



The same outcome decomposition from Experiment 078 was retained:



| Outcome | Contexts |

|---|---:|

| Beneficial | 16 |

| Neutral | 57 |

| Harmful | 2 |



The analysis compares ensemble uncertainty across these three groups.



\---



\## Outcome Uncertainty Summary



The held-out results were:



| Outcome | Mean Safety | Safety Std | Mean Downside | Downside Std | Realized Regret |

|---|---:|---:|---:|---:|---:|

| Beneficial | 0.775 | 0.358 | 0.004266 | 0.011247 | 0.000000 |

| Neutral | 0.752 | 0.357 | 0.004431 | 0.006457 | 0.004142 |

| Harmful | \*\*0.873\*\* | \*\*0.296\*\* | \*\*0.000397\*\* | \*\*0.001538\*\* | \*\*0.035122\*\* |



These results reject the original hypothesis.



\---



\## Safety Uncertainty Result



The harmful expansions had lower safety-model dispersion:



\\\[

\\boxed{

\\sigma\_p^{\\text{harmful}}

=

0.296

}

\\]



compared with



\\\[

\\boxed{

\\sigma\_p^{\\text{beneficial}}

=

0.358.

}

\\]



Thus the safety ensemble is actually more internally consistent on the harmful cases.



The harmful contexts are not being flagged by tree disagreement.



Instead, the forest is making a relatively confident but incorrect prediction.



\---



\## Downside Uncertainty Result



The same pattern appears even more strongly for downside prediction.



Beneficial expansions had mean downside standard deviation



\\\[

0.011247.

\\]



Harmful expansions had mean downside standard deviation



\\\[

\\boxed{

0.001538.

}

\\]



Thus



\\\[

\\sigma\_d^{\\text{harmful}}

<

\\sigma\_d^{\\text{beneficial}}.

\\]



The harmful cases are not only assigned extremely low predicted downside.



The trees largely agree on that incorrect prediction.



\---



\## Confidence-Bound Sweep



The experiment evaluated



\\\[

k

\\in

\\{

0,\\,

0.25,\\,

0.50,\\,

0.75,\\,

1.00,\\,

1.25,\\,

1.50,\\,

2.00

\\}.

\\]



The resulting mean bounds were:



| \\(k\\) | Beneficial Safety LCB | Harmful Safety LCB | Beneficial Downside UCB | Harmful Downside UCB |

|---:|---:|---:|---:|---:|

| 0.00 | 0.775 | 0.873 | 0.004266 | 0.000397 |

| 0.25 | 0.685 | 0.800 | 0.007078 | 0.000781 |

| 0.50 | 0.596 | 0.726 | 0.009889 | 0.001166 |

| 0.75 | 0.506 | 0.652 | 0.012701 | 0.001550 |

| 1.00 | 0.416 | 0.578 | 0.015513 | 0.001935 |

| 1.25 | 0.327 | 0.504 | 0.018325 | 0.002319 |

| 1.50 | 0.237 | 0.430 | 0.021137 | 0.002703 |

| 2.00 | 0.058 | 0.282 | 0.026760 | 0.003472 |



The harmful expansions retain more favorable confidence bounds at every tested value of \\(k\\).



\---



\## Failure of Safety Lower Confidence Bounds



For all tested \\(k\\),



\\\[

\\boxed{

LCB\_p^{\\text{harmful}}

>

LCB\_p^{\\text{beneficial}}.

}

\\]



At



\\\[

k=1,

\\]



for example:



\\\[

LCB\_p^{\\text{harmful}}

=

0.578

\\]



while



\\\[

LCB\_p^{\\text{beneficial}}

=

0.416.

\\]



Thus a lower-confidence-bound safety rule would not preferentially reject the harmful cases.



It would tend to reject beneficial cases first.



\---



\## Failure of Downside Upper Confidence Bounds



The downside confidence bounds show the same problem.



For all tested \\(k\\),



\\\[

\\boxed{

UCB\_d^{\\text{harmful}}

<

UCB\_d^{\\text{beneficial}}.

}

\\]



At



\\\[

k=1,

\\]



the harmful mean upper bound is only



\\\[

0.001935,

\\]



while the beneficial mean upper bound is



\\\[

0.015513.

\\]



Therefore a downside upper-bound guard would also favor the harmful expansions.



This is the opposite of the desired behavior.



\---



\## Ensemble Confidence Is Misleading



Experiment 079 shows that the remaining harmful contexts are not uncertain according to within-forest dispersion.



They are instead cases where the ensemble is strongly self-consistent but wrong.



This can be summarized as



\\\[

\\boxed{

\\text{low ensemble variance}

\\not\\Rightarrow

\\text{correct prediction}.

}

\\]



The forest's internal agreement is not a reliable epistemic uncertainty measure for these failures.



\---



\## Why Tree Variance Fails



All trees in a random forest are trained from variations of the same underlying training population and feature representation.



If the local region of feature space is poorly represented or systematically misleading, many trees can learn the same incorrect relationship.



Thus bootstrap and feature randomness do not guarantee that ensemble dispersion captures model ignorance.



The harmful contexts appear consistent with this type of failure.



\---



\## Likely Failure Modes



The results suggest several possibilities.



\### Insufficient Training Support



The harmful contexts may lie far from the 53-context meta-training distribution.



If so, all trees are extrapolating from weak local support.



\### Representation Error



The available features may fail to encode a latent variable that determines the true downside.



In that case, the models can confidently assign the wrong label because the observable representation aliases distinct physical states.



\### Local Data Sparsity



The harmful contexts may occupy a region represented by only a small number of similar training points.



Random-forest consensus can still occur in such a region even when generalization is unreliable.



\---



\## Epistemic Uncertainty Versus Ensemble Dispersion



Experiment 079 demonstrates that



\\\[

\\boxed{

\\text{ensemble dispersion}

\\neq

\\text{epistemic uncertainty}

}

\\]



in this setting.



Tree-to-tree variation measures disagreement within the learned ensemble.



It does not necessarily measure distance from known training support.



A more direct epistemic quantity should therefore consider the geometry of the training data.



\---



\## Training-Support Distance



A natural next diagnostic is nearest-neighbor distance in the learned feature space.



For a test context \\(x\\), define



\\\[

d\_{\\text{NN}}(x)

=

\\min\_{x\_i\\in\\mathcal D\_{\\text{meta}}}

\\|x-x\_i\\|.

\\]



A k-nearest-neighbor version can also be defined:



\\\[

d\_k(x)

=

\\frac{1}{k}

\\sum\_{i=1}^{k}

\\|x-x\_{(i)}\\|.

\\]



If harmful contexts have larger support distance than beneficial ones, this would provide a more useful epistemic uncertainty signal.



\---



\## Feature-Space Scaling



Because the feature vector contains heterogeneous quantities, raw Euclidean distance may be misleading.



A standardized feature representation should therefore be used.



For each feature \\(j\\),



\\\[

z\_j

=

\\frac{

x\_j-\\mu\_j

}{

\\sigma\_j

}.

\\]



Distances should then be measured in standardized space.



This prevents high-scale features from dominating the metric.



\---



\## Mahalanobis Distance



Another candidate support metric is Mahalanobis distance:



\\\[

d\_M(x)

=

\\sqrt{

(x-\\mu)^T

\\Sigma^{-1}

(x-\\mu)

}.

\\]



This accounts for feature covariance.



If the harmful contexts lie in unusual combinations of otherwise common feature values, Mahalanobis distance may detect them more effectively than nearest-neighbor distance.



\---



\## Structural Interpretation



Experiments 077–079 now establish a precise progression.



\### Experiment 077



Cost-aware gating reduces severe false-positive expansions.



\### Experiment 078



The remaining harmful cases are joint high-confidence prediction failures.



\### Experiment 079



Random-forest tree dispersion does not reveal those failures.



The harmful cases are actually more internally certain than the beneficial ones.



Therefore the remaining uncertainty problem is likely related to training support or representation rather than ensemble disagreement.



\---



\## Principal Conclusion



Experiment 079 decisively rejects within-random-forest variance as the appropriate uncertainty signal for the remaining harmful expansions.



Harmful contexts have:



\\\[

\\boxed{

\\text{lower safety dispersion}

}

\\]



and



\\\[

\\boxed{

\\text{lower downside dispersion}

}

\\]



than beneficial contexts.



Their confidence bounds remain more favorable at every tested uncertainty multiplier.



Therefore:



\\\[

\\boxed{

\\text{confidence-bound filtering based on tree variance would not solve}

\\atop

\\text{the remaining harmful expansions and may reject useful cases first.}

}

\\]



The next diagnostic should measure training-support distance directly.



\---



\## Next Research Direction



Experiment 080 should analyze support-aware epistemic distance.



Using the same action-specific feature vectors employed by the safety and downside models, the experiment should standardize the meta-training features and compute for each held-out expansion candidate:



\- nearest-neighbor distance,

\- mean distance to the \\(k\\) nearest neighbors,

\- local neighbor density,

\- Mahalanobis distance,

\- training-label agreement among nearby neighbors,

\- and distance to nearest safe and unsafe examples.



The analysis should compare:



\\\[

\\text{beneficial}

\\]



versus



\\\[

\\text{harmful}

\\]



expansions.



The central hypothesis becomes



\\\[

\\boxed{

\\text{harmful high-confidence errors occur farther from reliable}

\\atop

\\text{training support than beneficial expansions}.

}

\\]



If supported, the next controller can incorporate a support-aware epistemic gate that rejects actions when local training support is insufficient even when safety and downside models appear highly confident.

