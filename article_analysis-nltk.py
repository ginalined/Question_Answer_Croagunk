from stanfordcorenlp import StanfordCoreNLP
import sys
import nltk
nltk.download('punkt')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
from nltk.chunk import tree2conlltags


class ArticleAnalysis:
    def __init__(self, article):
        self.article = open(article).read()
    
    def sentence_segmentation(self):
        self.sentences = nltk.sent_tokenize(self.article)
        return self.sentences
    
    def word_tokenize(self):
        self.tokenizes = []
        for sentence in self.sentences:
            self.tokenizes.append(nltk.word_tokenize(sentence))
        return self.tokenizes
    
    def pos_tag(self):
        self.poss = []
        for sentence in self.tokenizes:
            self.poss.append(nltk.pos_tag(sentence))
        return self.poss
    
    def ner(self):
        # https://stackoverflow.com/questions/31836058/nltk-named-entity-recognition-to-a-python-list
        self.ners = []
        for sentence in self.poss:
            self.ners.append(nltk.ne_chunk(sentence))
        return self.ners
    
    def process(self):
        self.sentence_segmentation()
        self.word_tokenize()
        self.pos_tag()
        self.ner()


if __name__ == '__main__':
    article = sys.argv[1]
    aa = ArticleAnalysis(article)
    aa.process()
    print("1. Sentence Segmentation: ", aa.sentences)
    print("2. Word Tokenization: ", aa.tokenizes)
    print("3. POS: ", aa.poss)
    print("4. NER: ")
    for sentence in aa.ners:
        print(tree2conlltags(sentence))