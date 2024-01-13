from sklearn.feature_extraction.text import CountVectorizer
from feature import feature_word_select
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn import metrics
import time
import pandas as pd
import xgboost as xgb
from utils import load_data, remove_useless_word
def main():
    t = time.time()
    train_y, train_x, test_y, test_x = load_data(test_project='jEdit-4.2', export=False)
    
    word = feature_word_select(documents=train_x, labels=train_y, percentage=0.1)

    train_x, test_x = remove_useless_word(word, train_x), remove_useless_word(word, test_x)
    
    cv = CountVectorizer(min_df=1, max_df=0.5, ngram_range=(1, 2))
    cv.fit(train_x+test_x)
    cv_train_x, cv_test_x = cv.transform(train_x), cv.transform(test_x)
    cv_train_x, cv_val_x, train_y, val_y = train_test_split(cv_train_x, train_y, train_size=0.75)

    clf = xgb.XGBClassifier(max_depth=6, n_estimators=1000, colsample_bytree=0.8, objective='binary:logistic',
                            subsample=0.8, nthread=10, learning_rate=0.06, verbosity=0)
    clf.fit(cv_train_x, train_y, eval_set=[(cv_val_x, val_y)], early_stopping_rounds=30)

    preds = clf.predict(cv_test_x)
    print(metrics.classification_report(y_true=test_y, y_pred=preds, digits=4))
    print('time:', time.time()-t)

if __name__ == '__main__':
    main()


