# :material-clipboard-list: **Analysis Strategy and Methodology**

<!-- This analysis transitions away from the traditional High-Energy Physics (HEP) "event-loop" paradigm in favor of modern **columnar processing**. By utilizing the Scikit-HEP ecosystem—specifically `awkward` and `uproot`—distributed across a `Dask` cluster, particle properties are evaluated as contiguous arrays. This enables the rapid, parallel processing of millions of CMS NanoAOD events. -->

The workflow follows a "_Cut-and-Count_" strategy. This methodology is designed to filter proton-proton collisions down to a pure subset of candidate $H \to WW^* \to e^\pm \mu^\mp\nu\bar{\nu}$ events, while simultaneously defining orthogonal control regions to estimate background contamination.

<!-- \<div style="text-align: center;"\>
\<img src="../assets/flowchart.svg" alt="Analysis Workflow Flowchart" width="800"\>
\</div\> -->

---

## :material-database-check: **1. Data Ingestion and Validation**

Before evaluating the physics topology of an event, the raw datasets are validated for detector health and normalized for statistical comparison.

- **Observational Data:** For the real CMS collision data, the analysis strictly processes events recorded during verified periods of optimal detector performance. This is achieved by applying the official CMS [Golden JSON mask](https://opendata.cern.ch/record/14220) which systematically filters out runs and luminosity blocks where sub-detectors were malfunctioning.
<!-- * [`Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt`](https://opendata.cern.ch/record/14220), -->
- **Simulation Normalization (MC):** Monte Carlo datasets are generated with arbitrary event counts. To resolve this, a universal scale factor is applied to weight simulated events to their expected physical yields using the theoretical cross-section ($\sigma$), the integrated luminosity of the 2016 data ($L_{\text{int}} \approx 16.39 \text{ fb}^{-1}$), and the sum of generator weights.

---

## :material-filter-list: **2. Object Definition and Pre-Selection**

The first layer of physics selection isolates events containing the fundamental building blocks of the signal: exactly one electron and one muon.

- **Tight Lepton Selection:** To suppress backgrounds from non-prompt sources (such as heavy-flavor jet decays), only high-quality leptons are selected:
  - **Electrons** must pass the stringent `mvaFall17V2Iso_WP90` identification.
  - **Muons** must pass the standard CMS `TightID` and maintain strict Particle-Flow (PF) isolation.
- **The $e\mu$ Pre-Selection:** The analysis constructs a dilepton candidate by requiring **exactly two** tight leptons in the event. These leptons must possess different flavors, opposite electric charges ($q_e \times q_\mu < 0$), and satisfy baseline kinematic acceptances:
  - Leading lepton $p_T > 25 \text{ GeV}$
  - Sub-leading lepton $p_T > 13 \text{ GeV}$
  - $|\eta| < 2.5$ for electrons and $|\eta| < 2.4$ for muons.

---

## :material-shape-circle-plus: **3. Jet Cleaning and Categorization**

Hadronic jets play a critical role in distinguishing the Higgs production mechanisms and identifying top-quark backgrounds. The analysis evaluates standard jets passing basic ID requirements within $|\eta| < 4.7$. To suppress fake jets from pileup, jets with $p_T < 50 \text{ GeV}$ must also pass a strict Pileup ID (`puId >= 4`).

!!! warning "Lepton-Jet Cross-Cleaning"
Because prompt electrons and muons can be mistakenly reconstructed as jets, a cross-cleaning procedure is enforced. Any jet found within a tight angular cone ($\Delta R < 0.4$) of a selected signal lepton is considered a footprint of that lepton and is removed from the jet collection.

Based on the number of surviving jets with $p_T > 30 \text{ GeV}$, events are partitioned into three orthogonal categories:

1.  **0-Jet Category:** The **most** sensitive region, probing the pure Gluon-Gluon Fusion (ggH) signal.
2.  **1-Jet Category:** Probes ggH events accompanied by Initial State Radiation (ISR).
3.  **2-Jet Category:** Primarily used to probe Vector Boson Fusion (VBF) topologies, though it suffers from heavy top-quark contamination.

---

## **4. Global Kinematic Selection**

To remove the dataset of low-mass resonances and backgrounds lacking true neutrinos, a baseline set of global kinematic thresholds is applied across all jet categories:

- **$E_T^{\text{miss}} > 20 \text{ GeV}$:** Ensures the presence of genuine missing transverse energy from escaping neutrinos, aggressively suppressing backgrounds with low $E_T^{\text{miss}}$.
- **$p_T^{\ell\ell} > 30 \text{ GeV}$:** Demands a moderately boosted dilepton system, rejecting softer background processes.
- **$m_{\ell\ell} > 12 \text{ GeV}$:** Removes low-mass resonances.

---

## **5. Region Definitions (Signal and Control)**

In the final step, the surviving events are sorted into strictly orthogonal regions using boolean masking. The **Signal Region (SR)** isolates the Higgs events, while the **Control Regions (CR)** intentionally isolate backgrounds to validate Monte Carlo modeling.

### **Signal Region (SR)**

Optimized specifically for the $H \to WW^*$ kinematics:

- **$b$-jet Veto:** Absolutely no $b$-tagged jets are permitted. This is the primary defense against the massive $t\bar{t}$ backgrounds.
- **Higgs Transverse Mass:** The system must fall within the expected kinematic edge of the Higgs mass: $m_T^H > 60 \text{ GeV}$.
<!-- * **Sub-leading Transverse Mass:** Requiring $m_T(\ell_2, E_T^{\text{miss}}) > 30 \text{ GeV}$ suppresses $W$+Jets backgrounds where the $E_T^{\text{miss}}$ originates from a single $W$ decay. -->
- **Jet-categorisation:** Then, split the surviving events into three distinct jet categories:
  - **_0-jet category:_** No jet with $p_T\ >\ 30 \text{ GeV}$
  - **_1-jet category:_** 1 jet with $p_T\ >\ 30 \text{ GeV}$
  - **_2-jet category:_** 2 jet with $p_T\ >\ 30 \text{ GeV}$. For the 2-jet category, the dijet invariant mass ($m_{jj}$) is required to be outside the hadronic $W$ boson resonance window ($m_{jj} < 65 \text{ GeV}$ or $m_{jj} > 105 \text{ GeV}$).

### **Control Region: Top-Quark (CR-Top)**

Designed to cleanly capture the top-quark background:

- **Mass Cut:** Requires $m_{\ell\ell} > 50 \text{ GeV}$ to isolate the higher-mass kinematics typical of heavy top-quark decays and no $m_T^H$ requirement.
- **Inverted $b$-jet Veto:** The region strictly requires the presence of $b$-tagged jets.
<!-- * **Jet-categorisation:** Then, split the surviving events into three distinct jet categories:
  * ***0-jet category:*** No jet with $p_T\ >\ 30 \text{ GeV}$
  * ***1-jet category:*** 1 jet with $p_T\ >\ 30 \text{ GeV}$
  * ***2-jet category:*** 2 jet with $p_T\ >\ 30 \text{ GeV}$. -->

---

## **6. Event Weight Corrections and Systematics**

Because Monte Carlo simulations do not perfectly model the CMS detector's response or hardware efficiencies, Trigger Efficiency, Electron-ID, and Muon-IDs Scale Factors (SF) and their associated uncertainties are applied to the MC events.

- **Lepton ID & Isolation:** Corrections for Electron MVA ID, Muon Tight ID, and Muon Isolation are evaluated dynamically based on each lepton's $p_T$ and $\eta$.
- **Trigger Efficiency:** A global High-Level Trigger scale factor is applied to all simulated events to correct for differences in trigger firing rates between data and simulation.

---

## **7. Cutflow Tracking and Histogramming**

Throughout the execution of the notebook, the absolute and weighted number of surviving events is tracked at every major selection checkpoint (e.g., Pre-selection, Global Cuts, SR, CR-Top). This is exported as `Cutflow_Raw.csv` and `Cutflow_scaled.csv` to ensure transparency and reproducibility of the filtering logic.

Finally, the multi-dimensional event arrays are projected into using the `hist` library. These histograms cleanly separate the data by Dataset, Jet Category, and Selection Region, producing the final `.root` files (e.g., `HWW_analysis_output.root`) required for statistical extraction.

---

## **8. Statistical Interpretation (CMS Combine)**

For the last step of the methodology, the signal strength ($\mu$) of the Higgs boson is extracted using [CMS combine package](../combine/statistical-inference.md).

<!-- The output histograms are harvested and prepared into specialized data structures via `prepare_combine.py`. These shapes are injected into text-based **Datacards** (`combined_datacard.txt`) which mathematically define the likelihood model, incorporating the statistical yields of the SR and CRs alongside the assigned systematic uncertainties. The **CMS Combine tool** then performs a maximum profile-likelihood fit on these datacards to evaluate the statistical significance of the $H \to WW^*$ signal. -->

---

A complete flowchart showing all the stages is shown below.

![Flowchart](https://raw.githubusercontent.com/anrghv/H-to-WW-NanoAOD-analysis/main/assets/flowchart.svg)
