# Statistical Inference

After the analysis histograms are produced, the final step is extracting the **signal strength** and computing upper limits using the **CMS Combine** statistical tool.

---

## 1. Overview

The statistical analysis is performed with the [CMS HiggsAnalysis-CombinedLimit (Combine)](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/) tool. It implements a **profile likelihood ratio** test statistic, where systematic uncertainties are treated as constrained nuisance parameters (profiled over during the fit).

The quantity of interest is the **signal strength modifier** $\mu$, defined as:

$$\mu = \frac{\sigma_{\text{observed}}}{\sigma_{\text{SM}}}$$

- $\mu = 0$ → background-only hypothesis (no Higgs signal).
- $\mu = 1$ → Standard Model prediction (Higgs at exactly the SM rate).
- $\mu > 1$ → signal excess above the SM.

---

## 2. Preparing Combine Inputs

The script `Run_analysis/prepare_combine.py` converts the analysis histogram output into the two files required by Combine.

```bash
cd Run_analysis/
python prepare_combine.py
```

This produces in `Outputs/`:

| File                 | Contents                                                               |
| -------------------- | ---------------------------------------------------------------------- |
| `combine_input.root` | All signal and background histograms (nominal + systematic variations) |
| `hww_datacard.txt`   | Physics model definition: processes, regions, and uncertainties        |

### 2.1 Histogram Harvesting

`prepare_combine.py` extracts the relevant histogram (the Higgs transverse mass $m_T^H$ distribution) from each region and each sample, and writes them into the ROOT file in the naming convention expected by Combine:

```
<process>_<region>        → nominal shape
<process>_<region>_<syst>Up / Down  → systematic variation shapes
```

### 2.2 Bin Stabilization

Empty bins or bins with negative content (arising from negative MC weights) are set to a small positive value. This ensures numerical stability of the likelihood fit.

---

## 3. The Datacard

The datacard `Outputs/hww_datacard.txt` defines the full statistical model. It specifies:

- **Channels (bins):** The Signal Region and Top Control Region are fit **simultaneously**.
- **Processes:** Signal (`Higgs`) and all background components listed per channel.
- **Rates:** Expected yields in each channel.
- **Systematics:** The uncertainty model (see Section 4).

!!! note "Simultaneous fit"
By including the Top Control Region in the fit, the normalization of the dominant $t\bar{t}$ background is **constrained directly by data**, reducing the overall uncertainty on the signal extraction.

---

## 4. Systematic Uncertainties

Two types of systematic uncertainties are included in the datacard:

### 4.1 Normalization Uncertainties (`lnN`)

Log-normal uncertainties applied as an overall rate scaling:

| Uncertainty            | Type  | Value            |
| ---------------------- | ----- | ---------------- |
| Luminosity             | `lnN` | 1.025 (2.5%)     |
| Cross-section (theory) | `lnN` | Sample-dependent |

### 4.2 Shape Uncertainties

These modify the shape of the $m_T^H$ distribution. Shape systematic templates are stored in `combine_input.root` with `Up` / `Down` suffixes:

| Uncertainty               | Source                      |
| ------------------------- | --------------------------- |
| Trigger efficiency SF     | $\eta$–$p_T$ bin variations |
| Electron ID efficiency SF | $\eta$–$p_T$ bin variations |
| Muon ID efficiency SF     | $\eta$–$p_T$ bin variations |
| Muon isolation SF         | $\eta$–$p_T$ bin variations |

---

## 5. Running Combine

Combine can be installed via its [official documentation](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/). Once installed:

### 5.1 Expected Limits (Asymptotic CLs)

```bash
combine -M AsymptoticLimits hww_datacard.txt -n HWW --run expected
```

This computes the **95% CL expected upper limit** on $\mu$ using the asymptotic approximation:

```
 -- AsymptoticLimits ( CLs ) --
Expected  2.5%: r < ...
Expected 16.0%: r < ...
Expected 50.0%: r < ...
Expected 84.0%: r < ...
Expected 97.5%: r < ...
```

### 5.2 Best-Fit Signal Strength

```bash
combine -M FitDiagnostics hww_datacard.txt -n HWW --plots
```

This runs the full profile likelihood fit and returns:

- The best-fit $\hat{\mu}$ with uncertainties.
- Post-fit background normalization factors.
- A `fitDiagnostics.root` file with pre-fit and post-fit distributions.

### 5.3 Significance

```bash
combine -M Significance hww_datacard.txt -n HWW
```

Computes the observed (and expected) significance of any signal excess in units of standard deviations ($\sigma$).

---

## 6. Interpreting the Results

| Result                     | Interpretation                                        |
| -------------------------- | ----------------------------------------------------- |
| $\hat{\mu} \approx 1$      | Data consistent with SM Higgs signal                  |
| Upper limit on $\mu$ < 1   | Better-than-SM sensitivity (analysis is constraining) |
| Observed significance > 5σ | Discovery-level evidence for Higgs in this channel    |

!!! info "Open Data context"
This analysis uses a **subset** of the full CMS Run 2 dataset (~16 fb$^{-1}$ vs. ~137 fb$^{-1}$ total), and omits several advanced corrections applied in the official CMS analysis. The results are therefore educational in nature and should not be compared directly to the published CMS measurements.
