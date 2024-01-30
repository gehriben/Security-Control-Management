import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('punkt')

from rake_nltk import Rake

class RakeManager():
    def __init__(self, text):
        self.rake = Rake()
        self.text = text

    def do_nlp(self):
        # Extraction given the text.
        self.rake.extract_keywords_from_text(self.text)

        # To get keyword phrases ranked highest to lowest.
        keywords = self.rake.get_ranked_phrases()

        """for keyword in keywords:
            print(f"{keyword}")"""

        print(keywords)
        return keywords

        # To get keyword phrases ranked highest to lowest with scores.
        """keywords = self.rake.get_ranked_phrases_with_scores()
        for keyword in keywords:
            if keyword[0] > 2.5:
                print(f"{keyword[0]}: {keyword[1]}")"""