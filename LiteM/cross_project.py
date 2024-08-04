import sys
sys.path.append("..")
from project_Info import *
import pandas as pd
from lightgbm import LGBMClassifier
from utils import cal_metrics
import time

random_state = 1
label_column_name = 'CommentsAssociatedLabel'

def cross(test_file, train_files, granularity):
    # define features and labels
    if granularity == 'file':
        feature_names = file_feature_names_lowercase
    elif granularity == 'class':
        feature_names = class_feature_names_lowercase
    elif granularity == 'method':
        feature_names = method_feature_names_lowercase
    else:
        feature_names = block_feature_names_lowercase

    # load test set
    test = pd.read_csv(test_file)
    test.columns = test.columns.str.lower()
    X_test, y_test = test[feature_names], test[label_column_name.lower()]

    # load train set
    X_train_list = []
    y_train_list = []
    for train_file in train_files:
        train = pd.read_csv(train_file)
        train.columns = train.columns.str.lower()

        X_train_list.append(train[feature_names])
        y_train_list.append(train[label_column_name.lower()])
    
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
    latex_line = []
    for granularity in granularities:
        test_file = f'../code snippets-with-labels&metrics/{granularity}/{test_project}_{granularity}Level.csv'
        train_files = [(f'../code snippets-with-labels&metrics/{granularity}/{train_project}_{granularity}Level.csv') for train_project in train_projects]
        print('===='+project, granularity+'====')
        metrics = cross(test_file, train_files, granularity)
        latex_line = latex_line + [metrics['P'], metrics['R'], metrics['F1'], metrics['AUC'], metrics['MCC']]
    latex_matrix.append(latex_line)

print(time.time()-t)

from LatexTable import *
avgs = avgEachColumn(latex_matrix)
matrix = insertRow(latex_matrix, avgs, len(latex_matrix))
project_names.append('\\textbf{Average}')
matrix = insertColumn(matrix, project_names, 0)
writeTable(matrix, 'results/cross_project.txt')
