from question.wh_question import WhQuestion
from question.yes_no_question import YesNoQuestion
from nltk.parse.corenlp import CoreNLPDependencyParser
dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')

class QuestionGenerator:
    def __init__(self):
        return
        