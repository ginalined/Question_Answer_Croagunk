import random

class YesNoAnswer:
    def __init__(self, sentence, question):
        self.sentence = sentence
        self.question = question
        self.answer = ""
    
    def yesno(self):
        answer = "Yes"

        # if NERS unmatching
        for ner in self.sentence.ents:
            if ner.text not in [w.text for w in self.question.words]:
                answer = "No"
        # if parts match with not
        for token in self.question.words:
            if token.text not in str(self.question.text) :
                if token.text.endswith("n't") or token.tect.endswith('not') or token.text.endswith('no'):
                    answer = "No"
        return answer

