# fmriprep2NIDM
Repo for the process of adding the results of fmriprep processing to the NIDM graph.

This fmriprep2NIDM project is designed to be a specific example of a more generic [csv2NIDM](https://github.com/incf-nidash/PyNIDM?tab=readme-ov-file#csv-file-to-nidm-conversion) problem.

The goal is to 
* Run an analysis tool (such as fmriprep),
* Represent the results of the tool in a CSV file (example [here](CSVs/ABIDE_fmriprep_results_v2.csv))
* Generate a dictionary for the results as a CSV file (example [here](CSVs/fmriprep_data_dictionary_v3.csv))
* Generate a tool description file (as a CSV file) that captures the details of the analysis (example [here]())
* Use the above 3 CSV files as input to *pynidm* to generate either a standalone NIDM representation of the results
  of the analysis tool, or append the tool results to the NIDM representation of the dataset that the tool was applied to.

  ## Example
  ### Step 1: Run fmriprep
  Our friends at **INDI** have run the *fmriprep* tool on much of their publically hosted data, includeing the ABIDS and
  ADHD-200 datasets. These *fmriprep* results are available on the **INDI** AWS S3 bucket. The 'path' for such an
  example fmriprep run for sub-0050118 of the ABIDE dataset is:

  s3://fcp-indi/data/Projects/ABIDE/Outputs/fmriprep/fmriprep/sub-0050118

  There are many example results here.

  ### Step 2: Represent the results of the tool in a CSV file
  

  
  
