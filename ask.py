import sys
from nltk_process import NLTKProcessor
from stanza_process import StanzaProcessor
from nltk.parse import DependencyGraph
import nltk
from question.wh_question import WhQuestion
from question.yes_no_question import YesNoQuestion
# from nltk.parse.stanford import StanfordDependencyParser

# https://stackoverflow.com/questions/7443330/how-do-i-do-dependency-parsing-in-nltk
# path_to_jar = 'stanford-parser-full-2020-11-17/stanford-parser.jar'
# path_to_models_jar = 'stanford-parser-full-2020-11-17/stanford-parser-4.2.0-models.jar'

class Ask:
    def __init__(self, article, n):
        self.n = n
        self.questions = []
        #self.processor = NLTKProcessor(article)
        self.processor = StanzaProcessor(article)
        #self.parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
        self.processor.process()
    
    def generate(self):
        yesno = YesNoQuestion(self.processor.processed_article)
        yesno.ask()
        self.questions.extend(yesno.questions)
        count = 0
        for question in self.questions:
            if count < self.n:
                count += 1
                print(question)
        # wh = WhQuestion(self.processor.processed_article)
        # return self.questions

    # def build_dep_graphs(self):
    #     self.parses = dict()
    #     for sentence in self.processor.sentences:
    #         self.parses[sentence] = tuple(self.dep_parsing(sentence))
        
    
    # def dep_parsing(self, sentence):
    #     result = self.parser.raw_parse(sentence)
    #     return list(result)
    
if __name__ == '__main__':
    article = sys.argv[1]
    n = int(sys.argv[2])
    ask = Ask(article, n)
    ask.generate()

    # TO see the graph: 
    # dep_parsing = ask.dep_parsing("The quick brown fox jumps over the lazy dog.")

    # print(dep_parsing[0].to_dot())