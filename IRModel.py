import math
import operator

from pos_tag import *


class IRModel:
    _total = 0
    posTagFrequencies = {"N": 0, "V": 0, "R": 0, "J": 0, "P": 0, "I": 0}

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
        words = [(x[0], x[1]) for x in article.tokens]
        self.N += 1

        for i in range(len(words)):
            match = False
            word = words[i][0]

            _key = words[i][1][0]

            if _key in self.posTagFrequencies:
                self.posTagFrequencies[_key] += 1
                self._total += 1

            if word not in self._termList:
                self._termList.append(word)
                doc = DocTerm(article.id, 1, _key)
                self._docLists.append([doc])
            else:
                index = self._termList.index(word)
                _docList = self._docLists[index]

                for dt in _docList:
                    if dt.docId == article.id:
                        dt.tw += 1
                        match = True
                        break

                if not match:
                    doc = DocTerm(article.id, 1, _key)
                    _docList.append(doc)

    def build(self):
        print("Building the Vector Space Model")
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
        weight = 1

        for token in queryTokens:
            term = token[0]
            index = -1
            _key = token[1][0]

            for _, word in enumerate(self._termList):
                if word == term:
                    index = _
                    break

            if index < 0:
                continue

            docList = self._docLists[index]

            qtfidf = (1 + math.log10(1)) * math.log10(self.N * 1.0 / len(docList))
            self._queryLength += math.pow(qtfidf, 2)

            for i in range(len(docList)):
                doc = docList[i]

                weight = 1
                if _key == doc.posTag and _key in self.posTagFrequencies:
                    weight = 1 + self.posTagFrequencies[_key] / self._total * 1.0

                score = doc.tw * qtfidf * weight

                if (doc.docId not in docs):
                    docs[doc.docId] = score
                else:
                    docs[doc.docId] += score

        self._queryLength = math.sqrt(self._queryLength)

        cosineVals = dict()

        for docId, docScore in docs.items():
            cosineVals[docId] = docScore / (self._queryLength * self._docLength[docId])

        sorted_cosine = sorted(cosineVals.items(), key=operator.itemgetter(1), reverse=True)

        return [x[0] for x in sorted_cosine]


class DocTerm:
    def __init__(self, did, tw, posTag):
        self.docId = did
        self.tw = tw
        self.posTag = posTag


if __name__ == "__main__":
    articles = fileToArticles("data.json")
    ir = IRModel()

    for article in articles:
        ir.addDoc(article)

    ir.build()

    # one word case
    query1 = "funds"
    cosineSimilarity1 = ir.rankedSearch(query1)

    # two words case
    query2 = "terrorist attack"
    cosineSimilarity2 = ir.rankedSearch(query2)

    # three words case
    query3 = "US president Trump"
    cosineSimilarity3 = ir.rankedSearch(query3)

    # four words case
    query4 = "Facebook negotiate Cambridge analytica"
    cosineSimilarity4 = ir.rankedSearch(query4)

    print(cosineSimilarity1)
    print(cosineSimilarity2)
    print(cosineSimilarity3)
    print(cosineSimilarity4)
