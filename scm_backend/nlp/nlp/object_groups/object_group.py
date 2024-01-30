from abc import ABC, abstractmethod

class ObjectGroup(ABC):
    def __init__(self, parent_object):
        self.parent_object = parent_object
        self.child_objects = list()
    
    @abstractmethod
    def set_child_objects(self):
        pass

    def get_group_descriptions(self):
        descriptions = dict()
        descriptions[self.parent_object.name] = self.parent_object.name.lower() + "\n" + self.parent_object.description.lower()

        for child_object in self.child_objects:
            descriptions[child_object.name] = child_object.name.lower() + "\n" + child_object.description.lower()
        
        return descriptions
