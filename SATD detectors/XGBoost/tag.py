import pandas as pd
from XGBoost import XGBoost
import time
from utils import StringFormatter
import sys
sys.path.append("../../") 
from project_Info import *
encoding = 'utf-8-sig'
def main():
    t = time.time()
    train = pd.read_csv('exported_data/preprocessed_td.csv')
    train_x, train_y = train['comment'].values.tolist(), train['label'].values.tolist()
    sf = StringFormatter()
    xgboost = XGBoost()
    xgboost.setKeywords(train_x, train_y)
    for project in projects:

        CommentFile = '../../comments-without-labels/all/'+project+'_allLevel_comment.csv'
        CommentFileLabeled = '../../comments-with-labels/XGBoost/'+project+'_allLevel_comment.csv'
        test = pd.read_csv(CommentFile, encoding=encoding)
        test_x = test['comment'].values.tolist()
        for i in range(len(test_x)):
            test_x[i] = sf.format(test_x[i])

        xgboost.buildCountVectorizer(train_x+test_x)
        xgboost.fit(train_x=train_x, train_y=train_y)
        preds = xgboost.classify(test_x)

        test['xgboost'] = preds
        test.to_csv(CommentFileLabeled, index=False, encoding=encoding)

    print('time:', time.time()-t)
if __name__=='__main__':
    main()
