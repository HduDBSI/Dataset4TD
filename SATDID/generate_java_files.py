import pandas as pd
import sys
import os
from tqdm import tqdm
import time
sys.path.append("../") 
from project_Info import projects, project_names
import numpy as np

def generate_file(file_path, text):
    with open(file_path, "w", encoding='utf-8') as f:
        f.write('public class A{ public void B (){ ' + text + '}}')
    

def generate_files(project):
    df = pd.read_csv(f'../code snippets-with-labels&metrics/block/{project}_blockLevel.csv', encoding='utf-8')
    for i in tqdm(range(len(df))):
        id, label, code = df['ID'][i], df['CommentsAssociatedLabel'][i], df['Content'][i]
        file_path = f'data/java_files/{project}/Test{id}_{label}.java'
        generate_file(file_path, code)


times = []
for project in projects:
    t = time.time()
    if not os.path.exists(f'data/java_files/{project}'):
        os.mkdir(f'data/java_files/{project}')
    generate_files(project)
    times.append(time.time()-t)

with open('results/time1.txt', 'w') as f:
    for t, project in zip(times, project_names):
        f.write("{}\t{:.2f}\n".format(project, t))
    f.write("Median\t{:.2f}\n".format(np.median(times)))
    f.write("Total\t{:.2f}\n".format(np.sum(times)))

print('cost time:', sum(times))
