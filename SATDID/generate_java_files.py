import pandas as pd
import sys
import os
from tqdm import tqdm
from time import time
sys.path.append("../") 
from project_Info import projects

def generate_file(file_path, text):
    with open(file_path, "w", encoding='utf-8') as f:
        f.write('public class A{ public void B (){ ' + text + '}}')
    

def generate_files(project):
    df = pd.read_csv(f'../code snippets-with-labels&metrics/block/{project}_blockLevel.csv', encoding='utf-8')
    for i in tqdm(range(len(df))):
        id, label, code = df['ID'][i], df['CommentsAssociatedLabel'][i], df['Content'][i]
        file_path = f'data/java_files/{project}/Test{id}_{label}.java'
        generate_file(file_path, code)

t = time()
for project in projects:
    os.makedirs(f'data/java_files/{project}', exist_ok=True)
    generate_files(project)
print('cost time:', time()-t)