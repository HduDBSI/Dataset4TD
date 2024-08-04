import sys
sys.path.append("..")
from project_Info import *
from LatexTable import *
from utils import cal_metrics
from lightgbm import LGBMClassifier
import pandas as pd
import numpy as np
from ASMOTE import ASMOTE
random_state = 1

def split_labels(labels: np.array, train_ratio=0.60, random_seed=42):

    # Set the random seed
    np.random.seed(random_seed)

    # Get the indices for pos and neg samples
    pos_indices = np.where(labels == 1)[0]
    neg_indices = np.where(labels == 0)[0]

    # Shuffle the indices
    np.random.shuffle(pos_indices)
    np.random.shuffle(neg_indices)

    # Calculate the number of samples for each set
    pos_sample_num = len(pos_indices)
    neg_sample_num = len(neg_indices)

    # Calculate the number of samples for each class in train and val sets
    pos_train_size = int(train_ratio * pos_sample_num)
    neg_train_size = int(train_ratio * neg_sample_num)

    # Split the indices for each set
    pos_train_indices, pos_test_indices = pos_indices[:pos_train_size], pos_indices[pos_train_size:]
    neg_train_indices, neg_test_indices = neg_indices[:neg_train_size], neg_indices[neg_train_size:]

    # Concatenate the indices for each set
    train_indices = np.concatenate((pos_train_indices, neg_train_indices))
    test_indices = np.concatenate((pos_test_indices, neg_test_indices))

    # Shuffle the indices for each set
    np.random.shuffle(train_indices)
    np.random.shuffle(test_indices)

    return train_indices, test_indices

def train(file_name, level):
    # load dataset
    data = pd.read_csv(file_name)
    data.columns = data.columns.str.lower()

    # define features and labels
    if level == 'file':
        X = data[file_feature_names_lowercase]
        train_ratio = 0.8934
    elif level == 'class':
        X = data[class_feature_names_lowercase]
        train_ratio = 0.5365
    elif level == 'method':
        X = data[method_feature_names_lowercase]
        train_ratio = 0.2121
    else:
        X = data[block_feature_names_lowercase]
        train_ratio = 0.0653
    y = data['CommentsAssociatedLabel'.lower()]
    pseudo_y = data[pseudo.lower()]
    
    precisions = []
    recalls = []
    f1_scores = []
    AUCs = []
    MCCs = []
    X = X.fillna(-1)
    asmote = ASMOTE(random_state=1, clf=LGBMClassifier(random_state=1, n_jobs=12))
    random_states = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for rs in random_states:

        train_indices, test_indices = split_labels(y, train_ratio=train_ratio, random_seed=rs)
        # label evenly distributed
        X_train, X_test = X.iloc[train_indices], X.iloc[test_indices]
        y_train, y_test = pseudo_y.iloc[train_indices], y.iloc[test_indices]
        
        # over sampling
        X_train_resample, y_train_resample = asmote.fit_resample(X_train, y_train)

        # init classifier
        clf = LGBMClassifier(random_state=random_state, n_jobs=12, n_estimators=500, learning_rate=0.05)
        
        # train 
        clf.fit(X_train_resample, y_train_resample)
        
        # predict
        y_pred = clf.predict(X_test)
        y_pred_prob = clf.predict_proba(X_test)[:, 1]

        # calculate metrics
        metrics = cal_metrics(y_test, y_pred, y_pred_prob)

        # save this round result
        precisions.append(metrics['P'])
        recalls.append(metrics['R'])
        f1_scores.append(metrics['F1'])
        AUCs.append(metrics['AUC'])
        MCCs.append(metrics['MCC'])

    # calculate average
    mean_precision = sum(precisions) / len(random_states)
    mean_recall = sum(recalls) / len(random_states)
    mean_f1_score = sum(f1_scores) / len(random_states)
    mean_auc = sum(AUCs) / len(random_states)
    mean_mcc = sum(MCCs) / len(random_states)

    return mean_precision, mean_recall, mean_f1_score, mean_auc, mean_mcc

latex_matrix = []
pseudo = 'PseudoLabelForCASFromMAT'
for project in projects:
    latex_line = []
    for granularity in granularities:
        file = f'../code snippets-with-labels&metrics/{granularity}/{project}_{granularity}Level.csv'
        p, r, f, auc, mcc = train(file, granularity)
        latex_line = latex_line + [p, r, f, auc, mcc]
    latex_matrix.append(latex_line)

avgs = avgEachColumn(latex_matrix)
matrix = insertRow(latex_matrix, avgs, len(latex_matrix))
project_names.append('\\textbf{Average}')
matrix = insertColumn(matrix, project_names, 0)
writeTable(matrix, f'results/LiteMC-PseudoLabelForCASFromMAT.txt')



