import yake

class YakeManager():
    def __init__(self, text):
        self.nlp = yake.KeywordExtractor()
        self.text = text

    def do_nlp(self):
        keywords_list = list()
        keywords = self.nlp.extract_keywords(self.text)

        for keyword in keywords:
            keywords_list.append(keyword[0])

        return keywords_list