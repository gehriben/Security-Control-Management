from tags.models import Tag
from properties.models import PropertyTag
from metrics.metrics import Metrics

import configparser

ACCEPTED_CLUSTER_SIZE_DIFFERENCE = 8.0
ACCEPTED_CLUSTER_ASSOCIATED_OBJECT_DIFFERENCE = 10.0

class ClusterCleaning():
    def __init__(self, isPropertyTag=False):
        self.config = configparser.ConfigParser()  
        self.config.read('config.cfg')

        self.clusters = dict()
        self.isPropertyTag = isPropertyTag

        self.average_cluster_size = 0
        self.average_cluster_object_associations = 0
        self.deleted_clusters = 0

        if isPropertyTag:
            self.metrics = Metrics("Properties")
        else:
            self.metrics = Metrics("Security_Controls") 

        self.metrics.initalize()

    def start_cleaning(self):
        # Step 1
        self.clusters = self.get_clusters()

        # Step 2
        self.analyze_clusters()

        # Step 3
        self.clean_clusters()


    def get_clusters(self):
        if not self.isPropertyTag:
            return self.get_control_clusters()
        else:
            return self.get_property_clusters()

    def get_control_clusters(self):
        clusters = dict()
        tags = Tag.objects.all()
        for tag in tags:
            clusters[tag.name] = dict()
            keyword_list = list()
            for keyword in tag.keywords.all():
                keyword_list.append(keyword.name)
            
            clusters[tag.name] = {
                'id': tag.id,
                'associated_objects': tag.control_set.all(),
                'keywords': keyword_list
            }
        
        return clusters
    
    def get_property_clusters(self):
        clusters = dict()
        tags = PropertyTag.objects.all()
        for tag in tags:
            clusters[tag.name] = dict()
            keyword_list = list()
            for keyword in tag.property_keywords.split(";"):
                keyword_list.append(keyword)
            
            clusters[tag.name] = {
                'id': tag.id,
                'associated_objects': tag.property_set.all(),
                'keywords': keyword_list
            }
        
        return clusters

    def analyze_clusters(self):
        for cluster_name, cluster_infos in self.clusters.items():
            self.average_cluster_size += len(cluster_infos['keywords'])
            self.average_cluster_object_associations += len(cluster_infos['associated_objects'])
        
        self.average_cluster_size = self.average_cluster_size / len(self.clusters)
        self.average_cluster_object_associations = self.average_cluster_object_associations / len(self.clusters)
    
    def clean_clusters(self):
        for cluster_name, cluster_infos in self.clusters.items():
            if (len(cluster_infos['keywords']) > self.average_cluster_size * float(self.config["Clustering"]["accepted_cluster_size_difference"]) 
            or len(cluster_infos['associated_objects']) > self.average_cluster_object_associations * float(self.config["Clustering"]["accepted_cluster_associated_object_difference"]) ):
                if self.isPropertyTag:
                    PropertyTag.objects.filter(id=cluster_infos['id']).delete()
                else:
                    Tag.objects.filter(id=cluster_infos['id']).delete()
                
                self.deleted_clusters += 1
        
        self.metrics.set_deleted_clusters(self.deleted_clusters)
        print(f"{self.deleted_clusters} deleted clusters")

