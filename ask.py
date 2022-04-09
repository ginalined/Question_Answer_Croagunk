import sys
from stanza_process import StanzaProcessor
from question.wh_question import WhQuestion
from question.yes_no_question import YesNoQuestion

class Ask:
    def __init__(self, article, n):
        self.n = n
        self.questions = []
        self.processor = StanzaProcessor(article)
        self.processor.process()
    
    def generate(self):
        yesno = YesNoQuestion(self.processor.processed_article)
        wh = WhQuestion(self.processor.processed_article)
        yesno.ask()
        wh.ask()
        self.questions.extend(yesno.questions)
        self.questions.extend(wh.questions)

        self.rank_questions()

        count = 0
        for question in self.questions:
            if count < self.n:
                count += 1
                print(question)
    
    def rank_questions(self):
        # TODO: rank questions before printing
        return
    
if __name__ == '__main__':
    article = sys.argv[1]
    n = int(sys.argv[2])
    ask = Ask(article, n)
    ask.generate()