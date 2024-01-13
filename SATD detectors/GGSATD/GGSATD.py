import tensorflow._api.v2.compat.v1 as tf
tf.disable_v2_behavior()
from models import GNN
from utils import StringFormatter, load_word_embeddings, construct_feed_dict
from utils import preprocess_adj, preprocess_features, one_hot, cal_indicators
import numpy as np
from graph import graph
from sklearn.model_selection import train_test_split
from time import time
class GGSATD():
    def __init__(self, comments):
        tf.reset_default_graph()
        self.sf = StringFormatter()
        self.g = graph()
        self.word_embeddings = load_word_embeddings()
        self.g.build_corpus(comments)

        flags = tf.compat.v1.app.flags
        self.FLAGS = flags.FLAGS
        flags.DEFINE_float('learning_rate', 0.001, 'Initial learning rate.')
        flags.DEFINE_integer('epochs', 30, 'Number of epochs to train.')
        flags.DEFINE_integer('batch_size', 32, 'Size of batches per epoch.') 
        flags.DEFINE_integer('input_dim', 300, 'Dimension of input.')
        flags.DEFINE_integer('hidden', 96, 'Number of units in hidden layer.') # 32, 64, 96, 128
        flags.DEFINE_integer('steps', 2, 'Number of graph layers.')
        flags.DEFINE_float('dropout', 0.5, 'Dropout rate (1 - keep probability).')
        flags.DEFINE_float('weight_decay', 0, 'Weight for L2 loss on embedding matrix.') # 5e-4
        flags.DEFINE_integer('early_stopping', -1, 'Tolerance for early stopping (# of epochs).')
        
        self.placeholders = {
            'support': tf.placeholder(tf.float32, shape=(None, None, None)),
            'features': tf.placeholder(tf.float32, shape=(None, None, self.FLAGS.input_dim)),
            'mask': tf.placeholder(tf.float32, shape=(None, None, 1)),
            'labels': tf.placeholder(tf.float32, shape=(None, 2)),
            'dropout': tf.placeholder_with_default(0., shape=()),
            'num_features_nonzero': tf.placeholder(tf.int32)  # helper variable for sparse dropout
        }

        self.sess = tf.Session()
        self.model = GNN(self.placeholders, input_dim=self.FLAGS.input_dim, name='gnn')

        self.sess.run(tf.global_variables_initializer())

    def __del__(self):
        lst = list(self.FLAGS._flags().keys())
        for key in lst:
            self.FLAGS.__delattr__(key)
    
    def reinit(self):
        self.sess.run(tf.global_variables_initializer())
    
    def evaluate(self, features, support, mask, labels, placeholders):
        feed_dict_val = construct_feed_dict(features, support, mask, labels, placeholders)
        
        outs_val = self.sess.run([self.model.loss, self.model.accuracy, self.model.embeddings,
             self.model.preds, self.model.labels], feed_dict=feed_dict_val)
        
        return outs_val[3]
    
    def fit(self, train_x, train_y):
        train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, train_size=0.9)
        
        train_adj, train_feature = self.g.build_graphs(self.word_embeddings, train_x)
        train_adj, train_mask = preprocess_adj(train_adj)
        train_feature = preprocess_features(train_feature)
        train_label = one_hot(train_y)

        val_adj, val_feature = self.g.build_graphs(self.word_embeddings, val_x)
        val_adj, val_mask = preprocess_adj(val_adj)
        val_feature = preprocess_features(val_feature)
        val_label = one_hot(val_y)
        
        best_val_f1 = 0.2
        for epoch in range(self.FLAGS.epochs):
            t = time()
            indices = np.arange(0, len(train_label))
            np.random.shuffle(indices)
            
            train_loss, train_acc = 0, 0
            for start in range(0, len(train_label), self.FLAGS.batch_size):
                end = start + self.FLAGS.batch_size
                idx = indices[start:end]
                
                feed_dict = construct_feed_dict(train_feature[idx], train_adj[idx], train_mask[idx], train_label[idx], self.placeholders)
                feed_dict.update({self.placeholders['dropout']: self.FLAGS.dropout})

                outs = self.sess.run([self.model.opt_op, self.model.loss, self.model.accuracy], feed_dict=feed_dict)
                train_loss += outs[1]*len(idx)
                train_acc += outs[2]*len(idx)
            
            train_loss /= len(train_y)
            train_acc /= len(train_y)
            
            preds = self.evaluate(val_feature, val_adj, val_mask, val_label, self.placeholders)
            _, _, _, val_f1 = cal_indicators(preds=preds, labels=val_y)
            if best_val_f1 < val_f1:
                best_val_f1 = val_f1
                self.model.save(sess=self.sess)
            
            print("Epoch:", '%04d' % (epoch + 1), "train_loss=", "{:.5f}".format(train_loss),
            "train_acc=", "{:.5f}".format(train_acc), "time=", "{:.5f}".format(time() - t))
        self.model.load(sess=self.sess)
    
    def classify(self, test_x):
        adj, feature = self.g.build_graphs(self.word_embeddings, test_x)
        
        adj, mask = preprocess_adj(adj)
        feature = preprocess_features(feature)

        fake_label = np.ones([1, 2]) 
        preds = self.evaluate(feature, adj, mask, fake_label, self.placeholders)
        
        return preds
