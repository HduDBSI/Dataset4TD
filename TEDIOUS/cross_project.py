import sys
sys.path.append("../") 
from project_Info import projects, project_names
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import StratifiedKFold
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
import time
import numpy as np
random_state = 1

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

metrics = code_metrics + cs_metrics + pmd_metrics

def cross(test_file, train_files):

    # load test set
    test = pd.read_csv(test_file)
    X_test, y_test = test[metrics], test['CommentsAssociatedLabel']

    # load train set
    X_train_list = []
    y_train_list = []
    for train_file in train_files:
        train = pd.read_csv(train_file)

        X_train_list.append(train[metrics])
        y_train_list.append(train['CommentsAssociatedLabel'])
    
    X_train = pd.concat(X_train_list, axis=0)
    y_train = pd.concat(y_train_list, axis=0)
    
    X_train.reset_index(drop=True, inplace=True)
    y_train.reset_index(drop=True, inplace=True)
    
    # init classifier
    clf = LGBMClassifier(n_jobs=12, random_state=random_state, n_estimators=500, learning_rate=0.05)
    
    # train
    clf.fit(X_train, y_train)
    
    # predict
    y_pred = clf.predict(X_test)

    # calculate accuracy, precision, recall, f1-score
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("Accuracy:{:.2%}".format(accuracy))
    print("Precision:{:.2%}".format(precision))
    print("Recall:{:.2%}".format(recall))
    print("F1-score:{:.2%}".format(f1))
    
    return precision, recall, f1

import time
t = time.time()

latex_matrix = []
for project in projects:
    test_project = project
    train_projects = projects.copy()
    train_projects.remove(test_project)
    latex_line = []

    test_file = f'MatchResults/{test_project}_Matched.csv'
    train_files = [(f'MatchResults/{train_project}_Matched.csv') for train_project in train_projects]
    print('===='+project+'====')
    p, r, f = cross(test_file, train_files)
    latex_line = latex_line + [p, r, f]
    latex_matrix.append(latex_line)

print(time.time()-t)

from LatexTable import *
avgs = avgEachColumn(latex_matrix)
matrix = insertRow(latex_matrix, avgs, len(latex_matrix))
project_names.append('\\textbf{Average}')
matrix = insertColumn(matrix, project_names, 0)
writeTable(matrix, 'cross_project.txt')