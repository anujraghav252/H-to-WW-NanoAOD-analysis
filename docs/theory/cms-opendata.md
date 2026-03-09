## 1. CMS Open Data and NanoAOD

### 1.1 The CMS Experiment

The **Compact Muon Solenoid (CMS)** is one of two large general-purpose detectors at the Large Hadron Collider (LHC) at CERN. It records proton–proton collisions at a centre-of-mass energy of $\sqrt{s} = 13\,\text{TeV}$, providing data suitable for precision measurements of Standard Model (SM) processes and searches for new phenomena.

![CMS Logo](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/CMS_logo.png){ width="260" }

### 1.2 CMS Open Data

CMS Open Data is the public release of collision data collected by the CMS experiment, hosted on the [CERN Open Data Portal](https://opendata.cern.ch). By releasing high-level reconstructed data, CMS enables:

- **Education** — students can learn particle physics using real LHC data.
- **Independent research** — theorists and data scientists can apply new techniques to existing datasets.
- **Reproducibility** — external verification of scientific results strengthens community trust.

This analysis uses the **2016 Ultra-Legacy (UL) dataset**. "Ultra Legacy" refers to the final, best-quality reprocessing of all Run 2 data (2016–2018), offering the most refined object reconstruction and the lowest systematic uncertainties achievable.

![CERN Open Data](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/opendata.png){ width="260" }

!!! info "Integrated Luminosity"
The 2016 data used in this analysis corresponds to an integrated luminosity of $\mathcal{L}_{\text{int}} \approx 16.15\,\text{fb}^{-1}$, covering run periods **2016G–2016H**.

### 1.3 The NanoAOD Format

**NanoAOD** is a compact data format developed by CMS for the high-luminosity LHC era. It stores only the physics objects needed for analyses (leptons, jets, MET, etc.) as simple ROOT `TTrees`, providing several key advantages:

| Property            | NanoAOD             | MiniAOD          |
| ------------------- | ------------------- | ---------------- |
| File size per event | ~1–2 kB             | ~30–50 kB        |
| ROOT dependency     | Minimal             | Full CMSSW stack |
| Python readability  | Native (via Uproot) | Requires CMSSW   |

Because NanoAOD stores plain numeric types, it can be read directly by modern Python tools like **Uproot** and **Awkward Array** — no compiled CMSSW environment required.

---
