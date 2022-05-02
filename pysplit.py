# -*- coding: utf-8 -*-
"""
split the pinyin sequence
"""


def pysplit(word, wordList):
    """
    @function: use to call the recursive function DynamicProgramming
    and return the array storing the split results.
    @word: the pinyin sequence needed to be split
    @wordList: the list of split rules
    """
    res = []
    DynamicProgramming(res, word, wordList)
    return res


def DynamicProgramming(res, word, wordList, pinyinListStr=''):
    """
    @function: split the sequence recursively
    @res: the array to save the split result
    @word: the pinyin sequence
    @wordList: the list of split rules
    @pinyinListStr: the temporary variable to save the previous result
    """
    wordLen = len(word)
    for i in range(0, wordLen + 1):
        pList = pinyinListStr.split(',')
        if word[0:i] in wordList:
            if i == wordLen:
                pList.append(word[0:i])
                res.append(pList[1:])
            else:
                pList.append(word[0:i])
                DynamicProgramming(res, word[i:], wordList, ','.join(pList))