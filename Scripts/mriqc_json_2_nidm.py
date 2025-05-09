#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import json
import sys

# Get arguments, input json file, and filename for output
# Parse Command Line
print ('Usage: mriqc_json_2_nidm.py mriqc_json_file csv_output_file')
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

# Do the drop
updated_data = remove_keys(data, keys_to_drop)

# Let's see what we did
# print(len(updated_data)) 
#print()
#for key, value in updated_data.items():
    #print(f"{key}: {value}")

# Add the fields we want to add
# subject_id, ses, task, run and source_url
# get the values, somehow
# Pass on commandline?
# Extract from metadata?
subj = "0012345"
ses = "01"
task = "None"
run = ""
url = "S3://qwert"

updated_data.update({'subject_id': subj, 'ses': ses, 'taask': task, 'run': run, 'source_url': url})  

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
