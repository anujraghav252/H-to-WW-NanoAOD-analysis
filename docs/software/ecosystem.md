# Software Framework

This analysis is built on the modern **Scikit-HEP** Python ecosystem, a coordinated collection of libraries designed to replace the traditional C++ ROOT-based workflow with a high-performance, portable, and Pythonic alternative.

---

## 1. From Event Loops to Array-Based Processing

Traditional High-Energy Physics analysis has historically relied on an **event-loop** paradigm: iterate through the dataset one event at a time, reconstruct objects, and fill histograms sequentially. While conceptually simple, this approach suffers from poor performance in Python due to interpreter overhead and the absence of vectorization.

This analysis instead uses **columnar processing**:

> Rather than looping over every muon in every event to check its Transverse momentum, we operate on the _entire Transverse momentum array_ at once, a single NumPy-like operation. The computational burden shifts to compiled, highly optimized C++ kernels.

This approach enables CPU vectorization, reduces Python overhead, and when combined with **Dask** for parallelism, allows the same code to scale from a laptop to a full computing cluster without modification.

---

## 2. The Scikit-HEP Stack

![Scikit-HEP Logo](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/scikit_logo.png){ width="280" }

Each library in the stack addresses a specific challenge of HEP data processing:

### 2.1 Uproot: ROOT I/O without ROOT

[Uproot](https://uproot.readthedocs.io/) reads and writes ROOT files using pure Python, with no dependency on the C++ ROOT framework. In this analysis, Uproot handles the **input/output layer**, streaming NanoAOD `TTrees` from remote XRootD servers directly into memory as NumPy and Awkward arrays.

![Uproot](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/uproot_logo.webp){ width="30%" }

<!-- **Key capability used:** Lazy / chunked reading of remote ROOT files over XRootD. -->

### 2.2 Awkward Array: Jagged data structures

Particle physics data is inherently _irregular_: one event may contain zero muons, the next may have three. Standard flat libraries like NumPy cannot represent this naturally.

[Awkward Array](https://awkward-array.org/) provides **ragged (jagged) array** operations using familiar NumPy-style syntax — slicing, masking, and broadcasting — without losing the variable-length per-event structure.

![Awkward Array](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/awkward.svg){ width="15%" }

**Key capability used:** All lepton and jet collections are stored as Awkward arrays, enabling operations like `leptons[leptons.pt > 25]` without any Python `for` loops.

### 2.3 Vector — Lorentz four-vector arithmetic

Calculating invariant masses ($m_{\ell\ell}$), angular separations ($\Delta R$), and transverse masses requires Lorentz-covariant arithmetic. The [Vector](https://vector.readthedocs.io/) library integrates seamlessly with Awkward Array and provides this with a clean API:

```python
# Reconstruct the dilepton system from individual lepton four-vectors
dilepton = lepton1 + lepton2
m_ll     = dilepton.mass
```

![Vector](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/vector%20logo.svg){ width="15%" }

**Key capability used:** All kinematic reconstruction in `hww_tools/calculations.py`.

### 2.4 Hist — Multi-dimensional histograms

For accumulating event yields and kinematic distributions, this analysis uses [Hist](https://hist.readthedocs.io/), a Python histogramming library built on the fast C++ `boost-histogram` backend.

Hist natively supports:

- **Categorical axes**: simultaneously filling SR, CR-Top, and CR-DY in a single pass.
- **String-keyed variations**: storing nominal + systematic up/down shapes in one object.
- **Sparse storage**: efficient for many-bin, many-category histograms.

![Hist](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/histlogo.png){ width="15%" }

**Key capability used:** All analysis histograms in `hww_tools/Config.py` and filled in `Run_analysis.ipynb`.

### 2.5 Coffea — HEP analysis framework

[Coffea](https://coffea-hep.readthedocs.io/) provides high-level HEP analysis utilities on top of the Awkward/Uproot stack, including a schema layer that maps NanoAOD branch names to physics objects, and integration with Dask for distributed execution.

**Key capability used:** The `NanoAODSchema` is used to interpret NanoAOD branches as structured physics objects (`events.Electron`, `events.Muon`, etc.).

### 2.6 mplhep — CMS-style plotting

[mplhep](https://mplhep.readthedocs.io/) is a Matplotlib extension for High-Energy Physics. It applies CMS publication-quality styling to plots:

- Standard CMS label and preliminary watermarks.
- Proper error bar conventions for data points (Poisson $\sqrt{N}$).
- Stacked histogram conventions for background overlays.

![mplhep](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/mplhep.png){ width="15%" }

**Key capability used:** All Data/MC comparison plots in `hww_tools/plotting.py`.

---

## 3. Distributed Computing with Dask

To handle large-scale CMS data (terabytes of information across many files), this analysis uses [Dask](https://docs.dask.org/) for **task-graph-based parallelism**.

![Dask Logo](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/dask_horizontal.svg){ width="300" }

### How it works

Dask breaks the full dataset into **chunks** (file-level partitions) and constructs a _task graph_ — a directed acyclic graph (DAG) of pending computations. The graph is only evaluated when `.compute()` is called, at which point Dask schedules tasks across available CPU cores.

```python
# Example: submit the analysis to a local Dask cluster
from dask.distributed import Client, LocalCluster

cluster = LocalCluster(n_workers=4)
client  = Client(cluster)

# All processing happens lazily until .compute()
results = run_processor(fileset, processor=HWWProcessor())
results.compute()
```

### Performance gain

| Mode        | Setup                 | Approximate runtime |
| ----------- | --------------------- | ------------------- |
| Sequential  | Single Python process | Several hours       |
| Distributed | 4-core `LocalCluster` | ~20–40 minutes      |

!!! info "Laptop vs. cluster"
The `LocalCluster` used here runs on a single machine with multiple cores. The same code can be submitted to an HTCondor or SLURM batch cluster by swapping the cluster backend — no changes to analysis code required.

---

## 4. Full Dependency Table

| Package         | Version (min) | Role                              |
| --------------- | ------------- | --------------------------------- |
| `python`        | ≥3.10         | Language runtime                  |
| `uproot`        | ≥5.3          | ROOT file I/O                     |
| `awkward`       | ≥2.6          | Jagged array operations           |
| `vector`        | ≥1.3          | Lorentz four-vector arithmetic    |
| `hist`          | ≥2.7          | Histogramming                     |
| `coffea`        | ≥0.7          | NanoAOD schema + Dask integration |
| `dask`          | ≥2024.0.0     | Distributed/parallel computing    |
| `numpy`         | ≥1.26         | Numerical arrays                  |
| `scipy`         | ≥1.13         | Statistical utilities             |
| `matplotlib`    | ≥3.8          | Plotting base                     |
| `mplhep`        | latest        | CMS-style plots                   |
| `fsspec-xrootd` | ≥0.2          | XRootD file access                |
| `jupyterlab`    | ≥4.2          | Notebook environment              |

Full pinned versions: see [`requirements.txt`](https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis/blob/main/requirements.txt) and [`environment.yml`](https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis/blob/main/environment.yml).
