class Tag():
    def  __init__(self, name, description="", keywords=list(), tagged_objects = set()):
        self.name = name
        self.description = description
        self.keywords = keywords

        self.tagged_objects = tagged_objects
        self.tag_object = None
    
    def add_tagged_object(self, tagged_object):
        self.tagged_objects.add(tagged_object) 
    
    def add_keyword(self, keyword):
        self.keywords.append(keyword)
    
    def set_tag_object(self, tag_object):
        self.tag_object = tag_object


