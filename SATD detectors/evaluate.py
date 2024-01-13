import numpy as np
import pandas as pd
import sys
from scipy.stats import norm
sys.path.append("../") 
from project_Info import projects

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
    print("p-value: {:.100f}".format(p_value))
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

def tranform2(weighted):
    """
    Transforms weighted data into the required data format for Fleiss' Kappa calculation.

    Args:
        weighted: List of weighted ratings. Each row represents [rater_0_category, rater_1_category, ..., rater_n_category, weight].

    Returns:
        data: numpy array of shape (subjects, categories), where each element represents the number of raters
              who assigned a particular category to a subject.

    """
    n_rater = len(weighted[0]) - 1
    raters = [[] for _ in range(n_rater)]
    for i in range(len(weighted)):
        for j in range(len(raters)):
            raters[j] = raters[j] + [weighted[i][j] for _ in range(weighted[i][n_rater])]
    
    data = transform(*raters)
    
    return data

# def test():
#     # Example data provided by wikipedia https://en.wikipedia.org/wiki/Fleiss_kappa
#     data = np.array([
#         [0, 0, 0, 0, 14],
#         [0, 2, 6, 4, 2],
#         [0, 0, 3, 5, 6],
#         [0, 3, 9, 2, 0],
#         [2, 2, 8, 1, 1],
#         [7, 7, 0, 0, 0],
#         [3, 2, 6, 3, 0],
#         [2, 5, 3, 2, 2],
#         [6, 5, 2, 1, 0],
#         [0, 2, 2, 3, 7]
#     ])

#     fleiss_kappa(data)

#     # need transform
#     rater1 = [1, 2, 2, 1, 2, 2, 1, 1, 3, 1, 2, 2]
#     rater2 = [1, 2, 1, 2, 1, 2, 3, 2, 3, 2, 3, 1]
#     rater3 = [1, 2, 2, 1, 3, 3, 3, 2, 1, 2, 3, 1]

#     data = transform(rater1, rater2, rater3)
#     fleiss_kappa(data)

#     # The first row indicates that both rater 1 and 2 rated as category 0, this case occurs 8 times.
#     # need transform2
#     weighted_data = [
#         [0, 0, 8],
#         [0, 1, 2],
#         [0, 2, 0],
#         [1, 0, 0],
#         [1, 1, 17],
#         [1, 2, 3],
#         [2, 0, 0],
#         [2, 1, 5],
#         [2, 2, 15]
#     ]
#     data = tranform2(weighted_data)
#     fleiss_kappa(data)

# test()

def count_combinations(matrix):
    combinations, counts = np.unique(matrix, axis=0, return_counts=True)
    total_count = np.sum(counts)
    frequencies = counts / total_count

    for i, combination in enumerate(combinations):
        print(f"Combination: {combination}, Count: {counts[i]}, Frequency: {frequencies[i]}")


df_list = []
for project in projects:
    df = pd.read_csv(f'../comments-with-labels/Final/{project}_allLevel_comment.csv')
    df_list.append(df)

# join dataframes together
df = pd.concat(df_list, axis=0, ignore_index=True)
df[['xgboost', 'mat', 'ggsatd']].to_csv('out.csv', index=False)

rater1 = df['xgboost'].values.tolist()
rater2 = df['mat'].values.tolist()
rater3 = df['ggsatd'].values.tolist()

matrix = np.column_stack((rater1, rater2, rater3))
count_combinations(matrix)

data = transform(rater1, rater2, rater3)

fleiss_kappa(data)