# Reproduction
The code is reproduced from XGBoost (["Multiclass Classification for Self-Admitted Technical Debt Based on XGBoost"](https://doi.org/10.1145/3447247.)), whose authors did not share their code in the paper.

# Results
As the paper XGBoost (["Multiclass Classification for Self-Admitted Technical Debt Based on XGBoost"](https://doi.org/10.1145/3447247.)) focused on muticlass classification task for SATD, there are no binary classification results in their paper. Therefore, we only show the results of our reproduced model.

## results of our reproduced XGBoost

The table below is the running results of our reproduced model.

| **Project**|**Accuracy**|**Precision**|**Recall**|**F1-score**|
| ---------- | -------- | -------- | -------- | -------- |
| Ant        |  97.71%  |  69.70%  |  50.08%  |  58.27%  |
| ArgoUML    |  95.80%  |  83.83%  |  89.06%  |  86.36%  |
| Columba    |  99.17%  |  85.73%  |  88.38%  |  87.03%  |
| EMF        |  98.02%  |  65.26%  |  34.71%  |  45.31%  |
| Hibernate  |  95.31%  |  92.34%  |  76.86%  |  83.89%  |
| JEdit      |  98.23%  |  87.32%  |  33.71%  |  48.62%  |
| JFreeChart |  96.64%  |  71.77%  |  48.18%  |  57.66%  |
| JMeter     |  98.11%  |  81.95%  |  75.94%  |  78.82%  |
| JRuby      |  97.68%  |  91.63%  |  89.94%  |  90.77%  |
| SQuirrel   |  97.65%  |  75.43%  |  60.63%  |  67.17%  |
|**Average** |  97.43%  |  80.50%  |  64.75%  |  70.39%  |


For each project, the training and testing time is about 387s.

## File Explanation
[train.py-Line 12](/SATD%20detectors/XGBoost/train.py#Line12) sets one project as testing set and the others as training set. [*easy to modify*]

[XGBoost.py](/SATD%20detectors/XGBoost/XGBoost.py) makes the approach as a python class for easy calling. [*approach integration*]

[cross_project.py](/SATD%20detectors/XGBoost/cross_project.py) uses [XGBoost.py](/SATD%20detectors/XGBoost/XGBoost.py) for cross project experiments. [*get all results at one time*]

[tag.py](/SATD%20detectors/XGBoost/tag.py) exploits 10 projects (Apache Ant, ArgoUML, Columba, EMF, Hibernate ,JEdit ,JFreeChart ,JMeter ,JRuby ,SQuirrel) for model training, so as to obtain the labels for other 18 projects (ANTLR4, DBeaver, Elasticsearch, ExoPlayer, FastJSON, Flink, Guava, Jenkins, LibGDX, Logstash, Mockito, OpenRefine, Presto, Quarkus, QuestDB, Redisson, RxJava, Tink).
