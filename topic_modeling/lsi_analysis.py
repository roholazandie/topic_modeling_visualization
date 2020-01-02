from gensim.models import TfidfModel, LsiModel
from data.corpus import CorpusManager
from visualization import topic_modeling_semantic_network as topic_modeling_semantic_network
from configs import LSIConfig

config_file = "/Users/shasa/Downloads/topic_modeling_visualization-master/configs/lsi_config.json"
config = LSIConfig.from_json_file(config_file)


corpus_manager = CorpusManager()
corpus, dictionary = corpus_manager.read_corpus(config.dataset_dir)

tfidf = TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

lsi = LsiModel(corpus_tfidf, id2word=dictionary, num_topics=config.num_topics, power_iters=config.power_iters) # initialize an LSI transformation


topic_words = lsi.show_topics(config.num_topics_to_show, num_words=config.num_words, formatted=False)
topic_words = [j for (i, j) in topic_words]


visualize_method = ""
if config.dimension == 2:
    visualize_method = 'plotly'
elif config.dimension == 3:
    visualize_method = 'plotly3d'
else:
    raise("Wrong dimension, can accept only 2 or 3")

topic_modeling_semantic_network.visualize_semantic_netwrok(config,
                                                           topic_words,
                                                           visualize_method=visualize_method)

