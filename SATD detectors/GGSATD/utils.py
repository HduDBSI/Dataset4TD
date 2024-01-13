import re
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
class StringFormatter():
    def __init__(self):
        self.stem_wordnet = WordNetLemmatizer()
    
    def format(self, string):
        # if type(string) != str:
        #     string = ""
        return self.stem(self.clean(string))
    
    def clean(self, string):
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 删除链接
        string = pattern.sub(' ', string)
        # clean logs
        string = re.sub(r'\S+-\S+-\S+\s:\s+(\S|\s)+', '', string)
        string = re.sub(r'Contributor\(s\)(.+\n)+', '', string)
        string = re.sub(r'\*|/|=', '', string)
        string = re.sub(r'-', ' ', string)

        string = re.sub(r"<TABLE .*?>((.|\n)*?)</TABLE>", " ", string)
        string = re.sub(r"<table .*?>((.|\n)*?)</table>", " ", string)
        # clean html labels
        string=re.sub('<[^>]*>','', string)

        string = re.sub(r"[^A-Za-z(),\+!?\'\`]", " ", string)
        string = re.sub(r"\'s", " \'s", string)  #
        string = re.sub(r"\'ve", " \'ve", string)
        string = re.sub(r"n\'t", " n\'t", string)
        string = re.sub(r"\'re", " \'re", string)
        string = re.sub(r"\'d", " \'d", string)
        string = re.sub(r"\'ll", " \'ll", string)
        string = re.sub(r",", " , ", string)
        # string = re.sub(r"!", "\!", string)
        string = re.sub(r"\(", " ", string)
        string = re.sub(r"\)", " ", string)
        string = re.sub(r"\?", " \? ", string)
        string = re.sub(r"\+", " ", string)
        string = re.sub(r"\"", " ", string)
        string = re.sub(r",", " ", string)
        string = re.sub(r"\s{2,}", " ", string)
        return string.strip().lower()

    def stem(self, string):
        words = word_tokenize(string)
        # words = string.split()
        stemmed = []
        for word in words:
            if word == 'ca':
                stemmed.append('can')
            elif word == 'n\'t':
                stemmed.append('not')
            elif word == 'wo':
                stemmed.append('will')
            elif word == '"' or word == "'":
                continue
            else:
                stemmed.append(self.stem_wordnet.lemmatize(word))

        stemmed = ' '.join(stemmed)
        stemmed = stemmed.replace('\\ ?', '\\?')
        if stemmed == '':
            stemmed = '""'
        # stemmed = stemmed.replace("'", '')
        # stemmed = stemmed.replace('"', '')
        return stemmed

import pandas as pd
import numpy as np
import random
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
        df['commenttext'][i] = sf.format(df['commenttext'][i])
    
    if export:
        df[['commenttext', 'classification']][train_idx].to_csv('exported_data/train.csv', index=False)
        df[['commenttext', 'classification']][test_idx].to_csv('exported_data/test.csv', index=False)
    
    train_y, train_x = df['classification'][train_idx].values.tolist(), df['commenttext'][train_idx].values.tolist()
    test_y, test_x = df['classification'][test_idx].values.tolist(), df['commenttext'][test_idx].values.tolist()
    
    return train_y, train_x, test_y, test_x

from graph import graph
def build_graphs(train_x, test_x):
    word_embeddings = load_word_embeddings()
    g = graph()
    g.build_corpus(train_x+test_x)
    train_adj, train_feature = g.build_graphs(word_embeddings, train_x)
    test_adj, test_feature = g.build_graphs(word_embeddings, test_x)
    
    return train_adj, train_feature, test_adj, test_feature

import pickle as pkl
# def load_word_embeddings():
#     with open("cache/word_embeddings", 'rb') as f:
#         return pkl.load(f)

def load_word_embeddings():
    word_embeddings = {}
    with open("cache/glove.6B.300d.txt", 'r') as f:
        for line in f.readlines():
            data = line.split()
            word_embeddings[str(data[0])] = list(map(float,data[1:]))
    return word_embeddings

def load_corpus():
    with open('cache/corpus','rb') as f:
        return pkl.load(f)

def save_corpus(corpus):
    with open('cache/corpus', 'wb') as f:
        return pkl.dump(corpus, f)

def one_hot(labels):
    y = []
    for label in labels:
        if label == 0:  
            y.append([1, 0])
        else:
            y.append([0, 1])
    return np.array(y)

def preprocess_features(features):
    """Row-normalize feature matrix and convert to tuple representation"""
    max_length = max([len(f) for f in features])
    
    for i in range(features.shape[0]):
        feature = np.array(features[i])
        pad = max_length - feature.shape[0] # padding for each epoch
        if feature.shape == (0,):
            feature = np.ones([max_length, 300])
        else:
            feature = np.pad(feature, ((0,pad),(0,0)), mode='constant')       
        features[i] = feature
    
    return np.array(list(features))

def normalize_adj(adj):
    """Symmetrically normalize adjacency matrix."""
    rowsum = np.array(adj.sum(1))
    with np.errstate(divide='ignore'):
        d_inv_sqrt = np.power(rowsum, -0.5).flatten()
    d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.
    d_mat_inv_sqrt = np.diag(d_inv_sqrt)
    return adj.dot(d_mat_inv_sqrt).transpose().dot(d_mat_inv_sqrt)

def preprocess_adj(adj):
    """Preprocessing of adjacency matrix for simple GCN model and conversion to tuple representation."""
    max_length = max([a.shape[0] for a in adj])
    mask = np.zeros((adj.shape[0], max_length, 1)) # mask for padding

    for i in range(adj.shape[0]):
        adj_normalized = normalize_adj(adj[i]) # no self-loop
        pad = max_length - adj_normalized.shape[0] # padding for each epoch
        adj_normalized = np.pad(adj_normalized, ((0,pad),(0,pad)), mode='constant')
        mask[i,:adj[i].shape[0],:] = 1.
        adj[i] = adj_normalized

    return np.array(list(adj)), mask 

def construct_feed_dict(features, support, mask, labels, placeholders):
    feed_dict = dict()
    feed_dict.update({placeholders['labels']: labels})
    feed_dict.update({placeholders['features']: features})
    feed_dict.update({placeholders['support']: support})
    feed_dict.update({placeholders['mask']: mask})
    # feed_dict.update({placeholders['num_features_nonzero']: features[1].shape})
    return feed_dict

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
def cal_indicators(preds, labels):
    accuracy = accuracy_score(labels, preds)
    precision = precision_score(labels, preds)
    recall = recall_score(labels, preds)
    f1 = f1_score(labels, preds)
    return accuracy, precision, recall, f1

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

df = pd.read_csv('data/technical_debt_dataset.csv')
classification_counts = df['classification'].value_counts()
print(classification_counts)