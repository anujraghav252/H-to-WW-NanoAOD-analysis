"""
helper.py

This module contains utility functions for data loading and handling.
It includes:
- Parsing text files for XRootD URLs
- Loading event arrays from ROOT files using Uproot
- Scale factor application with uncertainty
- Histogram data extraction helper
"""

import os
import time
import uproot
import awkward as ak
import numpy as np
import hist

SAMPLE_MAPPING = {
    'data': 'Data',
    'higgs': 'ggH_HWW',
    'dytoll': 'DY_to_Tau_Tau',
    'top': 'Top_antitop',
    'fakes': 'Fakes',
    'vz': 'Diboson',
    'ggww': 'ggWW',
    'ww': 'WW',
    'vg': 'VG'
}

# function to load urls from text files
def load_urls_from_file(filepath, max_files=None):
    """Load XRootD URLs from text file"""
    urls = []
    if not os.path.exists(filepath):
        return urls
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and line.startswith('root://'):
                urls.append(line)
                if max_files and len(urls) >= max_files:
                    break
    return urls

def load_all_files(data_dir, mc_dir, max_per_sample=None):
    """Load all file URLs from directories"""
    
    files_dict = {}
    
    for directory in [data_dir, mc_dir]:
        if not os.path.exists(directory):
            continue
        for filename in os.listdir(directory):
            if not filename.endswith(('.txt')):
                continue
            filepath = os.path.join(directory, filename)
            filename_lower = filename.lower().replace('.txt', '')
            # Find label
            label = None
            for pattern, sample_label in SAMPLE_MAPPING.items():
                if pattern in filename_lower:
                    label = sample_label
                    break          
            if not label:
                print(f"   Unknown file: {filename} - skipping")
                continue
            
            # Load URLs
            urls = load_urls_from_file(filepath, max_per_sample)
            
            if urls:
                if label in files_dict:
                    files_dict[label].extend(urls)
                else:
                    files_dict[label] = urls
    
    return files_dict

def samples_to_process(files_dict):
    """
    Prints a formatted summary table of the files to be processed.
    Pass "files"dictionary as the arguement 
    """
    print("\n" + "="*70)
    print("FILES TO PROCESS")
    print("="*70)
    total = 0
    for label, urls in files_dict.items():
        print(f"{label:20s}: {len(urls):4d} files")
        total += len(urls)
    print("_"*70)
    print(f"{'TOTAL':20s}: {total:4d} files")
    print("="*70)

# Loading branches from root files
def load_events(file_url, batch_size= 1_000_000, timeout=600, max_retries=3, retry_wait=10, is_data = False):

    columns = [
        "Electron_pt", "Electron_eta", "Electron_phi", "Electron_mass", 
        "Electron_mvaFall17V2Iso_WP90", "Electron_charge",
        
        "Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", 
        "Muon_tightId", "Muon_charge", "Muon_pfRelIso04_all",
        "PuppiMET_pt", "PuppiMET_phi",
        
        "Jet_pt", "Jet_eta", "Jet_phi", "Jet_mass",
        "Jet_btagDeepFlavB", "nJet", "Jet_jetId", "Jet_puId",
    ]

    if is_data:
        columns.extend(["run","luminosityBlock"])
    else: columns.append("genWeight")
        
    for attempt in range(max_retries):
        try:
            
            with uproot.open(file_url, timeout=timeout) as f:
                tree = f['Events']
                
                
                for arrays in tree.iterate(columns, step_size=batch_size, library="ak"):
                    yield arrays
                
                return
                
        except (TimeoutError, OSError, IOError, ConnectionError) as e:
            error_type = type(e).__name__
            file_name = file_url.split('/')[-1]
            
            if attempt < max_retries - 1:
                print(f"      {error_type} on {file_name}")
                print(f"       Retry {attempt+1}/{max_retries-1} in {retry_wait}s...")
                time.sleep(retry_wait)
            else:
                print(f"     FAILED after {max_retries} attempts: {file_name}")
                print(f"       Error: {str(e)[:100]}")
                raise
                
        except Exception as e:
            
            file_name = file_url.split('/')[-1]
            print(f"     Unexpected error on {file_name}: {str(e)[:100]}")
            raise

def initialize_stage_histograms(stages_list, vars_dict, variations_list):
    stage_histograms = {}
    for stage in stages_list:
        stage_histograms[stage] = {}
        for var_name, axis in vars_dict.items():
            stage_histograms[stage][var_name] = {}
            for syst in variations_list:
                stage_histograms[stage][var_name][syst] = hist.Hist(axis, storage=hist.storage.Weight())
    return stage_histograms

def get_sf_with_uncertainty(eta_array, pt_array, lookup_table):
    sf_out = ak.ones_like(eta_array, dtype=float)
    err_out = ak.zeros_like(eta_array, dtype=float)
    
    eta_abs = abs(eta_array)
    
    for (eta_min, eta_max, pt_min, pt_max, sf_val, err_val) in lookup_table:
        mask = (eta_abs >= eta_min) & (eta_abs < eta_max) & \
               (pt_array >= pt_min) & (pt_array < pt_max)
        
        sf_out = ak.where(mask, sf_val, sf_out)
        err_out = ak.where(mask, err_val, err_out)
        
    return sf_out, err_out

def get_histogram_data(hist_data, sample, stage, variable, variation='nominal'):
    if sample not in hist_data: return None, None, None
    if stage not in hist_data[sample]: return None, None, None
    if variable not in hist_data[sample][stage]: return None, None, None
    
    vars_dict = hist_data[sample][stage][variable]
    if variation not in vars_dict: return None, None, None
        
    h = vars_dict[variation]
    
    try:
        return h.values(), h.variances(), h.axes[0].edges
    except:
        return None, None, None 

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

def merge_dask_results(results, arg_urls, files_dict, stage_names, cutflow_stages, vars_dict, variations):
    """
    Merges results from Dask workers into final aggregated dictionaries.
    Handles initialization of empty histograms and cutflows.
    """
    # 1. Initialize final storage
    hist_final = {}
    cutflow_final = {}
    weighted_cutflow_final = {}
    
    # Create structure for all samples (even those not processed yet)
    for label in files_dict.keys():
        hist_final[label] = initialize_stage_histograms(stage_names, vars_dict, variations)
        cutflow_final[label] = {stage: 0 for stage in cutflow_stages}
        weighted_cutflow_final[label] = {stage: 0.0 for stage in cutflow_stages}

    error_count = 0
    
    # 2. Iterate through results
    for task_idx, result in enumerate(results):
        if not result: continue # Skip empty/failed results that return None
        
        # Unpack result tuple from processor
        label, stage_histograms, cutflow, weighted_cutflow, error = result
        
        # Handle Errors
        if error:
            error_count += 1
            file_url = arg_urls[task_idx]
            file_name = file_url.split('/')[-1]
            print(f" ERROR in {label}/{file_name}")
            print(f"    Reason: {error}")
            continue

        # A. Merge Cutflows
        if cutflow:
            for stage, count in cutflow.items():
                if stage in cutflow_final[label]:
                    cutflow_final[label][stage] += count
        
        if weighted_cutflow:
            for stage, count in weighted_cutflow.items():
                if stage in weighted_cutflow_final[label]:
                    weighted_cutflow_final[label][stage] += count
        
        # B. Merge Histograms
        if stage_histograms:
            for stage, vars_dict_res in stage_histograms.items():
                for var, systs in vars_dict_res.items():
                    for syst, hist_obj in systs.items():
                        # Efficiently add histogram objects
                        hist_final[label][stage][var][syst] += hist_obj
                        
    return hist_final, cutflow_final, weighted_cutflow_final, error_count

def save_root_file(hist_data, output_path):
    """
    Saves the nested dictionary of histograms to a ROOT file using Uproot.
    Structure: Sample_Stage_Variable_Variation
    """
    import uproot
    print(f"\nSaving histograms to ROOT file: {output_path.name}...")
    try:
        with uproot.recreate(output_path) as root_file:
            for sample, stages in hist_data.items():
                for stage, variables in stages.items():
                    for var_name, variations in variables.items():
                        for syst_name, hist_obj in variations.items():
                            
                            # Create distinct name
                            hist_name = f"{sample}_{stage}_{var_name}_{syst_name}"
                            hist_name = hist_name.replace(" ", "_").replace("-", "_")
                            
                            # Write to file
                            root_file[hist_name] = hist_obj
                            
        print("  Success! ROOT file saved.")
    except Exception as e:
        print(f"  Error saving ROOT file: {e}")

# Append to Run_analysis/hww_tools/helper.py

def restore_histograms(sample_list, stage_names, vars_dict, variations, root_file_path):
    """
    Reconstructs the full nested dictionary of histograms from a saved ROOT file.
    
    Parameters
    ----------
    sample_list : list
        List of sample names (e.g., files.keys()) to initialize.
    stage_names : list
        List of analysis stages (e.g., Config.stage_names).
    vars_dict : dict
        Dictionary of variables (e.g., Plots_config.variables_to_plots).
    variations : list
        List of systematic variations (e.g., Config.VARIATIONS).
    root_file_path : str or Path
        Path to the .root file.

    Returns
    -------
    dict
        The fully populated hist_data dictionary.
    """
    import uproot
    from pathlib import Path
    
    path = Path(root_file_path)
    if not path.exists():
        print(f"CRITICAL: ROOT file not found at {path}")
        return {}

    print(f"Restoring histograms from: {path.name}")
    
    hist_data = {}
    
    # Open file once
    with uproot.open(path) as file:
        # Loop through known structure to find matching keys
        for sample in sample_list:
            # 1. Initialize empty structure for this sample
            hist_data[sample] = initialize_stage_histograms(stage_names, vars_dict, variations)
            
            # 2. Fill with data from ROOT file
            for stage in stage_names:
                for var in vars_dict.keys():
                    for syst in variations:
                        # Reconstruct the key name used during saving
                        # Format: Sample_Stage_Variable_Variation
                        hist_name = f"{sample}_{stage}_{var}_{syst}"
                        hist_name = hist_name.replace(" ", "_").replace("-", "_")
                        
                        if hist_name in file:
                            # .to_hist() converts Uproot object back to boost_histogram
                            hist_data[sample][stage][var][syst] = file[hist_name].to_hist()
                            
    print(f"Successfully restored data for {len(hist_data)} samples.")
    return hist_data