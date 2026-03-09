# Installation & Setup

This page describes how to set up the analysis environment on a local machine or a remote cluster.

---

## Requirements

- **Python ≥ 3.10**
- **Git**
- **Conda** (recommended) or **pip + virtualenv**
- Network access to CERN EOS via XRootD (for remote file reading)

---

## 1. Clone the Repository

```bash
git clone https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis.git
cd H-to-WW-NanoAOD-analysis
```

---

## 2. Set Up the Python Environment

=== "Conda (recommended)"

    The repository includes a complete `environment.yml` that specifies all required packages with minimum version constraints:

    ```bash
    conda env create -f environment.yml
    conda activate HEP_analysis
    ```

    This creates a Conda environment named `HEP_analysis` with:

    - All Scikit-HEP packages (`uproot`, `awkward`, `vector`, `hist`, `coffea`)
    - Dask for distributed computing
    - Jupyter Lab for interactive notebooks
    - `fsspec-xrootd` for XRootD file access

=== "pip (virtual environment)"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate   # Linux / macOS
    # .venv\Scripts\activate    # Windows

    pip install -r requirements.txt
    ```

!!! note "Windows"
The analysis runs on Windows, macOS, and Linux. On Windows, use Conda (via Miniconda or Anaconda) for the most reliable experience, as some dependencies have complex build requirements.

---

## 3. Verify the Installation

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
    "root://eospublic.cern.ch//eos/opendata/cms/mc/"
    "RunIISummer20UL16NanoAODv9/GluGluHToWWTo2L2N_M-125"
    "_TuneCP5_minloHJJ_13TeV-powheg-jhugen727-pythia8/"
    "NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/30000/"
    "00B3B6E3-3D68-C048-A8C4-04EB699CCE5D.root"
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

For a step-by-step walkthrough of the notebook and how to run a full batch job with Dask, see the [Execution Guide](../analysis/interactive-execution.md).

---

## Troubleshooting

??? question "Conda env create fails with solver errors"
Try using the `libmamba` solver which is significantly faster and more reliable:
`bash
    conda install -n base conda-libmamba-solver
    conda env create -f environment.yml --solver=libmamba
    `

??? question "XRootD not found / import error"
`fsspec-xrootd` requires the `xrootd` C++ library. On Linux this is available via Conda:
`bash
    conda install -c conda-forge xrootd
    `
On Windows and macOS, Conda from the `conda-forge` channel is the recommended route.

??? question "coffea import error after pip install"
Coffea ≥ 0.7 requires Python ≥ 3.8. If you are using a system Python, make sure to create an isolated virtual environment first.
