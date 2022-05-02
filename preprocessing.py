# -*- coding: utf-8 -*-
"""
corpus preprocessing
"""

import re

# use the regular grammar to filter some useless symbols
chinese = re.compile(r'[\u4E00-\u9FA5`~!@#$%^&*()_\-+=<>?:"{}|,.;·~！@#￥%……&*（）——\-+={}|《》？：“”【】、；‘，。、|\n]{1,}')

# read fr and process it into fw
fr = open('corpus/2014_corpus.txt', 'r', encoding='utf-8', errors='ignore')
fw = open('corpus/2014_corpus_pre.txt', 'w', encoding='utf-8')
txt = fr.read()
for w in chinese.findall(txt):
    fw.write(w)
fr.close()
fw.close()