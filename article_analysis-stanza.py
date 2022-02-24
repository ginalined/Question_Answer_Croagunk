import sys
import stanza


class ArticleAnalysis:
    def __init__(self, article):
        self.article = open(article).read()
        # https://stanfordnlp.github.io/stanza/ner.html
        self.stanza = stanza.Pipeline(lang='en', processors='tokenize,ner,pos')
    
    def process(self):
        self.processed_article = self.stanza(self.article)
        return self.processed_article


if __name__ == '__main__':
    article = sys.argv[1]
    aa = ArticleAnalysis(article)
    aa.process()
    for sent in aa.processed_article.sentences:
        for ent in sent.ents:
            print(f'entity: {ent.text}\ttype: {ent.type}')

        # for word in sent.words:
        #     print(f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}')