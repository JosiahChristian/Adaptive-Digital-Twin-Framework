\# Experiment 080 — Training-Support Epistemic Distance Analysis



\## Objective



Experiment 079 showed that within-random-forest ensemble dispersion does not identify the remaining harmful safe-action expansions.



The harmful cases were actually associated with:



\\\[

\\text{lower safety-model variance}

\\]



and



\\\[

\\text{lower downside-model variance}

\\]



than beneficial expansions.



This indicated that the failures were not ordinary ensemble-disagreement cases.



A new hypothesis was therefore introduced:



\\\[

\\boxed{

\\text{the harmful expansions may occur in regions with weak}

\\atop

\\text{direct training support.}

}

\\]



Experiment 080 tests that hypothesis using explicit feature-space support metrics.



The central question is



\\\[

\\boxed{

\\text{Are harmful high-confidence errors farther from the}

\\atop

\\text{meta-training distribution than beneficial expansions?}

}

\\]



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

| Support-model training | 53 |

| Held-out testing | 75 |



The cost-aware expansion operating point remained fixed at



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



Thus Experiment 080 analyzes the same 16 beneficial and 2 harmful expansion cases identified in Experiments 078 and 079.



\---



\## Action-Specific Feature Space



The analysis uses the same action-specific feature representation used by the learned action-safety and downside models.



For each action \\(a\\), the feature vector contains:



\- the original context features,

\- predicted under-persistence risk,

\- predicted losses for \\(k=1,2,3\\),

\- pairwise predicted-loss differences,

\- and action-specific terms.



Because these quantities have different numerical scales, the feature matrix is standardized using the meta-training distribution.



For feature \\(j\\),



\\\[

z\_j

=

\\frac{

x\_j-\\mu\_j

}{

\\sigma\_j

}.

\\]



All support distances are then computed in this standardized space.



\---



\## Nearest-Neighbor Distance



For each held-out action-specific sample \\(x\\), define



\\\[

d\_{\\text{NN}}(x)

=

\\min\_{x\_i\\in\\mathcal D\_{\\text{meta}}}

\\|x-x\_i\\|\_2.

\\]



This measures the distance to the closest meta-training example.



Small distance indicates strong direct training support.



Large distance indicates extrapolation.



\---



\## Mean k-Nearest-Neighbor Distance



The experiment also computes the average distance to the five nearest meta-training examples:



\\\[

d\_{5}(x)

=

\\frac{1}{5}

\\sum\_{i=1}^{5}

\\|x-x\_{(i)}\\|\_2.

\\]



This provides a more stable local support measure than nearest-neighbor distance alone.



\---



\## Local Safe Fraction



Among the five nearest training examples, the experiment computes the fraction whose action is truly safe:



\\\[

f\_{\\text{safe},5}(x)

=

\\frac{

\\#\\{\\text{safe neighbors}\\}

}{

5

}.

\\]



This tests whether harmful cases occur in locally ambiguous or locally unsafe regions.



\---



\## Distance to Safe and Unsafe Training Examples



Two additional quantities are measured:



\\\[

d\_{\\text{safe}}

=

\\min\_{x\_i:y\_i=1}

\\|x-x\_i\\|,

\\]



and



\\\[

d\_{\\text{unsafe}}

=

\\min\_{x\_i:y\_i=0}

\\|x-x\_i\\|.

\\]



Their difference defines a safe-distance advantage:



\\\[

\\Delta d

=

d\_{\\text{unsafe}}

\-

d\_{\\text{safe}}.

\\]



Positive values mean the sample is closer to a safe training example than to an unsafe one.



\---



\## Mahalanobis Distance



The experiment also computes Mahalanobis distance in standardized feature space:



\\\[

d\_M(x)

=

\\sqrt{

(x-\\mu)^T

\\Sigma^{-1}

(x-\\mu)

}.

\\]



This measures global atypicality relative to the joint covariance structure of the meta-training population.



\---



\## Support-Distance Results



The held-out support metrics were:



| Outcome | NN | 5-NN | Local Safe Fraction | Nearest Safe | Nearest Unsafe | Safe Advantage | Mahalanobis |

|---|---:|---:|---:|---:|---:|---:|---:|

| Beneficial | 1.769 | 2.557 | 0.625 | 1.826 | 2.737 | 0.911 | 3.299 |

| Neutral | 2.212 | 2.784 | 0.740 | 2.365 | 3.622 | 1.256 | 3.809 |

| Harmful | \*\*4.591\*\* | \*\*5.231\*\* | \*\*0.800\*\* | \*\*4.591\*\* | \*\*5.852\*\* | \*\*1.261\*\* | \*\*6.112\*\* |



This result strongly supports the training-support hypothesis.



\---



\## Nearest-Neighbor Separation



The harmful expansions had mean nearest-neighbor distance



\\\[

\\boxed{

4.591

}

\\]



compared with



\\\[

\\boxed{

1.769

}

\\]



for beneficial expansions.



Thus the harmful cases were approximately



\\\[

\\frac{4.591}{1.769}

\\approx

2.60

\\]



times farther from their nearest meta-training example.



This is a substantial separation.



\---



\## k-Nearest-Neighbor Separation



Mean five-neighbor distance showed the same pattern.



Beneficial expansions:



\\\[

d\_5

=

2.557.

\\]



Harmful expansions:



\\\[

\\boxed{

d\_5

=

5.231.

}

\\]



The harmful cases therefore lie in much more sparsely supported regions of feature space.



This result is stronger than the nearest-neighbor metric alone because it reflects broader local density rather than one isolated training example.



\---



\## Mahalanobis Separation



Mahalanobis distance also separates the groups.



Beneficial expansions had mean



\\\[

d\_M

=

3.299.

\\]



Harmful expansions had mean



\\\[

\\boxed{

d\_M

=

6.112.

}

\\]



Thus the harmful cases are globally atypical relative to the joint meta-training distribution.



The same conclusion is therefore supported by both:



\\\[

\\boxed{

\\text{local support distance}

}

\\]



and



\\\[

\\boxed{

\\text{global distribution distance}.

}

\\]



\---



\## Distance to Nearest Safe Example



The harmful cases were also much farther from their nearest known-safe meta-training example.



Beneficial:



\\\[

d\_{\\text{safe}}

=

1.826.

\\]



Harmful:



\\\[

\\boxed{

d\_{\\text{safe}}

=

4.591.

}

\\]



This is especially important because the action-safety classifier assigned the harmful cases high safe probabilities despite weak geometric support from actual safe examples.



\---



\## Local Safe Fraction Is Misleading



The local five-neighbor safe fraction was:



\\\[

0.625

\\]



for beneficial expansions but



\\\[

\\boxed{

0.800

}

\\]



for harmful expansions.



Therefore local class proportion alone does not identify the dangerous cases.



This is not a contradiction.



The harmful contexts can have a high safe-neighbor fraction while all of those neighbors are still far away.



Thus:



\\\[

\\boxed{

\\text{neighbor composition}

\\neq

\\text{neighbor proximity}.

}

\\]



A sparse remote region containing mostly safe labels can still provide weak evidence for generalization.



\---



\## Safe-Distance Advantage Is Also Insufficient



Safe-distance advantage was



\\\[

0.911

\\]



for beneficial cases and



\\\[

1.261

\\]



for harmful cases.



Thus the harmful contexts were relatively closer to safe examples than unsafe examples.



Again, this would appear reassuring if relative distance were considered alone.



However, both safe and unsafe training examples were far away.



This indicates that absolute support distance is more informative than relative class distance for these failures.



\---



\## Reconciliation With Experiment 079



Experiment 079 found that harmful cases had:



\\\[

\\text{low ensemble variance}

\\]



despite being wrong.



Experiment 080 now explains how that can occur.



The forests are extrapolating from a sparse region of training space.



Because all trees are trained from the same limited meta-training population and feature representation, they can agree strongly while still extrapolating incorrectly.



Therefore:



\\\[

\\boxed{

\\text{ensemble agreement}

\\not\\Rightarrow

\\text{strong training support}.

}

\\]



\---



\## Support Extrapolation as the Remaining Failure Mode



The two harmful cases now have a clear structural signature:



\\\[

\\boxed{

\\text{high safety confidence}

}

\\]



\\\[

\\boxed{

\\text{low predicted downside}

}

\\]



\\\[

\\boxed{

\\text{low ensemble variance}

}

\\]



but simultaneously



\\\[

\\boxed{

\\text{large training-support distance}.

}

\\]



This is characteristic of support extrapolation rather than ordinary model uncertainty.



The learned models are highly confident because they have learned a consistent mapping.



They are wrong because the held-out sample lies too far from the region in which that mapping was directly supported.



\---



\## Most Useful Support Signals



Among the tested metrics, the clearest separation appears in:



\\\[

\\boxed{

d\_{\\text{NN}}

}

\\]



\\\[

\\boxed{

d\_{5}

}

\\]



and



\\\[

\\boxed{

d\_M.

}

\\]



The harmful cases are substantially larger on all three metrics.



By contrast:



\- local safe fraction,

\- nearest-safe versus nearest-unsafe ordering,

\- and safe-distance advantage



do not distinguish them reliably.



This suggests future support gating should be based primarily on absolute distance or density.



\---



\## Candidate Support Gate



A support-aware expansion rule could extend the current cost-aware rule:



\\\[

\\hat p\_{\\text{safe}}(a)

\\geq

0.60,

\\]



\\\[

\\hat d(a)

\\leq

0.020,

\\]



with an additional requirement such as



\\\[

d\_5(x,a)

\\leq

\\tau\_{\\text{support}}.

\\]



Alternatively,



\\\[

d\_M(x,a)

\\leq

\\tau\_M.

\\]



The resulting rule would be



\\\[

\\boxed{

\\text{safe confidence}

\\land

\\text{low downside}

\\land

\\text{sufficient training support}.

}

\\]



\---



\## Support Threshold Selection



A useful next experiment should sweep several support thresholds rather than selecting one arbitrarily.



For example, k-nearest-neighbor thresholds could be chosen around the observed separation between beneficial and harmful cases.



Beneficial mean:



\\\[

2.557.

\\]



Harmful mean:



\\\[

5.231.

\\]



Therefore candidate thresholds might lie in the approximate region



\\\[

3

\\text{ to }

5\.

\\]



The important question is whether the harmful cases can be rejected without discarding many beneficial expansions.



\---



\## Structural Interpretation



Experiments 078–080 now form a clear uncertainty sequence.



\### Experiment 078



The remaining harmful expansions are high-confidence joint model failures.



\### Experiment 079



Random-forest ensemble dispersion does not identify them.



The harmful cases appear more certain than beneficial ones.



\### Experiment 080



Training-support distance does identify them.



The harmful cases are much farther from the meta-training distribution in both local and global feature-space geometry.



Therefore:



\\\[

\\boxed{

\\text{the relevant epistemic uncertainty signal is support distance,}

\\atop

\\text{not within-ensemble variance}.

}

\\]



\---



\## Principal Conclusion



Experiment 080 provides strong evidence that the remaining harmful expansions are support-extrapolation errors.



The harmful cases have:



\\\[

\\boxed{

d\_{\\text{NN}}

=

4.591

}

\\]



versus



\\\[

1.769

\\]



for beneficial expansions.



They have:



\\\[

\\boxed{

d\_5

=

5.231

}

\\]



versus



\\\[

2.557.

\\]



And they have:



\\\[

\\boxed{

d\_M

=

6.112

}

\\]



versus



\\\[

3.299.

\\]



Thus the harmful actions lie substantially farther from known meta-training support.



At the same time, their local safe-neighbor fraction remains high:



\\\[

0.800.

\\]



This shows that proximity, rather than nearby label composition alone, is the critical missing uncertainty signal.



The central conclusion is:



\\\[

\\boxed{

\\text{the surviving harmful expansions are best characterized as}

\\atop

\\text{training-support extrapolation failures}.

}

\\]



\---



\## Next Research Direction



Experiment 081 should convert the support-distance diagnostic into an execution gate.



The existing cost-aware conditions should remain:



\\\[

\\hat p\_{\\text{safe}}(a)

\\geq

0.60

\\]



and



\\\[

\\hat d(a)

\\leq

0.020.

\\]



A third support condition should then be added.



Candidate rules include:



\\\[

d\_5(x,a)

\\leq

\\tau\_k,

\\]



or



\\\[

d\_M(x,a)

\\leq

\\tau\_M.

\\]



Experiment 081 should sweep support thresholds and measure:



\- beneficial expansions retained,

\- harmful expansions rejected,

\- responsive-action retention,

\- safe-action recall,

\- safe-action precision,

\- policy mean regret,

\- under-persistence,

\- over-persistence,

\- action entropy,

\- expansion count,

\- recovered responsive contexts,

\- and harmful expansion count.



The primary goal is:



\\\[

\\boxed{

\\text{reject the two support-extrapolation failures while preserving}

\\atop

\\text{the majority of regret-free responsive expansions}.

}

\\]



The central question becomes



\\\[

\\boxed{

\\text{Can training-support-aware gating eliminate the remaining}

\\atop

\\text{harmful expansions without sacrificing the responsiveness gains?}

}

\\]

