# mriqc2NIDM
Example for the process of adding the results of mriqc processing to the NIDM graph.

> **Note**: The MRIQC to NIDM conversion script automatically extracts BIDS metadata and software provenance information. No manual editing of subject IDs, versions, or platform information is required.

### Step 1: Run mriqc
Our friends at **INDI** have run the *mriqc* tool on much of their publically hosted data, includeing the ABIDE and
ADHD-200 datasets. These *mriqc* results are available on the **INDI** AWS S3 bucket. The 'path' for such an
example mriqc run for sub-0051607 of the ABIDE dataset is:

  s3://fcp-indi/data/Projects/ABIDE/Outputs/mriqc/mriqc/sub-0051607_T1w.html

There are many example results there.

### Step 2: Represent the results of the tool in a CSV file
The mriqc processing generates many image quality metrics (IQMs). There is a different set of descriptors for T1, T2, diffusion, etc. scan types. It keeps its results in a .json file. An example of the T1w mriqc results .json file is at:

 s3://fcp-indi/data/Projects/ABIDE/Outputs/mriqc/mriqc/sub-0051607/anat/sub-0051607_T1w.json

This file needs to be converted to csv. We have a python script entitled *mriqc_json2csv.py* to do this. The script now automatically extracts BIDS metadata and generates software provenance information.

**Example Usage:**
```console
# Using the example MRIQC JSON file in this repository
>  python Scripts/mriqc_json2csv.py example/mriqc/sub-0051456_T1w.json example/mriqc/sub-0051456_mriqc_results.csv
```

**Output:**
```
Created dynamic software metadata: example/mriqc/sub-0051456_mriqc_results_software_metadata.csv
  Software: mriqc 25.0.0rc0
  Platform: Linux 4.18.0-372.9.1.el8.x86_64
Extracted BIDS info:
  Subject: 0051456
  Session: 01
  Task: 
  Run: 
  Source: example/mriqc/sub-0051456_T1w.json
```

This generates two CSV files:
1. **sub-0051456_mriqc_results.csv** - Contains all MRIQC quality metrics plus dynamically extracted BIDS fields
2. **sub-0051456_mriqc_results_software_metadata.csv** - Contains software provenance information extracted from the JSON

### Step 3: Generate a dictionary for the results as a CSV file
Given that the conversion of the .json mriqc results to csv generates a specific list of features, we need a dictionary for
files generated in this fashion. The dictionary includes information about the contents of each column including
name, description, value type, range, units, semantic annotation, etc. Since this is 'fixed' by the output of
the .json converter, other users do note need to generate this file themselves, but rather just need to fetch this file
from some source. The *mriqc* dictionary file is [here](CSVs/mriqc/mriqc_dictionary_v1.csv).

### Step 4: Generate a tool description file
With the *mriqc_json2csv.py* script, the tool description file is **automatically generated** from the MRIQC JSON provenance data. The generated file contains:

* **title**: mriqc
* **description**: MRIQC extracts no-reference IQMs...
* **version**: Extracted from JSON (e.g., 25.0.0rc0)
* **url**: https://mriqc.readthedocs.io/en/stable/
* **cmdline**: Generated (e.g., mriqc --version 25.0.0rc0)
* **platform**: System info (e.g., Linux 4.18.0-372.9.1.el8.x86_64)
* **ID**: https://scicrunch.org/resolver/RRID:SCR_022942

No manual editing is required - the script extracts the actual version used and system platform automatically!

### Step 5: Use *PyNIDM* and the  3 CSV files to generate the NIDM representation  
*PyNIDM* is available [here](https://github.com/incf-nidash/PyNIDM). We can create the NIDM representation of these 
results either as a 'stand alone' NIDM file, or attach it to the NIDM representation of the source imaging data that 
was used.

#### Stand-alone NIDM results
After installing PyNIDM, one can use the csv2nidm tool to perform the conversion. Using the example files generated in Step 2:

```console
>  csv2nidm -csv example/mriqc/sub-0051456_mriqc_results.csv \
   -csv_map CSVs/mriqc/mriqc_dictionary_v1.csv -no_concepts \
   -derivative example/mriqc/sub-0051456_mriqc_results_software_metadata.csv \
   -out example/mriqc/sub-0051456_nidm.ttl
```

In this command, the '-csv' flag indicates the full path to CSV file to convert that contains your ***processing results*** 
(in this example, the summarized results of the mriqc analysis. The '-csv_map' is followed by the full path to 
user-supplied CSV-version of ***data dictionary*** containing the following required columns: source_variable, label,
description, valueType, measureOf, isAbout(For multiple isAbout entries, use a ';' to separate them in a single column
within the csv file dataframe), unitCode, minValue, maxValue. The '-derivative', if set, indicates CSV file provided 
above is derivative data which includes columns 'ses','task','run' which will be used to identify the subject scan 
session, run, and verify against the task if an existing nidm file is provided and was made from bids (bidsmri2nidm).
Otherwise these additional columns (ses, task,run) will be ignored. After the '-derivative' flag one must provide 
the ***software metadata*** CSV file. Additionally, the '-no_concepts' flag specifies that no concept associations will 
be asked of the user.

#### Add derivatives to existing NIDM file
If you happen to have a NIDM file for the MRI images upon which your MRIQC was run, you can add these derivatives to that
NIDM file. The command is similar to the above stand-alone version except that we provide the '-nidm' flag followed by the 
NIDM (.ttl) file you want to add to.  We provide an example ABIDE site NIDM for the OHSU site [here](../TTLs/OHSU_nidm.ttl).

```console
>  csv2nidm -nidm TTLs/OHSU_nidm.ttl -csv example/mriqc/sub-0051456_mriqc_results.csv \
   -csv_map CSVs/mriqc/mriqc_dictionary_v1.csv -no_concepts \
   -derivative example/mriqc/sub-0051456_mriqc_results_software_metadata.csv
```
### Next steps
So, you have a NIDM file now, what can you do with it? We can query (ask questions of) it.

* What subjects do you have?

```console
>  pynidm query -nl ~/GitHub/fmriprep2NIDM/TTLs/OHSU_nidm.ttl -u /subjects
```

> Subject UUID                            Source Subject ID
> ------------------------------------  -------------------
> c77a326a-a169-11ec-b1dd-003ee1ce9545                50155
> 
> cc22f39c-a169-11ec-b1dd-003ee1ce9545                50169
> 
> c426355a-a169-11ec-b1dd-003ee1ce9545                50143

* What do we know about any given subject?

```console
>  pynidm query -nl ~/GitHub/fmriprep2NIDM/TTLs/OHSU_nidm.ttl -u /subjects/<subject_uuid>
```

### Summary: Complete MRIQC to NIDM Workflow

The workflow is now fully automated:

1. **Input**: MRIQC JSON file (e.g., `sub-0051456_T1w.json`)
2. **Run**: `python Scripts/mriqc_json2csv.py input.json output.csv`
3. **Outputs**: 
   - `output.csv` - MRIQC metrics with dynamic BIDS metadata
   - `output_software_metadata.csv` - Auto-generated software provenance
4. **Convert**: Use csv2nidm with the generated files
5. **Result**: NIDM file with complete metadata and provenance

No manual editing required - all metadata is extracted automatically!





