# -*- coding: utf-8 -*-
"""
HMM parameters calculation
init_prob - Initial state distribution
trans_prob - Transition probability matrix
emiss_prob - Observation probability matrix
"""

import pypinyin 
import json
import math
import re

# the folder to save the parameters
dirname = 'params'


def load():
    """
    @function: load the corpus and return the split sequences
    """
    file = 'corpus/2014_corpus_pre.txt' # the corpus

    # use regular grammar to extract the chinese from the preprocessed corpus
    chinese = re.compile(r'[\u4e00-\u9fa5]{2,}')
    with open(file, 'r', encoding='utf-8') as f:
        seqs = chinese.findall(f.read())
    return seqs


def count_init(seqs):
    """
    @function: calculate the initial state distribution
    @seqs: the split sequences
    """
    init_prob = {}  # the dictionary to save the initial state distribution
    num = 0 # counter of sequences
    len_ = len(seqs)

    for seq in seqs:
        num += 1
        if not num % 10000:
            print('{}/{}'.format(num, len_))
        if len(seq) == 0:
            continue

        # count the occurence of every chinese characters
        init_prob[seq[0]] = init_prob.get(seq[0], 0) + 1
    
    # use log to normalize the probability of occurence of every chinese character
    total = len(seqs)
    for key in init_prob.keys():
        init_prob[key] = math.log(init_prob.get(key) / total)

    save('init_prob', init_prob)


def count_trans(seqs):
    """
    @function: calculate the transition probability matrix
    @seqs: the split sequences
    *****format*****
    trans_prob = {
        word1: {pre_word11: num11, pre_word12: num12, ...},
        word2: {pre_word21: num21, pre_word22: num22, ...},
    }
    """
    trans_prob = {}  # the dictionary to save the transition probability matrix
    num = 0 # counter of sequences
    len_ = len(seqs)

    for seq in seqs:
        num += 1
        if not num % 10000:
            print('{}/{}'.format(num, len_))
        if len(seq) == 0:
            continue

        # split the seq into array of single chinese charaters
        seq = [w for w in seq]

        # for convenience, insert delimiters to the sequence
        seq.insert(0, 'BOS')
        seq.append('EOS')

        # count the occurence of "[pre][post]"
        for index, post in enumerate(seq):
            if index:
                pre = seq[index - 1]
                if not trans_prob.get(post, None):
                    trans_prob[post] = {}
                trans_prob[post][pre] = trans_prob[post].get(pre, 0) + 1

    # use log to normalize the transition probability matrix
    for word in trans_prob.keys():
        total = sum(trans_prob.get(word).values())
        for pre in trans_prob.get(word).keys():
            trans_prob[word][pre] = math.log(trans_prob[word].get(pre) / total)

    save('trans_prob', trans_prob)


def count_emiss(seqs):
    """
    @function: calculate the observation probability matrix
    (use pypinyin to tag every sentence)
    @seqs: the split sequences
    *****format*****
    emiss_prob = {
        word1 : {pinyin11: num11, pinyin12: num12, ...},
        word2 : {pinyin21: num21, pinyin22: num22, ...},
        ...
    }
    """
    emiss_prob = {} # the dictionary to save the observation probability matrix
    num = 0 # counter of sequences
    len_ = len(seqs)

    for seq in seqs:
        num += 1
        if not num % 10000:
            print('{}/{}'.format(num, len_))
        if len(seq) == 0:
            continue

        # tag every sentence
        pinyin = pypinyin.lazy_pinyin(seq)

        # count the occurence of pinyin of every chinese character
        for py, word in zip(pinyin, seq):
            if not emiss_prob.get(word, None):
                emiss_prob[word] = {}
            emiss_prob[word][py] = emiss_prob[word].get(py, 0) + 1

    # use log to normalize the observation probability
    for word in emiss_prob.keys():
        total = sum(emiss_prob.get(word).values())
        for key in emiss_prob.get(word):
            emiss_prob[word][key] = math.log(emiss_prob[word][key] / total)

    save('emiss_prob', emiss_prob)


def count_pinyin_states():
    """
    @function: find the homophonic characters
    """
    with open(dirname+'/emiss_prob.json') as f:
        emiss_prob = json.load(f)
    
    data = {}
    for key in emiss_prob.keys():
        for pinyin in emiss_prob.get(key):
            if not data.get(pinyin, None):
                data[pinyin] = []
            data[pinyin].append(key)
    
    with open(dirname+'/pinyin_states.json', 'w') as f:
        json.dump(data, f)


def save(filename, data):
    """
    @function: write data into json files
    @filename: json filename
    @data: the probability matrix
    """
    with open(dirname+'/' + filename + '.json', 'w') as f:
        json.dump(data, f, indent=2)
        

def count():
    """
    @function: parameter calculation
    """
    seqs = load()

    print('Count init prob...')
    count_init(seqs)
    
    print('Count emiss prob...')
    count_emiss(seqs)
    
    print('Count trans prob...')
    count_trans(seqs)
    
    print('Count pinyin states...')
    count_pinyin_states()
    
    print('That is all...')


if __name__=='__main__':
    count()

    
    