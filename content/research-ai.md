+++
title = "AI for Physics"
path = "research/ai"
template = "research.html"

[extra]
lede = "There is a lot of excellent work applying machine learning to particle physics, from jet tagging to tracking to fast simulation. The direction I think is most important, and least explored, is using AI to make better decisions about how an experiment is run, and making those decisions transparent enough that a large collaboration can trust them."
questions = [
    { id = "value", text = "Letting Physics Decide What We Keep" },
    { id = "benchmark", text = "An Open Benchmark" },
    { id = "legacy", text = "Keeping Analyses Alive" },
    { id = "trust", text = "Building Trust" },
]
+++

<p class="research-back"><a href="/research/">← Back to Research</a></p>

## Letting Physics Decide What We Keep {#value}

At LHCb, the bandwidth and storage given to each of the more than 4,000 offline selections is decided by negotiation between the analysis groups. This works, but it means the allocation reflects which groups make the strongest case, rather than a direct measure of the physics each selection delivers.

I believe the value of a selection should be measured by how much it improves our knowledge of the quantities we care about, such as the proton PDFs, the weak mixing angle or the W boson mass. For many measurements this can be calculated directly from their own sensitivity models, or from the impact of the data on the global fits. With that information, the question of what to keep becomes an optimization problem with a physics-driven objective, which reinforcement learning is well suited to solve, while every selection is protected by a guaranteed minimum signal efficiency.

This also connects the two sides of my research. For example, the forward jet triggers at LHCb are heavily prescaled in Run 3, even though forward jets are some of the most useful data for constraining the gluon at high *x*. A physics-driven allocation would be able to show how much those jets are worth to the PDF fits, and what it would cost elsewhere in the program to keep them.

## An Open Benchmark for Scientific Data Selection {#benchmark}

The machine learning community has benchmarks for image recognition, language and games, but very few for constrained resource allocation on real scientific data. The LHCb selection problem is a good candidate. It has thousands of coupled, discrete thresholds, hard rate and storage limits, and competing scientific goals, and every configuration can be evaluated exactly on real collision data.

I would like to see a version of this problem released publicly, with the selections anonymized and an evaluator that returns rates, overlaps and signal efficiencies for any configuration. This would allow computer science groups to work directly on a real problem from a running experiment, and would give our field access to methods we would not develop on our own. The same problem appears at every instrument that records more data than it can store, from LHCb Upgrade II and FCC-ee to large astronomical surveys.

## Keeping Analyses Alive {#legacy}

A large part of the cost of a long-running experiment is keeping old data and analyses usable as the software underneath them changes. Through the [LHCb Stripping Project](/publications/2025-stripping/), I led the reprocessing of the full Run 2 data set with a modernized software stack, and saw first-hand how much manual effort it takes to port, re-run and validate thousands of selections.

I think AI agents can take over a significant part of this work. An agent can read a selection or an analysis job, port it to a new framework or data format, run it, and compare the output against the original, flagging any differences for a person to review. If the cost of maintaining an analysis drops close to zero, the data collected in Runs 1 to 3 can stay ready for new physics well into the Upgrade II era, which is important for both the science and the sustainability of the experiment.

## Building Trust in AI Within a Large Collaboration {#trust}

None of this is useful unless physicists trust the results. I co-chair the LHCb forum on the use of AI in writing and reviewing analysis code, and in my experience the open questions are less about what the tools can do and more about how we check them.

One idea I find very promising is using AI as an independent second analyst. Collaborations already require important results to be cross-checked by an independent analyst, which takes a lot of person-power. An agent that rebuilds the key steps of an analysis from its documentation, and reports where it disagrees with the original, could make these cross-checks faster and more complete, while the final judgement stays with the reviewers.

The same principle applies to the machine learning models used in measurements. A jet tagger should be treated like any other part of the detector, with its output calibrated in data and its uncertainties propagated into the result. For example, a charge-sensitive charm tagger can provide a calibrated probability for every jet, which can enter the likelihood directly instead of being used only as a selection cut.

In all of these cases the goal is the same. AI does the large-scale, repetitive work, physicists decide what matters, and every decision can be checked and explained. If you are interested in working on any of these questions, as a student or a collaborator, please [get in touch](/contact/)!
