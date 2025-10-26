# H→WW Analysis Notebook: Physics Motivation, Methods, and Code Guide

This notebook documents the motivation, physics, and software used in our H→WW→eνμν analysis, and serves as a structured guide to the code and plots produced.

---

## 0) Executive Summary

- Physics target: Higgs boson decays to W boson pairs with opposite-flavor leptons (e, μ) and neutrinos (missing energy).
- Strategy: Select clean e–μ events, apply global quality and kinematic cuts, categorize by jet multiplicity (0/1/2 jets), define signal and control regions (SR/CR), validate with data.
- Outputs: Superimposed distributions (signal vs backgrounds) per stage and variable, plus stacked SR/CR plots with data as black dots and signal overlay.

---

## 1) Higgs Boson Basics

- Electroweak symmetry breaking (EWSB): The Higgs field acquires a nonzero vacuum expectation value (VEV) and gives masses to W/Z bosons and fermions through Yukawa couplings.
- The Higgs boson (H) is the quantum excitation of the Higgs field and was discovered at the LHC in 2012.
- Couplings scale with mass: heavier particles couple more strongly to the Higgs. This guides production/decay rates and analysis choices.

Key production modes at the LHC:
- ggF (gluon–gluon fusion): dominant cross section, inclusive.
- VBF (vector boson fusion): characterized by two forward jets with large rapidity separation and dijet mass.
- Associated production (VH, ttH): smaller cross sections; useful for coupling measurements.

Key decays near mH ≈ 125 GeV:
- H→bb (largest BR), H→WW (sizeable BR), H→ZZ, H→γγ, H→ττ, etc.

---

## 2) Why the Higgs Is Hard to Detect

- Small signal rates: Though ggF is large among Higgs modes, the inclusive rate times branching ratio is modest; tight selection needed.
- Large backgrounds:
  - Prompt WW production (continuum).
  - Top (tt̄, single top) with genuine leptons and MET.
  - Drell–Yan (Z/γ*→ℓℓ or ττ) faking MET or producing similar kinematics.
  - W+jets and multijets with nonprompt/fake leptons (analysis dependent).
- Invisible neutrinos: Multiple neutrinos smear mass-sensitive observables; no narrow mass peak (unlike H→γγ).
- Detector and pileup effects: Smear kinematics, add extra jets, complicate MET reconstruction.

---

## 3) Why Measuring H Matters

- Validate the Higgs mechanism: Couplings and rates must match SM predictions within uncertainties.
- Precision program: Measure production cross sections and branching ratios per category (ggF, VBF, …).
- Portal to new physics: Deviations in rates or kinematics may indicate BSM effects (anomalous couplings, invisible decays, EFT, …).

---

## 4) Our Physics Channel and Strategy

Target final state: H→WW→eνμν (opposite-flavor leptons, OS charge)
- Advantages: Lower Drell–Yan contamination than same-flavor channels.
- Topology: Two prompt isolated leptons (e, μ), significant MET from νs, limited mass resolution due to neutrinos.
- Categorization by jet multiplicity:
  - 0-jet, 1-jet: enhance ggF-like topologies; different background compositions.
  - 2-jet: enrich VBF; use dijet variables (e.g., mjj) for discrimination.

Region definitions (conceptual):
- Before cuts: post basic channel selection (e–μ).
- Global: quality/kinematic cuts to define a clean baseline sample (e.g., OS leptons, pT thresholds, Δφ/ptll/mT-based requirements, b-jet veto).
- Signal Regions (SR_0jet, SR_1jet, SR_2jet): tuned selections that maximize Higgs sensitivity in each jet bin.
- Control Regions (CR_top_X): enhance top background (often by inverting/relaxing b-jet veto).
- Control Regions (CR_tau_X): enhance Z→ττ background (use ττ-like kinematics; Δφ_ll, m_ll, mT shapes).

Exact thresholds are encoded in the analysis functions; this notebook documents the flow and where to adjust them.

---

## 5) Variables Used

We study these observables across stages/categories:
- m_ll (mass): dilepton invariant mass, $m_{\ell\ell}$.
- MET: missing transverse energy, $E_T^{miss}$.
- Δφ_ll: azimuthal separation of leptons, $\Delta\phi_{\ell\ell}$.
- pT_ll: dilepton transverse momentum, $p_T^{\ell\ell}$.
- mT^H: Higgs transverse mass proxy, $m_T^{H}$ (constructed from leptons and MET).
- mT(l2, MET): transverse mass of subleading lepton and MET.
- m_jj: dijet invariant mass (relevant in ≥2-jet / VBF-like events).

These variables are binned and visualized per stage to validate modeling and define SR/CR selections.

---

## 6) Datasets and Samples

- Signal: e.g., ggH→WW, VBF→WW.
- Backgrounds: WW, top (tt̄ + single top), Drell–Yan (Z/γ*→ℓℓ, ττ), possibly W+jets, dibosons (WZ, ZZ) depending on configuration.
- Data: real collision data for validation and normalizations in CRs.

Sample configuration SAMPLES (notebook-global) encodes:
- color for plots
- is_signal flag
- any metadata needed (xsec, n_gen, scaling)

---

## 7) Code Architecture (What the Notebook Runs)

High-level flow:
1) Read events in batches to control memory.
2) Build leptons and MET; select e–μ channel.
3) Compute kinematic variables once per batch.
4) Build masks for global selection and jet categories (0/1/2).
5) Compute mjj and b-jet veto, then derive SR and CR masks.
6) Collect per-stage arrays into `stage_collectors`.
7) Concatenate at the end into `stage_data_final` for plotting.

Key functions you will find in the notebook:

```python
def process_file_unified(fname, label):
    # Or memory-optimized variant
    # - Initializes collectors and cutflow
    # - Iterates load_events(..., batch_size=...)
    # - Calls process_single_batch(...)
    # - Finalizes per-stage arrays (awkward/NumPy)
    # - Returns stage_data_final[sample][stage][variable]
```

```python
def process_single_batch(arrays, stage_collectors, cutflow):
    # 1) select_tight_leptons(arrays)
    # 2) select_e_mu_events(tight_leptons, met)
    # 3) cal_kinematic_var(leading, subleading, met_selected)
    # 4) get_event_mapping_indices(...): map selections to event indices
    # 5) count_jets(...), calculate_mjj(...), apply_bjet_selections(...)
    # 6) apply_global_cuts(...), derive SR/CR masks
    # 7) collect_stage_data(...) per stage
```

```python
def collect_stage_data(stage_name, stage_collectors, kinematic_vars, mask=None, mjj_override=None):
    # Appends arrays per variable into stage-specific lists
    # Final concatenation happens once at the end
```

Data structure at the end:
```text
stage_data_final = {
  sample_name: {
    'before_cuts': {'mass': ak.Array([...]), 'met': ..., 'dphi': ..., 'ptll': ..., 'mt_higgs': ..., 'mt_l2_met': ..., 'mjj': ..., 'leading': ..., 'subleading': ...},
    'global': { ... },
    '0jet': { ... }, '1jet': { ... }, '2jet': { ... },
    'SR_0jet': { ... }, 'SR_1jet': { ... }, 'SR_2jet': { ... },
    'CR_top_0jet': { ... }, 'CR_top_1jet': { ... }, 'CR_top_2jet': { ... },
    'CR_tau_0jet': { ... }, 'CR_tau_1jet': { ... }, 'CR_tau_2jet': { ... }
  },
  ...
}
```

---

## 8) Plotting Outputs

- Superimposed plots per variable and category:
  - Show signal and all backgrounds overlaid (histtype='step' for MC; data as black dots when available).
  - Grids can show variables × {before, global, 0j, 1j, 2j}.

- Stacked plots for SR/CR with all jet categories:
  - Backgrounds stacked (filled), signal overlaid as a step outline.
  - Data drawn as black dots at bin centers (no stacking), often with log-y.
  - 3×3 layout: rows = {SR, CR_top, CR_tau}, cols = {0j, 1j, 2j}.

Example call in the notebook:
```python
fig = plot_sr_cr_stacked('mass', variables_to_plot['mass'], stage_data_final)
```

---

## 9) Programming Tools and Libraries

- Python 3.x in Jupyter Notebook.
- Awkward Array (`awkward`): columnar jagged arrays for HEP event data.
- NumPy: numerics, histogramming, vector operations.
- Uproot (implicitly via `load_events`): read ROOT files in Python (if used under the hood).
- Matplotlib: plotting (superimposed and stacked histograms, error bars, scatter).
- psutil (optional): memory monitoring for large-scale processing.
- gc: manual garbage collection to control memory peaks.
- Your analysis utilities:
  - `select_tight_leptons`, `select_e_mu_events`
  - `cal_kinematic_var`
  - `count_jets`, `calculate_mjj`
  - `apply_bjet_selections`
  - `apply_global_cuts`
  - `apply_signal_region_cuts`, `apply_control_region_cuts`

---

## 10) Normalization and Scaling

MC event yields are scaled to the target integrated luminosity:
- Per-sample weight:
  $$
  w_{\text{MC}} = \frac{\sigma \cdot \mathcal{L} \cdot \epsilon_{\text{filter}} \cdot k\text{-factor}}{N_{\text{generated}}}
  $$
- Data weight: 1.0 (counted as observed events).
- Optional per-event weights (if available): pileup, lepton ID/ISO scale factors, trigger SFs, b-tag SFs, etc.

Note: Apply scaling consistently to histogram fills and yield tables.

---

## 11) Physics Logic of the Selections (“Complete Requirements”)

Conceptual ingredients the code implements:

- Channel preselection (e–μ OS):
  - Exactly two tight leptons (sorted by pT), opposite charge, opposite flavor (eμ or μe).
  - Baseline pT thresholds (leading/subleading) and identification/isolation.

- Global selection:
  - Kinematic quality cuts using m_ll, Δφ_ll, pT_ll, MET, mT variables to reduce DY and nonprompt.
  - b-jet veto to suppress top in SR-like selections.

- Jet categories:
  - 0-jet / 1-jet / 2-jet masks from `count_jets` to control background mixture and target production modes.
  - In ≥2-jet, exploit VBF-like features (e.g., mjj) downstream.

- Signal regions (SR_0/1/2jet):
  - Tighten Higgs-like kinematics: characteristic Δφ_ll, pT_ll, m_ll, mT^H patterns.
  - Maintain b-jet veto, apply jet-bin-specific optimizations.

- Control regions:
  - CR_top_X: Enrich top (often by inverting/relaxing b-veto or selecting ≥1 b-tag).
  - CR_tau_X: Enrich Z→ττ (DY-like kinematics: m_ll, Δφ_ll, mT features tailored).
  - Used to validate shapes and constrain normalizations in a fit.

All selection thresholds are encoded in the helper functions. Adjust those to tune purities and acceptances.

---

## 12) Performance and Memory Notes

- Batch processing (`load_events(..., batch_size=...)`) prevents loading entire datasets in memory.
- Append-per-batch collections; concatenate once at the end.
- If memory pressure is high:
  - Reduce `batch_size`.
  - Periodically consolidate partial arrays (concatenate every N batches).
  - Convert large numeric buffers to NumPy where feasible before final awkward conversion.
  - Explicitly `del` intermediates and run `gc.collect()` per batch.

---

## 13) How to Run This Notebook End-to-End

1) Configure samples (SAMPLES) and input files.
2) Process each file:
```python
stage_data_final[label], _, cutflow = process_file_unified(fname, label)
```

3) Plot superimposed distributions (per variable × category grid):
```python
create_superimposed_plots(stage_data_final, SAMPLES)
```

4) Plot SR/CR stacks with data overlay:
```python
plot_sr_cr_stacked('mass', variables_to_plot['mass'], stage_data_final)
```

5) Inspect yields and cutflow to validate rates.

---

## 14) Glossary

- SR (Signal Region): region optimized for signal sensitivity.
- CR (Control Region): region enriched in a background used to constrain it.
- VBF: vector boson fusion production mode, typically two forward jets, high mjj.
- b-jet veto: requirement that no b-tagged jets are present (suppresses top).
- MET: missing transverse energy (from neutrinos, mismeasurements).
- mT: transverse mass, proxy for kinematics involving neutrinos.

---

## 15) Adapting and Extending

- To change SR/CR definitions, edit:
  - `apply_signal_region_cuts(...)`
  - `apply_control_region_cuts(...)`
- To add variables, compute them in `cal_kinematic_var(...)` and propagate through collectors.
- To add a new CR (e.g., W+jets CR), define a mask function and add it alongside SR/CR collection.

---

If anything in the physics or code needs deeper detail (exact thresholds, object definitions, trigger lists), add a dedicated section and link to the function that implements it.