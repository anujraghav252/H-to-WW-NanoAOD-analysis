# Installation & Setup

This page describes how to set up the analysis environment on a local machine or a remote cluster.

---

## Requirements

!!! info "Automatic Installation"
    All dependencies are installed automatically via `environment.yml` (Conda) or `requirements.txt` (pip).
    See [Set Up the Python Environment](#2-set-up-the-python-environment) for instructions.

### System & Environment

<div class="grid cards" markdown>

-   :material-language-python:{ .lg .middle } **Python ≥ 3.10**

    ---
    Required for all analysis scripts and notebooks.

-   :material-git:{ .lg .middle } **Git**

    ---
    For cloning the repository.

-   :material-hammer-wrench:{ .lg .middle } **C++ Compiler**

    ---
    Required for XRootD and compiled dependencies.
    GCC or Clang on Linux/macOS; use Conda on Windows.

-   :material-package-variant-closed:{ .lg .middle } **Conda** *(recommended)*

    ---
    Handles complex binary dependencies reliably.
    Requires Miniconda or Anaconda. `pip + virtualenv` also supported.

</div>

### Scikit-HEP Stack

<div class="grid cards" markdown>

-   :material-atom:{ .lg .middle } **uproot**

    ---
    ROOT file I/O in pure Python — no ROOT installation required.

-   :material-table-large:{ .lg .middle } **awkward**

    ---
    Columnar arrays for nested, variable-length data structures.

-   :material-axis-arrow:{ .lg .middle } **vector**

    ---
    Lorentz 4-vector calculations with NumPy and Awkward backends.

-   :material-chart-histogram:{ .lg .middle } **hist**

    ---
    Histogram management, filling, and plotting with a Pythonic API.

-   :material-chart-line:{ .lg .middle } **mplhep**

    ---
    Publication-ready HEP-style plots with CMS, ATLAS, and LHCb styles.

</div>

### Data Access, Computing & Interactivity

<div class="grid cards" markdown>

-   :material-server-network:{ .lg .middle } **fsspec-xrootd · xrootd**

    ---
    Stream ROOT files directly from CERN EOS — no local download required.

-   :material-math-compass:{ .lg .middle } **NumPy · pandas · SciPy · Matplotlib**

    ---
    Standard scientific Python stack for numerical computing and visualisation.

-   :material-flash:{ .lg .middle } **Dask**

    ---
    Distributed execution and lazy evaluation for large-scale NanoAOD workflows.

-   :material-notebook-outline:{ .lg .middle } **JupyterLab · ipywidgets · ipykernel**

    ---
    Interactive notebook environment with widget and kernel support.

</div>

---

## 1. Clone the Repository

```bash title="Terminal"
git clone https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis.git
cd H-to-WW-NanoAOD-analysis
```

---
## 2. Set Up the Python Environment

=== ":material-package-variant-closed: Conda (recommended)"

    The repository includes a complete `environment.yml` specifying all required packages
    with minimum version constraints:

    ```bash title="Create and activate the environment"
    conda env create -f environment.yml
    conda activate HEP_analysis
    ```

    This creates a Conda environment named `HEP_analysis` with:

    - All Scikit-HEP packages (`uproot`, `awkward`, `vector`, `hist`)
    - Dask for distributed computing
    - JupyterLab for interactive notebooks
    - `fsspec-xrootd` for XRootD file access

=== ":material-language-python: pip (virtual environment)"

    ```bash title="Create and activate the virtual environment"
    python3 -m venv .venv
    source .venv/bin/activate   # Linux / macOS
    # .venv\Scripts\activate    # Windows
    pip install -r requirements.txt
    ```

!!! note "Windows"
    The analysis runs on Windows, macOS, and Linux. On Windows, **Conda is strongly recommended** —
    some dependencies have complex build requirements that Conda resolves automatically.

## 3. Verify the Installation

=== ":material-check-circle-outline: Package check"

```python title="Verify all packages"
    import uproot, awkward as ak, vector, hist, dask
    print("All packages loaded successfully.")
    print(f"  uproot  : {uproot.__version__}")
    print(f"  awkward : {ak.__version__}")
    print(f"  dask    : {dask.__version__}")
```

=== ":material-server-network: XRootD connectivity"

```python title="Test CERN EOS access"
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

```bash title="Launch the notebook"
cd notebooks/
jupyter lab HWW_analysis.ipynb
```

For a step-by-step walkthrough and instructions for running a full batch job with Dask,
see the [Analysis notebook](../analysis/HWW_analysis.ipynb).