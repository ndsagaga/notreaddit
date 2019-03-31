import re
from datetime import datetime

import nltk

import pos_tag


class Article:
    def __init__(self, id, data):
        self.id = id
        self.title = data['title']
        self.body = data['content']
        self.timestamp = getTimestamp(data['date'], data['time'])
        self.tokens, self.tree = process(data['content'])


def process(text):
    tokens = pos_tag.posTag(text)
    tree = chunk(pos_tag.removeWordsWithTags(tokens))
    return tokens, tree


def getTimestamp(date, time):
    date = re.split(r'[\s,]', date)
    del date[-1]

    time = re.split(r'[\s:]', time)
    if time[-1] == 'pm':
        time[0] = str(int(time[0]) + 11)
    del time[-1]

    return int(datetime(int(date[2]), 2, int(date[0]), int(time[0]), int(time[1])).timestamp())


def chunk(tokens, grammar=None):
    if grammar is None:
        grammar = ('''
                    NP: {<DT>?<JJ>*<NN.?>+}
                    NIN: {<N(IN|P)><IN><NP>} 
                    NVN: {<N(IN|P)><VB.?><N(IN|P)>?}-
                    ''')
    chunkParser = nltk.RegexpParser(grammar)
    return chunkParser.parse(tokens)


if __name__ == '__main__':
    print(pos_tag.posTag("she thought about it, and said \"great\""))
