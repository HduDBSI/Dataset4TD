# Reproduction
The code is reproduced from MAT (["How Far Have We Progressed in Identifying Self-admitted Technical Debts? A Comprehensive Empirical Study"](https://doi.org/10.1145/3447247.)), whose authors uploaded their code in this [website](https://github.com/Naplues/MAT).

# Results Comparison
As the paper MAT (["How Far Have We Progressed in Identifying Self-admitted Technical Debts? A Comprehensive Empirical Study"](https://doi.org/10.1145/3447247.)) describes, fuzzy MAT performs better than strict MAT. Therefore, we here only reproduce the fuzzy one.

## results of MAT 
The table below is copied from MAT (["How Far Have We Progressed in Identifying Self-admitted Technical Debts? A Comprehensive Empirical Study"](https://doi.org/10.1145/3447247.)), which shows the performance of fuzzy MAT.

| **Project**| **Precision** | **Recall** | **F1-score** |
| ---------- | --------- | ------ | -------- |
| Ant        | 87.0%    | 46.1% | 60.3%   |
| ArgoUML    | 82.3%    | 93.4% | 87.4%   |
| Columba    | 90.6%    | 82.8% | 86.5%   |
| EMF        | 100.0%    | 35.1% | 52.0%   |
| Hibernate  | 94.5%    | 72.4% | 82.0%   |
| JEdit      | 85.1%    | 20.5% | 33.1%   |
| JFreeChart | 72.3%    | 72.3% | 72.3%   |
| JMeter     | 92.4%    | 78.0% | 84.6%   |
| JRuby      | 91.1%    | 88.3% | 89.7%   |
| SQuirrel   | 92.5%    | 61.2% | 73.7%   |
| **Average**    | 88.8%    | 65.0% | 72.2%   |

## results of our reproduced MAT

The table below is the running results of our reproduced model.

| **Project**    | **Accuracy** | **Precision** | **Recall** | **F1-score** |
| ---------- | -------- | --------- | ------ | -------- |
| Ant        | 98.17%   | 48.09%    | 90.00% | 62.69%   |
| ArgoUML    | 95.58%   | 88.04%    | 83.32% | 85.62%   |
| Columba    | 99.29%   | 86.27%    | 90.72% | 88.44%   |
| EMF        | 98.29%   | 29.81%    | 93.94% | 45.26%   |
| Hibernate  | 94.98%   | 72.88%    | 94.25% | 82.20%   |
| JEdit      | 97.90%   | 19.14%    | 83.05% | 31.11%   |
| JFreeChart | 96.60%   | 46.41%    | 71.85% | 56.40%   |
| JMeter     | 98.29%   | 74.60%    | 86.65% | 80.17%   |
| JRuby      | 97.84%   | 90.35%    | 92.43% | 91.38%   |
| SQuirrel   | 97.78%   | 53.85%    | 84.62% | 65.81%   |
| **Average**    | 97.47%   | 60.94%    | 87.08% | 68.91%   |

## File Explanation
[MAT.py](SATD%20detectors/MAT/MAT.py) makes the approach as a python class for easy calling. [*approach integration*]

[cross_project.py](SATD%20detectors/MAT/cross_project.py) uses [MAT.py](SATD%20detectors/MAT/MAT.py) for cross project experiments. [*get all results at one time*] Note that MAT is an unsupervised approach, so there are no training set or testing set.

[tag.py](SATD%20detectors/MAT/tag.py) obtains the labels for other 18 projects (ANTLR4, DBeaver, Elasticsearch, ExoPlayer, FastJSON, Flink, Guava, Jenkins, LibGDX, Logstash, Mockito, OpenRefine, Presto, Quarkus, QuestDB, Redisson, RxJava, Tink).
