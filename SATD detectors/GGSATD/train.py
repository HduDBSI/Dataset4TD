import tensorflow._api.v2.compat.v1 as tf
tf.disable_v2_behavior()
from models import GNN
from time import time
from sklearn import metrics
import utils
import numpy as np

def train(adj, feature, label, saveModel=False):
    adj, mask = utils.preprocess_adj(adj)
    feature = utils.preprocess_features(feature)
    label = utils.one_hot(label)
    
    for epoch in range(FLAGS.epochs):
        t = time()
        indices = np.arange(0, len(label))
        np.random.shuffle(indices)
        
        train_loss, train_acc = 0, 0
        for start in range(0, len(label), FLAGS.batch_size):
            end = start + FLAGS.batch_size
            idx = indices[start:end]
            
            feed_dict = utils.construct_feed_dict(feature[idx], adj[idx], mask[idx], label[idx], placeholders)
            feed_dict.update({placeholders['dropout']: FLAGS.dropout})

            outs = sess.run([model.opt_op, model.loss, model.accuracy], feed_dict=feed_dict)
            train_loss += outs[1]*len(idx)
            train_acc += outs[2]*len(idx)
        
        train_loss /= len(train_y)
        train_acc /= len(train_y)
        
        print("Epoch:", '%04d' % (epoch + 1), "train_loss=", "{:.5f}".format(train_loss),
          "train_acc=", "{:.5f}".format(train_acc), "time=", "{:.5f}".format(time() - t))

        if saveModel:
            model.save(sess)

def test(adj, feature, label):
    adj, mask = utils.preprocess_adj(adj)
    feature = utils.preprocess_features(feature)
    
    fake_label = np.ones([len(label), 2]) 
    _, _, _, _, preds, _ = evaluate(feature, adj, mask, fake_label, placeholders)

    print(metrics.classification_report(y_true=label, y_pred=preds, digits=4))
    print(metrics.confusion_matrix(y_true=label, y_pred=preds))   

def evaluate(features, support, mask, labels, placeholders):
    t_test = time()
    feed_dict_val = utils.construct_feed_dict(features, support, mask, labels, placeholders)
    
    outs_val = sess.run([model.loss, model.accuracy, model.embeddings, model.preds, model.labels], feed_dict=feed_dict_val)
    return outs_val[0], outs_val[1], (time() - t_test), outs_val[2], outs_val[3], outs_val[4]


start_time = time()
# projects = ['apache-ant-1.7.0', 'apache-jmeter-2.10', 'argouml', 'columba-1.4-src',
    # 'emf-2.4.1', 'hibernate-distribution-3.3.2.GA', 'jEdit-4.2',
    # 'jfreechart-1.0.19', 'jruby-1.4.0', 'sql12']
train_y, train_x, test_y, test_x = utils.load_data(test_project='sql12', export=False)
print('data has been loaded')
train_adj, train_feature, test_adj, test_feature = utils.build_graphs(train_x, test_x)
print('graphs have been built')


flags = tf.compat.v1.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_float('learning_rate', 0.001, 'Initial learning rate.')
flags.DEFINE_integer('epochs', 12, 'Number of epochs to train.')
flags.DEFINE_integer('batch_size', 32, 'Size of batches per epoch.') 
flags.DEFINE_integer('input_dim', 300, 'Dimension of input.')
flags.DEFINE_integer('hidden', 96, 'Number of units in hidden layer.') # 32, 64, 96, 128
flags.DEFINE_integer('steps', 2, 'Number of graph layers.')
flags.DEFINE_float('dropout', 0.5, 'Dropout rate (1 - keep probability).')
flags.DEFINE_float('weight_decay', 0, 'Weight for L2 loss on embedding matrix.') # 5e-4
flags.DEFINE_integer('early_stopping', -1, 'Tolerance for early stopping (# of epochs).')
flags.DEFINE_integer('max_degree', 3, 'Maximum Chebyshev polynomial degree.') # Not used
# Load data

placeholders = {
    'support': tf.placeholder(tf.float32, shape=(None, None, None)),
    'features': tf.placeholder(tf.float32, shape=(None, None, FLAGS.input_dim)),
    'mask': tf.placeholder(tf.float32, shape=(None, None, 1)),
    'labels': tf.placeholder(tf.float32, shape=(None, 2)),
    'dropout': tf.placeholder_with_default(0., shape=()),
    'num_features_nonzero': tf.placeholder(tf.int32)  # helper variable for sparse dropout
}

sess = tf.Session()
model = GNN(placeholders, input_dim=FLAGS.input_dim, name='gnn')

sess.run(tf.global_variables_initializer())
train(train_adj, train_feature, train_y)
test(test_adj, test_feature, test_y)
print(time()-start_time)


