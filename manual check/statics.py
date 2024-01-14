import pandas as pd
encoding='utf-8-sig'

df = pd.read_csv('all_comment.csv', encoding=encoding)
print('All:', len(df))
label_counts = df['label'].value_counts()

print(label_counts)


df = pd.read_csv('Negative/negative-uncertain-2manCheck1', encoding=encoding)
print('One Vote SATD:', len(df))



df = pd.read_csv('Positive/positive-withKeywords-1manCheck.csv', encoding=encoding)
print('Keywords:', len(df))



df = pd.read_csv('Positive/positive-withoutKeywords-2manCheck1.csv', encoding=encoding)
print('No Keywords:', len(df))



df = pd.read_csv('Gold Standard.csv', encoding=encoding)
print('Gold:', len(df))

