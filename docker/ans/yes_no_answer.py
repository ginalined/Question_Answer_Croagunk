import random

class YesNoAnswer:
    def __init__(self, sentence, question):
        self.sentence = sentence
        self.question = question
        self.answer = ""
    
    def answer(self):
        # for testing
        # return str(bool(random.getrandbits(1)))
        answer = "Yes"
        # if NERS unmatching
        for ner in self.sentence.ners:
            if ner.text not in self.question:
                answer = "No"
        # if parts match with not
        for token in self.question.words:
            if token.text not in str(self.question.text) :
                if token.text.endswith("n't") or token.tect.endswith('not') or token.text.endswith('no'):
                    answer = "No"
        return answer

    
    def rank(self):
        """
            TODO: there could be multiple potential answers
            we should rank them and select the best.
            Note that # of answers must equal to # of questions.
            # this type of question might not happen this problem.
        """