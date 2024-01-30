import textrazor

API_KEY = "7dc81e78422b327f49826592c3ad15d4ada0f632f806c2b74b5b4757"

class TextrazorManager():
    def __init__(self, text):
        textrazor.api_key = API_KEY
        self.nlp = textrazor.TextRazor(extractors=["entities", "topics"])
        self.text = text

    def do_nlp(self):
        keywords = list()
        try:
            response = self.nlp.analyze(self.text)

            for entity in response.entities():
                keywords.append(entity.id)
        except textrazor.TextRazorAnalysisException as e:
            print("Error in Textrazor analysis!")
            print(e)
        
        return keywords