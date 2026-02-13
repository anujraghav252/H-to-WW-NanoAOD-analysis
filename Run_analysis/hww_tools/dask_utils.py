"""
dask_utils.py

This module handles Dask cluster connection and worker environment setup.
"""

import os
import shutil
from dask.distributed import Client

def get_client(url="tls://localhost:8786"):
    """
    Connects to the Dask scheduler and returns the client.
    """
    client = Client(url)
    return client

def prepare_workers(client, package_name="hww_tools"):
    """
    Zips the local package, uploads it to the Dask scheduler, 
    and verifies that workers can import it.
    """
    # 1. Zip the package
    # Assumes the package folder is in the current working directory
    cwd = os.getcwd()
    print(f"Zipping {package_name} from {cwd}...")
    shutil.make_archive(package_name, 'zip', cwd, package_name)
    
    # 2. Upload to cluster
    zip_filename = f"{package_name}.zip"
    print(f"Uploading {zip_filename} to cluster...")
    client.upload_file(zip_filename)
    print(f"Upload complete. Workers can now import {package_name}.")
    
    # 3. Verify imports on workers
    def verify_import_task():
        import sys
        import os
        try:
            import hww_tools
            return f"SUCCESS: Imported hww_tools from {hww_tools.__file__}"
        except ImportError as e:
            return f"FAILURE: {e}. CWD contents: {os.listdir('.')}"

    print("Verifying import on workers...")
    results = client.run(verify_import_task)
    for worker, result in results.items():
        print(f"  {worker}: {result}")