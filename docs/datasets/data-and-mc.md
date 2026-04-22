# **Datasets**

This page describes the data and Monte Carlo (MC) simulation samples used in the analysis,
and explains how MC events are normalised to the observed luminosity.

---

## **1. Observed Data**

The analysis uses CMS proton–proton collision data collected during **Run 2016G and 2016H**,
corresponding to an [integrated luminosity](https://opendata.cern.ch/record/1059) of:

$$\mathcal{L}_{\text{int}} = 16.39\,\text{fb}^{-1}$$

### **1.1 Golden JSON Masking**

Not all luminosity blocks recorded by CMS are suitable for physics analysis, some periods
have sub-detectors switched off or operating in degraded mode. Only events within certified
luminosity blocks are used, enforced by filtering against the official [CMS Golden JSON file](https://opendata.cern.ch/record/14220):

```text
Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt
```

### **1.2 Data**
| Period | Dataset | CERN Open Data | $\mathcal{L}\ (\text{fb}^{-1})$ |
| ------ | ------- | -------------- | --------------------------- |
| 2016G  | /MuonEG/Run2016G-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD | [Link](https://opendata.cern.ch/record/30528) | 7.65 |
| 2016H  | /MuonEG/Run2016H-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD | [Link](https://opendata.cern.ch/record/30561) | 8.74 |

---

## **2. Monte Carlo Simulation**

All simulation samples correspond to the **CMS RunIISummer20UL16 (2016 Ultra-Legacy) campaign**
at $\sqrt{s} = 13\,\text{TeV}$, using NanoAOD v9 format. Samples are sourced from the
[CERN Open Data Portal](https://opendata.cern.ch) and accessed via XRootD:

```text
root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/...
```

### **2.1 Signal**

| Dataset                                                                 | CERN Open Data                                | $\sigma$ (pb) |
| ----------------------------------------------------------------------- | --------------------------------------------- | ------------- |
| GluGluHToWWTo2L2N_M-125_TuneCP5_minloHJJ_13TeV-powheg-jhugen727-pythia8 | [Link](https://opendata.cern.ch/record/37464) | 1.0315        |

### **2.2 Backgrounds**

#### **Drell-Yan**

| Dataset                                           | CERN Open Data                                | $\sigma $ (pb) |
| ------------------------------------------------- | --------------------------------------------- | -------------- |
| DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8 | [Link](https://opendata.cern.ch/record/35671) | 6189.39        |

#### **Top Quark**

| Dataset                                                                      | CERN Open Data                                | $\sigma$ (pb) |
| ---------------------------------------------------------------------------- | --------------------------------------------- | ------------- |
| TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8                                       | [Link](https://opendata.cern.ch/record/67801) | 87.310        |
| ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8     | [Link](https://opendata.cern.ch/record/64759) | 44.33         |
| ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8 | [Link](https://opendata.cern.ch/record/64659) | 26.38         |
| ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8                | [Link](https://opendata.cern.ch/record/64825) | 35.60         |
| ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8                    | [Link](https://opendata.cern.ch/record/64881) | 35.60         |
| ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8                  | [Link](https://opendata.cern.ch/record/64635) | 3.360         |

#### **Fakes ($W$+jets, semi-leptonic $t\bar{t}$)**

| Dataset                                       | CERN Open Data                                | $\sigma$ (pb) |
| --------------------------------------------- | --------------------------------------------- | ------------- |
| TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8 | [Link](https://opendata.cern.ch/record/67993) | 364.35        |
| WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8  | [Link](https://opendata.cern.ch/record/69747) | 61526.7       |

#### **Diboson (WZ, ZZ)**

| Dataset                                               | CERN Open Data                                | $\sigma$ (pb) |
| ----------------------------------------------------- | --------------------------------------------- | ------------- |
| WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8 | [Link](https://opendata.cern.ch/record/72742) | 5.5950        |
| WZTo3LNu_mllmin4p0_TuneCP5_13TeV-powheg-pythia8       | [Link](https://opendata.cern.ch/record/72750) | 4.42965       |
| ZZ_TuneCP5_13TeV-pythia8                              | [Link](https://opendata.cern.ch/record/75593) | 16.52300      |

#### **WW**

| Dataset                                | CERN Open Data                                | $\sigma$ (pb) |
| -------------------------------------- | --------------------------------------------- | ------------- |
| WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8 | [Link](https://opendata.cern.ch/record/72676) | 12.178        |

#### **ggWW**

| Dataset                                        | CERN Open Data                                | $\sigma$ (pb) |
| ---------------------------------------------- | --------------------------------------------- | ------------- |
| GluGluToWWToENEN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40044) | 0.06387       |
| GluGluToWWToENMN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40046) | 0.06387       |
| GluGluToWWToENTN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40048) | 0.06387       |
| GluGluToWWToMNEN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40050) | 0.06387       |
| GluGluToWWToMNMN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40052) | 0.06387       |
| GluGluToWWToMNTN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40054) | 0.06387       |
| GluGluToWWToTNEN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40056) | 0.06387       |
| GluGluToWWToTNMN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40058) | 0.06387       |
| GluGluToWWToTNTN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40060) | 0.06387       |

#### **V+$\gamma$**

| Dataset                                           | CERN Open Data                                | $\sigma$ (pb) |
| ------------------------------------------------- | --------------------------------------------- | ------------- |
| ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8 | [Link](https://opendata.cern.ch/record/73904) | 58.83         |
| WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8        | [Link](https://opendata.cern.ch/record/69577) | 405.271       |


---

## **3. MC Normalisation**

MC samples are generated with arbitrary statistics that do not automatically match the data
luminosity. Each simulated event is assigned a weight to correct for this:

$$\text{Scale Factor} = \frac{\sigma \times \mathcal{L}_{\text{int}} \times \text{genWeight}}{\sum \text{genWeight}}$$

| Symbol | Meaning |
|---|---|
| $\text{genWeight}$ | Per-event generator weight (positive or negative) |
| $\sigma$ | Process cross section in pb (see tables above) |
| $\mathcal{L}_{\text{int}}$ | Integrated luminosity: $16.39\,\text{fb}^{-1}$ |
| ${\sum \text{genWeight}}$ | Sum of all generator weights in the sample |

### **3.1 Sum of Generator Weights**

The denominator ${\sum \text{genWeight}}$ must be computed _before_ any selection is applied,
using all events in the original dataset. Since MC events can carry negative generator weights
(due to NLO subtractions), the sum is **not** simply equal to the total number of events.

!!! warning "Sum of weights vs. number of events"
    Always use the sum of `genWeight` (not raw event counts) in the normalisation denominator.
    Failing to do this with NLO samples will produce incorrect overall normalisation.

The computation is handled in the `xsec_weights.ipynb` notebook, which reads the sample file
lists and outputs a lookup dictionary of ${\sum \text{genWeight}}$ per sample.

<!-- ### **3.2 Cross-Section References**

| Code | Reference |
|---|---|
| E | [CMS Summary Table 1G 25ns](https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns) |
| I | [GenXSecAnalyzer](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HowToGenXSecAnalyzer) |
| Y | [CERN Yellow Report (BSM @ 13 TeV)](https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBSMAt13TeV) |

--- -->

## **4. File Lists**

Sample ROOT file lists are stored under `Datasets/`:

**Datasets/**

- **Higgs.txt** — Signal
- **WW.txt** — Continuum WW
- **ggWW.txt** — Loop-induced WW
- **DYtoLL.txt** — Drell-Yan
- **Top.txt** — $t\bar{t}$ + Single Top
- **Fakes.txt** — W+jets, semi-leptonic $t\bar{t}$
- **VZ.txt** — WZ, ZZ
- **VG.txt** — $W+\gamma$, $Z+\gamma$

Each file contains XRootD paths in the format:

```text
root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/...
```