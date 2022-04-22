class YesNoAnswer:
    def __init__(self, sentence, question):
        self.sentence = sentence
        self.question = question
        self.answer = ""

    def yesno(self):
        answer = "Yes"
        for ner in self.question.ents[1:]:
            if ner.text not in self.sentence.text:
                answer = "No"
                return answer

        for token in self.question.words:
            if token.text not in str(self.question.text):
                if token.text.endswith("n't") or token.tect.endswith('not') or token.text.endswith('no'):
                    answer = "No"
        return answer