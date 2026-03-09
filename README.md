# HSF-India Project: H → WW NanoAOD Analysis

[![Documentation](https://readthedocs.org/projects/h-to-ww-nanoaod-analysis/badge/?version=latest)](https://h-to-ww-nanoaod-analysis.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/github/license/anujraghav252/H-to-WW-NanoAOD-analysis?color=blue)](LICENSE)
![Repo Size](https://img.shields.io/github/repo-size/anujraghav252/H-to-WW-NanoAOD-analysis)
![Last Commit](https://img.shields.io/github/last-commit/anujraghav252/H-to-WW-NanoAOD-analysis)
![Python](https://img.shields.io/badge/Python-blue?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?logo=Jupyter&logoColor=white)
![Dask](https://img.shields.io/badge/Dask-Parallel_Computing-orange?logo=dask&logoColor=white)
![Scikit-HEP](https://img.shields.io/badge/Ecosystem-Scikit--HEP-brightgreen)
![CMS Open Data](https://img.shields.io/badge/Data-CMS_Open_Data-red)
![H to WW](https://img.shields.io/badge/Analysis-H_%E2%86%92_WW-blueviolet)

> **Disclaimer:** This repository is a work in progress. The code, documentation, and data may change frequently as updates and improvements are made.

The full documentation for this analysis is available at:
https://h-to-ww-nanoaod-analysis.readthedocs.io/en/latest/

This repository is part of the **[HSF-India project](https://research-software-collaborations.org/)**, focusing on the analysis of Higgs boson decays to **W boson pairs (H → WW → 2ℓ2ν)** using CMS Open Data in the NanoAOD format. The analysis targets the **gluon-gluon fusion (ggH)** production mode with **2016 Ultra-Legacy Monte Carlo** samples at **√s = 13 TeV**.

---

## Physics Overview

The **Higgs boson**, discovered in 2012 at the LHC, acquires mass for elementary particles through the mechanism of **electroweak symmetry breaking**. One of its dominant production modes at the LHC is **gluon-gluon fusion (ggH)**, where two gluons interact via a heavy-quark loop (predominantly the top quark) to produce a Higgs boson.

This analysis focuses on the decay channel:

**$H \to WW \to e\mu + \nu_e\nu_\mu$** (opposite-flavour dilepton final state)

which offers a clean leptonic signature and a sizeable branching fraction, making it a key channel for Higgs measurements.

---

## Repository Structure

```
H-to-WW-NanoAOD-analysis/
│
├── notebooks/                        # Analysis notebooks
│   ├── HWW_analysis.ipynb            # ★ Main analysis notebook (start here)
│   ├── Kinematic_plots.ipynb         # Introductory kinematic distributions
│   ├── Global_selection.ipynb        # Event selection criteria (global + 0-jet)
│   ├── xsec_weights.ipynb            # Cross-section weight computation
│   ├── Eff_txt_file_cleaning.ipynb   # Efficiency text file parsing/cleaning
│   ├── Physics_cuts.md               # Summary of physics selection cuts
│   ├── Data-MC_corrections/          # Data/MC correction & efficiency studies
│   │   ├── Lepton_ID_efficiency.ipynb
│   │   ├── Muon_EFF.ipynb
│   │   └── Trigger_efficiency.ipynb
│   └── plots_mplhep/                # Plots styled with mplhep (CMS style)
│
├── Auxillary_files/                  # Supporting input files
│   ├── Efficiencies/                 # Efficiency & scale-factor text files
│   │   ├── Eff_note.txt              # Trigger efficiency notes & cut summary
│   │   ├── Muon_tight_Eff.txt        # Muon tight-ID efficiency & SFs
│   │   ├── Muon_ISO_Eff.txt          # Muon isolation efficiency & SFs
│   │   └── egammaEffi_TightHWW_2016.txt  # Electron ID efficiency & SFs
│   ├── Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt  # Golden JSON
│   ├── Muon_ISO_Eff.txt              # Muon ISO efficiency (flat format)
│   ├── Muon_tight_Eff.txt            # Muon tight-ID efficiency (flat format)
│   ├── egammaEffi_TightHWW_2016.txt  # Electron efficiency (flat format)
│   ├── NUM_TightHWW_DEN_TrackerMuons_eta_pt.root   # Muon ID SF ROOT file
│   └── NUM_TightHWW_ISO_DEN_TightHWW_eta_pt.root   # Muon ISO SF ROOT file
│
├── Datasets/                         # MC sample definitions & cross sections
│   ├── README_MC_Samples_2016UL.md   # Sample table with cross sections & links
│   └── Summer20UL16_106x_noHIPM_nAODv9.py  # NanoAOD sample paths
│
├── Plots/                            # Saved output plots
├── Rollbacks/                        # Previous notebook versions / snapshots
├── Test/                             # Scratch / testing notebooks
├── scripts/
│   └── test_uproot.py                # Diagnostic script to verify environment
│
├── requirements.txt                  # Python dependencies (pip)
├── environment.yml                   # Conda environment specification
├── Higgs.md                          # Extended Higgs physics notes
└── .gitignore
```

---

<!--
## Key Notebooks

| Notebook                                               | Description                                                                                                                                                                                                    |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [**HWW_analysis.ipynb**](notebooks/HWW_analysis.ipynb) | **Main working notebook.** Contains the full end-to-end analysis: sample loading, object & event selection, kinematic distributions, Data/MC scale factors, and signal-background comparisons. **Start here.** |
| [xsec_weights.ipynb](notebooks/xsec_weights.ipynb)     | Computation of cross-section weights for proper luminosity normalisation.                                                                                                                                      | -->
<!--
### Data/MC Corrections (`notebooks/Data-MC_corrections/`)

| Notebook                                                                               | Description                                               |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| [Lepton_ID_efficiency.ipynb](notebooks/Data-MC_corrections/Lepton_ID_efficiency.ipynb) | Lepton identification efficiency scale-factor derivation. |
| [Muon_EFF.ipynb](notebooks/Data-MC_corrections/Muon_EFF.ipynb)                         | Muon efficiency studies (tight-ID & isolation).           |
| [Trigger_efficiency.ipynb](notebooks/Data-MC_corrections/Trigger_efficiency.ipynb)     | Trigger efficiency calculation for the eμ cross-triggers. |

### Efficiency Files (`Auxillary_files/Efficiencies/`)

The efficiency scale factors used in the analysis are stored as plain-text lookup tables in [`Auxillary_files/Efficiencies/`](Auxillary_files/Efficiencies/):

- **`Eff_note.txt`** — Documents the trigger efficiency (91.29 ± 0.08 %) and the full set of kinematic cuts used.
- **`Muon_tight_Eff.txt`** / **`Muon_ISO_Eff.txt`** — Muon tight-ID and isolation efficiencies with scale factors binned in (η, pT).
- **`egammaEffi_TightHWW_2016.txt`** — Electron TightHWW identification efficiencies and scale factors. -->

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis.git
cd H-to-WW-NanoAOD-analysis
```

<!-- --- -->

### 2. Set Up the Python Environment

#### 2.1 Conda (recommended)

The repository includes a complete `environment.yml` that specifies all required packages with minimum version constraints:

```bash
conda env create -f environment.yml
conda activate HEP_analysis
```

This creates a Conda environment named `HEP_analysis` with:

- All Scikit-HEP packages (`uproot`, `awkward`, `vector`, `hist`)
- Dask for distributed computing
- Jupyter Lab for interactive notebooks
- `fsspec-xrootd` for XRootD file access

#### 2.2 pip (virtual environment)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

> **Note (Windows):**
> The analysis runs on Windows, macOS, and Linux. On Windows, use Conda (via Miniconda or Anaconda) for the most reliable experience, as some dependencies have complex build requirements.

---

### 3. Verify the Installation

Launch Python and run a quick sanity check:

```python
import uproot, awkward as ak, vector, hist, coffea, dask
print("All packages loaded successfully.")
print(f"  uproot  : {uproot.__version__}")
print(f"  awkward : {ak.__version__}")
print(f"  coffea  : {coffea.__version__}")
print(f"  dask    : {dask.__version__}")
```

Or test XRootD connectivity:

```python
import fsspec

with fsspec.open(
    (
        "root://eospublic.cern.ch//eos/opendata/cms/mc/"
        "RunIISummer20UL16NanoAODv9/"
        "Higgs0Mf05ph0ToWW_M-125_TuneCP5_13TeV-powheg-jhugen727-pythia8/"
        "NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/40000/"
        "2600A354-96F9-4C48-99FA-D77C85CB7806.root"
    )
) as f:
    print("XRootD connection OK:", f.path)
```

---

## 4. Run the Analysis

Open the main analysis notebook:

```bash
cd notebooks/
jupyter lab HWW_analysis.ipynb
```

---

## Datasets

All Monte Carlo samples correspond to the **CMS 2016 Ultra-Legacy (Summer20UL16) campaign** and are sourced from CERN Open Data. A full listing of samples, cross sections, and links is available in [`Datasets/README_MC_Samples_2016UL.md`](Datasets/README_MC_Samples_2016UL.md).

| Category        | Example Processes                                 |
| --------------- | ------------------------------------------------- |
| **Signal**      | ggH → WW → 2ℓ2ν                                   |
| **Backgrounds** | Drell-Yan, tt̄, Single-top, WW, WZ, ZZ, Wγ, W+jets |

---

## Dependencies

The analysis is built on the modern Python HEP stack:

- **Data I/O:** `uproot`, `awkward`, `fsspec-xrootd`
- **Analysis:** `coffea`, `hist`, `vector`, `scipy`
- **Computing:** `numpy`, `pandas`, `dask`
- **Visualisation:** `matplotlib` (with `mplhep` CMS styling)
- **Environment:** `jupyterlab`, `ipywidgets`

See [`requirements.txt`](requirements.txt) for the full pinned list.

---

## Acknowledgements

This analysis is developed as part of the **HSF-India project**, an initiative to foster research software collaborations between India and the international High Energy Physics community.

<p align="center">
  <img src="assets/hsf-india_logo.png" width="200">
</p>
