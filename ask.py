import sys
from nltk_process import NLTKProcessor
import nltk
from question.question_generator import QuestionGenerator

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
        
    
if __name__ == '__main__':
    article = sys.argv[1]
    n = sys.argv[2]
    ask = Ask(article, n)
    ask.generate()
    print("Entities:", ask.entities)