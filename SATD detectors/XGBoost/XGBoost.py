from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import xgboost as xgb
from utils import remove_useless_word
from feature import feature_word_select

class XGBoost():
    word = None
    def __init__(self):
        self.cv = CountVectorizer(min_df=1, max_df=0.5, ngram_range=(1, 2))
        
    def buildCountVectorizer(self, comments):
        self.cv.fit(comments)
    
    def fit(self, train_x, train_y):
        if self.word == None:
            self.setKeywords(train_x, train_y)

        train_x = remove_useless_word(self.word, train_x)
        
        cv_train_x = self.cv.transform(train_x)
        cv_train_x, cv_val_x, train_y, val_y = train_test_split(cv_train_x, train_y, train_size=0.75)

        self.clf = xgb.XGBClassifier(max_depth=6, n_estimators=1000, colsample_bytree=0.8, objective='binary:logistic',
                            subsample=0.8, nthread=20, learning_rate=0.06, verbosity=0)
        self.clf.fit(cv_train_x, train_y, eval_set=[(cv_val_x, val_y)], early_stopping_rounds=30)

    def setKeywords(self, train_x, train_y):
        self.word = feature_word_select(documents=train_x, labels=train_y, percentage=0.1)

    def classify(self, test_x):
        test_x = remove_useless_word(self.word, test_x)
        cv_test_x = self.cv.transform(test_x)
        
        preds = self.clf.predict(cv_test_x)
        return preds
