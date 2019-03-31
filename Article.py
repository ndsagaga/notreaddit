import json
import re
from datetime import datetime


class Article:
    def __init__(self, id, data):
        self.id = id
        self.title = data['title']
        self.body = data['content']
        date = re.split(r'[\s,]', data['date'])
        del date[-1]
        time = re.split(r'[\s:]', data['time'])
        if time[-1] == 'pm':
            time[0] = str(int(time[0]) + 11)
        del time[-1]
        self.timestamp = int(datetime(int(date[2]), 2, int(date[0]), int(time[0]), int(time[1])).timestamp())


def convertArticle():
    i = 1
    articles = []

    try:
        with open("data.json") as outfile:
            json_data = json.load(outfile)

            for data in json_data['data']:
                article = Article(i, data)
                articles.append(article)
                i += 1

        # for a in articles:
        #     print(str(a.id) + a.title + "\n" + a.body + "\n" + str(a.timestamp) + "\n")

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
