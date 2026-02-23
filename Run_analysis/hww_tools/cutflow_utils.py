"""
cutflow_utils.py

This module handles the formatting and saving of cutflow tables.
A "cutflow" tracks how many events survive after each sequential analysis cut.
It is critical for verifying event yields and debugging selection criteria.

The module provides functions to:
- Parse nested cutflow dictionaries into standard table rows.
- Calculate total background (MC) yields.
- Save both Raw (unweighted) and Scaled (weighted) cutflows to CSV files.
"""

import csv
from . import Config

def get_cutflow_rows(cutflow_data, stage_info=None, sample_order=None):
    """
    Generates the header and rows for the cutflow table from raw tracking data.
    
    Parameters
    ----------
    cutflow_data : dict
        A nested dictionary containing event counts. 
        Format: { 'SampleName': { 'stage_name': count, ... }, ... }
    stage_info : list of tuples, optional
        Mapping of internal stage keys to display names. Defaults to Config.stage_info.
    sample_order : list of str, optional
        The order in which samples should appear as rows. Defaults to Config.sample_order.

    Returns
    -------
    header : list of str
        The column names for the table (Sample name + stage display names).
    rows : list of lists
        The table data containing numerical yields for each sample at each stage, 
        plus a final 'TOTAL (MC)' row summing all background/signal simulations.
    """
    # Use default configurations if none are provided
    if stage_info is None:
        stage_info = Config.stage_info
    if sample_order is None:
        sample_order = Config.sample_order

    # Separate Monte Carlo (simulation) samples from real Data
    mc_samples = [s for s in sample_order if s != 'Data']
    
    # Extract headers (display names) and keys (internal dictionary keys)
    stage_names = [s[1] for s in stage_info]
    stage_keys = [s[0] for s in stage_info]
    
    header = ['Sample'] + stage_names
    rows = []
    
    # ---------------------------------------------------------
    # 1. Fill rows for each individual sample
    # ---------------------------------------------------------
    for sample in sample_order:
        # Skip samples that weren't processed or have no data
        if sample not in cutflow_data: 
            continue
            
        row = [sample]
        for key in stage_keys:
            # SPECIAL HANDLING FOR DATA:
            # Real collision data has billions of events before the JSON filter.
            # We set the 'total' for Data to be the yield *after* the Golden JSON 
            # filter is applied, as events outside the JSON are physically unusable.
            if sample == 'Data' and key == 'total':
                val = cutflow_data[sample].get('after_json', 0)
            else:
                val = cutflow_data[sample].get(key, 0)
            row.append(val)
        rows.append(row)

    # ---------------------------------------------------------
    # 2. Calculate Total MC (Simulation) row
    # ---------------------------------------------------------
    # Sum up all Monte Carlo backgrounds and signals to compare against Data
    total_row = ['TOTAL (MC)']
    for idx, key in enumerate(stage_keys):
        total = sum(cutflow_data[s].get(key, 0) for s in mc_samples if s in cutflow_data)
        total_row.append(total)
    rows.append(total_row)
    
    return header, rows


def save_cutflows(cutflow_final, weighted_cutflow_final, output_dir):
    """
    Formats the raw numerical cutflow data and exports them as CSV files.
    
    This function handles string formatting to ensure the CSVs are readable
       
    Outputs:
    - Cutflow_Raw.csv: Exact integer counts of events.
    - Cutflow_scaled.csv: Event yields scaled by luminosity and cross-section.
    
    Parameters
    ----------
    cutflow_final : dict
        The unweighted event counts.
    weighted_cutflow_final : dict
        The scaled event yields (incorporating genWeights, scale factors, etc.).
    output_dir : pathlib.Path
        The directory where the CSV files will be saved.
    """
    
    # ---------------------------------------------------------
    # 1. Save Raw Events (Unweighted)
    # ---------------------------------------------------------
    header_raw, rows_raw = get_cutflow_rows(cutflow_final)
    raw_path = output_dir / "Cutflow_Raw.csv"
    
    formatted_rows_raw = []
    for row in rows_raw:
        sample_name = row[0]
        formatted = [sample_name] + [f"{float(val):.0f}" for val in row[1:]]
        formatted_rows_raw.append(formatted)
    
    try:
        with open(raw_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header_raw)
            writer.writerows(formatted_rows_raw)
        print(f"Saved Raw Cutflow to: {raw_path}")
    except Exception as e:
        print(f"Failed to save Raw CSV: {e}")

    # ---------------------------------------------------------
    # 2. Save Weighted Yields (Scaled)
    # ---------------------------------------------------------
    # Only process if weighted data exists
    if weighted_cutflow_final:
        header_w, rows_w = get_cutflow_rows(weighted_cutflow_final)
        weighted_path = output_dir / "Cutflow_scaled.csv"
        
        # Format Weighted numbers: Force exactly 2 decimal places.
        # This standardizes the table view and avoids long floating-point artifacts.
        formatted_rows_w = []
        for row in rows_w:
            sample_name = row[0]
            formatted = [sample_name] + [f"{float(val):.2f}" for val in row[1:]]
            formatted_rows_w.append(formatted)

        try:
            with open(weighted_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header_w)
                writer.writerows(formatted_rows_w)
            print(f"Saved Weighted Cutflow to: {weighted_path}")
        except Exception as e:
            print(f"Failed to save Weighted CSV: {e}")