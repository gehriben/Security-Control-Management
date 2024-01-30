from .models import Metric

class Metrics():
    def __init__(self, name):
        self.name = name
        self.metric_object = None

    def initalize(self, keywords_counter=0, tags_counter=0, keyword_cluster_distributions=dict(), control_cluster_distributions=dict(), average_keywords_per_tag=0, 
        average_controls_per_tag=0, deleted_clusters=0, matched_control_count=0, matched_tags=0, matching_tag_distribution=list(), other_metrics=dict()):
        
        self.keywords_counter = keywords_counter
        self.tags_counter = tags_counter
        self.keyword_cluster_distributions = keyword_cluster_distributions
        self.control_cluster_distributions = control_cluster_distributions
        self.average_keywords_per_tag = average_keywords_per_tag
        self.average_controls_per_tag = average_controls_per_tag
        self.deleted_clusters = deleted_clusters
        self.matched_control_count = matched_control_count
        self.matched_tags = matched_tags
        self.matching_tag_distribution = matching_tag_distribution
        self.other_metrics = other_metrics
    
    def create_metric_object(self):
        self.metric_object = Metric.objects.filter(name=self.name)

        if self.metric_object.exists():
            self.metric_object = self.metric_object[0]

            self.initalize(keywords_counter=self.metric_object.keywords_counter, tags_counter=self.metric_object.tags_counter, 
            keyword_cluster_distributions=self.metric_object.keyword_cluster_distributions, control_cluster_distributions=self.metric_object.control_cluster_distributions, 
            average_keywords_per_tag=self.metric_object.average_keywords_per_tag, average_controls_per_tag=self.metric_object.average_controls_per_tag, 
            deleted_clusters=self.metric_object.deleted_clusters, matched_control_count=self.metric_object.matched_control_count, matched_tags=self.metric_object.matched_tags, 
            matching_tag_distribution=self.metric_object.matching_tag_distribution, other_metrics=self.metric_object.other_metrics)
        else:
            self.metric_object = Metric.objects.create(name=self.name, keywords_counter=self.keywords_counter, tags_counter=self.tags_counter, 
                keyword_cluster_distributions=self.keyword_cluster_distributions, control_cluster_distributions=self.control_cluster_distributions,
                average_keywords_per_tag=self.average_keywords_per_tag, average_controls_per_tag=self.average_controls_per_tag, deleted_clusters=self.deleted_clusters,
                matched_control_count=self.matched_control_count, matched_tags=self.matched_tags, 
                matching_tag_distribution=self.matching_tag_distribution, other_metrics=self.other_metrics)
    
    def reset_metrics(self):
        self.set_matched_control_count(0)
        self.set_matched_tags(0)

    # ---------------------------------------------------
    # Set Methods
    # ---------------------------------------------------
    def set_keywords_counter(self, keyword_counter):
        if self.metric_object is None:
            self.create_metric_object()
        
        self.keywords_counter = keyword_counter
        self.metric_object = Metric.objects.filter(name=self.name).update(keywords_counter=self.keywords_counter)

    def set_tags_counter(self, tags_counter):
        if self.metric_object is None:
            self.create_metric_object()
        
        self.tags_counter = tags_counter
        self.metric_object = Metric.objects.filter(name=self.name).update(tags_counter=self.tags_counter)
    
    def set_keyword_cluster_distributions(self, tag_name, keyword_count):
        if self.metric_object is None:
            self.create_metric_object()
        
        if tag_name in self.keyword_cluster_distributions:
            self.keyword_cluster_distributions[tag_name] += keyword_count
        else:
            self.keyword_cluster_distributions[tag_name] = keyword_count
        self.metric_object = Metric.objects.filter(name=self.name)
        self.metric_object.update(keyword_cluster_distributions=self.keyword_cluster_distributions)

        self.__calculate_average_keyword_per_tag()
        self.metric_object = Metric.objects.filter(name=self.name).update(average_keywords_per_tag=self.average_keywords_per_tag)
    
    def set_control_cluster_distributions(self, tag_name, control_count):
        if self.metric_object is None:
            self.create_metric_object()
        
        if tag_name in self.control_cluster_distributions:
            self.control_cluster_distributions[tag_name] += control_count
        else:
            self.control_cluster_distributions[tag_name] = control_count
        self.metric_object = Metric.objects.filter(name=self.name).update(control_cluster_distributions=self.control_cluster_distributions)

        self.__calculate_average_control_per_tag()
        self.metric_object = Metric.objects.filter(name=self.name).update(average_controls_per_tag=self.average_controls_per_tag)
    
    def set_deleted_clusters(self, deleted_clusters):
        if self.metric_object is None:
            self.create_metric_object()
        
        self.deleted_clusters = deleted_clusters
        self.metric_object = Metric.objects.filter(name=self.name).update(deleted_clusters=self.deleted_clusters)

    def set_matched_control_count(self, matched_control_count):
        if self.metric_object is None:
            self.create_metric_object()
        
        self.matched_control_count = matched_control_count
        self.metric_object = Metric.objects.filter(name=self.name).update(matched_control_count=self.matched_control_count)
    
    def set_matched_tags(self, matched_tags):
        if self.metric_object is None:
            self.create_metric_object()
        
        self.matched_tags = matched_tags
        self.metric_object = Metric.objects.filter(name=self.name).update(matched_tags=self.matched_tags)
    
    def set_matching_tag_distribution(self, matching_tag_distribution):
        if self.metric_object is None:
            self.create_metric_object()
        
        self.matching_tag_distribution = matching_tag_distribution
        self.metric_object = Metric.objects.filter(name=self.name).update(matching_tag_distribution=self.matching_tag_distribution)

    def set_other_metrics(self, other_metrics):
        if self.metric_object is None:
            self.create_metric_object()
        
        self.other_metrics = other_metrics
        self.metric_object = Metric.objects.filter(name=self.name).update(other_metrics=self.other_metrics)

    # ---------------------------------------------------
    # Internal Functions
    # ---------------------------------------------------
    def __calculate_average_keyword_per_tag(self):
        sum = 0
        for tag_name, keyword_count in self.keyword_cluster_distributions.items():
            sum += keyword_count
        
        self.average_keywords_per_tag = sum / len(self.keyword_cluster_distributions)
    
    def __calculate_average_control_per_tag(self):
        sum = 0
        for tag_name, control_count in self.control_cluster_distributions.items():
            sum += control_count
        
        self.average_controls_per_tag = sum / len(self.control_cluster_distributions)


