# Physics Background

This analysis searches for the Higgs boson decaying via the $H \rightarrow W^+W^-$ channel using publicly available CMS Open Data. This page covers the experimental context, the signal process, and the background landscape.

---

## 1. Signal Process: $H \rightarrow WW^* \rightarrow e\nu\,\mu\nu$

### 2.1 Higgs Production at the LHC

The Higgs boson was discovered in 2012 at the LHC. At $\sqrt{s} = 13\,\text{TeV}$, the dominant production mode is **gluon-gluon fusion (ggH)**, where two gluons interact via a top-quark loop to produce a Higgs boson:

$$gg \xrightarrow{\text{top loop}} H$$

The ggH cross section at $m_H = 125\,\text{GeV}$ is approximately $49\,\text{pb}$, making it by far the most copiously produced Higgs process at the LHC.

### 2.2 The $H \rightarrow WW^*$ Decay Channel

With a branching fraction of $\sim 21\%$, $H \rightarrow WW^*$ is the second-largest Higgs decay mode. This analysis specifically targets the **fully leptonic, opposite-flavour (eμ) final state**:

$$gg \rightarrow H \rightarrow W^+W^{-*} \rightarrow e^{\pm}\,\nu_e\,+\,\mu^{\mp}\,\nu_\mu$$

#### Why the $e\mu$ final state?

- **Z-boson rejection**: The opposite-flavour ($e\mu$) requirement eliminates the massive Drell-Yan background from $Z \rightarrow ee$ and $Z \rightarrow \mu\mu$ decays, which would otherwise overwhelm the signal.
- **Clean signature**: Two isolated, high-$p_T$ leptons of opposite charge, plus genuine missing transverse energy ($E_T^{\text{miss}}$) from two escaping neutrinos.
- **Spin correlation**: Because the Higgs has spin-0, its decay products are correlated — the two charged leptons tend to be emitted **close together** (small $\Delta\phi_{\ell\ell}$), unlike many backgrounds where they are back-to-back.

#### Experimental signature summary

| Observable                | Signal                                |
| ------------------------- | ------------------------------------- |
| Lepton multiplicity       | Exactly 2 (one $e$, one $\mu$)        |
| Lepton charges            | Opposite sign ($q_e \cdot q_\mu < 0$) |
| Missing transverse energy | $E_T^{\text{miss}} > 20\,\text{GeV}$  |
| Azimuthal angle           | Small $\Delta\phi_{\ell\ell}$         |

!!! note "No invariant mass peak"
Because **two neutrinos** escape detection, the full Higgs invariant mass cannot be reconstructed. Instead we use the **Higgs transverse mass** $m_T^H$ as the primary discriminating variable:
$$m_T^H = \sqrt{2\,p_T^{\ell\ell}\,E_T^{\text{miss}}\left(1 - \cos\Delta\phi(\ell\ell,\,E_T^{\text{miss}})\right)}$$

---

## 3. Background Processes

Several Standard Model processes produce final states that are difficult to distinguish from the signal. Understanding their origin and suppression strategy is crucial for the analysis design.

### 3.1 Irreducible Backgrounds

These processes produce the **exact same** $e^\pm\mu^\mp + E_T^{\text{miss}}$ final state and cannot be removed by object selection alone.

#### $q\bar{q} \rightarrow WW$ (continuum WW)

The dominant irreducible background. Unlike the scalar Higgs (spin-0), the spin-1 $W$ bosons from $q\bar{q}$ annihilation lead to **larger opening angles** between the leptons ($\Delta\phi_{\ell\ell}$ tends to be larger). This spin-correlation difference is exploited in the final fit.

#### $gg \rightarrow WW$ (ggWW)

A rarer loop-induced process kinematically similar to the signal. It is treated as a separate background component in the statistical model.

### 3.2 Reducible Backgrounds

These processes mimic the signal due to object misidentification or specific decay topologies.

| Background                     | Why it mimics H→WW                                                                     | Suppression                           |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------- |
| **$t\bar{t}$ / Single Top**    | Top decays $t\to Wb$; if both $W$s decay leptonically: $e\mu + E_T^{\text{miss}} + 2b$ | **b-jet veto**                        |
| **Drell-Yan ($Z\to\tau\tau$)** | $\tau\to e/\mu + \nu\nu$: soft leptons + real $E_T^{\text{miss}}$                      | $m_T^H$ cut and $m_{\ell\ell}$ window |
| **Diboson (WZ, ZZ)**           | $WZ\to 3\ell\nu$: mimics signal if one lepton is lost                                  | 2-lepton selection                    |
| **V+γ ($W\gamma$, $Z\gamma$)** | $\gamma$ converts in tracker material → fake $e$                                       | Tight electron ID                     |
| **Fakes ($W$+jets, QCD)**      | Jet misidentified as a lepton                                                          | Tight ID + isolation                  |

---

## 4. Analysis Strategy

The analysis follows a **Cut-and-Count** strategy organized around mutually exclusive signal and control regions, built from the following steps:

1. **Data Quality**: Golden JSON masking (data) and luminosity normalization (simulation).
2. **Object Selection**: Tight lepton definitions ($e$: MVA WP90; $\mu$: Tight ID + PF isolation).
3. **Pre-Selection**: Exactly one $e\mu$ pair of opposite sign and opposite flavour.
4. **Corrections**: Data/MC scale factors for trigger, lepton ID, and isolation efficiencies.
5. **Event Variables**: Compute $m_T^H$, $m_{\ell\ell}$, $\Delta\phi_{\ell\ell}$, etc.
6. **Jet Categorization**: Split events into 0-jet, 1-jet, and ≥2-jet bins.
7. **Region Assignment**: Assign events to Signal Region (SR), Top Control Region (CR-Top), or DY Control Region (CR-DY).

!!! tip "See the full walkthrough"
For step-by-step details of each selection cut and the analysis code, see the [Process Flowchart](../analysis/flowchart.md) and [Execution Guide](../analysis/interactive-execution.md).
