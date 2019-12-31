# coding:utf-8
from __future__ import unicode_literals
from nltk.tokenize import RegexpTokenizer
import codecs
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer


class Preprocessing(object):
    '''
    this module do basic nlp preprocessing
    '''

    def __init__(self, ):
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = LancasterStemmer()
        self.stopwords = []

    def get_tokens(self, dataset):
        Tokens = []
        for key, value in dataset.iteritems():
            documentText = value
            cleanedTokens = self.process(documentText)
            for token in cleanedTokens:
                Tokens.append(token)
        return Tokens

    def process(self, document_text):
        tokens = self.remove_punctuations_and_numbers(document_text)
        tokens = self.lemmatizing(tokens)
        tokens = self.remove_stopwords(tokens)

        #tokens = self.Stemming(tokens)
        return tokens

    def simple_preprocess(self, sentence_text):
        tokens = self.remove_punctuations_and_numbers(sentence_text)
        tokens = self.lemmatizing(tokens)
        tokens = self.remove_stopwords(tokens)
        return ''.join(tokens)

    def remove_punctuations_and_numbers(self, document_text):
        Tokens = []
        toker = RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+|\d+.\d+|[0-9]+', gaps=True)
        tokensWithoutPunctuations = toker.tokenize(document_text)
        for token in tokensWithoutPunctuations:
            Tokens.append(token)
        return Tokens

    def remove_stopwords(self, tokens):
        new_stopwords = [stopword.encode('utf-8') for stopword in stopwords.words('english')]
        return [token for token in tokens if token.lower() not in new_stopwords]

    def stemming(self, tokens):
        return [self.stemmer(token) for token in tokens]

    def lemmatizing(self, words):
        lemmatizing_out = []

        for word in words:
            try:
                lemmatizing_out.append(self.lemmatizer.lemmatize(word))
            except:
                pass
        return lemmatizing_out