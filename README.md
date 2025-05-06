# fmriprep2NIDM
Repo for the process of adding the results of fmriprep processing to the NIDM graph.

This fmriprep2NIDM project is designed to be a specific example of a more generic [csv2NIDM](https://github.com/incf-nidash/PyNIDM?tab=readme-ov-file#csv-file-to-nidm-conversion) problem.

The goal is to 
* Run an analysis tool (such as fmriprep),
* Represent the results of the tool in a CSV file
* Generate a dictionary for the resuls as a CSV file
* Generate a tool description file (as a CSV file) that captures the details of the analysis
* Use the above 3 CSV files as input to *pynidm* to generate either a standalone NIDM representation of the results
  of the analysis tool, or append the tool results to the NIDM representation of the dataset that the tool was applied to.

  
