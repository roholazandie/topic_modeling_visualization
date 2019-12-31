import os
from data.lazy_corpus import LazyCorpus
from gensim import corpora
from data.preprocessing import Preprocessing
import gensim


class CorpusManager:
    '''
    CorpusManager use gensim dump files(.mm and .dict) to improve the performance when the files have not changes
    if there isn't any file CorpusManager will try to create those files
    '''

    def read_corpus(self, file_name):
        # to check if the file is too big we need to create a .mm and .dict file for future
        stat_info = os.stat(file_name)
        if stat_info.st_size > 1e6:
            if self.file_changed(file_name):
                corpus = []
                lazyCorpus = LazyCorpus(file_name)
                for vector in lazyCorpus:
                    corpus.append(vector)
                lazyCorpus.serialize_corpus(file_name + '.mm', corpus)
                lazyCorpus.save_dictionary(file_name + '.dict')
                dictionary = corpora.Dictionary.load(file_name + '.dict')
            else:
                corpus = corpora.MmCorpus(file_name + '.mm')
                dictionary = corpora.Dictionary.load(file_name + '.dict')
        else:
            corpus = []
            lazyCorpus = LazyCorpus(file_name)
            for vector in lazyCorpus:
                corpus.append(vector)

            lazyCorpus.save_dictionary(file_name + '.dict')
            dictionary = corpora.Dictionary.load(file_name + '.dict')
        return corpus, dictionary

    def file_changed(self, file_name):
        return True
        if os.path.isfile(file_name + 'db'):
            old_file_size = open(file_name + 'db').readline()
            if int(old_file_size) == os.stat(file_name).st_size:
                return False
            return True
        else:
            with open(file_name + 'db', 'w') as file_writer:
                file_writer.write(str(os.stat(file_name).st_size))
            return True


class DirDataset(object):
    """Iterate over sentences of all plaintext files in a directory """
    # SPLIT_SENTENCES = re.compile(u"[.!?:]\s+")  # split sentences on these characters
    SPLIT_SENTENCES = "\n"

    def __init__(self, dirname):
        self.dirname = dirname
        self.preprocessing = Preprocessing()

    def __iter__(self):
        for fn in os.listdir(self.dirname):
            text = open(os.path.join(self.dirname, fn)).read()
            for sentence in self.SPLIT_SENTENCES.split(text):
                yield self.preprocessing.process(sentence)

    def get_docs(self):
        docs = []
        for fn in os.listdir(self.dirname):
            text = open(os.path.join(self.dirname, fn)).read()
            doc = ""
            for sentence in self.SPLIT_SENTENCES.split(text):
                doc += self.preprocessing.process(sentence)
            docs.append(doc)
        return docs


class FileDataset():
    """each line is a document in this format"""
    SPLIT_DOCS = "\n"

    def __init__(self, filename):
        self.filename = filename
        self.preprocessing = Preprocessing()

    def get_docs(self):
        docs = []
        with open(self.filename) as read_file:
            for doc in read_file:
                docs.append(' '.join(gensim.utils.simple_preprocess(doc, deacc=True)))
                # docs.append(self.preprocessing.simple_preprocess(doc))
        return docs

    def file_changed(self):
        if os.path.isfile(self.filename + '.dataset.config'):
            old_file_size = open(self.filename + '.dataset.config').readline()
            if int(old_file_size) == os.stat(self.filename).st_size:
                return False
            return True
        else:
            with open(self.filename + '.dataset.config', 'w') as file_writer:
                file_writer.write(str(os.stat(self.filename + '.dataset.config').st_size))
            return True
