# **Higgs to WW Analysis: Using CMS Open Data**

Welcome to the documentation for the **[$H \rightarrow WW$ NanoAOD Analysis](https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis)**, an open, reproducible implementation of the $H \rightarrow W^+W^- \rightarrow e\nu\,\mu\nu$ measurement using CMS 2016 Ultra-Legacy Open Data.

This project is developed as part of the **[HSF-India project](https://research-software-collaborations.org/)**, an initiative to foster research software collaborations between India and the international High-Energy Physics community.

![HSF-India Logo](https://raw.githubusercontent.com/anujraghav252/H-to-WW-NanoAOD-analysis/main/assets/hsf-india_logo.png){ width="250" }

---

## What This Analysis Does?

This analysis searches for the **Standard Model Higgs boson** ($m_H = 125\,\text{GeV}$) decaying to a pair of $W$ bosons in the opposite-flavour dilepton final state:

$$gg \rightarrow H \rightarrow W^+W^{-*} \rightarrow e^\pm\,\nu_e\;+\;\mu^\mp\,\nu_\mu$$

Working entirely within the **Scikit-HEP Python ecosystem** (Uproot, Awkward Array, Dask), it demonstrates a complete, modern HEP analysis workflow, from raw NanoAOD files to final statistical limits, without requiring the traditional C++ ROOT/CMSSW stack.

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis.git
cd H-to-WW-NanoAOD-analysis

# 2. Create the environment (Conda recommended)
conda env create -f environment.yml
conda activate HEP_analysis

# 3. Open the main analysis notebook
cd notebooks/
jupyter lab HWW_analysis.ipynb
```

→ Full setup instructions: [Installation & Setup](getting-started/installation.md)

---

## Documentation Guide

| Section                                                            | What you'll find                                      |
| ------------------------------------------------------------------ | ----------------------------------------------------- |
| [Physics Background](theory/physics-background.md)                 | CMS Open Data, Higgs signal, and background processes |
| [Datasets](datasets/data-and-mc.md)                                | Sample list, cross sections, and MC normalization     |
| [Software Framework](software/ecosystem.md)                        | The Scikit-HEP framework explained                    |
| [Installation & Setup](getting-started/installation.md)            | Environment setup and verification                    |
| [Repository Architecture](getting-started/repository-structure.md) | Directory structure and module overview               |
| [Process Flowchart](analysis/flowchart.md)                         | Full analysis cut-flow and region definitions         |
| [Execution Guide](analysis/interactive-execution.md)               | Running notebooks and Dask batch jobs                 |
| [Statistical Inference](combine/statistical-inference.md)          | CMS Combine: datacards, limits, and signal strength   |

---

## Key Analysis Properties

| Property              | Value                                                    |
| --------------------- | -------------------------------------------------------- | ------------------ | -------------------------------------------- | --- | --- |
| Centre-of-mass energy | $\sqrt{s} = 13\,\text{TeV}$                              |
| Data-taking year      | 2016 (Run periods G–H)                                   |
| Integrated luminosity | $\mathcal{L}_{\text{int}} \approx 16.39\,\text{fb}^{-1}$ |
| <!--                  |                                                          | MC campaign        | RunIISummer20UL16 (Ultra-Legacy, NanoAOD v9) |     | --> |
| Signal process        | $ggH \rightarrow W^+W^- \rightarrow e\nu\,\mu\nu$        |
| Final state           | Opposite-sign, opposite-flavour dilepton ($e\mu$)        |
| Production mode       | Gluon-gluon fusion ($ggH$)                               |
| <!--                  |                                                          | Analysis framework | Coffea + Dask (columnar, array-based)        |     | --> |

---

## Acknowledgements

This analysis is developed as part of the **HSF-India project**. The datasets are sourced from the [CERN Open Data Portal](https://opendata.cern.ch). MC sample configurations follow [LatinoAnalysis](https://github.com/latinos/LatinoAnalysis) conventions for the Summer20UL16 campaign.
