import re
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def compute_sentiment_intensity(text):
    """Returns a [score] after a sentimental analysis on [text].
    As text consists of multiple sentences, calculates the score
    for each sentence and averages the scores for each sentence to
    get the score for [text].

    Negative scores = negative sentiment
    Positive scores = positive sentiment
    0               = neutral sentiment

    text: string """

    analyzer = SentimentIntensityAnalyzer()

    #Tokenizing the text into sentences
    splitter = re.compile(r"""
    (?<![A-Z])  # last character cannot be uppercase
    [.!?]       # match punctuation
    \s+         # followed by whitespace
    (?=[A-Z])   # next character must be uppercase
    """, re.VERBOSE)

    sentences = splitter.split(text)
    n_sentences = len(sentences)

    #Calculating the scores
    sentiment_scores = np.zeros(n_sentences)
    for idx,sentence in enumerate(sentences):
        score = analyzer.polarity_scores(sentence)
        sentiment_scores[idx] = score["compound"]

    avg_score = sum(sentiment_scores)/n_sentences

    return avg_score
