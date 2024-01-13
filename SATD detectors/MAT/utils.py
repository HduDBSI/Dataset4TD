import pandas as pd
def load_data(test_project):
    df = pd.read_csv('data/technical_debt_dataset.csv')

    # classification = ['DEFECT', 'DESIGN', 'IMPLEMENTATION', 'TEST', 'WITHOUT_CLASSIFICATION',
    # 'DOCUMENTATION']

    # projects = ['apache-ant-1.7.0', 'apache-jmeter-2.10', 'argouml', 'columba-1.4-src',
    # 'emf-2.4.1', 'hibernate-distribution-3.3.2.GA', 'jEdit-4.2',
    # 'jfreechart-1.0.19', 'jruby-1.4.0', 'sql12']
    
    def get_idx(df:pd.DataFrame, project:str):
        test_idx = df['projectname'] == project
        train_idx = ~test_idx

        negative_idx = df['classification'] == 'WITHOUT_CLASSIFICATION'
        positive_idx = ~negative_idx

        return test_idx, train_idx, positive_idx, negative_idx

    test_idx, train_idx, positive_idx, negative_idx = get_idx(df, test_project)

    df['classification'][positive_idx] = 1
    df['classification'][negative_idx] = 0
    
    train_y, train_x = df['classification'][train_idx].values.tolist(), df['commenttext'][train_idx].values.tolist()
    test_y, test_x = df['classification'][test_idx].values.tolist(), df['commenttext'][test_idx].values.tolist()
    
    return train_y, train_x, test_y, test_x


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
def cal_indicators(preds, labels):
    accuracy = accuracy_score(labels, preds)
    precision = precision_score(labels, preds)
    recall = recall_score(labels, preds)
    f1 = f1_score(labels, preds)
    return accuracy, precision, recall, f1