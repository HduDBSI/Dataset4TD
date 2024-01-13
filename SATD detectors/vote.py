import pandas as pd
import sys
sys.path.append("../") 
from project_Info import *
encoding = 'utf-8-sig'
# arr1 = [0, 0, 1, 1]
# arr2 = [1, 0, 0, 0]
# arr3 = [1, 1, 0, 0]
# arr  = [1, 0, 0, 0]
def vote(arr1, arr2, arr3):
    arr = []
    assert len(arr1) == len(arr2) and len(arr2) == len(arr3)
    for i in range(len(arr1)):
        if arr1[i]+arr2[i]+arr3[i] > 1:
            arr.append(1)
        else:
            arr.append(0)
    return arr  

classifiers = ['xgboost', 'mat', 'ggsatd']


# results can be found in 'comments-with-labels/Final'
for project in projects:
    df_xgboost = pd.read_csv('../comments-with-labels/XGBoost/'+project+'_allLevel_comment.csv', encoding=encoding)
    df_ggsatd = pd.read_csv('../comments-with-labels/GGSATD/'+project+'_allLevel_comment.csv', encoding=encoding)
    df_mat = pd.read_csv('../comments-with-labels/MAT/'+project+'_allLevel_comment.csv', encoding=encoding)

    label_xgboost= df_xgboost['xgboost'].values.tolist()
    label_ggsatd= df_ggsatd['ggsatd'].values.tolist()
    label_mat = df_mat['mat'].values.tolist()

    label_final = vote(label_xgboost, label_ggsatd, label_mat)

    df_final = df_xgboost.copy()

    df_final['mat'] = label_mat
    df_final['ggsatd'] = label_ggsatd
    df_final['label'] = label_final

    df_final.to_csv('../comments-with-labels/Final/'+project+'_allLevel_comment.csv', index=False, encoding=encoding)


