import sys
sys.path.append("..")
from project_Info import *
from LatexTable import *
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import StratifiedKFold
from lightgbm import LGBMClassifier
import pandas as pd
from imblearn.over_sampling import SMOTE
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

def makeXy():

    X_list, y_list = [], []
    for project in projects:
        file_name = f'MatchResults/{project}_Matched.csv'
        data = pd.read_csv(file_name)

        # define features and labels

        X_tmp = data[metrics]
        y_tmp = data['CommentsAssociatedLabel']
        
        X_list.append(X_tmp)
        y_list.append(y_tmp)

    X = pd.concat(X_list, axis=0)
    y = pd.concat(y_list, axis=0)
    X.reset_index(drop=True, inplace=True)
    y.reset_index(drop=True, inplace=True)
    
    return X, y


# ten fold cross validation
def ten_fold():
    # load dataset
    X, y = makeXy()
    
    # create StratifiedKFold object
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=random_state)

    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    feature_importances = []
    
    X = X.fillna(-1)
    # loop for cross validation
    for train_index, test_index in skf.split(X, y):
        # label evenly distributed
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
   
        X_train_resample, y_train_resample = X_train, y_train
        clf = LGBMClassifier(objective='binary', metric='binary_logloss', random_state=random_state, n_jobs=12)
        
        # train 
        clf.fit(X_train_resample, y_train_resample)
       
        # predict
        y_pred = clf.predict(X_test)

        # record importances
        importance = clf.feature_importances_
        feature_importances.append(importance)
        
        # calculate accuracy, precision, recall, f1-score
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # save this round result
        accuracies.append(accuracy)
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)

    # calculate average
    mean_accuracy = sum(accuracies) / len(accuracies)
    mean_precision = sum(precisions) / len(precisions)
    mean_recall = sum(recalls) / len(recalls)
    mean_f1_score = sum(f1_scores) / len(f1_scores)

    print("Mean Accuracy:{:.2%}".format(mean_accuracy))
    print("Mean Precision:{:.2%}".format(mean_precision))
    print("Mean Recall:{:.2%}".format(mean_recall))
    print("Mean F1-score:{:.2%}".format(mean_f1_score))
    return mean_precision, mean_recall, mean_f1_score

import time
t = time.time()
p, r, f = ten_fold()
print(time.time()-t)

with open('total_ten_fold.txt',"w") as ff:
    ff.write(f'P, R, F\n{p}, {r}, {f}')


