import sys
sys.path.append("../") 
from project_Info import projects
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import StratifiedKFold
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
import time
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

# k folds cross validation
def k_folds_train(project, k_fold=10):
    # load dataset
    file_name = f'MatchResults/{project}_Matched.csv'
    data = pd.read_csv(file_name)

    # define features and labels
    X, y = data[metrics], data['CommentsAssociatedLabel']
    
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
        smote = SMOTE(random_state=random_state)
        X_train_resample, y_train_resample = smote.fit_resample(X_train, y_train)
    
        # init classifier
        clf = RandomForestClassifier(n_jobs=12, random_state=random_state)
        
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

    return mean_accuracy, mean_precision, mean_recall, mean_f1_score, mean_cost_time

A, P, R, F, T = [], [], [], [], []
for project in projects:
    a, p, r, f, t = k_folds_train(project)
    A.append(a)
    P.append(p)
    R.append(r)
    F.append(f)
    T.append(t)
print("|    Project    | Accuracy | Precision | Recall | F1_score | Cost Time |")
for i in range(len(projects)):
    project_name = projects[i].split('-')[0]
    print("| {:^13} | {:^8.2%} | {:^9.2%} | {:^6.2%} | {:^8.2%} | {:9^.2f} |".
        format(project_name, A[i], P[i], R[i], F[i], T[i]))

print("|    Average    | {:^8.2%} | {:^9.2%} | {:^6.2%} | {:^8.2%} | {:9^.2f} |".
    format(np.mean(A), np.mean(P), np.mean(R), np.mean(F), np.mean(T)))

print(np.sum(T))
