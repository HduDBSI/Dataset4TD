import pandas as pd
import sys
import numpy as np
sys.path.append('../')
from project_Info import projects
encoding='utf-8-sig'
df_list = []
for project in projects:
    df = pd.read_csv(f'../comments-with-labels/Final/{project}_allLevel_comment.csv')
    df_list.append(df)

df = pd.concat(df_list, axis=0, ignore_index=True)
df.drop_duplicates(inplace=True)

idx1 = (df['xgboost'] == 0) & (df['mat'] == 0) & (df['ggsatd'] == 0)
idx2 = (df['xgboost'] == 1) & (df['mat'] == 1) & (df['ggsatd'] == 1)
idx3 = (df['xgboost'] == 1) & (df['mat'] == 1) & (df['ggsatd'] == 0)
idx4 = (df['xgboost'] == 1) & (df['mat'] == 0) & (df['ggsatd'] == 1)
idx5 = (df['xgboost'] == 0) & (df['mat'] == 1) & (df['ggsatd'] == 1)

idx =  ~ (idx1 | idx2 | idx3 | idx4 | idx5)
new_df = df[['comment', 'label']][idx]

new_df['label'] = -1

new_df.to_csv('Negative/negative-uncertain-2manCheck1.csv', index=False, encoding=encoding)
new_df.to_csv('Negative/negative-uncertain-2manCheck2.csv', index=False, encoding=encoding)