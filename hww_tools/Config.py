"""
Config.py

This module defines the global configuration for the analysis.
It includes:
- Directory paths (Input, Output, Auxiliary)
- Project constants (Analysis names)
- Run periods and Golden JSON paths
"""

import sys
import os 
from pathlib import Path

#==============================================================================
# ALL DIRECTORIES AND PATH 
#==============================================================================

# BASE PATHS
HOME_DIR = Path(os.environ.get("HOME", "/home/cms-jovyan"))
PROJECT_NAME = "H-to-WW-NanoAOD-analysis"

# DERIVED PATHS
PROJECT_DIR = HOME_DIR / PROJECT_NAME
# ANALYSIS_DIR = PROJECT_DIR / "HWW_analysis"
DATASETS_DIR = PROJECT_DIR / "Datasets"
DATA_DIR = DATASETS_DIR / "DATA"
MC_DIR = DATASETS_DIR / "MC_samples"
AUX_DIR = PROJECT_DIR / "Auxillary_files"
OUTPUT_DIR = PROJECT_DIR / "Outputs"
PLOTS_DIR = OUTPUT_DIR / "Plots"
 
# JSON FILES
GOLDEN_JSON_PATH = AUX_DIR / "Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"

# RUN PERIODS
RUN_PERIODS_2016 = {
    'Run2016G': {'run_min': 278820, 'run_max': 280385},
    'Run2016H': {'run_min': 280919, 'run_max': 284044}
}
 
# PRINT CONFIGURATION
# print(f"HOME_DIR:        {HOME_DIR}")
# print(f"PROJECT_DIR:     {PROJECT_DIR}")
# print(f"DATA_DIR:        {DATA_DIR}")
# print(f"MC_DIR:          {MC_DIR}")
# print(f"AUX_DIR:         {AUX_DIR}")
# print(f"OUTPUT_DIR:      {OUTPUT_DIR}")
# print(f"PLOTS_DIR:       {PLOTS_DIR}")
# print(f"JSON exists:     {GOLDEN_JSON_PATH.exists()}")
# print(f"GOLDEN_JSON:     {GOLDEN_JSON_PATH}")