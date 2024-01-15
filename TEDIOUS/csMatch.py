import pandas as pd
import sys
import os
from tqdm import tqdm
sys.path.append("../") 
from project_Info import projects
import re
import time
rules = [
    'LineLength',
    'FinalParameters',
    'MissingSwitchDefault',
    'LeftCurly',                
    'LocalVariableName',       
    'MethodLength', 
    'ParameterNumber',     
    'ParenPad',              
    'SimplifyBooleanReturns', 
]

method_info = [
    'FilePath', 'MethodName', 'Content', 'StartLine', 
    'EndLine', 'CommentsAssociatedLabel', 'ParNbr',
    'McCabe', 'LOC'
]

def readCS(file):
    pattern = r'\[ERROR\] (.+?):(\d+)(?::(\d+))?: (.+) \[(.+)\]'
    filePaths, lineNums, rules = [], [], []

    with open(file, 'r', encoding='utf-8') as f:
        # read all lines, skipping first line and last line.
        lines = f.readlines()[1:-1] 

        for line in lines:
            match = re.match(pattern, line)
            if match:
                filePath = match.group(1)
                lineNum = match.group(2)
                columnNum = match.group(3)
                discription = match.group(4)
                rule = match.group(5)
                
                # remove useless path
                index = filePath.find('..')
                filePath = filePath[index+3:]
                filePaths.append(filePath)
                lineNums.append(int(lineNum))
                rules.append(rule)
            else:
                print("No match found.")
                print(line)
    cs = pd.DataFrame()
    cs['FilePath'], cs['LineNum'], cs['Rule'] = filePaths, lineNums, rules
    
    return cs

def readMethod(file):
    method_info = pd.read_csv(file)
    
    for i in range(len(method_info)):
        method_info['FilePath'][i] = method_info['FilePath'][i].replace('..\\', '')

    return method_info

def match_fast(pmdFile, methodFile, matchedFile):
    t = time.time()
    cs, method_info = readCS(pmdFile), readMethod(methodFile)

    dummies = pd.get_dummies(cs['Rule'])
    counts = dummies.sum() # count for each column

    cs = pd.concat([cs[['FilePath', 'LineNum']], dummies], axis=1)
    cs.columns = ['FilePath', 'LineNum', *counts.index]

    missings = list(set(rules) - set(counts.index))
    for missing in missings:
        cs[missing] = 0
    
    merged = pd.merge(method_info, cs, on=['FilePath'], how='inner')
    merged = merged[(merged['LineNum'].between(merged['StartLine'], merged['EndLine']))]
    merged.reset_index(drop=True, inplace=True)
    merged = merged.groupby(['FilePath', 'MethodName', 'Content', 'StartLine', 'EndLine', 'CommentsAssociatedLabel']).sum().reset_index()

    merged.drop('LineNum', axis=1, inplace=True)
    merged.to_csv(matchedFile, index=False)
    print(time.time()-t)

def match_slow(csFile, methodFile, matchedFile):
    t = time.time()
    cs, method_info = readCS(csFile), readMethod(methodFile)
    
    rules_count = {rule: [] for rule in rules}

    for i in tqdm(range(len(method_info))):
        startLine, endLine = method_info['StartLine'][i], method_info['EndLine'][i]
        
        idx_same_path = cs['FilePath'] == method_info['FilePath'][i]
        idx_between_lines = (startLine <= cs['LineNum']) & (cs['LineNum'] <= endLine)

        idx_match = idx_same_path & idx_between_lines

        # cs_match contains matched data, while cs removes the matched data
        cs_match, cs = cs[idx_match], cs[~idx_match]

        cs_match.reset_index(drop=True, inplace=True)
        cs.reset_index(drop=True, inplace=True)

        if len(cs_match) == 0:
            for key in rules_count.keys():
                rules_count[key].append(0)
        else:
            for key in rules_count.keys():
                rules_count[key].append(cs_match['Rule'].str.contains(key).sum())
    
    df_metrics = pd.DataFrame(rules_count)
    merged = pd.concat([method_info, df_metrics], axis=1)

    merged.to_csv(matchedFile, index=False)
    print(time.time()-t)

for project in projects:
    csFile = f'csResults/{project}_cs.csv'
    methodFile = f'../code snippets-with-labels&metrics/method/{project}_methodLevel.csv'
    matchedFile = f'csMatchResults/{project}_csMatched.csv'
    os.makedirs('csMatchResults', exist_ok=True)
    # match_slow(csFile, methodFile, matchedFile)
    match_fast(csFile, methodFile, matchedFile)
