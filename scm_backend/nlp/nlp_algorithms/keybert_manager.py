from keybert import KeyBERT

class KeybertManager():
    def __init__(self, text):
        self.nlp = KeyBERT()
        self.text = text

    def do_nlp(self):
        keyword_list = list()

        keywords = self.nlp.extract_keywords(self.text)
        for keyword in keywords:
            keyword_list.append(keyword[0])
        
        return keyword_list