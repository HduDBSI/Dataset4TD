import sys
sys.path.append("..")
from project_Info import *
from LatexTable import *
from sklearn.model_selection import StratifiedKFold
from lightgbm import LGBMClassifier
import pandas as pd
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler, TomekLinks, EditedNearestNeighbours
from sklearn.tree import DecisionTreeClassifier
from ASMOTE import ASMOTE, NoSMOTE
import numpy as np
import scipy.io as sio
import time
import argparse
from utils import cal_metrics

def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--technique', choices=['ADASYN', 'ASMOTE', 'NoSMOTE', 'SMOTE', 'RUS', 'TL', 'ENN'], default='ENN', help='Data augmentation technique to use')
    parser.add_argument('--classifier', type=str, choices=['LightGBM', 'DecisionTree'], default='LightGBM')    
    parser.add_argument('--label_column_name', type=str, default='CommentsAssociatedLabel')
    parser.add_argument('--random_state', type=int, default=1)

    return parser

# ten folds cross validation
def ten_folds(file_name, level, k_fold=10):
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
    y = data[args.label_column_name.lower()]

    # create StratifiedKFold object
    skf = StratifiedKFold(n_splits=k_fold, shuffle=True, random_state=args.random_state)

    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    start_time = time.time()
    feature_importances = []
    AUCs = []
    MCCs = []
    X = X.fillna(-1)
    for train_index, test_index in skf.split(X, y):
        # label evenly distributed
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        # init classifier
        if args.classifier == 'LightGBM':
            clf = LGBMClassifier(random_state=args.random_state, n_jobs=12, n_estimators=500, learning_rate=0.05)
        else:
            clf = DecisionTreeClassifier(random_state=args.random_state)

        if args.technique == 'ASMOTE':
            if args.classifier == 'LightGBM':
                tech = ASMOTE(random_state=args.random_state, clf=LGBMClassifier(random_state=args.random_state))
            else:
                tech = ASMOTE(random_state=args.random_state, clf=DecisionTreeClassifier(random_state=args.random_state))

        elif args.technique == 'ADASYN':
            tech = ADASYN(random_state=args.random_state)
        elif args.technique == 'SMOTE':
            tech = SMOTE(random_state=args.random_state)
        elif args.technique == 'NoSMOTE':
            tech = NoSMOTE()
        elif args.technique == 'RUS':
            tech = RandomUnderSampler(random_state=args.random_state)
        elif args.technique == 'TL':
            tech = TomekLinks()
        elif args.technique == 'ENN':
            tech = EditedNearestNeighbours()

        X_train_resample, y_train_resample = tech.fit_resample(X_train, y_train)

        clf.fit(X_train_resample, y_train_resample)

        # predict
        y_pred = clf.predict(X_test)
        y_pred_prob = clf.predict_proba(X_test)[:, 1]

        # record importances
        importance = clf.feature_importances_
        feature_importances.append(importance)

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
    mean_cost_time = (time.time() - start_time) / k_fold
    mean_auc = sum(AUCs) / k_fold
    mean_mcc = sum(MCCs) / k_fold
    mean_feature_importances = np.mean(np.array(feature_importances), axis=0)
    mean_feature_importances = normalize_list(mean_feature_importances)

    print("Mean Accuracy:{:.2f}".format(mean_accuracy))
    print("Mean Precision:{:.2f}".format(mean_precision))
    print("Mean Recall:{:.2f}".format(mean_recall))
    print("Mean F1-score:{:.2f}".format(mean_f1_score))
    print("Mean AUC: {:.2f}".format(mean_auc))
    print("Mean MCC: {:.2f}".format(mean_mcc))
    print("Mean Cost Time: {:.2f} seconds".format(mean_cost_time))

    return mean_precision, mean_recall, mean_f1_score, mean_cost_time, mean_feature_importances, mean_auc, mean_mcc

def normalize_list(lst):
    min_value = min(lst)
    max_value = max(lst)
    return [(x - min_value) / (max_value - min_value) for x in lst]

parser = get_parser()
args = parser.parse_args()

latex_matrix = []
importances = []
times = []

for project in projects:
    latex_line = []
    for granularity in granularities:
        file = f'../code snippets-with-labels&metrics/{granularity}/{project}_{granularity}Level.csv'
        print('===='+project, granularity+'====')
        p, r, f, t, i, auc, mcc = ten_folds(file, granularity)
        latex_line = latex_line + [p, r, f, auc, mcc]
        times.append(t)
        importances.append(i)
    latex_matrix.append(latex_line)


# for importance in importances:
#     print(importance)

avgs = avgEachColumn(latex_matrix)
matrix = insertRow(latex_matrix, avgs, len(latex_matrix))
project_names.append('\\textbf{Average}')
matrix = insertColumn(matrix, project_names, 0)
writeTable(matrix, f'results/within_project_{args.technique}_{args.classifier}.txt')

with open(f'results/time_{args.technique}_{args.classifier}.txt', 'w') as f:
    for index, granularity in enumerate(granularities):
        time_mean = np.mean(times[index::4])
        time_mdian = np.median(times[index::4])
        time_total = np.sum(times[index::4])
        print(granularity + '-average', time_mean)
        print(granularity + '-median', time_mdian)
        f.write("{:.2f} {:.2f}\n".format(time_mdian, time_total))

sio.savemat(f'results/importance_{args.technique}_{args.classifier}.mat', {
    'data': importances,
    'file_feature_names': file_feature_names,
    'class_feature_names': class_feature_names,
    'method_feature_names': method_feature_names,
    'block_feature_names': block_feature_names,
})
