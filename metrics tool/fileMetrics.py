import pandas as pd
import sys
sys.path.append("../../") 
from project_Info import projects
from time import time

t = time()
for project in projects:
    m = pd.read_csv('../metrics/'+project+'-class.csv')
    m_group = m.groupby('FilePath').sum()
    m_group.to_csv('../metrics/'+project+'-file.csv')
print('cost time:', time()-t)
