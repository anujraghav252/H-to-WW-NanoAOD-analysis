"""
dask_utils.py

This module handles the connection and environment setup for Dask distributed computing.
Because the analysis is run on a cluster (multiple worker nodes/containers), the workers 
need access to the local `hww_tools` package to execute the analysis functions. 

This module provides utilities to:
- Establish a connection to the Dask scheduler.
- Package the local `hww_tools` directory into a zip file.
- Upload this zip file to all Dask workers.
- Verify that the workers can successfully import the required modules.
"""

import os
import shutil
from dask.distributed import Client

def get_client(url="tls://localhost:8786"):
    """
    Connects to the Dask scheduler and returns the client object.
    
    Parameters
    ----------
    url : str, optional
        The address of the Dask scheduler. Defaults to "tls://localhost:8786" 
        
    Returns
    -------
    client : dask.distributed.Client
        The active client connected to the Dask cluster.
    """
    client = Client(url)
    return client

def prepare_workers(client, package_name="hww_tools"):
    """
    Prepares the Dask workers by distributing the local analysis code to them.
    
    This function creates a zip archive of the specified local package, 
    uploads it to the cluster, and runs a quick diagnostic task on every 
    worker to ensure they can import the package successfully.
    
    Parameters
    ----------
    client : dask.distributed.Client
        The active Dask client connected to the scheduler.
    package_name : str, optional
        The name of the local Python package directory to distribute. 
        Defaults to "hww_tools".
    """
    # ---------------------------------------------------------
    # 1. Zip the local package
    # ---------------------------------------------------------
    # Assumes the package folder is located in the current working directory.
    cwd = os.getcwd()
    print(f"Zipping {package_name} from {cwd}...")
    shutil.make_archive(package_name, 'zip', cwd, package_name)
    
    # ---------------------------------------------------------
    # 2. Upload to the Dask cluster
    # ---------------------------------------------------------
    # Send the zip file to the scheduler, which distributes it to the workers.
    # Dask automatically extracts uploaded zip files into the workers' PYTHONPATH.
    zip_filename = f"{package_name}.zip"
    print(f"Uploading {zip_filename} to cluster...")
    client.upload_file(zip_filename)
    print(f"Upload complete. Workers can now import {package_name}.")
    
    # ---------------------------------------------------------
    # 3. Verify imports on all workers
    # ---------------------------------------------------------
    def verify_import_task():
        """
        A small diagnostic task that runs on each worker independently.
        It attempts to import the package and returns the file path it was 
        loaded from, or an error message if the import fails.
        """
        import sys
        import os
        try:
            import hww_tools
            return f"SUCCESS: Imported hww_tools from {hww_tools.__file__}"
        except ImportError as e:
            # If it fails, list the current directory contents for debugging
            return f"FAILURE: {e}. CWD contents: {os.listdir('.')}"

    print("Verifying import on workers...")
    
    # client.run() executes the given function on EVERY connected worker
    # and returns a dictionary mapping worker addresses to their results.
    results = client.run(verify_import_task)
    
    # Print the diagnostic results from each worker
    for worker, result in results.items():
        print(f"  {worker}: {result}")