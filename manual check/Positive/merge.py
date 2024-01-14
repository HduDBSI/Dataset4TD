import pandas as pd
encoding = 'utf-8-sig'

df1 = pd.read_csv("positive-withKeywords-1manChecked.csv", encoding=encoding)
df2 = pd.read_csv("positive-withoutKeywords-3manChecked.csv", encoding=encoding)

df3 = df2[['comment', 'label3']]
df3.rename(columns={'label3':'label'}, inplace=True)

new_df = pd.concat([df1, df3], axis=0)
new_df.to_csv('positive.csv', index=False, encoding=encoding)