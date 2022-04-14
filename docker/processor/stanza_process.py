import sys
import stanza
from nltk.tree import *
import logging
import spacy
from string import punctuation
nlp = spacy.load('en_core_web_sm')
stanza_logger = logging.getLogger('stanza')
stanza_logger.disabled = True

# xpos: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# con: http://surdeanu.cs.arizona.edu//mihai/teaching/ista555-fall13/readings/PennTreebankConstituents.html
class StanzaProcessor:
    def __init__(self, article=None, sentence=None):
        if article is not None:
            self.source = open(article).read()
        elif sentence is not None:
            self.source = sentence
        # https://stanfordnlp.github.io/stanza/ner.html
        self.stanza = stanza.Pipeline(lang='en', processors='tokenize,ner,pos,lemma,depparse,constituency')

    def process(self):
        self.source = self.pronoun_coref(self.source)
        self.processed_article = self.stanza(self.source)
        return self.processed_article
    
    # https://stackoverflow.com/questions/64284835/replace-personal-pronoun-with-previous-person-mentioned-noisy-coref
    def pronoun_coref(self, text):
        doc = nlp(text)
        pronouns = [(tok, tok.i) for tok in doc if (tok.tag_ == "PRP")]
        names = [(ent.text, ent[0].i) for ent in doc.ents if ent.label_ == 'PERSON']
        doc = [tok.text_with_ws for tok in doc]
        for p in pronouns:
            replace = max(filter(lambda x: x[1] < p[1], names),
                        key=lambda x: x[1], default=False)
            if replace:
                replace = replace[0]
                if doc[p[1] - 1] in punctuation:
                    replace = ' ' + replace
                if doc[p[1] + 1] not in punctuation:
                    replace = replace + ' '
                doc[p[1]] = replace
        doc = ''.join(doc)
        return doc

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
