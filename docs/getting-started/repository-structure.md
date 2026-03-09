# Repository Architecture

The repository is organized to keep analysis logic, data access, documentation, and outputs cleanly separated.

---

## Top-Level Layout

```
H-to-WW-NanoAOD-analysis/
│
├── Run_analysis/           # Main analysis code and notebook
│   ├── Run_analysis.ipynb  # Primary analysis notebook
│   ├── hww_tools/          # Analysis library (all Python modules)
│   └── prepare_combine.py  # Post-processing for CMS Combine
│
├── notebooks/              # Supplementary notebooks
│   ├── HWW_analysis.ipynb        # Exploratory / prototype notebook
│   ├── xsec_weights.ipynb        # Cross-section weight computation
│   └── Data-MC_corrections/      # Scale-factor derivation notebooks
│       ├── Lepton_ID_efficiency.ipynb
│       ├── Muon_EFF.ipynb
│       └── Trigger_efficiency.ipynb
│
├── Datasets/               # Sample file lists and cross-section info
│   ├── Higgs.txt           # Signal XRootD paths
│   ├── Top.txt             # tt̄ / Single Top paths
│   ├── WW.txt / ggWW.txt   # Diboson WW paths
│   ├── DYtoLL.txt          # Drell-Yan paths
│   ├── Fakes.txt           # W+jets / semi-leptonic tt̄ paths
│   ├── VZ.txt / VG.txt     # Remaining diboson / V+γ paths
│   └── README_MC_Samples_2016UL.md
│
├── Auxillary_files/        # Scale-factor lookup tables
│   └── Efficiencies/
│       ├── Eff_note.txt            # Trigger efficiency record
│       ├── Muon_tight_Eff.txt      # Muon tight-ID scale factors
│       ├── Muon_ISO_Eff.txt        # Muon isolation scale factors
│       └── egammaEffi_TightHWW_2016.txt  # Electron ID scale factors
│
├── Outputs/                # Analysis outputs
│   ├── combine_input.root  # ROOT histogram file for CMS Combine
│   └── hww_datacard.txt    # CMS Combine datacard
│
├── assets/                 # Images used in documentation
├── docs/                   # MkDocs documentation source
├── environment.yml         # Conda environment specification
├── requirements.txt        # pip dependency list
└── mkdocs.yml              # Documentation site configuration
```

---

## The `hww_tools` Analysis Library

The core analysis logic lives in `Run_analysis/hww_tools/`, structured as a proper Python package:

| Module                 | Responsibility                                                                      |
| ---------------------- | ----------------------------------------------------------------------------------- |
| `Config.py`            | Central configuration: histogram definitions, cutflow stage names, variable binning |
| `Physics_selection.py` | Lepton object definitions and the $e\mu$ pre-selection                              |
| `cuts.py`              | Global cuts and region masks (SR, CR-Top, CR-DY)                                    |
| `calculations.py`      | Kinematic variable computation ($m_T^H$, $m_{\ell\ell}$, $\Delta\phi$, etc.)        |
| `Efficiency_data.py`   | Data/MC scale-factor loading and application                                        |
| `json_validation.py`   | Golden JSON masking for observed data                                               |
| `cross_section.py`     | Cross-section lookup dictionary                                                     |
| `dask_utils.py`        | Dask task submission and cluster management helpers                                 |
| `cutflow_utils.py`     | Cutflow table accumulation and display                                              |
| `plotting.py`          | Data/MC stack plot production (mplhep-based)                                        |
| `Plots_config.py`      | Plot styling: axis labels, colors, y-axis ranges                                    |
| `helper.py`            | Miscellaneous utilities used throughout the analysis                                |
| `run_analysis.py`      | Top-level entry point for running the full processorr                               |

---

## Data Flow

```
XRootD (CERN EOS)
        │
        ▼ Uproot (chunked reads)
Awkward Arrays (jagged lepton/jet collections)
        │
        ▼ hww_tools (selection, corrections, calculations)
Hist histograms (SR, CR-Top, CR-DY × systematics)
        │
        ▼ prepare_combine.py
combine_input.root + hww_datacard.txt
        │
        ▼ CMS Combine
Signal strength μ, 95% CL limits
```

---

## Key Files at a Glance

| File                                   | Purpose                                                     |
| -------------------------------------- | ----------------------------------------------------------- |
| `Run_analysis/Run_analysis.ipynb`      | **Start here for the full analysis**                        |
| `Run_analysis/hww_tools/Config.py`     | Edit to change histogram binning or add variables           |
| `Run_analysis/hww_tools/cuts.py`       | Edit to change selection cuts or region definitions         |
| `Datasets/README_MC_Samples_2016UL.md` | Full sample list with cross sections and Open Data links    |
| `Auxillary_files/Efficiencies/`        | Scale-factor lookup tables consumed by `Efficiency_data.py` |
| `Outputs/hww_datacard.txt`             | CMS Combine datacard used for statistical inference         |
