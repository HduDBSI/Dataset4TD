import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import StratifiedKFold
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Embedding, CuDNNLSTM, Dense, GlobalMaxPooling1D, LSTM
from keras.preprocessing.text import Tokenizer
from keras.utils.data_utils import pad_sequences
import pandas as pd
import time
import sys
sys.path.append("../") 
from project_Info import projects
# parameter settings
latent_dim = 64
batch_size = 256
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

def makeXy():

    X, y = [], []
    for project in projects:
        file_name = f'data/{project}.csv'
        data = pd.read_csv(file_name)
        data.sort_values(by='ID', ascending=True, inplace=True)
        # define features and labels

        X_tmp = data['seq'].values.tolist()
        y_tmp = data['label'].values.tolist()
        
        X += X_tmp
        y += y_tmp
   
    return X, y


# ten fold cross validation
def ten_fold():
    start_time = time.time()

    # load dataset
    X, y = makeXy()

    # make text to sequence
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X)

    sequences = tokenizer.texts_to_sequences(X)
    vocab_size = len(tokenizer.word_index) + 1

    X = pad_sequences(sequences, maxlen=max_length)
    y = np.array(y)

    # create StratifiedKFold object
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=random_state)

    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []

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
        # y_pred = model.predict_classes(X_test)
        y_pred_prob = model.predict(X_test)
        y_pred = (y_pred_prob > 0.5).astype("int32")

        # calculate accuracy, precision, recall, f1-score
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # save this round result
        accuracies.append(accuracy)
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)
        print(time.time() - start_time)
    
    # 计算平均指标
    mean_accuracy = np.mean(accuracies)
    mean_precision = np.mean(precisions)
    mean_recall = np.mean(recalls)
    mean_f1_score = np.mean(f1_scores)
    mean_cost_time = (time.time()-start_time)/10
    print("Mean Accuracy:{:.2%}".format(mean_accuracy))
    print("Mean Precision:{:.2%}".format(mean_precision))
    print("Mean Recall:{:.2%}".format(mean_recall))
    print("Mean F1-score:{:.2%}".format(mean_f1_score))
    print("Mean cost time:{:.0f}s".format(mean_cost_time))
    return mean_accuracy, mean_precision, mean_recall, mean_f1_score, mean_cost_time

import time
tt = time.time()
_, p, r, f, t = ten_fold()
print(time.time()-tt)

with open('total_ten_fold.txt',"w") as ff:
    ff.write(f'P, R, F\n{p}, {r}, {f}')