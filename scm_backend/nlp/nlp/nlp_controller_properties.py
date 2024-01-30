import configparser

from nlp.nlp.nlp import NLP
from nlp.nlp.object_groups.property_group import PropertyGroup
from nlp.nlp.tag import Tag

from properties.models import Property
from properties.models import PropertyTag

from metrics.metrics import Metrics
from .cluster_cleaning import ClusterCleaning

MAX_CONTROLS = 0
MAX_PROPERTIES = 0

class NLPControllerProperties():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')

        self.metrics = Metrics("Properties")
        self.metrics.initalize()

        self.nlp = NLP(float(self.config["Clustering"]["property_cluster_fracture"]), self.metrics)

    def analyse_properties(self):
        tag_list = list()

        print("--- Startig NLP Analysis ---")
        
        # Step 1
        print(" --> Organize Properties")
        property_groups = self.organize_properties()
        print(" - All Properties are prepared -")

        print("")

        # Step 2
        print(" -- Analyse parent properties --")
        texts = dict()
        for property_group in property_groups:
            texts[property_group.parent_object.name] = property_group.parent_object.name.lower() + "\n" + property_group.parent_object.description.lower()

        tags = self.nlp.nlp(texts)
        tag_list.extend(tags)
        print(" -- Finishid analysis of parent properties --")

        print("")

        # Step 3
        print(" -- Analyse each property with its children --")
        for property_group in property_groups:
            if property_group.child_objects:
                print(f" - {property_group.parent_object.name} -")
                tags = self.nlp.nlp(property_group.get_group_descriptions())
                tag_list.extend(tags)
        print(" -- Finishid analysis --")
        
        print("")

        # Step 4
        print(" -- Create Tag objects and assigns tags to properties --")
        self.create_property_tag_objects(tag_list)
        self.assign_tags_to_properties(tag_list, property_groups)
        self.set_property_cluster_distribution_metric()

        print("")

        # Step 5
        if self.config["Clustering"]["use_cluster_cleaning"] == "true":
            print(" -- Cleaning Clusters --")
            cluster_cleaner = ClusterCleaning(isPropertyTag=True)
            cluster_cleaner.start_cleaning()

            print("")
        
        print(" --- NLP Analysis finished ---")

        # Print Results
        # self.print_controls()
    
    def organize_properties(self):
        property_groups = list()

        count = 0
        for property in Property.objects.filter(parent_property=None):
            if property.parent_property is None:
                property_group = PropertyGroup(property)
                property_group.set_child_objects()

                property_groups.append(property_group)
        
                count += 1

            if count >= MAX_PROPERTIES and not MAX_PROPERTIES <= 0:
                break
        
        return property_groups
    
    def create_property_tag_objects(self, property_tags):
        for tag in property_tags:
            keyword_string = ';'.join(str(e) for e in tag.keywords)

            tag_object =  PropertyTag.objects.filter(name=tag.name)
            if not tag_object:
                tag_object = PropertyTag.objects.create(name=tag.name, property_keywords=keyword_string)

                # Metric
                self.metrics.set_tags_counter(self.metrics.tags_counter + 1)
            else:
                tag_object = tag_object[0]
                keyword_string = tag_object.property_keywords + ";" + keyword_string
                tag_object.property_keywords = keyword_string
                
            tag.tag_object = tag_object

            # Metric
            self.metrics.set_keywords_counter(self.metrics.keywords_counter + len(tag.keywords))
            self.metrics.set_keyword_cluster_distributions(tag.name, len(tag.keywords))

    def assign_tags_to_properties(self, tags, property_groups):
        for property_group in property_groups:
            for tag in tags:
                for property in tag.tagged_objects:
                    property_group.assign_tag(tag.tag_object, property)
    
    def set_property_cluster_distribution_metric(self):
        property_tag_objects = PropertyTag.objects.all()
        for property_tag_object in property_tag_objects:
            self.metrics.set_control_cluster_distributions(property_tag_object.name, len(property_tag_object.property_set.all()))