# HSF-India Project: Higgs → WW NanoAOD Analysis

> **Disclaimer:** This repository is a work in progress. The code, documentation, and data may change frequently as updates and improvements are made.

---

## Overview

This repository contains a comprehensive analysis framework for studying **Higgs boson decays to W boson pairs $H\ \to WW\ \to e\nu\mu\nu$** using CMS NanoAOD data formats. Developed as part of the **HSF-India project**, this work implements a complete physics analysis pipeline from raw NanoAOD files to final physics results.

### What This Repository Does

The analysis pipeline performs:

1. **Data Processing**: Reads CMS NanoAOD ROOT files containing collision events
2. **Event Selection**: Applies physics-based selection criteria to identify Higgs $\to$ WW candidate events
3. **Background Estimation**: Analyzes and distinguishes signal from various Standard Model background processes
4. **Kinematic Analysis**: Studies particle properties (momentum, energy, angular distributions) to characterize the signal
5. **Statistical Analysis**: Applies weights, scale factors, and statistical methods to extract physics measurements

This framework is designed for both learning purposes and conducting real physics analysis, making it suitable for students, researchers, and physicists working with CMS data.

---

## Physics Background

### The Higgs Boson

The **Higgs boson** is a fundamental scalar particle discovered in 2012 at the Large Hadron Collider (LHC). It is associated with the Higgs field, which gives mass to elementary particles through the mechanism of **electroweak symmetry breaking**. Studying the Higgs boson's properties and decay modes is crucial for understanding the Standard Model of particle physics.

### Gluon-Gluon Fusion (ggH) Production

One of the dominant production mechanisms of the Higgs at the LHC is **gluon-gluon fusion (ggH)**:

- Two gluons from colliding protons interact through a **loop of heavy quarks** (predominantly top quarks)
- This loop produces a Higgs boson, which then decays according to its branching ratios
- The ggH process has the largest production cross-section at the LHC, making it the primary channel for Higgs studies

### H → WW Decay Channel

This analysis focuses on the decay channel **$H\ \to WW\ \to e\nu\mu\nu$**, where:

- The Higgs boson decays into two W bosons
- Each W boson subsequently decays into a charged lepton (electron or muon) and a neutrino
- The final state contains two opposite-sign leptons and missing transverse energy (from neutrinos)

This channel provides:
- **Clean experimental signature**: Two high-quality leptons are easily identifiable in the detector
- **Good signal-to-background ratio**: Specific kinematic selections can effectively suppress backgrounds
- **High sensitivity**: Despite the $W\to\ell\nu$ branching fraction being ~10% per lepton flavor, the clean signature compensates for the lower rate

---

## Repository Structure

```
H-to-WW-NanoAOD-analysis/
│
├── notebooks/              # Jupyter notebooks containing the analysis code
│   ├── H_WW_Dask.ipynb     # Main analysis notebook (START HERE)
│   ├── Kinematic_plots.ipynb
│   ├── Global_selection.ipynb
│   ├── xsec_weights.ipynb
│   └── Scale_factors.csv
│
├── Datasets/              # Directory for storing NanoAOD ROOT files
│
├── Plots/                 # Output directory for generated plots and figures
│
├── Auxillary_files/       # Supporting files 
│
├── scripts/               # Python utility scripts
│   └── test_uproot.py     # Environment verification script
│
├── Rollbacks/             # Previous versions and backup notebooks
│
├── Test/                  # Testing and development notebooks
│
├── requirements.txt       # Python package dependencies
├── environment.yml        # Conda environment specification
└── README.md              # This file
```

### Directory Descriptions

#### `notebooks/`
Contains all Jupyter notebooks for the analysis workflow. These notebooks implement the complete analysis chain from data reading to final plots.

**Main Notebook:**
- **`H_WW_Dask.ipynb`**: The primary analysis notebook that users should start with. This notebook uses Dask for efficient parallel processing of large NanoAOD datasets and contains the complete analysis pipeline including:
  - Data loading and preprocessing
  - Event selection criteria
  - Background process handling
  - Kinematic variable calculations
  - Plot generation and visualization
  - Statistical analysis with proper weighting

**Supporting Notebooks:**
- **`Kinematic_plots.ipynb`**: Generates basic kinematic distributions for signal and background processes (transverse momentum, pseudorapidity, invariant mass, etc.)
- **`Global_selection.ipynb`**: Implements event selection criteria and demonstrates the cutflow for the 0-jet category
- **`xsec_weights.ipynb`**: Calculates cross-section weights for normalizing Monte Carlo samples to their expected yields
- **`Scale_factors.csv`**: Contains scale factors for correcting simulation-to-data differences in lepton identification and trigger efficiencies

#### `Datasets/`
Storage location for CMS NanoAOD ROOT files. Users should place their signal and background Monte Carlo samples here. The analysis code reads files from this directory to perform the physics analysis.

**Expected content**: ROOT files containing NanoAOD trees with branches for physics objects (electrons, muons, jets, MET) and event-level information.

#### `Plots/`
Output directory where all generated plots and figures are automatically saved. This includes:
- Kinematic distributions (pT, η, φ for leptons and jets)
- Invariant mass distributions
- Missing transverse energy plots
- Cutflow diagrams
- Signal-background comparison plots

#### `Auxillary_files/`
Contains auxiliary data files required for the analysis:
- Cross-section values for different physics processes
- Branching ratio tables
- Luminosity information
- Generator-level weights
- Any additional reference data needed for calculations

#### `scripts/`
Python utility scripts for various tasks:
- **`test_uproot.py`**: A diagnostic script to verify that the Python environment is correctly configured and can read ROOT files using uproot

Additional scripts may include data validation tools, batch processing utilities, or helper functions used across multiple notebooks.

#### `Rollbacks/`
Archive of previous versions of notebooks and code. This directory serves as version control backup, allowing users to:
- Review earlier analysis iterations
- Restore previous working versions if needed
- Track the evolution of the analysis

#### `Test/`
Experimental and development space for:
- Testing new analysis techniques
- Debugging code snippets
- Prototyping features before integration into main notebooks
- Sandbox environment for learning and exploration

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Basic understanding of particle physics 
- Familiarity with Jupyter notebooks
- CMS NanoAOD data files (signal and background samples)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis.git
   cd H-to-WW-NanoAOD-analysis
   ```

2. **Set up a virtual environment (recommended):**
   
   Creating a dedicated Python virtual environment ensures isolation of dependencies and prevents conflicts with other projects.
   
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Linux/macOS
   .venv\Scripts\activate     # On Windows
   ```

3. **Install required dependencies:**
   
   All necessary Python packages are listed in `requirements.txt`. This includes libraries for ROOT file handling (uproot, awkward), data processing (numpy, pandas, dask), and visualization (matplotlib, seaborn).
   
   ```bash
   pip install -r requirements.txt
   ```
   
   Alternatively, if you prefer using conda:
   ```bash
   conda env create -f environment.yml
   conda activate higgs-analysis
   ```

4. **Verify the installation:**
   
   Run the diagnostic script to confirm that your environment is properly configured and can read ROOT files:
   
   ```bash
   python scripts/test_uproot.py
   ```
   
   This script will test basic functionality of the uproot library and verify that your environment can handle NanoAOD data structures.

5. **Obtain NanoAOD datasets:**
   
   Place your CMS NanoAOD ROOT files in the `Datasets/` directory. You will need:
   - Signal samples: Higgs → WW production (ggH, VBF, VH, ttH)
   - Background samples: Top quark pairs (ttbar), Drell-Yan, WW, WZ, ZZ, single top, W+jets
   
   Datasets can be obtained from CMS Open Data portal or through official CMS data access channels.

### Running the Analysis

1. **Start Jupyter:**
   ```bash
   jupyter notebook
   ```

2. **Open the main analysis notebook:**
   Navigate to `notebooks/H_WW_Dask.ipynb` in the Jupyter interface.

3. **Execute the analysis:**
   Run the cells sequentially to perform the complete analysis. The notebook is organized into logical sections:
   - Data loading and file handling
   - Object definitions and selections
   - Event-level cuts and categorization
   - Kinematic variable computation
   - Plotting and visualization
   - Results and interpretation

4. **Explore other notebooks:**
   - Start with `Kinematic_plots.ipynb` for introductory kinematic distributions
   - Review `Global_selection.ipynb` to understand the selection criteria
   - Check `xsec_weights.ipynb` for cross-section normalization details

---

## Analysis Workflow

The complete analysis follows these steps:

1. **Data Loading**: Read NanoAOD files using uproot and awkward arrays
2. **Object Selection**: Apply quality cuts on leptons, jets, and other physics objects
3. **Event Selection**: Implement trigger requirements and event-level criteria
4. **Categorization**: Classify events based on jet multiplicity (0-jet, 1-jet, 2-jet categories)
5. **Background Modeling**: Process and normalize background Monte Carlo samples
6. **Kinematic Calculations**: Compute derived quantities (invariant masses, transverse masses, angular variables)
7. **Weighting**: Apply generator weights, cross-section weights, and scale factors
8. **Visualization**: Create plots comparing signal and background distributions
9. **Statistical Analysis**: Extract signal significance and perform fits

---

## Key Features

- **Parallel Processing**: Utilizes Dask for efficient handling of large datasets
- **Modular Design**: Clean separation of data loading, selection, and analysis steps
- **Comprehensive Documentation**: Well-commented code explaining physics motivation for each step
- **Reproducible**: All random seeds and configurations are specified for consistent results
- **Educational**: Designed to teach both physics analysis techniques and programming best practices

---

## Learning Outcomes

By working through this analysis, users will learn:

- How to read and process CMS NanoAOD data files
- Event selection strategies in particle physics
- Kinematic variable construction and their physics interpretation
- Signal-background discrimination techniques
- Statistical treatment of Monte Carlo simulations
- Data visualization and presentation of physics results
- Computational techniques for handling large datasets

---

## Contributing

This is an active research project. Contributions, suggestions, and feedback are welcome. If you find issues or have ideas for improvements:

1. Open an issue describing the problem or suggestion
2. Fork the repository and create a feature branch
3. Submit a pull request with your changes

---

## Resources

### Physics References
- CMS Higgs to WW Analysis Documentation
- PDG Review on Higgs Physics
- Standard Model and Higgs Mechanism reviews

### Technical Documentation
- [Uproot Documentation](https://uproot.readthedocs.io/)
- [Awkward Array Documentation](https://awkward-array.readthedocs.io/)
- [Dask Documentation](https://docs.dask.org/)

### HSF-India Project
- More information about the HSF-India initiative and related projects

---

## Contact

For questions, issues, or collaboration opportunities related to this analysis, please open an issue in this repository.

---

## Acknowledgments

This work is developed as part of the HSF-India project, which aims to strengthen high-energy physics research capabilities and foster collaboration between international research communities.

---

**Note**: This analysis is based on Monte Carlo simulations and CMS Open Data. Results should be validated and cross-checked before drawing physics conclusions.
