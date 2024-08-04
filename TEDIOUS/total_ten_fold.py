import sys
sys.path.append("..")
from project_Info import *
from utils import cal_metrics
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import time

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

def makeXy():
    X_list, y_list = [], []
    for project in projects:
        file_name = f'MatchResults/{project}_Matched.csv'
        data = pd.read_csv(file_name)

        # define features and labels
        X_tmp = data[total_metrics]
        y_tmp = data[label_column_name]
        
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
    AUCs = []
    MCCs = []
    
    X = X.fillna(-1)
    # loop for cross validation
    for train_index, test_index in skf.split(X, y):
        # label evenly distributed
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
   
        clf = RandomForestClassifier(random_state=random_state, n_jobs=12)
        
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


t = time.time()
p, r, f1, auc, mcc = ten_fold()
print(time.time() - t)

with open('results/total_ten_fold.txt',"w") as f:
    f.write(f'P, R, F, AUC, MCC\n{p}, {r}, {f1}, {auc}, {mcc}')


