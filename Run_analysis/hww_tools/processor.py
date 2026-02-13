import sys
import os
import time
import awkward as ak
import numpy as np
import vector

# Internal tool imports
from . import Config
from . import Efficiency_data
from . import Physics_selection
from . import calculations
from . import cuts
from . import helper
from . import json_validation
from . import Plots_config
from .Config import VARIATIONS, stage_names, cutflow_stages
from .Plots_config import variables_to_plots
from .helper import initialize_stage_histograms

"""
processor.py
Contains the main event processing function to be run on Dask workers.
"""

def make_processor(golden_json_data, sample_info_detailed, luminosity, run_periods, project_dir):

    """
    Factory function that prepares the worker function with all necessary static data.
    
    This function "closes over" the configuration data (golden_json, luminosity, etc.)
    so that the returned `processing_file` function has immediate access to them 
    without needing them passed as arguments every time.

    Parameters
    ----------
    golden_json_data : dict or None
        The loaded content of the Golden JSON file. Used to filter Data events 
        based on valid run and luminosity blocks. If None, no JSON filtering is applied.
    
    sample_info_detailed : dict
        A dictionary containing metadata for Monte Carlo samples, specifically:
        - 'xsec': Cross-section of the process.
        - 'sum_genWeight': Sum of generator weights for the sample.
        Used to calculate the scaling factor: (xsec * luminosity) / sum_genWeight.
    
    luminosity : float
        The integrated luminosity to scale MC events to (e.g., 16.1 fb^-1).
    
    run_periods : dict
        Dictionary defining the run periods (e.g., 'B', 'C', 'D') and their 
        corresponding run number ranges. Used for detailed data validation.
    
    project_dir : str or pathlib.Path
        The base directory of the analysis project. Useful for constructing 
        absolute paths if needed.

    Returns
    -------
    function
        The `processing_file` function. 
        Signature: `processing_file(label, file_url, file_idx)`
        
        This returned function is what Dask actually executes on the workers. 
        It takes a single file, processes it, and returns the histograms and cutflows.
    """
    # Helper function 
    def get_sample_key(filename):
        fn = filename
        if any(x in fn for x in ["Run2016", "SingleMuon", "DoubleEG", "MuonEG"]): return None
        if "DYJetsToLL" in fn:         return "DYJetsToLL_M-50"
        if "TTTo2L2Nu" in fn:          return "TTTo2L2Nu"
        if "ST_t-channel_top" in fn:   return "ST_t-channel_top"
        if "ST_t-channel_antitop" in fn: return "ST_t-channel_antitop"
        if "ST_tW_antitop" in fn:      return "ST_tW_antitop"
        if "ST_tW_top" in fn:          return "ST_tW_top"
        if "ST_s-channel" in fn:       return "ST_s-channel"
        if "WJetsToLNu" in fn:         return "WJetsToLNu"
        if "TTToSemiLeptonic" in fn:   return "TTToSemiLeptonic"
        if "ZGToLLG" in fn:            return "ZGToLLG"
        if "WGToLNuG" in fn:           return "WGToLNuG"
        if "WZTo3LNu" in fn:           return "WZTo3LNu"
        if "WZTo2Q2L" in fn:           return "WZTo2Q2L"
        if "ZZ" in fn:                 return "ZZ"
        if "GluGluToWW" in fn:         return "GluGluToWW"
        if "WWTo2L2Nu" in fn:          return "WWTo2L2Nu"
        if "GluGluHToWW" in fn or "Higgs" in fn: return "Higgs"
        return "Unknown" 

    #        WORKER FUNCTION 
    def processing_file(label, file_url, file_idx):
        import sys
        import os
        import time
        import awkward as ak
        import numpy as np
        import vector
        

        from hww_tools import (
            Config,
            Efficiency_data,
            Physics_selection,
            calculations,
            cuts,
            helper,
            json_validation,
            Plots_config  
        )
        
        # Register vector behavior
        vector.register_awkward()

        file_name = file_url.split('/')[-1] 
        is_data = (label == 'Data')
        specific_sample_key = get_sample_key(file_url)

        empty_cutflow = {stage: 0 for stage in cutflow_stages}
        
        def fill_histograms(stage_name, mask, weights_dict, 
                           masses, met_pt, dphis, ptlls,
                           mt_higgs, mt_l2_met, mjj,
                           leading_pt, subleading_pt):
            
            if not isinstance(mask, np.ndarray):
                mask = ak.to_numpy(mask)

            if np.sum(mask) == 0:
                return

            def masked(arr, flatten=False):
                sliced = arr[mask]
                if flatten:
                    sliced = ak.flatten(sliced)
                return ak.to_numpy(sliced)

            for syst in VARIATIONS:
                w_syst = weights_dict.get(syst, weights_dict['nominal'])
                w = masked(w_syst)

                stage_histograms[stage_name]['mass'][syst].fill(masked(masses), weight=w)
                stage_histograms[stage_name]['met'][syst].fill(masked(met_pt), weight=w)
                stage_histograms[stage_name]['dphi'][syst].fill(masked(dphis), weight=w)
                stage_histograms[stage_name]['ptll'][syst].fill(masked(ptlls), weight=w)
                stage_histograms[stage_name]['mt_higgs'][syst].fill(masked(mt_higgs), weight=w)
                stage_histograms[stage_name]['mt_l2_met'][syst].fill(masked(mt_l2_met), weight=w)
                stage_histograms[stage_name]['mjj'][syst].fill(masked(mjj), weight=w)
                stage_histograms[stage_name]['leading_pt'][syst].fill(masked(leading_pt), weight=w)
                stage_histograms[stage_name]['subleading_pt'][syst].fill(masked(subleading_pt), weight=w)
        
        #        Main Event Loop
        try:
            stage_histograms = initialize_stage_histograms(stage_names, variables_to_plots, VARIATIONS)
            
            cutflow = empty_cutflow.copy()
            weighted_cutflow = {stage: 0.0 for stage in cutflow_stages}
            
            max_file_retries = 3
            
            for file_attempt in range(max_file_retries):
                try:
                    for arrays in helper.load_events(file_url, batch_size= 1_000_000, is_data=is_data):
                        
                        cutflow['total'] += len(arrays)

                        if is_data:
                            base_weight = ak.ones_like(arrays.PuppiMET_pt, dtype=float)
                        elif specific_sample_key in sample_info_detailed:
                            info = sample_info_detailed[specific_sample_key]
                            scale_factor = (info['xsec'] * luminosity) / info['sum_genWeight']
                            base_weight = arrays.genWeight * scale_factor
                        else:
                            base_weight = ak.zeros_like(arrays.PuppiMET_pt, dtype=float)

                        # Initialize Dictionary of Weights
                        weights_dict = {v: base_weight for v in VARIATIONS}

                        # APPLY TRIGGER SF & UNCERTAINTY (MC ONLY) 
                        if not is_data:
                            weights_dict['nominal'] = weights_dict['nominal'] * Efficiency_data.TRIGGER_SF_VAL
                            weights_dict['trigger_up']   = weights_dict['trigger_up'] * (Efficiency_data.TRIGGER_SF_VAL + Efficiency_data.TRIGGER_SF_ERR)
                            weights_dict['trigger_down'] = weights_dict['trigger_down'] * (Efficiency_data.TRIGGER_SF_VAL - Efficiency_data.TRIGGER_SF_ERR)
                            
                            for var in ['ele_id_up', 'ele_id_down', 'mu_id_up', 'mu_id_down']:
                                weights_dict[var] = weights_dict[var] * Efficiency_data.TRIGGER_SF_VAL

                        weighted_cutflow['total'] += float(ak.sum(weights_dict['nominal']))
                        
                        #    JSON MASK (DATA ONLY)   
                        if is_data and golden_json_data is not None:
                            try:
                                json_mask = json_validation.apply_json_mask(arrays, golden_json_data, run_periods=run_periods)
                                n_events_after = int(ak.sum(json_mask))
                                cutflow['after_json'] += n_events_after
                                weighted_cutflow['after_json'] += float(ak.sum(weights_dict['nominal'][json_mask]))

                                if n_events_after == 0:
                                    continue

                                arrays = arrays[json_mask]
                                for k in weights_dict:
                                    weights_dict[k] = weights_dict[k][json_mask]
                            except Exception as e: 
                                print(f"Warning: JSON mask failed for {file_name}: {e}")
                        
                        #    LEPTON SELECTION   
                        tight_leptons, _, _ = Physics_selection.select_tight_leptons(arrays)
                        met = ak.zip({"pt": arrays.PuppiMET_pt, "phi": arrays.PuppiMET_phi})
                        
                        leading, subleading, emu_cutflow, met_selected = Physics_selection.select_e_mu_events(tight_leptons, met)
                        
                        if leading is None or len(leading) == 0:
                            continue

                        sorted_leptons = tight_leptons[ak.argsort(tight_leptons.pt, ascending=False)]
                        has_2lep = ak.num(sorted_leptons) == 2
                        events_2lep = sorted_leptons[has_2lep]
                        
                        if len(events_2lep) == 0:
                            continue
                        
                        lead_all = events_2lep[:, 0]
                        sublead_all = events_2lep[:, 1]
                        
                        mask_1e1mu = ((lead_all.flavor == 11) & (sublead_all.flavor == 13)) | \
                                     ((lead_all.flavor == 13) & (sublead_all.flavor == 11))
                        mask_charge = lead_all.charge * sublead_all.charge < 0
                        mask_pt = (lead_all.pt > 25) & (sublead_all.pt > 13)
                        
                        eta_leading = ((lead_all.flavor == 11) & (abs(lead_all.eta) < 2.5)) | \
                                      ((lead_all.flavor == 13) & (abs(lead_all.eta) < 2.4))

                        eta_subleading = ((sublead_all.flavor == 11) & (abs(sublead_all.eta) < 2.5)) | \
                                         ((sublead_all.flavor == 13) & (abs(sublead_all.eta) < 2.4))
                        
                        mask_eta = eta_leading & eta_subleading
                        
                        emu_mask_2lep = mask_1e1mu & mask_charge & mask_pt & mask_eta
                        
                        indices_2lep = ak.where(has_2lep)[0]
                        indices_selected = ak.to_numpy(indices_2lep[emu_mask_2lep])
                        
                        emu_mask_full = np.zeros(len(has_2lep), dtype=bool)
                        emu_mask_full[indices_selected] = True
                        
                        for k in weights_dict:
                            weights_dict[k] = weights_dict[k][emu_mask_full]

                        #    LEPTON SCALE FACTORS & UNCERTAINTIES  
                        if not is_data:
                            # 1. Prepare Electron SFs
                            is_lead_ele = (leading.flavor == 11)
                            ele_pt = ak.where(is_lead_ele, leading.pt, subleading.pt)
                            ele_eta = ak.where(is_lead_ele, leading.eta, subleading.eta)

                            # Get Nominal and Error
                            ele_sf_nom, ele_sf_err = helper.get_sf_with_uncertainty(ele_eta, ele_pt, Efficiency_data.ELECTRON_SF_DATA)

                            # 2. Prepare Muon SFs
                            is_lead_mu = (leading.flavor == 13)
                            mu_pt = ak.where(is_lead_mu, leading.pt, subleading.pt)
                            mu_eta = ak.where(is_lead_mu, leading.eta, subleading.eta)

                            mu_tight_nom, mu_tight_err = helper.get_sf_with_uncertainty(mu_eta, mu_pt, Efficiency_data.MUON_TIGHT_DATA)
                            mu_iso_nom, mu_iso_err = helper.get_sf_with_uncertainty(mu_eta, mu_pt, Efficiency_data.MUON_ISO_DATA)
                            
                            # Combined Muon Nominal
                            mu_sf_nom = mu_tight_nom * mu_iso_nom
                            
                            # Combined Muon Error
                            mu_sf_up = (mu_tight_nom + mu_tight_err) * (mu_iso_nom + mu_iso_err)
                            mu_sf_down = (mu_tight_nom - mu_tight_err) * (mu_iso_nom - mu_iso_err)
                            
                            # Electron Up/Down
                            ele_sf_up    = ele_sf_nom + ele_sf_err
                            ele_sf_down = ele_sf_nom - ele_sf_err

                            # 3. Apply to Weights
                            # Nominal
                            weights_dict['nominal'] = weights_dict['nominal'] * ele_sf_nom * mu_sf_nom
                            
                            # Trigger Variations
                            weights_dict['trigger_up']   = weights_dict['trigger_up'] * ele_sf_nom * mu_sf_nom
                            weights_dict['trigger_down'] = weights_dict['trigger_down'] * ele_sf_nom * mu_sf_nom
                            
                            # Electron Variations
                            weights_dict['ele_id_up']    = weights_dict['ele_id_up'] * ele_sf_up * mu_sf_nom
                            weights_dict['ele_id_down']  = weights_dict['ele_id_down'] * ele_sf_down * mu_sf_nom
                            
                            # Muon Variations
                            weights_dict['mu_id_up']     = weights_dict['mu_id_up'] * ele_sf_nom * mu_sf_up
                            weights_dict['mu_id_down']   = weights_dict['mu_id_down'] * ele_sf_nom * mu_sf_down
                        
                        cutflow['e_mu_preselection'] += len(leading)
                        weighted_cutflow['e_mu_preselection'] += float(ak.sum(weights_dict['nominal']))
                        
                        #    KINEMATICS & FILLING   
                        masses, ptlls, dphis, mt_higgs, mt_l2_met = calculations.cal_kinematic_var(
                            leading, subleading, met_selected
                        )
                        
                        mjj_before = ak.zeros_like(masses)
                        all_true = np.ones(len(masses), dtype=bool)
                        
                        fill_histograms(
                            'before_cuts', all_true, weights_dict,
                            masses, met_selected.pt, dphis, ptlls,
                            mt_higgs, mt_l2_met, mjj_before,
                            leading.pt, subleading.pt
                        )
                        
                        indices_emu = indices_selected
                        
                        n_jets_full, _, sorted_jets_full, isZeroJet_full, isOneJet_full, isTwoJet_full = Physics_selection.count_jets(
                            arrays, tight_leptons=tight_leptons
                        )
                        
                        mjj_full = calculations.calculate_mjj(sorted_jets_full)
                        mjj_selected = ak.fill_none(mjj_full[indices_emu], 0.0)
                        
                        global_cut_mask, _ = cuts.apply_global_cuts(
                            leading, subleading, met_selected, mt_higgs, mt_l2_met, ptlls, masses
                        )
                        bjet_veto_full, bjet_info_full = Physics_selection.apply_bjet_selections(arrays)
                        bjet_veto_selected = bjet_veto_full[indices_emu]
                        bjet_info_selected = {
                            key: value[indices_emu] for key, value in bjet_info_full.items()
                        }
                        
                        global_mask_selected = global_cut_mask & bjet_veto_selected
                        global_mask_np = ak.to_numpy(global_mask_selected)
                        
                        cutflow['global_cuts'] += int(np.sum(global_mask_np))
                        weighted_cutflow['global_cuts'] += float(ak.sum(weights_dict['nominal'][global_mask_np]))
                        
                        if np.sum(global_mask_np) == 0:
                            continue
                        
                        fill_histograms(
                            'global', global_mask_np, weights_dict,
                            masses, met_selected.pt, dphis, ptlls,
                            mt_higgs, mt_l2_met, mjj_selected,
                            leading.pt, subleading.pt
                        )
                        
                        # Jet categories
                        isZeroJet = ak.to_numpy(isZeroJet_full[indices_emu])
                        isOneJet = ak.to_numpy(isOneJet_full[indices_emu])
                        isTwoJet = ak.to_numpy(isTwoJet_full[indices_emu])

                        jet_categories = [
                            ('0jet', isZeroJet),
                            ('1jet', isOneJet),
                            ('2jet', isTwoJet)
                        ]
                        
                        for jet_name, jet_mask in jet_categories:
                            mask = global_mask_np & jet_mask
                            n_events = int(np.sum(mask))
                            cutflow[jet_name] += n_events
                            weighted_cutflow[jet_name] += float(ak.sum(weights_dict['nominal'][mask]))
                            
                            fill_histograms(
                                jet_name, mask, weights_dict,
                                masses, met_selected.pt, dphis, ptlls,
                                mt_higgs, mt_l2_met, mjj_selected,
                                leading.pt, subleading.pt
                            )
                        
                        # Signal and Control Regions
                        sr_regions = cuts.apply_signal_region_cuts(
                            leading, subleading, met_selected, masses, ptlls, mt_higgs,
                            mt_l2_met, isZeroJet_full[indices_emu], isOneJet_full[indices_emu],
                            isTwoJet_full[indices_emu], bjet_veto_selected, mjj_selected
                        )
                        
                        cr_regions = cuts.apply_control_region_cuts(
                            leading, subleading, met_selected, masses, ptlls, mt_higgs,
                            mt_l2_met, isZeroJet_full[indices_emu], isOneJet_full[indices_emu],
                            isTwoJet_full[indices_emu], bjet_info_selected, mjj_selected
                        )
                        
                        all_regions = {**sr_regions, **cr_regions}
                        
                        for region_name, region_mask in all_regions.items():
                            region_mask_np = ak.to_numpy(region_mask)
                            n_events = int(np.sum(region_mask_np))
                            cutflow[region_name] += n_events
                            weighted_cutflow[region_name] += float(ak.sum(weights_dict['nominal'][region_mask_np]))
                            
                            fill_histograms(
                                region_name, region_mask_np, weights_dict,
                                masses, met_selected.pt, dphis, ptlls,
                                mt_higgs, mt_l2_met, mjj_selected,
                                leading.pt, subleading.pt
                            )
                    
                    # Return results on success
                    return label, stage_histograms, cutflow, weighted_cutflow, None
                    
                except (OSError, IOError, ValueError) as e:
                    if file_attempt < max_file_retries - 1:
                        print(f"  {label}/{file_name}: {type(e).__name__} - Retry {file_attempt+1}/{max_file_retries}")
                        time.sleep(3)
                        continue
                    else: 
                        error_msg = f"{file_name}: {type(e).__name__} after {max_file_retries} attempts - {str(e)[:100]}"
                        return label, initialize_stage_histograms(stage_names, variables_to_plots, VARIATIONS), empty_cutflow, {s: 0.0 for s in cutflow_stages}, error_msg
                
                except Exception as e:
                    error_msg = f"{file_name}: {type(e).__name__} - {str(e)[:100]}"
                    return label, initialize_stage_histograms(stage_names, variables_to_plots, VARIATIONS), empty_cutflow, {s: 0.0 for s in cutflow_stages}, error_msg
            
            return label, stage_histograms, cutflow, weighted_cutflow, None
            
        except Exception as e:
            error_msg = f"{file_name}: Unexpected error - {str(e)[:100]}"
            
            try:
                fallback_hist = initialize_stage_histograms(stage_names, variables_to_plots, VARIATIONS)
            except:
                fallback_hist = None 
                
            return label, fallback_hist, empty_cutflow, {s: 0.0 for s in cutflow_stages}, error_msg

    return processing_file