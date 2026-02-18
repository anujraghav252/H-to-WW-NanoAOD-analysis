# Search for the Higgs Boson in the H→WW→eμνν Channel Using CMS Open Data

---

## 1. CMS Open Data

### 1.1 What is CMS Open Data?
### 1.2 The CMS Experiment at the LHC
### 1.3 Purpose and Philosophy of Open Data in High-Energy Physics
### 1.4 Available Data Formats: NanoAOD, MiniAOD, and AOD
### 1.5 The Open Data Portal and Data Preservation

---

## 2. The Higgs Boson

### 2.1 The Standard Model and the Brout-Englert-Higgs Mechanism
### 2.2 Discovery of the Higgs Boson (2012)
### 2.3 Higgs Boson Production Modes at the LHC
#### 2.3.1 Gluon-Gluon Fusion (ggH) — Dominant Mode
#### 2.3.2 Vector Boson Fusion (VBF)
#### 2.3.3 Associated Production (VH, ttH)
### 2.4 Higgs Boson Decay Channels
#### 2.4.1 Overview of Branching Ratios
#### 2.4.2 The H→WW* Decay Mode
### 2.5 The Fully Leptonic Final State: H→WW*→eμνν
#### 2.5.1 Why the eμ Channel? — Suppressing Drell-Yan
#### 2.5.2 Kinematic Properties of the Signal
#### 2.5.3 The Role of Transverse Mass (m_T^H) as the Discriminating Variable

---

## 3. Signal and Background Processes

### 3.1 Signal Definition: gg→H→WW*→eμνν
### 3.2 Irreducible Backgrounds
#### 3.2.1 Non-Resonant WW Production (qq̄→WW→eμνν)
#### 3.2.2 Gluon-Induced WW (gg→WW)
### 3.3 Reducible Backgrounds
#### 3.3.1 Top Quark Pair Production (tt̄→2ℓ2ν) and Single Top
#### 3.3.2 Drell-Yan to Tau Pairs (Z/γ*→ττ→eμ+4ν)
#### 3.3.3 Non-Prompt / Fake Leptons (W+Jets, Semi-Leptonic tt̄)
#### 3.3.4 Diboson Production (WZ, ZZ)
#### 3.3.5 V+γ Processes (Wγ, Zγ)
### 3.4 Summary of Background Mimicry Mechanisms
### 3.5 Process Grouping and Sample Mapping Used in This Analysis

---

## 4. Analysis Strategy and Event Selection

### 4.1 Overview of the Analysis Chain
### 4.2 Data and Monte Carlo Samples
#### 4.2.1 Data: 2016 Legacy Re-Reco (Run2016G–H)
#### 4.2.2 Monte Carlo Simulation Samples
#### 4.2.3 Integrated Luminosity (16.1 fb⁻¹)
### 4.3 Golden JSON Filtering for Data Quality
### 4.4 Object Selection
#### 4.4.1 Electron Selection (MVA Fall17 V2 Iso WP90)
#### 4.4.2 Muon Selection (Tight ID + PF Relative Isolation < 0.15)
#### 4.4.3 Jet Selection (Jet ID, Pileup ID, Lepton Cleaning via ΔR > 0.4)
#### 4.4.4 Missing Transverse Energy (PuppiMET)
### 4.5 Event Pre-Selection
#### 4.5.1 Exactly One Electron and One Muon (eμ Channel)
#### 4.5.2 Opposite Charge Requirement
#### 4.5.3 Leading Lepton pT > 25 GeV, Subleading pT > 13 GeV
#### 4.5.4 Lepton η Acceptance (|η_e| < 2.5, |η_μ| < 2.4)
### 4.6 Kinematic Variable Computation
#### 4.6.1 Dilepton Invariant Mass (m_ℓℓ)
#### 4.6.2 Dilepton Transverse Momentum (pT_ℓℓ)
#### 4.6.3 Azimuthal Opening Angle (Δφ_ℓℓ)
#### 4.6.4 Higgs Transverse Mass (m_T^H)
#### 4.6.5 Subleading Lepton Transverse Mass (m_T(ℓ₂, MET))
#### 4.6.6 Dijet Invariant Mass (m_jj)
### 4.7 Global Cuts
#### 4.7.1 MET > 20 GeV
#### 4.7.2 pT_ℓℓ > 30 GeV
#### 4.7.3 m_ℓℓ > 12 GeV
### 4.8 Jet Categorization
#### 4.8.1 0-Jet Category
#### 4.8.2 1-Jet Category
#### 4.8.3 ≥2-Jet Category
### 4.9 Signal Region Definitions
#### 4.9.1 Common SR Cuts (m_T^H > 60 GeV, m_T(ℓ₂, MET) > 30 GeV, b-jet Veto)
#### 4.9.2 SR 0-Jet, SR 1-Jet, SR 2-Jet
#### 4.9.3 m_jj Window Veto in 2-Jet Category
### 4.10 Control Region Definitions
#### 4.10.1 Top Control Regions (m_ℓℓ > 50 GeV, b-tag Requirements)
##### 4.10.1.1 CR-Top 0-Jet (Soft b-jets: 20 < pT < 30 GeV)
##### 4.10.1.2 CR-Top 1-Jet and 2-Jet (Hard b-jets: pT > 30 GeV)
#### 4.10.2 Drell-Yan ττ Control Regions (m_T^H < 60, 40 < m_ℓℓ < 80 GeV, b-jet Veto)
##### 4.10.2.1 CR-ττ 0-Jet, 1-Jet, 2-Jet
### 4.11 Cutflow and Event Yields

---

## 5. Technical Framework and Tools

### 5.1 The Coffea-Casa Analysis Facility for CMS Open Data
### 5.2 Distributed Computing with Dask
#### 5.2.1 The Dask Scheduler-Worker Architecture
#### 5.2.2 Deploying the Analysis Package to Workers
#### 5.2.3 Performance Comparison: Sequential vs. Dask-Distributed Processing
### 5.3 Columnar Analysis with Awkward Array
#### 5.3.1 Jagged/Variable-Length Data Structures in HEP
#### 5.3.2 Vectorized Operations on Event Data
### 5.4 ROOT File I/O with Uproot
#### 5.4.1 Reading NanoAOD Files
#### 5.4.2 Batch Iteration over Large Files
#### 5.4.3 Writing Output ROOT Files
### 5.5 Lorentz Vector Computations with the Vector Library
### 5.6 Histogramming with the hist (boost-histogram) Library
#### 5.6.1 Weighted Histogram Storage
#### 5.6.2 Histogram Axes and Binning Definitions
### 5.7 Numerical Computing with NumPy
### 5.8 Visualization with matplotlib and mplhep
#### 5.8.1 CMS-Style Plotting
#### 5.8.2 Stacked Histogram Plots with Data/MC Ratio Panels
#### 5.8.3 Shape Comparison (Superimposed) Plots
### 5.9 Summary Table of Tools and References

---

## 6. Accessing CMS Open Data via XRootD

### 6.1 What is XRootD?
### 6.2 The EOSPUBLIC Storage Infrastructure at CERN
### 6.3 Constructing XRootD URLs for CMS Open Data Files
### 6.4 Organizing File Lists by Sample and Physics Process
### 6.5 Sample-to-Label Mapping Strategy
### 6.6 Handling Network Failures: Retry Logic and Timeouts

---

## 7. Monte Carlo Normalization and Cross-Section Weighting

### 7.1 Why MC Events Need Reweighting
### 7.2 The Normalization Formula: w = (σ × L) / Σw_gen
#### 7.2.1 Cross-Sections (σ)
#### 7.2.2 Integrated Luminosity (L = 16,150 pb⁻¹)
#### 7.2.3 Sum of Generator Weights (Σw_gen)
### 7.3 Generator-Level Weights (genWeight)
### 7.4 Cross-Section Sources: The LatinoAnalysis GitHub Repository
### 7.5 Cross-Section Values Used in This Analysis
### 7.6 Handling Negative Generator Weights

---

## 8. Data/MC Correction Factors (Scale Factors)

### 8.1 Why Scale Factors Are Needed
### 8.2 HLT Trigger Efficiency Scale Factor
#### 8.2.1 Flat SF Approach (SF = 0.9129 ± 0.0008)
#### 8.2.2 Propagation as a Systematic Uncertainty
### 8.3 Electron Identification Scale Factor
#### 8.3.1 MVA Fall17 V2 Iso WP90 Efficiency
#### 8.3.2 2D Lookup Table: |η| × pT Binning
#### 8.3.3 Up/Down Variations for Systematics
### 8.4 Muon Scale Factors
#### 8.4.1 Tight ID Efficiency Scale Factor
#### 8.4.2 PF Relative Isolation (Iso < 0.15) Scale Factor
#### 8.4.3 Combined Muon SF: Product of Tight ID × Isolation
#### 8.4.4 2D Lookup Table: |η| × pT Binning
#### 8.4.5 Correlated Up/Down Variations
### 8.5 Weight Dictionary and Systematic Variation Strategy
#### 8.5.1 Nominal Weight Construction
#### 8.5.2 Seven Variation Categories: nominal, trigger_up/down, ele_id_up/down, mu_id_up/down

---

## 9. Statistical Inference with the Combine Tool

### 9.1 Overview of the CMS Combine Framework
### 9.2 Preparing Inputs for Combine
#### 9.2.1 Harvesting Histograms from the Analysis Output
#### 9.2.2 Protecting Against Empty/Negative Bins
#### 9.2.3 Naming Convention: $PROCESS_$CHANNEL_$SYSTEMATIC
### 9.3 The Datacard Structure
#### 9.3.1 Channel and Process Definitions
#### 9.3.2 Observed and Expected Rates
#### 9.3.3 Nuisance Parameters
##### 9.3.3.1 Luminosity Uncertainty (lnN: 2.5%)
##### 9.3.3.2 Shape Systematics (Trigger, Electron ID, Muon ID)
#### 9.3.4 Automatic MC Statistical Uncertainties (autoMCStats)
### 9.4 Simultaneous Fit: Signal Region + Top Control Region

---

## 10. Limitations of CMS Open Data for Physics Analysis

### 10.1 Limited Run Periods and Luminosity Coverage
### 10.2 Absence of Official Correction Files (e.g., JSON POG)
### 10.3 Missing or Incomplete Scale Factor Derivation Tools
### 10.4 Lack of Official Trigger Efficiency Measurements for Open Data
### 10.5 No Access to Data-Driven Background Estimation Frameworks
### 10.6 Limited Documentation for Advanced Analysis Techniques
### 10.7 Software Environment Compatibility Challenges
### 10.8 Reduced Systematic Uncertainty Coverage Compared to Official Analyses
### 10.9 Validation Difficulties Without Internal Collaboration Benchmarks

---

## 11. Future Improvements for CMS Open Data

### 11.1 Publishing Complete Scale Factor and Correction Packages
### 11.2 Providing Pre-Computed Efficiency Maps and Trigger Turn-On Curves
### 11.3 Expanding the Available Luminosity and Run Periods
### 11.4 Releasing Reference Analysis Workflows as Benchmarks
### 11.5 Improving Documentation with Step-by-Step Analysis Tutorials
### 11.6 Enabling Data-Driven Techniques (e.g., Fake Factor Methods, Template Fits)
### 11.7 Better Integration with Modern Analysis Tools (Coffea, Dask, ServiceX)
### 11.8 Streamlining Access via Cloud-Native Analysis Facilities
### 11.9 Community-Driven Validation and Reproducibility Frameworks
### 11.10 Broadening Open Data for Education and Early-Career Researchers

---

## Appendices

### A. Complete List of Datasets and XRootD Endpoints
### B. Full Cutflow Tables (Raw and Weighted)
### C. Cross-Section and Generator Weight Summary Table
### D. Scale Factor Lookup Tables
#### D.1 Electron MVA ID SF Table
#### D.2 Muon Tight ID SF Table
#### D.3 Muon PF Isolation SF Table
### E. Datacard Example
### F. Software Versions and Environment Specifications

---

## References