from time import time
from MAT import MAT
from utils import *
def main():
    t = time()
    projects = ['apache-ant-1.7.0', 'argouml',  'columba-1.4-src',
      'emf-2.4.1', 'hibernate-distribution-3.3.2.GA', 'jEdit-4.2',
      'jfreechart-1.0.19', 'apache-jmeter-2.10', 'jruby-1.4.0', 'sql12']
    AA, PP, RR, FF = 0, 0, 0, 0
    res = {}
    mat = MAT()
    for project in projects:
        _, _, labels, comments = load_data(project)
        preds = []
        for comment in comments:
            preds.append(mat.classify(comment))
        A, P, R, F = cal_indicators(preds=preds, labels=labels)
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