from nlp.nlp.object_groups.object_group import ObjectGroup

from controls.models import Control

class SecurityControlGroup(ObjectGroup):
    def __init__(self, parent_control):
        super().__init__(parent_control)
    
    def set_child_objects(self):
        self.child_objects = Control.objects.filter(parent_control=self.parent_object)

    def assign_tag(self, tag, security_control):
        if security_control == self.parent_object.name:
            self.parent_object.tags.add(tag)
            return
        
        for child_control in self.child_objects:
            if child_control.name == security_control:
                self.parent_object.tags.add(tag)
                child_control.tags.add(tag)
                return