# **Signal and Background Processes**

## **The Signal Process**

As established in the previous section, this analysis targets the **fully leptonic different-flavor final state** of the Higgs boson produced via gluon-gluon fusion:

$$gg \to H \to WW^* \to e^{\pm}\mu^{\pm}\nu\bar{\nu}$$

This signal process is characterized by:

- **Two leptons of different flavor:** One electron and one muon, each carrying high transverse momentum
- **Two neutrinos:** Manifested as missing transverse energy (MET) in the detector
- **No jets:** Ideally, no hadronic jets

Several Standard Model processes can mimic this signature, either exactly or through partial overlap with the final state. Understanding and suppressing these backgrounds is crucial for isolating the signal.

---

## **Background Processes**

The backgrounds relevant to this analysis are several Standard Model processes that can mimic or partially overlap with the signal signature.

### **Drell-Yan to Tau-Tau**

**Final State:** $q\bar{q} \to Z^*/\gamma^* \to \tau^{+}\tau^{-}$ where, $\tau \to \ell\nu$


**Why It Mimics the Signal:**

- When $\tau$ leptons decay leptoically to different flavors ($\tau \to e^\pm \nu$, $\tau \to \mu^\pm \nu$), the visible dilepton state ($e^{\pm}\mu^{\pm}$) is identical to the signal topology.
  
- Both processes produce leptons with missing transverse energy.
  

**Suppression Strategy:**

- **Azimuthal Separation:** In Drell–Yan processes, the final-state particles are typically produced back-to-back, whereas in Higgs decays they are more collinearly produced.
   
- **Transverse Mass Selection:** The transverse mass $m_T^H$ distribution for signal peaks at the Higgs mass, while DY events have a broader, lower distribution. This provides additional separation

---

### **Top Quark Pair Production**

**Final State:** $q\bar{q} \to t\bar{t} \to (b\ell\nu)(b\bar{\ell}'\bar{\nu})$ 


**Why It Mimics the Signal:**

- Both the signal and top pair production result in two leptons of opposite charge with missing transverse energy
- Top events genuinely produce two neutrinos (one per top decay), resulting in significant MET similar to the signal
- The kinematic distributions can partially overlap with the signal

<!-- **Distinguishing Features:**

- **$b$-tagging:** Top events include two $b$-jets from the top quark decays; signal events have no such jets. This is the primary handle for background rejection
  
- **Kinematics:** Signal leptons originate from $W$ bosons from a single parent Higgs, while top leptons originate from two separate top quarks. This leads to different angular correlations and momentum distributions -->

**Suppression Strategy:**

- **Jet Veto / $b$-Jet Veto:** Requiring the absence of jets (especially $b$-tagged jets) suppresses top events while retaining signal events. Signal production via gluon fusion naturally has minimal jet activity
  
- **MET and Transverse Mass Cuts:** While top events do have significant MET, their transverse mass and dilepton momentum distributions differ from the signal, allowing additional discrimination

---

### **Diboson Production (VZ: WZ, ZZ)**

**Final State:** $q\bar{q} \to VV \to (W \to \ell\nu)(Z \to \ell^+\ell^-)$ 

**Why It Mimics the Signal:**

- WZ production with $W \to \ell\nu$ and $Z \to \ell^+\ell^-$ produces exactly two leptons and MET
    
- MET from the $W$ decay neutrino can be substantial

<!-- **Distinguishing Features:**

- **Dilepton Invariant Mass:** For WZ events, the mass is more constrained by the $Z$ mass ($\approx 91 \text{ GeV}$) compared to signal
  
- **Third Lepton or Jet Activity:** Some WZ/ZZ events have additional leptons or jets that help identify them -->

**Suppression Strategy:**

- **Dilepton Invariant Mass Windows:** Selecting events outside the $Z$ mass region suppresses this background
  
- **Additional Lepton/Jet Veto:** Rejecting events with third leptons or jets reduces contamination
  
---

### **WW Production (WW, ggWW)**

**Final State:** $q\bar{q}/gg \to WW \to (W \to e\nu)(W \to \mu\nu)$


**Why It Mimics the Signal:**

- Both WW and signal processes produce exactly two leptons of opposite charge and missing transverse energy
- The distributions are kinematically similar: two leptons and two neutrinos

<!-- **Key Difference:**
- The angular correlations differ between a scalar Higgs decay ($H \to WW$) and non-resonant WW production
  
- Signal Higgs decays produce a characteristic kinematic pattern: leptons tend to be more collimated with lower separation angles
  
- Continuum WW production has different angular correlations due to spin-1 vector bosons -->

**Suppression Strategy:**

- **Kinematic Distributions:** The transverse mass $m_T^H$, dilepton invariant mass $m_{\ell\ell}$, and angular separation $\Delta\phi_{\ell\ell}$ all differ between signal and WW
  
---

### **Diboson with Photons (VG)**

**Final State:** $q\bar{q} \to VG \to (\ell\nu)(\gamma)$


**Why It Can Mimic the Signal:**

- In rare cases, photons may be misidentified as leptons
  
- The MET from the $W$ or $Z$ decay neutrino can appear similar to the signal

**Suppression Strategy:**
- **Lepton Identification:** Strict electron and muon identification criteria suppress photon misidentification
  
---

### **Fakes**

**Final State:** Jets misidentified as leptons, producing a false dilepton + MET signature

<!-- **Nature:** This is a **reducible background** arising from QCD multi-jet and $W$/Z+jets events where jets are mislabeled as leptons. -->

**Why It Mimics the Signal:**

- Jets from b-quark or charm-quark decays can sometimes pass loose lepton selection criteria
  
- When multiple jets are selected as "leptons," the resulting four-vectors and MET can resemble the signal

**Suppression Strategy:**
- **Tight Lepton Identification:** Applying strict criteria on lepton isolation reduces this background
  
- **Lepton Multiplicity Requirements:** Selecting events with exactly two leptons, with well-defined kinematic properties, suppresses multi-jet contamination

---

<!-- ## **Background Hierarchy and Analysis Strategy**

The relative importance of these backgrounds depends on the specific selection criteria applied:

| Background | Type | Primary Suppression Method | Residual Importance |
| :--------: | :--: | :------------------------: | :-----------------: |
| $DY \to \ell\ell$ | Irreducible | MET + $m_{\ell\ell}$ window | **High** |
| $t\bar{t}$ | Reducible | $b$-jet veto | **Medium** |
| $DY \to \tau\tau$ | Reducible | MET + kinematic cuts | **Low** |
| Diboson (VZ) | Reducible | $m_{\ell\ell}$ window + lepton veto | **Medium** |
| $WW$ / $ggWW$ | Irreducible | Multivariate + $m_T^H$ | **Medium** |
| $VG$ | Reducible | Lepton ID + photon veto | **Low** |
| Fakes | Reducible | Tight lepton ID + isolation | **Low** |

Through a carefully optimized selection combining jet veto, kinematic requirements, and multivariate techniques, the signal significance can be maximized while maintaining a data-driven approach to background estimation through control regions and sideband measurements. -->
