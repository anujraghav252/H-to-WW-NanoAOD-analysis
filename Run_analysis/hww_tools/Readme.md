# hww_tools - Analysis Toolkit

Welcome to the `hww_tools` directory! This is the custom Python package powering our $H \to WW \to 2\ell 2\nu$ NanoAOD analysis. 

Instead of writing one massive, unreadable script, we broke the analysis logic down into modular files. This toolkit handles everything from applying trigger scale factors and calculating transverse masses, to orchestrating the Dask cluster and generating publication-ready plots. 

If you are looking for a specific function or variable, here is a breakdown of what lives in each file.

---

## Directory Contents

To make it easy to navigate, the modules are grouped below by their core job.

### 1. Configuration & Constants
These files act as the "source of truth" for the analysis. They don't really have functions; they just hold the dictionaries, lists, and numbers we need everywhere else. If you need to update a file path or a scale factor, you do it here.

* **`Config.py`**: Defines base directory paths, dataset locations, run periods, and the standard order of cutflow stages and systematic variations.
* **`cross_section.py`**: Contains the integrated luminosity for the era (`LUMINOSITY`) and a dictionary (`sample_info_detailed`) mapping all Monte Carlo samples to their theoretical cross-sections and generator weights.
* **`Efficiency_data.py`**: Holds the raw lookup tables for Data/MC corrections, including trigger efficiencies, electron ID, and muon ID/Isolation scale factors.

### 2. Physics & Kinematics
These modules do the actual scientific heavy lifting. They contain the functions that operate on the awkward arrays of particles to select objects, calculate physics variables, and apply our masks.

* **`Physics_selection.py`**: Handles object selection and filtering.
  * `select_tight_leptons`: Filters out loose/fake leptons based on ID and isolation.
  * `select_e_mu_events`: Finds the leading and subleading leptons and checks MET.
  * `count_jets`: Cleans jets against leptons and counts them.
  * `apply_bjet_selections`: Applies DeepJet b-tagging algorithms.
* **`calculations.py`**: Performs 4-vector kinematics using the vector package.
  * `wrap_angle_to_pi`: Normalizes angles for Delta Phi calculations.
  * `create_lepton_vector`: Converts awkward records to 4-momentum vectors.
  * `cal_kinematic_var`: Calculates basic kinematics like dilepton pT, Delta Phi, and transverse masses (like Higgs mT).
  * `calculate_mjj` and `apply_mjj_window`: Calculates dijet invariant mass for the 2-jet bin.
* **`cuts.py`**: Defines the boolean masks used to segment the events.
  * `apply_global_cuts`: Baseline cuts like MET > 20 and m_ll > 12.
  * `apply_signal_region_cuts`: Splits the Signal Region into 0, 1, and 2-jet bins.
  * `apply_control_region_cuts`: Defines the Top and Tau Control Regions.
* **`json_validation.py`**: Handles good-run filtering.
  * `apply_json_mask`: Applies the CMS Golden JSON to filter out bad collision data.

### 3. Execution & Orchestration
These files manage how the code actually runs, particularly distributing the heavy tasks across the computing cluster.

* **`dask_utils.py`**: Manages the Dask cluster connection.
  * `get_client`: Hooks up to the local or distributed scheduler.
  * `prepare_workers`: Zips up this entire `hww_tools` directory and ships it to the worker nodes so they have the latest code.
* **`run_analysis.py`**: The cluster manager.
  * `execute_analysis`: Takes the event-loop logic defined in your main notebook and distributes it via Dask. It handles the streaming progress bar and merges the dictionaries as results come back.
* **`helper.py`**: General utilities used throughout the processing loop.
  * `get_sample_key`: Maps complicated root filenames to our simple sample names.
  * `load_events`: Opens the ROOT files via uproot in manageable chunks.
  * `get_sf_with_uncertainty`: Queries our efficiency tables to grab the right scale factor for a given lepton.
  * `initialize_stage_histograms`, `save_root_file`, and `get_histogram_data`: Utilities for managing our massive nested histogram dictionaries.

### 4. Outputs & Visualization
Once the math is done, these modules make the results human-readable.

* **`Plots_config.py`**: The styling hub for matplotlib. Like the config files, it doesn't have functions, just dictionaries defining the color palette for backgrounds, axis limits, LaTeX variable labels, and stack orders.
* **`plotting.py`**: The plotting engine using mplhep.
  * `create_stacked_plots`: Generates CMS-styled stacked Data/MC plots, complete with ratio panels and uncertainty bands.
  * `create_superimposed_plots`: Generates normalized shape plots to compare signal vs background distributions.
* **`cutflow_utils.py`**: Formats the event counts into clean tables.
  * `get_cutflow_rows`: Parses our nested cutflow dictionaries into standard table rows.
  * `save_cutflows`: Dumps the raw and scaled event counts into CSV files.

---

## Where is everything saved?

Because this analysis processes hundreds of gigabytes of data, we keep the outputs completely separate from the codebase. Everything generated by this toolkit is automatically routed to the **Outputs/** directory located at the root of the project.

After running the analysis, you will find:
1. **`HWW_analysis_output.root`**: The master ROOT file containing every generated histogram for every sample, stage, variable, and systematic variation.
2. **`Cutflow_Raw.csv`**: A spreadsheet of the exact integer counts of events passing each stage.
3. **`Cutflow_scaled.csv`**: The physics-weighted cutflow spreadsheet (scaled by luminosity, cross-section, and scale factors).
4. **`Plots/`**: A subdirectory populated with the PNG files generated by the plotting script.

---

## How it interacts with the Main Notebook?

You might notice that the actual event loop (the thing that loops through events and says) is missing from this directory. 

By design, the core event loop is kept directly inside the main `Run_analysis.ipynb` notebook. This allows you to easily read, tweak, and debug the specific order of the physics cuts without having to dig through hidden files. The notebook acts as the brain that decides what to do, while this `hww_tools` directory acts as the muscle that provides the math functions and cluster management to get it done!