import sys
sys.path.append("../") 
from project_Info import projects, project_names
from utils import cal_metrics
from LatexTable import *
from sklearn.model_selection import StratifiedKFold
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
import time
import numpy as np
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

# k folds cross validation
def k_folds_train(project, k_fold=10):
    # load dataset
    file_name = f'MatchResults/{project}_Matched.csv'
    data = pd.read_csv(file_name)

    # define features and labels
    X, y = data[total_metrics], data[label_column_name]
    
    # create StratifiedKFold object
    skf = StratifiedKFold(n_splits=k_fold, shuffle=True, random_state=random_state)

    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    AUCs = []
    MCCs = []
    start_time = time.time()
    X = X.fillna(-1)

    # loop ten times for cross validation
    for train_index, test_index in skf.split(X, y):
        # label evenly distributed
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        # over sampling
        smote = SMOTE(random_state=random_state)
        X_train_resample, y_train_resample = smote.fit_resample(X_train, y_train)
    
        # init classifier
        clf = RandomForestClassifier(random_state=random_state, n_jobs=12)
        
        # train 
        clf.fit(X_train_resample, y_train_resample)
        
        # predict
        y_pred = clf.predict(X_test)
        y_pred_prob = clf.predict_proba(X_test)[:, 1]

        # calculate metrics
        metrics = cal_metrics(y_test, y_pred, y_pred_prob)

        # save this round result
        accuracies.append(metrics['ACC'])
        precisions.append(metrics['P'])
        recalls.append(metrics['R'])
        f1_scores.append(metrics['F1'])
        AUCs.append(metrics['AUC'])
        MCCs.append(metrics['MCC'])

    # calculate average
    mean_accuracy = sum(accuracies) / k_fold
    mean_precision = sum(precisions) / k_fold
    mean_recall = sum(recalls) / k_fold
    mean_f1_score = sum(f1_scores) / k_fold
    cost_time = time.time()-start_time
    mean_auc = sum(AUCs) / k_fold
    mean_mcc = sum(MCCs) / k_fold

    print("Mean Accuracy:{:.2f}".format(mean_accuracy))
    print("Mean Precision:{:.2f}".format(mean_precision))
    print("Mean Recall:{:.2f}".format(mean_recall))
    print("Mean F1-score:{:.2f}".format(mean_f1_score))
    print("Mean AUC: {:.2f}".format(mean_auc))
    print("Mean MCC: {:.2f}".format(mean_mcc))
    print("Cost Time: {:.2f} seconds".format(cost_time))

    return mean_precision, mean_recall, mean_f1_score, cost_time, mean_auc, mean_mcc

latex_matrix = []
times = []
for project in projects:
    print('===='+project+'====')
    p, r, f, t, auc, mcc = k_folds_train(project)
    latex_matrix.append([p, r, f, auc, mcc])
    times.append(t)

avgs = avgEachColumn(latex_matrix)
matrix = insertRow(latex_matrix, avgs, len(latex_matrix))
project_names.append('\\textbf{Average}')
matrix = insertColumn(matrix, project_names, 0)
writeTable(matrix, 'results/within_project.txt')

with open(f'results/time3.txt', 'w') as f:
    for t, project in zip(times, project_names):
        f.write("{}\t{:.2f}\n".format(project, t))
    f.write("Median\t{:.2f}\n".format(np.median(times)))
    f.write("Total\t{:.2f}\n".format(np.sum(times)))
