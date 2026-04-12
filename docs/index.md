---
template: home.html
title: H → WW NanoAOD Analysis
---

!!! warning "Documentation in Progress"
    This page is under active development — some sections may be incomplete or inconsistent.
    The [repository](https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis) is the authoritative reference in the meantime.

## What This Analysis Does

This analysis searches for the **Standard Model Higgs boson** ($m_H = 125\,\text{GeV}$) decaying
to a pair of $W$ bosons in the opposite-flavour dilepton final state:

$$gg \rightarrow H \rightarrow W^+W^{-*} \rightarrow e^\pm\,\nu_e\;+\;\mu^\mp\,\nu_\mu$$

Working entirely within the **Scikit-HEP Python ecosystem** (Uproot, Awkward Array, Dask), it
demonstrates a complete, modern HEP analysis workflow — from raw NanoAOD files to final statistical
limits — without requiring the traditional C++ ROOT/CMSSW stack.

---

## Key Analysis Properties

<div class="grid cards" markdown>

-   :material-lightning-bolt:{ .lg .middle } **Centre-of-mass energy**

    ---
    $\sqrt{s} = 13\,\text{TeV}$

-   :material-calendar:{ .lg .middle } **Data-taking period**

    ---
    2016 Ultra-Legacy (Run periods G–H)

-   :material-database:{ .lg .middle } **Integrated luminosity**

    ---
    $\mathcal{L}_{\text{int}} \approx 16.39\,\text{fb}^{-1}$

-   :material-atom:{ .lg .middle } **Signal process**

    ---
    $ggH \rightarrow W^+W^- \rightarrow e\nu\,\mu\nu$

-   :material-approximately-equal:{ .lg .middle } **Final state**

    ---
    Opposite-sign, opposite-flavour dilepton ($e\mu$)

-   :material-chart-bell-curve:{ .lg .middle } **Production mode**

    ---
    Gluon–gluon fusion ($ggH$)

</div>

---

## Quick Start

```bash title="Get up and running"
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

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **Physics Background**

    ---
    CMS Open Data, Higgs signal, and background processes.

    [:octicons-arrow-right-24: Theory](theory/higgs-physics.md)

-   :material-database:{ .lg .middle } **Datasets**

    ---
    Sample list, cross sections, and MC normalisation.

    [:octicons-arrow-right-24: Datasets](datasets/data-and-mc.md)

-   :material-wrench:{ .lg .middle } **Software Framework**

    ---
    The Scikit-HEP ecosystem explained.

    [:octicons-arrow-right-24: Framework](software/ecosystem.md)

-   :material-download:{ .lg .middle } **Installation & Setup**

    ---
    Environment setup and verification.

    [:octicons-arrow-right-24: Installation](getting-started/installation.md)

-   :material-folder-open:{ .lg .middle } **Repository Architecture**

    ---
    Directory structure and module overview.

    [:octicons-arrow-right-24: Architecture](getting-started/repository-structure.md)

-   :material-chart-timeline-variant:{ .lg .middle } **Process Flowchart**

    ---
    Full analysis cut-flow and region definitions.

    [:octicons-arrow-right-24: Flowchart](analysis/flowchart.md)

-   :material-play-circle-outline:{ .lg .middle } **Execution Guide**

    ---
    Running notebooks and Dask batch jobs.

    [:octicons-arrow-right-24: Execution](analysis/interactive-execution.md)

-   :material-chart-bar:{ .lg .middle } **Statistical Inference**

    ---
    CMS Combine: datacards, limits, and signal strength.

    [:octicons-arrow-right-24: Combine](combine/statistical-inference.md)

</div>

---

## Acknowledgements

This analysis is developed as part of the **HSF-India project**. Datasets are sourced from the
[CERN Open Data Portal](https://opendata.cern.ch). MC sample configurations follow
[LatinoAnalysis](https://github.com/latinos/LatinoAnalysis) conventions for the Summer20UL16 campaign.