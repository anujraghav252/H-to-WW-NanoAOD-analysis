# Software Framework

This analysis is built on the modern [**Scikit-HEP**](https://scikit-hep.org/) ecosystem, a coordinated collection of libraries designed for providing Particle Physics at large with an ecosystem for data analysis in Python. Some of the tutorials for Scikit-HEP can be found [here](https://hsf-training.github.io/hsf-training-scikit-hep-webpage/) and some more from HSF [here](https://hsf-training.org/training-center/).

---

## 1. From Event Loops to Array-Based Processing

Traditional High-Energy Physics analysis has historically relied on an **event-loop** paradigm: iterating through the dataset one event at a time, reconstructing objects, and filling histograms sequentially. While conceptually simple, this approach suffers from poor performance in Python due to interpreter overhead and the absence of vectorization.

This analysis instead uses **columnar processing**:

> Rather than looping over every muon in every event to check its Transverse momentum, we operate on the *entire Transverse momentum array* at once—a single NumPy-like operation. The computational burden shifts to compiled, highly optimized C++ kernels.

This approach enables CPU vectorization, reduces Python overhead, and, when combined with **Dask** for parallelism, allows the same code to scale from a laptop to a full computing cluster without modification. You can read more about "array-oriented" programming or "coloumnar" processing [here](https://hsf-training.github.io/hsf-training-scikit-hep-webpage/skhep-tutorial/introduction/).

---

## 2. The Scikit-HEP Stack

<div align="center">
<img src="https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/scikit_logo.png" width="280">
</div>

Each library in the stack addresses a specific challenge of HEP data processing:

---

### 2.1 Uproot: ROOT I/O without ROOT

[Uproot](https://uproot.readthedocs.io/) reads and writes ROOT files using pure Python, with no dependency on the C++ ROOT framework. In this analysis, Uproot handles the **input/output layer**, streaming NanoAOD `TTrees` from remote XRootD servers directly into memory as NumPy and Awkward arrays.

<div align="center">
<img src="https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/uproot_light.png" class="only-light" width="30%">
<img src="https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/uproot_dark.webp" class="only-dark" width="30%">
</div>

<!-- **Key capability used:** Lazy / chunked reading of remote ROOT files over XRootD. -->

---

### 2.2 Awkward Array: Jagged data structures

Particle physics data is inherently *irregular*: one event may contain zero muons, while the next may have three. Standard flat libraries like NumPy cannot represent this naturally.

[Awkward Array](https://awkward-array.org/) provides **jagged array** operations that allow us to manipulate these irregular, nested structures using NumPy-like idioms (slicing, masking, and broadcasting) without losing the event structure.

<div align="center">
<img src="https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/awkward.svg" width="30%">
</div>

---

### 2.3 Vector: Lorentz four-vector arithmetic

Calculating physical quantities such as invariant masses ($m_{\ell\ell}$), angular separations ($\Delta R$), and Lorentz boosts is handled by the [Vector](https://vector.readthedocs.io/en/latest/) library. It integrates seamlessly with Awkward Array, allowing us to perform complex 4-vector arithmetic on millions of particles simultaneously:

```python
# Reconstruct the dilepton system from individual lepton four-vectors
dilepton = lepton1 + lepton2
m_ll     = dilepton.mass
```

<div align="center">
<img src="https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/vector%20logo.svg" width="30%">
</div>

---

### 2.4 Hist: Multi-dimensional histograms

For the final accumulation of yields and distributions, we employ [Hist](https://hist.readthedocs.io/en/latest/). Based on the fast C++ `boost-histogram` library, Hist supports multi-dimensional, sparse, and categorical axes. This is essential for our analysis, which requires simultaneous categorization of events into multiple regions (Signal, Control) and systematic variations within a single object.

<div align="center">
<img src="https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/histlogo.png" width="30%">
</div>

<!-- **Key capability used:** All analysis histograms in `hww_tools/Config.py` and filled in `Run_analysis.ipynb`. -->

---

### 2.5 mplhep: CMS-style plotting

[mplhep](https://github.com/scikit-hep/mplhep) is a Matplotlib extension for high-energy physics. It provides tools for plotting data in the standard HEP style, including axis formatting, error bar conventions, and legend placement. In this analysis, mplhep is used to create standardized plots of the signal and control regions.

<div align="center">
<img src="https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/mplhep_light.png" class="only-light" width="30%">
<img src="https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/mplhep_dark.png" class="only-dark" width="30%">
</div>

---

## 3. Distributed Computing with Dask

<div align="center">
<img src="https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/Dask_light.png" class="only-light" width="300">
<img src="https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/Dask_dark.png" class="only-dark" width="300">
</div>

To handle the massive scale of CMS data (terabytes of information), we leverage [Dask](https://docs.dask.org/en/stable/), a flexible parallel computing library. Dask allows us to scale the same Python analysis from a single laptop to a cluster of machines without rewriting the code. It achieves this by breaking the dataset into smaller *“chunks”* (partitions) and processing them in parallel.

In this analysis, Dask is used to distribute the event processing across multiple CPU cores, significantly reducing the runtime.

To quantify the performance gain, we compare the wall-clock time required to process the full dataset:

* **Sequential Processing:** Processing the full dataset on a single core would be CPU-bound, taking several hours to complete.
* **Distributed Processing:** By distributing the workload across the Dask cluster, the total processing time is reduced to minutes.

| Mode        | Setup                     | Approximate runtime |
| ----------- | ------------------------- | ------------------- |
| Sequential  | Single Python process     | Several hours       |
| Distributed | multi-core `LocalCluster` | ~8–12 minutes       |

This reduction in runtime is important for the iterative nature of the analysis, where selection cuts and strategies are refined repeatedly. Faster processing enables quicker feedback and more efficient development cycles.

---

## 4. Full Dependency Table

### Core

* `python` — Language runtime
* `numpy` — Numerical arrays
* `scipy` — Statistical utilities

### I/O and Data Structures

* `uproot` — ROOT file I/O
* `awkward` — Jagged array operations
* `fsspec-xrootd` — XRootD file access

### Physics and Analysis

* `vector` — Lorentz four-vector arithmetic
* `hist` — Histogramming

### Parallel Computing

* `dask` — Distributed/parallel computing

### Visualization

* `matplotlib` — Plotting base
* `mplhep` — CMS-style plots

### Environment

* `jupyterlab` — Notebook environment



Full pinned versions: see [`requirements.txt`](https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis/blob/main/requirements.txt) and [`environment.yml`](https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis/blob/main/environment.yml).
