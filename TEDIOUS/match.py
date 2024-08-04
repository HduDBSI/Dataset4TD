import pandas as pd
import sys
sys.path.append("../") 
from project_Info import projects, project_names
import re
import time
import os
import numpy as np

columns_order = ['FilePath', 'LineNum', 'Rule']

pmd_rules = [
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

cs_rules = [
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

total_rules = pmd_rules + cs_rules

method_info = [
    'FilePath', 'MethodName', 'Content', 'StartLine', 
    'EndLine', 'CommentsAssociatedLabel', 'ParNbr',
    'McCabe', 'LOC', 'DeclNbr', 'ExprStmtNbr', 'CommentNbr'
]

from javalang import parse, tree
def compute_DeclNbr_ExprStmtNbr(code: str) -> str:
    DeclNbr, ExprStmtNbr = 0, 0
    try:
        ast = parse.parse('public class A{' + code + '}')
        for _, node in ast:
            if type(node) == tree.VariableDeclaration:
                DeclNbr += 1
            elif type(node) == tree.StatementExpression:
                ExprStmtNbr += 1
    except:
        # print('parse error')
        pass
    return f'{DeclNbr},{ExprStmtNbr}'

def compute_CommentNbr(comments: str) -> int:
    comment_list = comments.split('[[SEP]]')
    return len(comment_list)

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
 
    cs = pd.DataFrame({'FilePath': filePaths, 'LineNum': lineNums, 'Rule': rules})
    
    return cs[columns_order]

def readPMD(file):
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
    
    pmd = pd.read_csv(file, sep=':\t', header=None, names=['FilePath', 'Rule', 'Description'], encoding='gbk')
    pmd.drop('Description', axis=1, inplace=True)
    
    java_idx = pmd['FilePath'].str.contains('.java')
    pmd = pmd[java_idx]
    
    pmd.reset_index(drop=True, inplace=True)
    
    filePaths, lineNums = getFilePathAndLineNum(pmd['FilePath'].tolist())
    pmd['FilePath'], pmd['LineNum'] = filePaths, lineNums
    
    return pmd[columns_order]

def myReplace(s:str) -> str:
    return s.replace('..\\', '')

def readMethod(file):
    
    method = pd.read_csv(file)
    
    method['FilePath'] = method['FilePath'].apply(myReplace)
    
    method['DeclNbr,ExprStmtNbr'] = method['Content'].apply(compute_DeclNbr_ExprStmtNbr)
    method[['DeclNbr','ExprStmtNbr']] = method['DeclNbr,ExprStmtNbr'].str.split(',', expand=True)
    method.drop('DeclNbr,ExprStmtNbr', axis=1, inplace=True)

    method['CommentNbr'] = method['CommentsAssociated'].apply(compute_CommentNbr)
    
    method.rename(columns={'parametersQty': 'ParNbr', 'loc': 'LOC', 'wmc': 'McCabe'}, inplace=True)
  
    return method[method_info]

def match(cs_file, pmd_file, method_file, merged_file):
    df_cs, df_pmd, df_method = readCS(cs_file), readPMD(pmd_file), readMethod(method_file)
    df_metrics = pd.concat([df_cs, df_pmd], ignore_index=True).reset_index(drop=True)

    dummies = pd.get_dummies(df_metrics['Rule'])
    counts = dummies.sum() # count for each column

    df_metrics = pd.concat([df_metrics[['FilePath', 'LineNum']], dummies], axis=1)
    df_metrics.columns = ['FilePath', 'LineNum', *counts.index]

    missing_rules = list(set(total_rules) - set(counts.index))
    for missing_rule in missing_rules:
        df_metrics[missing_rule] = 0

    merged = pd.merge(df_method, df_metrics, on=['FilePath'], how='inner')
    merged = merged[(merged['LineNum'].between(merged['StartLine'], merged['EndLine']))]
    
    merged.reset_index(drop=True, inplace=True)
    
    merged = merged.groupby(method_info).sum().reset_index()

    df_method['TMP'] = df_method['FilePath'] + df_method['StartLine'].astype(str) + df_method['EndLine'].astype(str)
    merged['TMP'] = merged['FilePath'] + merged['StartLine'].astype(str) + merged['EndLine'].astype(str)
    idx = ~(df_method['TMP'].isin(merged['TMP']))
    merged = pd.concat([merged, df_method[idx]], ignore_index=True).reset_index(drop=True)
    merged.fillna(0, inplace=True)
    
    merged['TMP'] = pd.Categorical(merged['TMP'], categories=df_method['TMP'], ordered=True)
    merged = merged.sort_values('TMP').reset_index(drop=True)
    merged['TMP'] = merged['TMP'].astype(str)

    merged.drop(['LineNum', 'TMP'], axis=1, inplace=True)

    merged.to_csv(merged_file, index=False)

times = []
for project in projects:
    t = time.time()
    cs_file = f'csResults/{project}_cs.csv'
    pmd_file = f'pmdResults/{project}_pmd.csv'
    method_file = f'../code snippets-with-labels&metrics/method/{project}_methodLevel.csv'
    merged_file = f'MatchResults/{project}_Matched.csv'
    os.makedirs('MatchResults', exist_ok=True)
    match(cs_file, pmd_file, method_file, merged_file)
    times.append(time.time() - t)
    print(project, 'done.')

with open('results/time2.txt', 'w') as f:
    for t, project in zip(times, project_names):
        f.write("{}\t{:.2f}\n".format(project, t))
    f.write("Median\t{:.2f}\n".format(np.median(times)))
    f.write("Total\t{:.2f}\n".format(np.sum(times)))


print('cost time:', sum(times))
