#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import json
import sys

# Get arguments, input json file, and filename for output
# Parse Command Line
print ('Usage: mriqc_json2csv.py mriqc_json_file csv_output_file')
print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

json_file = sys.argv[1]
csv_file = sys.argv[2]

# Input jason file
# json_file = 'sub-0051607_T1w.json'

# Read the .json file into a dictionary
try:
    with open(json_file, 'r') as f:
            data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Error: JSON file not found at '{json_file_path}'")
except json.JSONDecodeError:
    raise json.JSONDecodeError("Error: Invalid JSON format in the file.", doc=data, pos=0)

# Setup the remove_keys() function
def remove_keys(my_dict, keys_to_remove):
  """Removes multiple keys from a dictionary.

    Args:
        my_dict (dict): The dictionary to remove keys from.
        keys_to_remove (list): A list of keys to remove.
  """
  for key in keys_to_remove:
    my_dict.pop(key, None)
  return my_dict

# Delete the items we do not want
keys_to_drop = ['bids_meta', 'provenance', 'qi_1', 'qi_2', 'size_x', 'size_y', 'size_z', 'spacing_x', 'spacing_y', 'spacing_z']

# Extract software metadata from provenance BEFORE removing it
def create_software_metadata_csv(json_data, csv_file_path):
    """Create dynamic software metadata CSV from MRIQC JSON provenance"""
    import platform
    
    # Extract from provenance if available
    if 'provenance' in json_data:
        prov = json_data['provenance']
        software = prov.get('software', 'mriqc')
        version = prov.get('version', 'unknown')
    else:
        software = 'mriqc'
        version = 'unknown'
    
    # Get system platform info
    platform_info = f"{platform.system()} {platform.release()}"
    
    # Create software metadata
    software_metadata = {
        'title': software,
        'description': 'MRIQC extracts no-reference IQMs (image quality metrics) from structural (T1w and T2w), functional and diffusion MRI data.',
        'version': version,
        'url': 'https://mriqc.readthedocs.io/en/stable/',
        'cmdline': f'{software} --version {version}',  # Simplified cmdline
        'platform': platform_info,
        'ID': 'https://scicrunch.org/resolver/RRID:SCR_022942'
    }
    
    # Write to CSV
    import pandas as pd
    df_software = pd.DataFrame(software_metadata, index=[0])
    software_csv_path = csv_file_path.replace('.csv', '_software_metadata.csv')
    df_software.to_csv(software_csv_path, index=False)
    
    print(f"Created dynamic software metadata: {software_csv_path}")
    print(f"  Software: {software} {version}")
    print(f"  Platform: {platform_info}")
    
    return software_csv_path

# Create dynamic software metadata CSV BEFORE removing provenance
software_csv_path = create_software_metadata_csv(data, csv_file)

# Do the drop
updated_data = remove_keys(data, keys_to_drop)

# Let's see what we did
# print(len(updated_data)) 
#print()
#for key, value in updated_data.items():
    #print(f"{key}: {value}")

# Add the fields we want to add
# subject_id, ses, task, run and source_url
# Extract from JSON file path and BIDS metadata
import os
import re

def extract_bids_info(json_file_path, json_data):
    """Extract BIDS information from file path and JSON metadata"""
    
    # Extract from BIDS metadata if available
    if 'bids_meta' in json_data:
        bids_meta = json_data['bids_meta']
        subj = bids_meta.get('subject', 'unknown')
        datatype = bids_meta.get('datatype', 'unknown')
        modality = bids_meta.get('modality', 'unknown')
    else:
        # Fallback to filename parsing
        filename = os.path.basename(json_file_path)
        subj = 'unknown'
        datatype = 'unknown'
        modality = 'unknown'
        
        # Parse BIDS filename pattern
        if filename.startswith('sub-'):
            subj = filename.split('_')[0].replace('sub-', '')
            
        # Extract modality from filename (e.g., T1w, bold, etc.)
        if '_' in filename:
            modality = filename.split('_')[-1].replace('.json', '')
    
    # Extract session, task, run from file path
    path_parts = json_file_path.split('/')
    ses = None
    task = None
    run = None
    
    # Look for session in path (ses-XX)
    for part in path_parts:
        if part.startswith('ses-'):
            ses = part.replace('ses-', '')
            break
    
    # Look for task in filename (task-XX)
    filename = os.path.basename(json_file_path)
    task_match = re.search(r'task-([^_]+)', filename)
    if task_match:
        task = task_match.group(1)
    else:
        # For anatomical data, task is typically None
        task = "None" if datatype == 'anat' else ""
    
    # Look for run in filename (run-XX)
    run_match = re.search(r'run-([^_]+)', filename)
    if run_match:
        run = run_match.group(1)
    else:
        run = ""
    
    # Use session 01 as default if not found
    if ses is None:
        ses = "01"
    
    return subj, ses, task, run

# Extract BIDS information dynamically
subj, ses, task, run = extract_bids_info(json_file, data)
url = json_file  # Use the full path as source URL

# Print extracted information for verification
print(f"Extracted BIDS info:")
print(f"  Subject: {subj}")
print(f"  Session: {ses}")
print(f"  Task: {task}")
print(f"  Run: {run}")
print(f"  Source: {url}")


updated_data.update({'subject_id': subj, 'ses': ses, 'task': task, 'run': run, 'source_url': url})  

# Lets look
#print(len(updated_data)) 
#print()
#for key, value in updated_data.items():
#    print(f"{key}: {value}")

# Turn the dictionary into a dataframe
df = pd.DataFrame(updated_data, index=[0])

# Write the dataframe out as csv
#csv_file = 'qwert.csv'

df.to_csv(csv_file, index=False)

# The end
