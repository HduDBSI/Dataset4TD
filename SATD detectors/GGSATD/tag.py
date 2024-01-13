import pandas as pd
from GGSATD import GGSATD
from utils import StringFormatter
import time
import sys
sys.path.append("../../") 
from project_Info import *
encoding = 'utf-8-sig'
def split_list_to_nlist(list, sub_list_size):
    num = 0
    tmp = []
    nlist = []
    for i in range(len(list)):
        if num == sub_list_size:
            nlist.append(tmp)
            tmp = []
            num = 0
        tmp.append(list[i])
        num += 1
    if tmp != []:
        nlist.append(tmp)
    return nlist


def main():
    t = time.time()

    train = pd.read_csv('exported_data/preprocessed_td.csv', keep_default_na=False)
    train_x, train_y = train['comment'].values.tolist(), train['label'].values.tolist()
    sf = StringFormatter()
    for project in projects:
        CommentFile = '../../comments-without-labels/all/'+project+'_allLevel_comment.csv'
        CommentFileLabeled = '../../comments-with-labels/GGSATD/'+project+'_allLevel_comment.csv'
        print(CommentFile)
        test = pd.read_csv(CommentFile, encoding=encoding)
        test_x = test['comment'].values.tolist()
        
        for i in range(len(test_x)):
            test_x[i] = sf.format(test_x[i])
        
        if len(test_x) > 30000:
            list_test_x = split_list_to_nlist(test_x, 20000)
            preds = []
            for test_xx in list_test_x:
                ggsatd = GGSATD(train_x+test_xx)
                ggsatd.fit(train_x=train_x, train_y=train_y)
                tmp_preds = ggsatd.classify(test_xx)
                preds = preds + tmp_preds.tolist()
                ggsatd.reinit()
                del ggsatd
        else:
            ggsatd = GGSATD(train_x+test_x)
            ggsatd.fit(train_x=train_x, train_y=train_y)
            preds = ggsatd.classify(test_x)
            ggsatd.reinit()
            del ggsatd
        test['ggsatd'] = preds
        test.to_csv(CommentFileLabeled, index=False, encoding=encoding)

    print('time:', time.time()-t)
if __name__=='__main__':
    main()