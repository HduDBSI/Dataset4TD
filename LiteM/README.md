# LiteM
## RQ2: Effectiveness of Data Augmentation
0. In [within_project.py](within_project.py), set the argument `classifier` as `LightGBM` and modify the argument `technique`.
1. Run [RQ2.py](RQ2.py), and the results of four augmentation techniques can be found in [results/RQ2.txt](results/RQ2.txt).

## RQ3: TDWA Detection
0. Run [within_project.py](within_project.py), with the argument `classifier` as `LightGBM` and the argument `technique` as `ASMOTE`.
1. Run [within_project.py](within_project.py), with the argument `classifier` as `DecisionTree` and the argument `technique` as `ASMOTE`.
2. GO to [../TEDIOUS](../TEDIOUS), and the results of TEDIOUS will be found in [../TEDIOUS/results/within_project.txt](../TEDIOUS/results/within_project.txt).
3. GO to [../SATDID](../SATDID), and the results of SATDID will be found in [../SATDID/results/within_project.txt](../SATDID/results/within_project.txt).
4. Run [RQ3.py](RQ3.py), and the results of four approaches can be found in [results/RQ3.txt](results/RQ3.txt).

## RQ4: Explainability of Model
0. Run [within_project.py](within_project.py), with the argument `classifier` as `LightGBM` and the argument `technique` as `ASMOTE`. The results can be found in [results/importance_ASMOTE_LightGBM.mat](results/importance_ASMOTE_LightGBM.mat).

# LiteMC
0. Run [LiteMC.py](LiteMC.py), with the variable `pseudo` as `PseudoLabelForCASFromMAT`, `PseudoLabelForCASFromXGBoost` and `PseudoLabelForCASFromGGSATD`.
1. Run [Table4LiteMC.py](Table4LiteMC.py)

## Why Not Total Ten Fold
0. Run [total_ten_fold.py](total_ten_fold.py), and the results of LiteM can be found in [results/total_ten_fold.txt](results/total_ten_fold.txt).
1. GO to [../TEDIOUS](../TEDIOUS), and the results of TEDIOUS will be found in [../TEDIOUS/total_ten_fold.txt](../TEDIOUS/total_ten_fold.txt).
2. GO to [../SATDID](../SATDID), and the results of SATDID will be found in [../SATDID/total_ten_fold.txt](../SATDID/total_ten_fold.txt).

## Why Not Cross Project
0. Run [cross_project.py](cross_project.py), and the results of LiteM can be found in [results/cross_project.txt](results/cross_project.txt).
1. GO to [../TEDIOUS](../TEDIOUS), and the results of TEDIOUS will be found in [../TEDIOUS/cross_project.txt](../TEDIOUS/cross_project.txt).
2. GO to [../SATDID](../SATDID), and the results of SATDID will be found in [../SATDID/cross_project.txt](../SATDID/cross_project.txt).
