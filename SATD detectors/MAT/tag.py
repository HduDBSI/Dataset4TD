import pandas as pd
from MAT import MAT
import time
import sys
sys.path.append("../../") 
from project_Info import *
encoding = 'utf-8-sig'
def main():
    t = time.time()
    
    mat = MAT()
    for project in projects:
        CommentFile = '../../comments-without-labels/all/'+project+'_allLevel_comment.csv'
        CommentFileLabeled = '../../comments-with-labels/MAT/'+project+'_allLevel_comment.csv'
        test = pd.read_csv(CommentFile, encoding=encoding)
        test_x = test['comment'].values.tolist()

        preds = []
        for x in test_x:
            if type(x) != str:
                x = ""
            preds.append(mat.classify(x))

        test['mat'] = preds
        test.to_csv(CommentFileLabeled, index=False, encoding=encoding)

    print('time:', time.time()-t)
if __name__=='__main__':
    main()
