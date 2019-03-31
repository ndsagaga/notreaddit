import operator

import math

from pos_tag import posTag


class IRModel:

    def __init__(self):
        self.N = 0
        self._termList = []
        self._docLists = []
        self._docLength = []
        self._queryLength = 0.0

    # split the words of one article
    # populate termList with raw terms
    # each term in the termList has a docList of DocTerm instance
    def addDoc(self, article):
        words = [x[0] for x in article.tokens]
        self.N += 1

        for i in range(len(words)):
            match = False
            word = words[i]

            if (word not in self._termList):
                self._termList.append(word)
                _docList = []
                doc = DocTerm(article.id, 1)
                _docList.append(doc)
                self._docLists.append(_docList)
            else:
                index = self._termList.index(word)
                _docList = self._docLists[index]

                for dt in _docList:
                    if (dt.docId == article.id):
                        dt.tw += 1
                        match = True
                        break

                if (not match):
                    doc = DocTerm(article.id, 1)
                    _docList.append(doc)


    # computer tfidf
    def build(self):
        self._docLength = [0] * self.N

        for i in range(len(self._termList)):
            docList = self._docLists[i]
            df = len(docList)

            for j in range(len(docList)):
                doc = docList[j]
                tfidf = (1 + math.log10(doc.tw)) * math.log10(self.N / df * 1.0)
                self._docLength[doc.docId] += math.pow(tfidf, 2)
                doc.tw = tfidf

        for i in range(self.N):
            self._docLength[i] = math.sqrt(self._docLength[i])


    # Ranked retrieval based on cosine similarity
    def rankedSearch(self, query):
        docs = dict()
        queryTokens = posTag(query)

        for token in queryTokens:
            term = token[0]
            index = -1

            for _, word in enumerate(self._termList):
                if word == term:
                    index = _

            if index < 0:
                continue

            docList = self._docLists[index]

            qtfidf = (1 + math.log10(1)) * math.log10(self.N * 1.0 / len(docList))
            self._queryLength += math.pow(qtfidf, 2)

            for i in range(len(docList)):
                doc = docList[i]
                score = doc.tw * qtfidf

                if (doc.docId not in docs):
                    docs[doc.docId] = score
                else:
                    score += docs[doc.docId]
                    docs[doc.docId] = score

        self._queryLength = math.sqrt(self._queryLength)

        # normalization begins here
        numerator = 0.0

        for docScore in docs.values():
            numerator += docScore

        cosineVals = dict()

        for docId, docScore in docs.items():
            cosineVals[docId] = numerator / (self._queryLength * self._docLength[docId])

        sorted_cosine = sorted(cosineVals.items(), key=operator.itemgetter(1), reverse=True)

        return [x[0] for x in sorted_cosine]


class DocTerm:
    def __init__(self, did, tw):
        self.docId = did
        self.tw = tw
