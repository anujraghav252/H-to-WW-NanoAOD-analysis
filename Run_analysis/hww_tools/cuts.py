"""
cuts.py

This module contains functions to apply the core analysis selections.
It defines the boolean masks that filter the dataset into specific regions:
- Global pre-selection: Baseline cuts applied to all events.
- Signal Regions (SR): Regions optimized to be rich in the H -> WW signal.
- Control Regions (CR): Regions enriched in specific backgrounds used to estimate background yields in the signal region.
"""

import awkward as ak
from .calculations import apply_mjj_window

def apply_global_cuts(leading, subleading, met, mt_higgs, mt_l2_met, ptlls, masses):
    """
    Applies the global pre-selection cuts to all candidate events.
    
    Parameters
    ----------
    leading, subleading, met, mt_higgs, mt_l2_met, ptlls, masses : awkward.Array
        Arrays containing the kinematic variables for each event.
        
    Returns
    -------
    global_mask : awkward.Array (boolean)
        A 1D boolean array where True indicates the event passed all global cuts.
    cutflow_dict : dict
        A dictionary containing the number of events passing each individual cut, 
        useful for tracking yields.
    """
    # Reject QCD multijet and low-MET backgrounds
    mask_met_pt = met.pt > 20
    
    # Require sufficient transverse momentum for the dilepton system
    mask_ptll  = ptlls > 30
    
    # Remove low-mass resonances
    mask_mll = masses > 12 
    
    # Combine all individual masks using AND
    global_mask = mask_met_pt & mask_ptll & mask_mll
    
    return global_mask, {
        'pass_met_pt': ak.sum(mask_met_pt),
        'pass_ptll': ak.sum(mask_ptll),
        'pass_mll': ak.sum(mask_mll),
        'pass_global': ak.sum(global_mask)
    }

def apply_signal_region_cuts(leading, subleading, met, masses, ptlls, mt_higgs, 
                             mt_l2_met, isZeroJet, isOneJet, isTwoJet, 
                             bjet_veto_mask, mjj=None):
    """
    Applies Signal Region (SR) selections and splits them into jet categories.
    
    Returns
    -------
    sr_regions : dict
        A dictionary mapping region names ('SR_0jet', 'SR_1jet', 'SR_2jet') 
        to their respective boolean masks.
    """
    # Define the core SR cuts common to all jet bins
    sr_specific_cuts = (
        (met.pt > 20) &            # Basic MET requirement
        (ptlls > 30) &             # Dilepton pT requirement
        (masses > 12) &            # Low mass resonance veto
        (mt_higgs > 60) &          # Selects Higgs-like high transverse mass
        (mt_l2_met > 30) &         # Suppresses W+jets (where jet fakes subleading lepton)
        bjet_veto_mask             # Strict b-jet veto to heavily suppress Top background
    )
    
    sr_base = sr_specific_cuts
    
    # Apply m_jj window exclusively for the 2-jet category to suppress Drell-Yan
    if mjj is not None:
        mjj_window = apply_mjj_window(mjj)
    else:
        mjj_window = ak.ones_like(isTwoJet, dtype=bool)
        
    # Create the final masks by intersecting the base SR cuts with the jet bin masks
    sr_regions = {
        'SR_0jet': sr_base & isZeroJet,
        'SR_1jet': sr_base & isOneJet,
        'SR_2jet': sr_base & isTwoJet & mjj_window
    }
    
    return sr_regions

def apply_control_region_cuts(leading, subleading, met, masses, ptlls, mt_higgs, 
                              mt_l2_met, isZeroJet, isOneJet, isTwoJet, 
                              bjet_info, mjj=None):
    """
    Applies Control Region (CR) selections for Top and Tau-Tau backgrounds.
    
    Returns
    -------
    cr_regions : dict
        A dictionary mapping CR names to their respective boolean masks.
    """
    # Baseline CR cuts (similar to global cuts, plus subleading lepton MT cut)
    cr_base = (
        (met.pt > 20) &
        (ptlls > 30) &
        (mt_l2_met > 30) &
        (masses > 12)
    )
    
    # Apply mjj window for 2-jet category
    if mjj is not None:
        mjj_window = apply_mjj_window(mjj)
    else:
        mjj_window = ak.ones_like(isTwoJet, dtype=bool)
        
    cr_regions = {}
    
    # =========================================================================
    # TOP CONTROL REGIONS
    # =========================================================================
    cr_top_base = cr_base & (masses > 50)  # Removes low-mass Drell-Yan
    
    cr_regions['CR_top_0jet'] = (
        cr_top_base & 
        isZeroJet & 
        bjet_info['has_btag_20_30']  # For 0-jet, look for soft b-jets (20 < pT < 30 GeV)
    )
    cr_regions['CR_top_1jet'] = (
        cr_top_base & 
        isOneJet & 
        bjet_info['has_btag_30']     # For 1-jet, require a hard b-jet (pT > 30 GeV)
    )
    cr_regions['CR_top_2jet'] = (
        cr_top_base & 
        isTwoJet & 
        mjj_window &
        bjet_info['has_btag_30']     # For 2-jet, require a hard b-jet (pT > 30 GeV)
    )
    
    # =========================================================================
    # TAU-TAU (Drell-Yan) CONTROL REGIONS
    # =========================================================================
    cr_tau_base = (
        cr_base & 
        (mt_higgs < 60) &              # Invert the Higgs MT cut (Signal has > 60)
        (masses > 40) & (masses < 80) & # Restrict to Z-boson mass window
        bjet_info['passes_bjet_veto']  # Veto b-jets to suppress Top contamination
    )
    
    cr_regions['CR_tau_0jet'] = cr_tau_base & isZeroJet
    cr_regions['CR_tau_1jet'] = cr_tau_base & isOneJet  
    cr_regions['CR_tau_2jet'] = cr_tau_base & isTwoJet & mjj_window
    
    return cr_regions