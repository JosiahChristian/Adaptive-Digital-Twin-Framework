\# Experiment 091 — Support Metric Action-Conditionality Audit



\## Objective



Experiment 091 audits the mathematical interpretation of the support-distance representation used in the preceding safe-action-expansion experiments.



Experiment 090 identified an important structural clue:



\\\[

d(x,k\_1)

=

d(x,k\_2)

=

d(x,k\_3)

\\]



at the aggregate level.



The purpose of Experiment 091 is to determine whether this equality also holds context by context and, if so, why.



The audit addresses four questions:



1\. Does the current support representation produce action-dependent distances?

2\. Do the appended action coordinates survive action-specific standardization?

3\. Does replacing the separate action scalers with one shared scaler restore action dependence?

4\. What scientific interpretation should be assigned to the support metric used in the previous experiments?



No controller policy is changed.



No new prospective validation block is consumed.



This is an implementation and representation audit.



\---



\# Audit Population



The audit uses three previously consumed generation seeds:



\\\[

44000,

\\]



\\\[

44011,

\\]



and:



\\\[

44031\.

\\]



These seeds sample three different portions of the existing experimental history without consuming new prospective seeds.



The resulting test population contains:



\\\[

\\boxed{

237

}

\\]



contexts.



For every context, support distance is calculated separately for:



\\\[

k\_1,\\quad k\_2,\\quad k\_3.

\\]



\---



\# Current Support Construction



The existing support representation begins with a context/model feature vector:



\\\[

\\phi(x).

\\]



It then appends three action coordinates:



\\\[

a,

\\]



\\\[

a-1,

\\]



and:



\\\[

3-a.

\\]



Thus the nominal action-specific representation is:



\\\[

z(x,a)

=

\[

\\phi(x),

a,

a-1,

3-a

].

\\]



Separate support matrices are then constructed for:



\\\[

k\_1,

\\]



\\\[

k\_2,

\\]



and:



\\\[

k\_3.

\\]



A separate `StandardScaler` is fitted to each action-specific matrix.



\---



\# Action-Coordinate Variance Under the Current Metric



For every audited seed and every action, the raw variance of the three appended action coordinates is:



\\\[

\\boxed{

\[0,0,0].

}

\\]



After standardization, their variance remains:



\\\[

\\boxed{

\[0,0,0].

}

\\]



This occurs for all three actions.



For example, within the \\(k\_1\\) training matrix every row contains the same action coordinates.



Likewise, every row in the \\(k\_2\\) matrix contains the same \\(k\_2\\) coordinates, and every row in the \\(k\_3\\) matrix contains the same \\(k\_3\\) coordinates.



Therefore these coordinates contain no within-action variation.



\---



\# Consequence of Separate Action Scaling



Because the action coordinates are constant within each action-specific training matrix, standardization cannot make them informative for nearest-neighbor geometry.



For any action \\(a\\):



\\\[

\\operatorname{Var}(a)=0.

\\]



Likewise:



\\\[

\\operatorname{Var}(a-1)=0

\\]



and:



\\\[

\\operatorname{Var}(3-a)=0.

\\]



The effective distance representation therefore reduces to the non-action-dependent context/model coordinates.



Conceptually:



\\\[

z(x,a)

\\longrightarrow

\\phi(x)

\\]



for the purpose of within-action Euclidean distance.



\---



\# Current-Metric Action Separation



Across all:



\\\[

237

\\]



audited contexts, the number exhibiting any action-distance separation above numerical tolerance is:



\\\[

\\boxed{

0\.

}

\\]



Therefore:



\\\[

\\boxed{

0/237

=

0.000\\%.

}

\\]



The mean maximum pairwise action-distance difference is:



\\\[

\\boxed{

0.000000000000.

}

\\]



The maximum observed pairwise action-distance difference is also:



\\\[

\\boxed{

0.000000000000.

}

\\]



Thus:



\\\[

\\boxed{

d(x,k\_1)

=

d(x,k\_2)

=

d(x,k\_3)

}

\\]



for every audited context within numerical tolerance.



\---



\# Context-Level Examples



The equality is visible directly in individual contexts.



For the first audited context:



\\\[

d(x,k\_1)

=

2.286780,

\\]



\\\[

d(x,k\_2)

=

2.286780,

\\]



and:



\\\[

d(x,k\_3)

=

2.286780.

\\]



For another context:



\\\[

d(x,k\_1)

=

3.337154,

\\]



\\\[

d(x,k\_2)

=

3.337154,

\\]



and:



\\\[

d(x,k\_3)

=

3.337154.

\\]



A more distant context gives:



\\\[

d(x,k\_1)

=

5.230597,

\\]



\\\[

d(x,k\_2)

=

5.230597,

\\]



and:



\\\[

d(x,k\_3)

=

5.230597.

\\]



The metric clearly distinguishes contexts from one another.



It does not distinguish actions within the same context.



\---



\# Shared-Scaler Audit



A second representation was constructed to test whether the action invariance resulted only from fitting separate scalers.



Instead of fitting one scaler per action, all action-context pairs were combined into a single matrix.



One shared `StandardScaler` was then fitted across:



\\\[

k\_1,

\\quad

k\_2,

\\quad

k\_3.

\\]



Under this representation, the action coordinates do exhibit global variance.



Before scaling:



\\\[

\\boxed{

\[0.6666667,\\ 0.6666667,\\ 0.6666667].

}

\\]



After scaling:



\\\[

\\boxed{

\[1,\\ 1,\\ 1]

}

\\]



within floating-point precision.



Therefore shared scaling successfully preserves variation in the action coordinates at the global representation level.



\---



\# Shared Scaling Does Not Restore Action Separation



Despite restoring global action-coordinate variance, the shared-scaler representation still produces:



\\\[

\\boxed{

0/237

}

\\]



contexts with nonzero action-distance separation.



The mean maximum pairwise difference remains:



\\\[

\\boxed{

0\.

}

\\]



The maximum pairwise difference remains:



\\\[

\\boxed{

0\.

}

\\]



Therefore:



\\\[

\\boxed{

d\_{\\text{shared}}(x,k\_1)

=

d\_{\\text{shared}}(x,k\_2)

=

d\_{\\text{shared}}(x,k\_3).

}

\\]



This demonstrates that separate scaling is not the only reason for the invariance.



\---



\# Why the Shared Scaler Still Fails



The reason follows directly from the nearest-neighbor construction.



For an action \\(a\\), the query point:



\\\[

z(x,a)

\\]



is compared only against training samples associated with the same action:



\\\[

z(x\_i,a).

\\]



Therefore the action coordinates are identical between the query and every candidate neighbor.



For the direct action coordinate:



\\\[

a-a=0.

\\]



Likewise:



\\\[

(a-1)-(a-1)=0

\\]



and:



\\\[

(3-a)-(3-a)=0.

\\]



Consequently, the action-coordinate contribution to Euclidean distance is:



\\\[

\\sqrt{

0^2+0^2+0^2

}

=

0\.

\\]



This remains true even when those coordinates were standardized using a shared scaler.



\---



\# General Geometric Result



Experiment 091 therefore establishes a more general result.



Appending a constant action identifier to a feature representation does not by itself create action-conditioned nearest-neighbor support when each action query is compared only against training examples carrying the same action identifier.



Formally, if:



\\\[

z(x,a)

=

\[

\\phi(x),

g(a)

]

\\]



and support for \\(a\\) is computed only against:



\\\[

\[

\\phi(x\_i),

g(a)

],

\\]



then:



\\\[

g(a)-g(a)=0.

\\]



The distance reduces to:



\\\[

d(

z(x,a),

z(x\_i,a)

)

=

d(

\\phi(x),

\\phi(x\_i)

).

\\]



Therefore:



\\\[

\\boxed{

\\text{constant action labels cannot create action-conditioned}

\\atop

\\text{within-action support geometry}.

}

\\]



\---



\# Audit Verdict



The current support metric is not action-conditional.



It measures:



\\\[

\\boxed{

d\_{\\text{context}}(x)

}

\\]



rather than:



\\\[

d\_{\\text{action}}(x,a).

\\]



The appropriate scientific interpretation is therefore:



\\\[

\\boxed{

\\text{local context familiarity}

}

\\]



or equivalently:



\\\[

\\boxed{

\\text{context-level epistemic support}.

}

\\]



\---



\# What the Existing Metric Actually Measures



The metric remains informative.



Contexts with smaller support distance lie closer to the training distribution in the learned context/model feature space.



Contexts with larger support distance are more epistemically remote from the training population.



Therefore the metric answers approximately:



\\\[

\\boxed{

\\text{“How well represented is this operating context}

\\atop

\\text{by the available training support?”}

}

\\]



It does not answer:



\\\[

\\text{“How well represented is action }a

\\text{ in this operating context?”}

\\]



\---



\# Implications for Experiments 080–090



This audit does not invalidate the numerical results of the previous support-aware experiments.



The measured support distances were real.



The controller decisions based on those distances were real.



The prospective outcomes remain unchanged.



The required correction is interpretive.



Previous terminology describing the metric as:



\\\[

\\text{action-specific support}

\\]



or:



\\\[

\\text{action-conditioned epistemic distance}

\\]



should instead be understood as:



\\\[

\\boxed{

\\text{context-level epistemic support}.

}

\\]



\---



\# Revised Interpretation of Harmful Expansion



Previous experiments showed that harmful expansion was associated with greater support distance.



The correct interpretation is therefore not:



\\\[

\\text{harmful expansions occur for poorly supported actions}.

\\]



Instead:



\\\[

\\boxed{

\\text{harmful expansions are more likely in epistemically}

\\atop

\\text{weakly supported operating contexts}.

}

\\]



This remains an important result.



It means local training-support density contains information about the reliability of safe-action expansion.



\---



\# Revised Interpretation of the Support Gate



The support-aware expansion rule should now be interpreted as:



\\\[

\\boxed{

\\text{expand the predicted safe set only when the current}

\\atop

\\text{operating context is sufficiently familiar}.

}

\\]



Thus the validated architecture is more accurately described as a:



\\\[

\\boxed{

\\text{context-support-aware safe-action expansion policy}.

}

\\]



This terminology should be used going forward unless a genuinely action-conditioned support representation is introduced.



\---



\# Why the Prior Results Still Matter



The audit changes the semantics of the metric, not the empirical observation that it helped discriminate risky expansion conditions.



In particular, prior experiments established that context-support gating could:



\- recover responsive actions,

\- reduce harmful expansions relative to less selective expansion,

\- identify epistemically remote failure cases,

\- and interact meaningfully with transient-state risk.



Those findings remain part of the experimental record.



The appropriate scientific correction is to narrow the claim to what the representation actually measures.



\---



\# Requirements for Genuine Action-Conditioned Support



A genuinely action-conditioned support representation must contain dimensions whose values vary meaningfully with both:



\\\[

x

\\]



and:



\\\[

a.

\\]



A constant action identifier is insufficient.



A future representation could take the form:



\\\[

z(x,a)

=

\[

\\phi(x),

\\psi(x,a)

],

\\]



where:



\\\[

\\psi(x,a)

\\]



contains action-dependent information.



Possible action-dependent quantities include:



\- predicted loss for action \\(a\\),

\- predicted downside for action \\(a\\),

\- predicted safety probability for action \\(a\\),

\- action-specific uncertainty,

\- action-specific regret margin,

\- action-specific outcome features,

\- or learned embeddings derived from realized action consequences.



In such a representation:



\\\[

\\psi(x,k\_1),

\\quad

\\psi(x,k\_2),

\\quad

\\psi(x,k\_3)

\\]



would differ for the same context.



Only then can the geometry genuinely become action-conditioned.



\---



\# Alternative Outcome-Support Construction



A second approach is to define support using historical action-outcome examples.



Instead of asking only whether context \\(x\\) resembles previous contexts, one could estimate support from observations of the form:



\\\[

(x\_i,a\_i,y\_i),

\\]



where:



\\\[

a\_i

\\]



is the evaluated action and:



\\\[

y\_i

\\]



contains its realized consequence.



Then support for:



\\\[

(x,a)

\\]



would depend on the density and relevance of historical observations specifically associated with action \\(a\\).



This would create genuine action-conditional empirical support rather than merely attaching an action label to context features.



\---



\# Scientific Value of the Audit



Experiment 091 demonstrates the importance of testing whether implementation geometry matches theoretical terminology.



Without this audit, subsequent experiments could have treated context familiarity as evidence for action-specific epistemic support.



The distinction matters because these are different scientific claims.



The audit therefore strengthens the framework by enforcing:



\\\[

\\boxed{

\\text{representation}

\\leftrightarrow

\\text{mathematical interpretation}

\\leftrightarrow

\\text{experimental claim}

}

\\]



consistency.



\---



\# Principal Finding



The primary result is:



\\\[

\\boxed{

d(x,k\_1)

=

d(x,k\_2)

=

d(x,k\_3)

}

\\]



for:



\\\[

\\boxed{

237/237

}

\\]



audited contexts.



Thus the existing support metric is conclusively action-invariant within numerical tolerance.



\---



\# Secondary Finding



Using a shared scaler restores global variance in the appended action coordinates but does not restore action-conditioned nearest-neighbor distance.



This proves that the deeper issue is not merely standardization.



It is the geometry of comparing each action query only against examples containing the identical constant action coordinates.



\---



\# Final Conclusion



Experiment 091 establishes that the support mechanism used in the preceding experiments should be interpreted as:



\\\[

\\boxed{

\\textbf{context-level epistemic support}

}

\\]



rather than:



\\\[

\\text{action-specific epistemic support}.

\\]



The existing experimental findings remain valid under this corrected interpretation.



The result also provides a clear representation-design requirement:



\\\[

\\boxed{

\\text{genuine action-conditioned support requires features}

\\atop

\\text{whose values vary jointly with context and action}.

}

\\]



\---



\# Next Research Direction



Experiment 092 should remain a representation experiment rather than a controller experiment.



No new prospective seed block should be consumed.



The next objective is to construct and compare candidate representations for genuine action-conditioned support.



The experiment should test whether an action-conditioned representation can produce:



\\\[

d(x,k\_1),

\\quad

d(x,k\_2),

\\quad

d(x,k\_3)

\\]



that differ meaningfully for the same context while retaining interpretable relationships with realized action consequences.



Candidate representations should be evaluated for:



1\. action-distance separation,

2\. within-seed stability,

3\. cross-seed stability,

4\. relationship to realized harmful expansion,

5\. relationship to realized incremental regret,

6\. redundancy with existing context support,

7\. and whether the representation adds information beyond predicted loss alone.



No new controller should use the new representation until its geometry and retrospective predictive value have been independently established.

