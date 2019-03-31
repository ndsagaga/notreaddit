import json

import gensim
from nltk.corpus import stopwords

from article import Article


def fileToArticles(filename):
    i = 0
    articles = []

    try:
        with open(filename) as outfile:
            json_data = json.load(outfile)

            for data in json_data['data']:
                article = Article(i, data)
                articles.append(article)
                i += 1

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

    return articles


if __name__ == '__main__':
    tos = []
    with open("data.json") as outfile:
        json_data = json.load(outfile)

        for data in json_data['data']:
            tos.append(
                [x for x in gensim.utils.simple_preprocess(data['content']) if x not in stopwords.words('english')])
    print(tos)
    model = gensim.models.Word2Vec(
        tos,
        size=len(tos),
        window=10,
        min_count=1,
        workers=10)
    model.train(tos, total_examples=len(tos), epochs=10)
    print(model.wv.similar_by_word("visit"))
