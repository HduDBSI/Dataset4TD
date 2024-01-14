import pandas as pd
import sys
sys.path.append('../')
from project_Info import projects

encoding = 'utf-8-sig'

def my_update(df_updater, df_updatee, based_column_name, update_column_name):
    # Create a mapping dictionary from the df_updater DataFrame
    mapping_dict = df_updater.set_index(based_column_name)[update_column_name].to_dict()

    update_column_type = df_updatee[update_column_name].dtype
    # Update the specified column in the df_updatee DataFrame using the mapping dictionary
    df_updatee[update_column_name] = df_updatee[based_column_name].map(mapping_dict).fillna(df_updatee[update_column_name])

    # Convert the column datatype back to its original datatype
    df_updatee[update_column_name] = df_updatee[update_column_name].astype(update_column_type)

    return df_updatee
    
# updater = pd.read_csv('all_comment_checked.csv', encoding=encoding)
updater = pd.read_csv('all_comment_checked_deprecated.csv', encoding=encoding)

for project in projects:
    df = pd.read_csv(f'../comments-with-labels/Final/{project}_allLevel_comment.csv')
    df_updated = my_update(updater, df, 'comment', 'label')
    df_updated.to_csv(f'../comments-with-labels-checked/Final/{project}_allLevel_comment.csv', index=False, encoding=encoding)