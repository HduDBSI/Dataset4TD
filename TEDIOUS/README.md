# Environment
Windows 10 Professional Edition

Download [JDK 11](https://corretto.aws/downloads/resources/11.0.18.10.1/amazon-corretto-11.0.18.10.1-windows-x64-jdk.zip).

Unzip amazon-corretto-11.0.18.10.1-windows-x64-jdk.zip to [jdk11](jdk11) in this directory.

# Steps
1. Run [analyzePMD&CS.py](analyzePMD&CS.py) to obtain [csResults](csResults) and [pmdResults](pmdResults).
2. Run [match.py](match.py) to obtain [MatchResults](/MatchResults). Or run [csMatch.py](scMatch.py)/[pmdMatch.py](pmdMatch.py) to obtain [csMatchResults](csMatchResults)/[pmdMatchResults](pmdMatchResults), then merge them to get [MatchResults](MatchResults).
3. Run [within_projects.py](within_projects.py), and the results can be found in [within_project.txt](within_project.txt). 
4. Run [total_ten_fold.py](total_ten_fold.py), and the results can be found in [total_ten_fold.txt](total_ten_fold.txt).
5. Run [cross_project.py](cross_project.py), and the results can be found in [cross_project.txt](cross_project.txt).

# Result
| **Project**    | **Accuracy** | **Precision** | **Recall** | **F1-score** | **Cost Time** |
| ---------- | -------- | --------- | ------ | -------- | -------- |
|    antlr4     |  88.43%  |  11.75%   | 26.00% |  15.86%  | 0.13 |
|    dbeaver    |  86.92%  |  11.09%   | 22.93% |  14.87%  | 0.16 |
| elasticsearch |  84.66%  |   9.36%   | 23.57% |  13.39%  | 0.29 |
|   exoplayer   |  78.51%  |  12.58%   | 48.44% |  19.97%  | 0.17 |
|   fastjson    |  84.65%  |  27.20%   | 68.21% |  38.78%  | 0.13 |
|     flink     |  88.55%  |   9.75%   | 29.88% |  14.69%  | 0.29 |
|     guava     |  78.21%  |  25.01%   | 50.14% |  33.32%  | 0.16 |
|    jenkins    |  76.35%  |  27.78%   | 38.41% |  32.12%  | 0.16 |
|    libgdx     |  95.39%  |  39.30%   | 42.98% |  40.94%  | 0.16 |
|   logstash    |  84.44%  |  11.66%   | 29.17% |  16.22%  | 0.12 |
|    mockito    |  87.29%  |  21.24%   | 38.57% |  26.46%  | 0.13 |
|  openrefine   |  81.24%  |  22.08%   | 32.50% |  26.14%  | 0.13 |
|    presto     |  80.83%  |  22.38%   | 38.67% |  28.34%  | 0.18 |
|    quarkus    |  82.58%  |  16.89%   | 33.41% |  22.15%  | 0.17 |
|    questdb    |  94.36%  |  16.88%   | 18.11% |  17.10%  | 0.14 |
|   redisson    |  96.03%  |  51.01%   | 70.33% |  57.52%  | 0.13 |
|    rxjava     |  95.99%  |  55.35%   | 65.90% |  58.92%  | 0.14 |
|     tink      |  86.33%  |  23.66%   | 57.00% |  33.34%  | 0.13 |
|    **Average**    |  86.15%  |  23.05%   | 40.79% |  28.34%  | 0.16 |