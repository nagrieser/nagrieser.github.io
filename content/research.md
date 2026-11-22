+++
title = "Research"
template = "research.html"

[extra]
lede = "The High-Luminosity LHC (HL-LHC) will deliver a huge data set over the next two decades. I believe what we learn from it will depend as much on how well we understand the proton, and on how well we decide which collisions to keep, as on the number of collisions it produces. These are the questions I think are most important for the field, and where my research fits in."
questions = [
    { id = "understand", text = "What Do We Need to Understand?" },
    { id = "maximize", text = "Maximizing the HL-LHC" },
    { id = "next", text = "Where Do We Go Next?" },
]
+++

## What Do We Need to Understand from the HL-LHC? {#understand}

Searches for new physics at the LHC look for a disagreement between a measured cross-section and the Standard Model prediction. Every one of those predictions relies on the parton distribution functions (PDFs), which describe how the momentum of the proton is shared between its quarks and gluons. PDF uncertainties are already a limiting factor for the projected precision of Higgs couplings at the HL-LHC, and for the reach of searches for heavy new particles. This is especially true for collisions where both partons carry a large fraction of the proton momentum (high *x*), which are the collisions most sensitive to new heavy particles. Understanding the proton is therefore critical to getting the most out of the HL-LHC physics program.

### Is There Charm in the Proton?

In the textbook picture, the proton is made of two up quarks and a down quark, bound together by gluons, with short-lived quark-antiquark pairs that appear when the proton is probed. In 1980, Brodsky and colleagues proposed that the proton could also contain charm quarks as a permanent part of its structure, known as intrinsic charm. Over 40 years later, this is still an open question. The NNPDF collaboration has reported [evidence for intrinsic charm in Nature](https://doi.org/10.1038/s41586-022-04998-2), as well as evidence for charm and anti-charm quarks carrying different momentum distributions. Other PDF fitting groups find the question unresolved, and so far no single measurement has isolated either effect.

I believe a direct measurement is the best way to settle this, and the forward acceptance of LHCb is uniquely suited for it. A Z boson produced at large rapidity comes from a collision where one parton carries a large fraction of the proton momentum and the other a very small one, and LHCb has already seen more charm produced alongside forward Z bosons than expected without intrinsic charm. The next step is to measure the charge of the charm jet, which would tell us whether charm and anti-charm are distributed differently in the proton. With the transformer-based jet taggers now being developed, along with the particle identification of LHCb, I think this measurement is within reach with the Run 3 data set. A positive result would change how we describe the proton. A null result would also be significant, since the W boson mass, the weak mixing angle, the top quark mass, and Higgs couplings at the HL-LHC all depend on how charm in the proton is modelled.

### Constraining the Gluon with Forward Jets

Searches for new particles at the TeV scale are limited by how well we know the gluon at high *x*, where global fits rely on a small number of central jet and top quark data sets. Forward jets at LHCb pair a high-*x* parton with a very low-*x* parton, so they probe the gluon at both ends, with systematic uncertainties that are complementary to the central detectors. In the most forward regions, the predictions of the major PDF sets differ by up to 10-15%, which makes these measurements very sensitive to the differences between them.

However, no forward jet measurement from LHCb is currently included in the global PDF fits, since they have been published without the bin-to-bin correlations the fitting groups need. I think it is important that our measurements are designed with the global fits in mind from the start, with flavour-specific jet calibrations and fully correlated uncertainties made publicly available.

This is a common thread through my own analysis work. The [W boson helicity measurement](/publications/2026-whelicity/) I proposed and led, along with the forward [W charge asymmetry](/publications/2026-wassym/) and [W cross-section](/publications/2026-wxsec/) measurements, all study how quarks share the proton momentum in a region beyond the reach of the central detectors.

## Maximizing the Potential of the HL-LHC {#maximize}

Equally important to understanding the proton is deciding which collisions we keep. Modern detectors read out far more collisions than can reasonably be stored, from both a cost and an environmental impact perspective. LHCb is a good example of this. Since Run 3, LHCb selects events fully in software, processing all 30 million bunch crossings per second without a hardware trigger, with around 4 TB/s of data in Run 3 and 10 TB/s expected in Run 4. The storage is shared between flavour physics, electroweak measurements, searches for light exotic particles, and a nuclear physics program. Today, this storage is divided by hand across more than 4,000 offline selections, with thresholds negotiated between hundreds of analysts. This leads to overlapping selections and overly cautious requirements that use storage on low-value events, while changing running conditions can reduce our sensitivity to rare signals.

Optimizing this is a difficult problem. Thresholds are discrete, so standard gradient-based methods do not work well. Selections are coupled through the events they share, so changing one affects the others. Evaluating a single configuration on real data takes minutes, so a brute-force search is not possible.

I believe this is an area where AI can have a huge impact on how experiments are run. The allocation can be treated as a constrained decision problem suited to reinforcement learning, with AI agents handling the workflow around it. This includes reading the code of each selection to understand the signal it targets, finding or requesting the needed simulation, testing configurations on real data, and preparing the changes for physicists to approve. Instead of editing and negotiating thresholds by hand, analysts review and sign off on the proposed changes. To be trusted, this needs to be fully transparent, with a minimum signal efficiency guaranteed for every selection and a full evaluation attached to every change. The tools to evaluate a configuration on real data in minutes [already exist](https://doi.org/10.1051/epjconf/202533701261), and the optimization is the missing piece. I describe how I think AI can change the way experiments are run in more detail on the [AI for Physics](/research/ai/) page.

My experience here comes from working directly on these systems. I designed, commissioned, and optimized the LHCb Run 3 jet trigger selections, have been in charge of all ion and special-configuration [Sprucing](/publications/2025-sprucing/) processings in Run 3, led the [Stripping Project](/publications/2025-stripping/) to reprocess the full Run 2 data set, and now serve as Project Leader of LHCb Data Processing and Analysis. I also co-chair the LHCb forum on the use of AI in writing and reviewing analysis code, since how these tools are brought into a large collaboration is just as important as the tools themselves.

These two areas are closely connected. The forward jet triggers at LHCb are heavily prescaled in Run 3, which limits the samples most needed for proton structure measurements, such as heavy-flavour tagged jets and high-mass forward di-jets. Removing those prescales requires taking bandwidth from elsewhere in the LHCb physics program, which is exactly the type of trade-off a physics-driven optimization should be able to make and justify.

<a class="research-callout" href="/research/ai/"><strong>AI for Physics →</strong> Using AI to decide how an experiment is run, and how a large collaboration can trust it</a>

## Where Do We Go Next? {#next}

The coming years are an important window. The data LHCb collected with the upgraded detector in 2024-2026 are on disk, and the current long shutdown is the time to turn them into the calibrations and measurements that Run 4 will build on, starting in 2030. Beyond that, LHCb Upgrade II will run at even higher rates, and its trigger and offline selection strategy is being designed now. At a future electron-positron collider such as FCC-ee, the same tools will be needed again, both for charm jet charge tagging and for choosing what to keep from roughly 5×10<sup>12</sup> Z boson decays.

Deciding what data to keep is not unique to particle physics. Any experiment that records more data than it can store faces the same problem, including large astronomical surveys. I would like the methods we develop for LHCb to be general and open, so they are useful well beyond our experiment.

Finally, none of this work is possible without students. Many of the people who will make the defining measurements of the HL-LHC era are students today, and several of the topics above started as [student projects](/students/). If any of these questions interest you, please [get in touch](/contact/)!
