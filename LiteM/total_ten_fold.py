import sys
sys.path.append("..")
from project_Info import *
from LatexTable import *
from sklearn.model_selection import StratifiedKFold
from lightgbm import LGBMClassifier
import pandas as pd
import numpy as np
from utils import cal_metrics
import time

random_state = 1
label_column_name = 'CommentsAssociatedLabel'
def makeXy(granularity):

    X_list, y_list = [], []
    for project in projects:
        file_name = f'../code snippets-with-labels&metrics/{granularity}/{project}_{granularity}Level.csv'
        data = pd.read_csv(file_name)
        data.columns = data.columns.str.lower()

        # define features and labels
        if granularity == 'file':
            X_tmp = data[file_feature_names_lowercase]
        elif granularity == 'class':
            X_tmp = data[class_feature_names_lowercase]
        elif granularity == 'method':
            X_tmp = data[method_feature_names_lowercase]
        else:
            X_tmp = data[block_feature_names_lowercase]

        y_tmp = data[label_column_name.lower()]
        
        X_list.append(X_tmp)
        y_list.append(y_tmp)

    X = pd.concat(X_list, axis=0)
    y = pd.concat(y_list, axis=0)
    X.reset_index(drop=True, inplace=True)
    y.reset_index(drop=True, inplace=True)
    
    return X, y

# ten folds cross validation
def ten_folds(granularity):
    # load dataset
    X, y = makeXy(granularity)
    
    # create StratifiedKFold object
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=random_state)

    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    AUCs = []
    MCCs = []

    X = X.fillna(-1)
    # loop for cross validation
    for train_index, test_index in skf.split(X, y):
        # label evenly distributed
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
   
        clf = LGBMClassifier(random_state=random_state, n_jobs=12, n_estimators=500, learning_rate=0.05)
        
        # train 
        clf.fit(X_train, y_train)
       
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
    mean_accuracy = sum(accuracies) / len(accuracies)
    mean_precision = sum(precisions) / len(precisions)
    mean_recall = sum(recalls) / len(recalls)
    mean_f1_score = sum(f1_scores) / len(f1_scores)
    mean_auc = sum(AUCs) / len(AUCs)
    mean_mcc = sum(MCCs) / len(MCCs)
    
    print("Mean Accuracy:{:.2f}".format(mean_accuracy))
    print("Mean Precision:{:.2f}".format(mean_precision))
    print("Mean Recall:{:.2f}".format(mean_recall))
    print("Mean F1-score:{:.2f}".format(mean_f1_score))
    print("Mean AUC: {:.2f}".format(mean_auc))
    print("Mean MCC: {:.2f}".format(mean_mcc))

    return mean_precision, mean_recall, mean_f1_score, mean_auc, mean_mcc

def normalize_list(lst):
    min_value = min(lst)
    max_value = max(lst)
    return [(x - min_value) / (max_value - min_value) for x in lst]

t = time.time()
latex_matrix = []

for granularity in granularities:
    print('===='+granularity+'====')
    p, r, f, auc, mcc = ten_folds(granularity)
    latex_line = [p, r, f, auc, mcc]
    latex_matrix.append(latex_line)

print(time.time()-t)

avgs = avgEachColumn(latex_matrix)
latex_matrix = insertRow(latex_matrix, avgs, len(latex_matrix))
latex_matrix = insertColumn(latex_matrix, ['File', 'Class', 'Method', 'Block', 'Average'], 0)
writeTable(latex_matrix, 'results/total_ten_fold.txt')
