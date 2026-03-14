# **The CMS Open Data**
The **[Compact Muon Solenoid (CMS)](https://home.cern/science/experiments/cms)** is one of two large general-purpose detectors at the Large Hadron Collider (LHC) at CERN. It records proton–proton collisions at a centre-of-mass energy of $\sqrt{s} = 13\,\text{TeV}$, providing data suitable for precision measurements of Standard Model (SM) processes and searches for new phenomena.

<div style="display:flex; justify-content:center; gap:20px;">
  <img src="https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/opendata_cms.png" width="260">
  <img src="https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/CMS_logo.png" width="260">
</div>

CMS Open Data is the public release of collision data collected by the CMS experiment, hosted on the [CERN Open Data Portal](https://opendata.cern.ch). By releasing high-level reconstructed data, CMS enables:

- **Education** — students can learn particle physics using real LHC data.
- **Independent research** — theorists and data scientists can apply new techniques to existing datasets.
- **Reproducibility** — external verification of scientific results strengthens community trust.

This analysis uses the **2016 Ultra-Legacy (UL) dataset**. "Ultra Legacy" refers to the final, best-quality reprocessing of all Run 2 data (2016–2018), offering the most refined object reconstruction and the lowest systematic uncertainties achievable.

!!! info "Integrated Luminosity"
The 2016 data used in this analysis corresponds to an integrated luminosity of [$\mathcal{L}_{\text{int}} \approx 16.39\,\text{fb}^{-1}$](https://opendata.cern.ch/record/1059), covering run periods **2016G–2016H**.

## The NanoAOD Format

**NanoAOD** is a compact data format developed by CMS for the high-luminosity LHC era. It stores only the physics objects needed for analyses (leptons, jets, MET, etc.) as simple ROOT `TTrees`, providing several key advantages:

| Property            | NanoAOD             | MiniAOD          |
| ------------------- | ------------------- | ---------------- |
| File size per event | ~1–2 kB             | ~30–50 kB        |
| ROOT dependency     | Minimal             | Full CMSSW stack |
| Python readability  | Native (via Uproot) | Requires CMSSW   |

Because NanoAOD stores plain numeric types, it can be read directly by modern Python tools like **Uproot** and **Awkward Array**, no compiled CMSSW environment required. For additional details about NanoAOD see the CMS [Twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD).

---
