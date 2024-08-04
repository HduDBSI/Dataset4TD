import sys
sys.path.append("../") 
from project_Info import projects, project_names
from utils import cal_metrics
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import time
import numpy as np
from LatexTable import *

random_state = 1
label_column_name = 'CommentsAssociatedLabel'

# 6 metrics
code_metrics = [ 
    'LOC', 
    'DeclNbr', 
    'ParNbr',
    'ExprStmtNbr', 
    'McCabe', 
    # 'CommentNbr'
]

# 9 metrics
cs_metrics = [
    'LineLength',
    'FinalParameters',
    'MissingSwitchDefault',
    'LeftCurly',
    'LocalVariableName',
    'MethodLength',
    'ParameterNumber',
    'ParenPad',
    'SimplifyBooleanReturns'
]

# 11 metrics
pmd_metrics = [
    'LocalVariableCouldBeFinal',
    'AvoidReassigningParameters',
    'CollapsibleIfStatements',
    'EmptyIfStmt',
    'IfStmtsMustUseBraces',
    'MethodArgumentCouldBeFinal',
    'OptimizableToArrayCall',
    'ShortVariable',
    'SwitchStmtsShouldHaveDefault',
    'UselessParentheses',
    'UseStringBufferForStringAppends'
]

total_metrics = code_metrics + cs_metrics + pmd_metrics

def cross(test_file, train_files):

    # load test set
    test = pd.read_csv(test_file)
    X_test, y_test = test[total_metrics], test[label_column_name]

    # load train set
    X_train_list = []
    y_train_list = []
    for train_file in train_files:
        train = pd.read_csv(train_file)

        X_train_list.append(train[total_metrics])
        y_train_list.append(train[label_column_name])
    
    X_train = pd.concat(X_train_list, axis=0)
    y_train = pd.concat(y_train_list, axis=0)
    
    X_train.reset_index(drop=True, inplace=True)
    y_train.reset_index(drop=True, inplace=True)
    
    # init classifier
    clf = RandomForestClassifier(n_jobs=12, random_state=random_state)
    
    # train
    clf.fit(X_train, y_train)
    
    # predict
    y_pred = clf.predict(X_test)
    y_pred_prob = clf.predict_proba(X_test)[:, 1]

    # calculate metrics
    metrics = cal_metrics(y_test, y_pred, y_pred_prob)

    print("Mean Accuracy:{:.2f}".format(metrics['ACC']))
    print("Mean Precision:{:.2f}".format(metrics['P']))
    print("Mean Recall:{:.2f}".format(metrics['R']))
    print("Mean F1-score:{:.2f}".format(metrics['F1']))
    print("Mean AUC: {:.2f}".format(metrics['AUC']))
    print("Mean MCC: {:.2f}".format(metrics['MCC']))
    
    return metrics

t = time.time()

latex_matrix = []
for project in projects:
    test_project = project
    train_projects = projects.copy()
    train_projects.remove(test_project)
    test_file = f'MatchResults/{test_project}_Matched.csv'
    train_files = [(f'MatchResults/{train_project}_Matched.csv') for train_project in train_projects]
    print('===='+project+'====')
    metrics = cross(test_file, train_files)
    latex_line = [metrics['P'], metrics['R'], metrics['F1'], metrics['AUC'], metrics['MCC']]
    latex_matrix.append(latex_line)

print(time.time()-t)

avgs = avgEachColumn(latex_matrix)
matrix = insertRow(latex_matrix, avgs, len(latex_matrix))
project_names.append('\\textbf{Average}')
matrix = insertColumn(matrix, project_names, 0)
writeTable(matrix, 'results/cross_project.txt')
