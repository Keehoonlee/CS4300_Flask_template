from nltk.corpus import wordnet
from nltk import word_tokenize

NUM_EXPAND = 5

def one_query(query):
    """return synonyms for one word"""
    synonyms = []
    for syn in wordnet.synsets(query):
        for l in syn.lemmas():
            if l.name() not in synonyms and l.name() != query:
                synonyms.append(l.name())
    return synonyms

def query_expand(queries, num=NUM_EXPAND):
    """return combined synonyms for multiple words"""
    words = word_tokenize(queries)
    all_query = []
    for w in words:
        all_query.append(one_query(w))
    res = []
    for i in range(num):
        cur = ""
        for a in all_query:
            cur += a[i]
            cur += " "
        res.append(cur)
    return res
