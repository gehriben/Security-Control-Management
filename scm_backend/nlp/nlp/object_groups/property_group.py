from nlp.nlp.object_groups.object_group import ObjectGroup

from properties.models import Property
class PropertyGroup(ObjectGroup):
    def __init__(self, parent_control):
        super().__init__(parent_control)
    
    def set_child_objects(self):
        self.child_objects = Property.objects.filter(parent_property=self.parent_object)

    def assign_tag(self, tag, property):
        if property == self.parent_object.name:
            self.parent_object.property_tags.add(tag)
            return
        
        for child_property in self.child_objects:
            if child_property.name == property:
                self.parent_object.property_tags.add(tag)
                child_property.property_tags.add(tag)

                return