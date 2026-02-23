"""
cross_section.py

This module contains the cross-section and luminosity information required 
to normalize Monte Carlo (MC) simulation events to the recorded data.

The values here are used to calculate the global event scaling factor for each MC sample.
This ensures that the predicted number of background and signal events 
matches the expected yield for the given data-taking period.
"""

# ==============================================================================
# INTEGRATED LUMINOSITY
# ==============================================================================
# The total integrated luminosity of the dataset being analyzed.
# Value is in inverse picobarns (pb^-1). 16,150.0 pb^-1 corresponds to 16.15 fb^-1,
# which represents a specific data-taking period (e.g., partial 2016 dataset- 2016G and 2016H).
LUMINOSITY = 16_150.0 

# ==============================================================================
# MONTE CARLO SAMPLE METADATA
# ==============================================================================
# Dictionary mapping the internal MC sample names to their physical properties.
# - 'xsec': The theoretical cross-section of the process in picobarns (pb).
# - 'sum_genWeight': The sum of all generator-level weights for the entire 
#                    generated sample (before any analysis cuts are applied).
sample_info_detailed = {
    # --------------------------------------------------------------------------
    # DRELL-YAN (Z/gamma* -> leptons)
    # --------------------------------------------------------------------------
    "DYJetsToLL_M-50":      { "xsec": 6189.39, "sum_genWeight": 82448537.0 },
    
    # --------------------------------------------------------------------------
    # TOP QUARK (Pair production and Single Top)
    # --------------------------------------------------------------------------
    "TTTo2L2Nu":            { "xsec": 87.31, "sum_genWeight": 3140127171.4748 },
    "ST_t-channel_top":     { "xsec": 44.33, "sum_genWeight": 6703802049.126 },
    "ST_t-channel_antitop": { "xsec": 26.38, "sum_genWeight": 1522100315.652 },
    "ST_tW_top":            { "xsec": 35.60, "sum_genWeight": 20635251.1008 },
    "ST_tW_antitop":        { "xsec": 35.60, "sum_genWeight": 27306324.658 },
    "ST_s-channel":         { "xsec": 3.36,  "sum_genWeight": 19429336.179 },
    
    # --------------------------------------------------------------------------
    # FAKES (Processes where a jet or photon is misidentified as a lepton)
    # --------------------------------------------------------------------------
    "WJetsToLNu":           { "xsec": 61526.7, "sum_genWeight": 9697410121705.164 },
    "TTToSemiLeptonic":     { "xsec": 364.35,  "sum_genWeight": 43548253725.284 },
    
    # --------------------------------------------------------------------------
    # V+GAMMA (Vector boson + photon)
    # --------------------------------------------------------------------------
    "ZGToLLG":              { "xsec": 58.83,   "sum_genWeight": 3106465270.711 },
    "WGToLNuG":             { "xsec": 405.271, "sum_genWeight": 3353413.0 },
    
    # --------------------------------------------------------------------------
    # DIBOSON (Production of two weak vector bosons)
    # --------------------------------------------------------------------------
    "WZTo3LNu":             { "xsec": 4.42965, "sum_genWeight": 4077550.6318 },
    "WZTo2Q2L":             { "xsec": 5.595,   "sum_genWeight": 129756627.882 },
    "ZZ":                   { "xsec": 16.523,  "sum_genWeight": 1151000.0 },
    
    # --------------------------------------------------------------------------
    # SIGNAL & IRREDUCIBLE BACKGROUNDS
    # --------------------------------------------------------------------------
    # GluGluToWW: Non-resonant WW production via gluon fusion (background)
    "GluGluToWW":           { "xsec": 0.06387, "sum_genWeight": 17662000.0 },
    # WWTo2L2Nu: WW pair production (dominant irreducible background)
    "WWTo2L2Nu":            { "xsec": 12.178,  "sum_genWeight": 32147079.595 },
    # Higgs: The main H -> WW signal process
    "Higgs":                { "xsec": 1.0315,  "sum_genWeight": 63281816.82 }
}