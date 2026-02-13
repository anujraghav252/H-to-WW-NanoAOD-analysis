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

# Sample order for printing (cutflow table)
sample_order = [
    'Data',
    'ggH_HWW',
    'WW',
    'Top_antitop',
    'DY_to_Tau_Tau',
    'Fakes',
    'ggWW',
    'Diboson',
    'VG',
]

cutflow_stages = [
    'total', 'after_json', 'e_mu_preselection', 'global_cuts',
    '0jet', '1jet', '2jet',
    'SR_0jet', 'SR_1jet', 'SR_2jet',
    'CR_top_0jet', 'CR_top_1jet', 'CR_top_2jet',
    'CR_tau_0jet', 'CR_tau_1jet', 'CR_tau_2jet'
]

# Stage names for histogram initialization
stage_names = [
    'before_cuts', 'global', '0jet', '1jet', '2jet',
    'SR_0jet', 'SR_1jet', 'SR_2jet',
    'CR_top_0jet', 'CR_top_1jet', 'CR_top_2jet',
    'CR_tau_0jet', 'CR_tau_1jet', 'CR_tau_2jet'
]

# Stage info: (internal_name, display_name) for cutflow table
stage_info = [
    ('total', 'Total'),
    ('e_mu_preselection', 'e-μ Preselect'),
    ('global_cuts', 'Global Cuts'),
    ('0jet', '0-jet'),
    ('1jet', '1-jet'),
    ('2jet', '2-jet'),
    ('SR_0jet', 'SR 0j'),
    ('SR_1jet', 'SR 1j'),
    ('SR_2jet', 'SR 2j'),
    ('CR_top_0jet', 'CR Top 0j'),
    ('CR_top_1jet', 'CR Top 1j'),
    ('CR_top_2jet', 'CR Top 2j'),
    ('CR_tau_0jet', 'CR Tau 0j'),
    ('CR_tau_1jet', 'CR Tau 1j'),
    ('CR_tau_2jet', 'CR Tau 2j'),
]

VARIATIONS = ['nominal', 'trigger_up', 'trigger_down', 'ele_id_up', 'ele_id_down', 'mu_id_up', 'mu_id_down']
