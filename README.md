# HSF-India Project: Higgs → WW NanoAOD Analysis

This repository is part of the **HSF-India project**, focusing on the analysis of Higgs boson decays to **W boson pairs (H $\to$ WW)** using CMS NanoAOD data formats. The current work emphasizes **Monte Carlo (MC) simulation studies**, starting with basic kinematic distributions of signal and background events.

---

## Background: The Higgs Boson and ggH Production

The **Higgs boson**, discovered in 2012 at the LHC, is a fundamental scalar particle associated with the Higgs field, which gives mass to elementary particles through the mechanism of **electroweak symmetry breaking**.  

One of the dominant production mechanisms of the Higgs at the LHC is **gluon-gluon fusion (ggH)**. In this channel:  

- Two gluons interact through a **loop of heavy quarks** (mostly the top quark).  
- This loop produces a Higgs boson, which then decays according to its branching ratios.  
- In this project, we are particularly interested in the decay channel **H $\to$ WW $\to$ leptons + neutrinos**, which is a key signature for Higgs studies due to its clean leptonic final states and sizeable branching fraction.  

---

## Repository Contents

- **Notebooks/**  
  - `basic_kinematics.ipynb`: A Jupyter notebook with initial kinematic plots for both signal (H $\to$ WW) and background processes. These include variables such as transverse momentum (pT), pseudorapidity ($\eta$), and invariant masses, serving as a foundation for deeper analysis.  

Future notebooks will expand this to include:  
- Event selection strategies.  
- Comparison between different MC samples.  
- Advanced discriminating variables for separating signal from background.  

---

## Getting Started

1. Clone the repository:  
   ```bash
   git clone https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis.git
   cd H-to-WW-NanoAOD-analysis
