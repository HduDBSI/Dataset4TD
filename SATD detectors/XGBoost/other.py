import numpy as np
def fs3(documents:list, labels:list, percentage:float):
    class_num = [labels.count(0), labels.count(1)]
            
    word_set = set()
    for document in documents:
        words = document.split()
        word_set.update(words)
    word_list = list(word_set)
    word_list.sort()
    
    word_dic = {}
    for i in range(len(word_list)):
        word_dic[word_list[i]] = i
    
    idx = np.zeros((len(word_list), 2), np.float32)
    for i in range(len(documents)):
        words = documents[i].split()
        for word in words:
            idx[word_dic[word]][labels[i]] += 1

    sorted_words = chi31(class_num, word_list, idx)
    top_k_words = sorted_words[:int(percentage * len(sorted_words))]
    
    return top_k_words
def chi31(class_num, word_list, idx):
    P1 = class_num[1] / (class_num[0] + class_num[1])
    P0 = 1 - P1
    A = idx
    B = np.column_stack((A[:,1], A[:,0]))
    C = np.repeat([np.array(class_num)], len(idx), axis=0) - A
    D = sum(class_num) - A - B - C
    
    chi_word_1_0 = (A*D-C*B)**2 / ((A+B)*(C+D))
    chi_word_1, chi_word_0 = chi_word_1_0[:,0], chi_word_1_0[:,1]
    chi_word = P0 * chi_word_0 + P1 * chi_word_1
    dic = {}
    for i in range(len(word_list)):
        dic[word_list[i]] = chi_word[i]
    sorted_list = sorted(dic.items(), key=lambda x:x[1], reverse=True)
    # sorted_word = []
    # for word, chi_word in sorted_list:
    #     sorted_word.append(word)
    sorted_word = [x[0] for x in sorted_list]
    return sorted_word
def chi3(class_num, word_list, idx):
    P1 = class_num[1] / (class_num[0] + class_num[1])
    P0 = 1 - P1
    dic = {}
    for i in range(len(idx)):
        A1 = idx[i][1]
        B1 = idx[i][0]
        C1 = class_num[1] - A1
        D1 = class_num[0] - B1
        A0, B0, C0, D0 = B1, A1, D1, C1
        chi_word_1 = (A1*D1-C1*B1)**2 / ((A1+B1)*(C1+D1))
        chi_word_0 = (A0*D0-C0*B0)**2 / ((A0+B0)*(C0+D0))
        chi_word = P0 * chi_word_0 + P1 * chi_word_1
        dic[word_list[i]] = chi_word
    sorted_list = sorted(dic.items(), key=lambda x:x[1], reverse=True)
    sorted_word = []
    for word, chi_word in sorted_list:
        sorted_word.append(word)
    
    return sorted_word

def fs2(documents, labels, percentage):
    word_set = set()
    for document in documents:
        words = document.split()
        word_set.update(words)
    word_list = list(word_set)
    word_list.sort()

    sorted_words = chi2(word_list, documents, labels)
    top_k_words = sorted_words[:int(percentage * len(sorted_words))]
    
    return top_k_words

def chi2(word_list, documents, labels, filter_size=12):
    
    def cal(word, labels, documents):
        A1, B1, C1, D1 = 0, 0, 0, 0
        A0, B0, C0, D0 = 0, 0, 0, 0
        for i in range(len(documents)):
            if word in documents[i].split():
                if labels[i] == 1:
                    A1 += 1
                    B0 += 1
                else:
                    B1 += 1
                    A0 += 1
            else:
                if labels[i] == 1:
                    C1 += 1
                    D0 += 1
                else:
                    D1 += 1
                    C0 += 1
        chi_word_1 = N * (A1*D1-C1*B1)**2 / ((A1+C1)*(B1+D1)*(A1+B1)*(C1+D1))
        chi_word_0 = N * (A0*D0-C0*B0)**2 / ((A0+C0)*(B0+D0)*(A0+B0)*(C0+D0))
        return chi_word_1, chi_word_0
    
    N = len(documents)
    P1 = labels.count(1) / N
    P0 = 1 - P1
    dic = {}
    for word in word_list:
        if len(word) > filter_size:
            continue
        chi_word_1, chi_word_0 = cal(word, labels, documents)
        chi_word = P0 * chi_word_0 + P1 * chi_word_1
        dic[word] = chi_word
    sorted_list = sorted(dic.items(), key=lambda x:x[1], reverse=True)
    sorted_word = []
    for word, chi_word in sorted_list:
        sorted_word.append(word)
    
    return sorted_word
    
def fs1(documents, labels, percentage):
    word_loc_dic = {} # each word's location
    for i in range(len(documents)):
        words = documents[i].split()
        for word in words:
            if len(word) > 12:
                continue
            if word not in word_loc_dic.keys():
                word_loc_dic[word] = [i]
            else:
                word_loc_dic[word].append(i)

    sorted_words = chi1(word_loc_dic, labels)
    top_k_words = sorted_words[:int(percentage * len(sorted_words))]
    
    return top_k_words    

def chi1(word_loc_dic, labels):
    def cal(word_loc, labels):
        word_notIn_loc = [x for x in range(len(labels)) if x not in word_loc]
        word_loc, word_notIn_loc, labels = np.array(word_loc), np.array(word_notIn_loc), np.array(labels)
        
        A1 = float(np.sum(labels[word_loc] == 1))
        B1 = float(np.sum(labels[word_loc] == 0))
        C1 = float(np.sum(labels[word_notIn_loc] == 1))
        D1 = float(np.sum(labels[word_notIn_loc] == 0))

        A0, B0, C0, D0 = B1, A1, D1, C1
        # chi_word_1 = N * (A1*D1-C1*B1)**2 / ((A1+C1)*(B1+D1)*(A1+B1)*(C1+D1))
        # chi_word_0 = N * (A0*D0-C0*B0)**2 / ((A0+C0)*(B0+D0)*(A0+B0)*(C0+D0))
        chi_word_1 = (A1*D1-C1*B1)**2 / ((A1+B1)*(C1+D1))
        chi_word_0 = (A0*D0-C0*B0)**2 / ((A0+B0)*(C0+D0))
        return chi_word_1, chi_word_0
    
    N = len(labels)
    P1 = labels.count(1) / N
    P0 = 1 - P1
    dic = {}
    for word, word_loc in word_loc_dic.items():
        # if len(word) > 12:
        #     continue
        chi_word_1, chi_word_0 = cal(word_loc, labels)
        chi_word = P0 * chi_word_0 + P1 * chi_word_1
        dic[word] = chi_word
    sorted_list = sorted(dic.items(), key=lambda x:x[1], reverse=True)
    sorted_word = []
    for word, chi_word in sorted_list:
        sorted_word.append(word)
    
    return sorted_word

print(1)



