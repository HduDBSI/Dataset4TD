# LiteM
## RQ2: Effectiveness of Data Augmentation
0. Run [within_project-SMOTE.py](within_project-SMOTE.py), and the results can be found in [results/within_project_SMOTE.txt](results/within_project_SMOTE.txt).
1. Run [within_project-ASMOTE.py](within_project-ASMOTE.py), and the results can be found in [results/within_project.txt](results/within_project.txt).
2. Run [within_project-NoSMOTE.py](within_project-NoSMOTE.py), and the results can be found in [results/within_project_NoSMOTE.txt](results/within_project_NoSMOTE.txt).
3. Run [within_project-ADASYN.py](within_project-ADASYN.py), and the results can be found in [results/within_project_ADASYN.txt](results/within_project_ADASYN.txt).
4. Run [ablation-table.py](ablation-table.py), and the results of four augmentation techniques can be found in [results/ablation.txt](results/ablation.txt).

## RQ3: TDU Detection
0. Run [within_project-ASMOTE.py](within_project-ASMOTE.py), and the results of LiteM can be found in [results/within_project.txt](results/within_project.txt).
1. Run [baseline.py](baseline.py), and the results of DT can be found in [results/baseline.txt](results/baseline.txt).
2. GO to [../TEDIOUS](../TEDIOUS), and the results of TEDIOUS will be found in [../TEDIOUS/within_project.txt](../TEDIOUS/within_project.txt).
3. GO to [../SATDID](../SATDID), and the results of SATDID will be found in [../SATDID/within_project.txt](../SATDID/within_project.txt).
4. Run [baselines-tables.py](baselines-tables.py), and the results of four approaches can be found in [results/comparison.txt](results/comparison.txt).

## RQ4: Explainability of Model
0. Run [within_project-ASMOTE.py](within_project-ASMOTE.py), and the results can be found in [results/importance.mat](results/importance.mat).

# LiteMC
Run [LiteMC.py](LiteMC.py), and the results can be found in [results/real.txt](results/real.txt).

## Why Not Total Ten Fold
0. Run [total_ten_fold.py](total_ten_fold.py), and the results of LiteM can be found in [results/total_ten_fold.txt](results/total_ten_fold.txt).
1. GO to [../TEDIOUS](../TEDIOUS), and the results of TEDIOUS will be found in [../TEDIOUS/total_ten_fold.txt](../TEDIOUS/total_ten_fold.txt).
2. GO to [../SATDID](../SATDID), and the results of SATDID will be found in [../SATDID/total_ten_fold.txt](../SATDID/total_ten_fold.txt).

## Why Not Cross Project
0. Run [cross_project.py](cross_project.py), and the results of LiteM can be found in [results/cross_project.txt](results/cross_project.txt).
1. GO to [../TEDIOUS](../TEDIOUS), and the results of TEDIOUS will be found in [../TEDIOUS/cross_project.txt](../TEDIOUS/cross_project.txt).
2. GO to [../SATDID](../SATDID), and the results of SATDID will be found in [../SATDID/cross_project.txt](../SATDID/cross_project.txt).