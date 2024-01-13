from GGSATD import GGSATD
from utils import load_data, cal_indicators
from time import time
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
        ggsatd = GGSATD(train_x+test_x)
        A, P, R, F = 0, 0, 0, 0
        for i in range(repeat_times):
            ggsatd.fit(train_x=train_x, train_y=train_y)
            preds = ggsatd.classify(test_x)
            a, p, r, f = cal_indicators(preds=preds, labels=test_y)
            A += a
            P += p
            R += r
            F += f
            ggsatd.reinit()
        del ggsatd
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
        print(project, 'Acc:', "{:.2f}".format(A*100),"Precision=", "{:.2f}".format(P*100),
            "Recall=", "{:.2f}".format(R*100), "F1-score=", "{:.2f}".format(F*100))
    
    print('Average', 'Acc:', "{:.2f}".format(AA*100),"Precision=", "{:.2f}".format(PP*100),
            "Recall=", "{:.2f}".format(RR*100), "F1-score=", "{:.2f}".format(FF*100))

    print('cost time:', time()-t)
if __name__=='__main__':
    main()