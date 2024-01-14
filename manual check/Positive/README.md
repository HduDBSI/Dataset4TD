# Classified as positive samples without keywords
0. Assumed that there are files named *positive-withoutKeywords-2manCheck1.csv* and *positive-withoutKeywords-2manCheck2.csv*.
1. After verification by People B and C, *positive-withoutKeywords-2manChecked1.csv* and *positive-withoutKeywords-2manChecked2.csv* are obtained.
2. Run *combine.py* to obtain *positive-withoutKeywords-2manChecked*.
3. Person A checks *positive-withoutKeywords-2manChecked.csv* and sets final label as `label3`, thereby obtaining *positive-withoutKeywords-3manChecked.csv*

# Classified as positive samples with keywords
0. Assumed that there is a file named *positive-withKeywords-1manCheck.csv*.
1. Person A checks them one by one, thereby obtaining *positive-withKeywords-1manChecked.csv*.

# Classified as positive samples
0. Run *merge.py* to merge *positive-withKeywords-1manChecked.csv* and *positive-withoutKeywords-3manChecked.csv* as *positive.csv*.