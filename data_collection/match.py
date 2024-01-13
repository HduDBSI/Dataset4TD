# this file is designed to match the code snippet with its metrics
# We study the most common classes and methods, while ignoring internal classes,
# anonymous classes, enum classes and inner interface
import sys
sys.path.append('../')
from LatexTable import *
import pandas as pd
from project_Info import *
from methodSimplifier import *
from time import time
encoding = 'utf-8-sig'
def match_code_with_metrics(cswl_file, m_file, cswlm_file, granularity):
    """
    Match code snippets with metrics

    :param cswl_file: file name of the code snippets with labels
    :type cswl_file: str
    :param m_file: file name of the metrics
    :type m_file: str
    :param cswlm_file: file name of the code snippets with labels and metrics
    :type cswlm_file: str
    :param granularity: granularity of the code snippets
    :type granularity: str
    :return: the number of TD and Non-TD code snippets
    :rtype: tuple
    """
    # read data from files
    cswl = pd.read_csv(cswl_file, encoding=encoding)
    m = pd.read_csv(m_file)

    # merge data based on granularity
    if granularity == 'file':
        subset = ['FilePath']
        cswlm = pd.merge(cswl, m, how='inner', on=subset)
    
    elif granularity == 'class':
        subset = ['FilePath', 'ClassName']
        m['ClassName'] = m['class'].replace({'\$': '.'}, regex=True)
        cswlm = pd.merge(cswl, m, how='inner', on=subset)
        
    elif granularity == 'method':
        subset = ['FilePath', 'ClassName', 'MethodSimplified']
        m['ClassName'] = m['class'].replace({'\$': '.'}, regex=True)

        cswl['MethodSimplified'] = cswl['MethodName'].apply(simplifyMethodSignature1)
        m['MethodSimplified'] = m['method'].apply(simplifyMethodSignature2)

        cswlm = pd.merge(cswl, m, how='inner', on=subset)

        duplicated_indices = cswlm[cswlm.duplicated(subset=subset, keep=False)].index
        mask = abs(cswlm['line'][duplicated_indices] - cswlm['StartLine'][duplicated_indices]) >= 2
        cswlm.drop(index=mask.index[mask], inplace=True)

    elif granularity == 'block':
        subset = ['ID', 'FilePath', 'ClassName', 'MethodName', 'StartLine', 'EndLine']
        cswlm = pd.merge(cswl, m, how='inner', on=subset)
    
    # for debug
    # dup = cswlm.duplicated(subset=subset)
    # if dup.any():
    #     print('has duplicated rows')
    #     print(cswlm['method'][dup].values)
    #     merged = pd.merge(cswl, m, how='outer', on=subset, indicator=True)
    #     cswl_only = merged[merged["_merge"] == "left_only"]
    #     m_only = merged[merged["_merge"] == "right_only"]
    #     print(len(cswlm), len(cswl_only), len(m_only))
    #     cswl_only.to_csv('cswlOnly.csv', index=False)
    #     m_only.to_csv('mOnly.csv', index=False)
    
    # output the results to the file
    cswlm.to_csv(cswlm_file, index=False, encoding=encoding)
    
    counts = cswlm['CommentsAssociatedLabel'].value_counts()
    TD_num = int(counts[1])
    NonTD_num = int(counts[0])

    print(f"metric:{len(m)}, code snippet w/ label:{len(cswl)}, code snippet w/ label&metric:{len(cswlm)}, TD:{TD_num}, NonTD:{NonTD_num}, NotMatch:{len(cswl)-len(cswlm)}")

    return TD_num, NonTD_num

t = time()
matrix = []
for project in projects:
    row = []
    print(project)
    for granularity in granularities:
        cswl_file = f'../code snippets-with-labels/{granularity}/{project}_{granularity}Level.csv'
        m_file = f'../metrics/{project}-{granularity}.csv'
        cswlm_file = f'../code snippets-with-labels&metrics/{granularity}/{project}_{granularity}Level.csv'
        
        TD_num, NonTD_num = match_code_with_metrics(cswl_file, m_file, cswlm_file, granularity)
        row = row + [TD_num, NonTD_num]
    matrix.append(row)
    

matrix = horizontalJoin(all_num, matrix)
sums = sumEachColumn(matrix)
matrix = insertRow(matrix, sums, len(matrix))

file_TD_ratio = listDivision(list_dividend=getColumn(matrix, 4), list_divisor=listAddition(getColumn(matrix, 4), getColumn(matrix, 5)))
class_TD_ratio = listDivision(list_dividend=getColumn(matrix, 6), list_divisor=listAddition(getColumn(matrix, 6), getColumn(matrix, 7)))
method_TD_ratio = listDivision(list_dividend=getColumn(matrix, 8), list_divisor=listAddition(getColumn(matrix, 8), getColumn(matrix, 9)))
block_TD_ratio = listDivision(list_dividend=getColumn(matrix, 10), list_divisor=listAddition(getColumn(matrix, 10), getColumn(matrix, 11)))

# print(file_TD_ratio)
# print(class_TD_ratio)
# print(method_TD_ratio)
# print(block_TD_ratio)
import scipy.io as sio
sio.savemat('ratio.mat', { 
    'file_td_ratio': file_TD_ratio,
    'class_td_ratio': class_TD_ratio, 
    'method_td_ratio': method_TD_ratio,
    'block_td_ratio': block_TD_ratio,
    })

project_names.append('\\textbf{Total}')
matrix = insertColumn(matrix, project_names, 0)
writeTable(matrix, 'distribution.txt')
print('cost time:', time()-t)