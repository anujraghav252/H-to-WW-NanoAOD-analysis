"""
Config.py

This module defines the global configuration and constants for the this analysis.
It serves as the single source of truth for:
- Directory paths (Input datasets, Outputs, Auxiliary files, Plots)
- Project constants and definitions
- Data validation requirements (Run periods and Golden JSON paths)
- Standardized lists for samples, cutflow stages, and systematic variations

Importing this module allows other scripts to access consistent paths and configurations.
"""

import sys
import os 
from pathlib import Path

# ==============================================================================
# ALL DIRECTORIES AND PATHS
# ==============================================================================

# BASE PATHS
# Define the root environment. Defaults to the standard CMS open data container path 
# if the HOME environment variable is not set.
HOME_DIR = Path(os.environ.get("HOME", "/home/cms-jovyan"))

# Name of the main project repository/directory
PROJECT_NAME = "H-to-WW-NanoAOD-analysis"

# DERIVED PATHS
# These paths are dynamically built from the base paths to ensure the code 
# works regardless of where the repository is cloned, as long as PROJECT_NAME matches.
PROJECT_DIR = HOME_DIR / PROJECT_NAME

# Data input directories
DATASETS_DIR = PROJECT_DIR / "Datasets"
DATA_DIR = DATASETS_DIR / "DATA"              # Real collision data files
MC_DIR = DATASETS_DIR / "MC_samples"          # Monte Carlo simulation files

# Auxiliary and Output directories
AUX_DIR = PROJECT_DIR / "Auxillary_files"     # Scale factors, efficiencies, JSONs
OUTPUT_DIR = PROJECT_DIR / "Outputs"          # ROOT files, CSVs, and logs
PLOTS_DIR = OUTPUT_DIR / "Plots"              # Generated histograms and graphs
 
# ==============================================================================
# DATA VALIDATION CONFIGURATION
# ==============================================================================

# JSON FILES
# Path to the "Golden JSON" provided by CMS. This file contains the list of 
# certified runs and luminosity blocks where the detector was fully operational.
GOLDEN_JSON_PATH = AUX_DIR / "Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"

# RUN PERIODS
# Defines the specific data-taking periods analyzed in this project (2016 G and H).
# Used to filter data events that fall outside these specific run ranges.
RUN_PERIODS_2016 = {
    'Run2016G': {'run_min': 278820, 'run_max': 280385},
    'Run2016H': {'run_min': 280919, 'run_max': 284044}
}

# ==============================================================================
# ANALYSIS DEFINITIONS & STAGES
# ==============================================================================

# Sample order for printing (cutflow table)
# Defines the standardized order in which samples should appear in terminal outputs, 
# tables, and CSVs. Starts with Data, followed by Signal, then Backgrounds.
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

# Cutflow Stages
# Defines the sequential checkpoints used to track how many events survive 
# after each progressive selection cut.
cutflow_stages = [
    'total',              # Initial number of events
    'after_json',         # Events passing Golden JSON filter (Data only)
    'e_mu_preselection',  # Events with exactly 1 electron and 1 muon
    'global_cuts',        # Events passing global kinematic cuts (pt, MET, mass)
    '0jet', '1jet', '2jet', # Jet binning categories
    'SR_0jet', 'SR_1jet', 'SR_2jet',                         # Signal Regions
    'CR_top_0jet', 'CR_top_1jet', 'CR_top_2jet',             # Top Control Regions
    'CR_tau_0jet', 'CR_tau_1jet', 'CR_tau_2jet'              # Tau Control Regions
]

# Stage names for histogram initialization
# Defines the specific stages where full kinematic histograms are saved.
# Note: 'total' and 'after_json' are excluded here to save memory, as kinematics 
# are only plotted from 'before_cuts' onwards.
stage_names = [
    'before_cuts', 'global', '0jet', '1jet', '2jet',
    'SR_0jet', 'SR_1jet', 'SR_2jet',
    'CR_top_0jet', 'CR_top_1jet', 'CR_top_2jet',
    'CR_tau_0jet', 'CR_tau_1jet', 'CR_tau_2jet'
]

# Stage info mapping for Cutflow Tables
# Format: (internal_variable_name, display_name_for_tables)
# Used by cutflow_utils.py to generate human-readable column headers in CSVs.
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

# Systematic Variations
# List of systematic uncertainties evaluated in the analysis.
# 'nominal' is the central value. The others represent +/- 1 standard deviation 
# shifts for trigger efficiencies, electron ID, and muon ID scale factors.
VARIATIONS = [
    'nominal', 
    'trigger_up', 'trigger_down', 
    'ele_id_up', 'ele_id_down', 
    'mu_id_up', 'mu_id_down'
]