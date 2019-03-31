import nltk


def isNoun(tag):
    return tag[0].upper() == 'N'


def isVerb(tag):
    return tag[0].upper() == 'V'


def isAdverb(tag):
    return tag[0].upper() == 'R'


def isPronoun(tag):
    return tag[0].upper() == 'P' and tag[1].upper() == 'R'


def isAdjective(tag):
    return tag[0].upper() == 'J'


def isPreposition(tag):
    return tag.upper() == 'IN'


def isPossessive(tag):
    return tag.upper() == 'POS'


def removeWordsWithTags(tokens):
    # Rules
    # if adjective,noun -> remove noun (the *happy* boy)
    # if Adverb,verb -> remove adverb (*slowly* walking)
    # if Verb,Verb -> remove first verb (she *was* thinking)
    # remove punctuations after removing everything because we need context for pronouns

    tokenStack = []

    for token in tokens:
        if isNoun(token[1]):
            if isAdjective(tokenStack[-1][1]):
                tokenStack.pop()
            tokenStack.append(token)

        if isVerb(token[1]):
            if isVerb(tokenStack[-1][1]) or isAdverb(tokenStack[-1][1]):
                tokenStack.pop()
            tokenStack.append(token)

        if isPossessive(token[1]):
            continue

        if isPronoun(token[1]):
            tokenStack.append(closelyRelatedNoun([t for t in tokenStack if isNoun(t)], token))

        if token[1] in [',', '.', ':', '\'', '\"', '(', ')', '!', '-']:
            continue

    return tokenStack


def posTag(text):
    tokens = nltk.word_tokenize(text)
    tokens = nltk.tag.pos_tag(tokens)

    stemmer = nltk.stem.snowball.SnowballStemmer("english")
    tokens = [tuple([stemmer.stem(token[0]), token[1]]) for token in tokens]

    return tokens


def closelyRelatedNoun(nouns, pronoun):
    return nouns[-1]


if __name__ == '__main__':
    print(nltk.pos_tag(nltk.word_tokenize("The quick good fox jumps over the lazy dog")))
    print(nltk.tag.pos_tag(nltk.word_tokenize("The quick brown fox jumps over the lazy dog")))
