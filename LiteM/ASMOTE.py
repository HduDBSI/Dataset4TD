import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from imblearn.over_sampling import SMOTE
from sklearn.base import BaseEstimator
class ASMOTE:
    def __init__(self, random_state: int, clf: BaseEstimator):
        self.random_state = random_state
        self.clf = clf
    
    def needSMOTE(self, X_train: pd.Series, y_train: pd.Series):
        try:
            X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=1/8, stratify=y_train, random_state=self.random_state)
        except:
            return True, 5
        
        self.clf.fit(X_train, y_train)
        y_pred = self.clf.predict(X_val)
        val_f1_best = f1_score(y_val, y_pred)

        if val_f1_best == 0:
            return True, 5

        for k in [5, 4, 3]:
            try:
                smote = SMOTE(k_neighbors=k, random_state=self.random_state)
                X_train_resample, y_train_resample = smote.fit_resample(X_train, y_train)
                self.clf.fit(X_train_resample, y_train_resample)

                y_pred = self.clf.predict(X_val)
                val_f1 = f1_score(y_val, y_pred)
                if val_f1 > val_f1_best:
                    return True, k
            except:
                pass
        return False, -1

    def fit_resample(self, X_train: pd.Series, y_train: pd.Series):
        need, best_k = self.needSMOTE(X_train, y_train)
        if need:
            for k in list(range(best_k + 1, 0, -1)):
                try:
                    smote = SMOTE(k_neighbors=k, random_state=1)
                    X_train_resample, y_train_resample = smote.fit_resample(X_train, y_train)
                    return X_train_resample, y_train_resample
                except:
                    pass
            return X_train, y_train
        else:
            return X_train, y_train

class NoSMOTE:
    def fit_resample(self, X_train: pd.Series, y_train: pd.Series):
        return X_train, y_train
