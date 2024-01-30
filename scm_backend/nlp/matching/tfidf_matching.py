import configparser
import numpy as np 

from sklearn.feature_extraction.text import TfidfVectorizer
from assets.models import Asset, AssetControlMatch
from controls.models import Control
from metrics.metrics import Metrics

class TFIDFMatching():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')
        self.tfidf_metric = Metrics("TFIDF")
        self.tfidf_metric.initalize()

        self.threshold_distribution = dict()
    
    def start_matching(self):
        print("--- Starting TFIDF Matching ---")

        # Step 1
        assets = self.get_assets()

        # Step 2
        controls = self.get_controls()

        # Step 3
        self.match_assets(assets, controls)

        # Step 4
        self.tfidf_metric.set_other_metrics(self.threshold_distribution)

        print("--- Finished TFIDF Matching ---")

    def get_assets(self):
        return Asset.objects.all()
    
    def get_controls(self):
        return Control.objects.all()

    def match_assets(self, assets, controls):
        for asset in assets:
            corpus = self.build_corpus(asset, controls)
            matching_indexes = self.calculate_similarity(corpus)
            matched_controls = set()
            for matching_index in matching_indexes:
                matched_controls.add(controls[matching_index-1])

            matched_controls = self.get_parent_controls(matched_controls)
            self.create_asset_control_association(asset, matched_controls)

            # Metric
            self.tfidf_metric.set_matched_control_count(self.tfidf_metric.matched_control_count + len(matched_controls))
    
    def build_corpus(self, asset, controls):
        corpus = [asset.description]
        
        control_descriptions = list()
        for control in controls:
            control_descriptions.append(control.description)

        corpus.extend(control_descriptions)

        return corpus

    def calculate_similarity(self, corpus):
        # Use sklearn to generate document term matrix
        vectorizer = TfidfVectorizer()
        document_term_matrix = vectorizer.fit_transform(corpus)

        # Generate document similarity matrix
        pairwise_similarity = document_term_matrix * document_term_matrix.transpose()

        # Show the document similarity matrix
        arr = pairwise_similarity.toarray()

        np.fill_diagonal(arr, -1)
        
        index_list = list()
        for index, value in enumerate(arr[0]):
            if value > float(self.config["Tfidf"]["threshold"]):
                index_list.append(index)
                self.set_threshold_distribution(value)

        return index_list
    
    def get_parent_controls(self, matched_controls):
        matched_controls_with_parents = set()
        for control in matched_controls:
            matched_controls_with_parents.add(control)
            if control.parent_control != None and control.parent_control not in matched_controls:
                print(f"Added parent {control.parent_control.name}")
                matched_controls_with_parents.add(control.parent_control)
        
        return matched_controls_with_parents

    def create_asset_control_association(self, asset, controls):
        for control in controls:
            AssetControlMatch.objects.create(asset=asset, control=control)
    
    def set_threshold_distribution(self, value):
        if value in self.threshold_distribution:
            self.threshold_distribution[value] += 1
        else:
            self.threshold_distribution[value] = 1