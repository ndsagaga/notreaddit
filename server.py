from flask import Flask

import notreaddit

app = Flask(__name__)


@app.route('/find/<query>', methods=['GET', 'POST'])
def search(query):
    return notreaddit.search(query)


@app.route('/')
def hello_world():
    return 'Welcome to !readdit'


if __name__ == '__main__':
    app.run("0.0.0.0", 80, True)
