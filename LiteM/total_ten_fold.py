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

        y_tmp = data['CommentsAssociatedLabel'.lower()]
        
        X_list.append(X_tmp)
        y_list.append(y_tmp)

    X = pd.concat(X_list, axis=0)
    y = pd.concat(y_list, axis=0)
    X.reset_index(drop=True, inplace=True)
    y.reset_index(drop=True, inplace=True)
    
    return X, y


# ten folds cross validation
def ten_folds_train(granularity):
    # load dataset
    X, y = makeXy(granularity)
    
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
    mean_feature_importances = np.mean(np.array(feature_importances), axis=0)

    print("Mean Accuracy:{:.2%}".format(mean_accuracy))
    print("Mean Precision:{:.2%}".format(mean_precision))
    print("Mean Recall:{:.2%}".format(mean_recall))
    print("Mean F1-score:{:.2%}".format(mean_f1_score))
    return mean_precision, mean_recall, mean_f1_score, mean_feature_importances

def normalize_list(lst):
    min_value = min(lst)
    max_value = max(lst)
    return [(x - min_value) / (max_value - min_value) for x in lst]


import time
t = time.time()
matrix = []
# granularities.remove('class')
# granularities.remove('method')
importances = []
for granularity in granularities:
    print('===='+granularity+'====')
    p, r, f, i = ten_folds_train(granularity)
    line = [p, r, f]
    importances.append(i)
    matrix.append(line)
print(time.time()-t)


# for importance in importances:
#     print(importance)

avgs = avgEachColumn(matrix)
matrix = insertRow(matrix, avgs, len(matrix))
matrix = insertColumn(matrix, ['File', 'Class', 'Method', 'Block', 'Average'], 0)
writeTable(matrix, 'results/total_ten_fold.txt')