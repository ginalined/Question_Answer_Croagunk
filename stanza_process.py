import sys
import stanza
import nltk
from nltk.tree import *

# xpos: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# con: http://surdeanu.cs.arizona.edu//mihai/teaching/ista555-fall13/readings/PennTreebankConstituents.html
class StanzaProcessor:
    def __init__(self, article):
        self.article = open(article).read()
        # https://stanfordnlp.github.io/stanza/ner.html
        self.stanza = stanza.Pipeline(lang='en', processors='tokenize,ner,pos,lemma,depparse,constituency')
    
    def sentence_segmentation(self):
        self.sentences = nltk.sent_tokenize(self.article)
        return self.sentences
    
    def process(self):
        self.processed_article = self.stanza(self.article)
        return self.processed_article

    def print_con_parse(self):
        for sent in self.processed_article.sentences:
            print(sent.constituency)
            Tree.fromstring(str(sent.constituency)).pretty_print()
    
    def print_dep_parse(self):
        msg = ""
        for sent in self.processed_article.sentences:
            for word in sent.words:
                msg += 'id: '+ str(word.id) + '\tword: ' + word.text + '\thead id: ' + str(word.head)
                if word.head > 0:
                    msg += '\thead: ' + sent.words[word.head-1].text
                else:
                    msg += '\thead: root'
                msg+= '\tdeprel: ' + word.deprel
            msg+='\n'
        print(msg)
    
    def print_ent_parse(self):
        for sent in self.processed_article.sentences:
            for ent in sent.ents:
                print(f'entity: {ent.text}\ttype: {ent.type}')


if __name__ == '__main__':
    article = sys.argv[1]
    aa = StanzaProcessor(article)
    aa.process()
    aa.print_con_parse()