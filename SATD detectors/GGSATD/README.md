# Reproduction
The code is reproduced from GGSATD (["Exploiting gated graph neural network for detecting and explaining self-admitted technical debts"](https://www.sciencedirect.com/science/article/pii/S0164121222000036.)), whose authors uploaded their code three times in this [website](https://figshare.com/articles/dataset/JSS-Graph/16869737). The first and second ones are same, and the third one is no publicly available. 

Note that, their available codes are same with the codes of [TextING](https://github.com/CRIPAC-DIG/TextING). The paper of [TextING](https://github.com/CRIPAC-DIG/TextING) is ["Every Document Owns Its Structure: Inductive Text Classification via Graph Neural Networks"](https://arxiv.org/abs/2004.13826/).

# Experiment Enviroment
- Ubuntu 18.04
- Python 3.6
- Cuda 11.1
- CuDNN 8.6.0
- RTX 3060 12GB
- Intel I9-10850K

Download pre-trained word embeddings glove.6B.300d.txt from [here](http://nlp.stanford.edu/data/glove.6B.zip) and unzip it to [SATD detectors/GGSATD/cache/glove.6B.300d.txt](/SATD%20detectors/GGSATD/cache/glove.6B.300d.txt).
```
conda create -n tf python=3.6
conda activate tf
pip install --upgrade pip
pip install tensorflow
pip install pandas nltk scipy scikit-learn

cd /Dataset4TD/SATD detectors/GGSATD
mkdir /home/xyh/miniconda3/envs/tf/nltk_data
mkdir /home/xyh/miniconda3/envs/tf/nltk_data/tokenizers
mv punkt /home/xyh/miniconda3/envs/tf/nltk_data/tokenizers/punkt

mkdir /home/xyh/miniconda3/envs/tf/nltk_data/corpora
mv wordnet /home/xyh/miniconda3/envs/tf/nltk_data/corpora/wordnet
mv omw-1.4 /home/xyh/miniconda3/envs/tf/nltk_data/corpora/omw-1.4
```

# Results Comparison
Cross-project: nine projects as the training set and the remaining one as the testing set.

## results of GGSATD
The table below is calculated by the confusion matrices provided by GGSATD, which shows the performance of GGSATD in cross-project scenarios.

| **Project**    | **Accuracy** | **Precision** | **Recall** | **F1-score** |
| ---------- | -------- | --------- | ------ | -------- |
| Apache Ant | 97.61%   | 62.42%    | 64.89% | 63.53%   |
| ArgoUML    | 96.06%   | 83.06%    | 92.51% | 87.51%   |
| Columba    | 99.25%   | 87.64%    | 88.87% | 88.22%   |
| EMF        | 98.26%   | 65.59%    | 57.98% | 61.35%   |
| Hibernate  | 95.32%   | 88.91%    | 80.68% | 84.58%   |
| JEdit      | 98.23%   | 71.86%    | 47.70% | 57.23%   |
| JFreeChart | 96.57%   | 68.63%    | 51.72% | 58.91%   |
| JMeter     | 98.27%   | 81.90%    | 80.78% | 81.28%   |
| JRuby      | 96.80%   | 89.98%    | 84.21% | 86.98%   |
| SQuirrel   | 97.57%   | 71.69%    | 65.10% | 68.06%   |
| **Average**| 97.40%   | 77.17%    | 71.44% | 73.77%   |

## results of our reproduced GGSATD

The table below is the running results of our reproduced model in cross-project scenarios. For the sake of fairness, we have run ten times to take the average value.

| **Project**    | **Accuracy** | **Precision** | **Recall** | **F1-score** |
| ---------- | -------- | --------- | ------ | -------- |
| Apache Ant | 97.32%   | 60.23%    | 51.30% | 55.00%   |
| ArgoUML    | 95.43%   | 83.30%    | 86.86% | 85.04%   |
| Columba    | 98.92%   | 86.14%    | 78.58% | 82.12%   |
| EMF        | 98.27%   | 68.52%    | 50.38% | 57.86%   |
| Hibernate  | 94.98%   | 89.47%    | 77.73% | 83.13%   |
| JEdit      | 98.16%   | 74.64%    | 39.34% | 51.30%   |
| JFreeChart | 96.83%   | 89.95%    | 37.37% | 52.76%   |
| JMeter     | 98.18%   | 82.86%    | 76.58% | 79.58%   |
| JRuby      | 94.57%   | 90.65%    | 63.95% | 74.89%   |
| SQuirrel   | 97.72%   | 77.48%    | 60.24% | 67.69%   |
| **Average**| 97.04%   | 80.32%    | 62.23% | 68.93%   |

## File Explanation
[train.py-Line 62](/SATD%20detectors/GGSATD/train.py#Line62) sets one project as testing set and the others as training set. [*easy to modify*]

[GGSATD.py](/SATD%20detectors/GGSATD/GGSATD.py) makes the approach as a python class for easy calling. [*approach integration*]

[cross_project.py](/SATD%20detectors/GGSATD/cross_project.py) uses [GGSATD.py](Dataset4TD/SATD%20detectors/GGSATD/GGSATD.py) for cross project experiments. [*get all results at one time*]

[tag.py](/SATD%20detectors/GGSATD/tag.py) exploits 10 projects (Apache Ant, ArgoUML, Columba, EMF, Hibernate ,JEdit ,JFreeChart ,JMeter ,JRuby ,SQuirrel) for model training, so as to obtain the labels for other 18 projects (ANTLR4, DBeaver, Elasticsearch, ExoPlayer, FastJSON, Flink, Guava, Jenkins, LibGDX, Logstash, Mockito, OpenRefine, Presto, Quarkus, QuestDB, Redisson, RxJava, Tink).
