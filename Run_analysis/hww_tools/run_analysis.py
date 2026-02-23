"""
run_analysis.py

This module handles the Dask distributed execution loop.
It takes the mapped processing task (defined in the main notebook) and 
orchestrates the submission, gathering, merging, and saving of results.
"""

import os
import time
import gc
from tqdm.auto import tqdm
from dask.distributed import as_completed

# Import local configurations
from . import Config
from . import Plots_config
from . import helper
from . import cutflow_utils

def execute_analysis(client, files, processing_task):
    """
    Executes the distributed analysis on the Dask cluster.
    
    Parameters
    ----------
    client : dask.distributed.Client
        The active Dask client.
    files : dict
        Dictionary of sample labels and their file URLs.
    processing_task : function
        The processor function initialized by make_processor() in the notebook.
        
    Returns
    -------
    hist_data_final, cutflow_final, weighted_cutflow_final
    """
    print("\n" + "="*70)
    print("PROCESSING START!! ")
    print(f"Output Directory: {Config.OUTPUT_DIR}")
    print("="*70)

    # 1. PREPARE ACCUMULATORS
    print("Initializing storage...")
    stage_names = Config.stage_names
    cutflow_stages = Config.cutflow_stages
    VARIATIONS = Config.VARIATIONS
    variables_to_plots = Plots_config.variables_to_plots

    hist_data_final = {}
    cutflow_final = {}
    weighted_cutflow_final = {}

    for label in files.keys():
        hist_data_final[label] = helper.initialize_stage_histograms(stage_names, variables_to_plots, VARIATIONS)
        cutflow_final[label] = {stage: 0 for stage in cutflow_stages}
        weighted_cutflow_final[label] = {stage: 0.0 for stage in cutflow_stages}

    # 2. SUBMIT TO CLUSTER
    arg_labels = []
    arg_urls = []
    arg_indices = []

    for label, urls in files.items():
        for file_idx, file_url in enumerate(urls):
            arg_labels.append(label)
            arg_urls.append(file_url)
            arg_indices.append(file_idx)

    print(f"\nSubmitting {len(arg_urls)} files to the cluster...")
    start_time = time.perf_counter()

    # Map the processing task provided by the notebook
    futures = client.map(
        processing_task, 
        arg_labels, arg_urls, arg_indices,
        retries=1  
    )

    # 3. STREAMING MERGE LOOP
    print("Processing and merging results as they arrive...")
    error_count = 0

    for future in tqdm(as_completed(futures), total=len(futures), unit="file"):
        try:
            result = future.result()
            if not result: continue
            
            label, stage_histograms, cutflow, weighted_cutflow, error = result
            
            if error:
                error_count += 1
                print(f" ERROR: {error}")
                continue

            # A. Merge Cutflows
            if cutflow:
                for stage, count in cutflow.items():
                    cutflow_final[label][stage] += count
            
            if weighted_cutflow:
                for stage, count in weighted_cutflow.items():
                    weighted_cutflow_final[label][stage] += count
            
            # B. Merge Histograms
            if stage_histograms:
                for stage, vars_dict in stage_histograms.items():
                    for var, syst_dict in vars_dict.items():
                        for syst, hist_obj in syst_dict.items():
                            hist_data_final[label][stage][var][syst] += hist_obj
            
            del result, stage_histograms, cutflow, weighted_cutflow

        except Exception as e:
            print(f"CRITICAL CLIENT ERROR: {e}")
            error_count += 1

    elapsed = time.perf_counter() - start_time

    # 4. SAVE RESULTS 
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    helper.save_root_file(hist_data_final, Config.OUTPUT_DIR / "HWW_analysis_output.root")
    cutflow_utils.save_cutflows(cutflow_final, weighted_cutflow_final, Config.OUTPUT_DIR)

    # 5. FINAL REPORT
    print("\n" + "="*70)
    print(f"{'SAMPLE':20s} | {'EVENTS':>12s}")
    print("-" * 35)
    total_events = 0
    for label in sorted(files.keys()):
        events = cutflow_final[label].get('total', 0)
        total_events += events
        print(f"{label:20s} | {events:>12,}")
    print("-" * 35)
    print(f"{'TOTAL':20s} | {total_events:>12,}")
    print("="*70)

    if error_count > 0:
        print(f"\n WARNING: {error_count} files failed processing.")

    print(f"\nTotal Time: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    if len(futures) > 0:
        print(f"Rate: {total_events/elapsed:,.0f} events/sec")

    del futures, arg_urls, arg_labels, arg_indices
    gc.collect()
    
    return hist_data_final, cutflow_final, weighted_cutflow_final