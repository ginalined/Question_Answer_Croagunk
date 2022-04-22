class YesNoAnswer:
    def __init__(self, sentence, question):
        self.sentence = sentence
        self.question = question
        self.answer = ""

    def yesno(self):
        answer = "Yes"
        if len(self.question.ents) <= 1:
            answer = "No"
            return answer
        for ner in self.question.ents[1:]:
            if ner.text not in self.sentence.text:
                answer = "No"
                return answer
        return answer