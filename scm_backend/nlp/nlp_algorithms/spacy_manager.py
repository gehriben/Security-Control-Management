from ast import keyword
import spacy
import pytextrank
import pandas as pd

from collections import Counter
from string import punctuation

T_VALUE = 10

class SpacyManager():
    def __init__(self, text):
        self.nlp = spacy.load("en_core_web_sm")
        self.text = text

    def do_nlp(self):
        keywords = list()

        output = set(self.get_hotwords(self.text))
        most_common_list = Counter(output).most_common(T_VALUE)
        for item in most_common_list:
            keywords.append(item[0])

        keywords.extend(self.get_textrank(self.text))
        
        return keywords

    def get_hotwords(self, text):
        result = []
        pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
        doc = self.nlp(text.lower()) 
        for token in doc:
            if(token.text in self.nlp.Defaults.stop_words or token.text in punctuation):
                continue
            if(token.pos_ in pos_tag):
                result.append(token.text.lower())

        return result
    
    def get_textrank(self, text):
        # add PyTextRank to the spaCy pipeline
        self.nlp.add_pipe("textrank")
        doc = self.nlp(text)
        # examine the top-ranked phrases in the document
        keywords = list()
        for phrase in doc._.phrases[:T_VALUE]:
            keywords.append(phrase.text.lower())
        
        return keywords