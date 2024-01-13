# Dataset
Click [here](https://github.com/HduDBSI/Dataset4TD/releases/download/dataset/code.snippets-with-labels.metrics.7z) to download the dataset.

# Automated Framework
To utilize this automated framework for constructing the aforementioned dataset or building your own dataset, please follow the steps outlined below.

0. Go to [projects](/projects) to download the projects.
1. Go to [javaparser_extract](/javaparser_extract) to extracts code snippets at the file-level, class-level, method-level, and block-level.
2. Go to [data_collection](/data_collection), run function [split](/data_collection/map_remap.py#L144 to extract comments from the code snippets. 
