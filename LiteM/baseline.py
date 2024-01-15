import sys
sys.path.append("..")
from project_Info import *
from LatexTable import *
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import time
random_state = 1

def needSMOTE(X_train:pd.Series, y_train:pd.Series):
    try:
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=1/8, stratify=y_train, random_state=random_state)
    except:
        return True, 5
    clf = DecisionTreeClassifier(random_state=random_state)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_val)
    val_f1_best = f1_score(y_val, y_pred)
    
    if val_f1_best == 0:
        return True, 5

    for k in  [5, 4, 3]:
        try:
            smote = SMOTE(k_neighbors=k, random_state=random_state)
            X_train_resample, y_train_resample = smote.fit_resample(X_train, y_train)
            clf.fit(X_train_resample, y_train_resample)
            
            y_pred = clf.predict(X_val)
            val_f1 = f1_score(y_val, y_pred)
            if val_f1 > val_f1_best:
                return True, k
        except:
            pass
    return False, -1


def ASMOTE(X_train:pd.Series, y_train:pd.Series):
    need, best_k = needSMOTE(X_train, y_train)
    if need:
        for k in list(range(best_k+1, 0, -1)):
            try:
                smote = SMOTE(k_neighbors=k, random_state=1)
                X_train_resample, y_train_resample = smote.fit_resample(X_train, y_train)
                return X_train_resample, y_train_resample
            except:
                pass
        return X_train, y_train
    else:
        return X_train, y_train

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
    y = data['CommentsAssociatedLabel'.lower()]
    
    # create StratifiedKFold object
    skf = StratifiedKFold(n_splits=k_fold, shuffle=True, random_state=random_state)

    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    start_time = time.time()
    
    X = X.fillna(-1)

    # loop ten times for cross validation
    for train_index, test_index in skf.split(X, y):
        
        # label evenly distributed
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        # over sampling
        # smote = SMOTE(random_state=random_state)
        # X_train_resample, y_train_resample = smote.fit_resample(X_train, y_train)
        X_train_resample, y_train_resample = ASMOTE(X_train, y_train)
        # X_train_resample, y_train_resample = X_train, y_train
    
        # init classifier
        clf = DecisionTreeClassifier(random_state=random_state)
        
        # train 
        clf.fit(X_train_resample, y_train_resample)
        
        # predict
        y_pred = clf.predict(X_test)
        
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

    print("Mean Accuracy:{:.2%}".format(mean_accuracy))
    print("Mean Precision:{:.2%}".format(mean_precision))
    print("Mean Recall:{:.2%}".format(mean_recall))
    print("Mean F1-score:{:.2%}".format(mean_f1_score))

    return mean_precision, mean_recall, mean_f1_score, mean_cost_time

latex_matrix = []
times = []
for project in projects:
    latex_line = []
    for granularity in granularities:
        file = f'../code snippets-with-labels&metrics/{granularity}/{project}_{granularity}Level.csv'
        print('===='+project, granularity+'====')
        p, r, f, t = ten_folds_train(file, granularity)
        latex_line = latex_line + [p, r, f]
        times.append(t)

    latex_matrix.append(latex_line)

print(np.mean(times[::4])) # file_average_Afold_train_time
print(np.mean(times[1::4]))
print(np.mean(times[2::4]))
print(np.mean(times[3::4]))
print(np.sum(times))

avgs = avgEachColumn(latex_matrix)
matrix = insertRow(latex_matrix, avgs, len(latex_matrix))
project_names.append('\\textbf{Average}')
matrix = insertColumn(matrix, project_names, 0)
writeTable(matrix, 'results/baseline.txt')

