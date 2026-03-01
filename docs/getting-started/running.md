# Running the Analysis

## Main Analysis Notebook

Open the main analysis notebook:

```bash
jupyter lab notebooks/HWW_analysis.ipynb
```

This notebook contains the full end-to-end analysis: sample loading,
object & event selection, kinematic distributions, Data/MC scale factors,
and signal-background comparisons.

## Supporting Notebooks

| Notebook | Description |
|----------|-------------|
| `xsec_weights.ipynb` | Cross-section weight computation |
| `sum_genW.ipynb` | Sum of generator weights calculation |
| `Trigger_efficiency.ipynb` | Trigger efficiency measurement |
| `Lepton_ID_efficiency.ipynb` | Lepton ID efficiency scale factors |
| `Muon_EFF.ipynb` | Muon efficiency studies |

## Statistical Fit (CMS Combine)

The `Run_analysis/` directory contains the full statistical workflow:

```bash
python Run_analysis/prepare_combine.py
```

This prepares the histograms and datacards for the CMS Combine tool.