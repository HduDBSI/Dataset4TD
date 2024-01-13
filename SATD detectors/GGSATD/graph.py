import scipy.sparse as sp
from numpy.random import uniform
from numpy import array
from random import shuffle
class graph():
    __MAX_TRUNC_LEN = 50
    def __init__(self, window_size=6, truncate=True, weighted=False):
        
        self.window_size = window_size
        self.truncate = truncate
        self.weighted = weighted

    def load_corpus(self, corpus):
        self.vocab = list(corpus)
        self.word_id_map = {}
        for i in range(len(self.vocab)):
            self.word_id_map[self.vocab[i]] = i
        
        self.oov = {}
        for v in self.vocab:
            self.oov[v] = uniform(1, 1, 300)

    def build_corpus(self, comments):
        # shuffle(comments)
        
        word_set = set()
        i = 0
        for comment in comments:
            words = comment.split()
            i += 1
            word_set.update(words)
        
        self.vocab = list(word_set)
        # self.vocab.sort()
        self.word_id_map = {}
        for i in range(len(self.vocab)):
            self.word_id_map[self.vocab[i]] = i
        
        self.oov = {}
        for v in self.vocab:
            self.oov[v] = uniform(1, 1, 300)
        
        return self.vocab
    
    # sliding windows
    def slide_window(self, doc_words):
        windows = []
        if len(doc_words) <= self.window_size:
            windows.append(doc_words)
        else:
            for j in range(len(doc_words) - self.window_size + 1):
                window = doc_words[j: j + self.window_size]
                windows.append(window)
        return windows
    
    def cal_word_pair_count(self, windows, word_id_map):
        word_pair_count = {}
        for window in windows:
            for p in range(1, len(window)):
                for q in range(0, p):
                    word_p = window[p]
                    word_p_id = word_id_map[word_p]
                    word_q = window[q]
                    word_q_id = word_id_map[word_q]
                    if word_p_id == word_q_id:
                        continue
                    word_pair_key = (word_p_id, word_q_id)
                    # word co-occurrences as weights
                    if word_pair_key in word_pair_count:
                        word_pair_count[word_pair_key] += 1.
                    else:
                        word_pair_count[word_pair_key] = 1.
                    # bi-direction
                    word_pair_key = (word_q_id, word_p_id)
                    if word_pair_key in word_pair_count:
                        word_pair_count[word_pair_key] += 1.
                    else:
                        word_pair_count[word_pair_key] = 1.
        return word_pair_count
    
    def make_adj(self, word_pair_count, doc_word_id_map):
        row = []
        col = []
        weight = []
        
        for key in word_pair_count:
            p = key[0]
            q = key[1]
            row.append(doc_word_id_map[self.vocab[p]])
            col.append(doc_word_id_map[self.vocab[q]])
            weight.append(word_pair_count[key] if self.weighted else 1.)
        adj = sp.csr_matrix((weight, (row, col)), shape=(len(doc_word_id_map), len(doc_word_id_map)))
        return adj
    
    def embed(self, doc_word_id_map, word_embeddings):
        features = []  
        for k, v in sorted(doc_word_id_map.items(), key=lambda x: x[1]):
            features.append(word_embeddings[k] if k in word_embeddings else self.oov[k])
        return features
    
    def format(self, adj, feature):
        formatted_adj = []
        formatted_feature = []
        for i in range(len(adj)):
            tmp_adj = adj[i].toarray()
            tmp_feature = array(feature[i])
            formatted_adj.append(tmp_adj)
            formatted_feature.append(tmp_feature)
        return array(formatted_adj), array(formatted_feature)
    
    def build_graph(self, word_embeddings, comment):
        doc_words = comment.split()
        if self.truncate:
            doc_words = doc_words[:self.__MAX_TRUNC_LEN]

        doc_vocab = list(set(doc_words))
        doc_nodes = len(doc_vocab)

        doc_word_id_map = {}
        for j in range(doc_nodes):
            doc_word_id_map[doc_vocab[j]] = j
        
        windows = self.slide_window(doc_words)
        word_pair_count = self.cal_word_pair_count(windows, self.word_id_map)
    
        adj = self.make_adj(word_pair_count, doc_word_id_map)
        features = self.embed(doc_word_id_map, word_embeddings)

        return adj.toarray(), array(features)
    
    def build_graphs(self, word_embeddings, comments):
        x_adj = []
        x_feature = []

        for comment in comments:
            adj, features = self.build_graph(word_embeddings, comment)
            x_adj.append(adj)
            x_feature.append(features)

        return array(x_adj), array(x_feature)
    
    def build_graph2(self, word_embeddings, comments):
        x_adj = []
        x_feature = []

        for comment in comments:
            doc_words = comment.split()
            if self.truncate:
                doc_words = doc_words[:self.__MAX_TRUNC_LEN]

            doc_vocab = list(set(doc_words))
            # doc_vocab.sort()
            doc_nodes = len(doc_vocab)

            doc_word_id_map = {}
            for j in range(doc_nodes):
                doc_word_id_map[doc_vocab[j]] = j
            
            windows = self.slide_window(doc_words)
            word_pair_count = self.cal_word_pair_count(windows, self.word_id_map)
        
            adj = self.make_adj(word_pair_count, doc_word_id_map)
            
            features = self.embed(doc_word_id_map, word_embeddings)

            x_adj.append(adj)
            x_feature.append(features)

        x_adj, x_feature = self.format(x_adj, x_feature)
        return x_adj, x_feature