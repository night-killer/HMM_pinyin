# -*- coding: utf-8 -*-
"""
HMM class
"""
import json
from pysplit import pysplit


def takeSecondFirst(elem):
    return elem[1][0]


def takeFirst(elem):
    return elem[0]

class HMM:
    def __init__(self):
        self.load_param()

    def load_param(self):
        """
        @function: load parameters necessary for HMM calculation
        @init_prob: initial state distribution
        @trans_prob: transition probability matrix
        @emiss_prob: observation probability matrix
        @pinyin_states: list of homophonic characters
        @pyList: list of pinyin split dictionary
        """
        self.init_prob = self.read('init_prob')
        self.emiss_prob = self.read('emiss_prob')
        self.trans_prob = self.read('trans_prob')
        self.pinyin_states = self.read('pinyin_states')
        self.pyList = []
        self.dictGenerate()

    def dictGenerate(self):
        """
        @function: generate pyList
        @smList: consonant list
        @ymList: rhyme list
        @ztrList: integral syllable list
        """
        smList = 'b,p,m,f,d,t,n,l,g,k,h,j,q,x,z,c,s,r,zh,ch,sh,y,w'.split(',')
        ymList = 'a,o,e,i,u,v,ai,ei,ui,ao,ou,iu,ie,ve,er,an,en,in,un,ang,eng,ing,ong,uai,ia,uan,uang,uo,ua'.split(',')
        ztrdList = 'a,o,e,ai,ei,ao,ou,er,an,en,ang,zi,ci,si,zhi,chi,shi,ri,yi,wu,yu,yin,ying,yun,ye,yue,yuan'.split(',')
        for s in smList:
            for y in ymList:
                tmp = s + y
                if tmp not in self.pyList:
                    self.pyList.append(tmp)

        for z in ztrdList:
            if z not in self.pyList:
                self.pyList.append(z)

    def read(self, filename):
        """
        @function: load the json file
        @filename: the file storing the probability matrix
        """
        with open('params/' + filename + '.json', 'r') as f:
            return json.load(f)

    def trans(self, strs):
        """
        @function: predict possible word sequences by viterbi algorithm
        @strs: the pinyin sequence
        """
        # split the pinyin sequence
        seq = pysplit(strs, self.pyList)
        self.min_f = -3.14e+100 # the minimum used to smooth
        res = [] # the array to store results

        for n in range(len(seq)):
            length = len(seq[n])
            viterbi = {} # the dictionary storing the possibility of every node on the route
            for i in range(length):
                viterbi[i] = {}

            # initize by using the initial state distribution
            # BOS is the symbol of a start of a word sequence
            # P[0][s] = P(s)*P(seq[n][0]|s)
            for s in self.pinyin_states.get(seq[n][0]):
                viterbi[0][s] = (self.init_prob.get(s, self.min_f) +
                                 self.emiss_prob.get(s, {}).get(seq[n][0], self.min_f), -1)

            # DP
            # P[i+1][s] = max(P[i][pre]P(s|pre)P(seq[n][i+1]|s))
            for i in range(length - 1):
                for s in self.pinyin_states.get(seq[n][i + 1]):
                    viterbi[i + 1][s] = max(
                        [(viterbi[i][pre][0] + self.emiss_prob.get(s, {}).get(seq[n][i + 1], self.min_f)
                          + self.trans_prob.get(s, {}).get(pre, self.min_f), pre) for pre in
                         self.pinyin_states.get(seq[n][i])])

            # P[length - 1][s] = P[length - 1][s]*P(EOS|s)
            for s in self.pinyin_states.get(seq[n][-1]):
                viterbi[length - 1][s] = (viterbi[length - 1][s][0] + self.trans_prob.get('EOS', {}).get(s, self.min_f),
                                          viterbi[length - 1][s][1])

            # take the most possible 100 results out
            words_list = [x for x in viterbi[length - 1].items()]
            words_list.sort(key=takeSecondFirst, reverse=True)
            for i in range(min(len(words_list), 100)):
                words = [None] * length
                words[-1] = words_list[i][0]

                for n in range(length - 2, -1, -1):
                    words[n] = viterbi[n + 1][words[n + 1]][1]

                res.append((i, ''.join(w for w in words)))
        res = list(set(res))
        res.sort(key=takeFirst)
        return [x[1] for x in res]
