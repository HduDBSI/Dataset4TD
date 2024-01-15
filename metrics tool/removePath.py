import pandas as pd
import sys
sys.path.append("../")
from time import time
from project_Info import projects

def remove(file:str):
    df = pd.read_csv(file, encoding="gbk")
    s = df['file'][0]
    idx = s.find('\\..')+1
    df['file'] = df['file'].str.slice(idx)
    df.rename(columns={'file': 'FilePath'}, inplace=True) 
    df.to_csv(file, index=False)

t = time()
granularities = ["class", "method"]
for project in projects:
    for granularity in granularities:
            remove('../metrics/'+project+'-'+granularity+'.csv')
print('cost time:', time()-t)