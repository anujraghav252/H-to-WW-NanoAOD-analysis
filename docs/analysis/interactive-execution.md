# Execution Guide

This page explains how to run the analysis: from an interactive step-by-step exploration in Jupyter to a fully automated distributed batch run using Dask.

---

## Prerequisites

Make sure the environment is set up and verified before proceeding:

- [Installation & Setup](installation.md) — clone the repo and install all dependencies.
- XRootD access to CERN EOS (required for remote file reading).

---

## 1. Notebook-Based Interactive Execution

The recommended starting point is the **main analysis notebook**, which runs the full pipeline interactively.

### 1.1 Launch JupyterLab

```bash
cd Run_analysis/
jupyter lab Run_analysis.ipynb
```

The notebook is structured to be run **cell-by-cell**, and each section is documented with physics context, code explanations, and expected outputs.

### 1.2 Notebook Structure

| Section            | What it does                                                                    |
| ------------------ | ------------------------------------------------------------------------------- |
| **Setup**          | Imports, connects to a local Dask cluster, and loads sample file lists          |
| **Sum of Weights** | Reads all samples to compute $\sum w_{\text{gen}}$ for luminosity normalization |
| **Run Processor**  | Submits the analysis to Dask and populates histograms                           |
| **Cutflow**        | Prints a formatted cutflow table showing event yields at each selection stage   |
| **Data/MC Plots**  | Produces stacked Data/MC comparison plots for SR, CR-Top, and CR-DY             |

### 1.3 Starting a Local Dask Cluster

The analysis uses Dask for parallelism. A `LocalCluster` running on your machine is sufficient for testing:

```python
from dask.distributed import Client, LocalCluster

cluster = LocalCluster(n_workers=4, threads_per_worker=1)
client  = Client(cluster)
print(client.dashboard_link)   # Open dashboard in browser
```

!!! tip "Dask Dashboard"
Opening `client.dashboard_link` in a browser shows real-time task progress, memory usage, and worker status. It is essential for monitoring long runs.

### 1.4 Running the Analysis Processor

```python
from hww_tools.run_analysis import run_processor

# fileset: dict mapping dataset names to lists of XRootD paths
results = run_processor(
    fileset   = fileset,
    chunksize = 100_000,   # events per Dask task
    maxchunks = None,      # set to e.g. 10 for testing on a subset
)
```

Set `maxchunks` to a small number (e.g. `10`) during development to get fast turnaround on a subset of the data before committing to a full run.

---

## 2. Supplementary Notebooks

### 2.1 Cross-Section Weights (`xsec_weights.ipynb`)

Before running the main analysis, the sum of generator weights ($\sum w_{\text{gen}}$) must be computed for every MC sample. This notebook:

1. Loops over all sample files in `Datasets/*.txt`.
2. Reads the `genWeight` branch for every event.
3. Outputs a dictionary `{sample_name: sum_of_weights}`.

```bash
jupyter lab notebooks/xsec_weights.ipynb
```

!!! warning "Run this first"
The main analysis notebook relies on the output of `xsec_weights.ipynb`. If you skip this step, MC normalization will be incorrect.

### 2.2 Data/MC Correction Notebooks (`notebooks/Data-MC_corrections/`)

These notebooks derive the **scale factors (SF)** used to correct MC efficiency to match data. They should be run before the main analysis if the efficiency files in `Auxillary_files/Efficiencies/` need to be updated.

| Notebook                     | Scale factor derived                   |
| ---------------------------- | -------------------------------------- |
| `Lepton_ID_efficiency.ipynb` | Electron MVA WP90 ID efficiency        |
| `Muon_EFF.ipynb`             | Muon tight ID and isolation efficiency |
| `Trigger_efficiency.ipynb`   | eμ cross-trigger efficiency            |

```bash
jupyter lab notebooks/Data-MC_corrections/Trigger_efficiency.ipynb
```

The derived efficiency tables are saved as plain-text files in `Auxillary_files/Efficiencies/`, and are loaded at runtime by `hww_tools/Efficiency_data.py`.

---

## 3. Full Batch Run

For a complete production run over all samples:

1. **Start a Dask cluster** (local or remote).
2. **Compute sum of weights** (run `xsec_weights.ipynb` or equivalent script).
3. **Run the main processor** with `maxchunks=None` to process all events.
4. **Save output histograms** to a ROOT file for CMS Combine.
5. **Run `prepare_combine.py`** to generate the datacard and input ROOT file.

```bash
# From Run_analysis/
python prepare_combine.py
```

See [Statistical Inference](../combine/statistical-inference.md) for what to do with the Combine output files.

---

## 4. Expected Outputs

After a successful run, the following files should appear in `Outputs/`:

| File                 | Description                                         |
| -------------------- | --------------------------------------------------- |
| `combine_input.root` | ROOT file containing all histograms for CMS Combine |
| `hww_datacard.txt`   | CMS Combine datacard (physics model + systematics)  |
| `cutflow_*.txt`      | Cutflow tables exported from the notebook           |
| `plots/`             | Data/MC comparison plots (`.png` / `.pdf`)          |

---

## 5. Troubleshooting

??? question "XRootD connection errors"
Make sure you have a valid CERN user account or are running from a machine with access to the CERN EOS public instance. Test connectivity with:
`bash
    xrdcp root://eospublic.cern.ch//eos/opendata/cms/mc/ /dev/null
    `

??? question "Dask workers run out of memory"
Reduce `chunksize` in `run_processor()` (try `50_000` instead of `100_000`) or increase the memory limit per worker in `LocalCluster`.

??? question "Negative sum of weights"
This is expected for some NLO samples where some events carry negative generator weights. The normalization formula handles this correctly — do not substitute the event count for $\sum w_{\text{gen}}$.
