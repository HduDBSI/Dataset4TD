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

def needSMOTE(X_train:pd.Series, y_train:pd.Series):
    try:
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=1/8, stratify=y_train, random_state=random_state)
    except:
        return True, 5
    clf = LGBMClassifier(random_state=random_state, n_jobs=12)
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

    # # Print the number of positive and negative samples in each set
    # train_pos_num = np.count_nonzero(labels[train_indices] == 1)
    # train_neg_num = np.count_nonzero(labels[train_indices] == 0)

    # test_pos_num = np.count_nonzero(labels[test_indices] == 1)
    # test_neg_num = np.count_nonzero(labels[test_indices] == 0)

    # print("=== The Results of Dataset Splitting ===")
    # print("Train set - positive samples:", train_pos_num)
    # print("Train set - negative samples:", train_neg_num)
    # print()
    # print("Test set - pos samples:", test_pos_num)
    # print("Test set - neg samples:", test_neg_num)
    # print()

    return train_indices, test_indices


#  reproduction of MAT https://github.com/Naplues/MAT/
#  paper: "How far have we progressed in identifying self-admitted technical debts? 
#         A comprehensive empirical study"
#  https://dl.acm.org/doi/10.1145/3447247
class MAT():
    __keywords = ["todo", "hack", "fixme", "xxx", "deprecated"]
    __TD = 1
    __NonTD = 0
    
    def filter(self, word: str) -> str: 
        res = ""
        for ch in word:
            if ('a' <= ch and ch <= 'z') or ('A' <= ch and ch <= 'Z'):
                res += ch
        return res.lower()


    def splitToTokens(self, comment: str) -> list:
        tokens = comment.split()
        words = []
        for token in tokens:
            word = self.filter(token)
            if 2 < len(word) and len(word) < 20:
                words.append(word)
        return words
    
    def classify(self, comment: str) -> int:
        tokens = self.splitToTokens(comment)
        for token in tokens:
            for keyword in self.__keywords:
                if token.startswith(keyword) or token.endswith(keyword):
                    if "xxx" in token and token != "xxx":
                        return self.__NonTD
                    else:
                        return self.__TD
        return self.__NonTD
    
seperator = "[[SEP]]"
mat = MAT()
def comment2label(comments:str):
    arr = comments.split(seperator)
    for a in arr:
        if mat.classify(a):
            return 1
    return 0


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
    y = data[label_column_name.lower()]

    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    start_time = time.time()
    feature_importances = []
    
    X = X.fillna(-1)

    random_states = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for rs in random_states:

        train_indices, test_indices = split_labels(y, train_ratio=train_ratio, random_seed=rs)
        # label evenly distributed
        X_train, X_test = X.iloc[train_indices], X.iloc[test_indices]
        y_test = y.iloc[test_indices]

        y_train = data['commentsassociated'][train_indices].apply(comment2label)
        # over sampling
        X_train_resample, y_train_resample = ASMOTE(X_train, y_train)

        # init classifier
        clf = LGBMClassifier(random_state=random_state, n_jobs=12, n_estimators=500, learning_rate=0.05)
        
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
    mean_accuracy = sum(accuracies) / len(random_states)
    mean_precision = sum(precisions) / len(random_states)
    mean_recall = sum(recalls) / len(random_states)
    mean_f1_score = sum(f1_scores) / len(random_states)
    mean_cost_time = (time.time()-start_time) / len(random_states)
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
        p, r, f, t, i = train(file, granularity)
        latex_line = latex_line + [p, r, f]
        times.append(t)
        importances.append(i)

    latex_matrix.append(latex_line)

print(np.mean(times[::4]))
print(np.mean(times[1::4]))
print(np.mean(times[2::4]))
print(np.mean(times[3::4]))
print(np.sum(times))
# for importance in importances:
#     print(importance)


avgs = avgEachColumn(latex_matrix)
matrix = insertRow(latex_matrix, avgs, len(latex_matrix))
project_names.append('\\textbf{Average}')
matrix = insertColumn(matrix, project_names, 0)
writeTable(matrix, 'results/real.txt')



