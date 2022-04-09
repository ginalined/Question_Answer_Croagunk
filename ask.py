import sys
from nltk_process import NLTKProcessor
import nltk
from question.question_generator import QuestionGenerator
from nltk.parse.stanford import StanfordDependencyParser
# https://stackoverflow.com/questions/7443330/how-do-i-do-dependency-parsing-in-nltk
path_to_jar = 'path_to/stanford-parser-full-2020-11-17/stanford-parser.jar'
path_to_models_jar = 'path_to/stanford-parser-full-2020-11-17/stanford-parser-4.2.0-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

class Ask:
    def __init__(self, article, n):
        self.n = n
        self.questions = dict()
        self.processor = NLTKProcessor(article)
        self.processor.process()
    
    def generate(self):
        self.process_ners()

    def process_ners(self):
        entities = [entity.text for entity in self.processor.ners.ents]
        self.entities = list(set(entities))
    
    def dep_parsing(self, sentence):
        return dependency_parser.raw_parse(sentence)
    
if __name__ == '__main__':
    article = sys.argv[1]
    n = sys.argv[2]
    ask = Ask(article, n)
    ask.generate()
    print("Entities:", ask.entities)