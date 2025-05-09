# "stuff"2NIDM
Repo for the process of adding the results of any processing (for example, fmriprep) to the NIDM graph.

These examples are designed to be specific examples of a generic [csv2NIDM](https://github.com/incf-nidash/PyNIDM?tab=readme-ov-file#csv-file-to-nidm-conversion) problem.

In general, the goal is to:
 
* Run an analysis tool (such as fmriprep),
* Represent the results of the tool in a CSV file (example [here](CSVs/fmriprep/ABIDE_fmriprep_results_v2.csv))
* Generate (or fetch) a dictionary for the results as a CSV file (example [here](CSVs/fmriprep/fmriprep_data_dictionary_v3.csv))
* Generate a tool description file (as a CSV file) that captures the details of the analysis
   (example [here](CSVs/fmriprep/fmriprep_software_metadata.csv))
* Use the above 3 CSV files as input to *pynidm* to generate either a standalone NIDM representation of the results
  of the analysis tool, or append the tool results to the NIDM representation of the dataset that the tool was applied to.

## Examples

### fmriprep
We show a worked example for ***fmriprep*** [here](docs/fmriprep.md)

### mriqc
We show a worked example for ***mriqc*** [here](docs/mriqc.md)



