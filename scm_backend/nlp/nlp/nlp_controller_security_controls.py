import configparser

from nlp.nlp.nlp import NLP
from nlp.nlp.object_groups.security_control_group import SecurityControlGroup
from nlp.nlp.tag import Tag

from controls.models import Control
from tags.models import Tag, Keyword
from metrics.metrics import Metrics
from .cluster_cleaning import ClusterCleaning

MAX_CONTROLS = 0
MAX_PROPERTIES = 0

class NLPControllerSecurityControls():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')

        self.metrics = Metrics("Security_Controls")
        self.metrics.initalize(0, 0, dict(), dict(), 0, 0, 0, 0, 0, list(), dict())

        self.nlp = NLP(float(self.config["Clustering"]["control_cluster_fracture"]), self.metrics)

    def analyse_security_controls(self):
        tag_list = list()

        print("--- Startig NLP Analysis ---")
        
        # Step 1
        print(" --> Organize Controls")
        security_control_groups = self.organize_security_controls()
        print(" - All Controls are prepared -")

        print("")

        # Step 2
        print(" -- Analyse parent controls --")
        texts = dict()
        for security_control_group in security_control_groups:
            texts[security_control_group.parent_object.name] = security_control_group.parent_object.name.lower() + "\n" + security_control_group.parent_object.description.lower()

        tags = self.nlp.nlp(texts)
        tag_list.extend(tags)
        print(" -- Finishid analysis of parent controls --")

        print("")

        # Step 3
        print(" -- Analyse each control with its children --")
        for security_control_group in security_control_groups:
            if security_control_group.child_objects:
                print(f" - {security_control_group.parent_object.name} -")
                tags = self.nlp.nlp(security_control_group.get_group_descriptions())
                tag_list.extend(tags)
        print(" -- Finishid analysis --")

        print("")

        # Step 4
        print(" -- Create Tag objects and assigns tags to security controls --")
        self.create_security_control_tag_objects(tag_list)
        self.assign_tags_to_security_controls(tag_list, security_control_groups)
        self.set_control_cluster_distribution_metric()

        print("")

        # Step 5
        if self.config["Clustering"]["use_cluster_cleaning"] == "true":
            print(" -- Cleaning Clusters --")
            cluster_cleaner = ClusterCleaning(isPropertyTag=False)
            cluster_cleaner.start_cleaning()

            print("")
        
        print(" --- NLP Analysis finished ---")

        # Print Results
        # self.print_controls()
    
    def organize_security_controls(self):
        security_control_groups = list()

        count = 0
        for security_control in Control.objects.filter(parent_control=None):
            if security_control.parent_control is None:
                security_control_group = SecurityControlGroup(security_control)
                security_control_group.set_child_objects()

                security_control_groups.append(security_control_group)
        
                count += 1

            if count >= MAX_CONTROLS and not MAX_CONTROLS <= 0:
                break
        
        return security_control_groups
    
    def create_security_control_tag_objects(self, security_control_tags):
        for tag in security_control_tags:
            tag_object =  Tag.objects.filter(name=tag.name)
            keyword_ids = self.create_security_control_keyword_objects(tag_object, tag.keywords)

            if not tag_object:
                tag_object = Tag.objects.create(name=tag.name, description=tag.description)

                # Metric
                self.metrics.set_tags_counter(self.metrics.tags_counter + 1)
            else:
                tag_object = tag_object[0]
                
            tag_object.keywords.add(* keyword_ids)
            tag.tag_object = tag_object

            # Metrics
            self.metrics.set_keyword_cluster_distributions(tag.name, len(keyword_ids))
    
    def create_security_control_keyword_objects(self, tag, keywords):
        keyword_ids = set()
        for keyword in keywords:
            keyword_object =  Keyword.objects.filter(name=keyword)
                
            if not keyword_object:
                keyword_object = Keyword.objects.create(name=keyword)
                
                # Metric
                self.metrics.set_keywords_counter(self.metrics.keywords_counter + 1)
            else:
                keyword_object = keyword_object[0]

            if not tag or not keyword_object.tag_set.filter(pk=tag[0].pk).exists():
                keyword_ids.add(keyword_object.pk)
        return keyword_ids

    def assign_tags_to_security_controls(self, tags, security_control_groups):
        for security_control_group in security_control_groups:
            for tag in tags:
                for control in tag.tagged_objects:
                    security_control_group.assign_tag(tag.tag_object, control)
    
    def set_control_cluster_distribution_metric(self):
        tag_objects = Tag.objects.all()
        for tag_object in tag_objects:
            self.metrics.set_control_cluster_distributions(tag_object.name, len(tag_object.control_set.all()))
        
