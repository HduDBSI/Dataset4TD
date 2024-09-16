from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, matthews_corrcoef
import numpy as np

def cal_metrics(y_true: np.array, y_pred: np.array, y_pred_positive_prob: np.array = None, output: bool = False):
    metrics = {}

    metrics['MCC'] = matthews_corrcoef(y_true, y_pred)

    if y_pred_positive_prob is not None:
        metrics['AUC'] = roc_auc_score(y_true, y_pred_positive_prob)

    metrics['ACC'] = accuracy_score(y_true, y_pred)
    metrics['P'] = precision_score(y_true, y_pred)
    metrics['R'] = recall_score(y_true, y_pred)
    metrics['F1'] = f1_score(y_true, y_pred)

    if output:
        print("Accuracy: {:.4f}".format(metrics['ACC']))
        print("Precision: {:.4f}".format(metrics['P']))
        print("Recall: {:.4f}".format(metrics['R']))
        print("F1-score: {:.4f}".format(metrics['F1']))
        print("MCC: {:.4f}".format(metrics['MCC']))
        if 'AUC' in metrics:
            print("AUC: {:.4f}".format(metrics['AUC']))

    return metrics

