import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
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

neg = pd.read_csv('Negative/negative.csv', encoding=encoding)
pos = pd.read_csv('Positive/positive.csv', encoding=encoding)

actual = neg['label'].tolist() + pos['label'].tolist()
predicted = [0] * len(neg) + [1] * len(pos)

acc = accuracy_score(actual, predicted)
precision = precision_score(actual, predicted)
recall = recall_score(actual, predicted)
f1 = f1_score(actual, predicted)

print(acc,  precision, recall, f1)

com = pd.concat([pos, neg], axis=0)
com.to_csv('Gold Standard.csv', encoding=encoding, index=False)


all = pd.read_csv('all_comment.csv', encoding=encoding)

all_updated = my_update(com, all, 'comment', 'label')
all_updated.to_csv('all_comment_checked.csv', encoding=encoding, index=False)

deprecated_idx = all_updated['comment'].str.contains('@deprecated|@Deprecated', case=False)
all_updated.loc[deprecated_idx, 'label'] = 1
all_updated.to_csv('all_comment_checked_deprecated.csv', encoding=encoding, index=False)


