"""
cutflow_utils.py
Handles the formatting and saving of cutflow tables to CSV files.
"""

import csv
from . import Config

def get_cutflow_rows(cutflow_data, stage_info=None, sample_order=None):
    """
    Generates header and rows for the cutflow table.
    Returns the data as raw numbers (ints or floats).
    """
    # Use defaults from Config if not provided
    if stage_info is None:
        stage_info = Config.stage_info
    if sample_order is None:
        sample_order = Config.sample_order

    mc_samples = [s for s in sample_order if s != 'Data']
    stage_names = [s[1] for s in stage_info]
    stage_keys = [s[0] for s in stage_info]
    
    header = ['Sample'] + stage_names
    rows = []
    
    # 1. Fill rows for each sample
    for sample in sample_order:
        if sample not in cutflow_data: 
            continue
            
        row = [sample]
        for key in stage_keys:
            # For Data, 'total' often refers to 'after_json' in this workflow
            if sample == 'Data' and key == 'total':
                val = cutflow_data[sample].get('after_json', 0)
            else:
                val = cutflow_data[sample].get(key, 0)
            row.append(val)
        rows.append(row)

    # 2. Calculate Total MC row
    total_row = ['TOTAL (MC)']
    for idx, key in enumerate(stage_keys):
        # Summing the values for all MC samples
        total = sum(cutflow_data[s].get(key, 0) for s in mc_samples if s in cutflow_data)
        total_row.append(total)
    rows.append(total_row)
    
    return header, rows

def save_cutflows(cutflow_final, weighted_cutflow_final, output_dir):
    """
    Saves the Raw and Weighted cutflow tables to CSV files.
    - Raw events -> Cutflow_Raw.csv (Formatted as Integers, no scientific notation)
    - Weighted events -> Cutflow_scaled.csv (Formatted to 2 decimal places, no scientific notation)
    """
    
    # ---------------------------------------------------------
    # 1. Save Raw Events (Unweighted)
    # ---------------------------------------------------------
    header_raw, rows_raw = get_cutflow_rows(cutflow_final)
    raw_path = output_dir / "Cutflow_Raw.csv"
    
    # Format Raw numbers: Force 0 decimal places (Integer look)
    formatted_rows_raw = []
    for row in rows_raw:
        sample_name = row[0]
        # "{:.0f}" forces strict integer formatting (e.g., 100000 not 1e+05)
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
    if weighted_cutflow_final:
        header_w, rows_w = get_cutflow_rows(weighted_cutflow_final)
        weighted_path = output_dir / "Cutflow_scaled.csv"
        
        # Format Weighted numbers: Force 2 decimal places (Fixed point)
        formatted_rows_w = []
        for row in rows_w:
            sample_name = row[0]
            # "{:.2f}" forces 2 decimals and suppresses exponential notation
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