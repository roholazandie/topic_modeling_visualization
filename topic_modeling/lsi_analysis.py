from gensim import models

from data.corpus import CorpusManager
from visualization import topic_modeling_semantic_network as topic_modeling_semantic_network

file_name = '/home/rohola/Codes/Python/topic_modeling_visualization/dataset/sample_texts/bbc_news_corpus.txt'
out_file_name = 'ssa'#
num_topics = 10#
num_topics_to_show = 5
num_words = 10
power_iters = 5 #controls the accuracy of the algorithm

corpus_manager = CorpusManager()
corpus, dictionary = corpus_manager.read_corpus(file_name)

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_topics, power_iters=power_iters) # initialize an LSI transformation

topics = []
for topic in lsi.print_topics(num_topics=num_topics_to_show, num_words=num_words):
    topics.append([((item.split('*')[1]).strip(' "'), float(item.split('*')[0])) for item in topic[1].split('+')])

topic_modeling_semantic_network.visualize_semantic_netwrok(topics,
                                                           visualize_method='plotly',
                                                           filename=out_file_name,
                                                           title='Latent Semantic Indexing')

print('done')
