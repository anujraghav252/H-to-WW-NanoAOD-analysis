import uproot
import hist
import os
import numpy as np

INPUT_FILE = "Outputs/HWW_analysis_output.root"

# Variable to fit
VAR_NAME = "mt_higgs"  

PROCESSES = [
    "ggH_HWW",       # Signal (must be index 0)
    "WW",            # Backgrounds
    "Top_antitop",
    "DY_to_Tau_Tau",
    "Fakes",
    "ggWW",
    "Diboson",
    "VG"
]

# Mapping: Internal Name -> (Combine Bin Name, Output ROOT name, Output Card name)
# The bin names perfectly match the aliases from your combineCards.py command!
REGIONS_CONFIG = {
    "SR_0jet":     ("ggH_hww_0j", "Combine/combine_input_SR0j.root", "Combine/hww_sr0j_datacard.txt"),
    "SR_1jet":     ("ggH_hww_1j", "Combine/combine_input_SR1j.root", "Combine/hww_sr1j_datacard.txt"),
    "SR_2jet":     ("ggH_hww_2j", "Combine/combine_input_SR2j.root", "Combine/hww_sr2j_datacard.txt"),
    "CR_top_0jet": ("Top_0j",     "Combine/combine_input_topCR0j.root", "Combine/hww_topCR0j_datacard.txt"),
    "CR_top_1jet": ("TOP_1j",     "Combine/combine_input_topCR1j.root", "Combine/hww_topCR1j_datacard.txt"),
    "CR_top_2jet": ("TOP_2j",     "Combine/combine_input_topCR2j.root", "Combine/hww_topCR2j_datacard.txt")
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

    os.makedirs("Combine", exist_ok=True)
    
    print("\n-- Harvesting Histograms & Creating Datacards --")
    
    # LOOP OVER ALL 6 REGIONS
    for internal_reg, (card_reg, out_root, out_card) in REGIONS_CONFIG.items():
        print(f"\nProcessing Region: {internal_reg} -> {card_reg}")
        
        f_out = uproot.recreate(out_root)
        
        # Dictionaries scoped specifically for this region
        rates = {card_reg: {}}
        data_yields = {card_reg: 0.0} 
        
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
        print(f"  Created ROOT file: {out_root}")
        
        # Pass dynamic filenames to the datacard creator
        create_datacard(rates, data_yields, card_reg, out_root, out_card)

    f_in.close()
    print("\nSuccessfully generated all 6 datacards and ROOT files!")

def create_datacard(rates, data_yields, card_reg, out_root, out_card):
    card_content = []
    
    sorted_regions = [card_reg]

    card_content.append(f"imax {len(sorted_regions)}  number of channels ({card_reg})")
    card_content.append(f"jmax {len(PROCESSES)-1}  number of backgrounds")
    card_content.append("kmax * number of nuisance parameters")
    card_content.append("-" * 30)
    
    # Dynamically extract just the ROOT file name (e.g., 'combine_input_SR1j.root')
    root_filename = os.path.basename(out_root)
    card_content.append(f"shapes * * {root_filename} $PROCESS_$CHANNEL $PROCESS_$CHANNEL_$SYSTEMATIC")
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

    with open(out_card, "w") as f:
        f.write("\n".join(card_content))
        
    print(f"  Created Datacard: {out_card}")

if __name__ == "__main__":
    main()