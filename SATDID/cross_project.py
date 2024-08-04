import numpy as np
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
max_length = 1500
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

def cross(test_file, train_files):
    start_time = time.time()

    # load test set
    test = pd.read_csv(test_file)
    test.sort_values(by='ID', ascending=True, inplace=True)
    X_test, y_test = test['seq'].values.tolist(), test['label'].values.tolist()

    # load train set
    X_train = []
    y_train = []
    for train_file in train_files:
        train = pd.read_csv(train_file)
        train.sort_values(by='ID', ascending=True, inplace=True)
        X_train += train['seq'].values.tolist()
        y_train += train['label'].values.tolist()

    # make text to sequence
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train+X_test)

    sequences_train = tokenizer.texts_to_sequences(X_train)
    sequences_test = tokenizer.texts_to_sequences(X_test)
    vocab_size = len(tokenizer.word_index) + 1

    # pad sequence, truncate if the length exceeds max_length
    sequences_train = pad_sequences(sequences_train, maxlen=max_length)
    sequences_test = pad_sequences(sequences_test, maxlen=max_length)
    
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    # create model
    model = create_model(vocab_size, max_length, latent_dim, drop_prob)

    # train
    model.fit(sequences_train, y_train, epochs=epochs, batch_size=batch_size, verbose=False)

    # predict
    y_pred_prob = model.predict(sequences_test)
    y_pred = (y_pred_prob > 0.5).astype("int32")

    # calculate metrics
    metrics = cal_metrics(y_test, y_pred, y_pred_prob)

    print("Mean Accuracy:{:.2f}".format(metrics['ACC']))
    print("Mean Precision:{:.2f}".format(metrics['P']))
    print("Mean Recall:{:.2f}".format(metrics['R']))
    print("Mean F1-score:{:.2f}".format(metrics['F1']))
    print("Mean AUC: {:.2f}".format(metrics['AUC']))
    print("Mean MCC: {:.2f}".format(metrics['MCC']))
    
    return metrics

t = time.time()

latex_matrix = []
for project in projects:
    test_project = project
    train_projects = projects.copy()
    train_projects.remove(test_project)
    test_file = f'data/{test_project}.csv'
    train_files = [(f'data/{train_project}.csv') for train_project in train_projects]
    print('===='+project+'====')
    metrics = cross(test_file, train_files)
    latex_line = [metrics['P'], metrics['R'], metrics['F1'], metrics['AUC'], metrics['MCC']]
    latex_matrix.append(latex_line)

print(time.time()-t)

avgs = avgEachColumn(latex_matrix)
matrix = insertRow(latex_matrix, avgs, len(latex_matrix))
project_names.append('\\textbf{Average}')
matrix = insertColumn(matrix, project_names, 0)
writeTable(matrix, 'results/cross_project.txt')
