import json
import sys

from IRModel import IRModel
from article import Article

ir = None


def fileToArticles(filename):
    global ir
    i = 0
    articles = []
    ir = IRModel()

    try:
        with open(filename) as outfile:
            print("Loading data from " + filename)
            json_data = json.load(outfile)

            for data in json_data['data']:
                article = Article(i, data)
                articles.append(article)
                ir.addDoc(article)
                i += 1

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

    ir.build()

    return articles


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        articles = fileToArticles(sys.argv[1])
    else:
        articles = fileToArticles("data.json")

    query = input("Enter a query or enter 'exit': ")

    while query != 'exit':
        results = ir.rankedSearch(query)

        for r in results:
            print("Article id: " + str(articles[r].id))
            print("Title: " + str(articles[r].title))
            print("Content: " + str(articles[r].body))
            print("-------------------------------------------------------------------------------")

            # if running in remote headless server, will throw error
            try:
                articles[r].tree.draw()
            except:
                print(articles[r].tree)

        query = input("Enter a query or enter 'exit': ")
