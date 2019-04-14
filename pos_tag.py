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


def isDeterminant(tag):
    return tag.upper()[-2:] == 'DT'


def removeWordsWithTags(tokens):
    # Rules
    # if adjective,noun -> remove noun (the *happy* boy)
    # if Adverb,verb -> remove adverb (*slowly* walking)
    # if Verb,Verb -> remove first verb (she *was* thinking)
    # possessive and determinant and punctuations are removed during pos-tagging

    tokenStack = []
    for token in tokens:
        if isNoun(token[1]):
            tokenStack.append(token)
            continue

        if isVerb(token[1]):
            tokenStack.append(token)
            continue

        if isPronoun(token[1]):
            n = closelyRelatedNoun([t for t in tokenStack if isNoun(t)], token)
            if n:
                tokenStack.append(n)
            continue

        if isPreposition(token[1]):
            tokenStack.append(token)
            continue

        if token[0] == token[1]:
            continue

    return tokenStack


def get_wordnet_pos(pos):
    """
    return WORDNET POS compliance to WORDENT lemmatization (a,n,r,v)
    """
    if pos[0] == 'J':
        return nltk.corpus.wordnet.ADJ
    elif pos[0] == 'V':
        return nltk.corpus.wordnet.VERB
    elif pos[0] == 'N':
        return nltk.corpus.wordnet.NOUN
    elif pos[0] == 'R':
        return nltk.corpus.wordnet.ADV
    else:
        # As default pos in lemmatization is Noun
        return nltk.corpus.wordnet.NOUN


# All pronouns are already dereferenced, but if by chance it has not, employ this method
def closelyRelatedNoun(nouns, pronoun):
    return nouns[-1] if len(nouns) > 0 else None


def posTag(text):
    tokens = nltk.word_tokenize(text)
    tokens = nltk.tag.pos_tag(tokens)

    cleanTokens = []

    # basic stopwords removal
    for token in tokens:
        if isPossessive(token[1]):
            continue
        if isDeterminant(token[1]):
            continue
        # punctuations
        if token[0] == token[1]:
            continue

        cleanTokens.append(
            tuple([nltk.stem.WordNetLemmatizer().lemmatize(token[0].lower(), get_wordnet_pos(token[1])), token[1]]))

    return cleanTokens