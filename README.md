# Dataset
Click [here](https://github.com/HduDBSI/Dataset4TD/releases/download/dataset/code.snippets-with-labels.metrics.7z) to download the dataset.

# Automated Framework
To utilize this automated framework for constructing the aforementioned dataset or building your own dataset, please follow the steps outlined below.

0. Go to [projects](/projects) to download the projects and create necessary directories.
1. Go to [javaparser_extract](/javaparser_extract) to extracts code snippets at the file-level, class-level, method-level, and block-level. The extracted code snippets can be found in [code snippets-without-labels](/code%20snippets-without-labels)
2. Go to [data_collection](/data_collection), run function [split](/data_collection/map_remap.py#L144) to extract comments from the code snippets. The extracted comments can be found in [comments-without-labels](/comments-without-labels)
3. Go to [SATD detectors](/SATD%20detectors), employ three SATD detectors to classify the comments. 

# Manual Check
