# The Standard Model and the Higgs Boson

The [Standard Model (SM)](https://home.cern/science/physics/standard-model) of the particle physics is a remarkably successful and tested theoretical framework that describes the fundamental constituents of matter adn their interactions. It classifies all known elementary particles into two board categories: spin-1/2 fermions and (quarks and leptons), which forms the building blocks of matter, and spin-1 gauge bosons (photons, gluons, and the $W^\pm$ and $Z$ bosons), which mediate the electromagnetic, strong, and weak fundamental forces respectively.

![Standard Model](https://cds.cern.ch/images/OPEN-PHO-CHART-2015-001-1/file?size=large){width="450"}

## **Where does the Higgs Boson stands here?**

One of the crucial requirement of the SM is a mechanism to generate the masses of these fundamental particles without violeting the underlying mathematical symmetries of the theory. This is achieved through a scalar field. The fundamental fermions and the massive weak forces carries ($W^\pm$ and $Z$ bosons) acquire their intrinsic masses by continously interacting with this field. A direct observable consequence of this field is the existence of a single, spin-0 scalar particle: [**Higgs Boson ($H$)**](https://cms.cern/physics/higgs-boson).

## **Discovery and the Precision Era**

In 2012, the ATLAS and the CMS collaborations at the LHC [announced](https://home.cern/news/press-release/cern/cern-experiments-observe-particle-consistent-long-sought-higgs-boson) the historic discovery of a new scalar resonance with a mass of $m_H \sim \text{125 GeV}$.

Subsequent experimental measurements have confirmed that the particle's properties strongly align with the predictions for the SM Higgs Boson. With, its mass now fixed, all other properties of the $H$ boson are constrained by SM.

## **Higgs Boson Production at the LHC**

At the LHC, protons are collided at ultra-high energies, specifically at a center-of-mass energy of $\sqrt{s} = \text{13 TeV}$ for the 2016 data-taking period utilized in this analysis. At such high energies, the collision occurs at the quarks level and due to massive amount of energy produced during the collision many heavy particles ($W^\pm,\ Z,\ H$) are produced.

There are four primary production mechanisms for the SM Higgs boson at the LHC:

1. **Gluon-Gluon Fusion (ggH or ggF):** Two gluons from the interacting protons fuse to produce a Higgs boson. Because gluons are massless, they cannot couple to Higgs directly. This process occurs via a virtual loop of heavy quarks. The top quark, having the largest Yukawa coupling, dominates this loop exchange.

   ![ggH Feynman Diagram](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/ggh_FD.png){width="250"}

2. **Vector Boson Fusion (VBF):** Two quarks from the incoming protons emits a gauge bososn ($W$ or $Z$), which then scatter and fuse to form a Higgs boson. This mode is characterized by two highly energetic forward jets in the detector.

   ![VBF Feynman Diagram](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/VBF_FD.png){width="250"}

3. **Associated Production (VH):** A quark and an antiquark annhilate to form an off-shell $W$ or $Z$ boson, which then radiates an $H$.

   ![VH Feynman Diagram](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/VH_FD.png){width="250"}

4. **Top Quark Associated Production (ttH):** Two gluons or quarks fuse to produce a top-antitop quark pair along with an $H$.

   ![ttH Feynman Diagram](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/ttH_FD.png){width="250"}

## **Dominance of Gluon-Gluon Fusion**

This analysis specifically focuses on the ggH production mode. The choice to isolate this channel over others is driven by two primary kinematic and experimental factors:

1. **Cross-section Dominance:** At a center-of-mass energy of $\sqrt(s)\ =\ \txt{13 TeV}$, ggH is by far the most abundant production mechanism. According to the LHC Higgs Cross Section Working Group, the inclusive cross-section for ggH at 13 TeV is $\sigma_{ggH}\sim \txt{48.58 pb}$. This accounts for approximately 87 % of the total Higgs boson production at the LHC. This overwhelming abundance ensures the maximum possible signal yield, providing good statistical foundation of the analysis.
   ![Higgs Cross-section at TeV scale](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/Higgs_xsec.png){width="250"}

2. **Signal Cleanliness:** Compared to other production modes, the ggH process offers a comparatively clean experimental topology. For example, the VBF channel, despite having the second largest cross-section, is characterized by the presence of two highly energetic "forward" jets. Identifying these jets and removing them from the background requires complex jet selections, making the analysis highly sensitive to pileup in the detector region. Similarly, the VH and ttH introduces additional heavy bosons or top quarks, making the final state cluttered with extra leptons and $b$-quarks. Thus, focussing on ggH allows for a cleaner extraction of the Higgs signal.
