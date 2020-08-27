# Python Standard Libraries
from collections import Counter
import string
import re
# External Libraries
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import numpy as np

def tokenize_string(string:str) -> list:
    tknzr = TweetTokenizer()
    return tknzr.tokenize(string)

def get_most_common_words(data):
    common_words = Counter()
    #for row in data:
    for word in data.split(" "):
        punctuation = str.maketrans(dict.fromkeys(string.punctuation))
        word = word.translate(punctuation)
        common_words[word] += 1
    return common_words

def get_most_common_bigrams(data):
    common_bigrams = Counter()
    
    last_word = ""
    rows = data.split(" ")
    for word in rows:
        punctuation = str.maketrans(dict.fromkeys(string.punctuation))
        word = word.translate(punctuation)
        if len(word) > 1:
            if len(last_word) > 1:
                common_bigrams[f"{last_word} {word}"] += 1
        last_word = word
    return common_bigrams
            

def get_most_common_words_lemmatized(data):
    common_words = Counter()
    for row in data:
        tokens = tokenize_string(row)
        for word in tokens:
            punctuation = str.maketrans(dict.fromkeys(string.punctuation))
            word = word.translate(punctuation)
            common_words[word] += 1
    return common_words

def remove_common_stop_words(common_words):
    for i, word in enumerate(list(common_words)):
        # This allows the method to be used on bigrams
        if isinstance(word, tuple):
            words = word[0].split(" ")
            for word in words:
                if word in stopwords.words("english") or len(word) < 3:
                    common_words[i] = ("", 0)
        else:
            if word in stopwords.words("english") or len(word) < 3:
                    common_words[word] = 0
    return common_words

def topic_modelling(title, data):
    # Remove punctuation
    data = re.sub('[,\.!?]', '', data)
    
    # Remove numbers
    data = re.sub('[0-9]', '', data)
    
    
    # Convert the titles to lowercase
    data = data.lower()
    
    count_vectorizer = CountVectorizer(stop_words='english')
    count_data = count_vectorizer.fit_transform([data])
    
    number_topics = 5
    number_words = 10
    
    lda = LDA(n_components=number_topics, n_jobs=-1)
    lda.fit(count_data)
    
    def print_topics(model, count_vectorizer, n_top_words):
        words = count_vectorizer.get_feature_names()
        for topic_idx, topic in enumerate(model.components_):
            print("\nTopic #%d:" % topic_idx)
            print(" ".join([words[i]
                            for i in topic.argsort()[:-n_top_words - 1:-1]]))
            
    print_topics(lda, count_vectorizer, number_words)
    pass