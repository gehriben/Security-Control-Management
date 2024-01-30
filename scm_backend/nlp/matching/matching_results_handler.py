from django.db.models import Count

from nlp.matching.control_matching import ControlMatching
from nlp.matching.property_matching import PropertyMatching

from metrics.metrics import Metrics
from controls.models import Control
from constraints.models import ConstraintAssociation
from assets.models import Asset, AssetControlMatch

class MatchingResultsHandler():
    def __init__(self):
        self.property_metric = Metrics("Properties")
        self.property_metric.initalize()
        self.control_metric = Metrics("Security_Controls")
        self.control_metric.initalize()

        self.property_matching = PropertyMatching(self.property_metric)
        self.control_matching = ControlMatching(self.control_metric)

    def get_matching_results_with_assets_per_control(self):
        # Step 1
        assets_per_control = self.get_assets_per_control()

        # Step 2
        matching_controls = self.organize_controls(assets_per_control)

        return matching_controls
    
    def get_matching_results_with_per_asset(self, asset_id):
        # Step 1
        assets_per_control = self.get_controls_per_asset(asset_id)

        # Step 2
        matching_controls = self.organize_controls(assets_per_control)

        return matching_controls

    def organize_controls(self, assets_per_control):
        # Step 1
        parent_controls = self.get_parent_controls(assets_per_control)
        child_controls = self.get_child_controls(assets_per_control)

        # Step 2
        control_count = self.handle_statistics(parent_controls, child_controls)

        # Step 3
        matching_controls = self.set_child_controls(parent_controls, child_controls, control_count)

        # self.validate_control_matches(control_matching_controls)
        # self.validate_property_matches(property_matching_controls)

        return matching_controls
    
    def get_controls_per_asset(self, asset_id):
        assets_per_control_dict = dict()
        controls_per_asset = AssetControlMatch.objects.filter(asset_id = asset_id)

        for control_per_asset in controls_per_asset:
            asset_object = { 'pk': control_per_asset.asset.pk, 'name': control_per_asset.asset.name }
            control = control_per_asset.control

            if control not in assets_per_control_dict:
                    assets_per_control_dict[control] = list()
            if asset_object not in assets_per_control_dict[control]:
                    assets_per_control_dict[control].append(asset_object)
        
        return assets_per_control_dict
    
    def get_assets_per_control(self):
        data = AssetControlMatch.objects.values('control_id').annotate(dcount=Count('control_id')).order_by()
        assets_per_control_dict = dict()

        for element in data:
            assets_per_control = AssetControlMatch.objects.filter(control_id = element["control_id"])
            for asset_per_control in assets_per_control:
                asset_object = { 'pk': asset_per_control.asset.pk, 'name': asset_per_control.asset.name }
                control = asset_per_control.control

                if control not in assets_per_control_dict:
                        assets_per_control_dict[control] = list()
                if asset_object not in assets_per_control_dict[control]:
                        assets_per_control_dict[control].append(asset_object)
        
        return assets_per_control_dict

    # Return all controls which have no parent and are therefore parent_controls itself
    def get_parent_controls(self, assets_per_control):
        parent_controls = list()
        for control, assets in assets_per_control.items():
            if control.parent_control is None:
                control_json = self.convert_control_object_to_json(control)
                control_json["concerend_assets"] = assets
                parent_controls.append(control_json)
        
        return parent_controls
    
    # Return all controls which have a parent and are therefore child controls
    def get_child_controls(self, assets_per_control):
        child_controls = list()
        for control, assets in assets_per_control.items():
            if control.parent_control is not None:
                    control_json = self.convert_control_object_to_json(control)
                    control_json["concerend_assets"] = assets
                    child_controls.append(control_json)
        
        return child_controls

    def convert_control_object_to_json(self, control_object):
        control_json = dict()
        control_json["pk"] = control_object.pk
        control_json["cn"] = control_object.cn
        control_json["name"] = control_object.name
        control_json["description"] = control_object.description
        if control_object.parent_control is not None:
           control_json["parent_control_id"] = control_object.parent_control.pk
        else:
           control_json["parent_control_id"] = None 

        return control_json

    # Evaluates various metrics about the assignment
    def handle_statistics(self, parent_controls, child_controls):
        # Set counter
        control_count = len(parent_controls) + len(child_controls)
        
        return control_count
    
    def check_child_controls_for_impcat(self, assets_per_control, parent_control, constraint_association):
        child_controls = Control.objects.filter(parent_control=parent_control)
        asset_object = {"pk":constraint_association.asset.pk, "name":constraint_association.asset.name}

        for child_control in child_controls:
            control_impacts = ConstraintAssociation.objects.filter(control_id=child_control.pk)
            for control_impcat in control_impacts:
                if constraint_association.selected_value["value"] == control_impcat.selected_value["value"]:
                    if child_control not in assets_per_control:
                        assets_per_control[child_control] = list()
            
                    if asset_object not in assets_per_control[child_control]:
                        assets_per_control[child_control].append(asset_object)
                    
        return assets_per_control

    # Assigns the child controls to the corresponding parent control and returns complete list
    def set_child_controls(self, parent_controls, child_controls, control_count):
        matching_controls = parent_controls
        for matching_control in matching_controls:
            matching_control["child_controls"] = list()
            matching_control["control_count"] = control_count
            for child_control in child_controls:
                if child_control["parent_control_id"] == matching_control["pk"]:
                    matching_control["child_controls"].append(child_control)
        
        return matching_controls