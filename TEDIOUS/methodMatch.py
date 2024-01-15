
import sys
import os
sys.path.append("../") 
from project_Info import projects
import pandas as pd
for project in projects:
    method_with_label = '../code snippets-with-labels&metrics/method/' + project + '_methodLevel.csv'
    method_info = 'methodsInfo/' + project + '.csv'
    df1 = pd.read_csv(method_with_label)
    print(len(df1))
    df2 = pd.read_csv(method_info)
    print(len(df2))
    df2['FilePath'] = df2['FilePath'].str.slice(start=3)
    df2['Content'] = df2['Content'].str.replace('\r', '')
    df3 = pd.merge(df1, df2, how='inner', on=['FilePath','MethodName', 'Content'])
    print(len(df3))
    assert len(df1) == len(df3), 'error'
    df4 = df3[['FilePath', 'MethodName', 'StartLine', 'EndLine', 'label']]
    df4.to_csv('methodsInfoUpdated/'+project+'.csv', index=False)