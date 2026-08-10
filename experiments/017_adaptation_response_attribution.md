\# Experiment 017 — Adaptation-Response Attribution



\## Objective



Determine whether different sources of digital-twin mismatch can be distinguished not only from the statistical behavior of estimator residuals, but from the internal adaptation required for the twin to restore consistency.



Experiment 016 demonstrated that process disturbance and structural change can both return to approximately consistent post-event normalized innovation statistics. Consequently, residual recovery alone does not uniquely identify the source of mismatch.



Experiment 017 therefore introduces a second attribution channel: the adaptation response of the digital twin itself.



The central hypothesis is:



\\\[

\\boxed{

\\text{Different physical causes of prediction disagreement require different internal adaptation trajectories.}

}

\\]



In particular, a transient process disturbance should produce temporary adaptation followed by recovery toward the original model, whereas a genuine structural change should require persistent modification of the estimated dynamical parameter.



\---



\## Experimental Regimes



Two regimes are compared.



\### 1. Process Disturbance



The underlying system parameter remains



\\\[

a = 0.92,

\\]



but a transient disturbance is introduced at the event time.



The physical system itself has not permanently changed.



Therefore, after recovery, the correct internal parameter remains approximately



\\\[

\\hat{a} \\approx 0.92.

\\]



\### 2. Structural Change



At the event time, the true dynamical parameter changes from



\\\[

a\_{\\text{pre}} = 0.92

\\]



to



\\\[

a\_{\\text{post}} = 0.80.

\\]



Recovery therefore requires the adaptive digital twin to revise its internal dynamical representation.



The expected post-adaptation parameter is



\\\[

\\hat{a} \\approx 0.80.

\\]



\---



\## Attribution Channels



The experiment considers two complementary sources of evidence.



\### Residual Evidence



The observation channel contains quantities derived from prediction disagreement:



\\\[

\\mathcal{O}\_k

=

\\{

\\nu\_k,

\\operatorname{NIS}\_k

\\}.

\\]



These variables describe how strongly observations disagree with predictions.



\### Adaptation Evidence



The adaptation channel contains quantities describing how the twin responds internally:



\\\[

\\mathcal{A}\_k

=

\\{

\\hat{a}\_k,

\\Delta \\hat{a}\_k,

\\lambda\_k,

Q\_k^{\\mathrm{eff}}

\\}.

\\]



These variables measure changes in the learned parameter and uncertainty-management mechanism.



The attribution problem can therefore be represented as



\\\[

z

=

\\Psi(

\\mathcal{O}\_{0:T},

\\mathcal{A}\_{0:T}

),

\\]



where \\(z\\) denotes the inferred source of mismatch.



\---



\## Temporal Parameter-Shift Features



Let



\\\[

\\bar{a}\_{\\mathrm{pre}},

\\qquad

\\bar{a}\_{\\mathrm{event}},

\\qquad

\\bar{a}\_{\\mathrm{post}}

\\]



denote the mean parameter estimates over the pre-event, event, and post-event windows.



Define



\\\[

\\Delta a\_{\\mathrm{event}}

=

\\bar{a}\_{\\mathrm{event}}

\-

\\bar{a}\_{\\mathrm{pre}},

\\]



and



\\\[

\\Delta a\_{\\mathrm{post}}

=

\\bar{a}\_{\\mathrm{post}}

\-

\\bar{a}\_{\\mathrm{pre}}.

\\]



The second quantity is particularly important because it distinguishes temporary adaptation from persistent model revision.



\---



\## Results



The experiment was evaluated across 100 random seeds for each regime, producing 200 trajectories.



\### Process Disturbance



The process-disturbance regime produced



\\\[

\\Delta a\_{\\mathrm{event}}

=

0.019047

\\pm

0.004450,

\\]



and



\\\[

\\Delta a\_{\\mathrm{post}}

=

0.000389

\\pm

0.002994.

\\]



The mean final parameter estimate was



\\\[

\\hat{a}\_{\\mathrm{final}}

=

0.920278

\\pm

0.004404.

\\]



The event-window normalized innovation statistic increased to



\\\[

\\overline{\\operatorname{NIS}}\_{\\mathrm{event}}

=

3.509529

\\pm

1.079513,

\\]



but subsequently returned to



\\\[

\\overline{\\operatorname{NIS}}\_{\\mathrm{post}}

=

0.972304

\\pm

0.269067.

\\]



The effective process uncertainty similarly decreased from



\\\[

\\overline{Q}^{\\mathrm{eff}}\_{\\mathrm{event}}

=

0.549123

\\]



to



\\\[

\\overline{Q}^{\\mathrm{eff}}\_{\\mathrm{post}}

=

0.080770.

\\]



The twin therefore responded strongly to the disturbance but ultimately returned to approximately the original dynamical model.



\---



\### Structural Change



The structural-change regime produced



\\\[

\\Delta a\_{\\mathrm{event}}

=

\-0.054530

\\pm

0.004206,

\\]



followed by the much larger persistent shift



\\\[

\\Delta a\_{\\mathrm{post}}

=

\-0.114467

\\pm

0.005471.

\\]



The mean final parameter estimate became



\\\[

\\hat{a}\_{\\mathrm{final}}

=

0.800990

\\pm

0.011398,

\\]



which is close to the new true parameter



\\\[

a\_{\\mathrm{post}}=0.80.

\\]



The event-window normalized innovation statistic was



\\\[

\\overline{\\operatorname{NIS}}\_{\\mathrm{event}}

=

2.698888

\\pm

0.400001,

\\]



while the post-event statistic returned to



\\\[

\\overline{\\operatorname{NIS}}\_{\\mathrm{post}}

=

0.981518

\\pm

0.260152.

\\]



Thus, statistical consistency was restored only after the twin substantially revised its internal parameter estimate.



\---



\## Direct Attribution Comparison



The strongest separation appears in the persistent parameter shift:



| Feature | Process Disturbance | Structural Change |

|---|---:|---:|

| Event parameter shift | +0.019047 | -0.054530 |

| Post parameter shift | +0.000389 | -0.114467 |

| Event mean absolute parameter update | 0.005728 | 0.009478 |

| Post mean absolute parameter update | 0.002907 | 0.006928 |

| Event cumulative absolute parameter update | 0.057278 | 0.094779 |

| Post cumulative absolute parameter update | 0.058137 | 0.138569 |

| Event mean NIS | 3.509529 | 2.698888 |

| Post mean NIS | 0.972304 | 0.981518 |

| Final parameter estimate | 0.920278 | 0.800990 |



The post-event NIS values are nearly identical:



\\\[

0.972304

\\quad\\text{and}\\quad

0.981518.

\\]



Therefore, once adaptation has succeeded, the residual statistics alone provide little evidence about the original cause of disagreement.



The adaptation history, however, remains strongly discriminative.



\---



\## Interpretation



The process disturbance follows the pattern



\\\[

\\text{large disagreement}

\\rightarrow

\\text{temporary adaptation}

\\rightarrow

\\text{return toward original model}.

\\]



The structural change follows



\\\[

\\text{large disagreement}

\\rightarrow

\\text{persistent adaptation}

\\rightarrow

\\text{new internal model}.

\\]



This distinction suggests that attribution should not depend exclusively on the magnitude or statistical consistency of residuals.



Instead, the twin should reason jointly over



\\\[

\\boxed{

\\text{what the system did}

\+

\\text{what the twin had to change in response}.

}

\\]



\---



\## Attribution Principle



The experiment motivates the following principle:



\\\[

\\boxed{

\\text{Residual recovery does not imply causal equivalence.}

}

\\]



Two mismatch mechanisms may produce similar post-adaptation residual statistics while requiring fundamentally different internal model responses.



A more complete mismatch representation is therefore



\\\[

\\mathcal{F}

=

\[

\\mathcal{F}\_{\\mathrm{residual}},

\\mathcal{F}\_{\\mathrm{temporal}},

\\mathcal{F}\_{\\mathrm{adaptation}}

].

\\]



The inferred mismatch class becomes



\\\[

\\hat{z}

=

\\Psi(\\mathcal{F}).

\\]



This creates the mathematical basis for an explicit residual-attribution layer.



\---



\## Conclusion



Experiment 017 demonstrates that adaptation-response features provide strong information about the cause of digital-twin mismatch.



A transient process disturbance generates a strong but temporary response, after which the learned dynamical parameter returns approximately to its original value.



A structural change instead requires persistent parameter adaptation, with the final learned parameter converging toward the new physical regime.



The results establish that residual evidence and adaptation evidence are complementary.



This motivates the next stage of development:



> \*\*Experiment 018 — Explicit Mismatch Classification\*\*



The next experiment will combine interpretable residual, temporal, and adaptation-response features into an explicit attribution mechanism that assigns observed disagreement to candidate physical causes.

