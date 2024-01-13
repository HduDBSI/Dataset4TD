# calculate chi(word,1) and chi(word,0)
def cal_chi_word_class(word, documents, labels):
    A1, B1, C1, D1 = 0., 0., 0., 0.
    for i in range(len(documents)):
        if word in documents[i].split():
            if labels[i] == 1:
                A1 += 1
            else:
                B1 += 1
        else:
            if labels[i] == 1:
                C1 += 1
            else:
                D1 += 1
    A0, B0, C0, D0 = B1, A1, D1, C1
    chi_word_1 = (A1*D1-C1*B1)**2 / ((A1+B1)*(C1+D1))
    chi_word_0 = (A0*D0-C0*B0)**2 / ((A0+B0)*(C0+D0))
    return chi_word_1, chi_word_0

def chi(word_list, documents, labels):
    P1 = labels.count(1) / len(documents)
    P0 = 1 - P1
    dic = {}
    for word in word_list:
        chi_word_1, chi_word_0 = cal_chi_word_class(word, documents, labels)
        chi_word = P0 * chi_word_0 + P1 * chi_word_1
        dic[word] = chi_word
    
    return dic

def split_list_to_nlist(list, sub_list_size):
    num = 0
    tmp = []
    nlist = []
    for i in range(len(list)):
        if num == sub_list_size:
            nlist.append(tmp)
            tmp = []
            num = 0
        tmp.append(list[i])
        num += 1
    if tmp != []:
        nlist.append(tmp)
    return nlist


# documents = [document_1, document_2, document_3, ...]
# document_i = "word_1 word_2 word_3" 
# labels is a list combined with 0 and 1
def feature_word_select(documents:list, labels:list, percentage=0.1):
    # get all words      
    word_set = set()
    for document in documents:
        words = document.split()
        word_set.update(words)
    word_list = list(word_set)
    word_list.sort()

    dic = chi(word_list, documents, labels)
    sorted_list = sorted(dic.items(), key=lambda x:x[1], reverse=True)
    sorted_chi_word = [x[0] for x in sorted_list]
    
    top_k_words = sorted_chi_word[:int(percentage * len(sorted_chi_word))]
    return top_k_words

# only for test
def main():
    documents = ["today i am happy !", "she is not happy at all", "let us go shopping !",
        "mike was so sad last night", "amy did not love it", "it is so amazing !"
    ]
    labels = [1, 0, 1, 0, 0, 1]
    words = feature_word_select(documents, labels, 0.3)
    print(words)

if __name__ == '__main__':
    main()