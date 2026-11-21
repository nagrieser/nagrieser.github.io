+++
title = "Research"
template = "research.html"

[extra]
lede = "The high-luminosity LHC is a multi-decade international investment, and what it discovers will not be set by the number of collisions it produces. It will be set by how well we understand the proton, and by what we choose to keep. These are the questions I think matter most, and the ones my work is aimed at."
questions = [
    { id = "understand", text = "What do we still need to understand?" },
    { id = "maximize", text = "How do we make the most of the data?" },
    { id = "next", text = "Where do we go next?" },
]
+++

## What do we still need to understand? {#understand}

New physics shows up as a disagreement between a measured cross-section and a prediction, and every prediction at a proton collider rests on the parton distribution functions (PDFs) that say what a proton is made of. Each gives the probability that a gluon or a given quark carries a fraction *x* of the proton's momentum. PDF uncertainty already limits the precision projected for Higgs couplings at the high-luminosity LHC and the reach of searches for heavy new particles. It is most limiting in the highest-energy collisions, where both partons carry large *x*, which are exactly the collisions sensitive to heavy new particles and to effects that grow with energy.

So, to me, the proton is not background to the physics program. It is one of the limits on it.

### Is there charm in the proton?

We teach that the proton is two up quarks and a down quark, held together by gluons, with quark–antiquark pairs that appear and vanish as it is probed. In 1980 Brodsky and colleagues proposed that the proton also carries charm quarks as a permanent part of its structure, each heavier than the proton itself. More than forty years later, the question is still open. The NNPDF collaboration has reported [evidence for this *intrinsic charm* in Nature](https://doi.org/10.1038/s41586-022-04998-2), and later for charm and anticharm carrying different momentum distributions. Other fitting groups reach more cautious conclusions, and no single measurement has isolated either effect.

When the fits disagree, I think only a measurement that isolates the effect can decide. LHCb is well placed to make it. A *Z* boson produced close to the beam direction comes from a lopsided collision, in which one parton carries a large share of the proton's momentum and the other a tiny one, and LHCb has already seen more charm produced with a forward *Z* than expected without intrinsic charm. The next step is to read the *charge* of the charm jet, which would show whether charm and anticharm sit in the proton differently. The transformer-based jet taggers we now have, combined with LHCb's particle identification, make that measurement realistic for the first time. Either answer would be worth having. A positive result changes the textbook picture of the proton. A null result removes an unresolved question about the proton that otherwise sits underneath the *W*-boson mass, the weak mixing angle, the top-quark mass and Higgs couplings at the high-luminosity LHC.

### The gluon at both ends of momentum fraction

Searches for new particles at a few TeV are limited by how well the gluon is known at large *x*, where global fits rely on a small number of central jet and top-quark datasets. Forward jets pair a parton at large *x* with one at very small *x*, so they reach the gluon at both ends, with systematic uncertainties unlike the central data's. In the most forward bins the major PDF sets disagree by 10–15%, which is precisely where a measurement can tell them apart.

Yet no forward LHCb jet measurement enters the global fits today, because forward jet results have been published without the bin-to-bin correlations a fit needs. I feel strongly that our measurements should be built to be *used*: calibrated flavour by flavour, released with their correlated uncertainties, and in a form the fitting groups can take directly, without collaboration membership.

This is the thread that runs through my own measurements. The [*W*-boson helicity measurement](/publications/2026-whelicity/) I proposed and led, and the forward [*W* charge asymmetry](/publications/2026-wassym/) and [cross-section](/publications/2026-wxsec/) papers, all probe how quarks share the proton's momentum in a region the central detectors cannot reach.

## How do we make the most of the data? {#maximize}

A signal that is not kept cannot be discovered, however well the proton is understood.

Detectors now read out far more collisions than can reasonably be stored, on grounds of both cost and environmental impact. LHCb is a sharp instance of the problem. It selects entirely in software, processing all 30 million bunch crossings per second with no hardware pre-filter: about 4 TB/s today, and 10 TB/s from Run 4. Storage is shared between quark-flavour physics, electroweak measurements, searches for light exotic particles and a nuclear-physics program, and today it is divided by hand, across more than 4,000 offline selections and tens of thousands of thresholds, by negotiation among hundreds of people. Overlapping selections and over-cautious settings spend storage on low-value events, and drifting conditions quietly erode sensitivity to rare or unexpected signals.

This is a hard problem, not just a tedious one. Thresholds act discretely, so their effects cannot be followed by gradients. Selections are coupled through the events they share, so tightening one changes the value of another. And an exact evaluation of a single configuration takes minutes on real data, which rules out brute-force search.

I think this is where AI will genuinely change how experiments run, and not only as a better classifier. I see it as a sequential decision problem under hard constraints, well suited to reinforcement learning, with AI agents running the workflow around it: reading each selection's code to identify the signal it selects, finding or requesting the simulation it needs, testing candidate configurations on real data, and writing the proposed changes for physicists to approve. The cycle in which hundreds of contributors edit, test and negotiate thresholds by hand becomes one that people *review* rather than carry out. For that to be trusted, it has to be auditable: every selection protected by a floor on its own signal efficiency, and every change justified with the evaluation attached. The tools to score any configuration on real data in minutes [now exist](https://doi.org/10.1051/epjconf/202533701261). What is missing is the optimiser.

I come to this problem from the inside. I designed, commissioned and optimised LHCb's Run 3 jet trigger menu, I have run every ion and special-configuration [Sprucing](/publications/2025-sprucing/) processing in Run 3, I led the [Stripping Project](/publications/2025-stripping/) that reprocessed the full Run 2 dataset, and I now lead LHCb's Data Processing and Analysis project. I also co-chair LHCb's forum on the use of AI in writing and reviewing analysis code, because how we bring these tools into a collaboration matters as much as the tools themselves.

The two halves of this page meet in practice. LHCb's forward single-jet and dijet triggers are heavily prescaled today, which starves exactly the samples a proton-structure program needs: heavy-flavour-tagged jets and the highest-mass, most forward dijets. Freeing that bandwidth means taking it from somewhere else in the program, and that is the kind of trade a principled, physics-driven allocation should be able to make and to justify.

## Where do we go next? {#next}

The timing is set by the accelerator. The data LHCb recorded in 2024–2026 with its upgraded detector are complete and on disk, and the current long shutdown is when they must become the calibrations the next run builds on. Run 4 begins in 2030. After that, LHCb Upgrade II will select at higher rates again, and its real-time and offline selection is being specified now. At a future electron–positron collider such as FCC-ee, the same two capabilities carry over directly: tagging the charge of charm jets, and choosing what to persist from roughly 5×10<sup>12</sup> *Z* decays.

The question of what to keep is not unique to particle physics. Every instrument that records more than it can store faces it, from the next generation of collider experiments to large astronomical surveys. I would like the methods we build for LHCb to be general, open, and auditable enough to be useful well beyond it.

And none of this happens without people. The measurements and tools that will define the high-luminosity era will largely be built by students who are starting out now, and several of the threads on this page began as [student projects](/students/). If any of these questions excite you, [get in touch](/contact/).
