import numpy as np
from sklearn.model_selection import StratifiedKFold
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Embedding, CuDNNLSTM, Dense, GlobalMaxPooling1D, LSTM
from keras.preprocessing.text import Tokenizer
from keras.utils.data_utils import pad_sequences
import pandas as pd
import time
import sys
sys.path.append("../") 
from project_Info import projects, project_names
from utils import cal_metrics
from LatexTable import *
# parameter settings
latent_dim = 64
batch_size = 64
drop_prob = 0.2
epochs = 40
random_state = 1

def create_model(input_dim, input_length, latent_dim, drop_prob):
    model = Sequential()
    model.add(Embedding(input_dim=input_dim, output_dim=latent_dim, input_length=input_length))
    model.add(CuDNNLSTM(units=latent_dim, return_sequences=True))
    # model.add(LSTM(units=latent_dim, return_sequences=True, dropout=drop_prob, recurrent_dropout=drop_prob))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(units=1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def k_folds(project, k_fold=10):
    start_time = time.time()
    
    df = pd.read_csv(f'data/{project}.csv')
    df.sort_values(by='ID', ascending=True, inplace=True)
    
    texts = df['seq'].values.tolist()
    labels = df['label'].values.tolist()

    # make text to sequence
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(texts)

    sequences = tokenizer.texts_to_sequences(texts)
    vocab_size = len(tokenizer.word_index) + 1

    max_length = max([len(seq) for seq in sequences])
    if max_length > 1500:
        max_length = 1500

    # pad sequence, truncate if the length exceeds max_length
    X = pad_sequences(sequences, maxlen=max_length)
    
    y = np.array(labels)

    # k folds cross validation
    skf = StratifiedKFold(n_splits=k_fold, shuffle=True, random_state=random_state)

    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    AUCs=[]
    MCCs=[]

    # loop k times for cross validation
    for train_index, test_index in skf.split(X, y):

        # label evenly distributed
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # create model
        model = create_model(vocab_size, max_length, latent_dim, drop_prob)

        # train
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=False)

        # predict
        y_pred_prob = model.predict(X_test)
        y_pred = (y_pred_prob > 0.5).astype("int32")

        # calculate metrics
        metrics = cal_metrics(y_test, y_pred, y_pred_prob)

        # save this round result
        accuracies.append(metrics['ACC'])
        precisions.append(metrics['P'])
        recalls.append(metrics['R'])
        f1_scores.append(metrics['F1'])
        AUCs.append(metrics['AUC'])
        MCCs.append(metrics['MCC'])
    
    # calculate average
    mean_accuracy = sum(accuracies) / k_fold
    mean_precision = sum(precisions) / k_fold
    mean_recall = sum(recalls) / k_fold
    mean_f1_score = sum(f1_scores) / k_fold
    mean_cost_time = (time.time() - start_time) / k_fold
    mean_auc = sum(AUCs) / k_fold
    mean_mcc = sum(MCCs) / k_fold

    print("Mean Accuracy:{:.2f}".format(mean_accuracy))
    print("Mean Precision:{:.2f}".format(mean_precision))
    print("Mean Recall:{:.2f}".format(mean_recall))
    print("Mean F1-score:{:.2f}".format(mean_f1_score))
    print("Mean AUC: {:.2f}".format(mean_auc))
    print("Mean MCC: {:.2f}".format(mean_mcc))
    print("Mean Cost Time: {:.2f} seconds".format(mean_cost_time))

    return mean_precision, mean_recall, mean_f1_score, mean_cost_time, mean_auc, mean_mcc

latex_matrix = []
times = []
for project in projects:
    print('===='+project+'====')
    p, r, f, t, auc, mcc = k_folds(project)
    latex_matrix.append([p, r, f, auc, mcc])
    times.append(t)

avgs = avgEachColumn(latex_matrix)
matrix = insertRow(latex_matrix, avgs, len(latex_matrix))
project_names.append('\\textbf{Average}')
matrix = insertColumn(matrix, project_names, 0)
writeTable(matrix, 'results/within_project.txt')

with open(f'results/time3.txt', 'w') as f:
    for t, project in zip(times, project_names):
        f.write("{}\t{:.2f}\n".format(project, t))
    f.write("Median\t{:.2f}\n".format(np.median(times)))
