import json
import sys

import spacy

from IRModel import IRModel
from article import Article

ir = None
articles = []


def fileToArticles(filename):
    global ir, articles
    i = 0
    articles = []
    ir = IRModel()
    nlp = spacy.load('en_coref_lg')

    try:
        with open(filename) as outfile:
            print("Loading data from " + filename)
            json_data = json.load(outfile)

            for data in json_data['data']:

                doc = nlp(data['content'])
                if doc._.has_coref:
                    data['content'] = doc._.coref_resolved

                article = Article(i, data)
                articles.append(article)
                ir.addDoc(article)
                i += 1

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

    ir.build()

    return articles


def search(query):
    results = ir.rankedSearch(query)

    for r in results:
        print("Article id: " + str(articles[r].id))
        print("Title: " + str(articles[r].title))
        print("Content: " + str(articles[r].body))

        # if running in remote headless server, will throw error
        try:
            articles[r].trees.draw()
        except:
            print(articles[r].trees)

        print("-------------------------------------------------------------------------------")


def build(filename=None):
    global articles

    if filename:
        articles = fileToArticles(sys.argv[1])
    else:
        articles = fileToArticles("data.json")


if __name__ == '__main__':
    build((sys.argv[1] if len(sys.argv) > 1 else None))

    query = input("Enter a query or enter 'exit': ")

    while query != 'exit':
        search(query)
        query = input("Enter a query or enter 'exit': ")
