"""
calculations.py

This module contains functions for calculating high-level kinematic variables 
necessary for this analysis. 

It handles:
- 4-vector kinematics using the `vector` package.
- Angle normalizations.
- Transverse Mass calculations (Higgs Mt, Subleading Lepton Mt).
- Invariant Mass calculations (Dilepton mass, Dijet mass).
"""

import numpy as np
import awkward as ak
import vector

def wrap_angle_to_pi(angle):
    """
    Wraps an angle to be within the range [-pi, pi].
    Crucial for calculating Delta Phi (dPhi) between two objects.
    
    Parameters
    ----------
    angle : float or awkward.Array
        The raw angle difference to be wrapped.
        
    Returns
    -------
    float or awkward.Array
        The normalized angle in the range [-pi, pi].
    """
    return (angle + np.pi) % (2 * np.pi) - np.pi

def create_lepton_vector(lepton):
    """
    Creates a 4-momentum vector array from an awkward array of leptons.
    Uses the `vector` package to enable relativistic kinematics calculations.
    
    Parameters
    ----------
    lepton : awkward.Record
        An awkward array record containing 'pt', 'eta', 'phi', and 'mass' fields.
        
    Returns
    -------
    vector.Momentum4D
        An array of 4-vectors representing the leptons.
    """
    return vector.array({
        "pt": lepton.pt,
        "eta": lepton.eta,
        "phi": lepton.phi,
        "mass": lepton.mass
    })

def cal_kinematic_var(leading, subleading, met):
    """
    Calculates the primary kinematic variables used for signal/background 
    discrimination in the this analysis.
    
    Parameters
    ----------
    leading : awkward.Record
        The leading (highest pT) lepton in the event.
    subleading : awkward.Record
        The subleading (second highest pT) lepton in the event.
    met : awkward.Record
        Missing Transverse Energy (MET) of the event.
        
    Returns
    -------
    tuple of awkward.Array
        (masses, ptll, dphi, mt_higgs, mt_l2_met) representing the calculated variables.
    """
    # Create 4-vectors for the leptons
    lepton_1 = create_lepton_vector(leading)
    lepton_2 = create_lepton_vector(subleading)
    
    # Create the dilepton system 4-vector by summing the two leptons
    dilepton = lepton_1 + lepton_2
    
    # ---------------------------------------------------------
    # Basic Variables
    # ---------------------------------------------------------
    masses = dilepton.mass  # Invariant mass of the dilepton system (m_ll)
    ptll = dilepton.pt      # Transverse momentum of the dilepton system (pT_ll)
    dphi = wrap_angle_to_pi(leading.phi - subleading.phi)  # Delta phi between the two leptons
    
    # ---------------------------------------------------------
    # Higgs Transverse Mass 
    # ---------------------------------------------------------
    # Transverse energy of the dilepton system
    dll_et = np.sqrt(dilepton.pt**2 + dilepton.mass**2)
    # Delta phi between the dilepton system and MET
    mt_higgs_dphi = wrap_angle_to_pi(dilepton.phi - met.phi)
    
    term_1 = masses**2
    term_2 = 2 * (dll_et * met.pt - dilepton.pt * met.pt * np.cos(mt_higgs_dphi))
    mt_higgs = np.sqrt(term_1 + term_2)
    
    # ---------------------------------------------------------
    # Subleading Lepton Transverse Mass (m_T(l2, MET))
    # ---------------------------------------------------------
    mt_l2_met_dphi = wrap_angle_to_pi(subleading.phi - met.phi)
    mt_l2_met = np.sqrt(2 * subleading.pt * met.pt * (1 - np.cos(mt_l2_met_dphi)))

    return masses, ptll, dphi, mt_higgs, mt_l2_met


def calculate_mjj(jets):
    """
    Calculates the invariant mass of the two leading jets (m_jj).
    This is primarily used for defining the 2-jet Signal and Control regions.
    
    Parameters
    ----------
    jets : awkward.Array
        An array of cleaned, sorted jets for each event.
        
    Returns
    -------
    awkward.Array
        The calculated m_jj values. Returns 0.0 for events with fewer than 2 jets.
    """
    # Get number of jets per event
    n_jets = ak.num(jets)
    
    # Initialize mjj with zeros for all events
    mjj = ak.zeros_like(n_jets, dtype=float)
    
    # Create mask for events with at least 2 jets
    has_two_jets = n_jets >= 2
    
    # Only proceed with the calculation if there are events with 2+ jets
    if ak.any(has_two_jets):
        # Pad the jets array so every event has at least 2 entries (fills with None)
        jets_padded = ak.pad_none(jets, 2, axis=1)
        
        # Create 4-vectors for the jets, filling 'None' padded values with 0.0
        jet_vectors = ak.zip({
            "pt": ak.fill_none(jets_padded.pt, 0.0),
            "eta": ak.fill_none(jets_padded.eta, 0.0),
            "phi": ak.fill_none(jets_padded.phi, 0.0),
            "mass": ak.fill_none(jets_padded.mass, 0.0)
        }, with_name="Momentum4D")
        
        # Get the two leading jets
        jet1 = jet_vectors[:, 0]
        jet2 = jet_vectors[:, 1]
        
        # Calculate invariant mass using vector addition
        dijet = jet1 + jet2
        mjj_calculated = dijet.mass
        
        # Apply the calculated mass only to events that actually had 2+ jets
        mjj = ak.where(has_two_jets, mjj_calculated, 0.0)
    
    return mjj

def apply_mjj_window(mjj):
    """
    Applies the m_jj mass window cut used in the 2-jet category.
    This vetoes the Z boson mass peak to reduce Drell-Yan background.
    
    Parameters
    ----------
    mjj : awkward.Array
        The calculated dijet invariant mass array.
        
    Returns
    -------
    awkward.Array (boolean mask)
        True for events passing the window requirement: 
        m_jj < 65 OR (105 < m_jj < 120)
    """
    return (mjj < 65) | ((mjj > 105) & (mjj < 120))