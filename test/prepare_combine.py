import uproot
import hist
import os
import numpy as np

# --- 1. CONFIGURATION (Matched to your Config.py) ---
INPUT_FILE = "HWW_analysis_output.root"
OUTPUT_ROOT = "combine_input.root"
OUTPUT_CARD = "hww_datacard.txt"

# variable to fit (Discriminant)
VAR_NAME = "mt_higgs" 

# Your Analysis Structure
PROCESSES = [
    "ggH_HWW",       # Signal (Index 0)
    "WW",            # Backgrounds...
    "Top_antitop",
    "DY_to_Tau_Tau",
    "Fakes",
    "ggWW",
    "Diboson",
    "VG"
]

# Map your analysis regions to simpler Datacard Channel names
# REMOVED DyCR (CR_tau_0jet)
REGIONS = {
    "SR_0jet":      "SR",
    "CR_top_0jet":  "TopCR"
}

# Map your variations to Combine Systematics (Name + Up/Down)
SYSTEMATICS = {
    "trigger": "CMS_trigger",
    "ele_id":  "CMS_eff_e",
    "mu_id":   "CMS_eff_m"
}

def main():
    print(f"Opening {INPUT_FILE}...")
    try:
        f_in = uproot.open(INPUT_FILE)
    except Exception as e:
        print(f"Error: Could not open input file. Make sure you run this from 'Run_analysis' folder. {e}")
        return

    f_out = uproot.recreate(OUTPUT_ROOT)
    
    # Store data for text card generation
    # Structure: rates[channel][process] = yield
    rates = {reg: {} for reg in REGIONS.values()}
    
    print("\n--- Harvesting Histograms ---")
    
    for internal_reg, card_reg in REGIONS.items():
        print(f"Processing Region: {internal_reg} -> {card_reg}")
        
        # 1. PROCESS DATA
        data_key = f"Data_{internal_reg}_{VAR_NAME}_nominal"
        if data_key in f_in:
            h_data = f_in[data_key].to_hist()
            # Save as: data_obs_Channel
            f_out[f"data_obs_{card_reg}"] = h_data
            print(f"  Saved Data: {h_data.sum().value:.0f} events")
        else:
            print(f"  WARNING: Data histogram {data_key} not found!")

        # 2. PROCESS SIGNAL & BACKGROUNDS
        for proc in PROCESSES:
            # A. Nominal
            nom_key = f"{proc}_{internal_reg}_{VAR_NAME}_nominal"
            
            if nom_key not in f_in:
                print(f"    Missing process: {proc} (skipping)")
                rates[card_reg][proc] = 0.0
                continue
                
            h_nom = f_in[nom_key].to_hist()
            
            # SANITIZE: Set slightly > 0 to avoid Combine crashes
            values = h_nom.view(flow=False).value
            values[values <= 0] = 1e-4
            h_nom.view(flow=False).value = values
            
            # Save Nominal: Process_Channel
            f_out[f"{proc}_{card_reg}"] = h_nom
            rates[card_reg][proc] = h_nom.sum().value
            
            # B. Systematics
            for internal_syst, combine_syst in SYSTEMATICS.items():
                up_key = f"{proc}_{internal_reg}_{VAR_NAME}_{internal_syst}_up"
                dn_key = f"{proc}_{internal_reg}_{VAR_NAME}_{internal_syst}_down"
                
                if up_key in f_in and dn_key in f_in:
                    h_up = f_in[up_key].to_hist()
                    h_dn = f_in[dn_key].to_hist()
                    
                    # Sanitize
                    h_up.view(flow=False).value[h_up.view(flow=False).value <= 0] = 1e-4
                    h_dn.view(flow=False).value[h_dn.view(flow=False).value <= 0] = 1e-4
                    
                    # Save: Process_Channel_SystUp
                    f_out[f"{proc}_{card_reg}_{combine_syst}Up"] = h_up
                    f_out[f"{proc}_{card_reg}_{combine_syst}Down"] = h_dn

    f_out.close()
    f_in.close()
    print(f"\nCreated ROOT file: {OUTPUT_ROOT}")
    
    # --- 3. GENERATE DATACARD ---
    create_datacard(rates)

def create_datacard(rates):
    card_content = []
    
    # Regions active in this card
    sorted_regions = ["SR", "TopCR"]

    # Header
    card_content.append(f"imax {len(sorted_regions)}  number of channels (SR, TopCR)")
    card_content.append(f"jmax {len(PROCESSES)-1}  number of backgrounds")
    card_content.append("kmax * number of nuisance parameters")
    card_content.append("-" * 30)
    
    # Shapes definition
    card_content.append(f"shapes * * {os.path.basename(OUTPUT_ROOT)} $PROCESS_$CHANNEL $PROCESS_$CHANNEL_$SYSTEMATIC")
    card_content.append("-" * 30)
    
    # Observation (Set to -1 to let Combine read from 'data_obs' histogram)
    # We build this string dynamically based on sorted_regions
    bin_line = f"{'bin':<15}"
    obs_line = f"{'observation':<15}"
    for reg in sorted_regions:
        bin_line += f"{reg:<15} "
        obs_line += f"{'-1':<15} "
    
    card_content.append(bin_line)
    card_content.append(obs_line)
    card_content.append("-" * 30)
    
    # Rates
    bin_line = f"{'bin':<15}"
    proc_name_line = f"{'process':<15}"
    proc_id_line = f"{'process':<15}"
    rate_line = f"{'rate':<15}"
    
    for reg in sorted_regions:
        for i, proc in enumerate(PROCESSES):
            bin_line += f"{reg:<15} "
            proc_name_line += f"{proc:<15} "
            # Signal (ggH_HWW) is 0, others are 1, 2, 3...
            pid = 0 if i == 0 else i
            proc_id_line += f"{pid:<15} "
            
            yield_val = rates[reg].get(proc, 0.0)
            rate_line += f"{yield_val:<15.4f} "
            
    card_content.append(bin_line)
    card_content.append(proc_name_line)
    card_content.append(proc_id_line)
    card_content.append(rate_line)
    card_content.append("-" * 30)
    
    # Systematics
    # 1. Luminosity (Log Normal - 2.5% uncertainty on all)
    # Applied to len(PROCESSES) * len(sorted_regions)
    card_content.append(f"{'lumi_13TeV':<15} {'lnN':<8} " + "1.025 " * (len(PROCESSES)*len(sorted_regions)))
    
    # 2. Shape Systematics
    for _, combine_name in SYSTEMATICS.items():
        line = f"{combine_name:<15} {'shape':<8} "
        for reg in sorted_regions:
            for proc in PROCESSES:
                # Check if process is likely to have this uncertainty
                # For simplicity, we apply "1" (active) to all MC. Data (not in loop) is ignored.
                line += "1.0 " if rates[reg].get(proc, 0) > 0 else "- "
        card_content.append(line)
        
    # 3. AutoMCStats
    card_content.append("* autoMCStats 0 1 1")

    with open(OUTPUT_CARD, "w") as f:
        f.write("\n".join(card_content))
        
    print(f"Created Datacard: {OUTPUT_CARD}")

if __name__ == "__main__":
    main()
