import pandas as pd
import sys
import os
from tqdm import tqdm
sys.path.append("../") 
from project_Info import projects
import time

rules = [
    'AvoidReassigningParameters',
    'CollapsibleIfStatements',
    'EmptyIfStmt',
    'IfStmtsMustUseBraces',
    'LocalVariableCouldBeFinal',
    'MethodArgumentCouldBeFinal', 
    'ShortVariable', 
    'SwitchStmtsShouldHaveDefault',
    'OptimizableToArrayCall', 
    'UseStringBufferForStringAppends',                
    'UselessParentheses', 
]

method_info = [
    'FilePath', 'MethodName', 'Content', 'StartLine', 
    'EndLine', 'CommentsAssociatedLabel', 'ParNbr',
    'McCabe', 'LOC'
]

# position = '..\projects\antlr4-4.11.0\runtime\JavaScript\src\antlr4\atn\ATNDeserializer.js:74'
    # filePath = '..\projects\antlr4-4.11.0\runtime\JavaScript\src\antlr4\atn\ATNDeserializer.js'
    # lineNum = 74
def getFilePathAndLineNum(positions):
    filePaths, lineNums = [], []
    for position in positions:
        filePath, lineNum = position.split(':')[:2]
        filePath = filePath.replace('..\\', '')
        try:
            lineNum = int(lineNum.strip())
        except:
            lineNum = 0

        filePaths.append(filePath)
        lineNums.append(lineNum)
    
    return filePaths, lineNums

def readPMD(file):
    pmd = pd.read_csv(file, sep=':\t', header=None, names=['FilePath', 'Rule', 'Description'], encoding='gbk')
    
    pmd.drop('Description', axis=1, inplace=True)
    
    java_idx = pmd['FilePath'].str.contains('.java')
    pmd = pmd[java_idx]
    
    pmd.reset_index(drop=True, inplace=True)
    
    filePaths, lineNums = getFilePathAndLineNum(pmd['FilePath'].values.tolist())
    pmd['FilePath'], pmd['LineNum'] = filePaths, lineNums
    
    return pmd

def readMethod(file):
    method = pd.read_csv(file)
    
    for i in range(len(method)):
        method['FilePath'][i] = method['FilePath'][i].replace('..\\', '')

    method.rename(columns={'parametersQty': 'ParNbr', 'loc': 'LOC', 'wmc': 'McCabe'}, inplace=True)
    
    return method[method_info]

def match_fast(pmdFile, methodFile, matchedFile):
    t = time.time()
    pmd, method = readPMD(pmdFile), readMethod(methodFile)

    dummies = pd.get_dummies(pmd['Rule'])
    counts = dummies.sum() # count for each column

    pmd = pd.concat([pmd[['FilePath', 'LineNum']], dummies], axis=1)
    pmd.columns = ['FilePath', 'LineNum', *counts.index]

    missings = list(set(rules) - set(counts.index))
    for missing in missings:
        pmd[missing] = 0
    
    merged = pd.merge(method, pmd, on=['FilePath'], how='inner')
    
    merged = merged[(merged['LineNum'].between(merged['StartLine'], merged['EndLine']))]
    merged.reset_index(drop=True, inplace=True)
    
    merged = merged.groupby(method_info).sum().reset_index()
    merged.drop('LineNum', axis=1, inplace=True)
    
    merged.to_csv(matchedFile, index=False)
    print(time.time()-t)


def match_slow(pmdFile, methodFile, matchedFile):
    t = time.time()
    pmd, method = readPMD(pmdFile), readMethod(methodFile)
    
    rules_count = {rule: [] for rule in rules}
    
    for i in tqdm(range(len(method))):      
        startLine, endLine = method['StartLine'][i], method['EndLine'][i]
        
        idx_same_path = pmd['FilePath'] == method['FilePath'][i]
        idx_between_lines = (startLine <= pmd['LineNum']) & (pmd['LineNum'] <= endLine)

        idx_match = idx_same_path & idx_between_lines

        # pmd_match contains matched data, while pmd removes the matched data
        pmd_match, pmd = pmd[idx_match], pmd[~idx_match]
     
        pmd_match.reset_index(drop=True, inplace=True)
        pmd.reset_index(drop=True, inplace=True)

        if len(pmd_match) == 0:
            for key in rules_count.keys():
                rules_count[key].append(0)
        else:
            for key in rules_count.keys():
                rules_count[key].append(pmd_match['Rule'].str.contains(key).sum())
    
    df_metrics = pd.DataFrame(rules_count)
    merged = pd.concat([method_info, df_metrics], axis=1)

    merged.to_csv(matchedFile, index=False)
    print(time.time()-t)


for project in projects:
    pmdFile = f'pmdResults/{project}_pmd.csv'
    methodFile = f'../code snippets-with-labels&metrics/method/{project}_methodLevel.csv'
    matchedFile = f'pmdMatchResults/{project}_pmdMatched.csv'
    os.makedirs('pmdMatchResults', exist_ok=True)
    match_fast(pmdFile, methodFile, matchedFile)

