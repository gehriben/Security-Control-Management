import pandas as pd
import matplotlib.pyplot as plt
import math
import configparser

from unidecode import unidecode
from sklearn.cluster import KMeans
from sklearn.feature_extraction._stop_words import ENGLISH_STOP_WORDS
from sklearn.decomposition import PCA

CLUSTER_FRACTURE = 0.2

class KeywordClustering():
    def __init__(self, keywords, cluster_fracture=CLUSTER_FRACTURE):
        self.config = configparser.ConfigParser()  
        self.config.read('config.cfg')

        self.keywords = keywords
        self.n_cluster = math.ceil(len(self.keywords) * cluster_fracture)

    def do_clustering(self):
        self.keywords["tokens"] = self.keywords["keywords"].apply(lambda x: self.to_tokens(x, stopwords=list(ENGLISH_STOP_WORDS), min_chars=3,))
        vocab = set(self.keywords["tokens"].explode())
        self.keywords["vector"] = self.keywords["tokens"].apply(lambda x: self.to_vector(x,vocab))
        self.clustering(self.keywords)
        # self.print_cluster(self.keywords)
        # self.visualize_cluster(self.keywords)

        return self.format_cluster(self.keywords)

    def to_tokens(self, s, stopwords=None, min_chars=1):
        """
        Transforms sentence to list of tokens.  

        Basic: transform special characters to ascii + lowercase.  
        Options:  
        - remove stopwords (provide list of stopwords)  
        - set minimum length for tokens: will remove any shorter token. 
        
        Returns sorted tokens
        """
        s = unidecode(str(s)) # convert to ASCII to remove special characters
        s = s.lower() # lowercase
        tokens = s.split(" ") # split the string into a list of words
        
        if min_chars > 1:
            tokens = [word for word in tokens if len(word) >= min_chars] # remove any shorter words
        
        if stopwords is not None:
            tokens = [word for word in tokens if word not in stopwords] # remove words if they appear in our stopwords list
        
        tokens = set(tokens) # transforming a list to a set removes duplicates
        tokens = sorted(tokens) # converts our set back to a list and sorts words in alphabetical order
        return tokens
    
    def to_vector(self, keyword,vocab):
        """
        Calculates vector of keyword on given vocabulary.

        Returns vector as a list of values.  
        """
        vector = []
        for word in vocab:
            if word in keyword:
                vector.append(1)
            else:
                vector.append(0)
        return vector
    
    def clustering(self, keywords):
        try:
            kmeans = KMeans(n_clusters = self.n_cluster, init=self.config["Clustering"]["clustering_algorithm"], random_state=0).fit(keywords["vector"].to_list())
            # kmeans = KMeans(n_clusters = self.n_cluster, init='random', random_state=0).fit(keywords["vector"].to_list())
            keywords["kmeans"] = list(kmeans.labels_)
        except:
            print("Clustering error!")
            print(keywords["vector"].to_list())
        # print(keywords.groupby("kmeans")["keywords"].count())

    def print_cluster(self, keywords):
        for i in range(self.n_cluster):
            print("")
            print(f"Cluster {i}")
            print("-----------------------------------")
            cluster = keywords[keywords["kmeans"] == i]
            print(cluster['keywords'])
            print("")

    def visualize_cluster(self, keywords):
        vectors = keywords["vector"].to_list()

        pca = PCA(n_components=2).fit(vectors)
        pca_2d = pca.transform(vectors)
        plt.scatter(pca_2d[:,0], pca_2d[:,1], c=keywords["kmeans"])
        plt.show()
    
    def format_cluster(self, keywords):
        keyword_clusters = dict()
        for i in range(self.n_cluster):
            cluster = keywords[keywords["kmeans"] == i]
            keywords_per_cluster = list()
            for index, row in cluster.iterrows():
                keyword = row['keywords']
                associated_security_controls = row['sc']

                keyword_dict = { keyword: associated_security_controls }
                keywords_per_cluster.append(keyword_dict)

            keyword_clusters["Cluster "+str(i)] = keywords_per_cluster

        return keyword_clusters
