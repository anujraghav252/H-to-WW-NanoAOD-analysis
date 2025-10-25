# Monte Carlo Samples and Cross Sections for 2016 UL Higgs to WW Analysis

Based on [LatinoAnalysis Summer20UL16 configuration](https://github.com/latinos/LatinoAnalysis/blob/UL_production/NanoGardener/python/framework/samples/Summer20UL16_106x_noHIPM_nAODv9.py#L35-L43)

## Signal

| Sample | Dataset | CERN Open Data | Cross Section (pb) | K-factor | Reference |
|--------|---------|----------------|-------------------|----------|-----------|
| **Higgs** | GluGluHToWWTo2L2N_M-125_TuneCP5_minloHJJ_13TeV-powheg-jhugen727-pythia8 | [Link](https://opendata.cern.ch/record/37464) | 1.0315 | 1.000 | Y |

## Backgrounds

### 1. Drell-Yan

| Sample | Dataset | CERN Open Data | Cross Section (pb) | K-factor | Reference |
|--------|---------|----------------|-------------------|----------|-----------|
| DYtoLL | DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8 | [Link](https://opendata.cern.ch/record/35671) | 6189.39 | 1.000 | X |

### 2. Top

| Sample | Dataset | CERN Open Data | Cross Section (pb) | K-factor | Reference |
|--------|---------|----------------|-------------------|----------|-----------|
| TTTo2L2Nu | TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8 | [Link](https://opendata.cern.ch/record/67801) | 87.310 | 1.000 | E |
| ST_t-channel_top | ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8 | [Link](https://opendata.cern.ch/record/64759) | 44.33 | 1.000 | E |
| ST_t-channel_antitop | ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8 | [Link](https://opendata.cern.ch/record/64659) | 26.38 | 1.000 | E |
| ST_tW_antitop | ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8 | [Link](https://opendata.cern.ch/record/64825) | 35.60 | 1.000 | E |
| ST_tW_top | ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8 | [Link](https://opendata.cern.ch/record/64881) | 35.60 | 1.000 | E |
| ST_s-channel | ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8 | [Link](https://opendata.cern.ch/record/64635) | 3.360 | 1.000 | E |

### 3. Fakes

| Sample | Dataset | CERN Open Data | Cross Section (pb) | K-factor | Reference |
|--------|---------|----------------|-------------------|----------|-----------|
| TTToSemiLeptonic | TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8 | [Link](https://opendata.cern.ch/record/67993) | 364.35 | 1.000 | E |
| WJetsToLNu | WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8 | [Link](https://opendata.cern.ch/record/69747) | 61526.7 | 1.000 | E |

### 4. Diboson (VZ)

| Sample | Dataset | CERN Open Data | Cross Section (pb) | K-factor | Reference |
|--------|---------|----------------|-------------------|----------|-----------|
| WZTo2Q2L | WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8 | [Link](https://opendata.cern.ch/record/72742) | 5.5950 | 1.000 | E |
| WZTo3LNu | WZTo3LNu_mllmin4p0_TuneCP5_13TeV-powheg-pythia8 | [Link](https://opendata.cern.ch/record/72750) | 4.42965 | 1.000 | E |
| ZZ | ZZ_TuneCP5_13TeV-pythia8 | [Link](https://opendata.cern.ch/record/75593) | 16.52300 | 1.000 | E |

### 5. ggWW

| Sample | Dataset | CERN Open Data | Cross Section (pb) | K-factor | Reference |
|--------|---------|----------------|-------------------|----------|-----------|
| GluGluToWWToENEN | GluGluToWWToENEN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40044) | 0.06387 | 1.000 | I |
| GluGluToWWToENMN | GluGluToWWToENMN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40046) | 0.06387 | 1.000 | I |
| GluGluToWWToENTN | GluGluToWWToENTN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40048) | 0.06387 | 1.000 | I |
| GluGluToWWToMNEN | GluGluToWWToMNEN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40050) | 0.06387 | 1.000 | I |
| GluGluToWWToMNMN | GluGluToWWToMNMN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40052) | 0.06387 | 1.000 | I |
| GluGluToWWToMNTN | GluGluToWWToMNTN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40054) | 0.06387 | 1.000 | I |
| GluGluToWWToTNEN | GluGluToWWToTNEN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40056) | 0.06387 | 1.000 | I |
| GluGluToWWToTNMN | GluGluToWWToTNMN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40058) | 0.06387 | 1.000 | I |
| GluGluToWWToTNTN | GluGluToWWToTNTN_TuneCP5_13TeV_MCFM701_pythia8 | [Link](https://opendata.cern.ch/record/40060) | 0.06387 | 1.000 | I |

### 6. WW

| Sample | Dataset | CERN Open Data | Cross Section (pb) | K-factor | Reference |
|--------|---------|----------------|-------------------|----------|-----------|
| WWTo2L2Nu | WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8 | [Link](https://opendata.cern.ch/record/72676) | 12.178 | 1.000 | E |

### 7. VG (V+gamma)

| Sample | Dataset | CERN Open Data | Cross Section (pb) | K-factor | Reference |
|--------|---------|----------------|-------------------|----------|-----------|
| ZGToLLG | ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8 | [Link](https://opendata.cern.ch/record/73904) | 58.83 | 1.000 | Rafael |
| WGToLNuG | WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8 | [Link](https://opendata.cern.ch/record/69577) | 405.271 | 1.000 | E |

## Notes

- All samples are in NANOAODSIM format for 2016 collision data (RunIISummer20UL16)
- Cross sections are given in picobarns (pb)
- References: E = Standard, Y = Higgs working group, I = ggWW theory, X = DY theory, Rafael = VG theory
