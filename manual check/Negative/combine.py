import pandas as pd
encoding = 'utf-8-sig'

df1 = pd.read_csv("negative-uncertain-2manCheck1.csv")
df2 = pd.read_csv("negative-uncertain-2manCheck2.csv")

merged_df = df1.merge(df2, on='comment')

merged_df = merged_df.rename(columns={'label_x': 'label1', 'label_y': 'label2'})

idx1 = merged_df['label1'] == 1
idx2 = merged_df['label2'] == 1

idx = idx1 & idx2

merged_df['label'] = 0
merged_df['label'][idx] = 1

merged_df.to_csv("negative-uncertain-2manChecked.csv", encoding=encoding, index=False)



