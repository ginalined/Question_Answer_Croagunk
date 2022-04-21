class HowWhatWhyAnswer:
    def __init__(self, sentence, question):
        self.sentence = sentence
        self.question = question
        self.answer = ""

    def what(self):
        answers = []
        for ent in self.sentence.ents:
            if ent.text not in self.question.text:
                return ent.text
        return "what can't find answer"


    def how(self):
        for ent in self.sentence.ents:
            if ent.text not in self.question.text:
                return ent.text
        return "how can't find answer"

    def why(self):
        for ent in self.sentence.ents:
            if ent.text not in self.question.text:
                return ent.text
        return "why can't find answer"





