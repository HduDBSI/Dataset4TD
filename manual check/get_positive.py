import pandas as pd
import sys
sys.path.append("../") 
from project_Info import projects
encoding = 'utf-8-sig'

df_list = []
for project in projects:
    df = pd.read_csv(f'../comments-with-labels/Final/{project}_allLevel_comment.csv')
    df_list.append(df)

# join dataframes together
df = pd.concat(df_list, axis=0, ignore_index=True)

# remove others columns
df = df[['comment', 'label']]

# remove duplicated comments
df.drop_duplicates(inplace=True)

# export 
df.to_csv(f'all_comment.csv', index=False, encoding=encoding)

# obtain the positive samples containing keywords
df_list = []
keywords1 = ['TODO', 'FIXME', 'HACK', 'XXX']
for keyword in keywords1:
    keyword_pos_idx = df['comment'].str.contains(keyword, case=False, regex=True) & (df['label'] == 1)
    keyword_pos_df = df[keyword_pos_idx].sort_values('comment', ascending=True)
    df_list.append(keyword_pos_df)

single_person_check_pos = pd.concat(df_list, axis=0, ignore_index=True)

# remove duplicated comments
single_person_check_pos.drop_duplicates(inplace=True)

# mask labels
single_person_check_pos['label'] = -1


# export
single_person_check_pos.to_csv('Positive/positive-withKeywords-1manCheck.csv', index=False, encoding=encoding)

# obtain the positive samples not containing keywords
keywords1 = 'TODO|FIXME|HACK|XXX'
keyword_idx = df['comment'].str.contains(keywords1, case=False, regex=True)
positive_idx = df['label'] == 1
multi_person_check_pos = df[(~keyword_idx) & positive_idx]

# mask labels
multi_person_check_pos = multi_person_check_pos.sort_values('comment', ascending=True)

multi_person_check_pos['label'] = -1

# export
multi_person_check_pos.to_csv('Positive/positive-withoutKeywords-2manCheck1.csv', index=False, encoding=encoding)
multi_person_check_pos.to_csv('Positive/positive-withoutKeywords-2manCheck2.csv', index=False, encoding=encoding)

