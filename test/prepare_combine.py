import uproot
import hist
import os
import numpy as np

INPUT_FILE = "Outputs/HWW_analysis_output.root"
OUTPUT_ROOT = "Combine/combine_input_topCR2j.root"
OUTPUT_CARD = "Combine/hww_topCR2j_datacard.txt"

# Variable to fit
VAR_NAME = "mt_higgs"  

PROCESSES = [
    "ggH_HWW",       # Signal (must be index 0
    "WW",            # Backgrounds
    "Top_antitop",
    "DY_to_Tau_Tau",
    "Fakes",
    "ggWW",
    "Diboson",
    "VG"
]

# REGIONS = {
#     "SR_2jet": "SR_2j"
# }

REGIONS = {
    "CR_top_2jet": "TopCR_2J"
}

SYSTEMATICS = {
    "trigger": "CMS_trigger",
    "ele_id":  "CMS_eff_e",
    "mu_id":   "CMS_eff_m"
}

def main():
    print(f"Opening {INPUT_FILE}")
    try:
        f_in = uproot.open(INPUT_FILE)
    except Exception as e:
        print(f"Error: Could not open input file. {e}")
        return

    os.makedirs(os.path.dirname(OUTPUT_ROOT), exist_ok=True)
    f_out = uproot.recreate(OUTPUT_ROOT)
    
    # Dictionaries to store yields for the datacard
    rates = {reg: {} for reg in REGIONS.values()}
    data_yields = {reg: 0.0 for reg in REGIONS.values()} 
    
    print("\n-- Harvesting Histograms --")
    
    for internal_reg, card_reg in REGIONS.items():
        print(f"Processing Region: {internal_reg} -> {card_reg}")
        
        # 1. Process Data
        data_key = f"Data_{internal_reg}_{VAR_NAME}_nominal"
        if data_key in f_in:
            h_data = f_in[data_key].to_hist()
            f_out[f"data_obs_{card_reg}"] = h_data
            
            # Capture the exact data yield
            obs_yield = h_data.sum().value
            data_yields[card_reg] = obs_yield
            print(f"  Saved Data: {obs_yield:.0f} events")
        else:
            print(f"  WARNING: Data histogram {data_key} not found!")

        # 2. Process MC Processes
        for proc in PROCESSES:
            nom_key = f"{proc}_{internal_reg}_{VAR_NAME}_nominal"
            
            if nom_key not in f_in:
                print(f"    Missing process: {proc} (skipping)")
                rates[card_reg][proc] = 0.0
                continue
                
            h_nom = f_in[nom_key].to_hist()
            
            values = h_nom.view(flow=False).value
            values[values <= 0] = 1e-4
            h_nom.view(flow=False).value = values
            
            f_out[f"{proc}_{card_reg}"] = h_nom
            rates[card_reg][proc] = h_nom.sum().value
            
            # 3. Process Systematics
            for internal_syst, combine_syst in SYSTEMATICS.items():
                up_key = f"{proc}_{internal_reg}_{VAR_NAME}_{internal_syst}_up"
                dn_key = f"{proc}_{internal_reg}_{VAR_NAME}_{internal_syst}_down"
                
                if up_key in f_in and dn_key in f_in:
                    h_up = f_in[up_key].to_hist()
                    h_dn = f_in[dn_key].to_hist()
                    
                    h_up.view(flow=False).value[h_up.view(flow=False).value <= 0] = 1e-4
                    h_dn.view(flow=False).value[h_dn.view(flow=False).value <= 0] = 1e-4
                    
                    f_out[f"{proc}_{card_reg}_{combine_syst}Up"] = h_up
                    f_out[f"{proc}_{card_reg}_{combine_syst}Down"] = h_dn

    f_out.close()
    f_in.close()
    print(f"\nCreated ROOT file: {OUTPUT_ROOT}")
    
    # Pass the data_yields dictionary to the datacard creator
    create_datacard(rates, data_yields)

def create_datacard(rates, data_yields):
    card_content = []
    
    sorted_regions = ["TopCR_2J"]

    card_content.append(f"imax {len(sorted_regions)}  number of channels (TOP CR)")
    card_content.append(f"jmax {len(PROCESSES)-1}  number of backgrounds")
    card_content.append("kmax * number of nuisance parameters")
    card_content.append("-" * 30)
    
    card_content.append(f"shapes * * {os.path.basename(OUTPUT_ROOT)} $PROCESS_$CHANNEL $PROCESS_$CHANNEL_$SYSTEMATIC")
    card_content.append("-" * 30)
    
    bin_line = f"{'bin':<15}"
    obs_line = f"{'observation':<15}"
    
    # Write the explicit data yield to the observation line
    for reg in sorted_regions:
        bin_line += f"{reg:<15} "
        obs_line += f"{data_yields[reg]:<15.0f} " 
    
    card_content.append(bin_line)
    card_content.append(obs_line)
    card_content.append("-" * 30)
    
    bin_line = f"{'bin':<15}"
    proc_name_line = f"{'process':<15}"
    proc_id_line = f"{'process':<15}"
    rate_line = f"{'rate':<15}"
    
    for reg in sorted_regions:
        for i, proc in enumerate(PROCESSES):
            bin_line += f"{reg:<15} "
            proc_name_line += f"{proc:<15} "
            pid = 0 if i == 0 else i 
            proc_id_line += f"{pid:<15} "
            
            yield_val = rates[reg].get(proc, 0.0)
            rate_line += f"{yield_val:<15.4f} "
            
    card_content.append(bin_line)
    card_content.append(proc_name_line)
    card_content.append(proc_id_line)
    card_content.append(rate_line)
    card_content.append("-" * 30)
    
    card_content.append(f"{'lumi_13TeV':<15} {'lnN':<8} " + "1.012 " * (len(PROCESSES)*len(sorted_regions)))
    
    for _, combine_name in SYSTEMATICS.items():
        line = f"{combine_name:<15} {'shape':<8} "
        for reg in sorted_regions:
            for proc in PROCESSES:
                line += "1.0 " if rates[reg].get(proc, 0) > 0 else "- "
        card_content.append(line)
        
    card_content.append("* autoMCStats 0 1 1")

    with open(OUTPUT_CARD, "w") as f:
        f.write("\n".join(card_content))
        
    print(f"Created Datacard: {OUTPUT_CARD}")

if __name__ == "__main__":
    main()