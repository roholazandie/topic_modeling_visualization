import numpy as np
from gensim.models import LdaModel
from data.corpus import CorpusManager
from visualization import topic_modeling_semantic_network as topic_modeling_semantic_network
from configs import LDAConfig

config_file = "/home/rohola/Codes/Python/topic_modeling_visualization/configs/lda_config.json"
config = LDAConfig.from_json_file(config_file)

corpus_manager = CorpusManager()
corpus, dictionary = corpus_manager.read_corpus(config.dataset_dir)



lda = LdaModel(corpus=corpus,
               id2word=dictionary,
               num_topics=config.num_topics,
               update_every=1,
               passes=6,
               alpha=config.alpha,
               eta='auto')

topic_words = lda.show_topics(config.num_topics_to_show, num_words=config.num_words, formatted=False)
topic_words =[j for (i,j) in topic_words]


for topic in topic_words:
    for word, p in topic:
        print(word)
    print('\n')

topic_modeling_semantic_network.visualize_semantic_netwrok(topic_words,
                                                           visualize_method='plotly',
                                                           filename=config.out_file_name,
                                                           title="Latent Dirichlet Analysis")