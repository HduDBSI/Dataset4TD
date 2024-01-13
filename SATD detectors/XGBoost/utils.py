from re import sub, compile
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import  PorterStemmer
from nltk.stem.lancaster import LancasterStemmer

class StringFormatter():
    def __init__(self):
        self.stem_wordnet = WordNetLemmatizer()
        self.pst = PorterStemmer()
        self.lst = LancasterStemmer()    
    
    def format(self, string):       
        return self.stem(self.clean(string))

    def clean(self, string):
        pattern = compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 删除链接
        string = pattern.sub(' ', string)
        # clean logs
        string = sub(r'\S+-\S+-\S+\s:\s+(\S|\s)+', '', string)
        string = sub(r'Contributor\(s\)(.+\n)+', '', string)
        string = sub(r'\*|/|=', '', string)
        string = sub(r'-', ' ', string)

        string = sub(r"<TABLE .*?>((.|\n)*?)</TABLE>", " ", string)
        string = sub(r"<table .*?>((.|\n)*?)</table>", " ", string)
        # clean html labels
        string=sub('<[^>]*>','', string)

        string = sub(r"[^A-Za-z(),\+!?\'\`]", " ", string)
        string = sub(r"\'s", " \'s", string)  #
        string = sub(r"\'ve", " \'ve", string)
        string = sub(r"n\'t", " n\'t", string)
        string = sub(r"\'re", " \'re", string)
        string = sub(r"\'d", " \'d", string)
        string = sub(r"\'ll", " \'ll", string)
        string = sub(r",", " , ", string)
        string = sub(r"!", "  ", string)
        string = sub(r"\(", " ", string)
        string = sub(r"\)", " ", string)
        string = sub(r"\?", " \? ", string)
        string = sub(r"\+", " ", string)
        string = sub(r"\"", " ", string)
        string = sub(r",", " ", string)
        string = sub(r"\s{2,}", " ", string)
        return string.strip().lower()

    
    def stem(self, string):
        words = word_tokenize(string)
        text = []
        for word in words:
            if word == 'ca':
                text.append('can')
            elif word == 'n\'t':
                text.append('not')
            elif word == 'wo':
                text.append('will')
            else:
                text.append(self.stem_wordnet.lemmatize(word))
        text = [self.pst.stem(w) for w in text]
        text = [self.lst.stem(w) for w in text]
        text = ' '.join(text)
        text = text.replace('\\ ?', '\\?')
        if text == '':
            text = '""'
        return text

import pandas as pd
import random
import numpy as np
def load_data(test_project='columba-1.4-src', balance=False, export=False):
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

    if balance:
        train_positive_idx = train_idx & positive_idx
        train_negative_idx = train_idx & negative_idx
        remove_num = np.sum(train_negative_idx) - np.sum(train_positive_idx)

        df['tmp_idx'] = range(0,len(df))
        train_negative_idx_loc = df['tmp_idx'][train_negative_idx].values
        random.shuffle(train_negative_idx_loc)
        removed_train_negative_idx_loc = train_negative_idx_loc[:remove_num]
        
        df.drop(removed_train_negative_idx_loc, inplace=True)
        df.drop(['tmp_idx'], axis=1, inplace=True)
        df = df.reset_index(drop=True)
        test_idx, train_idx, positive_idx, negative_idx = get_idx(df, test_project)

    df['classification'][positive_idx] = 1
    df['classification'][negative_idx] = 0
  
    sf = StringFormatter()
    for i in range(len(df)):
        df['commenttext'][i] = sf.clean(df['commenttext'][i])
        df['commenttext'][i] = sf.stem(df['commenttext'][i])
    
    if export:
        df[['commenttext', 'classification']][train_idx].to_csv('exported_data/train.csv', index=False)
        df[['commenttext', 'classification']][test_idx].to_csv('exported_data/test.csv', index=False)
    
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

def remove_useless_word(keywords, documents):
    def process_one(document):
        processed = []
        words = document.split()
        for word in words:
            if word in keywords:
                processed.append(word)
        return ' '.join(processed)
    
    for i in range(len(documents)):
        documents[i] = process_one(documents[i])            
    return documents

def data_preprocess():
    df = pd.read_csv('data/technical_debt_dataset.csv')
    
    negative_idx = df['classification'] == 'WITHOUT_CLASSIFICATION'
    positive_idx = ~negative_idx

    df['classification'][positive_idx] = 1
    df['classification'][negative_idx] = 0
  
    sf = StringFormatter()
    for i in range(len(df)):
        df['commenttext'][i] = sf.clean(df['commenttext'][i])
        df['commenttext'][i] = sf.stem(df['commenttext'][i])
    
    df.rename(columns={'commenttext': 'comment', 'classification': 'label'}, inplace=True)
    df[['comment', 'label']].to_csv('exported_data/preprocessed_td.csv', index=False)

