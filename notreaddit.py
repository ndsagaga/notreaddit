import json

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
    articles = fileToArticles("data.json")
    results = ir.rankedSearch("goods")
    print(results)

    for r in results:
        print(articles[r].body)
        articles[r].tree.draw()
