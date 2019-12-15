import json


class LDAConfig:

    def __init__(self,
                 dataset_dir="",
                 out_file_name="",
                 num_topics="",
                 num_topics_to_show="",
                 num_words="",
                 alpha=""):
        self.dataset_dir = dataset_dir
        self.out_file_name = out_file_name
        self.num_topics = num_topics
        self.num_topics_to_show = num_topics_to_show
        self.num_words = num_words
        self.alpha = alpha

    @classmethod
    def from_dict(cls, json_object):
        config = LDAConfig()
        for key in json_object:
            config.__dict__[key] = json_object[key]
        return config

    @classmethod
    def from_json_file(cls, json_file):
        with open(json_file) as f:
            config_json = f.read()

        return cls.from_dict(json.loads(config_json))

