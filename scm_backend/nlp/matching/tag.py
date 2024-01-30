class Tag():
    def __init__(self, name, keywords, tag_object=None):
        self.name = name
        self.keywords = keywords
        
        self.tag_object = tag_object
        self.assigned_controls = None
    
    def set_assigned_controls(self):
        if self.tag_object is not None:
            self.assigned_controls = self.tag_object.control_set.all()
        else:
            raise Exception("No tag_object set!")
    
    def get_assigned_controls(self):
        control_list = list()
        for assigned_control in self.assigned_controls:
            control_json = dict()
            control_json["pk"] = assigned_control.pk
            control_json["cn"] = assigned_control.cn
            control_json["name"] = assigned_control.name
            control_json["description"] = assigned_control.description

            if assigned_control.parent_control is not None:
                control_json["parent_control_id"] = assigned_control.parent_control.pk
            else:
                control_json["parent_control_id"] = None 

            control_list.append(control_json)
        
        return control_list
