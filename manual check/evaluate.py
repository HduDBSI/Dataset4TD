import pandas as pd
import numpy as np
from scipy.stats import norm
import sys
sys.path.append('../')
from utils import cal_metrics

encoding = 'utf-8-sig'

def fleiss_kappa(data: np.array):
    """
    Calculates Fleiss' kappa coefficient for inter-rater agreement.

    Args:
        data: numpy array of shape (subjects, categories), where each element represents
              the number of raters who assigned a particular category to a subject.

    Returns:
        kappa: Fleiss' kappa coefficient.
    """
    subjects, categories = data.shape
    n_rater = np.sum(data[0])

    p_j = np.sum(data, axis=0) / (n_rater * subjects)
    P_e_bar = np.sum(p_j ** 2)

    P_i = (np.sum(data ** 2, axis=1) - n_rater) / (n_rater * (n_rater - 1))
    P_bar = np.mean(P_i)

    K = (P_bar - P_e_bar) / (1 - P_e_bar)

    tmp = (1 - P_e_bar) ** 2
    var = 2 * (tmp - np.sum(p_j * (1 - p_j) * (1 - 2 * p_j))) / (tmp * subjects * n_rater * (n_rater - 1))
    
    # standard error
    SE = np.sqrt(var) 

    Z = K / SE

    p_value = 2 * (1 - norm.cdf(np.abs(Z)))

    ci_bound = 1.96 * SE / subjects
    lower_ci_bound = K - ci_bound
    upper_ci_bound = K + ci_bound

    print("Fleiss Kappa: {:.3f}".format(K))
    print("Standard Error: {:.3f}".format(SE))
    print("Z: {:.3f}".format(Z))
    print("p-value: {:.3f}".format(p_value))
    print("Lower 95% CI Bound: {:.3f}".format(lower_ci_bound))
    print("Upper 95% CI Bound: {:.3f}".format(upper_ci_bound))
    print()

def transform(*raters):
    """
    Transforms the ratings of multiple raters into the required data format for Fleiss' Kappa calculation.

    Args:
        *raters: Multiple raters' ratings. Each rater's ratings should be a list or array of annotations.

    Returns:
        data: numpy array of shape (subjects, categories), where each element represents the number of raters
              who assigned a particular category to a subject.

    """
    assert all(len(rater) == len(raters[0]) for rater in raters), "Lengths of raters are not consistent."
    
    subjects = len(raters[0])
    categories = max(max(rater) for rater in raters) + 1
    data = np.zeros((subjects, categories))

    for i in range(subjects):
        for rater in raters:
            data[i, rater[i]] += 1
    
    return data

gs = pd.read_csv('Gold Standard.csv', encoding=encoding)
print('voting results')
metrics = cal_metrics(y_true=gs['label'], y_pred=gs['voting_label'], output=True)

print('MAT')
metrics = cal_metrics(y_true=gs['label'], y_pred=gs['mat'], output=True)

print('XGB')
metrics = cal_metrics(y_true=gs['label'], y_pred=gs['xgboost'], output=True)

print('GGSATD')
metrics = cal_metrics(y_true=gs['label'], y_pred=gs['ggsatd'], output=True)

df = pd.read_csv('all_comment.csv', encoding=encoding)
xgb = df['xgboost'].values.tolist()
mat = df['mat'].values.tolist()
ggsatd = df['ggsatd'].values.tolist()
print(len(xgb), len(mat), len(ggsatd))

print('Fleiss Kappa of three classifiers')
fleiss_kappa(transform(xgb, mat, ggsatd))

mask = gs['annotator2_label'] == -1
rater2 = gs.loc[~mask, 'annotator2_label'].values.tolist()
rater3 = gs.loc[~mask, 'annotator3_label'].values.tolist()
print(np.sum(gs.loc[~mask, 'annotator2_label'] != gs.loc[~mask, 'annotator3_label']))
print(len(rater2), len(rater3))
print('Fleiss Kappa of two annotators')
fleiss_kappa(transform(rater2, rater3))

xgb = gs.loc[~mask, 'xgboost'].values.tolist()
mat = gs.loc[~mask, 'mat'].values.tolist()
ggsatd = gs.loc[~mask, 'ggsatd'].values.tolist()
print(len(xgb), len(mat), len(ggsatd))
print('Fleiss Kappa of three classifies and two annotators')
fleiss_kappa(transform(rater2, rater3, xgb, mat, ggsatd))



