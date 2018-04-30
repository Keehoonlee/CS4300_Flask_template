from nltk.corpus import wordnet
from nltk import word_tokenize
import os

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
    cur = ""
    for a in all_query:
        cur = ""
        for s in a:
            s = s.replace("_"," ")
            cur += s.encode("ascii")
            cur += " "

    return cur
