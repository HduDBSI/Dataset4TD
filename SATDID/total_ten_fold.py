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
from project_Info import projects
from utils import cal_metrics
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
    AUCs = []
    MCCs = []

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
    mean_accuracy = sum(accuracies) / len(accuracies)
    mean_precision = sum(precisions) / len(precisions)
    mean_recall = sum(recalls) / len(recalls)
    mean_f1_score = sum(f1_scores) / len(f1_scores)
    mean_auc = sum(AUCs) / len(AUCs)
    mean_mcc = sum(MCCs) / len(MCCs)

    print("Mean Accuracy:{:.2f}".format(mean_accuracy))
    print("Mean Precision:{:.2f}".format(mean_precision))
    print("Mean Recall:{:.2f}".format(mean_recall))
    print("Mean F1-score:{:.2f}".format(mean_f1_score))
    print("Mean AUC: {:.2f}".format(mean_auc))
    print("Mean MCC: {:.2f}".format(mean_mcc))

    return mean_precision, mean_recall, mean_f1_score, mean_auc, mean_mcc

tt = time.time()
p, r, f, auc, mcc = ten_fold()
print(time.time()-tt)

with open('results/total_ten_fold.txt',"w") as f:
    f.write(f'P, R, F, AUC, MCC\n{p}, {r}, {f}, {auc}, {mcc}')
