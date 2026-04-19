# Datasets

This page describes the data and Monte Carlo (MC) simulation samples used in the analysis,
and explains how MC events are normalised to the observed luminosity.

---

## 1. Observed Data

The analysis uses CMS proton–proton collision data collected during **Run 2016G and 2016H**,
corresponding to an integrated luminosity of:

$$\mathcal{L}_{\text{int}} = 16.15\,\text{fb}^{-1}$$

### 1.1 Golden JSON Masking

Not all luminosity blocks recorded by CMS are suitable for physics analysis — some periods
have sub-detectors switched off or operating in degraded mode. Only events within certified
luminosity blocks are used, enforced by filtering against the official CMS Golden JSON file:

```text
Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt
```

which lists the run numbers and luminosity block ranges that pass data quality requirements.
The implementation is handled by `hww_tools/json_validation.py`.

---

## 2. Monte Carlo Simulation

All simulation samples correspond to the **CMS RunIISummer20UL16 (2016 Ultra-Legacy) campaign**
at $\sqrt{s} = 13\,\text{TeV}$, using NanoAOD v9 format. Samples are sourced from the
[CERN Open Data Portal](https://opendata.cern.ch) and accessed via XRootD:

```text
root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/...
```

### 2.1 Signal
| Sample Tag | $\sigma$ (pb) | Record |
|---|---|---|
| **Higgs** | 1.0315 | [↗](https://opendata.cern.ch/record/37464) |

### 2.2 Backgrounds

#### Drell-Yan
| Sample Tag | $\sigma$ (pb) | Record |
|---|---|---|
| DYtoLL | 6189.39 | [↗](https://opendata.cern.ch/record/35671) |

#### Top Quark
| Sample Tag | $\sigma$ (pb) | Record |
|---|---|---|
| TTTo2L2Nu | 87.310 | [↗](https://opendata.cern.ch/record/67801) |
| ST_t-channel_top | 44.33 | [↗](https://opendata.cern.ch/record/64759) |
| ST_t-channel_antitop | 26.38 | [↗](https://opendata.cern.ch/record/64659) |
| ST_tW_antitop | 35.60 | [↗](https://opendata.cern.ch/record/64825) |
| ST_tW_top | 35.60 | [↗](https://opendata.cern.ch/record/64881) |
| ST_s-channel | 3.360 | [↗](https://opendata.cern.ch/record/64635) |

#### Fakes ($W$+jets, semi-leptonic $t\bar{t}$)
| Sample Tag | $\sigma$ (pb) | Record |
|---|---|---|
| TTToSemiLeptonic | 364.35 | [↗](https://opendata.cern.ch/record/67993) |
| WJetsToLNu | 61526.7 | [↗](https://opendata.cern.ch/record/69747) |

#### Diboson (WZ, ZZ)
| Sample Tag | $\sigma$ (pb) | Record |
|---|---|---|
| WZTo2Q2L | 5.595 | [↗](https://opendata.cern.ch/record/72742) |
| WZTo3LNu | 4.430 | [↗](https://opendata.cern.ch/record/72750) |
| ZZ | 16.523 | [↗](https://opendata.cern.ch/record/75593) |

#### Continuum WW ($q\bar{q} \to WW$)
| Sample Tag | $\sigma$ (pb) | Record |
|---|---|---|
| WWTo2L2Nu | 12.178 | [↗](https://opendata.cern.ch/record/72676) |

#### ggWW ($gg \to WW$, loop-induced)
Nine exclusive di-flavour final states (EN, MN, TN combinations), each with
$\sigma = 0.064\,\text{pb}$. Records:
[40044](https://opendata.cern.ch/record/40044) –
[40060](https://opendata.cern.ch/record/40060).

#### V+$\gamma$
| Sample Tag | $\sigma$ (pb) | Record |
|---|---|---|
| ZGToLLG | 58.83 | [↗](https://opendata.cern.ch/record/73904) |
| WGToLNuG | 405.271 | [↗](https://opendata.cern.ch/record/69577) |

---

## 3. MC Normalisation

MC samples are generated with arbitrary statistics that do not automatically match the data
luminosity. Each simulated event is assigned a weight to correct for this:

$$\text{Scale Factor} = \frac{\sigma \times \mathcal{L} \times \text{genWeight}}{\sum \text{genWeight}}$$

| Symbol | Meaning |
|---|---|
| $\text{genWeight}$ | Per-event generator weight (positive or negative) |
| $\sigma$ | Process cross section in pb (see tables above) |
| $\mathcal{L}$ | Integrated luminosity: $16.15\,\text{fb}^{-1}$ |
| ${\sum \text{genWeight}}$ | Sum of all generator weights in the sample |

### 3.1 Sum of Generator Weights

The denominator ${\sum \text{genWeight}}$ must be computed _before_ any selection is applied,
using all events in the original dataset. Since MC events can carry negative generator weights
(due to NLO subtractions), the sum is **not** simply equal to the total number of events.

!!! warning "Sum of weights vs. number of events"
    Always use the sum of `genWeight` (not raw event counts) in the normalisation denominator.
    Failing to do this with NLO samples will produce incorrect overall normalisation.

The computation is handled in the `xsec_weights.ipynb` notebook, which reads the sample file
lists and outputs a lookup dictionary of ${\sum \text{genWeight}}$ per sample.

### 3.2 Cross-Section References

| Code | Reference |
|---|---|
| E | [CMS Summary Table 1G 25ns](https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns) |
| I | [GenXSecAnalyzer](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HowToGenXSecAnalyzer) |
| Y | [CERN Yellow Report (BSM @ 13 TeV)](https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBSMAt13TeV) |

---

## 4. File Lists

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