# H -> WW Analysis Cuts
*Based on `Trigger_efficiency.ipynb`*

## 1. Object Selection (Tight Leptons)
**Electrons**
* **Identification:** `Electron_mvaFall17V2Iso_WP90 == True` (MVA ID with 90% efficiency working point)

**Muons**
* **Identification:** `Muon_tightId == True`
* **Isolation:** `Muon_pfRelIso04_all < 0.15` (Tight PF Isolation)

## 2. Event Selection
**Pre-Selection**
* **Lepton Count:** Exactly 2 "Tight" leptons.
* **Flavor:** Opposite Flavor (Electron + Muon).
* **Charge:** Opposite Charge ($q_1 \times q_2 < 0$).

## 3. Kinematic Cuts
**Lepton Kinematics**
* **Leading Lepton $p_T$:** $> 25$ GeV
* **Subleading Lepton $p_T$:** $> 13$ GeV
    * *Note: This is currently set to 13 GeV in the file, not 15 GeV.*
* **Pseudorapidity ($\eta$):** $|\eta| < 2.5$ for Electrons and $|\eta| < 2.4$ for Muons.
    

**Event Kinematics**
* **Invariant Mass ($m_{ll}$):** $> 12$ GeV
* **Dilepton $p_T$ ($p_{T}^{ll}$):** $> 30$ GeV
* **MET ($p_T^{miss}$):** $> 20$ GeV
* **Higgs Transverse Mass ($m_T^H$):** $> 60$ GeV
* **Lepton 2 Transverse Mass ($m_T^{L2}$):** $> 30$ GeV

## 4. Trigger Selection (HLT)
Events must pass **at least one** of the following Cross-Triggers:
* `HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ`
* `HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ`