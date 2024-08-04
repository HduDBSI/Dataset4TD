import pandas as pd
import sys
import numpy as np
sys.path.append('../')
from project_Info import projects
encoding = 'utf-8-sig'

df_list = []
kept_columns = ['comment', 'xgboost', 'mat', 'ggsatd', 'label']

for project in projects:
    df = pd.read_csv(f'../comments-with-labels/Final/{project}_allLevel_comment.csv', encoding=encoding)
    df_list.append(df)

# join dataframes together
df = pd.concat(df_list, axis=0, ignore_index=True).reset_index(drop=True)

# remove others columns
df = df[kept_columns]

# remove duplicated comments
df.drop_duplicates(subset='comment', keep='first', inplace=True)

# reset index
df = df.reset_index(drop=True)

print('The number of total samples:', len(df))

# export 
df.to_csv(f'all_comment.csv', index=False, encoding=encoding)

# rename column label to voting_label
df.rename(columns={'label': 'voting_label'}, inplace=True)

# add new columns and initialize it
df['annotator1_label'] = -1
df['annotator2_label'] = -1
df['annotator3_label'] = -1
df['label'] = -1

def get_potentialFalseNegatives(df: pd.DataFrame):
    
    idx1 = (df['xgboost'] == 1) & (df['mat'] == 0) & (df['ggsatd'] == 0)
    idx2 = (df['xgboost'] == 0) & (df['mat'] == 1) & (df['ggsatd'] == 0)
    idx3 = (df['xgboost'] == 0) & (df['mat'] == 0) & (df['ggsatd'] == 1)

    pfn =  df[(idx1 | idx2 | idx3)]

    return pfn

def get_potentialFalsePositives_And_remainingPositives(df: pd.DataFrame):

    keywords = 'TODO|FIXME|HACK|XXX'
    keyword_idx = df['comment'].str.contains(keywords, case=False, regex=True)
    positive_idx = df['voting_label'] == 1

    pfp = df[(~keyword_idx) & positive_idx]
    rp = df[keyword_idx & positive_idx]
    return pfp, rp

pfn = get_potentialFalseNegatives(df.copy(deep=True))
pfp, rp = get_potentialFalsePositives_And_remainingPositives(df.copy(deep=True))

print('The number of potential false negatives:', len(pfn))
print('The number of potential false positives:', len(pfp))
print('The number of remaining positives:', len(rp))

# merge potential false negatives and false positives into uncertain
uncertain = pd.concat([pfn, pfp], axis=0, ignore_index=True)

# shuffle uncertain
uncertain = uncertain.sample(frac=1).reset_index(drop=True)

# export
uncertain.to_csv('Uncertain.csv', index=False, encoding=encoding)
rp.to_csv('HavingKeywords.csv', index=False, encoding=encoding)