class Asset():
    def __init__(self, id, name, properties, asset_object):
        self.id = id
        self.name = name
        self.properties = properties
        self.matched_tags = list() # [{ [PropertyTag]: [ [Tag]:{matching_rate: 70%, ...}, [Tag]: {matching_rate: 0%, ...}, [Tag]: ... ] }]
        
        self.asset_object = asset_object

    def get_property_tags(self):
        property_tags = list()
        for property in self.properties:
            for property_tag in property.property_tags:
                property_tags.append(property_tag)
        
        return property_tags

class Property():
    def __init__(self, name, property_tags, property_object):
        self.name = name
        self.property_tags = property_tags

        self.property_object = property_object

class PropertyTag:
    def __init__(self, name, keywords, property_tag_object):
        self.name = name
        self.keywords = keywords

        self.property_tag_object = property_tag_object