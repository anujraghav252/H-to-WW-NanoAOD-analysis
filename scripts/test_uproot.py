"""
Purpose:
--------
This script demonstrates how to access and read ROOT files remotely using `uproot` and perform a basic check 
by plotting the pseudorapidity (η) distribution of electrons. 

It is mainly intended as a quick test to verify:
1. Uproot installation and functionality.
2. Ability to access ROOT files via a remote EOS URL.
3. Basic event data retrieval from NanoAOD format.

Workflow:
---------
1. Import required libraries (`uproot`, `numpy`, `matplotlib`).
2. Open a ROOT file from a remote EOS URL.
3. Access the 'Events' tree inside the ROOT file.
4. Retrieve the `Electron_eta` branch as a NumPy array.
5. Flatten the jagged array (since each event can have multiple electrons).
6. Plot a histogram of the electron η distribution for verification.

Instructions:
-------------
- Make sure you have `uproot` (v5 or later), `numpy`, and `matplotlib` installed.
- Ensure you have network access to the CERN EOS server if using a remote file.
- This can be adapted for other branches or particle types by changing the branch name.
"""



import uproot
import matplotlib.pyplot as plt
import numpy as np


url = "root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v1/40000/751D5714-5507-6343-818A-5DB7797D6632.root"


file = uproot.open(url)


#call the tree
tree = file["Events"]

lep_eta = tree["Electron_eta"].array(library="np")

lep_eta = np.concatenate(lep_eta)

#plotting eta
plt.hist(lep_eta, bins=60, range=(-3,3), histtype="step", color="red", label="DY electrons eta")
plt.xlabel("η")
plt.ylabel("Events")
plt.legend()
plt.grid()
plt.show()

