from assets.models import Asset

class ControlMatching():
    def __init__(self, metric=None):
        self.metric = metric
    
    # Returns controls which suit to the defined assets
    def match(self):
        assets_per_control = self.assign_assets_to_controls()

        return assets_per_control

    # Assigns for each control the asset that was responsible for its selection
    def assign_assets_to_controls(self):
        assets_per_control = dict()
        matching_tag_distribution_dict = dict()

        assets = Asset.objects.all()
        for asset in assets:
            asset_object = {"pk":asset.pk, "name":asset.name}
            for tag in asset.tags.all():
                # Metric
                self.metric.set_matched_tags(self.metric.matched_tags + 1)

                controls_for_tag = tag.control_set.all()
                for control in controls_for_tag:
                    if control not in assets_per_control:
                        assets_per_control[control] = list()
                    
                    if asset_object not in assets_per_control[control]:
                        assets_per_control[control].append(asset_object)
                
                if tag.name not in matching_tag_distribution_dict:
                    matching_tag_distribution_dict[tag.name] = 0
                
                matching_tag_distribution_dict[tag.name] += len(controls_for_tag)
        # Metric
        self.metric.set_matching_tag_distribution(matching_tag_distribution_dict)

        # Metric
        self.metric.set_matched_control_count(len(assets_per_control))

        return assets_per_control