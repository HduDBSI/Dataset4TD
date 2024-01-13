# cross-project sceneries testing
from time import time
from XGBoost import XGBoost
from utils import load_data, cal_indicators

def main():
    t = time()
    projects = [
        'apache-ant-1.7.0', 
        'argouml', 
        'columba-1.4-src', 
        'emf-2.4.1', 
        'hibernate-distribution-3.3.2.GA', 
        'jEdit-4.2', 
        'jfreechart-1.0.19',
        'apache-jmeter-2.10', 
        'jruby-1.4.0', 
        'sql12']
    AA, PP, RR, FF = 0, 0, 0, 0
    res = {}
    repeat_times = 10
    for project in projects:
        train_y, train_x, test_y, test_x = load_data(test_project=project, export=False)
        A, P, R, F = 0, 0, 0, 0
        xgboost = XGBoost()
        xgboost.setKeywords(train_x, train_y)
        xgboost.buildCountVectorizer(train_x+test_x)
        for _ in range(repeat_times):
            xgboost.fit(train_x=train_x, train_y=train_y)
            preds = xgboost.classify(test_x)
            a, p, r, f = cal_indicators(preds=preds, labels=test_y)
            A += a
            P += p
            R += r
            F += f
        A, P, R, F = A/repeat_times, P/repeat_times, R/repeat_times, F/repeat_times
        res[project] = [A, P, R, F]
        AA += A
        PP += P
        RR += R
        FF += F
    AA, PP, RR, FF = AA/len(projects), PP/len(projects), RR/len(projects), FF/len(projects)
    for project in res.keys():
        indicators = res[project]
        A, P, R, F = indicators[0], indicators[1], indicators[2], indicators[3]
        print(project, 'Acc:', "{:.4f}".format(A),"Precision=", "{:.4f}".format(P),
            "Recall=", "{:.4f}".format(R), "F1-score=", "{:.4f}".format(F))
    
    print('Average', 'Acc:', "{:.4f}".format(AA),"Precision=", "{:.4f}".format(PP),
            "Recall=", "{:.4f}".format(RR), "F1-score=", "{:.4f}".format(FF))

    print('cost time:', time()-t)


if __name__=='__main__':
    main()