import configparser
import pandas as pd

from django.db.models.query import EmptyQuerySet

from nlp.nlp_algorithms.rake_manager import RakeManager
from nlp.nlp_algorithms.spacy_manager import SpacyManager
from nlp.nlp_algorithms.keybert_manager import KeybertManager
from nlp.nlp_algorithms.yake_manager import YakeManager
from nlp.nlp_algorithms.textrazor_manager import TextrazorManager
from nlp.nlp.topic_modeling import TopicModeling
from nlp.nlp.keyword_clustering import KeywordClustering
from nlp.nlp.tag import Tag

class NLP():
    def __init__(self, cluster_fracture, metric=None):
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')

        self.nlp_algorithm = None
        self.metric = metric
        self.cluster_fracture = cluster_fracture

    def nlp(self, texts):
        # Step 1
        print("  --> Extracting Keywords")
        df_keywords = self.extract_keywords(texts)
        
        # Step 2
        print("  --> Clustering Keywords")
        keyword_clusters = self.cluster_keywords(df_keywords)

        # Step 3
        print("  --> Modeling topics and creates tags")
        tags = self.model_topics(keyword_clusters)

        return tags

    def extract_keywords(self, texts):
        keywords_dict = dict()
        df_keywords = pd.DataFrame({'keywords':[], 'sc': []})

        for object_name, text in texts.items():
            self.nlp_algorithm = self.get_keyword_extraction_algorithm(text)            
            keywords = self.nlp_algorithm.do_nlp()        

            for keyword in keywords:
                if keyword in keywords_dict and not object_name in keywords_dict[keyword]:
                    keywords_dict[keyword].append(object_name)
                else:
                    keywords_dict[keyword] = list()
                    keywords_dict[keyword].append(object_name)

        for key, value in keywords_dict.items():
            mapping_dict = {'keywords':key, 'sc':[value]}
            df_control_keywords = pd.DataFrame(mapping_dict)
            df_keywords = df_keywords.append(df_control_keywords, ignore_index = True)
        
        return df_keywords
    
    def cluster_keywords(self, df_keywords):
        keyword_clustering = KeywordClustering(df_keywords, self.cluster_fracture)
        return keyword_clustering.do_clustering()

    def model_topics(self, keyword_clusters):
        tags = list()
        for cluster, keywords in keyword_clusters.items():
            keyword_list = list()
            tagged_object_set = set()

            for keyword in keywords:
                keyword_list.append(list(keyword.keys())[0])

                tagged_objects = list(keyword.values())[0]
                for tagged_object in tagged_objects:
                    tagged_object_set.add(tagged_object)

            topic_modeling = TopicModeling(keyword_list)
            
            if self.config["TopicModeling"]["algorithm"] == "most_used_word":
                topic = topic_modeling.word_weighting()
            else:
                topic = topic_modeling.do_lda_topic_modeling()

            tag = Tag(name=topic, keywords=keyword_list, tagged_objects=tagged_object_set)
            tags.append(tag)

        return tags
    
    def get_keyword_extraction_algorithm(self, text):
        algorithm = self.config['KeywordExtraction']['algorithm']

        if algorithm == "Rake":
            return RakeManager(text)
        elif algorithm == "Spacy":
            return SpacyManager(text)
        elif algorithm == "Yake":
            return YakeManager(text)
        elif algorithm == "Keybert":
            return KeybertManager(text)
        else:
            raise("Invalid Keyword Extraction Algorithm (Choose between Rake, Spacy, Yake and Keybert)!")






