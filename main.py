# -*- coding: utf-8 -*-
# @Time : 2021/10/25 15:22
# @Author : huangkai
# @Email : huangkai@mucfc.com

import numpy as np
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence
import jieba

np.random.seed(1337)  # For Reproducibility
import sys

sys.setrecursionlimit(1000000)

# define parameters
maxlen = 100


def create_dictionaries(model=None,
                        combined=None):
    ''' Function does are number of Jobs:
        1- Creates a word to index mapping
        2- Creates a word to vector mapping
        3- Transforms the Training and Testing Dictionaries

    '''
    if (combined is not None) and (model is not None):
        gensim_dict = Dictionary()
        gensim_dict.doc2bow(model.wv.vocab.keys(),
                            allow_update=True)
        #  freqxiao10->0 所以k+1
        w2indx = {v: k + 1 for k, v in gensim_dict.items()}  # 所有频数超过10的词语的索引,(k->v)=>(v->k)
        w2vec = {word: model[word] for word in w2indx.keys()}  # 所有频数超过10的词语的词向量, (word->model(word))

        def parse_dataset(combined):  # 闭包-->临时使用
            ''' Words become integers
            '''
            data = []
            for sentence in combined:
                new_txt = []
                for word in sentence:
                    try:
                        new_txt.append(w2indx[word])
                    except:
                        new_txt.append(0)  # freqxiao10->0
                data.append(new_txt)
            return data  # word=>index

        combined = parse_dataset(combined)
        combined = sequence.pad_sequences(combined, maxlen=maxlen)  # 每个句子所含词语对应的索引，所以句子中含有频数小于10的词语，索引为0
        return w2indx, w2vec, combined
    else:
        print('No data provided...')


def input_transform(string, model):
    words = jieba.lcut(string)
    words = np.array(words).reshape(1, -1)

    _, _, combined = create_dictionaries(model, words)
    return combined


def lstm_predict(string, model, w2v_model):
    data = input_transform(string, w2v_model)
    data.reshape(1, -1)
    # print data
    result = model.predict_classes(data)
    # print result # [[1]]
    if result[0] == 1:
        return (string, ' positive')
    elif result[0] == 0:
        return (string, ' neural')
    else:
        return (string, ' negative')
