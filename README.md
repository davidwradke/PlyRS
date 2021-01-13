# PlyRS
Source code of Pleiotropy Ratio Score (PlyRS) calculation, from the paper Radke et al.: Purifying selection on noncoding deletions of human regulatory elements detected using their cellular pleiotropy (https://www.biorxiv.org/content/10.1101/2020.05.19.105205v1)

This collection of steps will enable determination of PlyRS values on a per base-pair (genomic coordinate) level from a set of input files of a feature annotation. The annotation could be sites of regulatory activity (as in our study) or any set of sites of interest based on some predetermined criteria.

---

Step 0: Gather set of input files of a feature annotation with corresponding genomic coordinates.
	e.g. from https://egg2.wustl.edu/roadmap/data/byFileType/peaks/consolidated/broadPeak/ , Roadmap Epigenomics Project: http://www.roadmapepigenomics.org/data/

Step 1: Create vector files to identify the presence of a feature annotation of interest using a 0/1 binary system (i.e. 1 means that the feature is present). The files should be set up per chromosome with the coordinate, then tab, then concatenated string of binary values across all input files for that coordinate. Only coordinates with at least one 1 annotation across any input file are needed, since PlyRS = 0 at coordinates where there is no feature annotation of interest in any input file.
	e.g. step1example-chr21_DHS_hotspot.vectors.head10000.txt which includes a vector derived from 25 input files
	
Step 2: Run configuration database python file [make_config_database.py], modifying it using the filepaths of the vectors files.
	e.g. step2example-DHS_hotspot-configurations_database.txt

Step 3: Run calculate n-effective python file [calc_n-eff.py], batching in chunks of 10000 configurations, by specifying start line (see script). This is designed to parallel process multiple batches at once, likely in a cluster compute context.

Step 4: Concatenate all files generated in Step 3. The fourth column (rightmost) displays the unrounded PlyRS value (ranging from >0 to 1) for the vector configuration shown in the first column (leftmost).
	e.g. step4example-neff_share_notshare_DHS_hotspot-groupall.txt

Step 5: Associate PlyRS values from Step 4 with the coordinates and configurations from Step 1. You can now run analyses on PlyRS values across genomic coordinates for that feature annotation.