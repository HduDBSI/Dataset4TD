# Dataset
Click [here](https://github.com/HduDBSI/Dataset4TD/releases/download/dataset/code.snippets-with-labels.metrics.7z) to download the dataset.

# Automated Framework
To utilize this automated framework for constructing the aforementioned dataset or building your own dataset, please follow the steps outlined below.

1. Go to [projects](/projects) to download the projects and create necessary directories. Run [mkdirs.py](projects/mkdirs.py) to make directories [/code snippets-without-labels](/code%20snippets-without-labels), [/comments-without-labels](/comments-without-labels), [/comments-with-labels](/comments-with-labels), [comments-with-labels-checked](comments-with-labels-checked), [code snippets-with-labels](code%20snippets-with-labels), [/metrics](/metrics) and [/code snippets-with-labels&metrics](/code%20snippets-with-labels&metrics).
2. Go to [javaparser_extract](/javaparser_extract) to extracts code snippets at the file-level, class-level, method-level, and block-level. The extracted code snippets can be found in [code snippets-without-labels](/code%20snippets-without-labels).
3. Go to [data_collection](/data_collection), run function [split](/data_collection/map_remap.py#L144) to extract comments from the code snippets. The extracted comments can be found in [comments-without-labels](/comments-without-labels).
4. Go to [SATD detectors](/SATD%20detectors), employ three SATD detectors to classify the comments. The classified comments can be found in [comments-with-labels](/comments-with-labels).
5. Go to [metrics tool](/metrics%20tool), utilize the tools to calculate code metrics at file, class, method and block levels.

# Manual Check
Go to [manual check](/manual%20check), use the scripts and the annotation tool to help manual check. The checked comments can be found in [comments-with-labels-checked](/comments-with-labels-checked).
