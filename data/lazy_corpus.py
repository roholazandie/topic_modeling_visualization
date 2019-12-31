import string
from gensim import corpora
from nltk.corpus import stopwords


class LazyCorpus(object):
    def __init__(self, corpus_name):
        self.corpus_name = corpus_name
        self.printable = set(string.printable)
        #words = [["".join(list(filter(lambda x: x in self.printable, word))) for word in line.lower().split()] for line in open(corpus_name, encoding="utf-8")]
        words = [[word for word in line.lower().split()] for line in open(corpus_name, encoding="utf-8")]
        num_docs = len(words)
        words = [[''.join(ch for ch in word if ch.isalnum() or ch == ' ') for word in doc] for doc in words]
        self.dictionary = corpora.Dictionary(words)
        #stop_ids = [self.dictionary.token2id[stopword] for stopword in stopwords.words('english') if stopword in self.dictionary.token2id]
        persian_stops = [s.rstrip() for s in open("/home/rohola/Codes/Python/topic_modeling_visualization/dataset/persian.txt").readlines()]
        stop_ids = [self.dictionary.token2id[stopword] for stopword in persian_stops if stopword in self.dictionary.token2id]

        bad_ids = [tokenid for tokenid, docfreq in self.dictionary.dfs.items() if docfreq<=20 or docfreq>= 0.7*num_docs]
        #bad_ids = [tokenid for tokenid, docfreq in self.dictionary.dfs.items() if docfreq == 1]
        self.dictionary.filter_tokens(stop_ids + bad_ids)
        self.dictionary.compactify()

    def __iter__(self):
        for line in open(self.corpus_name, encoding="utf-8"):
            words = [word for word in line.lower().split()]
            yield self.dictionary.doc2bow(words)#if some token in thw words is not in dictionary the doc2bow will ignore it

    def serialize_corpus(self, file_name,corpus):
        corpora.MmCorpus.serialize(file_name, corpus)

    def save_dictionary(self, file_name):
        self.dictionary.save(file_name)