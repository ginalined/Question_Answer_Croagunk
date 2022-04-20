import sys
import stanza
import nltk
from nltk.tree import *
import logging

stanza_logger = logging.getLogger("stanza")
stanza_logger.disabled = True

# xpos: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# con: http://surdeanu.cs.arizona.edu//mihai/teaching/ista555-fall13/readings/PennTreebankConstituents.html


class StanzaProcessor:
    def __init__(self, file=None, raw=None):
        if file is not None:
            self.article = open(file).read()
        elif raw is not None:
            self.article = raw
        # https://stanfordnlp.github.io/stanza/ner.html
        self.stanza = stanza.Pipeline(
            lang="en",
            processors="tokenize,ner,pos,lemma,mwt, depparse,constituency",
        )

    def sentence_segmentation(self):
        self.sentences = nltk.sent_tokenize(self.article)
        return self.sentences


    def process(self):
        
        def filter_not_sentence(sent):
            return sent and sent[-1] in "!?.,-"
        #because the sentece with no ending . has a large possibility to not be sentence. 
        self.article = "\n".join(list(filter(filter_not_sentence, self.article.split("\n"))))
       # self.article = [item for item in self.article.split("\n") if (item[-1] in "!?.,-") ]
        # self.article = "".join(
        #     "{}.\n".format(item)
        #     if (item and item[-1] not in "!?.,-")
        #     else "{}\n".format(item)
        #     for item in self.article.split("\n")
        # )
        
        self.sentences = self.sentence_segmentation()
        self.processed_article = []
        for sent in self.sentences:
            try:
                temp_nlp = self.stanza(sent)
                self.processed_article.append(temp_nlp)
            except:
                continue
        return self.processed_article

    def print_con_parse(self):
        for sent in self.processed_article.sentences:
            print(sent.constituency)
            Tree.fromstring(str(sent.constituency)).pretty_print()

    def print_dep_parse(self):
        msg = ""
        for sent in self.processed_article.sentences:
            for word in sent.words:
                msg += (
                    "id: "
                    + str(word.id)
                    + "\tword: "
                    + word.text
                    + "\thead id: "
                    + str(word.head)
                )
                if word.head > 0:
                    msg += "\thead: " + sent.words[word.head - 1].text
                else:
                    msg += "\thead: root"
                msg += "\tdeprel: " + word.deprel
            msg += "\n"
        print(msg)

    def print_ent_parse(self):
        for sent in self.processed_article.sentences:
            for ent in sent.ents:
                print(f"entity: {ent.text}\ttype: {ent.type}")


if __name__ == "__main__":
    file = sys.argv[1]
    aa = StanzaProcessor(file)
    aa.process()
    aa.print_con_parse()
