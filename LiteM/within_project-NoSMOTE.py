import sys
sys.path.append("..")
from project_Info import *
from LatexTable import *
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import StratifiedKFold
from lightgbm import LGBMClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import numpy as np
import scipy.io as sio
import time
random_state = 1
label_column_name = 'CommentsAssociatedLabel'

# ten folds cross validation
def ten_folds_train(file_name, level, k_fold=10):
    # load dataset
    data = pd.read_csv(file_name)
    data.columns = data.columns.str.lower()

    # define features and labels
    if level == 'file':
        X = data[file_feature_names_lowercase]
    elif level == 'class':
        X = data[class_feature_names_lowercase]
    elif level == 'method':
        X = data[method_feature_names_lowercase]
    else:
        X = data[block_feature_names_lowercase]
    y = data[label_column_name.lower()]
    
    # create StratifiedKFold object
    skf = StratifiedKFold(n_splits=k_fold, shuffle=True, random_state=random_state)

    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    start_time = time.time()
    feature_importances = []
    
    X = X.fillna(-1)

    # loop ten times for cross validation
    for train_index, test_index in skf.split(X, y):
        
        # label evenly distributed
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        # init classifier
        clf = LGBMClassifier(random_state=random_state, n_jobs=12, n_estimators=500, learning_rate=0.05)
        
        # train 
        clf.fit(X_train, y_train)
        
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
    mean_accuracy = sum(accuracies) / k_fold
    mean_precision = sum(precisions) / k_fold
    mean_recall = sum(recalls) / k_fold
    mean_f1_score = sum(f1_scores) / k_fold
    mean_cost_time = (time.time()-start_time) / k_fold
    mean_feature_importances = np.mean(np.array(feature_importances), axis=0)
    mean_feature_importances = normalize_list(mean_feature_importances)
    print("Mean Accuracy:{:.2%}".format(mean_accuracy))
    print("Mean Precision:{:.2%}".format(mean_precision))
    print("Mean Recall:{:.2%}".format(mean_recall))
    print("Mean F1-score:{:.2%}".format(mean_f1_score))

    return mean_precision, mean_recall, mean_f1_score, mean_cost_time, mean_feature_importances

def normalize_list(lst):
    min_value = min(lst)
    max_value = max(lst)
    return [(x - min_value) / (max_value - min_value) for x in lst]



latex_matrix = []

importances = []
times = []
for project in projects:
    latex_line = []
    for granularity in granularities:
        file = f'../code snippets-with-labels&metrics/{granularity}/{project}_{granularity}Level.csv'
        print('===='+project, granularity+'====')
        p, r, f, t, i = ten_folds_train(file, granularity)
        latex_line = latex_line + [p, r, f]
        times.append(t)
        importances.append(i)

    latex_matrix.append(latex_line)

print(np.mean(times[::4]))
print(np.mean(times[1::4]))
print(np.mean(times[2::4]))
print(np.mean(times[3::4]))

# for importance in importances:
#     print(importance)


avgs = avgEachColumn(latex_matrix)
matrix = insertRow(latex_matrix, avgs, len(latex_matrix))
project_names.append('\\textbf{Average}')
matrix = insertColumn(matrix, project_names, 0)
writeTable(matrix, 'results/within_project_NoSMOTE.txt')


