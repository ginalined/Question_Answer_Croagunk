from mimetypes import init
from stanfordcorenlp import StanfordCoreNLP
import sys
import nltk
nltk.download('punkt')


class ArticleAnalysis:
    def __init__(self, article):
        self.article = open(article).read()
        self.corenlp = StanfordCoreNLP('http://localhost', 9000)
    
    def word_tokenize(self, sentence):
        self.tokenizes = []
        for sentence in self.sentences:
            self.tokenizes.append(self.corenlp.word_tokenize(sentence))
        return self.tokenizes
    
    def ner(self):
        self.ners = []
        for sentence in self.sentences:
            self.ners.append(self.corenlp.ner(sentence))
        return self.ners
    
    def sentence_segmentation(self):
        self.sentences = nltk.sent_tokenize(self.article)
        return self.sentences
    
    def process(self):
        self.sentence_segmentation()
        self.ner()
        self.corenlp.close()
        return self.ners


if __name__ == '__main__':
    article = sys.argv[1]
    aa = ArticleAnalysis(article)
    aa.process()
    print("Sentence Segmentation: ", aa.sentences)
    print("NER: ", aa.ners)