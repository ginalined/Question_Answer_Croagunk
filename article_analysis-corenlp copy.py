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
    
    def pos_tag(self):
        self.poss = []
        for sentence in self.sentences:
            self.poss.append(self.corenlp.pos_tag(sentence))
        return self.poss
    
    def ner(self):
        self.ners = []
        for sentence in self.sentences:
            self.ners.append(self.corenlp.ner(sentence))
        return self.ners
    
    def sentence_segmentation(self):
        self.sentences = nltk.sent_tokenize(self.article)
        return self.sentences
    



if __name__ == '__main__':
    article = sys.argv[1]
    aa = ArticleAnalysis(article)
    aa.sentence_segmentation()
    print("1. Sentence Segmentation: ", aa.sentences)
    aa.ner()
    print("2. NER: ", aa.ners)
    aa.pos_tag()
    print("3. POS: ", aa.poss)

    aa.corenlp.close()