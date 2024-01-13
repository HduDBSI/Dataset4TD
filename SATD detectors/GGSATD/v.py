import pandas as pd

df = pd.read_csv('data/technical_debt_dataset.csv')

projects = ['apache-ant-1.7.0', 'apache-jmeter-2.10', 'argouml', 'columba-1.4-src',
 'emf-2.4.1', 'hibernate-distribution-3.3.2.GA', 'jEdit-4.2',
 'jfreechart-1.0.19', 'jruby-1.4.0', 'sql12']

# 创建透视表
pivot_table = pd.pivot_table(df, values='classification', index='projectname', columns='classification', aggfunc='size', fill_value=0)
classification = ['DEFECT', 'DESIGN', 'IMPLEMENTATION', 'TEST', 'WITHOUT_CLASSIFICATION',
    'DOCUMENTATION']
# 选取指定的项目和类别
pivot_table = pivot_table.loc[projects, classification]

print(pivot_table)
