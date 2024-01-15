# Reproduction
The code is reproduced from SATDID of ["A framework for conditional statement technical debt identification and description"](https://link.springer.com/article/10.1007/s10515-022-00364-8).

# Experiment Environment
- Ubuntu 18.04
- Python 3.8
- Cuda 11.1
- CuDNN 8.6.0
- RTX 3060 12GB
- Intel I9-10850K
- Python packages requirements.txt 

# Usage
1. Run [generate_java_files.py](generate_java_files.py) to generate java files for block statements.
2. Run [generate_SBTs.py](generate_SBTs.py) to generate SBT sequences from java files.
3. Run [within_projects.py](within_projects.py), and the results can be found in [within_project.txt](within_project.txt). 
4. Run [total_ten_fold.py](total_ten_fold.py), and the results can be found in [total_ten_fold.txt](total_ten_fold.txt).
5. Run [cross_project.py](cross_project.py), and the results can be found in [cross_project.txt](cross_project.txt).

# Experiment Result
The results are reported in [within_project.txt](within_project.txt)
## batch_size = 256, use CuDNNLSTM intead of LSTM

| **Project**    | **Accuracy** | **Precision** | **Recall** | **F1-score** | **Cost Time** |
| ---------- | -------- | --------- | ------ | -------- | -------- |
|    antlr4     |  97.60%  |   0.00%   | 0.00%  |  0.00%   | 9 |
|    dbeaver    |  94.29%  |  15.22%   | 7.55%  |  9.23%   | 38 |
| elasticsearch |  94.14%  |  18.25%   | 17.22% |  17.53%  | 165 |
|   exoplayer   |  96.73%  |  44.13%   | 40.93% |  41.86%  | 81 |
|   fastjson    |  96.92%  |   5.00%   | 2.50%  |  3.33%   | 11 |
|     flink     |  96.81%  |  16.10%   | 15.53% |  15.52%  | 163 |
|     guava     |  95.50%  |  69.20%   | 63.09% |  65.77%  | 62 |
|    jenkins    |  88.15%  |  18.98%   | 16.57% |  17.28%  | 33 |
|    libgdx     |  92.59%  |  38.73%   | 47.91% |  39.70%  | 22 |
|   logstash    |  95.95%  |   0.00%   | 0.00%  |  0.00%   | 5 |
|    mockito    |  96.25%  |   0.00%   | 0.00%  |  0.00%   | 15 |
|  openrefine   |  90.73%  |  21.08%   | 8.44%  |  10.70%  | 9 |
|    presto     |  92.77%  |  27.60%   | 22.87% |  24.44%  | 93 |
|    quarkus    |  92.14%  |  28.63%   | 23.86% |  25.73%  | 65 |
|    questdb    |  97.20%  |  23.79%   | 8.64%  |  11.51%  | 32 |
|   redisson    |  91.04%  |  30.00%   | 17.38% |  20.42%  | 6 |
|    rxjava     |  96.12%  |  10.00%   | 5.00%  |  6.67%   | 17 |
|     tink      |  98.03%  |   0.00%   | 0.00%  |  0.00%   | 15 |
|    Average    |  94.61%  |  20.37%   | 16.53% |  17.21%  | 47 |

## batch_size = 64, use CuDNNLSTM intead of LSTM. 

The experimental parameters used the best parameters provided in the original papar.
| **Project**    | **Accuracy** | **Precision** | **Recall** | **F1-score** | **Cost Time** |
| ---------- | -------- | --------- | ------ | -------- | -------- |
|    antlr4     |  96.54%  |   0.00%   | 0.00%  |  0.00%   | 24 |
|    dbeaver    |  93.84%  |  16.43%   | 11.30% |  13.08%  | 104 |
| elasticsearch |  92.56%  |  13.35%   | 17.59% |  14.86%  | 459 |
|   exoplayer   |  96.72%  |  43.35%   | 39.97% |  41.48%  | 220 |
|   fastjson    |  98.27%  |  78.50%   | 68.50% |  68.44%  | 28 |
|     flink     |  95.91%  |  12.29%   | 16.01% |  13.12%  | 453 |
|     guava     |  95.71%  |  70.44%   | 64.67% |  67.22%  | 169 |
|    jenkins    |  88.57%  |  22.43%   | 18.64% |  20.08%  | 90 |
|    libgdx     |  94.96%  |  50.86%   | 52.25% |  50.18%  | 59 |
|   logstash    |  94.37%  |  28.10%   | 25.00% |  23.56%  | 12 |
|    mockito    |  95.27%  |  30.80%   | 19.29% |  20.19%  | 37 |
|  openrefine   |  90.27%  |  45.11%   | 25.67% |  31.76%  | 23 |
|    presto     |  92.54%  |  27.05%   | 23.93% |  25.08%  | 247 |
|    quarkus    |  90.78%  |  24.49%   | 27.06% |  25.48%  | 177 |
|    questdb    |  96.67%  |  18.87%   | 10.82% |  13.67%  | 87 |
|   redisson    |  95.44%  |  85.32%   | 75.48% |  78.28%  | 13 |
|    rxjava     |  97.60%  |  86.13%   | 55.42% |  64.54%  | 44 |
|     tink      |  97.92%  |  33.33%   | 22.50% |  25.71%  | 36 |
|    Average    |  94.66%  |  38.16%   | 31.89% |  33.15%  | 127 |

