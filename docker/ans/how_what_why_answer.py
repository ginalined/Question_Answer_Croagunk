class HowWhatWhyAnswer:
    def __init__(self, sentence, question):
        self.sentence = sentence
        self.question = question
        self.answer = ""

    def what(self):
        num = 0
        answer = ""
        for ent in self.sentence.ents:
            if ent.text not in self.question.text:
                num = num + 1
                answer = ent.text
        if num > 1:
            return self.question.text
        if num == 1:
            return answer
        return "what can't find answer"


    def how(self):
        num = 0
        answer = ""
        for ent in self.sentence.ents:
            if ent.text not in self.question.text:
                num = num + 1
                answer = ent.text
        if num > 1:
            return self.question.text
        if num == 1:
            return answer
        return "how can't find answer"

    def why(self):
        num = 0
        answer = ""
        for ent in self.sentence.ents:
            if ent.text not in self.question.text:
                num = num + 1
                answer = ent.text
        if num > 1:
            return self.question.text
        if num == 1:
            return answer
        return "why can't find answer"





