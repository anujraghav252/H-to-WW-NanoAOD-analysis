# Higgs to WW analysis: Using CMS Open Data

This repository is part of the **[HSF-India project](https://research-software-collaborations.org/)**, focusing on the analysis of Higgs boson decays to **W boson pairs (H → WW → 2ℓ2ν)** using CMS Open Data in the NanoAOD format. The analysis targets the **gluon-gluon fusion (ggH)** production mode with **2016 Ultra-Legacy Monte Carlo** samples at **√s = 13 TeV**.

---

## Physics Overview

The **Higgs boson**, discovered in 2012 at the LHC, acquires mass for elementary particles through the mechanism of **electroweak symmetry breaking**. One of its dominant production modes at the LHC is **gluon-gluon fusion (ggH)**, where two gluons interact via a heavy-quark loop (predominantly the top quark) to produce a Higgs boson.

This analysis focuses on the decay channel:

**H → WW\* → eμ + 2ν** (opposite-flavour dilepton final state)

which offers a clean leptonic signature and a sizeable branching fraction, making it a key channel for Higgs measurements.

---

## Key Notebooks

| Notebook                                               | Description                                                                                                                                                                                                    |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [**HWW_analysis.ipynb**](notebooks/HWW_analysis.ipynb) | **Main working notebook.** Contains the full end-to-end analysis: sample loading, object & event selection, kinematic distributions, Data/MC scale factors, and signal-background comparisons. **Start here.** |
| [xsec_weights.ipynb](notebooks/xsec_weights.ipynb)     | Computation of cross-section weights for proper luminosity normalisation.                                                                                                                                      |

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
- **`egammaEffi_TightHWW_2016.txt`** — Electron TightHWW identification efficiencies and scale factors.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis.git
cd H-to-WW-NanoAOD-analysis
```

### 2. Set Up the Environment

**Option A — pip (virtual environment):**

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

**Option B — Conda:**

```bash
conda env create -f environment.yml
conda activate <env-name>
```

### 3. Verify the Installation

A diagnostic script is provided to confirm that the environment is configured correctly:

```bash
python scripts/test_uproot.py
```

### 4. Run the Analysis

Open the **main analysis notebook** and follow along:

```bash
jupyter lab notebooks/HWW_analysis.ipynb
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
![HSF-India Logo](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/hsf-india_logo.png)
