# CMS Open Data Project: $H \rightarrow W^+W^-$  Analysis

## 1. Introduction to CMS Open Data

### 1.1 The CMS Experiment at the LHC

<div align="center">
<img src="Images/CMS_logo.png" alt="CMS Logo" width="300"/>
</div>

The Compact Muon Solenoid (CMS) is one of the two large general-purpose particle physics detectors built on the Large Hadron Collider (LHC) at CERN. It is designed to investigate a wide range of physics, including the study of the [Standard Model](https://home.cern/science/physics/standard-model) (the framework that describes the fundamental particles and their interactions), the search for extra dimensions, and particles that could make up dark matter.


### 1.2 What is CMS Open Data? 

<div align="center">
<img src="Images/opendata_cms.png" alt="CMS Open Data" width="400"/>
</div>

CMS Open Data is the public release of data collected by the CMS experiment. It represents a commitment to scientific transparency and the long-term value of the data collected at the LHC. The data is hosted on the [CERN Open Data Portal](https://opendata.cern.ch).
 
 #### 1.2.1 What is the purpose of CMS Open Data?
 The primary goal of the Open Data project is to democratize access to high-energy physics. Traditionally, analyzing LHC data required membership in the collaboration and access to restricted computing grids. By releasing high-level data to the public, CMS enables:

 - **Education**: Students can learn particle physics using real data.

 - **Independent Research**: Theorists and data scientists can test new models or apply novel machine learning techniques to existing datasets.

 - **Reproducibility**: External verification of scientific results strengthens the community's trust in the findings.

 This analysis utilizes the 2016 Ultra Legacy (UL) dataset. In CMS terms, "Legacy" refers to the reprocessing of data after the data-taking run has concluded. "Ultra Legacy" represents the ultimate refinement of the Run 2 data (2016-2018), offering the best possible object reconstruction performance and reduced systematic uncertainties.

 #### 1.2.2 What is NanoAOD? 
 NanoAOD is a data format developed by the CMS collaboration to adderss the computing challenges of the high-luminosity LHC era. It offer several distinct advantages for open data analysis:
 - **Size**: It is approximately 20-50 times smaller than its predecessor (MiniAOD), makes it feasible to stored on local machines and processed rapidly in the cloud.
 - **Portability**: NanoAOD stores simple native types which makes it readable by non-ROOT tools, specifically the **Python scientific ecosystem** (Numpy, Pandas, Awkward Array)
 
 To read more about CMS data formats refer this [twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookAnalysisOverviewIntroduction) and for NanoAOD read this [twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD)

---
## 2. Physics Framework: Signal and Backgrounds

### 2.1 The Higgs Boson and $e\mu$ channel
The Standard Model of particle physics was completed with the discovery of the [Higgs boson](https://home.cern/science/physics/higgs-boson) in 2012 at the LHC.  
This analysis searches for the Higgs boson decaying into a pair of $W$ bosons, which subsequently decay into leptons.

<div align="center">

$gg \to WW \to e\nu_e + \mu\nu_\mu$

</div>

We are specifically focussing on the Opposite sign, Different Flavour (DF) final state.

- **Why this channel?** The $e\mu$ combination eliminates the massive background from Z boson decays ($Z \to \mu\mu$ or $Z \to ee$), providing a much cleaner signal sample than same flavour channels.
- **The Challenge:** The presence of two neutrinos means the full invariant mass of the Higgs cannot be reconstructed. Instead of a sharp mass peak, we rely on the **Transverse Mass** and lepton kinematics to distinguish the signal from the background.

**So, what does the signal look like?**
1. **Two isolated leptons** ($e, \mu$) with high transverse momentum ($p_T$).
2. **opposite electric charge** ($q_e \cdot q_\mu = -1$)
3. **Missing Transverse Energy** ($E_T^{miss}$) due to escaping neutrinos.
4. **Spin correlation:** Since the Higgs has spin-0, the two charged leptons tend to be emitted close to each other in the detector (small $\Delta \phi_{\ell\ell}$), unlike many background processes where they are back-to-back.


### 2.2 Background Processes
Several Standard Model processes mimic this signature. Understanding how they differ is crucial for defining our selection cuts.

For better understanding, let us categorize the backgrounds into two categories.

#### 2.2.1 Irreducible Backgrounds
These processes produce the exact same final state ($e^\pm \mu^\mp + MET$) as the signal and cannot be removed by object selection alone.

1. **$q\bar{q} \to WW$ (Sample: `WW`):**  
   The dominant irreducible background. It consists of continuum $W$ pair production from quark-antiquark annihilation. Unlike the scalar Higgs (spin-0), these events have different spin correlations, leading to larger opening angles ($\Delta \phi_{\ell\ell}$) between the leptons.

2. **$gg \to WW$ (Sample: `ggWW`):**  
   A rarer process where gluons fuse to form $W$ pairs via loop diagrams. While kinematically similar to the signal, it is treated as a distinct background component in this analysis.


#### 2.2.2 Reducible Backgrounds
These processes mimic the signal due to lost particles, misidentification, or specific decay chains.

1. **Top Quark Processes (Sample: `Top_antitop`):**
   - **$t\bar{t}$ Production:** The most abundant background. Top quarks decay as $t\to Wb$. If both W bosons decay leptonically, the final state is $e\mu + MET + 2b$-jets.
   - **Single Top:** Events where a single top quark is produced, often associated with a W boson ($tW$).  
   - _Suppression Strategy:_ Since the signal contains no jets (or only gluon radiation jets), these backgrounds are heavinly suppressed by applying a **b-jet veto**.

2. **Drell–Yan to Taus (Sample: `DY_to_Tau_Tau`):**  
   Produced when a $Z/\gamma^*$ decays into a pair of tau leptons, which subsequently decay into leptons mimicking the electron–muon + neutrinos final state.  
   - _Supression strategy:_ These events typically have lower $p_T$ leptons and an invariant mass closer to $Z$ peak mass window (50 < $m_{ll}$ < 80 GeV).

3. **Diboson/VZ (Sample: `Diboson`):**
   - **$WZ \to 3\ell + \nu$:** Mimics the signal if one of the three leptons is faked.
   - **$ZZ \to 4\ell$:** Mimics the signal if two of the four leptons are faked.  
   - _Suppression Strategy:_ Events with only two leptons are selected.

4. **Vector Boson + Gamma (Sample: `VG`):**  
   Includes $W\gamma$ and $Z\gamma$ production.
   - These mimic the signal if the photon ($\gamma$) converts into an electron–positron pair in the detector material and is misidentfied as a prompt electron.  
   - _Suppression Strategy:_ Strict electron track quality requirements reduce the rate of photon conversion misidentification.

5. **Fakes (Sample: `Fakes`):**  
   This category typically covers $W$ + jets and **QCD** multijet events.
   - A "fake" lepton occurs when a jet is misidentified as a lepton, or a real lepton is produced inside a jet and passes isolation criteria.
   - _Suppression Strategy:_ Tight identification and isolation cuts are applied to all leptons.

---

## 3. Analysis Strategy and Event Selection

### 3.1 Overview of the Analysis Workflow

The analysis is implemented using the Scikit-HEP framework, which replaces the traditional event-loop paradigm with columnar processing. The core logic is encapsulated in the processor.py module, which is distributed across a cluster using Dask. This approach allows us to process millions of events in parallel by treating particle properties (like $p_t$, $\eta$, $\phi$) as contiguous arrays rather than individual objects.

The execution flow for each data chunk follows a strict "Cut-and-Count" methodology:

- **Validation:** Quality filtering and weight initialization.
- **Object Selection:** Constructing valid physics objects (Leptons, Jets).
- **Pre-Selection:** Isolating the $e^\pm \mu^\mp$ candidate pair.
- **Corrections:** Applying Scale Factors (SF) to simulation.
- **Global Cuts:** Baseline kinematic requirements.
- **Categorization:** Sorting events into orthogonal Signal and Control regions.


### 3.2 Step 1: Data Ingestion and Validation

Before any physics selection occurs, the raw events are filtered to ensure data quality and correct normalization.

#### 3.2.1 Golden JSON Masking (Data Only)

For observational data, we must ensure we only analyze luminosity blocks where all CMS sub-detectors were functioning correctly.

- **Implementation:** The `json_validation.apply_json_mask` function filters events against the official CMS Golden JSON file (`Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt`).
- **Run Periods:** The analysis covers runs 2016G through 2016H.

#### 3.2.2 MC Cross-Section Weighting (Simulation Only)

Monte Carlo (MC) samples are generated with varying numbers of events that do not match the actual integrated luminosity of the data 
($L_{\text{int}} \approx 16.15\,\text{fb}^{-1}$). 
To compare MC with data, we assign a weight ($w_{\text{event}}$) to each simulated event:

$$
w_{\text{event}} 
= \text{genWeight} \times 
\frac{\sigma_{\text{process}} \times L_{\text{int}}}
{\sum w_{\text{gen}}}.
$$



- **$\sigma_{process}$:** The theoretical cross-section for the physics process (sourced from `hww_tools/cross_section.py` or `Datasets/README_MC_Samples_2016UL.md`).
- **$\Sigma w_{gen}$:** The sum of generator weights, used to normalize the sample size.
- **Implementation**: This calculation happens at the start of the event loop in `processor.py`.


### 3.3 Step 2: Lepton Definition and Pre-Selection

We will target the fully leptonic decay channel. We explicitly identify "*Tight*" leptons to suppress backgrounds from non-prompt sources (like QCD). These definitions are handled in `hww_tools/Physics_selection.py`.

#### 3.3.1 Object Definitions

- **Electrons**: We select electrons passing the `Electron_mvaFall17V2Iso_WP90` identification. "WP90" implies a working point with 90% signal efficiency, optimized for isolating prompt electrons from $W/Z$ decays.  
  - Cut: `Electron_mvaFall17V2Iso_WP90 == 1`

- **Muons**: We require Tight ID and strict Particle Flow Isolation.  
  - ID: `Muon_tightId == 1` (Standard CMS cut for $W/Z$ muons).  
  - Isolation: `Muon_pfRelIso04_all < 0.15`. This ensures the muon is isolated from other hadronic activity in a cone of $\Delta R < 0.4$.

#### 3.3.2 The eμ Pre-Selection

The `select_e_mu_events` function constructs the dilepton candidate:

- **Sorting**: Valid leptons are sorted by transverse momentum ($p_T$) in descending order.
- **Multiplicity**: Events must contain exactly two tight leptons.
- **Flavor**: One electron and one muon ($e\mu$).
- **Charge**: They must have opposite electric charge (Opposite-Sign, $q_e \times q_\mu < 0$).

- **Kinematics**:
  - Leading Lepton: $p_T > 25$ GeV.
  - Sub-leading Lepton: $p_T > 13$ GeV.

- **Acceptance**: $|\eta_e| < 2.5$ and $|\eta_\mu| < 2.4$.


### 3.4 Step 3: Event Weight Corrections (MC)

Simulations do not perfectly model the detector response. We apply Scale Factors (SF) to correct the MC weights to match Data efficiencies. These are managed in `hww_tools/Efficiency_data.py`.

- **Trigger SF:** Corrects for the efficiency of the HLT paths used to collect the data.
- **Lepton ID & Isolation SF:**
  - Corrections are pulled from [approved](https://github.com/latinos/LatinoAnalysis/tree/UL_production/NanoGardener/python/data/scale_factor/Full2016v9noHIPM) lookup tables (ROOT/Text files) based on the lepton's $p_T$ and $\eta$.
  - **Systematics:** We compute up and down variations for these weights to estimate uncertainties, which are propagated through to the final histograms.



### 3.5 Step 4: Kinematic Reconstruction

Before applying topological cuts, we compute the necessary kinematic variables in `hww_tools/calculations.py`.

- **Higgs Transverse Mass ($m_{TH}$)**: Since neutrinos escape detection, we cannot reconstruct the invariant mass. We use the transverse mass as the primary discriminator:

$$
m_{T}^H = \sqrt{2\, p_{T}^{\ell\ell}\, E_T^{miss} \left(1 - \cos \Delta \phi(\ell\ell, E_T^{miss})\right)}
$$

This variable peaks near the Higgs mass for the signal but has a broad continuum for the WW background.

- **Lepton-$E_T^{miss}$ Transverse Mass ($m_T(\ell_2, E_T^{miss})$)**: The transverse mass of the sub-leading lepton and the $E_T^{miss}$. This is useful for suppressing $W$+Jets background where the $E_T^{miss}$ comes from a single W decay.
- **Dijet Invariant Mass ($m_{jj}$)**: Calculated for events with ≥2 jets to identify Vector Boson Fusion (VBF) topology.



### 3.6 Step 5: Jet Cleaning and Categorization

Jets are critical for separating the production modes (ggH vs VBF) and rejecting the Top background.

#### 3.6.1 Cleaning and Counting

We select jets with $p_T > 30$ GeV and $|\eta| < 4.7$ that pass Tight Jet ID and Pileup ID. Crucially, we perform Lepton Cleaning, where any jet found within a cone of $\Delta R < 0.4$ of a selected signal lepton is considered a "footprint" of the lepton and is removed from the jet collection.

#### 3.6.2 Jet Bins

Events are classified into three exclusive categories based on the number of cleaned jets:

- **0-Jet**: Pure Gluon-Fusion (ggH) signal region.
- **1-Jet**: ggH with Initial State Radiation (ISR).
- **2-Jet**: Contaminated by Top background and VBF signal.


### 3.7 Step 6: Global Selection Cuts

A set of baseline "Global Cuts" is applied to all categories to remove obvious backgrounds and low-mass resonances. Implemented in `cuts.apply_global_cuts`:

- $E_T^{miss} > 20$ GeV: Ensures real missing energy is present, suppressing Drell-Yan and QCD.
- $p_T^{\ell\ell} > 30$ GeV: The Higgs is typically produced with moderate boost; this rejects softer backgrounds.
- $m_{\ell\ell} > 12$ GeV: Rejects low-mass resonances (like $J/\psi$, $\Upsilon$) and low-mass Drell-Yan.


### 3.8 Step 7: Region Definitions

Finally, events are split into orthogonal regions for Signal extraction (SR) and Background estimation (CR). These logic masks are defined in `hww_tools/cuts.py`.

#### 3.8.1 Signal Region (SR)

Optimized for the ggH signal, we require:

- **b-jet Veto**: No b-tagged jets ($p_T > 20$ GeV) to reject Top quarks.
- **Higgs $m_T > 60$ GeV**: Focuses on the Higgs mass peak area.
- **$m_T(\ell_2, E_T^{miss}) > 30$ GeV**: Suppresses W+Jets and non-prompt leptons.
- **2-Jet Veto**: In the 2-jet category only, we apply an $m_{jj}$ window cut (veto 65 < $m_{jj}$ < 105 GeV) to remove hadronic $W/Z$ decays.

#### 3.8.2 Control Region Top (CR-Top)

Used to normalize the $t\bar{t}$ background. Defined by inverting the b-veto.

- 0-Jet Bin: Looks for "soft" b-jets (20 < $p_T$ < 30 GeV) which are often missed in the standard jet collection.
- 1/2-Jet Bins: Requires at least one standard b-jet ($p_T > 30$ GeV).
- Cuts: Global Cuts + $m_{\ell\ell} > 50$ GeV + b-tag requirement.

#### 3.8.3 Control Region DY (CR-$\tau\tau$)

Used to normalize the Drell-Yan background. Defined by inverting the $m_T^H$ cut.

- **Cuts:** Global Cuts + b-jet Veto + $m_{T}^H < 60$ GeV.
- **Z-Mass Window:** We strictly select events inside the Z-peak window (40 < $m_{\ell\ell}$ < 80 GeV) to capture $Z \to \tau\tau$ events.

### 3.9 Step 8: Cutflow and Validation

To validate the analysis logic and monitor the efficiency of each selection step, we track the cumulative event yields across the entire workflow.

#### 3.9.1 Tracking Stages

We define specific "checkpoints" in the analysis chain where event counts are recorded. These are defined in `hww_tools/Config.py` and populated dynamically during the event loop in `processor.py`.

The monitored stages are:

- **Total**: Raw number of events in the input files.
- **After JSON**: Events remaining after applying the Golden JSON (Data only).
- **eμ Pre-selection**: Events with exactly one electron and one muon of opposite sign.
- **Global Cuts**: Events passing the baseline $E_T^{miss} > 20$ GeV and $m_{\ell\ell} > 12$ GeV logic.
- **Jet Categories**: Counts for 0-Jet, 1-Jet, and 2-Jet sub-groups.
- **Signal/Control Regions**: Final counts in the orthogonal SR, CR-Top, and CR-DY regions.

#### 3.9.2 Raw vs. Weighted Yields

We maintain two parallel cutflow tables:

- **Raw Cutflow**: Counts the absolute number of processed events. Useful for debugging code performance and statistical errors.
- **Weighted Cutflow**: Sums the weights ($w_{event}$) of surviving events. This represents the expected physical yields (normalized to $16.15 \text{ fb}^{-1}$) and is used for physics comparisons.

---
## 4. Technical Framework

### 4.1 Event-Loop vs Array-Based Processing 
Traditional High-Energy Physics (HEP) analysis has historically relied on an Event-Loop paradigm (typically using C++ ROOT macros). In this model, the processor iterates through the dataset one event at a time, reconstructing objects and filling histograms sequentially. While conceptually simple, this approach often suffers from poor performance in interpreted languages like Python due to loop overhead and lack of vectorization.
To address this, instead of processing events row-by-row, we treat data as contiguous arrays of properties (columns). For example, rather than looping over every muon in every event to check its transverse momentum ($p_T$), we perform a single operation on the entire $p_T$ array (e.g., `muon_pt > 25`). This approach shifts the computational burden to compiled, highly optimized libraries (like NumPy and C++ kernels), allowing us to exploit modern CPU vectorization and ensuring high-throughput data processing.

### 4.2 Core Toolset

<div align="center">
<img src="Images/scikit_logo.png" alt="Scikit-HEP Logo" width="350"/>
</div>

The analysis is built upon the modern [Scikit-HEP](https://scikit-hep.org/) scientific Python ecosystem. Each tool in the stack addresses a specific challenge of processing HEP data:

1. **`Uproot`:** 

<div align="center">
<img src="Images/uproot_logo.png" alt="Uproot Logo" width="200"/>
</div>

To interface with the vast legacy of data stored in ROOT format, we utilize [Uproot](https://pypi.org/project/uproot/). Unlike PyROOT, Uproot is purely Python-based and does not require the massive C++ ROOT software stack. In this analysis, Uproot handles the input/output layer, streaming NanoAOD data directly from remote XRootD servers into local memory buffers.
2. **`Awkward Array`:** 

<div align="center">
<img src="Images/awkward.svg" alt="Awkward Array Logo" width="200"/>
</div>

Particle physics data is inherently "*jagged*" or irregular—one event may contain zero muons, the next might have two, and a third might have one. Standard "*flat*" array libraries like [NumPy](https://numpy.org/) cannot handle this structure naturally. We solve this using [Awkward Array](https://pypi.org/project/awkward/), which allows us to manipulate these irregular, nested structures using NumPy-like idioms (slicing, masking, and broadcasting) without losing the event structure.
3. **`Vector`:** 

<div align="center">
<img src="Images/vector logo.svg" alt="Vector Logo" width="200"/>
</div>

Calculating physical quantities such as invariant masses ($m_{\ell\ell}$), angular separations ($\Delta R$), and Lorentz boosts is handled by the [Vector](https://vector.readthedocs.io/en/latest/) library. It integrates seamlessly with Awkward Array, allowing us to perform complex 4-vector arithmetic on millions of particles simultaneously with a syntax as simple as `lepton1 + lepton2`.
4. **`Hist`:** 

<div align="center">
<img src="Images/histlogo.png" alt="Hist Logo" width="200"/>
</div>

For the final accumulation of yields and distributions, we employ [Hist](https://hist.readthedocs.io/en/latest/). Based on the fast C++ `boost-histogram` library, Hist supports multi-dimensional, sparse, and categorical axes. This is essential for our analysis, which requires simultaneous categorization of events into multiple regions (Signal, Control) and systematic variations within a single object.
5. **`Mplhep`:** 

<div align="center">
<img src="Images/mplhep_logo.png" alt="Mplhep Logo" width="250"/>
</div>

[Mplhep](https://github.com/scikit-hep/mplhep) is a Matplotlib extension for high-energy physics. It provides tools for plotting data in the standard HEP style, including axis formatting, error bar conventions, and legend placement. In this analysis, Mplhep is used to create standardized plots of the signal and control regions.

### 4.3 Distributed Computing with Dask

<div align="center">
<img src="Images/dask_horizontal.svg" alt="Dask Logo" width="300"/>
</div>


To handle the massive scale of CMS data (terabytes of information), we leverage [Dask](https://docs.dask.org/en/stable/), a flexible parallel computing library. Dask allows us to scale the same Python analysis from a single laptop to a cluster of machines without rewriting the code. It achieves this by breaking the dataset into smaller *“chunks”* (partitions) and processing them in parallel.

In this analysis, Dask is used to distribute the event processing across multiple CPU cores, significantly reducing the runtime.

To quantify the performance gain, we compare the wall-clock time required to process the full dataset:

* **Sequential Processing:** Processing the full $16.15 \text{ fb}^{-1}$ dataset on a single core would be CPU-bound, taking several hours to complete.

* **Distributed Processing:** By distributing the workload across the Dask cluster, the total processing time is reduced to minutes.

This reduction in runtime is important for the iterative nature of the analysis, where selection cuts and strategies are refined repeatedly. Faster processing enables quicker feedback and more efficient development cycles.

---

## 5. Statistical Interpretation

### 5.1 CMS Combine Tool

<div align="center">
<img src="Images/combine_logo.png" alt="Combine Logo" width="300"/>
</div>

The final statistical analysis is performed using the [CMS Higgs Combine Tool](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/). It computes the **signal strength (μ)**, defined as the ratio of the observed signal yield to the Standard Model prediction, and evaluates the statistical significance of any excess. The tool uses a **profile likelihood fit**, where systematic uncertainties are treated as nuisance parameters constrained by the data.

### 5.2 Input Preparation
The script `Run_analysis/prepare_combine.py` converts the analysis output into the format required by Combine.

- **Harvesting:** Extracts the relevant histograms (e.g., `mt_higgs`) from the Signal and Control Regions.
- **Smoothing:** Empty or negative bins are set to a small positive value to ensure fit stability.
- **Output files:**
  1. `combine_input.root` – Contains nominal shapes and systematic variations.
  2. `hww_datacard.txt` – Defines the physics model and uncertainties.

### 5.3 Datacard and Fit Strategy
The datacard (`Outputs/hww_datacard.txt`) performs a **simultaneous fit** of:

1. **Signal Region (SR):** Main search region.
2. **Top Control Region (TopCR):** Used to constrain the dominant top-quark background.

Systematic uncertainties are included as:

- **lnN (log-normal):** Normalization uncertainties (e.g., luminosity).
- **Shape:** Kinematic uncertainties such as trigger and lepton ID efficiencies.
