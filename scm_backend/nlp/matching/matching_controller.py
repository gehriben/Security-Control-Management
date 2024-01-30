from nlp.matching.control_matching import ControlMatching
from nlp.matching.property_matching import PropertyMatching

from metrics.metrics import Metrics
from controls.models import Control
from constraints.models import ConstraintAssociation
from assets.models import Asset, AssetControlMatch

class MatchingController():
    def __init__(self):
        self.property_metric = Metrics("Properties")
        self.property_metric.initalize()
        self.control_metric = Metrics("Security_Controls")
        self.control_metric.initalize()

        self.property_matching = PropertyMatching(self.property_metric)
        self.control_matching = ControlMatching(self.control_metric)

    def match(self):
        print("--- Startig Control Matching ---")
        # Step 1
        control_matching_controls = self.control_matching.match()
        property_matching_controls = self.property_matching.match()
        assets_per_control = self.combine_dicts(control_matching_controls, property_matching_controls)
        
        # Step 2
        assets_per_control = self.get_child_controls_by_impact(assets_per_control)

        # Step 3
        self.create_asset_control_association(assets_per_control)

        print(" --- Control Matching finished! ---")

    def combine_dicts(self, control_matching_controls, property_matching_controls):
        assets_per_control = control_matching_controls

        for property_matching_control, assets in property_matching_controls.items():
            if property_matching_control not in assets_per_control:
                assets_per_control[property_matching_control] = list()
            
            for asset in assets:
                if asset not in assets_per_control[property_matching_control]:
                    assets_per_control[property_matching_control].append(asset)
        
        return assets_per_control

    def get_child_controls_by_impact(self, assets_per_control):
        assets_per_control_with_impact = assets_per_control.copy()

        for control, assets in assets_per_control.items():
            if control.parent_control is None:
                for asset in assets:
                    constraint_associations = ConstraintAssociation.objects.filter(asset_id=asset["pk"])
                    for constraint_association in constraint_associations:
                        if constraint_association.constraint.name == "Impact":
                            assets_per_control_with_impact = self.check_child_controls_for_impcat(assets_per_control_with_impact, control, constraint_association)
                            
        return assets_per_control_with_impact
    
    def create_asset_control_association(self, assets_per_control):
        AssetControlMatch.objects.all().delete()
        for control, assets in assets_per_control.items():
            for asset in assets:
                asset = Asset.objects.get(pk=asset["pk"])
                AssetControlMatch.objects.create(asset=asset, control=control)

