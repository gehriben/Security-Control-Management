import configparser

from nlp.matching.asset import Asset, Property, PropertyTag
from nlp.matching.tag import Tag

from assets.models import Asset as Asset_Model
from properties.models import Property as Property_odel
from tags.models import Tag as Tag_Model

class PropertyMatching():
    def __init__(self, metric=None):
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')

        self.metric = metric

    def match(self):
        # Step 1
        tag_list = self.get_all_tags()
        asset_list = self.get_assets_with_properties()

        # Step 2
        matched_controls = self.check_for_matches(asset_list, tag_list)

        # Step 3
        assets_json = self.convert_asset_object_to_json(asset_list)

        # Step 4
        # self.extract_relevant_controls(asset_list)

        # Step 5: Metric
        self.metric.set_matched_control_count(len(matched_controls))
        self.metric.set_other_metrics(assets_json)

        
        return matched_controls

    def get_all_tags(self):
        tag_list = list()

        tag_objects = Tag_Model.objects.all()
        for tag_object in tag_objects:
            tag = Tag(tag_object.name, tag_object.keywords.all(), tag_object=tag_object)
            tag.set_assigned_controls() 
            tag_list.append(tag)
        
        return tag_list
    
    def get_assets_with_properties(self):
        asset_list = list()

        assets = Asset_Model.objects.all()
        for asset_object in assets:
            property_list = list()
            for property_object in asset_object.properties.all():
                property_tag_list = list()
                for property_tag_object in property_object.property_tags.all():
                    property_tag = PropertyTag(property_tag_object.name, property_tag_object.property_keywords.split(";"), property_tag_object)
                    property_tag_list.append(property_tag)
                
                property = Property(property_object.name, property_tag_list, property_object)
                property_list.append(property)
            
            asset = Asset(asset_object.pk, asset_object.name, property_list, asset_object)
            asset_list.append(asset)
        
        return asset_list
    
    def check_for_matches(self, asset_list, tag_list):
        assets_per_control = dict()
        matching_tag_distribution_dict = dict()

        for asset in asset_list:
            property_tags = asset.get_property_tags()
            for property_tag in property_tags:
                matched_control_tags = list()
                for control_tag in tag_list:
                    matching_keywords = self.compare_keywords(property_tag, control_tag)
                    total_keywords = len(property_tag.keywords) + len(control_tag.keywords) - len(matching_keywords)
                    matching_rate = len(matching_keywords) / total_keywords

                    if matching_rate > float(self.config["TagBasedMatching"]["threshold"]):
                        control_tag_dict = {control_tag.name: { 
                            'matching_rate': matching_rate, 
                            'total_keywords': total_keywords, 
                            'matching_keywords': matching_keywords, 
                            'correspondig_control_count': len(control_tag.get_assigned_controls())  } }     
                        matched_control_tags.append(control_tag_dict)
                        assets_per_control = self.set_assets_per_control_dict(assets_per_control, asset, control_tag.assigned_controls)

                        # Metric
                        matching_tag_distribution_dict = self.calculate_matching_tag_distribution_metric(property_tag, control_tag, matching_keywords, matching_tag_distribution_dict)
                
                if matched_control_tags:
                    asset.matched_tags.append({ property_tag.name: matched_control_tags }) 

        # Metric
        self.metric.set_matching_tag_distribution(matching_tag_distribution_dict)

        return assets_per_control
    
    def compare_keywords(self, property_tag, control_tag):
        matching_keywords = list()
        for property_tag_keyword in property_tag.keywords:
            for control_tag_keyword in control_tag.keywords:
                if property_tag_keyword == control_tag_keyword.name:
                    matching_keywords.append(f"{property_tag_keyword} ({ property_tag.name }) -> { control_tag_keyword.name }({control_tag.name})")
        
        return matching_keywords

    def set_assets_per_control_dict(self, assets_per_control, asset, controls):
        asset_object = {"pk":asset.id, "name":asset.name}
        for control in controls:
            if control not in assets_per_control:
                assets_per_control[control] = list()
            
            if asset_object not in assets_per_control[control]:
                # Metric
                self.metric.set_matched_tags(self.metric.matched_tags + 1) 

                assets_per_control[control].append(asset_object)
        
        return assets_per_control

    def convert_asset_object_to_json(self, asset_list):
        assets_json = list()
        for asset in asset_list:
            asset_json = dict()
            asset_json["pk"] = asset.asset_object.pk
            asset_json["name"] = asset.name
            asset_json["matched_tags"] = asset.matched_tags

            assets_json.append(asset_json)

        return assets_json
    
    def calculate_matching_tag_distribution_metric(self, property_tag, control_tag, matching_keywords, matching_tag_distribution_dict):
        # Metric
        if property_tag.name not in matching_tag_distribution_dict:
            matching_tag_distribution_dict[property_tag.name] = {'count': 0}
            matching_tag_distribution_dict[property_tag.name]["keywords"] = matching_keywords

        matching_tag_distribution_dict[property_tag.name]["count"] += len(control_tag.get_assigned_controls())
        matching_tag_distribution_dict[property_tag.name]["keywords"].extend(matching_keywords)
        
        return matching_tag_distribution_dict

    """def extract_relevant_controls(self, asset_list):
        parent_controls = list()
        child_controls = list()

        for asset in asset_list:
            for matched_tag in asset.matched_tags:
                for property_tag, property_tag_value in matched_tag.items():
                    for control_tag in property_tag_value:
                        for tag, value in control_tag.items():
                            for coressponding_control in value["correspondig_controls"]:
                                print(coressponding_control["name"])
                                if coressponding_control["parent_control"] is None:
                                    if "concerend_assets" not in coressponding_control:
                                        coressponding_control["concerend_assets"] = list()
                                    coressponding_control["concerend_assets"].append(asset.name)
                                    parent_controls.append(control_json)
                                elif coressponding_control["parent_control"] is not None:
                                    coressponding_control["concerend_assets"] = assets
                                    child_controls.append(control_json)"""



