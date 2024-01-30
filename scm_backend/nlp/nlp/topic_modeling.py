import gensim
import string

import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


class TopicModeling():
    def __init__(self, docs):
        self.docs = docs

    def do_lda_topic_modeling(self):
        self.docs = self.transform_keywords(self.docs)

        # Creating the term dictionary of our courpus, where every unique term is assigned an index. dictionary = corpora.Dictionary(doc_clean)
        dictionary = corpora.Dictionary(self.docs)
        # print(dictionary)

        # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in self.docs]
        # print(doc_term_matrix)

        # Creating the object for LDA model using gensim library
        Lda = gensim.models.ldamodel.LdaModel

        # Running and Trainign LDA model on the document term matrix.
        ldamodel = Lda(doc_term_matrix, num_topics=1, id2word = dictionary, passes=50)

        topic = ldamodel.show_topics(num_topics=1, num_words=3, formatted=False)[0][1][0][0]

        return topic

    def transform_keywords(self, keywords):
        keyword_list = list()

        for keyword in keywords:
            keyword_list.append([keyword])
        
        return keyword_list
    
    def word_weighting(self):
        word_tokens = dict()
        for keyword in self.docs:
            words = keyword.split(" ")
            for word in words:
                if word in word_tokens:
                    word_tokens[word] += 1
                else:
                    word_tokens[word] = 1
        
        word_tokens_sorted = dict(sorted(word_tokens.items(), key=lambda item: item[1], reverse=True))
        return list(word_tokens_sorted.keys())[0]




