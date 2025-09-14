# HSF-India Project: Higgs → WW NanoAOD Analysis*

>**Disclaimer:** This repository is a work in progress. The code, documentation, and data may change frequently as updates and improvements are made.


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
  - [Basic_kinematics.ipynb](notebooks/Kinematic_plots.ipynb): A Jupyter notebook with initial kinematic plots for both signal (H $\to$ WW) and background processes. These include variables such as transverse momentum (pT), pseudorapidity ($\eta$), and invariant masses, serving as a foundation for deeper analysis.  

  -  [Global_selections.ipynb](notebooks/Global_selection.ipynb): This jupyter notebook contains event selection criteria (global criteria + criteria for 0-jet category)

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
  
2. Configure a virtual environment:

   It is recommended to create a dedicated Python virtual environment to ensure isolation of dependencies.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  (#Linux)
   .venv\Scripts\activate    (#windows)

3. Install the required dependencies:

   All necessary Python packages are listed in the [requirements.txt](requirements.txt) file. Install them using:

   ```bash 
   pip install -r requirements.txt

4. Verify the installation:

   A [diagnostic script](scripts/test_uproot.py) is provided to confirm that the environment has been configured correctly. Run:
   ```bash 
   python scripts/test_uproot.py 

5. Begin the Analysis: 

   Analysis notebooks are present in [notebooks](notebooks) directory. Users may start with [kinematic_plots.ipynb](notebooks/Kinematic_plots.ipynb) as an introductory example.
 
